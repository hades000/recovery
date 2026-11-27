# RWB-S2-E3015-APP Capture the collateral inspection in the field

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-015 for rwb-treatment. The field capture leaves the monolith's S2 service in the one `recovery` schema and becomes the field-inspection step of `TreatmentWorkflow` on this service's own task queue, writing the inspection outcome, the checklist references and the bill references on the treatment row in the same transaction as the local decision record (DP-03), taking the collateral facts from the case signal instead of a `v_ace_collateral` read (DP-05), requesting the checklist, the photographs and the bills as documents of rwb-document, reaching the field app and the screens through the gateway-bff composite route (DP-19), and reporting INSPECTION_COMPLETED of R-DIL-22 to the parent `CaseWorkflow` without a case status of its own. No event is published on this path. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-Z |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3015-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the field-inspection step of `TreatmentWorkflow` on task queue `rwb-treatment` — the completion of the checklist with its photographs and its bills against a treatment (`inspectionOutcome`, `inspectionChecklistRef`, `inspectionPhotoRefs`, `inspectionBillRefs`, `inspectedAt`, `fieldOfficerRef`), the validation of the required elements (VR-S2-015-1, MSG-GEN-001), the local decision record written in the same transaction (DP-03), and the INSPECTION_COMPLETED outcome of R-DIL-22 reported to the parent `CaseWorkflow`** — with the case status and the case task held by rwb-case, the collateral facts arriving on the case signal, the checklist, the photographs and the bills stored as documents of rwb-document, and the screens and the field app reached through the gateway-bff composite route, so that **a deed in lieu stops waiting on a paper inspection and reaches the asset-unlock decision the same day, and no case table, no document table and no ACE collateral view is read or written by this service**.

This is the application slice of legacy RWB-E3-015. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and data rows they depend on;
- the field-inspection step of `TreatmentWorkflow`, the stage child of `CaseWorkflow` on rwb-case, with the four activities `attachInspectionCaptures`, `recordInspection`, `recordAndApply` and `reportInspectionOutcome`;
- the treatment columns that hold the inspection facts, in schema `rwb_treatment`, added on the service's own migration sequence;
- the local decision record written through RWB-PLT-E1027-CON in the same transaction as the treatment change (DP-03);
- the request for the checklist, the photograph set and the bills on rwb-document's queue through the workflow kit, and the references that return as facts;
- the entry of the capture and the screen path of SCR-14, SCR-15 and SCR-16 through the gateway-bff composite route (DP-19).

It does not own: the published element set, the no-new-table rule, the compatibility rule and the fakes, which are RWB-S2-E3015-CON; the treatment record and its fields DF-TRT-001 to DF-TRT-033, which are RWB-S2-E3001-APP; the offer, the settlement range and the below-floor signature, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the deed-in-lieu stage that schedules the inspection and runs the transfer, which is RWB-S2-E3012-APP; the asset-unlock rule, which is the slice of RWB-E3-014; the documents, their templates and the field captures, which are rwb-document and FEAT-TRT-18; the case status, the case task and the inspector's queue, which stay rwb-case's; and the deployment, the flags and the alerts, which are this legacy key's DevOps story.

### 2. Business rationale

A restructure, a settlement or a deed in lieu takes 23 to 26 days and is tracked by hand (FSD S2 A2.15.1; A1.3), against the module's own five-day turnaround target measured from the decision log and the Workbench records. In a deed in lieu the step that costs the days is not a decision: it is the visit to the property, the checklist, the photographs and the bills, and the hand-carried return of all four to the officer (R-DIL-18 then R-DIL-22: the case is held at WITH_FIELD_INSPECTION until `checklist, photographs and bills captured`). FEAT-TRT-15 asks for that visit to be recorded in the Workbench against the case, with the field app and the document hub as its integration points.

The monolith answered it in one process: the S2 service moved `recovery_case.status` itself, wrote `decision_log_entry` with the rule version, wrote `document` rows for the photographs, read `v_ace_collateral` and `v_ace_collateral_detail` directly for the title document number, the plot number and the lien rank, and had no place of its own for the checklist or the bills, which is why they were distinguished by screens and free text. In the 19-service target each of those facts has a different owner. The case status and the inspector's task are rwb-case's and reach the step on the case signal the parent forwards (ASM-4409). The record is the platform library's, written locally in this service's schema (DP-03). The collateral facts are rwb-source-data's, and the connection matrix gives rwb-treatment no call to rwb-source-data, so they arrive as facts on the signal and no `v_ace_*` view is read here (DP-05; ASM-4409). The checklist, the photographs and the bills are documents of rwb-document, requested and referenced (ASM-4410).

What the business keeps is the rule, not the code: R-DIL-22 moves the case to the asset-unlock decision when the checklist, the photographs and the bills have been captured, and R-DIL-18 is the rule that scheduled the visit. The state names, the checklist items, the clocks and the reason codes are values in force of their owners, never constants (BR-S2-015).

AC2 and AC3 name R-RES-12 and R-SET-09, the credit-decline and counter-offer steps of the other two routes: they are carried verbatim because the legacy story owns them and are evaluated by the sibling slices (GAP-2678; ASM-4412). No requirement of the FSD maps to FEAT-TRT-15 (GAP-2678; ASM-4410).

### 3. Preconditions

- RWB-S2-E3015-CON is published: the inspection element set with its values and its absent-until rule, the no-new-table rule, the reference to the treatment update surface, the compatibility rule and the fakes (H).
- RWB-PLT-E1027-CON is published (DP-03): `DecisionRecordWriter.record(DecisionRecord)` with propagation `MANDATORY`, the refusal `DecisionLogRecordInvalidException` with MSG-P7-009 and its field, and `DecisionLogUnavailableException` with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): the gateway-bff composite route by which the field app and SCR-14, SCR-15 and SCR-16 reach this service, one hop (H).
- RWB-S2-E3001-APP is done: `treatment` exists in schema `rwb_treatment` with DF-TRT-001 to DF-TRT-033, and the service's own migration sequence is the only place a column is added.
- RWB-S2-E3012-APP is done or in build in the same lane: `TreatmentWorkflow` runs as the stage child of `CaseWorkflow` on queue `rwb-treatment`, and R-DIL-18 has put the case at WITH_FIELD_INSPECTION; this step is entered from that state.
- The case signal carries the case status, the product, the case and collateral facts and the inspection need; the parent moves the status and raises the task (ASM-4409).
- `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed and the DEEDINLIEU package is in force with its version label, evaluated by the embedded Drools runtime (ASM-4411).
- The document hub answers on rwb-document's queue through the workflow kit and returns document references, never content (ASM-4410).
- The access guard is the platform guard library's: the capability area is "Treatment and offer" and the right the capture needs is U, held by the roles TSD S2 T6.1 lists; the field collector of the legacy story is a person holding one of those roles, because the matrix names no separate field role (GAP-2678; ASM-4412).
- The checklist items, the required elements, the clocks and the reason codes are values in force of their owners; this step holds no copy of any of them.
- No approval of this story is needed to build against a Draft contract baseline; RWB-S2-E3015-CON tags the version when its tests pass (ASM-4413).

### 4. Flow

1. The parent `CaseWorkflow` on rwb-case forwards the case signal to the running `TreatmentWorkflow` child on `rwb-treatment`; the signal carries the case status WITH_FIELD_INSPECTION, the product, the treatment ID, the collateral facts and the inspection need, and the status stays rwb-case's (ASM-4409).
2. The field collector opens the capture on the field app, which reaches this service through the gateway-bff composite route; the guard checks the capability area "Treatment and offer" and right U against the roles of TSD S2 T6.1 (DP-19; ASM-4412).
3. `attachInspectionCaptures`: the checklist entries, the photograph set and the bills are submitted; the step requests their storage on rwb-document's queue through the workflow kit and holds the returned references, never the content (ASM-4410).
4. Validation runs against VR-S2-015-1: an element the checklist in force marks required and the submission leaves empty stops the step with MSG-GEN-001 and the field name, and nothing is written.
5. `recordInspection` composes `inspectionOutcome` from the checklist against the values in force and stamps `inspectedAt` and `fieldOfficerRef` from the actor of the request, not from a stored personal field.
6. `recordAndApply`, one transaction: the treatment row takes `inspectionOutcome`, `inspectionChecklistRef`, `inspectionPhotoRefs`, `inspectionBillRefs`, `inspectedAt` and `fieldOfficerRef`; the decision record is written through `DecisionRecordWriter.record` (decision code D6.4, the rule ID and the rule version of the package that answered, the recommendation, the final call, the outcome and the time); no outbox row is written because this step publishes nothing (GAP-2678; ASM-4410).
7. `reportInspectionOutcome` returns INSPECTION_COMPLETED of R-DIL-22 to the parent; the parent moves the case to ASSET_UNLOCK_DECISION and the asset-unlock rule of R-DIL-23 runs in the slice of RWB-E3-014, not here.
8. A checklist that is incomplete holds the case at WITH_FIELD_INSPECTION and names the missing item with MSG-GEN-001; no unlock is run and no treatment fact is written on a partial submission.
9. A redelivered case signal or a repeated submission answers the open step and starts no second document request and no second record: the rejection and the workflow ID of this treatment carry the idempotency. The locks of the route are workflow timers of the stage, so a restart loses nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without right U submits or reads a capture | 403 from the guard; the refusal is logged and nothing changes | MSG-P4-002 | TC-E3-015-05 |
| X2 | The decision record cannot be written | The transaction rolls back: no treatment column, no reference and no report to the parent | MSG-P7-003 | AC4, TC-E3-015-06 |
| X3 | The record is refused for a missing or invalid field | The transaction rolls back and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | A required element of the checklist is empty | The step holds at WITH_FIELD_INSPECTION and names the field; nothing is written | MSG-GEN-001 | AC1, TC-E3-015-01 |
| X5 | The document hub does not answer inside the step | The request is retried on the kit's policy; the capture is held and no reference is invented | None | AC1 |
| X6 | The offer or settlement figures the screen shows are stale | The screen asks for a new figure and the step does not depend on the stale one | MSG-S2-002 | AC1 |
| X7 | The case is not at WITH_FIELD_INSPECTION when the capture arrives | The step refuses the submission, names the state it holds and reports nothing to the parent | None | AC1 |

X1 and X2 are the two exception flows the FSD records for FEAT-TRT-15, AC-EXC-S2-015-01 (a role without the right) and AC-EXC-S2-015-02 (the decision cannot be recorded), and are carried as written (FSD S2 A2.15.4.3). MSG-S2-001 and MSG-S2-003 belong to the offer slices and are listed in section 14 because the legacy story carried them.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published element set and fakes of RWB-S2-E3015-CON, the decision-record contract and the gateway route; no live rwb-case or rwb-document is needed to start, and the case status, the collateral facts and the document references arrive on mocks |
| Negotiable | The activity names, the checklist composition and the request bodies are this story's choice; the checklist items, the required elements, the clocks and the state names are fixed by their owners' data |
| Valuable | A field visit reaches the Workbench the same day, the inspection is provable with the rule version that answered, and the deed in lieu stops waiting on paper |
| Estimable | One stage step, four activities, six treatment columns and one report to the parent |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments and checklists through the contract fakes, plus one component test of the guard and the step entry |

### 7. Acceptance criteria

```gherkin
Feature: Capture the collateral inspection in the field

  Scenario: AC1 Capture the collateral inspection in the field (legacy RWB-E3-015 AC1)
    Given the rwb-case contract mock returns the case signal in state WITH_FIELD_INSPECTION
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the field officer record the inspection, the checklist and the bills against the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-12 (legacy RWB-E3-015 AC2)
    Given the rwb-case contract mock returns case status AWAITING_CREDIT_APPROVAL
    Given a case in state AWAITING_CREDIT_APPROVAL
    When credit declined
    Then record the reason against the limit applied
    Then the case moves to DECLINED_BY_CREDIT

  Scenario: AC3 Rule R-SET-09 (legacy RWB-E3-015 AC3)
    Given the rwb-case contract mock returns case status OFFER_WITH_CUSTOMER_SET
    Given a case in state OFFER_WITH_CUSTOMER_SET
    When customer counter offered
    Then return the case to the officer and re-test against the floor
    Then the case moves to WITH_FCR_OFFICER_SET

  Scenario: AC4 Not recorded (legacy RWB-E3-015 AC4)
    Given the decision-record library mock returns the failure MSG-P7-003
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line and every legacy value above is kept character for character, including the legacy repetition of `Then`; what changes is where it runs, who holds each fact and how it is reached. "The user acts on the screen" of AC1 is the field collector on the capture of the field app through the gateway-bff composite route (DP-19), and the step it reaches is the field-inspection step of `TreatmentWorkflow` on queue `rwb-treatment` in namespace `rwb-recovery` (DP-12). "Record the inspection, the checklist and the bills against the case" is the treatment row taking `inspectionOutcome`, `inspectionChecklistRef`, `inspectionPhotoRefs` and `inspectionBillRefs`, the documents themselves being rwb-document's (ASM-4410). "Writes the result to the decision log with the rule version" is the local `decision_record` written through RWB-PLT-E1027-CON in the same transaction, so the version of the package that answered is provable; `decision_log_entry` is P7's ledger and is neither written nor read here (DP-03). The states of AC2 and AC3 — AWAITING_CREDIT_APPROVAL, DECLINED_BY_CREDIT, OFFER_WITH_CUSTOMER_SET, WITH_FCR_OFFICER_SET — stay rwb-case's, which is why the two added Given lines are answered by the rwb-case contract mock standing in for the case signal: the stage reports the rule outcome and the parent moves the status (ASM-4409). R-RES-12 and R-SET-09 are the credit-decline and counter-offer rules of the restructure and settlement slices, not of the inspection step, and are carried because the legacy story names them (GAP-2678; ASM-4412); the inspection step's own answer is R-DIL-22. The mock of AC4 is the decision-record library's own failure answer (MSG-P7-003). Values that no source gives — the checklist item set, the element types and the reference shapes — are Not specified in the source documents (GAP-2678; ASM-4410).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The checklist, the photographs and the bills are captured against the treatment, and the step holds at WITH_FIELD_INSPECTION until all three are complete | R-DIL-22; FSD S2 A2.15.2 |
| BR2 | A required element left empty stops the step and names the field, and nothing is written | VR-S2-015-1; MSG-GEN-001 |
| BR3 | The step reports INSPECTION_COMPLETED to the parent, and the asset-unlock rule that follows is not this step's | R-DIL-22; R-DIL-23 |
| BR4 | The inspection facts live on the treatment row and no table is created for the inspection, the checklist, the photographs or the bills | TSD S2 T3.1; GAP-2678; ASM-4410 |
| BR5 | The checklist, the photographs and the bills are stored by rwb-document and the treatment holds references only | ASM-4410; DP-01 |
| BR6 | No value a business person may change is written in code: the checklist items, the required elements, the clocks, the state names and the reason codes are read as values in force with their version | BR-S2-015; FSD S2 A2.15.3.1 |
| BR7 | A step whose decision cannot be recorded does not take effect: the record joins the caller's transaction and a failed append rolls everything back | R-UNI-39; RWB-PLT-E1027-CON; Principle 5 |
| BR8 | The case status, the case task and the inspector's queue stay rwb-case's, and the collateral facts arrive on the case signal | DP-01; ASM-4409 |
| BR9 | The capture acts on the capability area "Treatment and offer" with right U, and a role the matrix does not grant is refused | TSD S2 T6.1; MSG-P4-002; ASM-4412 |

**Where each rule lives in the target.** BR1 and BR2 are `attachInspectionCaptures` and `recordInspection`: the checklist in force is read with its version and the required set is its data, not a constant (BR6). BR3 is `reportInspectionOutcome`, a report on the workflow and never a status write. BR4 is the six treatment columns and the absence of an inspection table. BR5 is the request to rwb-document and the references that return. BR6 is served by reading every value from its owner; the only fixed strings in this story are the element names of its contract. BR7 is `recordAndApply`: the treatment update and the decision record commit together, and `DecisionLogUnavailableException` (MSG-P7-003) and `DecisionLogRecordInvalidException` (MSG-P7-009) roll it back. BR8 is the signal contract with the parent. BR9 is the platform guard and its data.

### 9. State transitions

None of the states below is this service's to change (ASM-4409). The step evaluates the rule, records the outcome and reports it to the parent `CaseWorkflow`, and the parent moves the case status in rwb-case. The first two rows are the inspection step this story builds; the last two are the rows AC2 and AC3 name and are shown as the stage asserts them, applied by the restructure and settlement slices (GAP-2678).

| From (case status, rwb-case's) | Event | Condition | To (case status, rwb-case's) | Rule |
|---|---|---|---|---|
| OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product = MTG and signature is wet ink per Legal | WITH_FIELD_INSPECTION | R-DIL-18 |
| WITH_FIELD_INSPECTION | INSPECTION_COMPLETED | checklist, photographs and bills captured | ASSET_UNLOCK_DECISION | R-DIL-22 |
| AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | `final_call = rejected` | DECLINED_BY_CREDIT | R-RES-12 |
| OFFER_WITH_CUSTOMER_SET | CUSTOMER_COUNTER_OFFERED | `counter_amount < floor_price` | WITH_FCR_OFFICER_SET | R-SET-09 |

The treatment's own `inspectionOutcome` is empty until the checklist has been captured and carries the value in force after it; the treatment has no state machine of its own beyond the LOV-TRT-OUTCOME values that later steps write (TSD S2 T3.2).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the step, the four activities and the six treatment columns |
| The field collector, in the field app | Submits the checklist, the photographs and the bills; holds one of the roles TSD S2 T6.1 lists with right U in "Treatment and offer" (ASM-4412) |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Hold C, R and U in "Treatment and offer" and may capture or correct an inspection |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the roles listed "and 12 more" | Hold R and may read the capture |
| RW-AUDIT, RW-COE | Read the recorded decision and the inspection outcome; they change nothing |
| rwb-case (P3) | Owns the case status, the case task and the inspector's queue |
| rwb-document (P5) | Owns the checklist, the photographs, the bills and their templates |
| rwb-source-data (P1) | Owns the collateral and customer read that reaches this step as facts |
| rwb-decision (P7) | Owns the rule packages, their versions and the ledger |
| No delegation of authority level applies to this story | The story builds the step; no credit decision is taken here |

No credential, personal name or email address appears in the workflow input, the activity payloads or the logs, which carry treatment and case identifiers, checklist codes, document references, versions and timestamps only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| (no field ID) | treatment | inspectionOutcome, inspectionChecklistRef, inspectionPhotoRefs, inspectionBillRefs, inspectedAt, fieldOfficerRef | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record (library object in `rwb_treatment`) | id, case_id, decision_code, rule_id, rule_version, decision_at and the rest | Write through `DecisionRecordWriter` |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral (`rwb_source_data`'s read) | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and the rest | Read as facts on the case signal, never from the view |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail (`rwb_source_data`'s read) | asset_key, title_doc_no, plot_no, area_text, province, lien_rank and the rest | Read as facts on the case signal, never from the view |
| DF-REF-001 to DF-REF-015 | rule_row (`rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and the rest | Read as the evaluated package, never from the table |

`treatment` is this service's table and the only one this story writes, together with the library's `decision_record` in the same schema (DP-01; DP-03). The six inspection columns carry no field ID and no definition in the TSD, which lists DF-TRT-001 to DF-TRT-033 and has no inspection, no checklist and no bill: their names and types are the working read of the gap and the assumption below. `recovery_case`, `document` and the two collateral views belong to rwb-case, rwb-document and rwb-source-data: the case and collateral facts arrive on the case signal, the documents are requested and not written, and no ACE view is named in a statement of this service (DP-05). Field IDs are those of the Logical Data Model and Data Dictionary. The inspection elements, their types and the treatment's holding of them are Not specified in the source documents (GAP-2678; ASM-4410).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story declares no operation of its own: the capture rides on the treatment surface its siblings publish. The treatment resource and its read are RWB-S2-E3001-CON's (`POST /cases/{caseId}/treatments`, `GET /treatments/{treatmentId}`), and the change of the treatment's terms is RWB-S2-E3002-CON's (`PATCH /treatments/{treatmentId}`), which is the operation the field app calls with the inspection elements; the submit and offer forms belong to the sibling slices.

| Element this story writes on the treatment | Domain | Absence rule |
|---|---|---|
| `inspectionOutcome` | The checklist result of R-DIL-22: complete, or incomplete with the missing item named | Absent until R-DIL-22 has answered |
| `inspectionChecklistRef` | The document reference rwb-document returns for the completed checklist | Absent until the checklist is stored |
| `inspectionPhotoRefs` | The document references of the photograph set | Absent until the photographs are stored |
| `inspectionBillRefs` | The document references of the bills captured at the visit | Absent until the bills are stored |
| `inspectedAt` | timestamptz of the completed capture | Absent until the capture is recorded |
| `fieldOfficerRef` | The user identifier of the officer who captured, never a name | Absent until the capture is recorded |

The element names, their types and their reference shapes are Not specified in the source documents (GAP-2678; ASM-4410), and RWB-S2-E3015-CON fixes them for the wave.

#### 12.2 REST operations consumed

None. The case status, the product, the collateral facts and the inspection need arrive on the case signal the parent `CaseWorkflow` forwards, which is the only way a case fact reaches this service (ASM-4409). The document storage is reached through Temporal on rwb-document's queue, because route services reach shared capabilities through Temporal and never REST (Architecture v5 slide 13 note; ASM-4410). The Work Package lists no contract dependency for this story, and none is added.

#### 12.3 Events published

None on this path. The service publishes one event type, `rwb.treatment.TreatmentApproved.v1` (EV-10) on `rwb.treatment.events.v1`, and the deed-in-lieu offer slice — RWB-S2-E3012-APP at R-DIL-16 — publishes it; the inspection completion of R-DIL-22 writes no outbox row.

| Event | Topic | Key | This story | Purpose |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | Not published here: the envelope is RWB-S2-E3003-CON's and the publication is the offer slice's | EV-10: tells rwb-comms to issue the offer documents and rwb-payment to expect the settlement of the debt |

No source names an event for the inspection completion, so the outcome reaches rwb-case on the case signal and the absence is recorded below. Inventing a second event would break the one-event rule of the catalogue, which gives S2 exactly EV-10 (GAP-2678).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | EV-30: names the DEEDINLIEU package version in force, which the step evaluates and writes into the decision record; a version is swapped in at the next event and no restart is needed |

Consumed through the inbox of the outbox library, so a redelivery is deduplicated by the cloud event id. The other events this service subscribes to — `rwb.payment.TreatmentBooked.v1` (EV-11), `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.deviation.DeviationRaised.v1` (EV-06) — are consumed by other stages of `TreatmentWorkflow` and not by this one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow` (rwb-case), one execution per case and stage | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, case status, product, treatment ID and the case and collateral facts; the stage outcome returned to the parent; search attributes CaseId and Stage |
| `attachInspectionCaptures` | Activity | `rwb-treatment` | The checklist, the photograph set and the bills submitted, and the document references returned on rwb-document's queue; idempotent by treatment and request |
| `recordInspection` | Activity | `rwb-treatment` | The checklist composed against the values in force; `inspectionOutcome`, `inspectedAt` and `fieldOfficerRef` |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: the six treatment columns and the decision record through RWB-PLT-E1027-CON |
| `reportInspectionOutcome` | Activity | `rwb-treatment` | INSPECTION_COMPLETED of R-DIL-22 reported to the parent, or the hold with the missing item |

DP-03, DP-05, DP-13 and DP-19 are the patterns this story applies; the activity names are a target design choice fixed by no source document, and the stage model is the workflow kit's. The retry policy is the kit's, and the checklist in force, the clocks and the state names are values the step reads and never sets.

#### 12.6 Schedules

None. The step is signal-started inside `TreatmentWorkflow` and owns no Temporal Schedule and no legacy Quartz job. The clocks of the route — the offer validity, the title hold and the plan installments of the sibling slices — are workflow timers of their steps, and the inspection has no clock of its own in any source.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Updated by `recordAndApply` with the six inspection columns; no row is inserted here |
| `decision_record` | `rwb_treatment` | PLT (library object, written through RWB-PLT-E1027-CON) | Written in the same transaction as the treatment update (DP-03) |
| `outbox` | `rwb_treatment` | S2, from the service template | Not written: this step publishes nothing |
| `document` | `rwb_document` | P5 | Not written and not read: the checklist, the photographs and the bills are requested and their references return as facts |
| `recovery_case`, `assignment` | `rwb_case` | P3 | Not written and not read: the status, the task and the facts arrive on the case signal |
| `v_ace_collateral`, `v_ace_collateral_detail` | ACE views, `rwb_source_data`'s read | P1 | Never named in a statement of this service (DP-05) |

No table is created for the inspection, the checklist, the photographs or the bills, and no foreign key crosses a schema (DP-01; BR4).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3015-CON inspection fake | The six treatment elements and their absent-until rule | A treatment at each inspection state, one with no checklist, one with no photographs, one with no bills and a complete capture |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |
| RWB-PLT-N001-CON gateway route fake | The composite route of the field app and SCR-14, SCR-15 and SCR-16 | A granted right U for the field collector; a refused answer; a scope miss |
| rwb-case case-signal mock | The added Given line of AC1 and the facts of the step entry | Case status WITH_FIELD_INSPECTION, the product and the collateral facts, and the status the parent reports back |
| rwb-document request fake | The checklist, the photographs and the bills | A capture accepted with its references; a missing template; a timeout |
| Inspection value fixture | The values in force | The checklist items, the required set and the reason codes of their owners |

The element, decision-record and gateway fakes are the published contracts of those stories; the case-signal mock stands in for the signal, which is the only way a case fact reaches this service; the document fake stands in for the Temporal call to its owner.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the step declares no operation | 0 | The treatment resource and the terms change are sibling CON stories, reached through gateway-bff (DP-19) |
| Kafka | 0: no event on this path | 1 event (`rwb.decision.RulePackageInForce.v1`) | CloudEvents 1.0 envelope, inbox of the service template |
| Temporal | 1 stage workflow and 4 activities | 1 activity request to rwb-document on its queue | Namespace `rwb-recovery`; no Schedule |
| File | None | None | No file is read or written; the photographs and the bills are documents of rwb-document |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `field-inspection` and `treatment`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract or the service's own ACE views; here the collateral facts arrive on the case signal and no view is named | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record of the capture inside the same transaction; DP-05 is the collateral read that comes to this step as facts, because the connection matrix gives rwb-treatment no call to rwb-source-data; DP-13 fixes the service base on which the sibling operations answer; DP-19 is the route by which the field app and the three screens reach this service. The ownership rule of DP-01 is applied in prose and in the SQL: `recovery_case`, `document` and the two views are never named in a statement of this service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (field-inspection step) | Workflow | The step entry, the capture, the record, the outcome report and the hold |
| `attachInspectionCaptures` | Activity | The document requests and the references that return |
| `recordInspection` | Activity | The checklist composition and the three outcome columns |
| `recordAndApply` | Activity | The six columns and the decision record in one transaction |
| `reportInspectionOutcome` | Activity | The INSPECTION_COMPLETED report to the parent |
| `FieldInspectionHandler` | Handler | The step entry from the case signal: the state, the treatment and the facts mapped onto the step input |
| `TreatmentRepository` | Repository | The update of `treatment` by ID, with the optimistic-lock version of the row |

**Database.** `treatment` already holds DF-TRT-001 to DF-TRT-033. This story adds the six inspection columns on the service's own migration sequence and creates no table: the checklist, the photographs and the bills have none of their own, and their content is rwb-document's (GAP-2678; ASM-4410). `decision_record` is the library object of RWB-PLT-E1027-CON in the same schema.

**Configuration and reference data.** The checklist items, the required set, the state names, the clocks and the reason codes are values in force of their owners and are read, never set here (BR6). The package version arrives through `rwb.decision.RulePackageInForce.v1`. The capability area and the rights are the guard library's data.

**Build steps**

1. The migration that adds the six inspection columns to `treatment` on the service sequence, with no new table.
2. `attachInspectionCaptures` against the document fake, with the accepted capture, the missing template and the timeout (AC1).
3. `recordInspection` against the checklist fixture, complete and incomplete, with MSG-GEN-001 and the field name (AC1).
4. `recordAndApply` with the treatment update and the decision record through the fake, and the rollback on MSG-P7-003 and MSG-P7-009 (AC4).
5. The step entry and the guard, with the case signal, a role without right U and the state that is not WITH_FIELD_INSPECTION (AC1; TC-E3-015-05).
6. `reportInspectionOutcome` and the mocked parent status, plus the two legacy rules of AC2 and AC3 as the sibling slices assert them (AC2, AC3).
7. Tests for AC1 to AC4 against the fakes and the fixtures.

**Feature flag.** `rwb.treatment.field-inspection`.

**Done when.** The tests in section 16 pass, a synthetic deed in lieu walks from WITH_FIELD_INSPECTION to ASSET_UNLOCK_DECISION in SIT with the checklist, the photograph and the bill references recorded on the treatment, an incomplete checklist holds the case with MSG-GEN-001, a forced record failure leaves the treatment unchanged with MSG-P7-003, and the field app shows the capture through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-001 | The offer or settlement figure of the case is below the floor of its case and has been routed for approval (sibling slices) | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | The offer to the customer carries its end date | The offer to the customer ends on {date}. |
| MSG-S2-002 | The payoff or the figure behind the offer is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | A required element of the checklist is empty | Enter {field}. |
| MSG-P4-002 | The role does not hold the right the capture needs in "Treatment and offer" | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to the customer) | The decision record was refused: {field} is missing or not valid. |

The six legacy texts are carried unchanged; MSG-P7-009 comes with the decision-record contract of RWB-PLT-E1027-CON. MSG-S2-001, MSG-S2-002 and MSG-S2-003 belong to the offer and settlement slices and are listed because the legacy story carried them. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record (Draft; submitted; approved; booked; broken) and SCR-15 Settlement offer (Draft; below floor; approved; sent; accepted) are the two screens the legacy story names, and SCR-16 Deed in lieu (Checks; appraisal; approved; transferred) is the screen of the route this capture belongs to (FSD S2 Screens). The capture itself is opened on the field app, which is the integration point the FSD names for FEAT-TRT-15; no source names a screen, a state set or a field list for the inspection, so this story declares the service side only and the missing screen is the placeholder of the gap (GAP-2678; ASM-4412). All three screens and the field app reach this service through the gateway-bff composite route (DP-19), which calls rwb-treatment and the screen's other owners in parallel, one hop each.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-015-01 | AC1 | End to end | A deed-in-lieu treatment at WITH_FIELD_INSPECTION; the field collector acts on the capture and the checklist, the photographs and the bills are recorded; the decision record carries the rule version |
| TC-E3-015-02 | AC2 | End to end | Case status AWAITING_CREDIT_APPROVAL on the case-signal mock; credit declined; the reason is recorded against the limit applied and the case reaches DECLINED_BY_CREDIT |
| TC-E3-015-03 | AC3 | End to end | Case status OFFER_WITH_CUSTOMER_SET on the case-signal mock; the customer counter offers; the case returns to the officer, is re-tested against the floor and reaches WITH_FCR_OFFICER_SET |
| TC-E3-015-04 | AC4 | End to end | The decision-record fake refuses the write; nothing changes and MSG-P7-003 is shown |
| TC-E3-015-05 | Access | Component | A role without right U submits a capture; refused with MSG-P4-002 and nothing changes |
| TC-E3-015-06 | Principle 5 | Component | A forced decision-record write failure stops the action with MSG-P7-003; the treatment row, the document references and the parent report are unchanged |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The contract fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies belong to the wave 2 integration harness, RWB-ITG-W2, and are not listed here.

### 17. Guardrails

- No business value in code: the checklist items, the required set, the clocks, the state names and the reason codes are values in force of their owners, read with their version, never constants (BR6).
- No personal data in logs, events, workflow inputs or the fixture: the step carries treatment and case identifiers, checklist codes, document references, versions and timestamps, and `fieldOfficerRef` is a user identifier, never a name.
- No photograph, bill or checklist content in the service, in a payload or in a log: the documents are rwb-document's and this service holds references only (BR5).
- No read of another service's table and no read of an ACE view: the case and collateral facts arrive on the case signal and no `v_ace_*` view is named in a statement of this service (DP-01; DP-05).
- No new table for the inspection, the checklist, the photographs or the bills, and no second write path for an inspection fact (BR4).
- No write outside the transaction that records the change: the treatment update and the decision record commit together or not at all (DP-03; BR7).
- No case status and no case task is written: the parent moves the status and raises the task on the step outcome (ASM-4409).
- No event is invented for the inspection, and no credential, secret or document content appears in code, configuration or a prompt.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| Not specified in the source documents (GAP-2678; ASM-4410) | No requirement of the FSD S2 maps to FEAT-TRT-15; the module's REQ-S2-001 to REQ-S2-010 are traced to FEAT-TRT-01 (TSD S2 T8) | Business Requirements Program, section 5.9 | FEAT-TRT-15 | 07 Route, settle and claim | R-DIL-18; R-DIL-22 | TC-E3-015-01 |
| (no requirement ID) | The inspection feeds the deed-in-lieu readiness of the route | Business Requirements Program, section 5.9 | FEAT-TRT-15 | 07 Route, settle and claim | R-DIL-22 | TC-E3-015-01 |
| Legacy rules named by the criteria | R-RES-12 and R-SET-09 are the credit-decline and counter-offer steps of the restructure and settlement slices | Business Requirements Program, section 5.9 | The legacy story's own feature | 07 Route, settle and claim | R-RES-12; R-SET-09 | TC-E3-015-02, TC-E3-015-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3015-CON | Contract | H: declares the inspection element set, the no-new-table rule, the compatibility rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, its `MANDATORY` rule and its two exceptions (DP-03) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of the field app and the three screens (DP-19) |
| RWB-S2-E3001-APP, RWB-S2-E3002-APP | App development | Same lane, earlier: the treatment record and the terms surface the capture is written through |
| RWB-S2-E3012-APP | App development | Same lane: the deed-in-lieu stage that schedules the inspection and runs the transfer |
| The slice of RWB-E3-014 | App development | Same service: the asset-unlock rule that follows INSPECTION_COMPLETED |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the same legacy key against rwb-case and rwb-document; not this story's |

### 19. Out of scope

- The published element set, the no-new-table rule, the compatibility rule and the fakes: RWB-S2-E3015-CON.
- The treatment record, its creation, its fields DF-TRT-001 to DF-TRT-033 and its own migration: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The terms surface `PATCH /treatments/{treatmentId}`, the offer and the settlement range: RWB-S2-E3002-APP and RWB-S2-E3002-CON.
- The below-floor second signature and the floor comparison: RWB-S2-E3003-APP and RWB-S2-E3003-CON.
- The scheduling of the inspection (R-DIL-18), the asset-unlock decision (R-DIL-23 to R-DIL-26) and the transfer (R-DIL-28): RWB-S2-E3012-APP and the slice of RWB-E3-014.
- The checklist, the photographs, the bills, their templates, their retention and the document hub: rwb-document and FEAT-TRT-18.
- The field app itself, its offline behaviour and its device capture: the platform edge and the field app's own stories.
- The collateral and customer read: rwb-source-data; the facts reach this step on the case signal and no view is read here.
- The case status, the case table, the inspector's task and the queue: rwb-case and RWB-P3-E1018.
- The rule packages, their versions, the ledger and the approval side of any exception: rwb-decision.
- The topic, its ACLs, the retry topics and the dead-letter topic: the event platform and the platform infrastructure stories.
- The deployment, the flag, the dashboards and the alerts of this build: this legacy key's DevOps story.
- The real cross-service proof against the live rwb-case and rwb-document: the wave 2 integration harness.
