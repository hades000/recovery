# RWB-ITG-E1032-ITG Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1032-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Partner frame note | Partner-slice frame (schema rwb_partner, base /api/recovery/partner/v1, topic rwb.partner.events.v1, queue rwb-partner, package th.co.scb.ace.workbench.recovery.partner) used until the S9 frame is published (GAP-3137) |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Wave note | Wave 1 kept per W-MAP for EP01, with one conflict row per service and business epic under R5.6; Architecture v5 places rwb-partner in wave 4 (GAP-0065), and the rwb-partner service wave 4 governs its later stories; the wave 1 entry check confirms the S9 frame and platform baseline are available (GAP-3139) |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1032-ITG-16); the squad sizes it at refinement |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Shared platform baseline (wave 0) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON held for DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19; not H for this slice |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None; the five integration dependencies are built by their owning stories and consumed through their published contracts |
| Contract dependencies | RWB-ITG-E1032-CON |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E1032-ITG-23); the /v1 path is the only version given |
| Integration dependencies | RWB-P5-E1032-APP, RWB-S9-E1032-APP, RWB-P3-E1032-APP, RWB-P6-E1032-APP, RWB-P7-E1032-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-032 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 34 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-032 automatic attach across P5 rwb-document (intake, match, store, held items), P3 rwb-case (the case directory and case status), P6 rwb-comms (the letter copy), S9 rwb-partner (the partner result file) and P7 rwb-decision (the DOCATT decision records)**, so that **every document that names its case or account is attached without a person and every doubtful one is held, proved on the real wave 1 services**.

### 2. Business rationale

The legacy story runs the match step inside the Quartz job JOB-12 every 15 minutes in business hours. The step selects the intake items that hold OCR text, no document and a predicted type, reads the case numbers and account numbers from the extracted fields and from the text, resolves them through the P3 `CaseDirectory` published interface, stores the matched file through the P5 `DocumentStore` and writes the `DOCATT` entry through the P7 `DecisionLogWriter`. A person attaches everything the matcher holds.

In the 19-service target JOB-12 becomes an event-started `DocumentIntakeWorkflow` in P5 rwb-document, started from the document event and scaled on KEDA workers (DP-10; Architecture v5 slide 44). The case lookup is the P3 rwb-case case contract rather than an in-process interface (DP-11), and ACE account data is read through the P1 rwb-source-data views or the owning service's own ACE views (DP-05). The intake parameters stay data rows (DP-06) and the document type and intake status lists are reference data read through the P3 reference-data contract (DP-07). The document events travel on `rwb.document.events.v1` through outbox and inbox with CloudEvents (DP-09); the topic carries the service name of the naming rule, and the legacy `rwb.p<n>.` names disappear with it. Each attach writes its `DOCATT` record locally in rwb_document and P7 rwb-decision collects it within five minutes (DP-03). The held-item list and the reviewer's attach use the P5 operations of the Ownership Map, `GET /review-items` and `POST /intake-items/{intakeItemId}/resolve`, and not the legacy `/attach` path. The screen is reached through gateway-bff (DP-19) but is not built or tested here.

This ITG story owns no legacy acceptance criterion. Legacy AC1 to AC15 sit at component level with RWB-P5-E1032-APP, and the access and the resilience criteria sit with the sibling APP stories RWB-P3-E1032-APP, RWB-P6-E1032-APP, RWB-S9-E1032-APP and RWB-P7-E1032-APP. The seventeen scenarios of section 7 are the integration proof across the five owners, and every value in them is a legacy value.

Two of the three intake sources are contracts of services that only exist in the target: the letter copy that P6 rwb-comms generates in `NoticeDispatchWorkflow` and the partner result file that S9 rwb-partner records from the partner gateway. They are why RWB-P6-E1032-APP and RWB-S9-E1032-APP sit in the chain. Without them only the scan path of P5 would be proved, AC4 would have no partner result to arrive on, and the letter copy would never become an intake item in the evidence.

Where the sources do not name the event that starts the workflow, the operation and version field that resolve a held item, the home of the three intake parameters in the target, or the exact P6 and S9 paths that feed the hub, the suite asserts through the owners' contracts and records the open point as `Not specified in the source documents (GAP-0356; ASM-0454)`.

### 3. Preconditions

- RWB-P5-E1032-APP is done: intake, match, store, the held-item list and the resolve operation are in SIT on P5 rwb-document.
- RWB-S9-E1032-APP is done: the partner result file reaches the document hub from the partner gateway.
- RWB-P3-E1032-APP is done: the case directory contract returns a case by case number, the open cases of an account number, and the case read of the suite.
- RWB-P6-E1032-APP is done: the letter copy generated by P6 rwb-comms reaches the document hub as an intake item.
- RWB-P7-E1032-APP is done: the DOCATT records written locally in rwb_document are collected into the central ledger of P7 rwb-decision.
- The published contracts of P5, P3, P6, S9 and P7 are deployed under their own per-service bases behind gateway-bff.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic cases RW-2026-000123, RW-2026-000456 and RW-2026-000789, its accounts TEST-ACC-0001, TEST-ACC-0002 and TEST-ACC-0003, its synthetic users and its synthetic files.
- The parameters CASE_NO_PATTERN = "RW-[0-9]{4}-[0-9]{6}", ACCOUNT_NO_PATTERN = "[0-9]{10}" (assumed; DL21) and CLASSIFY_THRESHOLD = 0.80 are loaded as data rows and read through the parameters contract of P3 rwb-case.
- The feature flag `rwb.dochub.autoattach` is on.
- The synthetic users, roles and scopes of section 10 are loaded: TEST-CO-01, TEST-LIT-01, TEST-LIT-02 and TEST-TM-01.
- No production data is used and no production connection is opened, and the release date 30 November 2026 is tentative; a date is not a precondition of this story.
- The story has no build dependency, so it is ready on Day 1 and waits only on its five integration dependencies.

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, accounts, users and files of the harness RWB-ITG-W1J01-ITG; no production data is used. Case RW-2026-000123 is open, owned by TEST-CO-01 and linked to TEST-ACC-0001; RW-2026-000456 is open and linked to TEST-ACC-0002; RW-2026-000789 is closed.
2. Harness: signs in as the synthetic users of section 10 through gateway-bff and holds their roles and scopes for the run.
3. Harness: stores the three intake sources — a scanned notice through POST /api/recovery/document/v1/cases/{caseId}/documents on P5 rwb-document, a partner result file through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results on the S9 partner gateway path, and a letter copy through POST /api/recovery/comms/v1/cases/{caseId}/notices on P6 rwb-comms — and reads the returned upload link, the instruction result and the notice.
4. Harness: waits on `rwb.document.DocumentStored.v1`, `rwb.document.DocumentFieldsExtracted.v1` and `rwb.agent.AgentRunCompleted.v1` before it asserts any item, and records the elapsed time of each wait.
5. Harness: reads the documents of the case through GET /api/recovery/document/v1/cases/{caseId}/documents and asserts the type, source, confidence, review status and write-once flag of each, then reads the `DOCATT` entries through GET /api/recovery/decision/v1/decision-log and asserts the model version, the confidence, the match method, the approver where a person decided, and the five-minute collection.
6. Harness: reads the held items through GET /api/recovery/document/v1/review-items and each one through GET /api/recovery/document/v1/intake-items/{intakeItemId}, with the OCR text pages from the content path.
7. Harness: resolves the held items through POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve as TEST-LIT-01 and TEST-LIT-02, at the item version read in the previous step, and asserts the stored document and the approver on the `DOCATT` entry.
8. Harness: runs the repeats and the negative cases — the same file twice, the repeat run over matched items, the closed case, the conflict, the unknown type, the case outside the scope, the type not in force, two reviewers at one version and the role without Documents C.
9. Harness: proves the decision-record failure path with the agreed test-only fault switch, restores the switch and the feature flag, writes the evidence report and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No readable case ID or account number | The item is held with match_status NO_MATCH and the OCR text stays for a person | MSG-P5-003 | AC2 |
| X2 | The account number matches two or more open cases | The item is held with match_status MULTIPLE and every candidate is offered by GET /review-items | MSG-P5-003 | AC3 |
| X3 | The case ID and the account point to different cases | The item is held with match_status CONFLICT and both cases are offered | MSG-P5-003 | AC5 |
| X4 | A case ID is read that does not exist | No candidate is returned and the item has match_status NO_MATCH | MSG-P5-003 | AC6 |
| X5 | The only candidate case is closed | The item is held with match_status CASE_CLOSED; no document row is written | MSG-P5-003 | AC7 |
| X6 | The same file is already on the matched case | The item is linked to the existing document; no second document and no second entry | None | AC8 |
| X7 | The workflow runs again over the attached items | No second attach, entry or event is written | None | AC9 |
| X8 | The classification confidence is below the threshold and one case is matched | The document is stored with review_status PENDING and write_once false | MSG-P5-003 | AC10 |
| X9 | Classification returns no agreed type | The item is held with match_status NO_TYPE | MSG-P5-003 | AC11 |
| X10 | The reviewer picks a case outside the scope | Refused with status 403 and the item stays held | MSG-P4-003 | AC13 |
| X11 | The reviewer picks a type not in force | Refused with status 422 naming the type | MSG-P5-006 | AC14 |
| X12 | Two reviewers resolve the same item at the same version | The first call returns 201 and the second 409 | MSG-GEN-004 | AC15 |
| X13 | The decision record cannot be written during an attach | Nothing is stored; an automatic item stays PENDING for the next run; a manual call returns 503; an incident is raised (R-UNI-39) | MSG-P7-003 | AC17 |
| X14 | A role without Documents C resolves a held item | Refused with status 403 and the item stays held | MSG-P4-002 | AC16 |
| X15 | A consumed call exceeds the 2 s timeout or returns a server error | The call is retried once under the suite policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC12 |
| X16 | The fixture set does not match the harness RWB-ITG-W1J01-ITG expectations, or the classifier returns no fixture answer | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the five APP stories and the published contracts of P5, P3, P6, S9 and P7, not their source code |
| Negotiable | The patterns, the threshold, the fixture sizes and the fault-switch mechanism are data rows or properties of the harness; the story fixes the assertions and the call set |
| Valuable | Attach without a person and the four held outcomes are proved on real services across five owners before wave 1 exits, not assumed from a unit test |
| Estimable | One suite module, one fixture pack of scans, a partner result and a letter copy, one item-version control, one decision-record assertion and one evidence report |
| Small | Fits in one sprint: nineteen scenarios over five services and one shared ledger topic; no service code and no schema change |
| Testable | Every scenario asserts a contract response, a stored document, a `DOCATT` entry, an event, a status or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-document, rwb-case, rwb-comms, rwb-partner and rwb-decision are deployed in SIT with their published contracts behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic cases, accounts, users and files are loaded and no production data is used
    Given case "RW-2026-000123" is open, owned by "TEST-CO-01" and linked to account "TEST-ACC-0001"
    Given case "RW-2026-000456" is open and linked to account "TEST-ACC-0002"
    Given case "RW-2026-000789" is closed
    Given parameter CLASSIFY_THRESHOLD is 0.80

  Scenario: AC1 Auto attach by case ID (new, D-RCV-60)
    Given a scanned notice with case ID "RW-2026-000123", classified "COURT_NOTICE" at 0.93 by classifier version "CLS-1.0"
    When intake completes
    Then the document is stored on the case with type "COURT_NOTICE", source "SCAN", classification_confidence 0.9300 and review_status "NOT_NEEDED" without a person
    Then one DOCATT entry holds model version "CLS-1.0", confidence 0.93 and match method "CASE_ID"
    Then DocumentStored is published and the intake item has match_status "MATCHED" with the document ID

  Scenario: AC2 No match (new, D-RCV-60)
    Given a scan with no readable case ID and no readable account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"
    Then GET /api/recovery/document/v1/intake-items/{intakeItemId} returns its OCR text pages
    Then no document row is written

  Scenario: AC3 Two candidates (new, D-RCV-60)
    Given a scan whose account number "TEST-ACC-0003" is linked to open cases "RW-2026-000321" and "RW-2026-000654"
    When intake completes
    Then the intake item has match_status "MULTIPLE"
    Then both candidate cases are offered by GET /api/recovery/document/v1/review-items
    Then no document row is written

  Scenario: AC4 Match by account number from a partner result (new, D-RCV-60)
    Given a partner result file submitted from screen PRT-02 Instruction through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results with no case ID and account number "TEST-ACC-0002", classified "DEMAND_LETTER" at 0.88
    When intake completes
    Then the document is stored on case "RW-2026-000456"
    Then the DOCATT entry holds match method "ACCOUNT_NO" and source "PARTNER"

  Scenario: AC5 Case ID and account disagree (new, D-RCV-60)
    Given a scan with case ID "RW-2026-000123" and account number "TEST-ACC-0002"
    When intake completes
    Then the intake item has match_status "CONFLICT" with candidates "RW-2026-000123" and "RW-2026-000456"

  Scenario: AC6 Case ID that does not exist (new, D-RCV-60)
    Given a scan with case ID "RW-2026-999999" and no account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"

  Scenario: AC7 Only candidate is closed (new, D-RCV-60)
    Given a scan with case ID "RW-2026-000789"
    When intake completes
    Then the intake item has match_status "CASE_CLOSED" with candidate "RW-2026-000789"
    Then no document row is written

  Scenario: AC8 The same file is already on the case (new, D-RCV-60)
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    Given a second intake item holds the same file with the same hash
    When intake completes
    Then the second item has match_status "MATCHED" with the document ID from AC1
    Then the case holds one copy of that court notice and one DOCATT entry for it

  Scenario: AC9 Repeat run (new, D-RCV-60)
    Given 15 intake items are already "MATCHED"
    When the intake workflow runs again
    Then no further document row, DOCATT entry or DocumentStored event is written for them

  Scenario: AC10 Low classification confidence with one case (new, D-RCV-60)
    Given a scan with case ID "RW-2026-000123" classified "APPRAISAL_REPORT" at 0.62 with candidates APPRAISAL_REPORT 0.62 and TITLE_DEED 0.30
    When intake completes
    Then the document is stored on the case with review_status "PENDING", write_once false and the file in "rwb-docs"
    Then the document carries document_type "APPRAISAL_REPORT" and both candidates for SCR-31

  Scenario: AC11 No agreed type (new, D-RCV-60)
    Given a scan with case ID "RW-2026-000123" and review_reason "UNKNOWN_TYPE" from classification
    When intake completes
    Then the intake item has match_status "NO_TYPE" with candidate "RW-2026-000123"

  Scenario: AC12 A reviewer attaches a held item (new, D-RCV-60)
    Given the item from AC3 and reviewer "TEST-LIT-01" holding RW-LITOFF with both candidate cases in scope
    When the reviewer calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve with case "RW-2026-000654", type "GUARANTOR_NOTICE" and the item version
    Then the document is stored on the case with type "GUARANTOR_NOTICE"
    Then the DOCATT entry names "TEST-LIT-01" as approver and match method "PERSON"
    Then the item has match_status "MATCHED"

  Scenario: AC13 Reviewer picks a case outside the scope (new, D-RCV-60)
    Given reviewer "TEST-LIT-02" whose scope excludes case "RW-2026-000654"
    When the reviewer resolves the item from AC3 to that case
    Then the call returns 403 with MSG-P4-003
    Then the item keeps match_status "MULTIPLE"

  Scenario: AC14 Reviewer picks a type not in force (new, D-RCV-60)
    Given the item from AC2 and a reviewer with scope ALL
    When the reviewer resolves it to "RW-2026-000123" with type "PAYSLIP"
    Then the call returns 422 with MSG-P5-006 naming "PAYSLIP"

  Scenario: AC15 Two reviewers attach the same item (new, D-RCV-60)
    Given the item from AC2 at version 3
    When two reviewers resolve it at the same time with version 3
    Then one call returns 201 and the other 409 with MSG-GEN-004
    Then one document row exists

  Scenario: AC16 A role without Documents C is refused (new, D-RCV-60)
    Given test user "TEST-TM-01" holds RW-TEAMMGR with Documents R only
    When the user resolves a held item
    Then the call returns 403 with MSG-P4-002 and the item stays held

  Scenario: AC17 A decision record that cannot be written stores nothing (new, D-RCV-60)
    Given the local DOCATT write is switched to fail by the agreed test-only fault switch
    When an automatic and a manual attach run
    Then nothing is stored, the automatic item stays PENDING for the next run and the manual call returns 503 with MSG-P7-003
    Then an incident is raised

  Scenario: AC18 Architecture constraints hold for JOB-12, the decision record and cross-service calls (new, D-RCV-60)
    Given the wave 1 services are deployed in SIT
    When the intake workflow is started by an intake event and cross-service calls are made
    Then JOB-12 runs as an event-started DocumentIntakeWorkflow in rwb-document with KEDA workers and no Quartz job or schedule
    Then each attach writes its DOCATT decision record in rwb_document in the same transaction as the document and publishes it on rwb.decision-record.v1
    Then P7 rwb-decision has collected each DOCATT record within five minutes
    Then the intake parameters are read as document_hub_parameter data rows in P5 and every cross-service call is one hop with a 2 s timeout

  Scenario: AC19 Activity retry and timeout (new, D-RCV-60)
    Given an intake activity call to a dependency fails or exceeds its timeout
    When the intake workflow runs
    Then the activity is retried under the retry policy Not specified in the source documents (NEWAC-RWB-ITG-E1032-ITG-AC19)
    Then an attach already stored is not stored again and its DOCATT entry is not duplicated
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A classified document attaches to its case without a person when exactly one open case is found | RWB-E1-032 BR1; REQ-DCM-007; FEAT-DCM-12 |
| BR2 | The case is found by the case ID or the account number read from the document; the account number is the join to other systems | RWB-E1-032 BR2; DL21 (assumption: Not specified in the source documents (DOR-RWB-ITG-E1032-ITG-18)); parameters CASE_NO_PATTERN and ACCOUNT_NO_PATTERN |
| BR3 | No match, more than one candidate, disagreement, a closed case or no agreed type goes to a person | RWB-E1-032 BR3; REQ-DCM-005; FSD P5 A2.12.4 |
| BR4 | A document classified below the threshold is stored for review in the standard container, not write-once, until a person confirms its type | RWB-E1-032 BR4; parameter CLASSIFY_THRESHOLD; RWB-E1-054; CTL-12 |
| BR5 | Each attach is written to the decision log with the classifier version, the confidence and the person where one decided, before the document is stored | RWB-E1-032 BR5; Principle 5; R-UNI-39; REQ-DRI-004 |
| BR6 | An item attached once is not attached again | RWB-E1-032 BR6; R-UNI-40 |
| BR7 | A reviewer attaches only to a case in their scope | RWB-E1-032 BR7; CTL-09 |
| BR8 | JOB-12 is an event-started DocumentIntakeWorkflow in P5 rwb-document with KEDA workers, not a Quartz job, and it runs no Schedule | DP-10; Architecture v5 slide 44; ASM-0454 |
| BR9 | Each attach writes its DOCATT decision record in rwb_document in the same transaction as the document and publishes it on `rwb.decision-record.v1`; P7 rwb-decision collects it within five minutes | DP-03; ADR-022; Architecture v5 slide 28 |
| BR10 | The intake parameters stay document_hub_parameter data rows in P5 and are read as data, and every cross-service call is one hop with a 2 s timeout | DP-06; DP-11; ADR-020; ASM-0456 |

### 9. State transitions

None for the case status. This story changes no case status and reads the status only to prove the closed case of AC7. It changes the intake item match_status and creates the document record, both in P5 rwb_document. A held value becomes MATCHED when a reviewer resolves the item through the P5 resolve operation, and the suite reads every state through that contract and writes none of them itself. A held item and a refused attach store no document and write no DOCATT entry; the hold is only the match_status of the intake item in rwb_document (GAP-2446).

| Object | State | Meaning |
|---|---|---|
| document_intake | PENDING | The item holds OCR text, no document and a predicted type; the match step may pick it up |
| document_intake | MATCHED | The item is attached to one case and holds the document ID; a repeat run skips it |
| document_intake | NO_MATCH | No readable case ID and no readable account number, or a case ID that does not exist; the OCR text is held for a person |
| document_intake | MULTIPLE, CONFLICT | More than one open case was found for the account number, or the case ID and the account number point to different cases; every candidate is held |
| document_intake | CASE_CLOSED, NO_TYPE | The only candidate case is closed and no document row is written, or classification returned no agreed type; the item is held for a person |
| document | COPY_PENDING, STORED | The file is written to its container and the metadata is committed with the DOCATT record in one transaction; the file is then in its final place |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| SY-OCR, OCR and extraction pipeline | Matches and attaches automatically (Documents C) |
| SY-DECLOG, decision log writer | Writes the DOCATT record locally in rwb_document; P7 rwb-decision collects it |
| Roles with Documents C and the candidate case in scope (for example RW-LITOFF, RW-CASEOWN) | See and attach held items that name a candidate in their scope |
| Roles with Documents C and scope ALL (for example RW-LEGAL) | See and attach held items with no candidate |
| Roles with Documents R only (for example RW-TEAMMGR) | See attached documents on cases in their scope; no attach |

The synthetic users of the run are TEST-CO-01, TEST-LIT-01, TEST-LIT-02 and TEST-TM-01; no other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002, DF-CAS-005 | recovery_case (P3 rwb-case) | id, case_no, status | Read, through GET /api/recovery/case/v1/cases/{caseId} |
| DF-CAS-026 | case_account (P3 rwb-case) | account_key | Read, through GET /api/recovery/case/v1/cases/{caseId} |
| DF-ACE-002 | v_ace_account (P1 rwb-source-data views) | account_code | Read, through the P1 views or the owning service's ACE views |
| DF-DOC-001 to DF-DOC-011 | document (P5 rwb-document) | all fields | Write by P5 inside its workflow; read through GET /api/recovery/document/v1/cases/{caseId}/documents |
| DF-DOC-004, DF-DOC-007, DF-DOC-008, DF-DOC-010 | document (P5 rwb-document) | document_type, classification_confidence, review_status, write_once | Read |
| DF-DOC-056, DF-DOC-060, DF-DOC-061 | document_intake (P5 rwb-document) | file_sha256, case_id, document_id | Read |
| DF-DOC-070, DF-DOC-073, DF-DOC-075, DF-DOC-076, DF-DOC-080 | document_intake (P5 rwb-document) | predicted_type, classifier_version, match_status, candidate_case_ids, review_reason | Read |
| DF-DOC-089 | document_text (P5 rwb-document) | text_content | Read, through the content path of the item |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (local record in P5; central ledger in P7) | all fields | Read, through GET /api/recovery/decision/v1/decision-log |
| Intake trigger, parameter home and item version | DocumentIntakeWorkflow, the intake parameters and the resolve request | The event that starts the workflow, the home of the three parameters and the version field of the resolve call | Not specified in the source documents (GAP-0356; ASM-0454) |

The legacy story writes these fields in the monolith. In the target they are written by P5 rwb-document inside its own workflow and schema, and the suite only reads them through the P5, P3 and P7 contracts (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/document/v1/cases/{caseId}/documents | P5 rwb-document | Store a synthetic scan on a case and read the returned upload link |
| GET /api/recovery/document/v1/cases/{caseId}/documents | P5 rwb-document | Read the documents of a case and the type, source, confidence, review status and write-once flag of each |
| GET /api/recovery/document/v1/review-items | P5 rwb-document | Read the held items and their candidates, oldest first |
| GET /api/recovery/document/v1/intake-items/{intakeItemId} | P5 rwb-document | Read match_status, the candidates, the predicted type, the confidence and the version of the item |
| GET /api/recovery/document/v1/intake-items/{intakeItemId}/content | P5 rwb-document | Read the file and the OCR text pages of a held item |
| POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve | P5 rwb-document | Attach a held item to a case with a type and the item version, as the reviewer |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the case, its status, its owner and its account |
| GET /api/recovery/case/v1/admin/parameters | P3 rwb-case | Read CASE_NO_PATTERN, ACCOUNT_NO_PATTERN and CLASSIFY_THRESHOLD as data rows |
| POST /api/recovery/comms/v1/cases/{caseId}/notices | P6 rwb-comms | Request the letter copy that becomes an intake item |
| POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results | S9 rwb-partner | Submit the partner result file on the partner gateway path |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Read the DOCATT entries and the collection time against the five-minute target |

The resolve call carries the case, the type and the item version in its request; the exact version field and the held-item semantics are the open point recorded as `Not specified in the source documents (GAP-0356; ASM-0455)`. Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event; every event of the chain is published by its owning service through its own outbox.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | The document is stored; the suite waits for it before it asserts the item and the DOCATT entry |
| rwb.document.DocumentFieldsExtracted.v1 | rwb.document.events.v1 | P5 rwb-document | The case number and account number fields are extracted; the match step and the suite wait for it |
| rwb.agent.AgentRunCompleted.v1 | rwb.agent.events.v1 | P10 rwb-agent | The classify run behind the intake returned its answer; the suite asserts the type and confidence from the fixture |
| rwb.comms.NoticeGenerated.v1 | rwb.comms.events.v1 | P6 rwb-comms | Notification to rwb-decision only; the document hub receives the letter copy by call from rwb-comms (GAP-1202) |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P5 rwb-document, with the central ledger in P7 rwb-decision | The DOCATT record is collected into the ledger inside the five-minute target |

The suite consumes no other event and produces none. The P6 letter copy and the S9 partner result are the two intake sources that make RWB-P6-E1032-APP and RWB-S9-E1032-APP part of the chain (ASM-0457).

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Holds the OCR step, the classify step, the extract step and the match step under test; started by the document event, not by a Schedule |
| AgentRunWorkflow | P10 rwb-agent | rwb-agent | Serves the classify run of the item: 60 seconds, then the rule result |
| NoticeDispatchWorkflow | P6 rwb-comms | rwb-comms | Generates the letter copy that becomes an intake item |

#### 12.6 Schedules

None. JOB-12 has no Schedule in the target: the workflow starts from `DocumentStored` and scales on KEDA workers (DP-10; Architecture v5 slide 44). The suite waits on no Schedule and moves no clock.

#### 12.7 Tables owned

None (DP-01). document, document_intake, document_text, document_type and document_hub_parameter are P5 tables, decision_log_entry is written locally by P5 and held centrally by P7, and the suite owns no table and never reads another service's schema.

#### 12.8 Contract fakes

Contract fake for rwb-case, rwb-comms, rwb-decision, rwb-document and rwb-partner: Not specified in the source documents (DOR-RWB-ITG-E1032-ITG-22); no contract fake library version is recorded as published. No fake is used by this story: every call of section 12.2 goes to the real SIT service on its published wave 1 contract. The files are synthetic, and the classifier returns the fixture answers of the harness. AC17 uses the agreed test-only fault switch on the P5 decision-record write, agreed with the service owner, and it is the only intervention in a running service.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 11 |
| Kafka | 0 | 5 |
| Temporal | 0 | 3 observed |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the seventeen scenarios against SIT and holds no service code |
| Fixture pack | Test data | Synthetic scans, the partner result file and the P6 letter copy, with the three cases, the three accounts and the four synthetic users |
| Item-version control | Harness control | Reads the item version before a resolve and sends the same version twice for AC15, then restores the item |
| Decision-record assertion | Assertion | Reads the DOCATT entry of each attach, compares the model version, the confidence and the match method, and measures the collection time against the five-minute target |
| Evidence report | Report | Records per scenario the item ids, the document ids, the DOCATT entries, the events and their times, the statuses and the messages |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | document, document_intake, document_text, document_type and document_hub_parameter stay in the owner schema of P5; the suite asserts through the P5, P3, P6, S9 and P7 contracts only |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic rwb.decision-record.v1 | H RWB-PLT-E1027-CON | On RWB-P5-E1032-APP and RWB-P7-E1032-APP; this suite only waits for the collected record and measures the five minutes |
| DP-05 | AceSourceQuery, v_ace_*, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | On RWB-P3-E1032-APP and RWB-P5-E1032-APP for the account read; the suite never reads an ACE table |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On the APP stories; the three intake values stay document_hub_parameter data rows in P5 and are read as data (ASM-0456) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories for the document types and the intake status list; the suite sends the codes as data |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On RWB-P5-E1032-APP for DocumentStored, DocumentFieldsExtracted and the attach event rwb.document.DocumentAttached.v1 (GAP-0991, catalogue confirmation pending), on RWB-P6-E1032-APP for NoticeGenerated, and on every owner for DecisionRecorded; the suite consumes them |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-12 becomes DocumentIntakeWorkflow on queue rwb-document, started from the document event and scaled on KEDA workers; the suite observes the run |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The eleven consumed REST operations of section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P5-E1032-APP and RWB-P7-E1032-APP for the match columns and the local record; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; SCR-31 and SCR-30 are not built or tested here |

The dependency-added column records the build dependency of the owning story. Those H and C dependencies belong to the owning APP stories, not to this suite; this story's H, C and X lists are exactly those of the metadata table — no H, the one contract dependency RWB-ITG-E1032-CON as C and no X — and its I list is the five integration dependencies RWB-P5-E1032-APP, RWB-S9-E1032-APP, RWB-P3-E1032-APP, RWB-P6-E1032-APP and RWB-P7-E1032-APP. An ITG story waits on no build of its own. The dependencies that the DP table of the ten patterns adds are recorded here and leave the metadata rows unchanged: H RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, C RWB-P3-E1042-CON and RWB-P3-E1043-CON, and the authorise contract RWB-P4-E1037-CON. The owning stories build against the fakes of these contracts on Day 1 (GAP-2448). The shapes of IntakeItem, IntakeItemPage, IntakeAttachRequest and the not-found answer are the smallest superset of the legacy list, with every unnamed element behind a placeholder until the owner documents confirm it (GAP-0992). The two rwb-case case reads consumed by the baseline are declared with fakes in RWB-ITG-E1032-CON; their exact paths are not specified in the source documents (GAP-0992). Capacity values of the intake-match path are not specified in the source documents (GAP-0993); they are provisioned now and set per environment from SIT measurement.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5, P3, P6, S9 and P7 through gateway-bff.
2. Build the fixture pack: the three synthetic cases, the three accounts, the four synthetic users, the scans, the partner result file and the P6 letter copy, with the three parameters held as document_hub_parameter data rows and read as data.
3. Add the three intake sources: the scan through the P5 upload, the partner result through the S9 partner gateway path and the letter copy through the P6 notice request; assert that each becomes one intake item.
4. Implement AC1 to AC4 with the event waits on DocumentStored, DocumentFieldsExtracted and AgentRunCompleted and the contract reads of section 12.2.
5. Implement AC5 to AC9 and AC11: the two held outcomes with their candidates, the closed case, the unknown type, the duplicate file and the repeat run, and assert that no document row is written where the story says so.
6. Implement AC10 with the low-confidence fixture, the standard container and write_once false, and assert both candidates on the document for the review queue.
7. Implement AC12 to AC16 with the item-version control, the resolve operation, the two scopes, the type not in force and the role holding Documents R only.
8. Implement AC17 through the agreed test-only fault switch on the P5 decision-record write, assert the PENDING item, the 503 and the incident, restore the switch and the flag, then write the evidence report and run the suite in SIT against the wave 1 release candidate.

Done when: all seventeen test cases pass in SIT against the published wave 1 contracts of P5, P3, P6, S9 and P7, the evidence report shows for each item the document row, the DOCATT entry and the event that prove it, every DOCATT entry is collected into the ledger inside the five-minute target, and no service code or schema was changed by this story apart from the agreed test-only fault switch.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | Item held for a person or document stored for review | Some fields need checking. The document is in the review queue. |
| MSG-P5-006 | Reviewer picks a type not in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-GEN-001 | Case or type missing on resolve | Enter {field}. |
| MSG-GEN-004 | Item attached by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Chosen case outside the scope | This case is not in your scope. |

The message IDs and wording are copied from RWB-E1-032. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the held list loads |
| SCR-31 Document review queue | list | The held tab: items oldest first with source, received time, match status, proposed type and candidate cases |
| SCR-31 Document review queue | reviewed | The item is attached; it leaves the list and the document opens on SCR-30 of the chosen case |
| SCR-31 Document review queue | empty | Not specified in the source documents (CG-ALL-313) |
| SCR-31 Document review queue | error | Not specified in the source documents (CG-ALL-313) |
| SCR-31 Document review queue | no access | Not specified in the source documents (CG-ALL-313) |
| SCR-30 Case documents | list | An automatically attached document shows on its case; a PENDING document shows MSG-P5-003 |
| SCR-30 Case documents | Loading | Not specified in the source documents (CG-ALL-312) |
| SCR-30 Case documents | empty | Not specified in the source documents (CG-ALL-312) |
| SCR-30 Case documents | error | Not specified in the source documents (CG-ALL-312) |
| SCR-30 Case documents | no access | Not specified in the source documents (CG-ALL-312) |

The suite builds and tests neither screen and reads the same states through the contracts of section 12.2; the tab for documents pending type or field review on SCR-31 is built in RWB-E1-054 and is not in this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-032-01-ITG | AC1, BR1, BR5 | Integration | Synthetic notice with RW-2026-000123 at 0.93 and classifier version CLS-1.0; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-02-ITG | AC2, BR3 | Integration | Synthetic scan with no identifiers; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-03-ITG | AC3, BR3 | Integration | Account TEST-ACC-0003 on two open cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-04-ITG | AC4, BR2 | Integration | Partner result file with account TEST-ACC-0002 only; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-05-ITG | AC5, BR3 | Integration | Case ID and account on different cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-06-ITG | AC6, BR3 | Integration | Case ID RW-2026-999999; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-07-ITG | AC7, BR3 | Integration | Closed case RW-2026-000789; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-08-ITG | AC8, BR6 | Integration | The same file in two intake items; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-09-ITG | AC9, BR6 | Integration | 15 items already matched; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-10-ITG | AC10, BR4 | Integration | Scan classified APPRAISAL_REPORT at 0.62 on a matched case; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-11-ITG | AC11, BR3 | Integration | Item with review_reason UNKNOWN_TYPE; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-12-ITG | AC12, BR5 | Integration | TEST-LIT-01 resolves a MULTIPLE item; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-13-ITG | AC13, BR7 | Component | TEST-LIT-02 with a scope that excludes the chosen case; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-14-ITG | AC14 | Component | Type PAYSLIP not in force; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-15-ITG | AC15 | Integration | Two parallel resolve calls at version 3; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-16-ITG | AC16, access | Component | TEST-TM-01 holding RW-TEAMMGR with Documents R only; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-17-ITG | AC17, resilience | NFR | Decision-record write forced to fail during an automatic and a manual attach; nothing stored, MSG-P7-003, incident raised; end-to-end: real services on the wave 1 contracts |
| TC-E1-032-18-ITG | section 12 operations, events, activities | Contract | Each operation, event and activity of section 12 against its published wave 1 contract; no contract fake |
| TC-E1-032-19-ITG | AC18, BR8, BR9, BR10 | Contract | Not specified in the source documents (NEWAC-RWB-ITG-E1032-ITG-AC18); end-to-end: real services on the wave 1 contracts |
| TC-E1-032-20-ITG | AC19, resilience | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1032-ITG-AC19); end-to-end: real services on the wave 1 contracts |

### 17. Guardrails

- No business value in code: the case number and account number patterns and the classification threshold are data rows read through the parameters contract.
- No personal data in logs, events, evidence or fixtures: account numbers and OCR text are never logged; logs carry the intake item ID and the outcome; every test account and file is synthetic.
- No cross-service table read: cases, accounts, documents, notice copies, partner results and decision records are read through the owner's contract, and the suite owns no table.
- One hop and a 2 s timeout on every consumed call (ADR-020).
- The matcher never picks one of several candidates; any doubt goes to a person.
- A document stored for type review is never put in the write-once container before its type is confirmed (RWB-E1-054).
- The decision-record fault switch is test-only, agreed with the service owner, and restored at the end of the run.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG; no production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | DocumentIntakeWorkflow, rwb.document.DocumentStored.v1, GET /api/recovery/document/v1/cases/{caseId}/documents, GET /api/recovery/document/v1/review-items | TC-E1-032-01-ITG, TC-E1-032-02-ITG, TC-E1-032-03-ITG, TC-E1-032-04-ITG, TC-E1-032-05-ITG, TC-E1-032-06-ITG, TC-E1-032-07-ITG, TC-E1-032-08-ITG, TC-E1-032-09-ITG, TC-E1-032-10-ITG, TC-E1-032-11-ITG |
| REQ-DRI-004 | The document attached record is written for every attach | The local DOCATT record, rwb.decision.DecisionRecorded.v1 and GET /api/recovery/decision/v1/decision-log | TC-E1-032-12-ITG, TC-E1-032-13-ITG, TC-E1-032-14-ITG, TC-E1-032-15-ITG, TC-E1-032-17-ITG |
| REQ-DCM-005 | A type below the threshold goes to review; no agreed type is held | review_status PENDING, write_once false, type_candidates, match_status NO_TYPE, MSG-P5-003 | TC-E1-032-03-ITG, TC-E1-032-11-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | rwb.document.events.v1, rwb.comms.events.v1, rwb.agent.events.v1 and rwb.decision-record.v1 through the outbox and inbox of each owner | TC-E1-032-01-ITG, TC-E1-032-09-ITG |
| ADR-022 | Local decision record plus central ledger | One local DOCATT record in rwb_document per attach, collected by P7 rwb-decision within five minutes | TC-E1-032-17-ITG |
| DP-05 | ACE data only through the owner's contract or its views | The account read of the case through the P1 views or the P3 contract | TC-E1-032-04-ITG, TC-E1-032-06-ITG |

The legacy AC1 to AC15 at component level belong to RWB-P5-E1032-APP and the sibling APP stories RWB-P3-E1032-APP, RWB-P6-E1032-APP, RWB-S9-E1032-APP and RWB-P7-E1032-APP, not to this story.

### 19. Out of scope

- The five APP builds RWB-P5-E1032-APP, RWB-S9-E1032-APP, RWB-P3-E1032-APP, RWB-P6-E1032-APP and RWB-P7-E1032-APP, and their unit and component tests.
- The CON, INF and OPS stories of the five services.
- Source pickup from scanners, SFTP and mailboxes, and the intake item base record (RWB-E1-057).
- Confirming or correcting the type and the fields of a document stored for review (RWB-E1-054).
- Moving an attached document to another case (Epic 2).
- Attach of field app photos (RWB-E2-024).
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing.
