# Technical Specification — RWB-E1-054 Review queue for low-confidence documents

| Field | Value |
|---|---|
| Story | RWB-E1-054 — Review queue for low-confidence documents |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-076-epic-1-RWB-E1-054` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DCM-005); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 054 Review queue for low confidence documents v1.md`; FSD P5 A2.10–A2.11; TSD P5 T3.1 |
| Upstream IDs | REQ-DCM-005; FEAT-DCM-10, FEAT-DCM-11; US-RWB-E1-054; DL11, DL19, DL26, DL31; R-UNI-39, R-UNI-40; CTL-09, CTL-11, CTL-12 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-31 Document review queue: list, detail panel with file and OCR text, type and case choosers, field Confirm/Correct, Attach and Discard, reviewed and empty states. |
| Logic In Scope | `YES` — queue composition, scope, type change, field validation, attach, duplicate link, discard, stored-document review, labeled set, concurrency and decision log. |
| API In Scope | `YES` — new review queue, intake item read/resolve and document review endpoints; the field PATCH endpoint is extended in use. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `DocumentHubController` (field PATCH); `document_intake` (outcome columns); `document` (`review_status`); SCR-31; SCR-30. |
| New Nodes Required | `YES` — `ReviewQueueController`, `ReviewQueueService`, `ReviewResolutionService`, `LabeledSetReader`, `DocumentIntakeRepository`, `ReviewQueuePage`, `ReviewItemPanel`. |
| Inherited Existing Behavior | Intake items and reasons (RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-032); document store and DOCATT (RWB-E1-024); case record view (RWB-E1-035); checklist (RWB-E1-040); parameters (RWB-E1-042); decision log (RWB-E1-027). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The queue holds intake items with a review reason and no outcome, and documents with `review_status PENDING`. | SPEC-RWB-E1-054-001 | DIRECT | Union of intake items and stored documents; held match outcomes are included through their match status (CLAR-003). | COVERED |
| BR2 | An item with no case is shown to the review team named in `REVIEW_TEAM_UNATTACHED` and to roles with scope ALL; an item with candidate cases and a document are shown by case scope. | SPEC-RWB-E1-054-001, SPEC-RWB-E1-054-013 | DIRECT | Scope rule applied in the queue query; no-candidate items only for scope ALL. | COVERED |
| BR3 | Attach and complete are allowed only when no field is in REVIEW, the type is in force and the case is open. | SPEC-RWB-E1-054-004, SPEC-RWB-E1-054-006, SPEC-RWB-E1-054-009 | DIRECT | Preconditions checked before the store. | COVERED |
| BR4 | `review_status` becomes CONFIRMED when type, case and values are kept, CORRECTED when any changes. | SPEC-RWB-E1-054-006, SPEC-RWB-E1-054-009 | DIRECT | Outcome derived from the changes. | COVERED |
| BR5 | A corrected value keeps the extracted value in `extracted_value` and the corrector in `confirmed_by`. | SPEC-RWB-E1-054-005, SPEC-RWB-E1-054-006 | DIRECT | Field update writes both columns. | COVERED |
| BR6 | Attach stores through `DocumentStore`, which writes DOCATT first and places a legal type in the write-once container. | SPEC-RWB-E1-054-006, SPEC-RWB-E1-054-012 | DIRECT | Store is the only write path; failed log prevents the store. | COVERED |
| BR7 | Each resolved item is a labeled example for the model evaluations. | SPEC-RWB-E1-054-010 | DIRECT | `LabeledSetReader` returns predicted and confirmed values. | COVERED |
| BR8 | A change saved against an old version is refused. | SPEC-RWB-E1-054-011 | DIRECT | Optimistic `version`; 409 MSG-GEN-004. | COVERED |
| BR9 | A discarded item keeps its file in the intake container and records the reason and the person. | SPEC-RWB-E1-054-008 | DIRECT | No file deletion; `review_outcome DISCARDED`. | COVERED |
| BR10 | Field values are masked unless the role may see them. | SPEC-RWB-E1-054-003, SPEC-RWB-E1-054-016 | DIRECT | P4 masking; OCR text and values never logged. | COVERED |
| AC1, AC14 | The queue lists low-confidence items with reason and candidates, in scope, oldest first, with no other team's item. | SPEC-RWB-E1-054-001, SPEC-RWB-E1-054-002 | DIRECT | Scope and ordering in one query. | COVERED |
| AC2 | A corrected item is attached with type, corrected value, extracted value, state CORRECTED, confirmed_by, review_status CORRECTED, outcome ATTACHED, DOCATT and a labeled example. | SPEC-RWB-E1-054-004, SPEC-RWB-E1-054-005, SPEC-RWB-E1-054-006, SPEC-RWB-E1-054-010 | DIRECT | Type, case and field changes; store; labeled set. | COVERED |
| AC3, AC17 | A stored document field is confirmed; the status becomes CONFIRMED; a repeat returns the saved field without change. | SPEC-RWB-E1-054-005, SPEC-RWB-E1-054-009 | DIRECT | Idempotent confirm. | COVERED |
| AC4, AC13 | An empty correction or an empty discard reason is refused with 422; nothing changes. | SPEC-RWB-E1-054-005, SPEC-RWB-E1-054-008 | DIRECT | Required value and reason. | COVERED |
| AC5 | A type not in force is refused with 422 MSG-P5-006. | SPEC-RWB-E1-054-004 | DIRECT | Type checked against the catalog in force. | COVERED |
| AC6 | A corrected date outside the allowed range is refused with 422 MSG-GEN-002 naming the field and the limits. | SPEC-RWB-E1-054-005 | DIRECT | `REVIEW_DATE_MIN` and `REVIEW_DATE_MAX`. | COVERED |
| AC7, AC8 | Attach with a field still in REVIEW, or to a closed case, is refused with 422 and nothing is stored. | SPEC-RWB-E1-054-006 | DIRECT | BR3 preconditions. | COVERED |
| AC9 | Two officers on one item produce one 201 and one 409; one document. | SPEC-RWB-E1-054-011 | DIRECT | Optimistic version. | COVERED |
| AC10 | A type change re-runs extraction for the new type and shows its fields, each in REVIEW; the old type's fields are gone. | SPEC-RWB-E1-054-004 | DIRECT | `FieldExtraction.extractIntake`; manual type change marks the new fields for confirmation. | COVERED |
| AC11 | A file already on the chosen case is linked to the existing document; no second document; MSG-P5-024 names it. | SPEC-RWB-E1-054-007 | DIRECT | Hash match on the case. | COVERED |
| AC12 | A discard with a reason sets DISCARDED, the reason, the officer and the time; the item leaves the queue. | SPEC-RWB-E1-054-008 | DIRECT | Outcome columns. | COVERED |
| AC15 | An empty queue shows "No documents are waiting for review." | SPEC-RWB-E1-054-015 | DIRECT | Empty state. | COVERED |
| AC16 | A document outside the officer's scope returns 404 MSG-P4-003. | SPEC-RWB-E1-054-013 | DIRECT | Scope filter before read. | COVERED |
| X1..X3 | Empty correction, type not in force, or date outside the range. | SPEC-RWB-E1-054-004, SPEC-RWB-E1-054-005 | DIRECT | 422; nothing saved. | COVERED |
| X4, X5 | A field still in REVIEW on attach, or a closed case. | SPEC-RWB-E1-054-006 | DIRECT | 422; nothing stored. | COVERED |
| X6 | Another officer saved the item first. | SPEC-RWB-E1-054-011 | DIRECT | 409 MSG-GEN-004. | COVERED |
| X7 | The same file is already on the chosen case. | SPEC-RWB-E1-054-007 | DIRECT | Link; MSG-P5-024. | COVERED |
| X8 | Discard without a reason. | SPEC-RWB-E1-054-008 | DIRECT | 422 MSG-GEN-001. | COVERED |
| X9..X11 | Empty queue, out-of-scope document, or a repeated confirmation. | SPEC-RWB-E1-054-001, SPEC-RWB-E1-054-005, SPEC-RWB-E1-054-013, SPEC-RWB-E1-054-015 | DIRECT | Empty state; 404; idempotent 200. | COVERED |
| X12, X13 | Documents R only, or a decision log failure on attach. | SPEC-RWB-E1-054-012, SPEC-RWB-E1-054-013 | DIRECT | 403 MSG-P4-002; nothing stored; 503 MSG-P7-003. | COVERED |

## User story intent interpretation

As a **litigation officer**, I want **a queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set**, so that **no document is attached wrongly and the models improve**. The story builds SCR-31, the queue over held intake items and pending documents, and the resolution actions. It is the human half of the pipeline: 049, 050, 053 and 032 produce the reasons; 054 resolves them and feeds the labeled set.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | The officer opens SCR-31 Document review queue; the officer opens an item and chooses Set type, Confirm, Correct, Attach or Discard. |
| Preconditions | RWB-E1-049, 050, 053, 032, 024 and 035 done; `REVIEW_TEAM_UNATTACHED`, `REVIEW_DATE_MIN`, `REVIEW_DATE_MAX` and `REVIEW_PAGE_SIZE` loaded; DOCTYPE version in force; the officer holds RW-LITOFF (Documents CRU) with team scope; flag `rwb.dochub.review` on. |
| Input | Intake items with a review reason or held match status and no outcome; documents with `review_status PENDING`; the officer's type, case and field choices. |
| Output | Queue page; resolved intake items; stored or linked documents; confirmed or corrected fields; DOCATT; `DocumentFieldsExtracted` (EV-17); labeled examples. |
| Feature flag | `rwb.dochub.review`. Off: SCR-31 is hidden and review items stay in the queue untouched. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `review_outcome` | Empty | System writes ATTACHED or DISCARDED | LOV-INTAKE-OUTCOME; one value. |
| `document_intake` | `resolved_by`, `resolved_at` | Empty | System writes | The officer and the time. |
| `document_intake` | `discard_reason` | Empty | Officer enters on Discard | Required for Discard; up to 400 characters. |
| `document_intake` | `version` | Current | System increments | Optimistic lock; stale version 409. |
| `document` | `review_status` | PENDING | System writes CONFIRMED or CORRECTED | LOV-REVIEW. |
| `document_field` | `field_value` | Extracted value | Officer edits on Correct | Must match the field data type; not empty. |
| `document_field` | `state` | REVIEW | System writes CONFIRMED or CORRECTED | LOV; no field may remain REVIEW on attach. |
| `document_field` | `confirmed_by` | Empty | System writes | The officer's user ID. |
| `document_field` | `extracted_value` | Extracted value | Read-only | Kept when the value is corrected. |
| `document_field` | `version` | Current | System increments | `If-Match` on the field PATCH. |
| Request | `action` | None | Officer chooses | SET_TYPE, ATTACH or DISCARD. |
| Request | `documentType`, `caseId`, `fields`, `discardReason`, `version` | Screen | Officer chooses or enters | Type in force; case open and in scope; no field in REVIEW on attach. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Intake item with a review reason | Attach | BR3 passes; store succeeds | `review_outcome ATTACHED` | Document stored or linked; DOCATT; item leaves the queue. |
| Intake item with a review reason | Discard | A reason is given | `review_outcome DISCARDED` | Reason, officer and time recorded; file retained; item leaves the queue. |
| `document.review_status PENDING` | Review completed | Nothing changed | `CONFIRMED` | All fields confirmed; document leaves the queue. |
| `document.review_status PENDING` | Review completed | A value or type changed | `CORRECTED` | `extracted_value` kept; `confirmed_by` set. |
| `document_field.state REVIEW` | Confirm or Correct | Value valid | `CONFIRMED` or `CORRECTED` | `confirmed_by`; version increments. |

No case status changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Correct with an empty value | 422; nothing saved | MSG-GEN-001 |
| X2 | Chosen type not in force | 422; nothing saved | MSG-P5-006 |
| X3 | Corrected date outside the allowed range | 422; nothing saved | MSG-GEN-002 |
| X4 | Attach or complete with a field still in REVIEW | 422; nothing stored | MSG-GEN-001 |
| X5 | Chosen case is closed | 422; nothing stored | MSG-P5-005 |
| X6 | Another officer saved the item first | 409; reload | MSG-GEN-004 |
| X7 | Same file already on the chosen case | Link to the existing document; no second document | MSG-P5-024 |
| X8 | Discard without a reason | 422; item stays | MSG-GEN-001 |
| X9 | No item in the officer's queue | Empty state | None |
| X10 | Document outside the officer's scope | 404 | MSG-P4-003 |
| X11 | Same confirmation sent twice | 200 with the saved field; nothing changes | None |
| X12 | Documents R only | 403 | MSG-P4-002 |
| X13 | Decision log write fails on attach | Nothing stored; item unchanged; incident raised | MSG-P7-003 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/review-items` (API-P5-010); `GET /api/recovery/v1/intake-items/{intakeItemId}` (API-P5-011); `GET /api/recovery/v1/intake-items/{intakeItemId}/content` (API-P5-012); `POST /api/recovery/v1/intake-items/{intakeItemId}/resolve` (API-P5-013); `POST /api/recovery/v1/documents/{documentId}/review` (API-P5-014). |
| Existing endpoint extended in use | `PATCH /api/recovery/v1/documents/{documentId}/fields/{fieldId}` (API-P5-006). |
| Contract delta | `ReviewItemPage` with kind, reason, candidates and version; `IntakeItem` with pages, fields and candidates; `IntakeResolveRequest` with action SET_TYPE/ATTACH/DISCARD; `DocumentReviewRequest` with action COMPLETE and version. |
| Backward compatibility | New endpoints; the field PATCH keeps its contract; the resolve endpoint extends the RWB-E1-032 shape with action and discard. |
| Authorization | Documents R for the queue and reads; Documents U for resolve, field and review; 403 MSG-P4-002; 404 MSG-P4-003. |
| Error behaviour | 401; 403; 404; 409 MSG-GEN-004; 422 MSG-P5-005/006 or MSG-GEN-001/002; 503 MSG-P7-003 or MSG-GEN-006. |
| Versioning | First release of the review endpoints; no version change to the field PATCH. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-005; SPEC-RWB-E1-054-001..016 | New SCR-31 list, detail panel, type and case choosers, field actions, Attach and Discard. | Component tests for loading, list, reviewed, empty, each validation and the scope error. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-005; SPEC-RWB-E1-054-001..016 | New queue and resolution services, controller, labeled set reader and repository. | Unit tests for queue scope and order, SET_TYPE, confirm/correct, attach, duplicate link, discard, stored review, concurrency and decision log failure. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ReviewQueueController` | Controller | `GET /review-items`, intake item read and content, `POST /resolve`, `POST /documents/{id}/review`. |
| `DocumentHubController` | Controller | `PATCH /documents/{documentId}/fields/{fieldId}`. |
| `ReviewQueueService` | Service | Builds the queue with the scope rule. |
| `ReviewResolutionService` | Service | SET_TYPE, ATTACH and DISCARD; field confirm and correct; complete for documents. |
| `LabeledSetReader` | Published interface | Resolved items as labeled examples. |
| `DocumentIntakeRepository` | Repository | Reads and writes `document_intake`, including the outcome columns. |
| `ReviewQueuePage` | React component | SCR-31 list, paging and empty state. |
| `ReviewItemPanel` | React component | File and OCR viewer, type chooser, case chooser, fields, Attach and Discard. |

### Package and boundaries

`recovery/dochub/review`, Java package `recovery.dochub.review`; front end `recovery/documents`. Cases come through `CaseDirectory`; the document is stored only through `DocumentStore` (RWB-E1-024); extraction re-runs through `FieldExtraction` (RWB-E1-053); the decision log only through `DecisionLogWriter`.

### Data and migration

- Reads: `document_intake` (`review_reason`, `predicted_type`, `type_candidates`, `candidate_case_ids`, `extracted_fields`, `match_status`, `version`), `document_text` (`text_content`), `document` (`review_status`, `case_id`), `document_field` (`field_value`, `extracted_value`, `confidence`, `state`, `version`), `document_hub_parameter`.
- Writes: `document_intake` (`review_outcome`, `resolved_by`, `resolved_at`, `discard_reason`), `document` (`review_status`), `document_field` (`field_value`, `state`, `confirmed_by`, `version`), `decision_log_entry` and `outbox` through the store.
- Migration `V1_5_054__review_outcome.sql` adds `review_outcome varchar(12)`, `resolved_by uuid`, `resolved_at timestamptz`, `discard_reason varchar(400)` to `document_intake`.
- Indexes: `ix_intake_review ON document_intake (received_at) WHERE review_reason IS NOT NULL AND review_outcome IS NULL`; `ix_document_review ON document (review_status, created_at) WHERE review_status = 'PENDING'`.

### Review rules

1. Queue: union held intake items (review reason or held match status, no outcome) and documents with `review_status PENDING`; apply BR2 scope; oldest first; page size `REVIEW_PAGE_SIZE`.
2. SET_TYPE: validate the type in force; call `FieldExtraction.extractIntake`; replace the offered fields with the new type's fields, each in REVIEW for confirmation; do not keep the old type's fields.
3. Confirm/Correct: validate the value against the field data type and the date range; empty is refused; write `field_value`, keep `extracted_value`, set `state`, `confirmed_by` and version; a repeat with the same value and flag returns the saved field.
4. Attach: require no field in REVIEW, the type in force, the case open and in scope, and the current item version; call `DocumentStore.store` with the officer as approver; write DOCATT; set `review_outcome ATTACHED`; set `review_status CONFIRMED` when nothing changed, CORRECTED when type, case or a value changed; write EV-17.
5. Duplicate: if the file hash is already on the chosen case, link the item to the existing document; no second document, DOCATT or event; show MSG-P5-024.
6. Discard: require a reason; set `review_outcome DISCARDED`, `resolved_by`, `resolved_at` and `discard_reason`; keep the file in the intake container.
7. Stored document: confirm or correct each field, then complete the review; all fields must be out of REVIEW; set `review_status CONFIRMED` or CORRECTED.
8. Labeled set: `LabeledSetReader.resolvedSince` returns intake or document ID, predicted type, confirmed type, and extracted and confirmed values.

### Transaction, events and decision log

- One transaction per resolution; the intake item or document is locked; the version is checked.
- The DOCATT entry is written by `DocumentStore` before the document row; a failed write rolls back the store and leaves the item unchanged; a manual attach returns 503.
- EV-17 is written in the same transaction as the document fields.
- A discarded item keeps its file; no delete path exists.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-LITOFF | Documents CRU | Team or all |
| RW-CASEOWN | Documents CRU | Own cases |
| RW-TEAMMGR | Documents R | Team; no correct or attach |
| SY-OCR | Documents CRU | Re-run extraction on a type change |
| SY-DECLOG | Decision log C | DOCATT through the store |
| RW-COE | Documents R | Labeled examples through the model evaluation |

Field values, OCR text and discard reasons are masked by role and never logged. The labeled examples stay inside the bank.

### Observability, performance and operations

- Metrics: queue depth by reason, age of oldest item, resolved per day, correction rate per field, attach failures, duplicate links, decision log failures.
- Alerts: queue age above the run book threshold; decision log failure; a rise in CONFLICT or CASE_CLOSED.
- Run book: SCR-31 and the review queue note in RWB-E1-056.
- Performance: queue query uses the partial indexes; page size 50; one item read per open; no batch over the whole queue.

### Feature flag and rollback

`rwb.dochub.review`. Off: SCR-31 is hidden and review items stay untouched. Rollback: turn the flag off; the migration is forward-only and the new columns are nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-054-01 | AC1, BR1 | System | Intake item at 0.62 with two candidates | Listed with reason and both candidates. |
| TC-E1-054-02 | AC2, BR4..BR7 | System | Hearing date corrected; case RW-2026-000201 | Stored; field CORRECTED; DOCATT; outcome ATTACHED; labeled example. |
| TC-E1-054-03 | AC3, BR4 | System | Stored document with one field in review | Field CONFIRMED; document CONFIRMED. |
| TC-E1-054-04 | AC4 | System | Empty correction | 422 MSG-GEN-001; unchanged. |
| TC-E1-054-05 | AC5, BR3 | System | Type PAYSLIP | 422 MSG-P5-006. |
| TC-E1-054-06 | AC6 | System | Date 2569-12-16 as a Gregorian year | 422 MSG-GEN-002 with the limits. |
| TC-E1-054-07 | AC7, BR3 | System | Two fields in review, one confirmed | 422 naming the field; nothing stored. |
| TC-E1-054-08 | AC8, BR3 | System | Closed candidate case | 422 MSG-P5-005; nothing stored. |
| TC-E1-054-09 | AC9, BR8 | System | Two sessions on one item version | One 201; one 409; one document. |
| TC-E1-054-10 | AC10 | System | Demand letter changed to guarantor notice | New type's four fields in REVIEW; old fields gone. |
| TC-E1-054-11 | AC11 | System | Same file hash already on the case | Link; no second document; MSG-P5-024. |
| TC-E1-054-12 | AC12, BR9 | System | Unreadable item discarded with a reason | DISCARDED with reason, officer and time; file retained. |
| TC-E1-054-13 | AC13 | System | Discard with an empty reason | 422; item stays. |
| TC-E1-054-14 | AC14, BR2 | System | Five items across two teams | Three in-scope items, oldest first; no other team. |
| TC-E1-054-15 | AC15 | System | No item for the team | Empty state. |
| TC-E1-054-16 | AC16, BR10 | System | Document of team HP-NE | 404 MSG-P4-003. |
| TC-E1-054-17 | AC17 | System | Same PATCH sent twice | 200; saved field; no change. |
| TC-E1-054-18 | X12 | Security | RW-TEAMMGR calls resolve | 403 MSG-P4-002. |
| TC-E1-054-19 | X13 | Resilience | Decision log write forced to fail on Attach | Nothing stored; item unchanged; 503 MSG-P7-003; incident. |

## Guardrails

- No business value in code: the review team, date limits, page size and type list come from `document_hub_parameter` and the type table.
- No personal data in logs, tests or prompts: field values and OCR text are masked by role and never logged; labeled examples stay inside the bank.
- No read of another module's tables: cases come through `CaseDirectory`; scope comes from the ACE common access check.
- Attach goes only through `DocumentStore`, so a document never exists without its decision log entry.

## Out of scope

- Setting the review reasons: OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching (RWB-E1-032).
- The model evaluations that read the labeled examples (RWB-E1-060).
- Assigning review work to named people by queue rules (RWB-E2-011).
- The case checklist on the review screen (RWB-E1-040).

## Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-01..19 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §12, §13, TC-E1-054-18; SPEC-001 | Section 12 names `/review-items`, `/intake-items/{id}` and `/resolve`; section 13 and the access test name `/review-queue`, `/document-intake/{id}` and `/document-intake/{id}/resolve`. | Determines the endpoints the screen calls. | Use API-P5-010..013 (`/review-items`, `/intake-items/{id}`, `/resolve`); the section 13 wording is a known defect. | RESOLVED | SPEC-RWB-E1-054-001 |
| CLAR-002 | Header; SPEC-006 | The header `Depends on` omits RWB-E1-024, which section 3 and flow step 7 require for `DocumentStore.store`. | The story cannot store without it. | Add RWB-E1-024 as a dependency; it is already in the Epic 1 sequence. | RESOLVED | SPEC-RWB-E1-054-006 |
| CLAR-003 | BR1; RWB-E1-032; SPEC-001 | 054 says the queue holds items with a `review_reason`; 032 holds unmatched items by `match_status` with no review reason. | The queue would omit the Unmatched tab. | Include items with a review reason or a held match status; display `review_reason` when present, otherwise `match_status`. One queue, two tabs. | RESOLVED | SPEC-RWB-E1-054-001 |
| CLAR-004 | Contract; SPEC-006 | The story sends `caseNo`; the API schema `IntakeResolveRequest` uses `caseId`. | Determines the request field. | Use `caseId`; the screen resolves a typed case number through `CaseDirectory` before the call. | RESOLVED | SPEC-RWB-E1-054-006 |
| CLAR-005 | Preconditions; SPEC-001 | `REVIEW_TEAM_UNATTACHED` is "DOC-SVC" in the story and "LIT-BKK" in the test background. | Determines which team sees no-candidate items. | It is a parameter; DOC-SVC is the assumed production value and LIT-BKK is the test fixture. | RESOLVED | SPEC-RWB-E1-054-001 |
| CLAR-006 | AC10; RWB-E1-053 BR2; SPEC-004 | AC10 says a type change shows every new field in REVIEW, while 053 marks fields OK at or above the threshold. | Determines whether the officer must confirm every field after a type change. | A manual type change is a review action: re-run extraction and mark the new type's fields REVIEW for confirmation. Automatic extraction keeps 053's threshold rule. | RESOLVED | SPEC-RWB-E1-054-004 |
| CLAR-007 | AC3; SPEC-009 | Can a stored document's type be changed? | Determines whether 054 can correct a wrong stored type. | Not in this story: 054 confirms or corrects fields of a stored document and does not change its type. The stored-type and write-once question is CLAR-010. | RESOLVED | SPEC-RWB-E1-054-009 |
| CLAR-008 | BR9; SPEC-008 | Does a discard delete the file? | Determines retention behaviour. | No: the file stays in the intake container and the reason and person are recorded, under REQ-DCM-019. | RESOLVED | SPEC-RWB-E1-054-008 |
| CLAR-009 | BR7; SPEC-010 | What does the labeled set expose? | Determines the model evaluation feed. | Intake or document ID, predicted type, confirmed type, and extracted and confirmed values per field; no OCR text. | RESOLVED | SPEC-RWB-E1-054-010 |
| CLAR-010 | BR6; RWB-E1-032 CLAR-008; SPEC-009 | A stored low-confidence document whose type is confirmed as legal may need to move to the write-once container; 054's review request carries no type. | Determines whether 054 can complete such a document's review. | 054 confirms fields only for a stored document; the type confirmation and the write-once move are owned by RWB-E1-032 CLAR-008. 054 does not move the file. | RESOLVED | SPEC-RWB-E1-054-009 |

`CLARIFICATION_STATUS: RESOLVED` — all 10 items are answered from the story, the FSD/TSD, the API specification or the decision log. No item changes the business outcome of 054; CLAR-010 records the boundary with the blocked RWB-E1-032.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New SCR-31 review queue with intake resolution, field review, attach, discard and labeled-set feed; new review endpoints and the existing field PATCH.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new review capability with new endpoints and a new screen]
REQUIREMENT_COVERAGE_SUMMARY: All 10 business rules, 17 acceptance criteria and 13 exception paths are mapped; CLAR-010 records the dependency on RWB-E1-032 CLAR-008.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 10] [COVERED_RULES: 10] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 2] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md; the stored-document type move waits on RWB-E1-032 CLAR-008; then start the Implementation Planner.
```
