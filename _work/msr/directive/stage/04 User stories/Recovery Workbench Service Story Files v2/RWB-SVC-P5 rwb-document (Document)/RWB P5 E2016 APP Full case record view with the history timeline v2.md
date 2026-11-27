# RWB-P5-E2016-APP Full case record view with the history timeline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP19 |
| Parallel lane | L-P5-V |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2016-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-WKM-008, REQ-OCC-008, REQ-CWC-016, REQ-DRI-002, REQ-WKM-014) |
| Size | Fits two weeks (the squad confirms the size at refinement) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-016 for rwb-document. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E2016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 9 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the documents of my case, with their stored date, type, actor and version history, to appear on the case timeline and in the documents section of the record view**, so that **I read what was attached, when and by whom without leaving the case**.

### 2. Business rationale

A case lives for months or years and passes through several teams, partners and courts. The record view is the place where a new owner learns what happened, and the documents are the part of it that proves the facts: the court notice, the appraisal report, the title deed, the settlement agreement. The legacy story puts every action, decision, transfer, letter and document of a case on one timeline with type and date filters, and its measure is that a case history with 30 events reads in under 2 seconds (NFR-009) and stays under 2 seconds at the 2031 data size (NFR-070).

This story is the rwb-document part of legacy key RWB-E2-016. The timeline endpoint, the merge, the ordering, the paging, the queue history and all twelve legacy criteria are rwb-case's, in RWB-P3-E2016-APP and its contract RWB-P3-E2016-CON; the notice items are rwb-comms' and the decision items are rwb-decision's. What this slice owns is the document item source: for a case and a date window, rwb-document returns the document items with their timestamp, their type label, a summary built from codes, the actor and the document reference, plus the version count and the version history of each document, inside the 2 second budget the gateway gives it, masked by role and filtered by scope, and it opens the document detail behind an item. The document store itself — the file, the container, the version chain and the write path — is RWB-P5-E1024-APP; this story reads it and adds no write.

In the monolith the case timeline called `DocumentQuery.forCase(...)` inside the case module. In the target that in-process call is a REST call on the owner's base (DP-11): `rwb.document` under `/api/recovery/document/v1` (DP-13) instead of the shared base, one hop from rwb-case, a 2 s timeout and a breaker per downstream, and one GET retry with jitter as slide 11 of Architecture v5 fixes for every call. Architecture v5 slide 10 is explicit that the Documents tab loads on click from rwb-document, one hop, inside the 2 s target, that screens never chain calls, and that the gateway asks each owner directly and only for what is on screen; the case timeline therefore reads the document items directly from this service and never through a second service. The page size and the item cap are parameters instead of configuration in code (DP-06), the type labels are data rows with a version in force (DP-07), and the screen is composed at the edge by gateway-bff (DP-19). The service owns the topic `rwb.document.events.v1` and publishes nothing to it in this story (DP-14): the timeline is pulled, not pushed.

Three values of this slice are not settled by the sources and are carried as register rows, because the sources give the document read for the Documents tab and not yet for the timeline shape: the contract shape rwb-case and rwb-document share for the case timeline, which is the operation name, the window parameters and the item field names (GAP-1059; ASM-2007); whether the version count travels on the item or only on the document detail (GAP-1060; ASM-2008); the summary wording of a document item (GAP-1061; ASM-2009); and which table supplies the type label the item shows, because the document type table is rwb-document's own reference data while DP-07 sends lists through rwb-case (GAP-1062; ASM-2010). The story builds on Day 1 against the RWB-P3-E2016-CON fake and is proven end to end by RWB-ITG-E2016-ITG.

### 3. Preconditions

- RWB-P3-E2016-CON is published: the timeline operation of rwb-case, the `TimelinePage` and `TimelineItem` components with `at`, `type`, `summary`, `by`, `reference` and the seven type values including DOCUMENT, the error mapping and the fakes of the consumed contracts, so this story knows the shape its items must fit. The operation that rwb-case calls on rwb-document is API-P5-002 on base `/api/recovery/document/v1`, with the window carried as `from` and `to`, inclusive, and the items carrying `at`, `type`, `summary`, `by`, `reference` and `doc_version`; the names are fixed at the RWB-P3-E2016-CON baseline review, and both sides build against the fake until then (GAP-1059).
- The `rwb_document` baseline is in place: `document`, `document_field`, `document_custody`, `document_type`, `case_document_check`, `document_hub_parameter`, `document_intake`, `document_text` and `retention_action` exist at the platform migration version (TSD P5 T3.1), and the local decision-record table is created by the decision-record library (DP-03).
- The documents of the case exist and are `STORED`: they are written by RWB-P5-E1024-APP (the store, the version chain and the metadata) and by the intake stories of the same service; a document whose state is `COPY_PENDING` is a document whose content read answers 503 while its metadata already lists (FSD P5 AC-EXC-P5-002-03).
- The `document_type` table version in force is the one the stored documents were typed against, so a type code always resolves to a label; the label row a document of an older type table version shows is Not specified in the source documents (GAP-1062; ASM-2010).
- The parameters exist as rows: the page size, its bounds and the item cap of the document item list, read through the parameters contract of rwb-case and its client library (DP-06), and the same row held in `document_hub_parameter` where TSD P5 places it (DF-REF-244 to DF-REF-251).
- The role of the caller is resolved by rwb-access: the authorise answer carries the scope over the case and the letters of the capability area DOCUMENTS, cached by the guard library (DP-08), and a refusal is MSG-P4-002 or MSG-P4-003 and never an empty list.
- The case facts needed for the scope test come one hop from rwb-case through the case read of RWB-P3-E2016-CON; this service holds no copy of a `rwb_case` row (DP-01).
- The login is the rwb-document login (DP-02), one per service, and the schema is `rwb_document`.
- The browser never calls this service directly: every call arrives from rwb-case or through the gateway-bff composite route (DP-19).

### 4. Flow

1. The case owner opens SCR-04 Case timeline from SCR-03 Case record. The browser calls the gateway-bff composite route and never an owner service directly (DP-19).
2. rwb-case decides the item types the caller may read and calls the case-scoped document read of this service once, with the case ID, the date window of the filter and the page parameters; the call is one hop, with the 2 s timeout of the case contract, a breaker per downstream and one GET retry with jitter (DP-11).
3. rwb-document receives the call on base `/api/recovery/document/v1` (DP-13) and validates the request before any row is read: `to` not before `from` (422, MSG-GEN-003), a page size outside the bounds (422, MSG-GEN-002), a case ID that is not a UUID (422).
4. ScopeGuard asks the guard library for the caller's rights: Documents R over the case, and the scope of the caller's roles. The guard library answers from the cached authorise data of rwb-access; a missing Documents R is a 403 with MSG-P4-002 and a case outside the scope is a 404 with MSG-P4-003.
5. For the scope test the scope facts of the case are read one hop from rwb-case through the case read of RWB-P3-E2016-CON; no `rwb_case` column is read and no scope copy is kept in `rwb_document`.
6. DocumentItemReader reads `document` for the case and the window — the stored date from the standard record column `created_at`, the type code, the actor, the document ID and `doc_version` — newest first, with the source sequence kept on a tie, within the page size and the item cap of the parameters.
7. DocumentItemMapper maps each row to one document item of the timeline: `at` (the stored date), `type` "DOCUMENT", `summary` (built from the type label and the version count, never from a free text), `by` (the actor of the document) and `reference` (the document ID), and attaches the version count of the document.
8. DocumentVersionReader walks the version chain of each document in the page by `previous_version_id` and returns, per version, the version number, the stored date, the actor and `content_sha256`; a document with one version returns one entry and a document with three versions returns three, the current version last.
9. The masking path applies the role mask to every field that carries a personal value before the answer leaves the service; no personal value, no storage reference and no document text is part of a document item.
10. The answer returns 200 with the page of items, `page`, `size` and `total`; on a document store that does not answer inside the budget the answer is a 503 with MSG-GEN-006 naming "Document hub", which rwb-case turns into the partial timeline of the legacy exception path X1 and never into a failed case read.
11. The case owner opens a document item; the front end follows the item `reference` to `GET /api/recovery/document/v1/documents/{documentId}` and reads the document detail: the metadata, the current `doc_version`, the version history with the hash of each version and the extracted fields, masked by role; the owner then downloads the content through `GET /api/recovery/document/v1/documents/{documentId}/content`.
12. The documents section of SCR-03 asks the same case-scoped read with the date window of the section and shows the same items; a filter by type or date reloads it in state Filtered, and no read of this story writes a row, a decision record or an event.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | rwb-document does not answer inside the 2 second budget, or its breaker at rwb-case is open | The case timeline shows the 25 items of the other sources and names the missing source; the case read itself does not fail | MSG-GEN-006 | AC5 |
| X2 | The caller's role holds no Documents R | The service answers 403 and rwb-case leaves the document items out without an error; the other item types are unaffected | MSG-P4-002 | AC4 |
| X3 | The case is unknown, or outside the caller's scope | The service answers 404 before any document row is read; nothing is returned and nothing is written | MSG-P4-003 | AC6 |
| X4 | `to` is before `from` | Refused before any row is read, with both field names | MSG-GEN-003 | AC7 |
| X5 | The page size is outside the API bounds, or not an integer | Refused before any row is read, with the field and its bounds | MSG-GEN-002 | AC7 |
| X6 | The document store does not answer, or its read times out | 503 with the display name of this service, so the caller shows the partial timeline; the retry is one GET with jitter | MSG-GEN-006 | AC5 |
| X7 | A document of the page is in state `COPY_PENDING` | The item still shows with its metadata and its stored date; the content read of that document answers 503 with MSG-GEN-006 naming "Document storage" | MSG-GEN-006 | AC1 |
| X8 | A document row of the case carries a type code with no label row in the version in force | The item shows with the type code itself and the case read continues; no item is dropped and no row is guessed | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-P3-E2016-CON fake; the documents it reads are written by RWB-P5-E1024-APP and the rights come from the published rwb-access contract, so no team waits for another team's release |
| Negotiable | The summary wording, the window parameter names and the position of the version count can change; the items, the ordering, the budget and the rights are fixed |
| Valuable | The part of the case history that proves the facts reads from one owner, inside the 2 second wait, with no schema read across services |
| Estimable | One case-scoped read, one item mapper, one version reader, one scope guard, one controller and one screen component |
| Small | Fits one iteration with its tests, as a secondary slice of the legacy key |
| Testable | Component tests over seeded `rwb_document` rows, contract tests against the RWB-P3-E2016-CON fake and one timed run at the 95th percentile over 20 runs |

### 7. Acceptance criteria

```gherkin
Feature: Full case record view with the history timeline — the rwb-document items

  Background:
    Given the business date is 2026-12-20
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000601"
    Given the rwb-case contract mock returns case "RW-2026-000601" of team "MTG-BKK" in the scope of "U-CO-01"
    Given the rwb-access contract mock returns Documents R for "U-CO-01" over case "RW-2026-000601"
    Given the rwb-decision contract mock returns the 6 decision log entries of case "RW-2026-000601" with the same values, all kept
    Given the schema "rwb_document" holds the 5 documents of case "RW-2026-000601"

  Scenario: AC1 The document items of a case (new, D-RCV-60)
    Given case "RW-2026-000601" has 30 events: 4 assignments, 3 transfers, 8 contacts, 6 decision log entries, 2 notices, 5 documents and 2 timer events
    Given the 5 documents of case "RW-2026-000601" are stored between 2026-11-30 and 2026-12-18
    When rwb-case calls the document items of case "RW-2026-000601" for the window 2026-11-30 to 2026-12-20
    Then rwb-document returns 5 items newest first
    And each item carries "at" as the stored date, type "DOCUMENT", a summary of the English label of the document type followed by the version count, built from data rows only, "by" as the actor and "reference" as the document ID
    And each item carries the version count of its document
    And no item carries a person name, an account number, an identity number, a storage reference or document text

  Scenario: AC2 A document with three versions keeps its history (new, D-RCV-60)
    Given document "DOC-0601" of case "RW-2026-000601" has 3 versions stored on 2026-11-30, 2026-12-05 and 2026-12-08
    When rwb-document answers the document items of case "RW-2026-000601"
    Then the item of "DOC-0601" carries doc_version 3
    And the version history of that document lists version 1, version 2 and version 3, each with its stored date, its actor and its content_sha256
    When the caller follows the item reference to GET /api/recovery/document/v1/documents/{documentId}
    Then the answer carries the metadata, doc_version 3, the 3 versions and the extracted fields of the document
    And no version of the document replaces another, and the superseded versions are still readable

  Scenario: AC3 The date filter includes both ends (new, D-RCV-60)
    Given case "RW-2026-000601" holds documents stored on 2026-11-30, 2026-12-05, 2026-12-08, 2026-12-12 and 2026-12-18
    When rwb-case asks for the document items from 2026-12-05 to 2026-12-08
    Then exactly the documents stored on 2026-12-05 and on 2026-12-08 are returned, newest first
    And the document stored on 2026-11-30 and the two stored on 2026-12-12 and 2026-12-18 are not returned
    And the end date 2026-12-08 is included whole, to its last second

  Scenario: AC4 Only a role with Documents R sees the document items (new, D-RCV-60)
    Given user "U-PC-01" holds RW-PHONECOL with case "RW-2026-000601" in scope
    Given the rwb-access contract mock returns Case record R and Documents R for "RW-PHONECOL", all kept
    When "U-PC-01" opens the case timeline
    Then the 5 document items of the case show
    Given a caller whose role holds Case record R and no Documents R with the case in scope
    When rwb-case asks for the document items of case "RW-2026-000601"
    Then rwb-document answers 403 with MSG-P4-002 for action "open the documents of the case"
    And rwb-case answers no document item and its other 25 items are unaffected

  Scenario: AC5 The answer stays inside the 2 second budget, and a late answer is a partial timeline (new, D-RCV-60)
    Given case "RW-2026-000601" holds 30 documents stored between 2026-11-30 and 2026-12-18
    When rwb-case asks for the document items of the case 20 times
    Then every answer arrives within the 2 second budget at the 95th percentile
    And the first page of document items of case "RW-2026-000604", whose timeline holds 4,000 items, at page size 50 arrives inside the same budget
    Given rwb-document does not answer within 2 seconds
    When rwb-case asks for the 30 items of case "RW-2026-000601"
    Then the 25 items of the other sources show and no document item shows
    And the notice names MSG-GEN-006 with "Document hub"
    And no partial page of document items is shown as if it were the whole page

  Scenario: AC6 A case outside the caller's scope is not found (new, D-RCV-60)
    Given case "RW-2026-000603" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    Given the rwb-case contract mock returns no scope for "U-CO-01" over case "RW-2026-000603", all kept
    When rwb-case asks for the document items of case "RW-2026-000603"
    Then rwb-document answers 404 with MSG-P4-003
    And no document row of that case is read and no item is returned
    And the scope is taken from the one-hop rwb-case case read, not from a copy in "rwb_document"

  Scenario: AC7 The window and the page size are validated before any read (new, D-RCV-60)
    When rwb-case asks for the document items from 2026-12-10 to 2026-12-01
    Then the request is refused with 422 and MSG-GEN-003 naming "to" and "from"
    And no document row is read
    When rwb-case asks for the document items with a page size outside the API bounds
    Then the request is refused with 422 and MSG-GEN-002 naming the field with its bounds
    And the read writes nothing: no document row, no field row, no version, no decision record and no event
    And no document of another case is returned for case "RW-2026-000601", whether or not that case is in the caller's scope
```

The seven criteria above are new and test only this slice: the document items of the case, their stored date, their type label, their summary, their actor and their reference, their version count and version history, the inclusive window, the role and scope filter, the 2 second budget and the partial answer, and the parameter validation. The twelve legacy criteria of RWB-E2-016 are rwb-case's and are carried by RWB-P3-E2016-APP; no legacy criterion text is copied into this section, and only the source values of the legacy story are reused: case "RW-2026-000601", its 5 documents among 30 events, user "U-CO-01" holding RW-CASEOWN, user "U-PC-01" holding RW-PHONECOL, the window 2026-12-05 to 2026-12-08, the wrong order 2026-12-10 to 2026-12-01, case "RW-2026-000603" of team "SME-NTH", the 4,000 item case "RW-2026-000604" at page size 50 and the 2 second budget.

Scenario: AC8 A document read takes its rows from rwb_document only and the case facts one hop from rwb-case; no rwb_case column is read (new, D-RCV-60)
Scenario: AC9 The document type label and the list values come from data rows with the version in force, and no label is written in code (new, D-RCV-60)
Scenario: AC10 A document not visible in the caller's scope is absent from the answer, never a redacted item and never a count that reveals it (new, D-RCV-60)
Scenario: AC11 The page size and the item cap are read from parameters, and a case of 4,000 items returns one page of document items inside the 2 second budget (new, D-RCV-60)
Scenario: AC12 BR9, BR11 and BR13 are proved by the boundary test over the read path and the data rows, not per request (new, D-RCV-60)
Scenario: AC13 A call of a provided operation without a valid caller is answered 401 (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The timeline holds every document of the case (legacy BR1, the document part): a document stored on the case appears as one document item in its window, and a superseded version appears inside that item's history, never as a second item | REQ-WKM-008; casemodel.txt Case file; legacy BR1 |
| BR2 | Items are returned newest first from the stored date; two documents stored at the same instant keep the order of their source sequence, so the same query returns the same page | events.txt Rules (ordering); legacy BR2 |
| BR3 | A document item shows only to a role with Documents R; the list is filtered by the role's letters and by its scope, and masking by role applies to every field that carries a personal value (CTL-11, DL26) | roles.txt Permissions; CTL-09; CTL-11; DL26; legacy BR3 |
| BR6 | Personal data in a summary is masked by role, and a document item never carries a person name, an account number, an identity number, a storage reference or document text | CTL-11; DL26; legacy BR6 |
| BR7 | A source that does not answer in time does not stop the timeline: this service answers a 503 with MSG-GEN-006 and the caller shows the other items | NFR-008; legacy BR7 |
| BR8 | Every call is one hop with a 2 s timeout and a breaker per downstream, and a GET is retried once with jitter; no call chains and no call reads a downstream of a downstream | Architecture v5 slides 10 and 11; DP-11 |
| BR9 | The service reads only `rwb_document` and its own ACE attachments; no `rwb_case` column is read, and the case facts arrive one hop through the rwb-case contract | Architecture v5 slide 13; DP-01 |
| BR10 | The page size, its bounds and the item cap are parameters, and the number of items one answer may carry is the parameter value, never a constant | Template and Rules §R5.5 DP-06 |
| BR11 | The document type label and the list values are data rows with a version in force; no type code, label or list value is written in code | TSD P5 T3.1, T3.2; DP-07 |
| BR12 | The read writes nothing: no document row, no field row, no version, no custody row, no decision record, no access-log row of this service and no event | Legacy solution plan; Template and Rules §R7.2 s17 |
| BR13 | A document that is not visible in the caller's scope is absent from the answer, never a redacted item and never a count that reveals it | CTL-11; Architecture v5 slide 10 |

### 9. State transitions

None. This story changes no document state and no case state; it reads records only, writes no row, raises no event and starts no workflow. The document states below are read-only facts that an item or its detail may show.

| From | Event | Condition | To |
|---|---|---|---|
| — | — | — | None: this story performs no transition |

| State it may show | Written by | Appears as |
|---|---|---|
| `COPY_PENDING` | RWB-P5-E1024-APP, when the storage copy of a stored document has not completed | A document item with its metadata and stored date, and a content read that answers 503 with MSG-GEN-006 naming "Document storage" |
| `STORED` | RWB-P5-E1024-APP, once the file is in its container | A document item whose content read returns the file, and a version entry in the history |
| `SUPERSEDED` | RWB-P5-E1024-APP, when a further version of the same document is stored | A version entry in the history of the item; the superseded version is still readable and never replaces the current one |

The states above are the values of `state` on `document` as TSD P5 T3.0 and the store story define them; this story reads them and never sets one. A review status (`LOV-REVIEW`) and a retention class are shown on the detail, not on the item.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the timeline and queue history (Case record R; Decision log R; Documents R; Litigation R), so every document item of the case shows |
| RW-TEAMMGR, team manager | Reads the timeline and queue history (Case record R; Decision log R); document items show only if the role also holds Documents R |
| RW-PHONECOL, phone collector | Reads the timeline without decisions and notices (Case record R; Documents R), so the document items show |
| RW-CONDUCT, conduct and QA officer | Reads every item (R in all areas), so the document items show |
| RW-AUDIT, internal audit | Reads every item (R in all areas); changes nothing |
| rwb-document service identity (the rwb-document login, DP-02) | Serves the case-scoped document read, the document detail and the content, applies the role filter and the mask, and writes nothing |
| rwb-case (the caller) | Asks for the document items of one case and one window, one hop, and merges them with its own items; it holds no copy of a document row |
| gateway-bff (the platform edge) | Calls each owner directly for what is on screen and merges the answers; the browser never calls rwb-document (DP-19) |

A decision item needs Decision log R, a document item needs Documents R and a notice item needs Litigation R (legacy BR3). rwb-access decides every one of those letters and the scope (DP-08) and answers a refusal with MSG-P4-002 for a missing letter and MSG-P4-003 for a case outside the scope; this service holds no role, letter, scope or masking rule of its own and grants nothing.

### 11. Data

| BR Field ID | Entity in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id — the item reference | Read |
| DF-DOC-002 | document | case_id — the filter of the read | Read |
| DF-DOC-004 | document | document_type — the code the summary label resolves from | Read |
| DF-DOC-005 | document | source — shown on the detail and used for the summary where the type label is absent | Read |
| DF-DOC-009 | document | retention_class — shown on the detail, never on the item | Read |
| DF-DOC-011 | document | doc_version — the version count of the item | Read |
| DF-DOC-025 | document | previous_version_id — the chain the version history walks | Read |
| DF-DOC-026 | document | content_sha256 — the hash of each version in the history | Read |
| DF-DOC-027 | document | captured_at — the capture time, shown on the detail and not used as the item date | Read |
| DF-REF-219 | document_type | doc_type_code — the code a stored document carries | Read |
| DF-REF-220 | document_type | label_en — the English label the summary is built from | Read |
| DF-REF-221 | document_type | label_th — the Thai label of the same row | Read |
| DF-CAS-001 | case (owner rwb-case) | id — the case of the request and of the scope answer | Read only through the rwb-case contract, one hop |
| DF-CAS-011 | case (owner rwb-case) | team_code — the team the scope test compares | Read only through the rwb-case contract, one hop |
| DF-REF-244 to DF-REF-251 | document_hub_parameter | `param_code`, `param_value`, `table_version`, `valid_from`, `valid_to` — the page size, its bounds and the item cap | Read |
| Standard record columns | document | created_at (the stored date of the item), created_by (the actor), state | Read |

No `rwb_case` column is read by this story: `DF-CAS-001` and `DF-CAS-011` arrive in the answer of the rwb-case case read, and the two columns are named here only to say which fact the scope test needs. No `document_text` row, no `document_intake` row and no `document_custody` row is read by the item list; the content of API-P5-004 is streamed from the Blob container of the store story and is never loaded into a table by this service. Field IDs are those in the Logical Data Model and Data Dictionary v9 and TSD P5 T3.1.

### 12. Contract

Contract version fixed: v1, base `/api/recovery/document/v1` (API-P5-002).

#### 12.1 REST operations provided

Base `/api/recovery/document/v1`; owner rwb-document (P5). This slice adds no path: it serves the read operations of TSD P5 appendix T-A behind the case timeline and the documents section, and the write side (upload, store, new version, field review, custody, generation) stays with RWB-P5-E1024-APP and the other P5 stories.

| API | Method | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| API-P5-002 | GET | `/cases/{caseId}/documents` | Path `caseId`; query `type`, `page`, `size` (TSD P5 T-A.2) and the date window `from` and `to`, inclusive (GAP-1059) | 200 `DocumentPage`: the documents of the case in the window, newest first, each with `at`, `type` "DOCUMENT", `summary`, `by`, `reference` and `doc_version`, plus `page`, `size` and `total`; the item fields are `at`, `type`, `summary`, `by`, `reference` and `doc_version` (GAP-1059); the summary template is Not specified in the source documents (GAP-1060, GAP-1061; ASM-2008, ASM-2009) | 401 no session (MSG-P4-001); 403 no Documents R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 422 `to` before `from` (MSG-GEN-003) or a page size outside the bounds (MSG-GEN-002); 503 the document store is down (MSG-GEN-006) | Documents, right R, scope applied; each service authorises the object itself (Architecture v5 slide 10) | Not applicable: the call writes nothing |
| API-P5-003 | GET | `/documents/{documentId}` | Path `documentId` | 200 `Document`: the metadata, the current `doc_version`, the version history (version, stored date, actor, `content_sha256` per version) and the extracted fields of `document_field`, masked by role | 401 (MSG-P4-001); 403 no Documents R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 503 the store is down (MSG-GEN-006) | Documents, right R, scope applied | Not applicable |
| API-P5-004 | GET | `/documents/{documentId}/content` | Path `documentId` | 200 the file of the version as `application/octet-stream`; 503 while the state is `COPY_PENDING` (FSD P5 AC-EXC-P5-002-03) | 401 (MSG-P4-001); 403 no Documents R (MSG-P4-002); 404 unknown or out of scope (MSG-P4-003); 503 (MSG-GEN-006 naming "Document storage") | Documents, right R, scope applied | Not applicable |

The operation that rwb-case calls for the timeline is Not specified in the source documents (GAP-1059; ASM-2007): no source names a case-timeline operation of this service, and TSD P5 T-A.2 gives API-P5-002 the query `type`, `page` and `size` with no date window, while RWB-P3-E2016-CON consumes "the document metadata of a case in the date range". This story therefore serves the case-scoped document read on API-P5-002, carries the window as two date parameters, and builds the case timeline use against the RWB-P3-E2016-CON fake until the baseline review fixes the names on both sides. No path is invented and no response field of TSD P5 T-A.2 is removed.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case exists, its team and its scope answer, for the 404 test of AC6; one hop, no copy kept. The answer field names are Not specified in the source documents (GAP-1059; ASM-2007) | One hop, 2 s, breaker, one GET retry with jitter |
| — | RWB-P3-E2016-CON, the timeline contract of rwb-case | rwb-case (P3) | The shape of the document item this service returns and the operation name rwb-case calls; both sides fake it on Day 1; the name and the field names are Not specified in the source documents (GAP-1059; ASM-2007) | One hop, 2 s, breaker |

The access check is not a contract dependency of this story: it is the cached authorise call of the guard library that every service makes (DP-08), answered by the published contract of rwb-access, and it caches for the request. No other service is called: this story never calls rwb-decision, rwb-comms, rwb-source-data or the gateway, and it never calls a downstream of a downstream (DP-11).

#### 12.3 Events published

None. The timeline is pulled, not pushed: this read writes no row, so it has no outbox row and publishes nothing. The service owns `rwb.document.events.v1` (DP-14) and publishes `DocumentStored` and `DocumentFieldsExtracted` on it from the store and extraction stories; this story adds no event, and the two events are consumed by rwb-case and rwb-agent for their own projections (Architecture v5 slide 42), never by this read.

#### 12.4 Events consumed

None. This service is the producer of the document events, not a consumer of them: it answers from its own `rwb_document` rows at the moment of the request, so an item is never a projection and never stale. `DocumentFieldsExtracted` is used inside the service by the extraction path, not by this story, and no consumer group is created here.

#### 12.5 Workflows and activities

None. The case-scoped read, the detail and the content are synchronous REST calls inside the request and inside the 2 second budget; this story starts no workflow, adds no activity and holds no timer. The `DocumentIntakeWorkflow` of the store and extraction stories owns the writes, and this story reads what those activities have already committed.

#### 12.6 Schedules

None. The retention Schedule of this service belongs to the retention story, and the document intake Schedule to the intake story (TSD P5 T5.3, Architecture v5 slide 44); a read needs no Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| document | P5 (`rwb_document`) | The document item: ID, case, type, source, version, hash, capture time and the standard record columns |
| document_type | P5 (`rwb_document`) | The type code and the labels a summary is built from, at the version in force |
| document_field | P5 (`rwb_document`) | The extracted fields of a document, shown on the detail only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_document` | Present in the schema; this story writes none of them |
| document_custody, case_document_check, document_intake, document_text, retention_action, document_hub_parameter | P5 (`rwb_document`) | Same service; this story reads `document_hub_parameter` only, and the other tables belong to their own stories |

`recovery_case`, `assignment`, `queue` and `timer` are rwb-case's tables and are read only through its contract (DP-01). No table of another service is named in a query of this story and no foreign key crosses a schema; `document.case_id` and `document.previous_version_id` are references by value, as TSD P5 T3.3 records them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P3-E2016-CON fake | The timeline shape and the operation rwb-case calls | A page of `TimelineItem` with the seven type values, the item fields and the DOCUMENT type name; an empty page; a window parameter pair; the merged answer that must show 25 items when this service is late |
| rwb-case case read fake | The scope test of AC6 | Case "RW-2026-000601" of team "MTG-BKK" in scope; case "RW-2026-000603" of team "SME-NTH" out of scope with MSG-P4-003 |
| rwb-access authorise fake (guard library) | The rights and the mask of the caller | Documents R for RW-CASEOWN and for RW-PHONECOL; no Documents R for the refused caller with MSG-P4-002; the masking policy of the caller's role |
| Seeded `rwb_document` fixture | The item, the detail and the history | The 5 documents of case "RW-2026-000601" with their stored dates, document "DOC-0601" with 3 versions, the 30 documents of the timed run, the 4,000 timeline items of case "RW-2026-000604", of which the document items are one page and one document in state `COPY_PENDING` |
| gateway-bff composite route fake | The screen path (DP-19) | The composite answer of SCR-03 and SCR-04 with the documents section filled from this service, and the partial answer when this service is late |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed, 1 cached | Three read operations of base `/api/recovery/document/v1`; the rwb-case case read consumed for the scope test; the authorise answer of rwb-access through the guard library, cached; one hop, 2 s, breaker, one GET retry with jitter |
| Kafka | None | The service owns `rwb.document.events.v1`; this story publishes nothing to it and consumes nothing (12.3, 12.4) |
| Temporal | None | No workflow and no activity; the writes this story reads are committed by the intake workflow of the store stories |
| File | 1 on demand | The content of API-P5-004 is streamed from the Blob container of the store story, only when a user opens a document; the timeline itself reads no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `casetimeline`, Java package `th.co.scb.ace.workbench.recovery.document.casetimeline`; front end component `CaseDocumentsSection` in `src/modules/recovery/document/casetimeline`, rendered inside SCR-03 and SCR-04.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; here as a prohibition, because a read writes no record | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; here the labels are versioned rows of the owner's `document_type` | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are held by the platform and service contract stories and are not repeated in the metadata rows, which carry the contract story of this key. This is a secondary slice of the legacy key: it adds no in-lane build dependency of its own, so metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P3-E2016-CON` exactly as the Work Package fixes them, and "Ready to start" stays Day 1.

**DP-11, the one-hop REST contract to rwb-case.** The legacy `DocumentQuery.forCase(caseId, from, to)` is a Java interface called inside the case module. Here it is a REST call on this service's base, one hop from rwb-case, with the 2 s budget the case contract sets, a Resilience4j circuit breaker and bulkhead per downstream at the caller, and one GET retry with jitter; this service answers inside its own part of that budget and never calls another service to complete an item. Architecture v5 slide 10 fixes the route — the Documents tab loads on click from rwb-document, one hop, inside the 2 s target — and slide 11 fixes the failure handling. The contract is faked on Day 1, so rwb-case builds its half before this service exists.

**DP-03 as a prohibition.** The document item is a read of metadata; it takes no decision and records none. This story constructs no `DecisionLogWriter`, writes no row to `rwb_document`'s decision-record table and publishes nothing on `rwb.decision-record.v1`; the record of a document decision belongs to the store, review and retention stories that take it. The contract library is on the classpath because every service carries it, and its presence is not a write path here.

**DP-06, the page size and the item cap.** The page size, its lower and upper bound and the item cap of one answer are rows read through the parameters contract, and the service holds the same rows in `document_hub_parameter` where TSD P5 places them. No default, bound or cap is a constant in Java: a value outside the bound is refused with MSG-GEN-002 before a row is read, and the item cap is the largest page the answer will ever carry, so a large case pages rather than streams.

**DP-07, the type labels.** The document type code, the English label and the Thai label are rows of `document_type` at the version in force, with `table_version`, `valid_from` and `valid_to` (DF-REF-229 to DF-REF-231). No type code and no label appears in Java or in the front end; a document typed against an older type table version shows its code rather than a guessed label, and where the list must agree with rwb-case's LOV-DOC-TYPE the comparison goes through the reference-data contract, never through a copied list.

**DP-14, the topic this service owns.** The service owns `rwb.document.events.v1` and the event names follow `rwb.document.<Event>.v1`; this story publishes nothing to the topic and names no legacy `rwb.p5.` or `rwb.casewf.` topic. The two events that the topic carries today, `DocumentStored` and `DocumentFieldsExtracted`, are written by the store and extraction stories, and rwb-case consumes them for its own projection.

**DP-19, the gateway route and the tab.** SCR-03 and SCR-04 are composed by gateway-bff, which calls rwb-case for the case and the timeline and each owner for its own panel, one hop each and in parallel, and only for what is on screen. The Documents tab and the documents section load on click; the browser never calls rwb-document. This story ships the React component that renders the panel and its states, and the route specification itself is RWB-PLT-N001-CON's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentItemsController | Controller | Serves API-P5-002 as the case-scoped read: validates the window and the page parameters, maps the errors to problem details, applies the access check and returns the page |
| ScopeGuard | Component | Asks the guard library for Documents R, the scope and the mask of the caller, and turns a refusal into 403 MSG-P4-002 or 404 MSG-P4-003 before any row is read |
| DocumentItemReader | Repository | Reads `document` for one case and one window newest first within the page size and the item cap, from `created_at`, `document_type`, `created_by`, `state` and `doc_version` |
| DocumentItemMapper | Service | Maps a document row and its type label to one timeline item: `at`, `type` "DOCUMENT", `summary`, `by`, `reference` and the version count, with no personal value and no storage reference |
| DocumentVersionReader | Service | Walks `previous_version_id` per document of the page and returns the version history: version, stored date, actor and `content_sha256`, current version last |
| DocumentDetailReader | Service | Serves API-P5-003 and API-P5-004 from the same rows: metadata, version history, the masked extracted fields of `document_field`, and the content stream with the `COPY_PENDING` refusal |
| DocumentTypeLabelReader | Repository | Reads the label of a type code from `document_type` at the version in force, and falls back to the code without inventing a label |
| CaseDocumentsSection | React component | The documents section of SCR-03 and the document part of SCR-04, with the Loading, Filtered, error and partial states, and the open of an item by its `reference` |

**Database and migrations**

- Reads `document`, `document_type` and `document_field` in schema `rwb_document`; writes no table and creates no column. The item list is a read of `document`; the detail adds the chain and the fields.
- The baseline is RWB-P5-E1024-APP's per-service Flyway sequence (DP-15). If the baseline holds no index on the case and the stored date, this story adds `V2016_1__document_timeline_index.sql` with `ix_document_case_captured_at ON document (case_id, captured_at DESC)`; if it holds no index on the version chain, the same migration adds `ix_document_previous_version ON document (previous_version_id)`. The migration runs in the rwb_document sequence of the service's own schema, touches no other schema and creates no index on another service's table.
- A page of the newest documents of a case must be read through that index only, with no sort of the whole case, which is the same check the legacy story makes for its 4,000 item case.

**Configuration and reference data**

- `rwb.document.timeline.page-size` is the default page size of the document item list, read as a parameter (DP-06) with its bounds; the value the API documents is 50 and the bound is 1 to 200, both as rows and neither as a constant.
- `rwb.document.timeline.item-cap` is the largest number of document items one answer may carry, read as a parameter and never larger than the page size bound.
- `rwb.document.timeline.label-source` names the source of the type label shown on an item, `document_type` in `rwb_document`, and is the switch between the English and the Thai label column; which column a screen shows by locale, and which row an old type table version shows, are Not specified in the source documents (GAP-1062; ASM-2010).
- The type codes and labels are rows of `document_type` with `table_version` and validity dates (DF-REF-219 to DF-REF-231); LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-RETENTION are compared through the reference-data contract of rwb-case where a list must agree (DP-07).
- The masking policy of the caller's role is read through the guard library and applied by the ACE common masking path; this service keeps no masking rule.
- The feature switch is `rwb.document.timeline.enabled`, read as a parameter: off means the case-scoped read answers 503 with MSG-GEN-006 naming "Document hub", so the caller shows its partial timeline and never an empty document list that would read as a case with no documents.

**Build steps**

1. `DocumentItemReader` and `DocumentTypeLabelReader` over the seeded `rwb_document` rows, with the newest-first order, the tie order of the source sequence and the index-only page; unit tests for AC1 and AC3.
2. `DocumentItemMapper` with the summary built from the label and the version count, and the no-personal-value rule; tests for AC1 and for the type code with no label row (X8).
3. `DocumentVersionReader` over `previous_version_id`, with one version, three versions and a broken chain; tests for AC2.
4. `DocumentDetailReader` for API-P5-003 and API-P5-004, with the version history, the masked fields and the `COPY_PENDING` refusal; tests for AC2 and X7.
5. `ScopeGuard` against the rwb-access fake and the rwb-case case read fake, with the granted path, the missing-letter 403 and the out-of-scope 404; tests for AC4 and AC6.
6. The parameter validation of the window and the page size, with no row read on a refusal; tests for AC7.
7. `CaseDocumentsSection` with the Loading, Filtered, error and partial states, the open of an item by its `reference`, and the composite-route contract test with gateway-bff; tests for AC1 and AC5.
8. The timed run over the 30 document case and the first page of the 4,000 item case, 20 runs at the 95th percentile inside the 2 second budget, plus the query plan check that the page uses `ix_document_case_created_at` only; tests for AC5.
9. The contract-fake run of RWB-P3-E2016-CON, so the story builds and proves every answer before rwb-case and the other services are live.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E2016-CON stay green against this service's answer, the 30 document case and the first page of the 4,000 item case answer inside 2 s at the 95th percentile over 20 runs, a role without Documents R receives 403 with MSG-P4-002 and no document item, a case outside the scope receives 404 with MSG-P4-003, and no answer of this story carries a personal value, a storage reference or document text.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | The document source does not answer in time, or the content is not yet in its container | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The caller's role holds no Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-001 | The call carries no session | Not specified in the source documents (DOR-RWB-P5-E2016-APP-9) |
| MSG-GEN-003 | Date to is before date from | {field} cannot be before {other}. |
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-P3-019 | No document of the case matches the filter — the caller's sentence on the screen | Nothing on this case matches the filter. |

For MSG-GEN-006 in this story, {system} is the display name of the missing source as the screen shows it, "Document hub" for this service and "Document storage" for the container of a stored document. For MSG-GEN-003 the fields are "to" and "from"; for MSG-GEN-002 the field is "size" with its bounds. For MSG-P4-002, {action} names the action the caller tried — for example "open the documents of the case" — and never a case fact, a document type or a role name. MSG-P3-019 is the caller's sentence for an empty page: this service answers an empty page with `total` 0 and the screen of rwb-case shows that sentence. Thai text follows DL10, on the assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL26 is applied to BR3 and BR6 on the assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-04 Case timeline | Loading | Sees skeleton rows while gateway-bff answers; the document items arrive with the rest of the timeline |
| SCR-04 Case timeline | Filtered | Filters by type and date; the document items follow the window; opens a document item by its reference |
| SCR-04 Case timeline | Partial | Reads the timeline without the document items when this service is late, with MSG-GEN-006 naming "Document hub" |
| SCR-04 Case timeline | Error | Reads the refusal of the case read itself, MSG-P4-003 or MSG-P4-002, which is rwb-case's answer and not this service's empty page |
| SCR-04 Case timeline | Empty | Not specified in the source documents (CG-ALL-6144) |
| SCR-04 Case timeline | No access | The document items are left out without an error and the other item types are unaffected; the refusal is MSG-P4-002 or MSG-P4-003 (section 5, X2 and X3) |
| SCR-03 Case record, documents section | Loading | Opens the Documents tab and sees the section load on click from this service, one hop |
| SCR-03 Case record, documents section | Filtered | Reads the documents of the window with type, stored date, actor and version count, and opens one document detail |
| SCR-03 Case record, documents section | Empty | Not specified in the source documents (CG-ALL-6143) |
| SCR-03 Case record, documents section | Error | The documents read answers 503 with MSG-GEN-006 naming "Document hub"; the case read itself does not fail (section 5, X1 and X6) |
| SCR-03 Case record, documents section | No access | The documents read answers 403 with MSG-P4-002 when Documents R is missing and 404 with MSG-P4-003 when the case is outside scope (section 5, X2 and X3) |

Both screens are composed by the gateway-bff route, which asks rwb-case for the case and the timeline and this service for its own items, one hop each and in parallel, and only for what is on screen (DP-19). The browser never calls rwb-document directly: the panel is filled from the composite answer, and an item opened by its reference follows the document detail operation behind the same route. The route path, the screen field list and the merge order of the composite answer are RWB-PLT-N001-CON's and RWB-P3-E2016-CON's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-016-01 | AC1, AC2, AC5, BR1, BR2 | End to end | The 5 documents of the 30 items of case "RW-2026-000601"; 20 timed runs, newest first |
| TC-E2-016-02 | No criterion here; the merge and the timeline belong to RWB-P3-E2016-APP | End to end | Filter DECISION over the case of TC-E2-016-01 |
| TC-E2-016-03 | No criterion here; the merge and the timeline belong to RWB-P3-E2016-APP | End to end | One allocation and three transfers with reasons R05, R06, R01 |
| TC-E2-016-04 | AC4, BR1 | End to end | Date filter 2026-12-05 to 2026-12-08, both ends included |
| TC-E2-016-05 | AC5, BR3, BR6 | End to end | RW-PHONECOL ("U-PC-01") on the case of TC-E2-016-01; then a caller without Documents R refused with MSG-P4-002 |
| TC-E2-016-06 | AC6, BR7, BR8 | End to end | The document source delayed beyond 2 seconds; the 25 items of the other sources and MSG-GEN-006 naming "Document hub" |
| TC-E2-016-07 | AC7, BR12 | End to end | From 2026-12-10, to 2026-12-01; then a page size outside the API bounds |
| TC-E2-016-08 | No criterion here; the empty state belongs to RWB-P3-E2016-APP | End to end | NOTICE filter in November |
| TC-E2-016-09 | No criterion here; the merge and the timeline belong to RWB-P3-E2016-APP | End to end | Assignment with no queue recorded |
| TC-E2-016-10 | AC6, BR3 | End to end | Case "RW-2026-000603" of team "SME-NTH" against a scope Own in team "MTG-BKK"; 404 with MSG-P4-003 |
| TC-E2-016-11 | AC11, BR10 | End to end | Case "RW-2026-000604" whose timeline holds 4,000 items, its document items paged 50, page size 50, one page of document items inside the 2 second budget |
| TC-E2-016-12 | No criterion here; the access refusal on the timeline belongs to RWB-P3-E2016-APP | Component | RW-REFADM (no Case record right) calls the timeline; refused with MSG-P4-002 |
| TC-E2-016-13 | AC1, AC5 | Contract | API-P5-002 on base `/api/recovery/document/v1`: the operations, events and activities of section 12 against the published contract |
| TC-E2-016-14 | AC7, BR12 | Component | Each table of section 12.7 read at its boundary rows for the version in force |
| TC-E2-016-15 | AC8, BR9 | Component | Document read on rwb_document only; case facts through the rwb-case contract; no rwb_case column read |
| TC-E2-016-16 | AC9, BR11 | Component | Type label and list values read from data rows for the version in force; no label written in code |
| TC-E2-016-17 | AC10, BR13 | End to end | A document outside the caller's scope in the case of TC-E2-016-01; absent from the answer and from the count |
| TC-E2-016-18 | AC12, BR9, BR11, BR13 | Component | Not specified in the source documents (NEWAC-RWB-P5-E2016-APP-AC12) |
| TC-E2-016-19 | AC13 | Contract | Not specified in the source documents (NEWAC-RWB-P5-E2016-APP-AC13) |

The legacy levels map System to End to end and Access to Component. Every legacy test case of this key is listed above with the slice of the behaviour this story answers — the document items, their window, their role filter, the budget, the partial answer and the validation for TC-E2-016-01, TC-E2-016-04, TC-E2-016-05, TC-E2-016-06, TC-E2-016-07, TC-E2-016-10 and TC-E2-016-11 — and no criterion for the cases whose behaviour is rwb-case's: the merge, the queue history, the decision items, the empty state, the pre-queue assignment and the access refusal. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies are not here: they belong to RWB-ITG-E2016-ITG, which proves the same values across rwb-case, rwb-document, rwb-decision, rwb-comms and the gateway end to end.

### 17. Guardrails

- No business value in code: the page size, its bounds, the item cap, the type labels and the window names are parameters or rows; no type code, label, number or field name of a screen is a Java constant (BR10, BR11).
- No personal data in events, logs, workflow inputs, tests or prompts. A document item carries the document ID, the stored date, the type label, the version count and the actor ID; no person name, account number, identity number, storage reference or document text leaves this service in an item, and the test data is synthetic.
- ACE data only through the owner's contract or the owner's `v_ace_*` views — and this story reads neither: it works on its own attachments and on the case facts of the rwb-case contract, and only rwb-source-data reads the `recovery.v_ace_*` views (ADR-010).
- No cross-schema read: `rwb_document` holds no foreign key into another schema and no copy of a case row, a party row or a scope (BR9, DP-01); the case facts arrive one hop and are not stored.
- Masking by role: the mask of the caller's role is applied before the answer leaves the service and the unmasked value is never returned and never logged (BR3, BR6, CTL-11, DL26).
- 2 s and the breaker: every call is one hop with the 2 s timeout, a breaker and bulkhead per downstream and one GET retry with jitter; a late answer is a 503 with MSG-GEN-006, never a partial page presented as the whole page (BR7, BR8, DP-11).
- The read never writes: no row, no version, no custody move, no decision record, no event and no workflow state, and a refusal writes nothing (BR12).
- No document of another case is returned for a case ID, whether or not the other case is in the caller's scope (BR13).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-008 | Queue and transfer history visible on the case, with the documents of the case readable from the record | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | R-UNI-24; CTL-09; CTL-11 | TC-E2-016-01, TC-E2-016-04, TC-E2-016-05 |
| REQ-OCC-008 | History timeline of every state change, transfer, contact, document and decision | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | CTL-09; CTL-11 | TC-E2-016-01, TC-E2-016-06, TC-E2-016-11 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it; the document item of a case carries its own stored date and actor on the same timeline | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | R-UNI-24 | TC-E2-016-01, TC-E2-016-10 |
| REQ-DRI-002 | The decision log is append only; a correction is a new record naming the one it corrects, and a superseded document version is still readable | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08 | 06 Take over and own the case; All recovery processes | R-UNI-24; CTL-11 | TC-E2-016-01, TC-E2-016-05 |
| REQ-WKM-014 | The next action is visible on the case record and in every queue view; the documents section of the record view shows what was attached, when and by whom | Business Requirements Epic 2, sections 3.3 and 4; Program, section 5.3 | FEAT-WKM-08, FEAT-WKM-09 | 06 Take over and own the case; All recovery processes | None | TC-E2-016-01, TC-E2-016-04 |

| Legacy reference | Where it is kept |
|---|---|
| Story RWB-E2-016 | Split across RWB-P3-E2016-APP and RWB-P3-E2016-CON (the timeline, the merge, the ordering, the paging, the queue history and the twelve criteria), RWB-P5-E2016-APP (this story: the document items and their version history), the rwb-comms and rwb-decision slices of the same key, and RWB-ITG-E2016-ITG |
| Legacy AC1 (timeline, 30 events, 2 seconds) | RWB-P3-E2016-APP AC1; here AC1 and AC5 for the 5 documents of the 30 items and the budget |
| Legacy AC2 to AC11 | RWB-P3-E2016-APP AC2 to AC11; here AC3 (the date filter), AC4 (the role filter), AC5 (the late source), AC6 (the scope) and AC7 (the validation) only |
| Legacy BR1, BR2, BR3, BR6, BR7 | Sections 8 of this story (the document part) and of RWB-P3-E2016-APP (the whole timeline) |
| Legacy BR4, BR5 | RWB-P3-E2016-APP section 8 (queue history and the decision entry) |
| Legacy section 12, `DocumentQuery.forCase(...)` | Section 12 of this story: API-P5-002 on base `/api/recovery/document/v1`, one hop, 2 s, breaker (DP-11, DP-13) |
| Legacy section 11, DF-DOC-001, 004, 005 | Section 11 of this story, read from `rwb_document` instead of through an in-process interface |
| Legacy section 13, the timeline service and mapper | Split: the merge and the screen stay with RWB-P3-E2016-APP; the document item reader, mapper, version reader and the documents section are this story |
| Legacy section 16, TC-E2-016-01 to TC-E2-016-12 | Section 16 of this story, with the seven cases this slice answers and the five that stay with RWB-P3-E2016-APP |
| Legacy `-ITG` copies of the cases | RWB-ITG-E2016-ITG |
| Legacy section 15, SCR-03 and SCR-04 | Section 15 of this story (the documents section and the document part of the timeline) and of RWB-P3-E2016-APP (the screens themselves) |

### 19. Out of scope

- The timeline endpoint, the merge, the ordering, the paging and the queue history: RWB-P3-E2016-CON and RWB-P3-E2016-APP.
- The decision items: rwb-decision and the P7 slice of this legacy key.
- The notice items: rwb-comms and the P6 slice of this legacy key.
- The clocks and deviations panels of SCR-03: RWB-E2-015, carried in RWB-P3-E2015-APP.
- The document store, the versions and the detail panel's write path: RWB-P5-E1024-APP (the store, the container, the version chain, the upload and the field review).
- The intake, the OCR and the extraction: RWB-P5-E1049-APP, RWB-P5-E1050-APP and RWB-P5-E1053-APP.
- The end-to-end proof of these values across the services and the gateway: RWB-ITG-E2016-ITG.
