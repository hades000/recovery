# RWB-ITG-E1054-ITG Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1054-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-054 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1035-APP, RWB-P5-E1054-APP, RWB-P4-E1054-APP, RWB-P3-E1054-APP, RWB-P7-E1054-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-005, REQ-DCM-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-054 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E1054-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-054 review queue across P5 rwb-document (the queue, intake items, the field patch, the review completion and the document read), P3 rwb-case (the case status behind the closed case), P4 rwb-access (the session scope and the role rights) and P7 rwb-decision (the DOCATT ledger entry collected within five minutes)**, so that **no low-confidence or unmatched document reaches a case without a person checking it, and every correction is kept as a labeled example, proved on the real wave 1 services before wave 1 exits**.

### 2. Business rationale

The legacy story runs the review queue inside the document hub of the monolith. One screen, SCR-31, lists every intake item the pipeline could not type, read or match and every stored document with a field below its threshold; one officer keeps or changes the type, chooses the case, confirms or corrects each marked field, then attaches the item or discards it with a reason. A stored document with a field in review is confirmed or corrected on the same screen and completed with the review operation. Each resolution leaves a labeled example behind for the model evaluations.

In the 19-service target the queue, the items, the field patch and the review completion are P5 rwb-document behaviour inside its own schema and its own service (DP-01). The case is read through the P3 rwb-case case contract instead of the in-process `CaseDirectory` (DP-11), and the officer's team and rights are read through the P4 rwb-access session contract instead of the shared ACE access check (DP-08 dependency on the access owner). The document type list in force and the review reasons are reference data read through the P3 reference-data contract (DP-07), and the attach writes its `DOCATT` record locally in rwb_document with the change in one transaction, then P7 rwb-decision collects it into the central ledger within five minutes (DP-03; Architecture v5 slide 28). The document events travel on `rwb.document.events.v1` through the outbox and inbox library with CloudEvents (DP-09). Every path moves to the per-service base of DP-13, and the screen is reached through gateway-bff (DP-19) but is not built or tested here.

This ITG story owns no legacy acceptance criterion. Legacy AC1 to AC17 sit at component level with RWB-P5-E1054-APP, which is why the `acs` list of the work package is empty for this slice; the sixteen scenarios of section 7 are the integration proof of the same legacy behaviour across the four owners, and every business value in them is a legacy value. The suite provides no REST operation, publishes no event and owns no table; it consumes the ten operations of section 12.2 and the three events of section 12.4 and nothing else.

Two of the five integration dependencies exist only because the target separates concerns the monolith held in one call: RWB-P3-E1035-APP carries the case status that decides the closed case of AC8, and RWB-P4-E1054-APP carries the right and the scope that decide the refusals of AC11 and AC15. Without them the closed case and the out-of-scope refusals would be proved against a fixture and not against the services that own the facts.

The resolve call carries the item version returned by the read, and the labeled example is read through the resolved item and its fields on the P5 review contract (ASM-0487; ASM-0490); neither value is invented by the suite.

### 3. Preconditions

- RWB-P5-E1054-APP is done: the review queue, the intake item reads and content, the resolve operation, the field patch, the review completion and the document read are in SIT on P5 rwb-document.
- RWB-P3-E1054-APP is done: the case read of the suite returns the case, its status and its owner through GET /api/recovery/case/v1/cases/{caseId}.
- RWB-P3-E1035-APP is done: the case status returned by the P3 case contract is the status the closed-case rule reads.
- RWB-P4-E1054-APP is done: the session contract returns the officer's role, team and scope, and the role-rights check of Documents R and Documents U is enforced on the P5 operations.
- RWB-P7-E1054-APP is done: the `DOCATT` records written locally in rwb_document are collected into the central ledger of P7 rwb-decision within five minutes and are readable through the decision-log operation.
- The published contracts of P5, P3, P4 and P7 are deployed in SIT under their own per-service bases behind gateway-bff.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic cases RW-2026-000201, RW-2026-000202, RW-2026-000203 and RW-2026-000150, its synthetic users, teams LIT-BKK and HP-NE and its synthetic files.
- DOCTYPE-2026.11 is in force and the classify_threshold of every type is 0.8000, loaded as reference data and read through the P3 reference-data contract.
- REVIEW_TEAM_UNATTACHED is "LIT-BKK" for the test, REVIEW_DATE_MIN is 2000-01-01, REVIEW_DATE_MAX is 2100-12-31 and REVIEW_PAGE_SIZE is 50, loaded as data rows of the document hub.
- The synthetic users, roles and scopes of section 10 are loaded: the litigation officer with RW-LITOFF in team LIT-BKK, a case owner with RW-CASEOWN, a team manager with RW-TEAMMGR holding Documents R only, and a center of excellence analyst with RW-COE holding Documents R.
- The feature flag `rwb.dochub.review` is on.
- No production data is used and no production connection is opened, and the release date 30 November 2026 is tentative; a date is not a precondition of this story.
- The story has no build dependency, so it is ready on Day 1 and waits only on its five integration dependencies.

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, users, teams and files of the harness RWB-ITG-W1J01-ITG; no production data is used. Case RW-2026-000201 is open and owned by the case owner, RW-2026-000202 and RW-2026-000203 are open, and RW-2026-000150 is closed.
2. Harness: signs in as the synthetic litigation officer of section 10 through gateway-bff, holds the RW-LITOFF role with team LIT-BKK and reads the session through GET /api/recovery/access/v1/me/session.
3. Harness: waits on `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` before it asserts any item or document, and records the elapsed time of each wait.
4. Harness: reads the queue through GET /api/recovery/document/v1/review-items and asserts, for each row, the kind, the item or document ID, the case number, the review reason, the predicted type, the two candidates, the confidence, the received time and the version; it asserts the order and the scope against the session of step 2.
5. Harness: opens one item through GET /api/recovery/document/v1/intake-items/{intakeItemId} and its file and OCR text pages through GET /api/recovery/document/v1/intake-items/{intakeItemId}/content, and asserts the masked fields, the fields in REVIEW and the version.
6. Harness: resolves the items through POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action SET_TYPE, ATTACH or DISCARD at the version read in the previous step, and asserts the stored document through GET /api/recovery/document/v1/documents/{documentId} and its case status through GET /api/recovery/case/v1/cases/{caseId}.
7. Harness: confirms and corrects a stored document's fields through PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} and completes the review through POST /api/recovery/document/v1/documents/{documentId}/review, then repeats the same patch to prove it changes nothing.
8. Harness: reads the `DOCATT` entries through GET /api/recovery/decision/v1/decision-log?caseId={caseId}, asserts one entry per attach with the confirmed type and the approver, and measures the collection time against the five-minute target.
9. Harness: runs the refusals and the conflicts — the empty correction, the type not in force, the date outside the allowed range, the field still in review, the closed case, the stale version, the duplicate file, the item and document outside the scope, the discard without a reason and the role holding Documents R only.
10. Harness: proves the failed local record with the agreed test-only fault switch on the P5 local-record write, restores the switch and the flag, writes the evidence report and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Correct is chosen with an empty value | 422; nothing saved; the field keeps its value | MSG-GEN-001 | AC4 |
| X2 | The chosen type is not in the type list in force | 422; nothing saved; the item keeps its predicted type | MSG-P5-006 | AC5 |
| X3 | A corrected date is outside the allowed range | 422; nothing saved; the field keeps its extracted value | MSG-GEN-002 | AC6 |
| X4 | Attach or complete with a field still in REVIEW | 422; nothing stored; the item keeps its outcome | MSG-GEN-001 | AC7 |
| X5 | The chosen case is closed, as read through the P3 case contract | 422; nothing stored; the item stays in the queue | MSG-P5-005 | AC8 |
| X6 | Another officer saved the same item first | 409; the officer reloads and resends at the new version | MSG-GEN-004 | AC9 |
| X7 | The same file is already on the chosen case | The item is linked to the existing document; no second document | MSG-P5-024 | AC10 |
| X8 | Discard without a reason | 422; the item stays in the queue | MSG-GEN-001 | AC13 |
| X9 | No item in the officer's queue | The queue answers with an empty page and the empty message | None | AC14 |
| X10 | An item or document outside the officer's scope | 404; nothing is returned | MSG-P4-003 | AC11 |
| X11 | The same confirmation is sent twice | The second call returns the saved field; nothing changes | None | AC3 |
| X12 | The user holds Documents R only and resolves an item | 403; the item stays in the queue | MSG-P4-002 | AC15 |
| X13 | The local DOCATT record cannot be written on attach | Nothing stored; the item unchanged; 503; an incident is raised; no ledger entry | MSG-P7-003 | AC16 |
| X14 | A consumed call exceeds the 2 s timeout or returns a server error | The call is retried once under the suite policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC12 |
| X15 | The fixture set does not match the harness expectations, or a service returns no fixture answer | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the five APP stories and the published contracts of P5, P3, P4 and P7, not their source code |
| Negotiable | The review team, the date limits, the page size and the type list are data rows or harness properties; the story fixes the assertions and the call set |
| Valuable | The one screen that keeps a wrong type or a wrong hearing date off a case is proved against the real owners of the queue, the case status, the scope and the ledger before wave 1 exits |
| Estimable | One suite module, one fixture pack of synthetic items and documents, one item-version control, one fault switch and one evidence report |
| Small | Sixteen scenarios over four services and one shared ledger topic; no service code and no schema change |
| Testable | Every scenario asserts a contract response, a stored field, a document, an outcome, an event, a message or the ledger; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-document, rwb-case, rwb-access and rwb-decision are deployed in SIT with their published contracts behind gateway-bff
    Given DOCTYPE-2026.11 is in force and the classify_threshold of every type is 0.8000
    Given REVIEW_TEAM_UNATTACHED is "LIT-BKK" for this test
    Given a litigation officer with role RW-LITOFF in team "LIT-BKK" with team scope
    Given the RWB-ITG-W1J01-ITG synthetic cases, users, teams and files are loaded and no production data is used

  Scenario: AC1 The queue lists a low-confidence item with its two candidates and its scope (new, D-RCV-60)
    Given intake item "IN-0101" on which classification returned "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100
    Given its review_reason is "LOW_CONFIDENCE" and it names no case
    When the officer reads GET /api/recovery/document/v1/review-items through gateway-bff
    Then the page lists "IN-0101" with reason "LOW_CONFIDENCE", predicted type "COURT_NOTICE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21"
    Then the row carries confidence 0.6200, the received time and the version, and the item is in the run of the team "LIT-BKK" read through GET /api/recovery/access/v1/me/session

  Scenario: AC2 A corrected item attaches as one document with one DOCATT record and one labeled example (new, D-RCV-60)
    Given intake item "IN-0101" in the review queue with hearing_date "2026-12-15" in state "REVIEW" at version 3
    When the officer sets type "COURT_NOTICE", corrects hearing_date to "2026-12-16", confirms the other fields, chooses case "RW-2026-000201" and calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH and version 3
    Then the document on "RW-2026-000201" has type "COURT_NOTICE" and a hearing_date field with field_value "2026-12-16", extracted_value "2026-12-15", state "CORRECTED" and confirmed_by the officer's user ID, read through GET /api/recovery/document/v1/documents/{documentId}
    Then the document review_status is "CORRECTED" and "IN-0101" has review_outcome "ATTACHED"
    Then exactly one DOCATT entry for the document is returned by GET /api/recovery/decision/v1/decision-log?caseId={caseId}, and it is collected into the central ledger of P7 rwb-decision within five minutes
    Then the labeled example of "IN-0101" is readable through GET /api/recovery/document/v1/intake-items/{intakeItemId} with predicted type "COURT_NOTICE", confirmed type "COURT_NOTICE", extracted value "2026-12-15" and confirmed value "2026-12-16"

  Scenario: AC3 A stored document field is confirmed, and the same confirmation sent twice changes nothing (new, D-RCV-60)
    Given document "DOC-0103" on case "RW-2026-000202" has black_case_no "Por 2001/2569" in state "REVIEW" and review_status "PENDING"
    When the officer confirms black_case_no through PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} with confirmed true and value "Por 2001/2569"
    And the officer completes the review through POST /api/recovery/document/v1/documents/{documentId}/review with action COMPLETE
    Then black_case_no has state "CONFIRMED" and confirmed_by the officer's user ID
    Then the document review_status is "CONFIRMED"
    When the same PATCH with confirmed true and the same value is sent again
    Then the response is 200 with the saved field
    Then confirmed_by and updated_at are unchanged

  Scenario: AC4 An empty correction is refused (new, D-RCV-60)
    Given document "DOC-0103" has court_name in state "REVIEW"
    When the officer chooses Correct on court_name through PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} with an empty value
    Then the response is 422 with MSG-GEN-001 naming "Court name"
    Then court_name is unchanged

  Scenario: AC5 A type not in force is refused (new, D-RCV-60)
    Given intake item "IN-0104" in the review queue
    When the officer sets the type to "PAYSLIP" through POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action SET_TYPE
    Then the response is 422 with MSG-P5-006 naming "PAYSLIP"
    Then the item keeps its predicted type

  Scenario: AC6 A date outside the allowed range is refused (new, D-RCV-60)
    Given REVIEW_DATE_MIN is 2000-01-01 and REVIEW_DATE_MAX is 2100-12-31
    When the officer corrects hearing_date on "IN-0101" to "2569-12-16"
    Then the response is 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31"
    Then hearing_date keeps its extracted value

  Scenario: AC7 Attach with a field still in review is refused (new, D-RCV-60)
    Given intake item "IN-0105" has two fields in state "REVIEW" and the officer has confirmed one
    When the officer calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH and the item version
    Then the response is 422 with MSG-GEN-001 naming the field still in review
    Then the system stores no document and "IN-0105" keeps its review_outcome

  Scenario: AC8 A closed case is refused through the P3 case status (new, D-RCV-60)
    Given intake item "IN-0106" with review_reason "CASE_CLOSED" and candidate case "RW-2026-000150"
    Given GET /api/recovery/case/v1/cases/{caseId} returns status "Closed" for "RW-2026-000150" from the synthetic SIT case seeded through the P3 contract
    When the officer chooses case "RW-2026-000150" and calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH
    Then the response is 422 with MSG-P5-005 naming "RW-2026-000150"
    Then the system stores no document

  Scenario: AC9 Two officers on one item (new, D-RCV-60)
    Given two officers opened intake item "IN-0107" at version 3
    Given the first officer attached it, so the item is at version 4
    When the second officer calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH and version 3
    Then the response is 409 with MSG-GEN-004
    Then one document exists for "IN-0107"

  Scenario: AC10 The same file already on the chosen case (new, D-RCV-60)
    Given document "DOC-0109" on case "RW-2026-000203" holds a file with hash "H109"
    Given intake item "IN-0109" holds the same file
    When the officer attaches "IN-0109" to "RW-2026-000203" through POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH
    Then the system stores no second document and "IN-0109" is linked to "DOC-0109"
    Then the response carries MSG-P5-024 naming "DOC-0109"

  Scenario: AC11 An item or document outside the officer's scope is refused through the P4 scope (new, D-RCV-60)
    Given document "DOC-0111" belongs to a case of team "HP-NE"
    Given the session read of GET /api/recovery/access/v1/me/session returns team "LIT-BKK" with team scope for the officer
    When the officer calls GET /api/recovery/document/v1/documents/{documentId} for "DOC-0111"
    Then the response is 404 with MSG-P4-003
    Then the same 404 with MSG-P4-003 is returned when the officer reads an intake item whose candidate cases are all of team "HP-NE" through GET /api/recovery/document/v1/intake-items/{intakeItemId}

  Scenario: AC12 An unreadable item is discarded with a reason and the file is retained (new, D-RCV-60)
    Given intake item "IN-0110" with review_reason "UNREADABLE_FILE"
    When the officer calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action DISCARD and reason "Blank page from the branch scanner"
    Then "IN-0110" has review_outcome "DISCARDED" with the reason, the officer's user ID and the time
    Then the file of "IN-0110" is still returned by GET /api/recovery/document/v1/intake-items/{intakeItemId}/content
    Then "IN-0110" leaves the queue and no document is stored

  Scenario: AC13 Discard without a reason is refused (new, D-RCV-60)
    Given intake item "IN-0112" with review_reason "RESCAN"
    When the officer calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action DISCARD and an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "IN-0112" stays in the queue

  Scenario: AC14 The queue lists items in scope oldest first and shows the empty state (new, D-RCV-60)
    Given 3 review items for team "LIT-BKK" received on 2 November, 4 November and 3 November
    Given 2 review items of team "HP-NE"
    When the officer reads GET /api/recovery/document/v1/review-items
    Then 3 items show, in the order 2 November, 3 November, 4 November
    Then no item of team "HP-NE" shows
    When no review item is left for team "LIT-BKK"
    Then the page holds no row and the empty message "No documents are waiting for review."

  Scenario: AC15 A role with Documents R only is refused (new, D-RCV-60)
    Given a user in team "LIT-BKK" holding role RW-TEAMMGR with Documents R only
    When the user calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH
    Then the response is 403 with MSG-P4-002
    Then the item stays in the queue

  Scenario: AC16 A failed local DOCATT record stops the attach (new, D-RCV-60)
    Given the local DOCATT record write of P5 rwb-document is switched to fail by the agreed test-only fault switch
    When the officer calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action ATTACH
    Then no document is stored and the item keeps its review_outcome
    Then the response is 503 with MSG-P7-003
    Then an incident is raised
    Then GET /api/recovery/decision/v1/decision-log?caseId={caseId} returns no DOCATT entry for the item
    And the fault switch is restored
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The queue holds intake items with a review_reason and no review_outcome, and documents with review_status PENDING; both are P5 rwb-document rows read through the P5 contract | RWB-E1-054 BR1; RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-032; LOV-REVIEW |
| BR2 | An item with no case is shown to the review team named in REVIEW_TEAM_UNATTACHED and to roles with scope All; an item with candidate cases and a document are shown by the case scope, and the scope comes from the P4 rwb-access session | RWB-E1-054 BR2; permission matrix scope; CTL-09; REVIEW_TEAM_UNATTACHED |
| BR3 | Attach and complete are allowed only when no field is in REVIEW, the type is in force and the case is open, the last read through the P3 case status | RWB-E1-054 BR3; LOV-REVIEW; DocumentTypeCatalog; DF-CAS-005 |
| BR4 | review_status becomes CONFIRMED when the type, the case and the values are kept, and CORRECTED when any of them changes | RWB-E1-054 BR4; LOV-REVIEW |
| BR5 | A corrected value keeps the extracted value in extracted_value and the corrector in confirmed_by | RWB-E1-054 BR5; DF-DOC-017; FEAT-DCM-11 |
| BR6 | The attach is stored by P5 rwb-document in one transaction with its local DOCATT record and the file in the write-once container; P7 rwb-decision collects the record into the central ledger within five minutes | RWB-E1-054 BR6; DP-03; ADR-022; Architecture v5 slide 28 |
| BR7 | Each resolved item is a labeled example that holds the predicted type, the confirmed type, the extracted value and the corrected value | RWB-E1-054 BR7; FEAT-AGT-04; FEAT-DCM-11 |
| BR8 | A change saved against an old version is refused with 409, and a repeat of the same confirmation changes nothing | RWB-E1-054 BR8; MSG-GEN-004 |
| BR9 | A discarded item keeps its file in the intake container and records the reason and the person | RWB-E1-054 BR9; REQ-DCM-019 |
| BR10 | Field values are masked unless the role may see them, by the masking policy of P4 rwb-access | RWB-E1-054 BR10; DF-DOC-015; CTL-11; DL26 |
| BR11 | No service reads another service's tables: the suite reads the queue, the items, the documents, the case, the session and the ledger only through the owner's contract, one hop with a 2 s timeout | DP-01; DP-11; ADR-020 (new, D-RCV-60) |

### 9. State transitions

None for the case status. This story changes no case status and reads it only to prove the closed case of AC8. The transitions below are the ones the suite proves; every one of them is written by its owner, never by the suite.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| document_intake | item with a review_reason and no outcome | Attach | BR3 passes and the local record is written | review_outcome ATTACHED |
| document_intake | item with a review_reason and no outcome | Discard | A reason is given | review_outcome DISCARDED |
| document | review_status PENDING | Review completed | Type, case and values kept | review_status CONFIRMED |
| document | review_status PENDING | Review completed | The type, the case or a value changed | review_status CORRECTED |
| document_field | state REVIEW | Confirm or Correct | The value passes the type and range check | state CONFIRMED or CORRECTED |
| decision_log_entry | no record | Attach | The local write succeeds | One DOCATT record, collected by P7 within five minutes |

A discarded item leaves the queue and keeps its file. A refused call of section 5 leaves every state unchanged.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report; no service right of its own |
| RW-LITOFF, litigation officer | Lists, reads, corrects, attaches and discards review items in scope (Documents CRU) |
| RW-CASEOWN, case owner | Lists, reads, corrects and attaches review items of own cases (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the queue for the team (Documents R) and cannot correct, attach or discard |
| RW-COE, center of excellence analyst | Reads the resolved items as labeled examples (Documents R) |
| P5 rwb-document owner | Owns the queue, the intake items, the documents, the fields and the local DOCATT record |
| P3 rwb-case owner | Owns the case, its status and its owner, served by the case contract |
| P4 rwb-access owner | Owns the roles, the team scope, the masking policy and the session contract |
| P7 rwb-decision owner | Owns the central decision ledger and the collection of the DOCATT records |

The synthetic users of the run are the litigation officer of team LIT-BKK, a case owner, a team manager holding Documents R only and a center of excellence analyst. No other role and no person is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Owner and access |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | P3 rwb-case; read through GET /api/recovery/case/v1/cases/{caseId} |
| DF-CAS-005 | recovery_case | status | P3 rwb-case; read through the case contract, to prove the closed case of AC8 |
| DF-DOC-001 to DF-DOC-011 | document | all fields | P5 rwb-document; written by P5 on attach, read through GET /api/recovery/document/v1/documents/{documentId} |
| DF-DOC-008 | document | review_status | P5 rwb-document; read only, PENDING to CONFIRMED or CORRECTED |
| DF-DOC-015 | document_field | field_value | P5 rwb-document; read only, masked by the role |
| DF-DOC-017 | document_field | confirmed_by | P5 rwb-document; read only |
| DF-DOC-034 | document_field | extracted_value | P5 rwb-document; read only |
| DF-DOC-070 | document_intake | predicted_type | P5 rwb-document; read only |
| DF-DOC-072 | document_intake | type_candidates | P5 rwb-document; read only |
| DF-DOC-076 | document_intake | candidate_case_ids | P5 rwb-document; read only |
| DF-DOC-077 | document_intake | extracted_fields | P5 rwb-document; read only, masked by the role |
| DF-DOC-080 | document_intake | review_reason | P5 rwb-document; read only |
| DF-DOC-081 | document_intake | review_outcome | P5 rwb-document; read only, ATTACHED or DISCARDED |
| DF-DOC-082 | document_intake | resolved_by | P5 rwb-document; read only |
| DF-DOC-083 | document_intake | resolved_at | P5 rwb-document; read only |
| DF-DOC-084 | document_intake | discard_reason | P5 rwb-document; read only |
| DF-DOC-089 | document_text | text_content | P5 rwb-document; read only through the content path of the item |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Written locally by P5 in rwb_document and held centrally by P7 rwb-decision; read through GET /api/recovery/decision/v1/decision-log?caseId={caseId} |
| Standard column | document_field, document_intake | state, version | P5 rwb-document; read only, the version is sent back on every resolve and patch |
| Standard column | document_intake | version, sent on the resolve call; the resolved item and its fields are the labeled example | P5 rwb-document; read only (ASM-0487; ASM-0490) |

The legacy story writes these fields in one module; in the target they are written by P5 rwb-document inside its own schema, the case status is owned by P3 rwb-case and the ledger entry by P7 rwb-decision, and the suite only reads them through the four contracts (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/document/v1/review-items | P5 rwb-document | Read the queue with the reason, the predicted type, the two candidates, the confidence, the age and the version of each row, oldest first |
| GET /api/recovery/document/v1/intake-items/{intakeItemId} | P5 rwb-document | Read one item with its candidates, candidate cases, masked fields, review_outcome, resolved_by, resolved_at and version |
| GET /api/recovery/document/v1/intake-items/{intakeItemId}/content | P5 rwb-document | Read the file and the OCR text pages of an item, including a discarded one |
| POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve | P5 rwb-document | Set the type, attach the item to a case or discard it with a reason, at the item version |
| PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} | P5 rwb-document | Confirm or correct one field of a stored document, and repeat the same confirmation |
| POST /api/recovery/document/v1/documents/{documentId}/review | P5 rwb-document | Complete the review of a stored document with action COMPLETE |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the document, its type, its fields with state and values, and its review_status |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the case, its status and its owner, to prove the closed case of AC8 |
| GET /api/recovery/access/v1/me/session | P4 rwb-access | Read the officer's role, team, scope and rights, and prove the refusals of AC11 and AC15 |
| GET /api/recovery/decision/v1/decision-log?caseId={caseId} | P7 rwb-decision | Read the DOCATT entries of the case and measure the five-minute collection |

Every call is one hop from gateway-bff with a 2 s timeout and a retry of GET only (ADR-020, DP-11). The resolve call carries the action, the type, the case, the fields, the reason and the item version returned by the read (ASM-0487).

#### 12.3 Events published

None. The suite publishes no event; every event of the chain is published by its owning service through its own outbox.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | The document is stored; the suite waits for it before it asserts the document, its fields and the DOCATT entry |
| rwb.document.DocumentFieldsExtracted.v1 | rwb.document.events.v1 | P5 rwb-document | The fields of the item or the document were extracted or re-extracted; the suite waits for it before it asserts a field state |
| DecisionRecorded | rwb.decision-record.v1 | P5 rwb-document, with the central ledger in P7 rwb-decision | The DOCATT record is collected into the ledger inside the five-minute target |

The suite consumes no other event and produces none. A duplicate delivery is absorbed by the inbox of the consumer and changes no assertion.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Carries the intake of each item under test and the re-extraction of a changed type; the suite observes its run and asserts nothing about its history |

The suite starts no workflow of its own and reads no workflow history through an owner's schema. It waits on the two document events and observes the workflow through its published interface only.

#### 12.6 Schedules

None. The review queue has no Schedule in the target: the queue is a read of the P5 rows and the re-extraction of a changed type is part of the intake workflow. The suite waits on no Schedule and moves no clock.

#### 12.7 Tables owned

None (DP-01). document, document_field, document_intake, document_text, document_type and document_hub_parameter are P5 tables, recovery_case is a P3 table, role and permission data are P4 tables, and decision_log_entry is written locally by P5 and held centrally by P7. The suite owns no table and never reads another service's schema.

#### 12.8 Contract fakes

External controls and synthetic SIT fixtures only; no service contract is faked.

| Element | Kind | Use |
|---|---|---|
| P5 local-record fault switch | Agreed test-only switch in the P5 configuration | Forces the local DOCATT record write to fail for AC16, and is restored at the end of the run |
| P3 closed case | Synthetic SIT row seeded through the P3 case contract | Case RW-2026-000150 with status Closed for AC8; the real P3 contract answers |
| P4 scoped users | Synthetic SIT users and roles seeded through the P4 access contract | The HP-NE scope of AC11 and the RW-TEAMMGR rights of AC15; the real P4 session answers |
| Clock | Harness control | Measures the age column and the five-minute collection target |

No service contract is faked: every call of section 12.2 goes to the real SIT service on its published wave 1 contract, and the queue, the items, the documents, the fields and the ledger are always the real P5 and P7 answers.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 10 |
| Kafka | 0 | 3 |
| Temporal | 0 | 1 observed |
| File | 0 | 1 as needed |

The only file read is the item content through the P5 content call; the suite opens no file share and no container of its own, and writes no file except its evidence report.

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the sixteen scenarios against SIT and holds no service code |
| Fixture pack | Test data | Synthetic intake items, stored documents, cases, teams, users and files with the legacy values of section 7 |
| Item-version control | Harness control | Reads the item version before a resolve and sends a stale and a repeated version for AC9 and AC3, then restores the item |
| Scope and rights control | Harness control | Holds the LIT-BKK session, the HP-NE document and the RW-TEAMMGR rights of AC11 and AC15 |
| Ledger assertion | Assertion | Reads the DOCATT entry of each attach and measures the collection time against the five-minute target of 300 seconds |
| Evidence report | Report | Records per scenario the item and document IDs, the field states and values, the outcome, the DOCATT entry, the events and their times, the statuses and the messages |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | document, document_field, document_intake, document_text, document_type and document_hub_parameter stay in rwb_document under P5, recovery_case in rwb_case under P3 and the ledger in rwb_decision under P7; the suite asserts through the four contracts only |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic rwb.decision-record.v1 | H RWB-PLT-E1027-CON | On RWB-P5-E1054-APP and RWB-P7-E1054-APP; the suite only waits for the collected record and measures the five minutes |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On RWB-P5-E1054-APP for the type list in force and the review reasons; the suite sends the codes as data |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On RWB-P5-E1054-APP for DocumentStored and DocumentFieldsExtracted and on every owner for DecisionRecorded; the suite consumes them |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The ten consumed REST operations of section 12.2, one hop from gateway-bff |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every path sits under /api/recovery/document/v1 for P5, /api/recovery/case/v1 for P3, /api/recovery/access/v1 for P4 and /api/recovery/decision/v1 for P7 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P5-E1054-APP for the review outcome columns and the two review indexes; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; SCR-31 and SCR-30 are not built or tested here |

The dependency-added column records the build dependency of the owning story. Those H and C dependencies belong to the owning APP stories, not to this suite. This story's H, C and X lists are exactly those of the metadata table — no H, no C and no X — and its I list is the five integration dependencies RWB-P3-E1035-APP, RWB-P5-E1054-APP, RWB-P4-E1054-APP, RWB-P3-E1054-APP and RWB-P7-E1054-APP. An ITG story waits on no build of its own.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5, P3, P4 and P7 through gateway-bff.
2. Build the fixture pack: the four synthetic cases, the two teams, the four synthetic users, the intake items IN-0101 to IN-0112, the documents DOC-0103, DOC-0109 and DOC-0111, the file with hash H109 and the OCR text and field values of section 7, all with the legacy values.
3. Implement AC1 and AC14 with the queue read, the row assertions and the order and scope assertions against the session read.
4. Implement AC2 with the attach at the item version, the document read, the DOCATT entry, the five-minute collection and the labeled example through the item read.
5. Implement AC3 and AC17's behaviour in one scenario with the field patch, the review completion and the repeated patch, and assert that confirmed_by and updated_at do not move.
6. Implement AC4 to AC8 with the four refusals of the queue and the document path: the empty correction, the type not in force, the date outside the allowed range, the field still in review and the closed case read through the P3 status.
7. Implement AC9 to AC13 with the item-version control, the duplicate file link, the two scope refusals and the discard with and without a reason, and assert that no document is stored where the story says so.
8. Implement AC15 with the RW-TEAMMGR rights from the P4 session, then AC16 through the agreed test-only fault switch on the P5 local-record write; assert the 503, the unchanged item, the incident and the empty ledger, restore the switch and the flag, and write the evidence report.

Done when: all twenty test cases pass in SIT against the published wave 1 contracts of P5, P3, P4 and P7, the evidence report shows for each scenario the response, the field state, the document, the outcome and the ledger entry that prove it, every DOCATT entry is collected into the ledger inside the five-minute target, and no service code or schema was changed by this story apart from the agreed test-only fault switch.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | An item or document is in the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P5-005 | The chosen case is closed | Case {case} is closed. Choose an open case. |
| MSG-P5-006 | The chosen type is not in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-P5-024 | The file is already on the case | This file is already on the case as {document}. |
| MSG-GEN-001 | Empty value, empty reason, or field still in review | Enter {field}. |
| MSG-GEN-002 | Date outside the allowed range | {field} must be between {min} and {max}. |
| MSG-GEN-004 | Saved against an old version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | Field, attach or discard saved | Saved. |
| MSG-P7-003 | Decision log write failed on attach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Caller lacks Documents U | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Item or document outside the caller's scope | This case is not in your scope. |

The message IDs and the wording are copied from RWB-E1-054. No new message ID is added by this story. Thai text for each message follows decision DL10.

The ledger line of the evidence report carries no message ID: {stored} of {expected} attachments of case {caseId} were stored with their DOCATT entry, and the slowest entry was collected into the central ledger of rwb-decision in {seconds} seconds against the five-minute target of 300 seconds.

### 15. Screens and states

No screen is built or tested in this story. The suite reaches the services through gateway-bff (DP-19) and reads the same states the screens render.

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the queue loads |
| SCR-31 Document review queue | List | Review items oldest first with the reason, the candidates, the confidence and the age; one item opens with the file, the OCR text, the type chooser, the case chooser and the fields marked for review |
| SCR-31 Document review queue | Reviewed | After attach, discard or complete the item leaves the list and MSG-GEN-005 shows |
| SCR-31 Document review queue | Empty | "No documents are waiting for review." |
| SCR-30 Case documents | List | The attached document with its confirmed or corrected type and fields |

The four states of SCR-31 and the one state of SCR-30 are the only screens of the legacy story and no screen is added by this story.

### 16. Test cases

The ITG copies keep the legacy test case ids of RWB-E1-054 and are re-pointed at the scenarios of section 7; the twentieth row is the new end-to-end copy of the failed local record.

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-054-01-ITG | AC1, BR1 | Integration | Intake item IN-0101 classified COURT_NOTICE 0.6200 and DEMAND_LETTER 0.2100 with reason LOW_CONFIDENCE; real services on the wave 1 contracts |
| TC-E1-054-02-ITG | AC2, BR4, BR5, BR6, BR7 | End to end | Hearing date corrected from 2026-12-15 to 2026-12-16 on synthetic case RW-2026-000201; one DOCATT entry inside five minutes; real services on the wave 1 contracts |
| TC-E1-054-03-ITG | AC3, BR4 | Integration | Document DOC-0103 with black_case_no "Por 2001/2569" in REVIEW; real services on the wave 1 contracts |
| TC-E1-054-04-ITG | AC4 | Contract | Empty correction on court_name of DOC-0103, refused with MSG-GEN-001 naming Court name; real services on the wave 1 contracts |
| TC-E1-054-05-ITG | AC5, BR3 | Contract | Type PAYSLIP not in force, refused with MSG-P5-006; real services on the wave 1 contracts |
| TC-E1-054-06-ITG | AC6 | Contract | 2569-12-16 entered as a Gregorian year against 2000-01-01 and 2100-12-31, refused with MSG-GEN-002 naming Hearing date; real services on the wave 1 contracts |
| TC-E1-054-07-ITG | AC7, BR3 | Integration | IN-0105 with two fields in REVIEW and one confirmed; attach refused with MSG-GEN-001; real services on the wave 1 contracts |
| TC-E1-054-08-ITG | AC8, BR3 | Integration | IN-0106 with reason CASE_CLOSED and candidate case RW-2026-000150 returned as Closed by the P3 status; refused with MSG-P5-005; real services on the wave 1 contracts |
| TC-E1-054-09-ITG | AC9, BR8 | Integration | Two sessions on IN-0107 at version 3 and 4; the second refused with 409 and MSG-GEN-004, one document; real services on the wave 1 contracts |
| TC-E1-054-10-ITG | AC10 | Integration | IN-0109 carrying the file with hash H109 already held by DOC-0109 on RW-2026-000203; no second document, MSG-P5-024; real services on the wave 1 contracts |
| TC-E1-054-11-ITG | AC11, BR2 | Integration | DOC-0111 of team HP-NE read by the LIT-BKK officer; 404 with MSG-P4-003; real services on the wave 1 contracts |
| TC-E1-054-12-ITG | AC12, BR9 | End to end | IN-0110 with reason UNREADABLE_FILE discarded with "Blank page from the branch scanner"; the file is still read and the item leaves the queue; real services on the wave 1 contracts |
| TC-E1-054-13-ITG | AC13 | Contract | IN-0112 with reason RESCAN discarded with an empty reason; 422 with MSG-GEN-001 naming Reason, the item stays; real services on the wave 1 contracts |
| TC-E1-054-14-ITG | AC14, BR2 | Integration | Five review items across teams LIT-BKK and HP-NE received on 2, 3 and 4 November; order and scope asserted; real services on the wave 1 contracts |
| TC-E1-054-15-ITG | AC14 | Integration | No review item for team LIT-BKK; the empty message "No documents are waiting for review."; real services on the wave 1 contracts |
| TC-E1-054-16-ITG | AC11, BR10 | Contract | Item whose candidate cases are all of team HP-NE read by the LIT-BKK officer; 404 with MSG-P4-003; real services on the wave 1 contracts |
| TC-E1-054-17-ITG | AC3 | Integration | The same confirmation of black_case_no sent twice; 200 with the saved field and confirmed_by and updated_at unchanged; real services on the wave 1 contracts |
| TC-E1-054-18-ITG | AC15 | Contract | User in team LIT-BKK holding RW-TEAMMGR with Documents R only calling the resolve with action ATTACH; 403 with MSG-P4-002; real services on the wave 1 contracts |
| TC-E1-054-19-ITG | AC16, BR6 | NFR | Local DOCATT record write forced to fail on attach; no document, the item unchanged, 503 with MSG-P7-003, incident raised; real services on the wave 1 contracts |
| TC-ITG-E1054-ITG-20 | AC16, BR6, BR11 | End to end | The same failed local record proved end to end: the P7 decision-log of the case holds no DOCATT entry for the item and the fault switch is restored; real services on the wave 1 contracts |

Every test uses synthetic data and runs against the real services on the wave 1 contracts. The legacy full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same legacy test case id.

### 17. Guardrails

- No business value in code: the review team, the date limits, the page size and the type list come from data rows and from the reference-data contract, never from the suite source.
- No personal data in logs, events, evidence or fixtures: the OCR text and the field values are masked by role and never logged, and every case, item, document, file and user of the suite is synthetic.
- No cross-service table read: the queue, the items, the documents, the fields, the case, the session and the ledger are read through the owner's contract, and the suite owns no table.
- One hop and a 2 s timeout on every consumed call, with a retry of GET only (ADR-020, DP-11).
- The type list in force and the closed case are never assumed by the suite: the first comes from the reference data and the second from the P3 case status.
- A discarded item keeps its file; nothing is ever removed silently (REQ-DCM-019).
- The local-record fault switch is test-only, agreed with the service owner, and restored at the end of the run.
- The P3 closed case and the P4 scoped users are synthetic SIT rows seeded through the published P3 and P4 contracts, and no real contract is replaced in the normal path.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG; no production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue, checked by a person | GET /api/recovery/document/v1/review-items, GET /api/recovery/document/v1/intake-items/{intakeItemId}, rwb.document.DocumentFieldsExtracted.v1, MSG-P5-003 | TC-E1-054-01-ITG, TC-E1-054-02-ITG, TC-E1-054-03-ITG, TC-E1-054-04-ITG, TC-E1-054-05-ITG, TC-E1-054-06-ITG, TC-E1-054-07-ITG, TC-E1-054-08-ITG, TC-E1-054-10-ITG, TC-E1-054-14-ITG, TC-E1-054-15-ITG, TC-E1-054-16-ITG, TC-E1-054-17-ITG |
| REQ-DCM-019 | A discarded document is never removed silently; the reason and the person are kept with the file | POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with action DISCARD, GET /api/recovery/document/v1/intake-items/{intakeItemId}/content, GET /api/recovery/document/v1/intake-items/{intakeItemId} | TC-E1-054-12-ITG, TC-E1-054-13-ITG |
| DP-01 | No service reads another service's tables | All ten operations of section 12.2; the suite owns no table | TC-E1-054-01-ITG, TC-E1-054-11-ITG, TC-E1-054-16-ITG |
| DP-03 | Local decision record plus central ledger | The local DOCATT record, DecisionRecorded on rwb.decision-record.v1 and GET /api/recovery/decision/v1/decision-log?caseId={caseId} | TC-E1-054-02-ITG, TC-E1-054-19-ITG, TC-ITG-E1054-ITG-20 |
| DP-07 | Reference data through the contract of rwb-case | The type list in force DOCTYPE-2026.11 and the review reasons read as data | TC-E1-054-05-ITG, TC-E1-054-01-ITG |
| DP-09 | Kafka with outbox, inbox and CloudEvents | rwb.document.events.v1 and rwb.decision-record.v1 through the outbox of each owner | TC-E1-054-01-ITG, TC-E1-054-02-ITG, TC-E1-054-09-ITG |
| DP-13 | /api/recovery/<short>/v1 | Every consumed path under the four per-service bases | TC-E1-054-01-ITG, TC-E1-054-08-ITG, TC-E1-054-11-ITG |
| DP-19 | gateway-bff composite route | The suite enters through gateway-bff; SCR-31 and SCR-30 are not built or tested here | TC-E1-054-01-ITG, TC-E1-054-14-ITG |
| ASM-0487 | The queue, item read, content, resolve, field patch and document review are the P5 operations named by the Ownership Map under /api/recovery/document/v1 | The six P5 operations of section 12.2 | TC-E1-054-01-ITG, TC-E1-054-02-ITG, TC-E1-054-05-ITG, TC-E1-054-07-ITG, TC-E1-054-12-ITG, TC-E1-054-15-ITG |
| ASM-0488 | The case and its closed status come from P3 GET /cases/{caseId}, and the roles and scope from P4 GET /me/session; no role or permission table is read | GET /api/recovery/case/v1/cases/{caseId} and GET /api/recovery/access/v1/me/session | TC-E1-054-08-ITG, TC-E1-054-11-ITG, TC-E1-054-15-ITG, TC-E1-054-16-ITG |
| ASM-0489 | Attach stores the document through P5 with the DOCATT local record in one transaction, and the record reaches P7 through rwb.decision-record.v1; a failed local record leaves the item unchanged with MSG-P7-003 | The attach operation, the decision-log read and the five-minute collection | TC-E1-054-02-ITG, TC-E1-054-19-ITG, TC-ITG-E1054-ITG-20 |
| ASM-0490 | The labeled example stays in P5 and is read through the resolved item and its fields; the suite does not call the P10 evaluation endpoints | GET /api/recovery/document/v1/intake-items/{intakeItemId} after the resolve | TC-E1-054-02-ITG, TC-E1-054-03-ITG |

The legacy AC1 to AC17, including the type-change re-extraction of legacy AC10, sit at component level with RWB-P5-E1054-APP, not with this story. The access and the resilience criteria are proved here through the P4 and P7 owners and are held at component level by RWB-P4-E1054-APP and RWB-P7-E1054-APP.

### 19. Out of scope

- The APP and CON builds RWB-P5-E1054-APP, RWB-P5-E1054-CON, RWB-P3-E1054-APP, RWB-P4-E1054-APP and RWB-P7-E1054-APP, and their unit and component tests.
- The CON, INF, DB and OPS stories of P5, P3, P4 and P7.
- Setting the review reasons: OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching (RWB-E1-032).
- The type-change re-extraction at component level (legacy AC10) and the intake steps that produce an item.
- The model evaluations that read the labeled examples (RWB-E1-060).
- Assigning review work to named people by queue rules (RWB-E2-011).
- The case checklist on the review screen (RWB-E1-040).
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing beyond the one resilience scenario of AC16.
