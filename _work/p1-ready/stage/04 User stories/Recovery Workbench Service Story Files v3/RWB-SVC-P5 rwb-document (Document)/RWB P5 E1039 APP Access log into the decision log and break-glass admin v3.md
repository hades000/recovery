# RWB-P5-E1039-APP Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Decision-record event type name corrected to `rwb.decision.DecisionRecorded.v1`; topic `rwb.decision-record.v1` unchanged (RD-P1-008).
- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

| Item | Value |
|---|---|
| Story key | RWB-P5-E1039-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | L-P5-J |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E1039-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-009, FR-P5-010) |
| Status | Draft (directive resolutions) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P5-E1039-APP-14); to be confirmed against the epic design record |
| Size | Not specified in the source documents (DOR-RWB-P5-E1039-APP-16) |
| Open decisions | DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL38 (assumptions ASM-0245, ASM-1413, ASM-1424, ASM-1508); both still open |
| Readiness decisions | RD-P1-008, RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: the document half of RWB-E1-039 becomes the recorder of one `AC-READ` access entry per served document content read in `rwb_document`, written through the DP-03 library before the first byte of the file, marked with the grant and the incident while a break-glass grant is active, and failing closed when it cannot be written; the writer, the grant, the access-log read and the central ledger stay with rwb-access and rwb-decision. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1039-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 17 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **security administrator (RW-SECADM)**, I want **every read of a document's content through the Workbench to be written into the access log as one `AC-READ` entry before the file is returned, with the case, the document, the actor and — while emergency access is on — the grant and the incident, and to return nothing when that entry cannot be written**, so that **no document leaves the Workbench unrecorded and a document read can be audited from the same log as the decisions and the emergency access**.

This story is the `rwb-document` part of legacy RWB-E1-039 — the recorder of a document content read:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1`, task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- What this story owns is one act, done once per served read: a local decision record with decision code `AC-READ`, the actor, the case id, the document id, the area and the right, and the grant id and incident reference when the caller holds an active break-glass grant — committed through the DP-03 library in `rwb_document` before the first byte of the file is streamed, and collected into the central ledger from `rwb.decision-record.v1`.
- What this story does not own, and must not build, is the access log, the writer of the access event, the break-glass grant, the two-person rule, the time box and the access-log read: they are rwb-access's in RWB-P4-E1039-CON and RWB-P4-E1039-APP. The central ledger, the `GET /decision-log` query and the chain verification are rwb-decision's in RWB-P7-E1039-APP. This service holds no access-log table and evaluates no grant (DP-01).
- Neighbours of the same legacy key: RWB-P4-E1039-APP (all ten legacy criteria), RWB-P4-E1039-CON (the shapes this story builds to), RWB-P4-E1039-DB and RWB-P4-E1039-OPS, RWB-P7-E1039-APP (the ledger and the query) and RWB-ITG-E1039-ITG (the end-to-end journey).
- The row the entry describes is written by RWB-P5-E1024-APP; the store's own decision record on a store is decision code `DOCATT` and is not this story; the content read is reached from SCR-30 Case documents (RWB-P5-E1026-APP) through the gateway-bff route.
- The entry carries references and codes only: the user id, the case id, the document id, the document type code and — while a grant is active — its id and incident reference. No person name, no account number, no identity number, no extracted field value and no file content is in the entry or in a log line.

### 2. Business rationale

The bank cannot answer today who read a debtor's document on a given date, and an administrator with emergency access leaves no trace of what was opened. RWB-E1-039 answered both with one in-process publisher and one `decision_log_entry` table inside one module. In the target the entry is a decision record of the service that served the read (DP-03), the central ledger collects it from `rwb.decision-record.v1`, and the access-log read and the grant belong to rwb-access. For rwb-document the debt is exact: one correct entry, in the right transaction, before the bytes leave.

The architecture fixes each part: every service writes its decisions to its own chain through the library and publishes on the shared topic; the ledger collects them and answers the workbench-wide query (Architecture v5 slides 28 and 42; ADR-022); the write-once Blob copy is read only through this service (slide 9). The functional source states the same fact for the document hub: the module writes the decision log entry before any change and records each document read (FSD P5 A1, and the read rules of A2.1 and A2.6); the technical source gives the content read `Documents` right `R` with scope applied and the error set 401, 403, 404, 503 (TSD P5 API-P5-004, T6.1).

The value is trust in one category the case service cannot produce: the document read. It meets REQ-ACA-006 for the content read and REQ-ACA-008 for the marking of a break-glass read, and it supports controls CTL-09 and CTL-11. The measure is reads of the document store written to the access log: target 100 percent (NFR-042).

### 3. Preconditions

- RWB-P4-E1039-CON is published: the record shape of one access-log entry, the six decision codes `AC-SIGN`, `AC-DENY`, `AC-READ`, `AC-EXPT`, `AC-BGON` and `AC-VERS`, the optional `grantId` and `incidentReference`, the session answer with the break-glass state and its end time, the fail-closed rule and the refusal vocabulary. This story consumes those shapes and calls none of the four grant and log operations.
- The DP-03 library is part of the `rwb_document` baseline (RWB-PLT-E1027-CON): the local decision-record table, the chain and the publish of `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`. This story writes rows, not DDL, and adds no build dependency of its own — the Work Package fixes "Depends on (build)" as None for this secondary slice.
- RWB-P5-E1024-APP is done: the `document` row exists with its case id, type, version, content hash and storage reference, and the file is in the write-once container. A content read of a missing or pending copy is the store's path, not this story's.
- LOV-DECISION holds `AC-READ` with the other access event codes, read through the reference-data contract of rwb-case at the version in force (DP-07, C RWB-P3-E1043-CON); no decision code is written in code.
- The caller's identity and break-glass state reach the service in the forwarded session envelope of gateway-bff, and the session answer of rwb-access is the authority for the grant (DP-19, DP-11). The mechanism that carries the grant id and the incident is Not specified in the source documents (GAP-2339; ASM-3893).
- The tunables of this story — the name of the platform administrator incident queue, the lifetime of the cached session answer and the 2 s client budget — are parameter rows behind the parameters contract of rwb-case (DP-06, C RWB-P3-E1042-CON), never constants. The break-glass window and the review window are rwb-access's parameter rows and are not restated here.
- The exact capability-area code and result code of a document read in an entry are Not specified in the source documents (GAP-2340; ASM-3894). Which P5 reads other than the content read write an entry is Not specified in the source documents (GAP-2341; ASM-3895).
- No approval is required for a Draft story in this run; the story builds against the published contract and its fake (R5.4 class C).

### 4. Flow

1. Caller: a user with `Documents` right `R` opens a document on SCR-30 Case documents and asks for its content; the browser calls `GET /api/recovery/documents/{documentId}/content` through gateway-bff, one hop.
2. `DocumentReadAuthoriser` takes the caller identity, the rights and the break-glass state from the forwarded session envelope, refuses a caller without `Documents` right `R` (403, MSG-P4-002) and a document outside the caller's scope (403) before any row is read for streaming.
3. `DocumentReadService` resolves the `document` row in `rwb_document` — case id, type, version, storage reference, content hash — and confirms the copy is present. A missing row answers 404 and a pending copy 503 with MSG-GEN-006; neither writes an entry.
4. `AccessEntryFactory` builds the entry from the row and the session, not from the request: decision code `AC-READ` from LOV-DECISION, actor user id, case id, document id, capability area and right of the operation, result, and the grant id and incident reference when the session carries an active grant.
5. `AccessEntryRecorder` writes the entry through the DP-03 library in the read's transaction, with the occurred time and the actor, and the library publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` from the outbox. The entry carries no file content, no hash, no storage reference and no field value.
6. The write commits. Only now does `DocumentContentStreamer` open the blob and stream the bytes to the caller; the response carries no entry id and no ledger reference.
7. The central ledger of rwb-decision collects the record and answers the workbench-wide query; RW-AUDIT reads the reads of a case from that query with decision `AC-READ` (RWB-P7-E1039-APP, not this story).
8. RW-SECADM reads the same entries from `GET /api/recovery/access/v1/admin/access-log` of rwb-access, which is the access log the legacy story built (RWB-P4-E1039-APP).
9. While a grant is active: every entry this service writes carries the grant id and the incident reference, so the review of the use finds the document reads of the incident; at the end time the session stops marking and the grant stops applying, with no action by anyone.
10. A second read of the same document is a second read and writes a second entry: the log answers who read what and when, and a repeat by the same person on the same day is two facts, not one.
11. The entry is never written after the bytes: a read that cannot be recorded returns 503 with MSG-P7-003, no bytes and no partial file, and raises one incident to the platform administrator queue (AC2).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The entry cannot be written (library unavailable, chain refused, timeout) | The read returns nothing: 503, no bytes, no partial file, no retry that serves the file | MSG-P7-003 | AC2 |
| X2 | The session envelope carries no break-glass state, or an expired one | The grant is not applied and nothing is marked; the role's own letters decide the read, and the check runs on every request | MSG-P4-002 when the right is missing | AC3 |
| X3 | A caller without `Documents` right `R` asks for the content | Refused before the row is read and before any entry; the denial entry is rwb-access's | MSG-P4-002 | AC5 |
| X4 | The document is outside the caller's scope | Refused with 403 before any entry; no bytes and no case fact in the answer | None (the API's 403) | AC5 |
| X5 | The document id does not exist | 404 with no entry, no incident and no decision record — no read happened | None (the API's 404) | AC5 |
| X6 | The copy of the document is still pending | 503 with MSG-GEN-006 and no entry; the read is refused, not served empty | MSG-GEN-006 | AC5 |
| X7 | The reference-data read of LOV-DECISION fails | The cached version in force is used; if no version is cached the read fails closed with MSG-P7-003, because an entry without a listed code is not written | MSG-P7-003 | AC1, AC2 |
| X8 | The session answer does not arrive inside 2 s | The read fails closed with MSG-GEN-006 and no entry; the breaker opens and the next request is refused until it closes | MSG-GEN-006 | AC3, AC5 |
| X9 | The blob read fails after the entry is committed | The caller gets 503 and no bytes; the entry stands, because a read was attempted and refused, and the store's own path reports the storage fault | MSG-GEN-006 | AC2 |
| X10 | A caller asks for the content of an earlier version of a document | The row served is the version's own row; the entry names the document id of that version, so the log distinguishes the versions | None | AC6 |

X9 is the one path where an entry stands for a read that returned nothing. That is deliberate: the entry records the attempt to read the content and its refusal, and a log that lost it would hide the attempt.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E1039-CON and its fake, the DP-03 library of the baseline and the store of RWB-P5-E1024-APP; no build dependency of its own |
| Negotiable | The grant-carrying mechanism, the cache lifetime and the queue name are open; the entry shape, the fail-closed rule and the order of entry and bytes are fixed |
| Valuable | Every document content read is auditable from one log, and an unauditable read is refused |
| Estimable | One authoriser, one entry factory, one recorder, one streamer and one contract test |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Each criterion of section 7 runs over the committed record and the response bytes, with the access contract and the library stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Access log into the decision log and break-glass admin — the rwb-document content read

  Background:
    Given the rwb-access contract mock returns the entry shape of one access-log entry with decision code "AC-READ" and the optional values "grantId" and "incidentReference"
    Given the rwb-access contract mock returns no active grant for test user "U-4101"
    Given the rwb-access contract mock returns an active grant for test user "U-4102" with incident "INC0004521" and end time 14:30
    Given the decision-record stub accepts one record per call and can be forced to fail

  Scenario: AC1 A content read commits one AC-READ entry before the file is returned (new, D-RCV-60)
    Given test user "U-4101" holding RW-CASEOWN opens document "DOC-2026-0009981" on case "RW-2026-000123" at 10:15 on 3 December 2026
    When GET /api/recovery/document/v1/documents/{documentId}/content returns the file
    Then one local decision record with decision code "AC-READ", actor "U-4101", the case ID "RW-2026-000123", the document ID "DOC-2026-0009981", capability area "DOCUMENTS" and right "R" is committed before the first byte of the file is returned
    And the record carries no field value, no extracted field value, no person name and no file content
    And one read writes one record and no second record

  Scenario: AC2 The read fails closed when the entry cannot be written (new, D-RCV-60)
    Given the decision-record stub is forced to fail
    When test user "U-4101" opens document "DOC-2026-0009981" on case "RW-2026-000123"
    Then the call returns status 503 with message MSG-P7-003 and no byte of the file
    And no record is committed and no partial file is streamed
    And one incident is raised to the platform administrator queue
    And the same read succeeds once the stub accepts the record, with exactly one record for that read

  Scenario: AC3 An active grant marks every entry until its end time (new, D-RCV-60)
    Given test user "U-4102" holds RW-PLATADM and has an active break-glass grant for incident "INC0004521" ending at 14:30
    When "U-4102" reads document "DOC-2026-0009981" at 14:20
    Then one record with decision code "AC-READ" is committed with the grant ID and incident "INC0004521"
    And the end time and the banner state MSG-P4-004 are the rwb-access answer, never a value this service computes
    When "U-4102" reads the same document at 14:31
    Then the read is refused with status 403 and message MSG-P4-002 before any record is written
    And this service writes no AC-DENY record, because the refusal is rwb-access's to record

  Scenario: AC4 No access log of its own: the entry is this service's decision record (new, D-RCV-60)
    Given document "DOC-2026-0009981" of case "RW-2026-000123" is read by "U-4101"
    When "U-4101" reads document "DOC-2026-0009981" through GET /api/recovery/document/v1/documents/{documentId}/content
    Then the record is written in "rwb_document" through the DP-03 library and published as "rwb.decision.DecisionRecorded.v1" on "rwb.decision-record.v1"
    And rwb-document holds no access-log table, reads no "rwb_access" table and calls no access-log read and no grant operation (the grant operation is POST /admin/break-glass-grants of rwb-access; the legacy path POST /admin/break-glass is its alias and is not called here)
    And the access-log read stays with GET /api/recovery/access/v1/admin/access-log and the reads of a case stay with the ledger query of rwb-decision
    And the case ID and the document ID in the record are values taken from the "document" row, not foreign keys

  Scenario: AC5 A refused, absent or pending document writes no entry (new, D-RCV-60)
    Given test user "U-4101" holding RW-CASEOWN requests document "DOC-2026-0009981" of a case outside the caller's scope
    When "U-4101" requests the content of document "DOC-2026-0009981"
    Then the call is refused with status 403 before any record and no byte is returned
    And a document id that does not exist answers 404 with no record, no incident and no decision record
    And a caller without the Documents right is refused with MSG-P4-002 and no record
    And a content read whose copy is still pending answers 503 with MSG-GEN-006 and no record

  Scenario: AC6 The record names the version that was served (new, D-RCV-60)
    Given document "DOC-2026-0009981" of case "RW-2026-000123" is at version 2 of type "COURT_NOTICE"
    When the content of version 2 is read
    Then the record names the document ID of that version and its case
    And a read of an earlier version names that version's own document row, so the log tells the versions apart
    And the record never carries the storage reference, the content hash or the retention class

  Scenario: AC7 A call with no valid session is answered 401 and writes no record (new, D-RCV-60)
    Given test user "U-4101" has no valid session
    When the content of document "DOC-2026-0009981" is requested through GET /api/recovery/document/v1/documents/{documentId}/content
    Then the call returns status 401 with no byte of the file
    And no record is committed and no incident is raised

  Scenario: AC8 A grant opens no document beyond the RW-PLATADM letters (new, D-RCV-60)
    Given test user "U-4102" holds RW-PLATADM without the Documents right and has an active break-glass grant for incident "INC0004521" ending at 14:30
    When "U-4102" reads document "DOC-2026-0009981" at 14:20
    Then the read is refused with status 403 and message MSG-P4-002 and no record is written
    And the grant marks no record and opens no document the role could not read

  Scenario: AC9 A personal-data pattern in the record or a log line fails the build (new, D-RCV-60)
    Given the build runs the personal-data scan over the record fields, the log lines and the test fixtures of the content read
    When a fixture for test user "U-4101" carries a name, an identity number or a file body in the record or a log line
    Then the build fails and no artefact is published
```

The nine criteria are new and test only this deliverable: the record, its ordering against the bytes, the fail-closed path, the grant marking, the prohibition of a second access log, the refusals, the version, the grant that opens no document, and the personal-data guard. No legacy criterion of RWB-E1-039 is copied into this section: AC1 to AC10 belong to RWB-P4-E1039-APP, and their end-to-end form belongs to RWB-ITG-E1039-ITG. The values reused here are the legacy ones: case "RW-2026-000123", document "DOC-2026-0009981", the read time 10:15 on 3 December 2026, users "U-4101" and "U-4102", incident "INC0004521", the end time 14:30 with the read at 14:20 and the refusal at 14:31, and the messages MSG-P4-002, MSG-P4-004, MSG-GEN-006 and MSG-P7-003.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every read of a document's content writes one access entry as it happens; here one record per served read, committed before the bytes (legacy BR1) | REQ-ACA-006; FEAT-ACA-08; NFR-042; legacy BR1 |
| BR2 | A read whose access entry cannot be written returns no data (legacy BR2) | Principle 5; R-UNI-39; legacy BR2 |
| BR3 | An access entry lists field IDs and their masking position, never field values; a content read names the case and the document and no extracted value (legacy BR3) | NFR-040; legacy BR3 |
| BR4 | Break-glass needs an approval in the bank IAM against an open incident and a reason within the reason-length bounds held as parameters (open under DL38; legacy value 20 characters); this service verifies nothing and accepts the rwb-access answer (legacy BR4) | Admin and access model, section 5.3; REQ-ACA-008; legacy BR4 |
| BR5 | A grant ends at the earlier of the window and the IAM group end, enforced on every request rather than by a job (legacy BR5) | rwb.access.breakglass.window-hours; DL38; legacy BR5 |
| BR6 | Every action under break-glass is marked with the grant and the incident reference; here every record written while the grant is active (legacy BR6) | Admin and access model, section 5.3; legacy BR6 |
| BR7 | A platform administrator holds only the letters of RW-PLATADM, which include Documents R; a right beyond them comes only from an active grant (legacy BR8) | Admin and access model, section 3.2; TSD P5 T6.1; legacy BR8 |
| BR8 | The entry is the serving service's own decision record and the ledger collects it; no service holds a second access-log table (DP-03, DP-01) | ADR-022; Architecture v5 slides 28 and 42 |
| BR9 | No personal data in the record, the log lines, the metrics or the tests: the actor is a user id, the document a reference, the case a reference (legacy guardrail) | NFR-040; legacy section 17 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by `AccessEntryRecorder` being the only path that writes the record, by the record being committed before `DocumentContentStreamer` opens the blob, and by the absence of any cached-serve path that returns a file without the record. A second read is a second record.
- BR2 is executed by the read's transaction: the record and the open of the blob are in one unit of work, so a failed record raises MSG-P7-003 and no byte is written to the response. There is no asynchronous after-commit log and no "log it later" queue on this side.
- BR3 is executed by the entry factory reading five columns of the row — case, document, type, version and the actor from the session — and by no field of `document_field` being read for the entry at all.
- BR4 and BR5 are executed by this service not evaluating a grant: `DocumentReadAuthoriser` takes the state from the session answer, which rwb-access has already bounded by its window and the group end, and re-reads it on every request, so a grant that ended one second ago cannot mark a record.
- BR6 is executed by the entry factory copying the grant id and the incident reference from the session answer onto the record, and by the refusal to derive either from the request: a caller cannot name a grant.
- BR7 is executed by the matrix of TSD P5 T6.1, where RW-PLATADM already holds Documents R, and by nothing in this service extending a right: the grant marks the record, it does not open a document the role could not read.
- BR8 is a prohibition with an owner elsewhere: the access log is rwb-access's and the ledger is rwb-decision's, so this service may write its own record and nothing else. A class that appends to a shared access-log table fails the build.
- BR9 is executed by the record's field list and by the test fixtures: no fixture carries a name, an identity number or a file body, and a personal-data pattern in the record or a log line fails the build.
- Break-glass grant operation and fault point (GAP-0359): the grant is activated by `POST /admin/break-glass-grants` in rwb-access (Ownership Map), and the legacy `POST /admin/break-glass` path is an alias of that published operation. The local-record fault point is the failed record write that raises MSG-P7-003 (BR2). The SIT evidence location is Not specified in the source documents (GAP-0359).
- Local decision record and actions (GAP-0780): the entry is the serving service's own decision record (BR8), named by its contract and not by a table name. The library table name is Not specified in the source documents (GAP-0780). The keys and their order in the actions element for a refusal and for an export are Not specified in the source documents (GAP-0780).

### 9. State transitions

No case transition: this story changes no case status and moves no stage. It adds the lifecycle of one access record and reads the lifecycle of the grant as rwb-access states it.

| From | Event | Condition | To |
|---|---|---|---|
| (no record) | a content read is authorised and the row resolves | The caller holds Documents R, the document is in scope and the copy is present | record written, bytes not yet sent |
| record written | the record commits | The DP-03 library accepts the entry | `committed`; the library outbox publishes it on `rwb.decision-record.v1` |
| record written | the write fails | Library unavailable, chain refused, timeout | `none`; the read answers 503 with MSG-P7-003 and one incident |
| committed | the central ledger collects the record | rwb-decision's consumer group reads the topic | `collected`, and the ledger query answers it |

Read-only, for the reader of the record:

| Grant state (rwb-access answer) | What the record says |
|---|---|
| `ACTIVE` with end time 14:30 | The grant id and incident `INC0004521` are on every record written before 14:30 |
| `ENDED` | No grant on the record; a read the role cannot make is refused 403 with MSG-P4-002 and no record |
| No grant | The record carries the role's own right only |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM, security administrator | Reads the entries of document reads from the access log of rwb-access and reviews each break-glass use in the review window; Platform administration R |
| RW-AUDIT, internal audit | Reads the document reads of a case from the ledger query of rwb-decision; changes nothing |
| RW-COMPLY, compliance and PDPA officer | Reads the same entries; receives an unreviewed use from the access side |
| RW-PLATADM, platform administrator | Holds Documents R and reads a document content; a read under an active grant marks the record, and the role gains no document right from it |
| Every bank role with Documents R | Generates the entry by reading a document content; the entry names the user id |
| SY-OCR and SY-AGENT | Read a document through the store and the extraction path, not through the content read; their reads are their own stories' |
| The rwb-document service identity (the rwb_document login, DP-02) | Writes the record in `rwb_document` through the DP-03 library and runs the outbox relay |
| Nobody | Holds an access-log table, appends to the access log of rwb-access, reads `rwb_access` or grants a break-glass right from this service |

The refusals are the operation's and are quoted, not built, here: MSG-P4-002 for a missing Documents right or a read after the grant has ended, MSG-GEN-006 for a document storage that cannot answer, MSG-P7-003 for a record that cannot be written.

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Read into the record as the document reference |
| DF-DOC-002 | `document` | case_id | Read into the record as the case reference |
| DF-DOC-004 | `document` | document_type (LOV-DOC-TYPE) | Read into the record as the type code |
| DF-DOC-011 | `document` | doc_version | Read to name the version that was served |
| DF-DOC-006 | `document` | storage_ref | Read to open the blob only; never carried in the record |
| DF-DOC-026 | `document` | content_sha256 | Read by the store's own check only; never carried in the record |
| DF-DEC-002 | the DP-03 local record in `rwb_document` | case_id | Write; empty for a sign-in, a refusal and an export, never empty for this read |
| DF-DEC-003 | the DP-03 local record | decision_code | Write `AC-READ` from LOV-DECISION |
| DF-DEC-014 | the DP-03 local record | actions | Write the area, the right, the result, the document id and, while a grant is active, the grant id and the incident |
| DF-DEC-016 | the DP-03 local record | decided_at | Write the occurred time of the read |
| DF-DEC-030 | the DP-03 local record | actor_user_id | Write the caller's user id |
| DF-DEC-001 to DF-DEC-018 | the DP-03 local record | all fields | Write (one record per read) as the library shapes them |

The row and the record carry different things on purpose. The `document` row holds the storage reference, the hash, the retention class and the party reference; the record holds references and codes. DF-DOC-003, DF-DOC-006, DF-DOC-009 and DF-DOC-026 stay in `rwb_document` and never travel, because the log needs to know *that* the content was read, of which document, by whom and when, and not what is in it. The legacy field IDs of the decision record are kept unchanged (DF-DEC-001 to DF-DEC-018, with DF-DEC-002, -003, -014, -016 and -030 the ones this story writes); `decision_log_entry` and its index belong to rwb-decision, and no record of this service is written into `rwb_decision`. The legacy `decision_log_id` reference that the retention rows carry (DF-DOC-095) stays with the retention stories.

### 12. Contract

The story builds against the `/api/recovery/document/v1` path; the contract version it is fixed to is Not specified in the source documents (DOR-RWB-P5-E1039-APP-23).

#### 12.1 REST operations provided

One operation of the `rwb-document` contract changes behaviour; its path, request, response and error set stay those of the API Specification.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P5-004 | GET | `/documents/{documentId}/content` | Download the document content; one `AC-READ` record is committed before the first byte; response Binary; errors 401, 403, 404, 503, with 503 and MSG-P7-003 when the record cannot be written and 503 with MSG-GEN-006 when the copy is not available | Documents, right R, scope applied | Not applicable, read only |

No field, header or path parameter is added, so a caller learns nothing new: no record id and no ledger reference is returned. A read that is refused for want of a record answers the same 503 envelope as a read the store cannot serve, and no caller can ask for "unlogged" content.

#### 12.2 REST operations consumed

One hop, 2 s timeout and a breaker per downstream (DP-11). One operation at run time and two contract facts:

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller identity, the roles and the break-glass state with the grant id, the incident reference and the end time; the state is re-read for the request, never cached across a request |
| — | the entry shape and the code list of RWB-P4-E1039-CON | P4 rwb-access | A fact and a fixture: `decisionCode`, `actorReference`, `caseReference`, `documentReference`, `capabilityArea`, `right`, `result`, `grantId`, `incidentReference` and `decidedAt`. This story writes its own record to that shape and calls no access-log operation |
| — | the parameters and reference-data contracts | P3 rwb-case | A fact: LOV-DECISION at the version in force and the tunables of section 13 (DP-06, DP-07) |

The access-log read `GET /api/recovery/access/v1/admin/access-log`, the two grant writes and the grant read are declared by RWB-P4-E1039-CON and are never called from this service. The ledger query `GET /api/recovery/decision/v1/decision-log` is rwb-decision's and is not called here either.

#### 12.3 Events published

None of its own. The access record leaves the service as the DP-03 library's message, named here so that the reader of the ledger recognises it and never declared as this story's contract:

| Message | Topic | Owner of the schema | Carries |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` (shared) | RWB-PLT-E1027-CON | The local record of this service, envelope and payload as the library defines them; key caseId, so the records of a case travel in order |

The service's own topic `rwb.document.events.v1` carries `DocumentStored` and `DocumentFieldsExtracted` only, and this story adds no message to it (DP-14): an access record is a decision record, not a document event.

#### 12.4 Events consumed

None. This story subscribes to no topic and creates no consumer group in `rwb_document`; the grant state is read from the session answer, not from an event.

#### 12.5 Workflows and activities

None. The read is synchronous in the caller's thread, the record is written in that transaction, and no activity or child workflow is started. The `DocumentIntakeWorkflow` and its activities belong to RWB-P5-E1049-APP and RWB-P5-E1024-APP; queue `rwb-document` gains no task from this story.

#### 12.6 Schedules

None. The grant end is enforced on every request rather than by a job (BR5), the review window is rwb-access's parameter and its review list is RWB-P4-AD008-APP, and the outbox relay of JOB-11 is the platform's one-minute Schedule, not this story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `document` | P5 (`rwb_document`) | Read for the case id, the type, the version and the reference; written by RWB-P5-E1024-APP |
| the DP-03 local decision-record table | PLT library, created in `rwb_document` | The `AC-READ` record, written in the read's transaction (DP-03) |
| `outbox_event` | PLT library, created in `rwb_document` | The record's outbox row, written by the library; the relay publishes it |
| `document_field` | P5 (`rwb_document`) | Not read by this story: the record carries no field value (BR3) |

No foreign-schema table is read (DP-01). `decision_log_entry` and its index are rwb-decision's, the break-glass grant is rwb-access's, and the case is a value taken from the `document` row, not a foreign key into `rwb_case`.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-access contract fake | RWB-P4-E1039-CON | The entry shape and the code list; the session answer with no grant for "U-4101" and an active grant for "U-4102" with incident "INC0004521" ending at 14:30; the 403 with MSG-P4-002 after the end |
| decision-record stub | RWB-PLT-E1027-CON | One accepted record per call, the forced failure of AC2 and X1, and the published `DecisionRecorded` message of 12.3 |
| document store fixture | RWB-P5-E1024-APP | A committed row for document "DOC-2026-0009981" of case "RW-2026-000123" at version 2, the earlier version row, the missing id of X5 and the pending copy of X6 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DECISION with `AC-SIGN`, `AC-DENY`, `AC-READ`, `AC-EXPT`, `AC-BGON` and `AC-VERS` at the version in force, and the failed read of X7 |
| parameters fake | RWB-P3-E1042-CON | The queue name, the cached-session lifetime and the 2 s client budget |
| gateway-bff session envelope fixture | RWB-PLT-N001-CON | The forwarded identity and roles, the break-glass claim, and the missing-answer path of X8 |

Contract fake library version: Not specified in the source documents (DOR-RWB-P5-E1039-APP-22); no fake library version is recorded as published.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | The content read on `/api/recovery/document/v1`; the session read of rwb-access, one hop with a 2 s budget and a breaker |
| Kafka | 0 published by this story, 1 named | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` through the DP-03 library; no subscription |
| Temporal | None | No workflow, activity or Schedule in this story |
| File | 1 read | The content is streamed from the write-once Blob copy through this service only; the record carries no storage reference and no claim-check link |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `accesslog`, Java package `th.co.scb.ace.workbench.recovery.document.accesslog`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentReadAuthoriser | Service | Takes the identity, the rights and the break-glass state from the forwarded session envelope; refuses a missing Document R and an out-of-scope document before the row is read for streaming |
| AccessEntryFactory | Service | Builds the `AC-READ` entry from the `document` row and the session: code, actor, case, document, type, area, right, result, grant id and incident; refuses a code outside LOV-DECISION and derives nothing from the request body |
| AccessEntryRecorder | Service | Writes the entry through the DP-03 library in the read's transaction and returns only when the record is committed; the single path that writes an access record in this service |
| DocumentContentStreamer | Service | Opens the blob and streams the bytes after the record commits; renders 503 with MSG-P7-003 when the record fails and 404 or 503 before any record when the row or the copy is missing |
| AccessRecordContractTest | Test component | Asserts the record against the shape of RWB-P4-E1039-CON and the library's message: fields, code list, grant marking, key caseId and the absence of a personal value |

**Database and migrations.** None, and that is the DP-15 statement for this story: the per-service Flyway sequence of `rwb_document` is not extended. The local record table and the outbox table arrive with the DP-03 library at the baseline; the `document` table is unchanged and no index is added, because the ledger query runs on rwb-decision's side.

**Configuration.**

- `rwb.document.access-log.queue` is the platform administrator incident queue, read as a parameter (DP-06); its name is Not specified in the source documents (GAP-2342; ASM-3896).
- `rwb.document.access-log.session-cache` bounds the reuse of the session answer within one request only; a grant is re-checked for every read (BR5).
- `rwb.document.access.client.timeout` is the 2 s budget of the session read, with a breaker per downstream.
- `rwb.access.access-log` is rwb-access's flag and is not read here; this story adds no switch that can turn the entry off, because a switch that serves content unlogged is the fault the story prevents.
- The exact capability-area code and the result code of a document read are Not specified in the source documents (GAP-2340; ASM-3894), and the mechanism that carries the grant id and the incident reference is Not specified in the source documents (GAP-2339; ASM-3893).

**Screen states.** For SCR-30 and SCR-38 the empty, error and no-access states are Not specified in the source documents (DOR-RWB-P5-E1039-APP-10); for SCR-43 the empty, loading, error and no-access states are Not specified there too.

**Schema ownership.** `rwb_access` belongs to rwb-access; this story reads and writes none of it (DP-01), and `rwb_document` is this service's own schema.

**Build steps**

1. `DocumentReadAuthoriser` over the session envelope, with the missing-right refusal (MSG-P4-002) and the scope refusal before any record (AC5).
2. `AccessEntryFactory` over five columns of the row and the session, with a negative test per forbidden field (no hash, no storage reference, no field value, no person name) and the code check against LOV-DECISION (AC1, AC6).
3. `AccessEntryRecorder` inside the read's transaction, with the record-before-bytes assertion, the forced failure of AC2 and the one-record-per-read test.
4. `DocumentContentStreamer` after the commit, with the 404, the pending copy, the scope refusal and the blob fault of X9; no partial file on any path.
5. The grant marking from the session answer, with the 14:20 read marked and the 14:31 read refused before any record (AC3).
6. The negative tests of DP-01 and DP-03: no access-log table, no `rwb_access` read, no call of the access-log read or the grant operations, and no second writer of an access record (AC4).
7. The contract test against RWB-P4-E1039-CON and RWB-PLT-E1027-CON, then the same run against the real session and ledger in SIT.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The record is written in `rwb_document`, and the break-glass grant and `decision_log_entry` are only named | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. This is the pattern that carries the story: one local record per read, published on the shared topic | H RWB-PLT-E1027-CON, satisfied by the baseline of `rwb_document`; the Work Package fixes this slice as a secondary story with no build dependency of its own |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library: the queue name, the cache bound and the timeout are rows, not code | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON (baseline) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: the `AC-READ` code and the other five codes arrive with the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON (baseline) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The content read answers the caller and the session read is the only outbound call | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1`; the content read sits under the service base and no other base appears | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake). The legacy key knew a lake copy of the log and a lake read to be logged; neither exists, and no access record travels to a lake — the ledger of rwb-decision is the reporting path | none; no lake data is needed |
| DP-19 | Screen, ace-web | gateway-bff composite route: SCR-30 asks the document owner for the content and the session, one hop each; the route passes the identity and the grant claim | H RWB-PLT-N001-CON, satisfied by the platform baseline |

DP-03 is the pattern that carries the story, and DP-01 and DP-17 are the two prohibitions that shape it: no second access-log table inside this service, and no lake copy of the entry. DP-11 and DP-13 keep the read a one-hop REST call under the service base; DP-19 is the route it is reached through; DP-06 and DP-07 keep the values in rows and lists rather than in code. This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P4-E1039-CON` exactly as the Work Package fixes them, and the platform libraries arrive with the baseline of `rwb_document`.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P4-E1039-CON and RWB-PLT-E1027-CON stay green, one document content read in SIT produces exactly one `AC-READ` record before the first byte with the case, the document, the actor and no personal data, a read under an active grant carries the grant and the incident, a forced record failure returns 503 with MSG-P7-003 and no bytes, and no class of the service writes an access-log row or reads `rwb_access`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The access record of the read cannot be written, so no byte is served | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller lacks Documents right R, or reads after the grant has ended | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller; the banner shows the end time | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-006 | The document storage does not answer inside 2 s, or the copy is still pending | {system} is not available. Try again in a few minutes. |

The texts are the legacy texts, copied unchanged; this story adds no message id of its own. For MSG-P4-002 the {action} value names the action, for example "read a document", and never a case fact, a document type or a role name. For MSG-GEN-006 the {system} value is "Document storage". Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and no state on a screen. The read is reached from SCR-30 Case documents (RWB-P5-E1026-APP) through the gateway-bff route; the entries are read elsewhere — the access log on SCR-43 Roles and access (Epic 8) and the reads of a case on SCR-38 Decision log query (RWB-E2-005, RWB-P7-E1039-APP). The ACE front-end shell shows the MSG-P4-004 banner while a grant is active, from the session answer, and this story adds no field to that route.

The user-visible consequence is indirect and worth one sentence in the test pack: a document that will not be recorded does not open, and the user sees MSG-P7-003 instead of a file; the successful read looks exactly as it does today.

States of SCR-30 Case documents (CG-ALL-5861): empty, error and no access are Not specified in the source documents (CG-ALL-5861); the other states are taken from Screen Specifications v1, section SCR-30.

States of SCR-38 Decision log query (CG-ALL-5862): empty, error and no access are Not specified in the source documents (CG-ALL-5862); the other states are taken from Screen Specifications v1, section SCR-38.

States of SCR-43 Roles and access (CG-ALL-5863): empty, loading, error and no access are Not specified in the source documents (CG-ALL-5863).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-01 | AC1, BR1, BR3; here AC1, AC6 | End to end | Synthetic case RW-2026-000123 with masked personal fields; the `AC-READ` record of document DOC-2026-0009981 read at 10:15 on 3 December 2026; record committed before the first byte |
| TC-E1-039-02 | AC2, BR4, BR5, BR6, BR8; here AC3 | End to end | Incident INC0004521, IAM request IAM-778812, test clock 10:30 to 14:31; the read at 14:20 marked with the grant, the read at 14:31 refused with MSG-P4-002 — The grant itself belongs to RWB-P4-E1039-APP |
| TC-E1-039-03 | AC3, BR1; here AC1 | End to end | Case list filter returning 37 synthetic cases — The export entry is rwb-case's; this story covers the document read of the same log |
| TC-E1-039-04 | AC4, BR1; here AC1, AC6 | End to end | Document DOC-2026-0009981 read at 10:15 on 3 December 2026: one record with the case, the document, the actor and no field value |
| TC-E1-039-05 | AC5, BR4; here AC3 | End to end | RW-PLATADM test user "U-4104" outside the break-glass group: no grant, no marking — The refusal and its AC-DENY entry belong to RWB-P4-E1039-APP |
| TC-E1-039-06 | AC6, BR4; here AC3 | End to end | An activation with no incident reference and a 12-character reason — The validation is RWB-P4-E1039-APP's; here the read is unaffected because no grant was granted |
| TC-E1-039-07 | AC7, BR2; here AC2 | End to end | Decision-record stub forced to fail during the content read: 503, MSG-P7-003, no bytes, one incident, no partial file |
| TC-E1-039-08 | AC8, BR6; here AC1, AC3 | End to end | Three reads of one case on one day, one under the grant — The query is rwb-decision's; this story produces the three records |
| TC-E1-039-09 | AC9, BR1; here AC5 | Component | RW-PHONECOL test user calling an admin API — The refusal entry is rwb-access's; here a caller without Documents R is refused before the read and no record is written |
| TC-E1-039-10 | AC10; here AC3 | End to end | Two Idempotency-Keys for one active grant — The grant is rwb-access's; here two reads under one grant carry one grant ID |
| TC-E1-039-11 | Access; here AC3, AC5 | Component | A role without Documents R is refused with MSG-P4-002 and no record; the grant end is enforced on the request, not by a job |
| TC-E1-039-12 | Principle 5; here AC2 | NFR | The record write forced to fail during a content read: no bytes, 503, MSG-P7-003, one incident, and the p95 of a logged read inside the 2 s target |
| TC-E1-039-13 | Section 12 operations, events and activities; here AC4 | Component | Contract test of the operations, events and activities of section 12 against the RWB-P4-E1039-CON and RWB-PLT-E1027-CON fakes of 12.8 |
| TC-E1-039-14 | Section 12.7 tables; here AC4 | Component | Boundary test of the tables of section 12.7: each owned table at its boundary and no foreign-schema table read (DP-01); ASM-3438 |
| TC-E1-039-15 | AC7; here AC7 | Component | Content read of DOC-2026-0009981 with no valid session: status 401, no bytes, no record, no incident |
| TC-E1-039-16 | AC8, BR7; here AC8 | Component | Test user "U-4102" holds RW-PLATADM without the Documents right and has an active grant for incident "INC0004521" ending at 14:30: the read at 14:20 refused with MSG-P4-002, no record, and the grant opens no document |
| TC-E1-039-17 | AC9, BR9; here AC9 | Component | Scan of the record, the log lines and the fixtures of a content read of DOC-2026-0009981 for a name, an identity number or a file body: any match fails the build |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. All twelve legacy cases of this key are listed with the slice this story answers: the four cases whose behaviour is the document read keep their legacy wording and gain the half this story proves (TC-E1-039-01, -04, -07 and -12), and the eight cases whose behaviour is the grant, the export, the admin API or the query are kept with their legacy wording and marked with their owner. The `-ITG` copies are not here; they belong to RWB-ITG-E1039-ITG.

### 17. Guardrails

- No business value in code: the decision codes come from LOV-DECISION through the reference-data contract, and the queue name, the cache bound and the timeout are parameter rows. No window, pattern or bound of the break-glass rule is restated in this service.
- No personal data in the record, the log lines, the metrics, the tests or the prompts. The actor is a user id, the document and the case are references, and the type is a code; no name, account number, identity number, extracted value or file body appears anywhere.
- The record is committed before the first byte and in the read's transaction. No after-commit log, no "log it later" queue and no cached serve that skips the record — a read that cannot be recorded is refused.
- No access log of its own (DP-01, BR8): no access-log table in `rwb_document`, no read of `rwb_access`, no call of `GET /admin/access-log`, of the grant operations or of the ledger query. A class that adds one fails the build.
- The grant is accepted, never evaluated or granted here. The grant id and the incident come from the session answer and never from a request field, and the end is re-checked on every request.
- No cross-schema read: the case and the document are values in the `document` row, and the copy is read through the write-once Blob reference, not through another service's table.
- One record per read and one read per record: no batching of reads into one entry, no sampling and no suppression for a service identity or a bulk reader.
- The record carries the reference of the version that was served, so two versions of one document are two facts in the log.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | Business Requirements Epic 1, section 3.4 | FEAT-ACA-07, FEAT-ACA-08, FEAT-ACA-16 | 16 Manage risk, control and compliance | BR1, BR2, BR3, BR8 | TC-E1-039-01, TC-E1-039-04, TC-E1-039-07, TC-E1-039-08, TC-E1-039-09, TC-E1-039-12 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | Business Requirements Epic 1, section 3.4 | FEAT-ACA-09, FEAT-ACA-10 | 16 Manage risk, control and compliance | BR4, BR5, BR6, BR7 | TC-E1-039-02, TC-E1-039-05, TC-E1-039-06, TC-E1-039-10, TC-E1-039-11 |

| Legacy reference | Where it is kept |
|---|---|
| Access event codes `AC-SIGN`, `AC-DENY`, `AC-READ`, `AC-EXPT`, `AC-BGON` and `AC-VERS` in LOV-DECISION | Sections 3, 7 (AC1), 11, 12.8, 17 |
| Legacy AC4, the document read logged before the file is returned | Sections 1, 7 (AC1, AC2), 8 (BR1), 16 (TC-E1-039-04) |
| Legacy AC7 and BR2, the read that cannot be logged returns nothing | Sections 5 (X1), 7 (AC2), 8 (BR2), 16 (TC-E1-039-07, TC-E1-039-12) |
| Legacy AC2 and BR5, BR6, BR8: the grant, its end and the marking | Sections 5 (X2), 7 (AC3), 8 (BR4 to BR7), 16 (TC-E1-039-02) |
| Legacy AC1 and BR3: field IDs and the masking position, never a value | Sections 7 (AC1), 8 (BR3), 11 |
| Legacy sections 10 and 19: the authority of the log and what stays with the IAM, the screens and the data lake | Sections 10, 15, 19 |
| Legacy ACs 1 to 10 and TC-E1-039-01 to -12 | Section 16 and section 19; the whole of them in RWB-P4-E1039-APP and RWB-ITG-E1039-ITG |
| MSG-P4-002, MSG-P4-004, MSG-GEN-006, MSG-P7-003 | Section 14 |

The features the legacy story pairs with these requirements are FEAT-ACA-07 (write every access event to the access log), FEAT-ACA-08 (write the access log into the decision log), FEAT-ACA-09 and FEAT-ACA-10 (break-glass and its review) and FEAT-ACA-16 (answer an access audit query). This slice answers FEAT-ACA-08 and FEAT-ACA-16 for the document content read and FEAT-ACA-09 and FEAT-ACA-10 only as the marking of an entry; the writer, the grant and the read are RWB-P4-E1039-APP's, and the query is RWB-P7-E1039-APP's.

### 19. Out of scope

- The access-event writer, the `GET /admin/access-log` read, the break-glass grant, its end, its two-person rule, its time box and its review: RWB-P4-E1039-CON, RWB-P4-E1039-APP, RWB-P4-E1039-DB and RWB-P4-E1039-OPS.
- The central ledger, the `GET /decision-log` query and the chain verification of rwb-decision: RWB-P7-E1039-APP.
- The entry of a case record read, of a case list export, of a sign-in and of a refusal: rwb-case and rwb-access, not this service.
- The reads of the document store other than the content read — the metadata read of API-P5-003, the search of API-P5-009 with its `DOCUMENT_SEARCH` event (legacy RWB-E1-033) and the intake reads of API-P5-011 and API-P5-012 — which follow their own legacy keys and would wire the same recorder.
- The store, the copy states, the write-once container and the store's own `DOCATT` record: RWB-P5-E1024-APP; the screens that hold the read: RWB-P5-E1026-APP.
- The break-glass request, approval and review records, which are held in the bank IAM, and the scheduled alert for an unreviewed use (Epic 8, FEAT-ADM-12 Manage an incident).
- The decision log query screen SCR-38 (RWB-E2-005) and the roles and access screen SCR-43 (Epic 8).
- The end-to-end proof of the same values across rwb-document, rwb-access and rwb-decision: RWB-ITG-E1039-ITG.
- The `rwb_document` schema baseline, the DP-03 table, the topic `rwb.decision-record.v1`, the observability and the runbook of this service: the platform stories RWB-PLT-E1027-CON, RWB-PLT-E1044-CON and the observability epic.
