# Technical Specification — RWB-E1-032 Automatic attach from the OCR intake

| Field | Value |
|---|---|
| Story | RWB-E1-032 — Automatic attach from the OCR intake |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-068-epic-1-RWB-E1-032` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DCM-007); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 032 Automatic attach from the OCR intake v1.md`; FSD P5 A2.12; TSD P5 T3.1 |
| Upstream IDs | REQ-DCM-007; FEAT-DCM-12; US-RWB-E1-032; DL21; R-UNI-39, R-UNI-40; CTL-09, CTL-12 |
| Status | SUCCESS — CLAR-008 resolved by decision D-RCV-31 (2026-11-06) |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-31 Document review queue adds the Unmatched tab with the scan viewer, OCR text, candidate cases, case picker and type picker; SCR-30 shows the attached document. |
| Logic In Scope | `YES` — identifier collection, matching outcomes, auto attach, held items, manual attach, duplicate link, concurrency and decision log. |
| API In Scope | `YES` — four new endpoints for the review queue and intake item resolution. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | JOB-12 Document intake (new `matchStep`); `document_intake` (match columns); SCR-31; SCR-30. |
| New Nodes Required | `YES` — `MatchStep`, `CaseMatcher`, `MatchPatterns`, `AutoAttachService`, `ManualAttachService`, `IntakeItemController`, `IntakeItemRepository`, `UnmatchedIntakeTab`. |
| Inherited Existing Behavior | Document store and DOCATT decision log (RWB-E1-024); classification (RWB-E1-050); extraction (RWB-E1-053); case and account lookup through `CaseDirectory` (P3); review queue (RWB-E1-054). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A classified document attaches to its case without a person when exactly one open case is found. | SPEC-RWB-E1-032-004 | DIRECT | `AutoAttachService` calls `DocumentStore.store` only for a single open candidate. | COVERED |
| BR2 | The case is found by the case ID or the account number read from the document; the account number is the join to other systems. | SPEC-RWB-E1-032-002, SPEC-RWB-E1-032-003 | DIRECT | `CASE_NO_PATTERN` and `ACCOUNT_NO_PATTERN` are parameters; identifiers come from extracted fields and OCR text. | COVERED |
| BR3 | No match, more than one candidate, disagreement, a closed case or no agreed type goes to a person. | SPEC-RWB-E1-032-003, SPEC-RWB-E1-032-006, SPEC-RWB-E1-032-007 | DIRECT | Outcomes NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE are held. | COVERED |
| BR4 | A document classified below the threshold is stored for review in the standard container, not write-once, until a person confirms its type. On confirmation of a write-once type, it is re-stored through `DocumentStorage.store` into `rwb-docs-legal` (D-RCV-31). | SPEC-RWB-E1-032-005 | DIRECT | `review_status PENDING` and `write_once false`; file in `rwb-docs`; the confirm step applies the D-RCV-31 re-store, audit entry and refusal paths. | COVERED |
| BR5 | Each attach is written to the decision log with the classifier version, the confidence and the person where one decided, before the document is stored. | SPEC-RWB-E1-032-004, SPEC-RWB-E1-032-010, SPEC-RWB-E1-032-012 | DIRECT | DOCATT entry is written by `DocumentStore`; a failed write prevents the store. | COVERED |
| BR6 | An item attached once is not attached again. | SPEC-RWB-E1-032-008, SPEC-RWB-E1-032-009 | DIRECT | Duplicate hash links to the existing document; MATCHED items are skipped. | COVERED |
| BR7 | A reviewer attaches only to a case in their scope. | SPEC-RWB-E1-032-010, SPEC-RWB-E1-032-013 | DIRECT | Scope check before the store; 403 MSG-P4-003. | COVERED |
| AC1 | A scanned notice with a case ID is stored automatically with type, source, confidence and NOT_NEEDED; DOCATT records model version, confidence and CASE_ID; DocumentStored; item MATCHED. | SPEC-RWB-E1-032-001, SPEC-RWB-E1-032-004 | DIRECT | Match then store; no person. | COVERED |
| AC2 | A scan with no readable case or account number is NO_MATCH; the item read returns OCR pages; no document row. | SPEC-RWB-E1-032-006 | DIRECT | Held item with OCR text; no store. | COVERED |
| AC3 | An account number linked to two open cases is MULTIPLE; both candidates are offered; no document row. | SPEC-RWB-E1-032-003, SPEC-RWB-E1-032-006 | DIRECT | `candidate_case_ids` holds both. | COVERED |
| AC4 | A scan with only an account number is stored on that case; DOCATT records ACCOUNT_NO. | SPEC-RWB-E1-032-002, SPEC-RWB-E1-032-004 | DIRECT | Account lookup through `CaseDirectory`. | COVERED |
| AC5 | A case ID and an account that point to different cases is CONFLICT with both candidates. | SPEC-RWB-E1-032-003, SPEC-RWB-E1-032-006 | DIRECT | Disagreement goes to a person. | COVERED |
| AC6 | A case ID that does not exist is NO_MATCH. | SPEC-RWB-E1-032-003, SPEC-RWB-E1-032-006 | DIRECT | No candidate. | COVERED |
| AC7 | A closed case is CASE_CLOSED with the candidate; no document row. | SPEC-RWB-E1-032-003, SPEC-RWB-E1-032-006 | DIRECT | Closed status from `CaseDirectory`. | COVERED |
| AC8 | A second intake item with the same file is linked to the existing document; one copy and one DOCATT. | SPEC-RWB-E1-032-008 | DIRECT | Hash match on the case. | COVERED |
| AC9 | A repeat run over 15 MATCHED items writes no further document, entry or event. | SPEC-RWB-E1-032-009 | DIRECT | Selection excludes MATCHED and items with a document ID. | COVERED |
| AC10 | A low-confidence type with one case is stored PENDING, write_once false, in rwb-docs, with both candidates. | SPEC-RWB-E1-032-005 | DIRECT | Type review path. | COVERED |
| AC11 | An item with UNKNOWN_TYPE is NO_TYPE with the candidate case. | SPEC-RWB-E1-032-007 | DIRECT | No store. | COVERED |
| AC12 | A reviewer attaches a MULTIPLE item to a chosen case; DOCATT names the reviewer and PERSON; item MATCHED. | SPEC-RWB-E1-032-010 | DIRECT | Manual attach. | COVERED |
| AC13 | A reviewer choosing an out-of-scope case gets 403 MSG-P4-003; the item stays MULTIPLE. | SPEC-RWB-E1-032-010, SPEC-RWB-E1-032-013 | DIRECT | Scope check before the store. | COVERED |
| AC14 | A type not in force is refused with 422 MSG-P5-006. | SPEC-RWB-E1-032-010 | DIRECT | Type checked against the catalog in force. | COVERED |
| AC15 | Two reviewers on one item produce one 201 and one 409; one document row. | SPEC-RWB-E1-032-011 | DIRECT | Optimistic version on the item. | COVERED |
| X1..X5, X9 | No match, multiple candidates, conflict, closed case or no type. | SPEC-RWB-E1-032-003, SPEC-RWB-E1-032-006, SPEC-RWB-E1-032-007 | DIRECT | Held with match status and candidates. | COVERED |
| X6, X7 | Same file already on the case, or a repeat run. | SPEC-RWB-E1-032-008, SPEC-RWB-E1-032-009 | DIRECT | Link; skip. | COVERED |
| X8 | Low classification confidence with one case. | SPEC-RWB-E1-032-005 | DIRECT | Store PENDING in the standard container. | COVERED |
| X10, X11, X14 | Out-of-scope case, type not in force, or no Documents C. | SPEC-RWB-E1-032-010, SPEC-RWB-E1-032-013 | DIRECT | 403 MSG-P4-003; 422 MSG-P5-006; 403 MSG-P4-002. | COVERED |
| X12, X13 | Two reviewers attach at once, or the decision log write fails. | SPEC-RWB-E1-032-011, SPEC-RWB-E1-032-012 | DIRECT | 409 MSG-GEN-004; nothing stored; 503 MSG-P7-003. | COVERED |

## User story intent interpretation

As a **case owner**, I want **documents from the OCR intake attached to their case automatically when the case ID or the account number is read, with unmatched or ambiguous documents held for a person who sees the OCR text and the candidate cases and attaches the document**, so that **no document is filed by hand when the case is clear and none is filed on the wrong case when it is not**. The story adds `matchStep` to JOB-12 and the Unmatched tab on SCR-31. It never picks one of several candidates: any doubt goes to a person.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake: `matchStep` after `extractStep`. |
| Schedule | Every 15 minutes in business hours, as set by RWB-E1-049. |
| Preconditions | RWB-E1-024, RWB-E1-050 and RWB-E1-053 done; `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` loaded; `CaseDirectory` returns a case by case number and the open cases for an account; reviewer holds Documents C; flag `rwb.dochub.autoattach` on. |
| Input | Intake items with `ocr_status DONE`, `match_status PENDING`, no `document_id` and a predicted type (review reason empty or LOW_CONFIDENCE); extracted fields `case_no` and `account_no`; OCR text. |
| Output | Documents stored on their case; held items with match status and candidates; DOCATT decision log entries; `DocumentStored`; counts on the job record. |
| Feature flag | `rwb.dochub.autoattach`. Off: `matchStep` sets every classified item to `NO_MATCH`; reviewers attach them by hand. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `match_status` | `PENDING` | System writes MATCHED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED or NO_TYPE | LOV-INTAKE-MATCH. |
| `document_intake` | `candidate_case_ids` | Empty | System writes the candidate list | JSON array of case IDs; empty on NO_MATCH. |
| `document_intake` | `case_id` | Empty | System writes on MATCHED | Must be an open case in scope for a manual attach. |
| `document_intake` | `document_id` | Empty | System writes on MATCHED | One document per item. |
| `document` | `classification_confidence` | Classifier output | System writes | `numeric(5,4)`. |
| `document` | `review_status` | `NOT_NEEDED` | System writes `PENDING` for a low-confidence type | LOV-REVIEW. |
| `document` | `write_once` | Type table | System writes `false` for a type under review | True for a confirmed legal type; the file re-stores into `rwb-docs-legal` per D-RCV-31. |
| `document` | `document_type` | Predicted type or reviewer choice | System writes | Must be in the catalog in force. |
| `document` | `type_candidates` | Classifier output | System writes | Two highest agreed types for SCR-31. |
| `decision_log_entry` | DOCATT fields | New row | `DocumentStore` writes | Classifier version, confidence and match method. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `match_status PENDING` | `matchStep` | Exactly one open case found | `MATCHED` | Document stored; DOCATT; DocumentStored; `case_id` and `document_id` set. |
| `match_status PENDING` | `matchStep` | No readable or resolvable identifier | `NO_MATCH` | Held; OCR text available; no document. |
| `match_status PENDING` | `matchStep` | Account matches two or more open cases | `MULTIPLE` | Held; both candidates offered; no document. |
| `match_status PENDING` | `matchStep` | Case ID and account disagree | `CONFLICT` | Held; both candidates offered; no document. |
| `match_status PENDING` | `matchStep` | The only candidate is closed | `CASE_CLOSED` | Held; candidate offered; no document. |
| `match_status PENDING` | `matchStep` | No agreed type | `NO_TYPE` | Held; candidate case retained; no document. |
| Held status | Reviewer attaches | Scope, type and version checks pass | `MATCHED` | Document stored; DOCATT with PERSON; item leaves the queue. |

No case status changes. The document is `COPY_PENDING` then `STORED` through RWB-E1-024.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No readable case ID or account number | NO_MATCH; OCR text held for the reviewer; no document | MSG-P5-003 |
| X2 | Account matches two or more open cases | MULTIPLE; every candidate offered; no document | MSG-P5-003 |
| X3 | Case ID and account point to different cases | CONFLICT; both cases offered | MSG-P5-003 |
| X4 | Case ID does not exist | NO_MATCH | MSG-P5-003 |
| X5 | The only candidate is closed | CASE_CLOSED | MSG-P5-003 |
| X6 | Same file already on the matched case | Link to the existing document; no second document or DOCATT | None |
| X7 | Repeat run over attached items | No second attach, entry or event | None |
| X8 | Low classification confidence with one case | Store PENDING; write_once false; standard container | MSG-P5-003 |
| X9 | No agreed type | NO_TYPE; candidate retained | MSG-P5-003 |
| X10 | Reviewer picks a case outside scope | 403; item stays held | MSG-P4-003 |
| X11 | Reviewer picks a type not in force | 422 | MSG-P5-006 |
| X12 | Two reviewers attach the same item | First succeeds; second 409 | MSG-GEN-004 |
| X13 | Decision log write fails | Nothing stored; automatic stays PENDING; manual 503; incident raised | MSG-P7-003 |
| X14 | Role without Documents C attaches | 403 | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/review-items` (API-P5-010); `GET /api/recovery/v1/intake-items/{intakeItemId}` (API-P5-011); `GET /api/recovery/v1/intake-items/{intakeItemId}/content` (API-P5-012); `POST /api/recovery/v1/intake-items/{intakeItemId}/resolve` (API-P5-013). |
| Contract delta | `ReviewItemPage`; `IntakeItem` with pages, candidates and fields; `IntakeResolveRequest` with action ATTACH, caseId, documentType and version; `IntakeResolution`. |
| Backward compatibility | New endpoints; no existing contract changes. |
| Authorization | Documents R for the reads; Documents C with case scope for the attach; 403 MSG-P4-002/MSG-P4-003. |
| Error behaviour | 401; 403; 404; 409 MSG-GEN-004; 422 MSG-P5-006 or MSG-GEN-001; 503 MSG-P7-003. |
| Versioning | First release of these endpoints; no version change to existing endpoints. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-007; SPEC-RWB-E1-032-006, -010, -013 | New Unmatched tab, scan viewer, OCR text, candidate list, case picker and type picker. | Component tests for list, detail, attach, empty and error states. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-007; SPEC-RWB-E1-032-001..014 | New job step, matcher, auto and manual attach services, controller and repository. | Unit tests for the five outcomes, duplicate link, low-confidence store, repeat run, manual attach, scope, type, concurrency and decision log failure. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `MatchStep` | Job step | Selects items, matches, stores or holds, updates the item, writes counts. |
| `CaseMatcher` | Service | Reads case and account numbers; resolves them through `CaseDirectory`; returns the outcome and candidates. |
| `MatchPatterns` | Rule table | Reads `CASE_NO_PATTERN` and `ACCOUNT_NO_PATTERN`. |
| `AutoAttachService` | Service | Builds the `StoreRequest`; applies the low-confidence review rule; updates the item. |
| `ManualAttachService` | Service | Scope and type checks, optimistic lock, store with the approver. |
| `IntakeItemController` | Controller | The four intake item endpoints. |
| `IntakeItemRepository` | Repository | Reads and writes `document_intake` only. |
| `UnmatchedIntakeTab` | React component | Unmatched list on SCR-31 with the scan viewer, OCR text, candidates, case and type pickers. |

### Package and boundaries

`recovery/dochub/attach`, Java package `recovery.dochub.attach`; front end `recovery/documents`. Cases and accounts are read only through `CaseDirectory`; the document is stored only through `DocumentStore` (RWB-E1-024); the decision log only through `DecisionLogWriter`.

### Data and migration

- Reads: `document_intake` (`id`, `ocr_status`, `match_status`, `document_id`, `predicted_type`, `review_reason`, `classification_confidence`, `type_candidates`, `file_sha256`), `document_text` (`page_no`, `text_content`), `document` (hash and case for the duplicate check), `document_hub_parameter`.
- Writes: `document_intake` (`match_status`, `candidate_case_ids`, `case_id`, `document_id`), `document` (through the store), `decision_log_entry` (through the store), `outbox`.
- Migration `V1_5_032__intake_match.sql` adds `match_status varchar(12) default 'PENDING'` and `candidate_case_ids jsonb`; index `ix_intake_held ON document_intake (match_status, received_at) WHERE match_status NOT IN ('PENDING','MATCHED')`.
- No rule row: the outcomes are the fixed behaviour of the story. Patterns and threshold are parameters.

### Matching rules

1. Collect case numbers from the extracted field `case_no` and from the OCR text with `CASE_NO_PATTERN`; collect account numbers from `account_no` and the text with `ACCOUNT_NO_PATTERN`.
2. Resolve each case number with `CaseDirectory.findByCaseNo`; resolve each account with `CaseDirectory.findOpenCasesByAccountNo`.
3. If both identifiers resolve and point to different cases, the outcome is CONFLICT.
4. If exactly one open case remains, the outcome is MATCHED; if none, NO_MATCH; if more than one, MULTIPLE; if the only candidate is closed, CASE_CLOSED.
5. If the item has `review_reason UNKNOWN_TYPE` or `MODEL_UNAVAILABLE`, the outcome is NO_TYPE and the candidate case is retained.
6. No person is involved in steps 1 to 5; the matcher never chooses among candidates.

### Attach, duplicate and concurrency

- Auto attach calls `DocumentStore.store` with the case, predicted type, source, file, hash and extracted fields. The store writes the DOCATT entry with classifier version, confidence and match method (`CASE_ID` or `ACCOUNT_NO`), the document row and `DocumentStored`.
- A low-confidence type is stored with `review_status PENDING` and `write_once false` in `rwb-docs`; the candidates are kept for SCR-31.
- **Type confirmation of a write-once legal type (D-RCV-31, ruled 2026-11-06):** the confirm step
  calls the published `DocumentStorage.store` interface so the confirmed file is written into
  `rwb-docs-legal` at `{caseId}/{documentId}/v{docVersion}`; `storage_ref` moves to the legal
  container; a DOCATT audit entry names the container, the confirmed type and the confirming user;
  the standard-container object stays available for evidence under the `rwb-docs` versioning policy;
  the write refuses with MSG-GEN-006 when the `rwb-docs-legal` immutability policy is absent. No blob
  is written anywhere except through `DocumentStorage` (RWB-TE-012, CTL-12, NFR-029).
- If the same hash is already on the case, the item is linked to the existing document; no second document, DOCATT or event is written.
- Manual attach checks the case is open and in scope, the type is in force and the item version matches; it calls the store with the reviewer as approver and match method `PERSON`.
- Two reviewers on one item: the first commits; the second gets 409 MSG-GEN-004; one document row exists.

### Transaction, events and decision log

- One transaction per item; the row is locked with `SKIP LOCKED`.
- The DOCATT entry is written before the document row; a failed write rolls back the store. An automatic attach stays PENDING for the next run; a manual attach returns 503.
- `DocumentStored` (EV-16) is written in the same transaction as the document.
- Idempotency key: intake item ID; in the store, case, type and file hash.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR | Documents C | All intake items |
| RW-LITOFF, RW-CASEOWN | Documents C | Candidate cases in scope |
| RW-LEGAL and other roles with Documents C and scope ALL | Documents C | Items with no candidate |
| RW-TEAMMGR | Documents R | Attached documents in scope; no attach |
| SY-DECLOG | Decision log C | All |

Items with no candidate are visible only to roles with scope ALL. Field values and OCR text are masked by role and never logged.

### Observability, performance and operations

- Job counts: items matched, held by outcome, duplicate links, failed.
- Metrics: match rate by method, held rate by outcome, decision log failures, attach duration.
- Alerts: decision log failure; a rise in CONFLICT or NO_MATCH above the run book threshold.
- Run book: JOB-12 `matchStep` in RWB-E1-056.
- Performance: one lookup per identifier per item; the held index supports the review queue; the 180-sample SIT check requires every item with one readable case ID and confidence at or above 0.80 to attach in the same run.

### Feature flag and rollback

`rwb.dochub.autoattach`. Off: every classified item becomes NO_MATCH and reviewers attach by hand. Rollback: turn the flag off and redeploy the previous tag; the migration is forward-only and the columns are nullable or defaulted.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-032-01 | AC1, BR1, BR5 | System | Notice with RW-2026-000123 at 0.93 | Stored NOT_NEEDED; DOCATT CASE_ID; DocumentStored; item MATCHED. |
| TC-E1-032-02 | AC2, BR3 | System | Scan with no identifiers | NO_MATCH; OCR pages readable; no document. |
| TC-E1-032-03 | AC3, BR3 | System | Account on two open cases | MULTIPLE; both candidates; no document. |
| TC-E1-032-04 | AC4, BR2 | System | Account TEST-ACC-0002 only | Stored on RW-2026-000456; DOCATT ACCOUNT_NO. |
| TC-E1-032-05 | AC5, BR3 | System | Case ID and account on different cases | CONFLICT; both candidates. |
| TC-E1-032-06 | AC6, BR3 | System | Case ID RW-2026-999999 | NO_MATCH. |
| TC-E1-032-07 | AC7, BR3 | System | Closed case RW-2026-000789 | CASE_CLOSED; candidate; no document. |
| TC-E1-032-08 | AC8, BR6 | System | Same file in two intake items | Second item linked; one document; one DOCATT. |
| TC-E1-032-09 | AC9, BR6 | System | 15 MATCHED items | No further document, entry or event. |
| TC-E1-032-10 | AC10, BR4 | System | APPRAISAL_REPORT at 0.62 on a matched case | PENDING; write_once false; rwb-docs; both candidates. |
| TC-E1-032-11 | AC11, BR3 | System | Item with UNKNOWN_TYPE | NO_TYPE; candidate case. |
| TC-E1-032-12 | AC12, BR5 | System | Reviewer attaches a MULTIPLE item | Stored; DOCATT PERSON; item MATCHED. |
| TC-E1-032-13 | AC13, BR7 | System | Reviewer scope excludes the chosen case | 403 MSG-P4-003; item stays MULTIPLE. |
| TC-E1-032-14 | AC14 | System | Type PAYSLIP | 422 MSG-P5-006. |
| TC-E1-032-15 | AC15 | System | Two parallel attach requests at version 3 | One 201; one 409; one document. |
| TC-E1-032-16 | X14 | Security | RW-TEAMMGR with Documents R only attaches | 403 MSG-P4-002. |
| TC-E1-032-17 | X13 | Resilience | Decision log write forced to fail on auto and manual attach | Nothing stored; auto PENDING; manual 503 MSG-P7-003; incident. |

## Guardrails

- No business value in code: the case and account patterns and the threshold are parameters.
- No personal data in logs, tests or prompts: account numbers and OCR text are never logged; logs carry the intake ID and the outcome; test accounts are synthetic.
- No read of another module's tables: cases and accounts are resolved through `CaseDirectory`.
- The matcher never picks one of several candidates; any doubt goes to a person.
- A document stored for type review is never put in the write-once container before its type is confirmed.

## Out of scope

- Confirming or correcting the type and fields of a document stored for review (RWB-E1-054).
- Source pickup from scanners, SFTP and mailboxes, and the intake item base record (RWB-E1-057).
- Moving an attached document to another case (Epic 2).
- Attach of field app photos (RWB-E2-024).

## Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-032-01..17 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Flow step 8; contract; SPEC-010 | Flow names `GET /intake-items` and `POST /intake-items/{intakeItemId}/attach`; section 12 and the API specification name `GET /review-items` and `POST /intake-items/{intakeItemId}/resolve`. | Determines the endpoints the tab calls. | Use API-P5-010 and API-P5-013 (`/review-items` and `/resolve`). The flow wording is a known defect. | RESOLVED | SPEC-RWB-E1-032-010 |
| CLAR-002 | Contract; RWB-E1-054; SPEC-006 | 032 defines `GET /review-items` with a `matchStatus` filter; 054 defines `kind` and `reason`. | One endpoint must serve both tabs. | One endpoint API-P5-010 with `kind`, `reason`, `page` and `size`; the Unmatched tab uses `kind=INTAKE` and displays `match_status` in the reason column when `review_reason` is empty. | RESOLVED | SPEC-RWB-E1-032-006 |
| CLAR-003 | Contract; RWB-E1-054; SPEC-010 | 032 sends `caseId` on resolve; 054 sends `caseNo`. | Determines the request schema. | `IntakeResolveRequest.caseId` per API-P5-013; the screen resolves a typed case number to `caseId` through `CaseDirectory` before the call. | RESOLVED | SPEC-RWB-E1-032-010 |
| CLAR-004 | BR2; SPEC-002 | Are `CASE_NO_PATTERN` and `ACCOUNT_NO_PATTERN` approved? | They determine what the matcher reads. | Assumed under DL21: `RW-[0-9]{4}-[0-9]{6}` and `[0-9]{10}`; load as parameters and confirm before go-live. | RESOLVED | SPEC-RWB-E1-032-002 |
| CLAR-005 | BR3; SPEC-003 | What is the precedence when a case ID and an account give different candidates? | Determines CONFLICT versus MATCHED. | Any disagreement between identifiers is CONFLICT; if only one identifier resolves, use it; if only a closed case is found, CASE_CLOSED. This follows BR3 and AC5/AC7. | RESOLVED | SPEC-RWB-E1-032-003 |
| CLAR-006 | BR4; SPEC-005 | Can a stored low-confidence document's type be changed later? | Determines whether a legal type can move to the write-once container. | Not in this story: 032 does not change the type of a stored document; the type and container question is CLAR-008. | RESOLVED | SPEC-RWB-E1-032-005 |
| CLAR-007 | BR5; SPEC-004 | Which match method values are recorded in DOCATT? | The builder needs the values. | `CASE_ID`, `ACCOUNT_NO` and `PERSON`, as the story states; they are payload values, not a reference list. | RESOLVED | SPEC-RWB-E1-032-004, SPEC-RWB-E1-032-010 |
| CLAR-008 | BR4; SPEC-005 | BR4 says a low-confidence document is stored in the standard container "until a person confirms its type"; no source stated how a confirmed legal type moves to the write-once container. | Determines whether a legal document can remain in `rwb-docs` after its type is confirmed, which affects the write-once control (CTL-12, NFR-029). | **Ruled 2026-11-06 as D-RCV-31:** on confirmation of a write_once type, the confirm step re-stores the file through the published `DocumentStorage.store` interface into `rwb-docs-legal` at `{caseId}/{documentId}/v{docVersion}`, moves `storage_ref`, writes a DOCATT audit entry naming the container, the confirmed type and the confirming user, and keeps the standard-container object for evidence under the `rwb-docs` versioning policy; the write refuses when the immutability policy is absent (MSG-GEN-006). No blob is written except through `DocumentStorage` (RWB-TE-012). Owner: solution architect with Compliance. | `RESOLVED` | SPEC-RWB-E1-032-005 |

`CLARIFICATION_STATUS: RESOLVED` — no open items. CLAR-008 is answered by decision D-RCV-31 and
carried into BR4, the field matrix and the type-confirmation behaviour above.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this story. RUN_STATUS: SUCCESS — CLAR-008 resolved by D-RCV-31.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New matching step on JOB-12, four new intake item endpoints and the Unmatched tab on SCR-31.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new auto-attach capability with new review queue endpoints and UI]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 15 acceptance criteria and 14 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 2] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Start the Implementation Planner on this specification.
```
