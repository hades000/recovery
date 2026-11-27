# RWB-S2-E3018-APP Generate the treatment document set

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E3-018 for rwb-treatment. The four legacy acceptance criteria are kept word for word with their origin tag and now run on the document-set branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, reached through the gateway-bff composite route (DP-19) and served on the base `/api/recovery/treatment/v1` (DP-13); the one `recovery` schema becomes `rwb_treatment` and no other service's table is read (DP-01); the party set the documents are issued to is read from the service's own read-only `v_ace_customer` view (DP-05); the legacy `DecisionLogWriter` write to the shared `decision_log_entry` becomes the local decision record of RWB-PLT-E1027-CON written in the same transaction as the change (DP-03); the rendering itself is the generation activity of RWB-S2-E2026-APP against the published RWB-P5-E2026-CON and is not restated here; the set answer, the completeness rule and the error set have no source shape and are declared as the working read (GAP-2684; ASM-4425, ASM-4426, ASM-4427, ASM-4428). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 18 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-AC |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (not sized in this story) |
| Depends on (build) | RWB-S2-E3018-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1 (path /api/recovery/treatment/v1, DP-13) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the Workbench to produce the agreement, contract, credit approval and mortgage documents for the treatment chosen**, so that **restructures and settlements reach booking in days instead of the 23 to 26 days the module takes today**.

This is the application slice of legacy RWB-E3-018. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the document-set branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the composition of the set for the treatment chosen — which of the four document types the treatment requires — and the completeness check of the set the rendering returns;
- the rules R-DIL-14 of the DEEDINLIEU package and R-RES-10 and R-RES-13 of the RESTRUCTURE package, with the offer validity and the 3 working-day approval clock read from the rule set in force;
- the local decision record of each set outcome, written through RWB-PLT-E1027-CON in the same transaction as the `treatment` row (DP-03);
- the party set the documents are issued to, read from the service's own read-only `v_ace_customer` view (DP-05), so the set check knows how many parties the set must name;
- the outcome of the `treatment` row in schema `rwb_treatment`, the optional `documentSet` section of the treatment answer, and the stage outcome the parent `CaseWorkflow` uses to move the case status.

It does not own: the published shape of the set section, of the set request and of the error set, which are RWB-S2-E3018-CON; the rendering engine, the templates, the merge fields, the rendered body, the file custody, the retention and the e-signature, which are RWB-S2-E2026-APP, P5 rwb-document and P6 rwb-comms (ASM-4427); the offer, the terms, the transfer price, the floor and the second signature, which are RWB-S2-E3012-APP and its siblings; the treatment record and the treatment read, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the case, its status, its tasks and its timers, which are rwb-case's (ASM-4425); the ACE views themselves and their grant, which are P1's and the ACE DB stories'; the central ledger, which is P7's; and the deployment, which is the wave 2 harness and the platform DevOps stories.

### 2. Business rationale

Legacy RWB-E3-018 existed because the agreement, contract, credit approval and mortgage documents of a treatment were typed by hand from the case file, so a restructure or a settlement sat for weeks between the agreed terms and the booking. The functional specification keeps the objective unchanged — it produces the documents for the treatment chosen from templates — and the program keeps the requirement: REQ-S2-006 states that the credit application, contract and mortgage documents for a deed in lieu are generated from templates, and the module target for the restructure turnaround is 5 days.

What D-RCV-60 changes is where the set is composed, what decides it and what records it. In the monolith the set was a method in the same process as the case row and the decision log. In the target:

- the set branch runs inside `TreatmentWorkflow` on task queue `rwb-treatment`, as the stage child of `CaseWorkflow`, so the document set is decided where the RESTRUCTURE and DEEDINLIEU rules live and the case keeps one parent workflow from entry to closure (ASM-4425);
- the rendering is a call the treatment side already owns: RWB-S2-E2026-APP's `generateContractDocument` activity asks the generation operation of RWB-P5-E2026-CON, and this story composes the set, checks what comes back and records it. The call, its contract, its fake and its error set are that story's, so this one publishes no REST call and records no C dependency (ASM-4427);
- the party set is read from the ACE customer view this service is granted, read only, and never from another service's table (DP-05; DP-01);
- the set outcome and the decision go to `rwb_treatment` and to the local decision record in one transaction (DP-03);
- the case status stays rwb-case's: the stage reports an outcome and the parent moves the status (ASM-4425);
- the officer reads the set through the gateway-bff composite route, one hop, on SCR-15 and SCR-14 (DP-19; DP-13).

No business value moves. The 14-day offer validity of R-DIL-14 and the 3 working-day approval clock of R-RES-10 are values in force in the rule set, read with the rule version and never written in code (BR-S2-018).

### 3. Preconditions

- RWB-S2-E3018-CON is published: the `documentSet` section of the treatment answer, its properties, the set request element, the error set, the compatibility rule and the fakes are baselined and handed to this story. The section and the request have no source shape and are published as the working read (GAP-2684; ASM-4428).
- RWB-PLT-E1027-CON is published with its writer fake: `DecisionRecordWriter.record(DecisionRecord)` runs with `@Transactional(propagation = MANDATORY)`, refuses with MSG-P7-009 and fails with MSG-P7-003, so the set outcome and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-15 Settlement offer and SCR-14 Treatment record reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The document set is rendered by the `generateContractDocument` activity of RWB-S2-E2026-APP, built against RWB-P5-E2026-CON with its fake; that contract answers the generated documents with `documentId`, `documentType`, `docVersion`, `templateCode`, `templateVersion` and `status`. This story consumes that activity's result inside the same service and declares no REST call of its own (ASM-4427).
- The four document types of the set are the catalogue's values — the agreement, the contract, the credit approval and the mortgage document — with the template code and the Legal-approved template version of each read at their version in force; no code, no version and no type is written in code (BR-S2-018; ASM-4427).
- `v_ace_customer` is readable by the login of rwb-treatment with SELECT only and carries the party rows of the case, DF-ACE-055 to DF-ACE-074; the read establishes which parties the set must name, and the merged personal values on the document body belong to the rendering engine and are masked by policy (DP-05; ASM-4426).
- The case status signal is available: the parent `CaseWorkflow` forwards the case status change to the running stage, carrying the case, the route, the treatment type and the treatment reference. Where the rwb-case contract fixes field names, they are copied from it; no source fixes them here (GAP-2684; ASM-4425).
- The embedded Drools runtime and the RESTRUCTURE and DEEDINLIEU packages are the service template's wave-0 capability, and the package version in force arrives on `rwb.decision.RulePackageInForce.v1`; this story names the packages and their versions and adds no build dependency of its own (ASM-4429).
- The access guard, the outbox and inbox library and the workflow kit are service-template capabilities; this story declares the capability area "Treatment and offer", the rights C and R and the call types and adds no build dependency of its own (ASM-4430).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with DF-TRT-001 to DF-TRT-033 and the library object `decision_record`; this story adds no table, no column and never edits an applied migration.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3018-CON when its tests pass.

### 4. Flow

1. The case reaches TRANSFER_PRICE_SET on the deed-in-lieu route or WITH_FCR_OFFICER on the restructure route; the parent `CaseWorkflow` forwards the status change to the running `TreatmentWorkflow` child on queue `rwb-treatment` as a signal, and the stage never calls rwb-case (ASM-4425).
2. `composeDocumentSet` reads the treatment row — the type (DF-TRT-004), the transfer price or offer amount (DF-TRT-007) and the validity (DF-TRT-010) — and builds the set the treatment type requires: for a deed in lieu the credit approval, the contract and the mortgage document, for a restructure the agreement, each with the template code and the version in force.
3. The same activity reads `v_ace_customer` for the party set of the case, read only, and records on the set request how many parties the documents must name; no name, no identifier and no address is copied into the request, and no field classed as personal data is carried in it (DP-05; ASM-4426).
4. The request is handed to the `generateContractDocument` activity of RWB-S2-E2026-APP, which owns the call to the generation operation of RWB-P5-E2026-CON, one hop with a 2 s timeout and a breaker; this stage waits for the generation result and never calls rwb-document itself (ASM-4427).
5. The generation result returns one document per requested template code, each with `documentId`, `documentType`, `docVersion`, `templateCode`, `templateVersion` and `status`, or a refusal with its message identifier and the field it names.
6. `evaluateSetRules` checks the set against the request — every type present once, every `templateVersion` the approved version in force, no document in a refused state — and evaluates the rule set: R-DIL-14 on TRANSFER_PRICE_SET with `transfer_price >= floor_price` sends the set to OFFER_WITH_CUSTOMER_DIL; R-RES-10 on WITH_FCR_OFFICER with the offer outside the range or `deviation_flag = Y` sends the case to AWAITING_CREDIT_APPROVAL; R-RES-13 escalates an approval that ages past `approval_escalation_limit` to the head of credit and keeps the state.
7. `recordAndApply` assembles the `DecisionRecord` — the decision code of the set event, the case, the rule ID with the package version, the recommendation, the final call and the actor — and writes it through `DecisionRecordWriter.record` in the caller's transaction, then writes the set outcome and the decision reference to the `treatment` row in the same transaction (DP-03).
8. The stage publishes nothing: it reports the outcome to the parent `CaseWorkflow`, which moves the case status and raises the officer task where the set was refused or incomplete (ASM-4425).
9. The officer reads the set on SCR-15 Settlement offer and SCR-14 Treatment record, through the treatment read and its `documentSet` section, one hop through the gateway-bff composite route (DP-19): the type, the template code, the pinned template version, the document reference, the set status, the rule ID and version, and the completion time.
10. On a refused or incomplete set nothing moves and the case stays where it is: the officer sees the named field or the refused template, corrects the terms through the offer stories, and the stage re-runs on the next signal with a new decision record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role does not hold the right on "Treatment and offer" | 403 before any read; the refusal is the guard library's and is logged by it | MSG-P4-002 | AC1, TC-E3-018-05 |
| X2 | The decision record cannot be written | `recordAndApply` throws before the `treatment` row is written and the transaction rolls back; nothing changes | MSG-P7-003 | AC4, TC-E3-018-06 |
| X3 | The decision record is refused for a missing or invalid field | Nothing is written and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | A value the document needs is absent, or the rendering refuses the set for a field | The set is marked incomplete with the field it names, nothing moves and the officer task names the field | MSG-GEN-001 | AC1 |
| X5 | The template version is not the approved version in force, or the template is withdrawn | The set is refused before the request names it, the reason is recorded and nothing moves | None in the source | AC1 |
| X6 | No template covers the treatment type and the product group | The set cannot be composed: the stage reports an unmatched outcome and raises a task for the case owner; nothing is generated | None in the source | AC1 |
| X7 | The price is below the floor on the deed-in-lieu route | Not this story: the set is not composed for that state and the second-signature route is RWB-S2-E3016-APP's | None in the source | AC2 |
| X8 | The rule package in force is not the one the step started on | The step re-evaluates against the package named on `rwb.decision.RulePackageInForce.v1` and records the version it used | None | AC1, AC3 |

X1 to X3 are the exception paths of RWB-E3-018 carried onto the split, X4 to X6 are the set paths the catalogue and the rendering add, X7 is the boundary with the offer stories of the same module, and X8 belongs to the parent-and-child workflow model of the target. The offer validity of 14 days and the 3 working-day approval clock are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published set contract, the decision-record library, the generation activity of the sibling story and the gateway route with their fakes, on its own schema and its own ACE view, and needs no live rwb-case, no live rwb-document and no live rwb-decision to start |
| Negotiable | The activity names, the decision code per set event and the shape of the stage outcome are this story's choice; the rules, the four document types, the messages and the two screens are fixed |
| Valuable | The four documents of a treatment exist and are checked before the offer leaves, and every set carries the template version and the rule version that produced it |
| Estimable | One workflow branch, three activities, one view read set, one repository and one record write |
| Small | Finished inside two weeks with its tests on the fakes and the view fixture |
| Testable | Each criterion runs on synthetic treatments and party rows through the fake and the rwb-source-data contract fake for the party read, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Generate the treatment document set

  Scenario: AC1 Generate the treatment document set (legacy RWB-E3-018 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the agreement, contract, credit approval and mortgage documents for the treatment chosen
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIL-14 (legacy RWB-E3-018 AC2)
    Given the rwb-case contract mock returns case status TRANSFER_PRICE_SET
    Given a case in state TRANSFER_PRICE_SET
    When price inside floor
    Then generate the credit approval, the contract and the mortgage documents
    Then the case moves to OFFER_WITH_CUSTOMER_DIL

  Scenario: AC3 Rule R-RES-10 (legacy RWB-E3-018 AC3)
    Given the rwb-case contract mock returns case status WITH_FCR_OFFICER
    Given a case in state WITH_FCR_OFFICER
    When offer prepared
    Then route the offer to credit approval; 44% of TDR cases deviate today
    Then the case moves to AWAITING_CREDIT_APPROVAL

  Scenario: AC4 Not recorded (legacy RWB-E3-018 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Each rule of section 8 is applied (new, D-RCV-60)
    Given the rule set and the catalogue are in place
    When a set is composed for a treatment
    Then the rules BR1 to BR8 of section 8 are applied as stated there

  Scenario: AC6 A retried or timed-out activity does not record a second outcome (new, D-RCV-60)
    Given an activity of the document-set branch is retried or times out
    When the retry or the timeout occurs
    Then the decision record holds one outcome for the treatment, written with the rule version

  Scenario: AC7 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case status that the model does not allow to move to the next status
    When the stage reports an outcome that would move the case
    Then the stage reports the refusal and no status is moved by this service
```

**Target reading.** Every line and every value above is the legacy line and the legacy value, unchanged, including the repetition of `Then`, the legacy wording `the action is taken` and the 44% the legacy AC3 carries. What changes is where it runs, what renders the set and how it is reached. The one added line is the mock Given of AC2 and AC3, which stands in for the case status that rwb-case owns, so the stage can be tested before the live case workflow exists (ASM-4425). The set runs on the document-set branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, with the activities `composeDocumentSet`, `evaluateSetRules` and `recordAndApply`. The agreement, contract, credit approval and mortgage documents of AC1 and AC2 are the four document types of the catalogue, rendered by the `generateContractDocument` activity of RWB-S2-E2026-APP against the published RWB-P5-E2026-CON; this stage composes the set, checks every returned document against the approved template version in force, and records the outcome (ASM-4427). "The decision log" of AC1 and AC4 is the local decision record of `decision_record` in `rwb_treatment`, written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)` in the same transaction as the `treatment` row; `decision_log_entry` is P7's ledger and is neither written nor read here (DP-03). The states of AC2 and AC3 — TRANSFER_PRICE_SET, OFFER_WITH_CUSTOMER_DIL, WITH_FCR_OFFICER and AWAITING_CREDIT_APPROVAL — are case statuses of rwb-case: the stage reports the outcome and the parent moves the status, so the transition is proved against the mock and not by a write of this service (ASM-4425). The set answer the officer reads, its property names and the set request are published by RWB-S2-E3018-CON as the working read (ASM-4428).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A deed-in-lieu case whose transfer price is at or above the floor has the credit approval, the contract and the mortgage documents generated before the offer goes to the customer | R-DIL-14; REQ-S2-006 |
| BR2 | A restructure offer outside the approved range, or carrying a deviation flag, is routed to credit approval while its agreement is produced; the approval that ages past its limit escalates to the head of credit and keeps the state | R-RES-10, R-RES-13 |
| BR3 | The set is composed for the treatment type from the catalogue at its version: no document type, template code or template version is a constant of this service | BR-S2-018; ASM-4427 |
| BR4 | A set is complete only when every type the treatment requires is present once, with the approved template version in force, and no document is in a refused state | ASM-4428 |
| BR5 | The decision is recorded with the rule version before or with the change; if it cannot be recorded, nothing changes | DP-03; MSG-P7-003 |
| BR6 | No value a business person may change is written in code: the offer validity, the approval clock, the escalation limit and the document types are values in force, read with their version | BR-S2-018 |
| BR7 | The case status and the officer task are not this service's: the stage reports and the parent moves and raises | DP-01; ASM-4425 |
| BR8 | ACE data is read only, through this service's own view, and never written and never copied into another service's table; the merged personal values on a document body are the rendering engine's and never this service's payload | DP-05; DP-01; ASM-4426 |

**Where each rule lives in the target.** BR1 and BR2 are `evaluateSetRules` against the DEEDINLIEU and RESTRUCTURE packages, with the price, the range, the deviation flag and the approval age taken from the treatment row and the rule set, and no threshold in code. BR3 is the catalogue read of the template code and the version in force, taken at their version and never configured here. BR4 is the completeness test over the generation result and the reason the officer task names the missing type or the refused template. BR5 is the `MANDATORY` transaction of the library, so the `treatment` row and the `decision_record` row commit together or not at all. BR6 is the reason the four clocks and the type list are read from the rule set and the catalogue with their version. BR7 is the reason the stage outcome carries the request and the parent moves the case. BR8 is the reason the view read is a SELECT of party keys and the reason no personal value enters the request, the event or the log. The review and the signature of a generated document are requested through the P5 and P6 contracts, the set holds only the document reference on the `treatment` row, and no document content is written to `rwb_treatment` (GAP-1704). The wording of MSG-P4-002 and MSG-P7-003 is served from the catalogues of the services that own them, MSG-S2-001 is held in this service's catalogue with a Thai and an English version, and all of them pass DL10 before wave 3 release (GAP-1710).

### 9. State transitions

The case status is rwb-case's and is not changed by this story: the set branch reports an outcome and the parent `CaseWorkflow` moves the case (ASM-4425). The transitions below are the rule set's, and each row is one outcome this story reports.

| From | Event | Condition | To (rule) |
|---|---|---|---|
| TRANSFER_PRICE_SET | PRICE_INSIDE_FLOOR | transfer_price >= floor_price | OFFER_WITH_CUSTOMER_DIL (R-DIL-14) |
| WITH_FCR_OFFICER | OFFER_PREPARED | offer outside the range or deviation_flag = Y | AWAITING_CREDIT_APPROVAL (R-RES-10) |
| AWAITING_CREDIT_APPROVAL | APPROVAL_SLA_BREACHED | approval_age > approval_escalation_limit | AWAITING_CREDIT_APPROVAL (R-RES-13) |

| `treatment.state` | Event | Condition | To |
|---|---|---|---|
| Draft | set composed and complete | the treatment type has a set in the catalogue | Draft, with `outcome` and `outcome_at` written and the decision reference set |
| Draft | set refused or incomplete | X4, X5, X6 | Draft, unchanged |
| Draft | decision record refused or failed | X2, X3 | Draft, unchanged |

The branch moves from running to waiting on each signal and ends when the parent closes the stage. No set state is stored as a lifecycle of its own: the answer is the outcome columns, the set section and the decision record, and the case states above stay the parent's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the set branch, the three activities, the view read and the repository |
| RW-RESTRUCT, restructuring officer (FCR) | Starts the set with the offer, reads the answer and corrects the terms; holds CRUA |
| RW-CASEOWN, case owner | Reads the answer and receives the task of an incomplete set; holds CRU |
| RW-SPECIAL, RW-GUARANT | Read the answer; hold CRU |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-CREDCOMM, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL | Read the answer only |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities, subject to the same checks |
| The case status and the officer task | Not this story: rwb-case owns them and the parent moves and raises (ASM-4425) |
| The transfer price, the floor and the second signature | Not this story: the deed-in-lieu offer stories hold them (RWB-S2-E3012-APP, RWB-S2-E3016-APP) |
| The template catalogue and the Legal approval of a version | Not this story: P6 rwb-comms and P5 rwb-document own them (ASM-4427) |

The rights above are those of TSD S2 T6.1 and the legacy permission table for the capability area "Treatment and offer", and the check itself is the platform guard library's: this story declares the area and the rights C and R and calls the guard, and it owns no check of its own. No delegation of authority level applies, because producing a document set is not a credit decision; the approval that follows the set is R-RES-10's and sits with the credit approval committee. No credential and no personal name appears in the request, the payloads or the logs, which carry case and treatment identifiers, document identifiers, type codes, template codes and versions, statuses and dates only.

### 11. Data

| BR Field ID | Entity or view | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read: the treatment of the set, and the key of the write |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write: the entry id returned by `DecisionRecordWriter.record` |
| DF-TRT-004 | treatment | treatment_type | Read: the type that selects the set |
| DF-TRT-007 | treatment | offer_amount | Read: the amount the documents carry |
| DF-TRT-010 | treatment | valid_until | Read: the offer validity the set dates |
| DF-TRT-013 | treatment | outcome | Write: the set outcome |
| DF-TRT-014 | treatment | outcome_at | Write |
| T3.0 `state`, `version`, `updated_at`, `updated_by` | treatment | standard record columns | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record | the record fields of the library | Write through RWB-PLT-E1027-CON |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | person_key, cif_no, customer_status and the party fields of the view | Read only: the party set the documents must name |
| DF-DOC-001 to DF-DOC-011 | document (rwb_document) | document and document-type rows | Not read and not written: the reference of each generated document arrives on the set answer (ASM-4427) |
| DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016 | rwb-case | case, assignment and task rows | Not read and not written: the parent owns them (ASM-4425) |

`treatment` is the only business table this story writes, in schema `rwb_treatment` and through this service's own login (DP-01). `v_ace_customer` is read with SELECT only under DP-05 and no ACE object is written; the `decision_record` row is a library object of RWB-PLT-E1027-CON written in the caller's transaction. The set itself has no column in `rwb_treatment`: TSD S2 T3.1 carries no document-set, template-version or set-status field, so the set travels in the answer section, in the decision record and, for the rendered reference, in the columns RWB-S2-E2026-APP already holds on the same row (GAP-2684; ASM-4428).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). None of its own. The set answer is served as the optional `documentSet` section of the treatment read `GET /treatments/{treatmentId}`, whose operation entry belongs to RWB-S2-E3001-CON and whose section is declared by RWB-S2-E3018-CON as a compatible addition at major version 1. This story fills that section and publishes no operation entry of its own: the set is composed when the case reaches TRANSFER_PRICE_SET or WITH_FCR_OFFICER and the officer takes no separate action to produce it, so there is no write operation to publish, and the legacy endpoint table of RWB-E3-018 names the treatment create and read only.

The section carries the set status, one element per document with its type, template code, pinned template version, document reference and document version, the completion time, the rule ID and version, and the reason of a refused set — the property names are the working read of the contract story and are not restated here.

#### 12.2 REST operations consumed

None. This is the one place where the split has to be read carefully: the documents are rendered by the `generateContractDocument` activity of RWB-S2-E2026-APP, which owns the one-hop call to the generation operation of RWB-P5-E2026-CON with its 2 s timeout, its breaker and its fake. That call is built and tested under that story, this story consumes only the activity's result inside the same service, and no second call is made from here; the case status arrives on the signal the parent forwards, the party set comes from this service's own view, and the decision record is called in process inside the caller's transaction (DP-03; DP-05; ASM-4425, ASM-4427). This is why the Work Package records no C dependency for this story.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its event `TreatmentApproved` (EV-10) belongs to the approval story of the module. This story writes no outbox row of its own and reports its outcome to the parent as a stage outcome.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | The RESTRUCTURE and DEEDINLIEU package versions in force, so each set outcome is evaluated and recorded with the version it used |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | A deviation raised on the case, so the stage holds while the case clock is paused |

Both events arrive through the inbox of the outbox library, deduplicated by cloud event id, so a redelivery changes nothing. The case status change is not an event of this table: it arrives as the signal the parent forwards (ASM-4425).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (document-set branch) | Workflow, one execution per case per stage, the child of `CaseWorkflow` | `rwb-treatment` in namespace `rwb-recovery` | Input: the case, the route, the treatment type and the treatment reference; signals: the case status forwarded by the parent, the rule package in force and the deviation |
| `composeDocumentSet` | Activity | `rwb-treatment` | The treatment row and the party set of the view in; the set request with the type, the template code and the version in force out |
| `evaluateSetRules` | Activity | `rwb-treatment` | The generation result in; the completeness answer and the outcome of R-DIL-14, R-RES-10 and R-RES-13 with the rule version out |
| `recordAndApply` | Activity | `rwb-treatment` | The `DecisionRecord` and the `treatment` row written in one transaction through RWB-PLT-E1027-CON, and the stage outcome for the parent |

The branch is part of the one `TreatmentWorkflow` the service owns, and the parent-and-child model with the steps of receive, ask, record and apply, wait is the one of the target design. The activity names are a design choice of this story and are fixed by no source document. A workflow class never calls the decision-record library directly: the call is made inside `recordAndApply`, so a replay reuses the recorded decision. The rendering itself is not declared here: it is the `generateContractDocument` activity of RWB-S2-E2026-APP on the same queue (ASM-4427).

#### 12.6 Schedules

None. The branch runs from the signal the parent forwards, and the 14-day offer validity of R-DIL-14, the 3 working-day approval clock of R-RES-10 and the escalation limit of R-RES-13 are durable timers inside the workflow and values in force in the rule set, not Temporal Schedules. The service has no legacy Quartz job in this legacy key.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Written for `decision_log_id`, `outcome`, `outcome_at` and the standard record columns; created by the per-service Flyway sequence and never re-created here |
| `decision_record` | `rwb_treatment` | PLT, library object | Not written directly: the row is written by RWB-PLT-E1027-CON in the caller's transaction (DP-03) |
| `v_ace_customer` | `recovery` (read-only view) | ACE, read through DP-05 | Read only; never written and never owned |

No table of another service is read and no foreign key crosses a schema (DP-01). `document`, `document_type` and `document_hub_parameter` are rwb-document's and P6's and are not read here; the case, the assignment and the task are rwb-case's and are not read here (ASM-4425, ASM-4427). No set, template-version or set-status column is added to `treatment`, because no source gives one (GAP-2684; ASM-4428).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3018-CON set fake | The `documentSet` section, the set request and the error set | A complete deed-in-lieu set of three documents; a complete restructure agreement; a set with one refused template; a set missing a type; a set refused for a named field |
| RWB-PLT-E1027-CON writer fake | The decision record | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; a failed write raising MSG-P7-003 |
| RWB-PLT-N001-CON route fake | The gateway-bff composite route | A composite answer for SCR-15 that joins the treatment read and its set section; a refused route for a role without the right |
| rwb-case case-status mock | The signal the parent forwards, used by AC2 and AC3 | A case at TRANSFER_PRICE_SET and a case at WITH_FCR_OFFICER; a case status the set branch does not accept. Test-only, adds no contract dependency (ASM-4425) |
| Generation result fake (owned by RWB-S2-E2026-APP) | The result of the `generateContractDocument` activity | One document per requested type with its template code and version; a refusal naming a field; a withdrawn template; a refusal beyond 2 s. Referenced, not restated here (ASM-4427) |
| rwb-source-data contract fake | The party set of the case, as the read of `v_ace_customer` | A case with one party; a case with two parties; a case with no party row |

The set fake is the published contract of RWB-S2-E3018-CON; the case-status mock stands in for the signal of the parent and the rwb-source-data contract fake for the party read, which have no published shape of their own here (GAP-2684; ASM-4425, ASM-4426).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 operations of its own | 0 | The set section is served inside the treatment read of RWB-S2-E3001-CON; the generation call is RWB-S2-E2026-APP's |
| Kafka | 0 | 2 events (`rwb.decision.RulePackageInForce.v1`, `rwb.deviation.DeviationRaised.v1`) | Own topic unused by this story; inbox dedupe by cloud event id |
| Temporal | 0 | `TreatmentWorkflow` set branch and 3 activities on `rwb-treatment` | Namespace `rwb-recovery`; stage child of `CaseWorkflow`; no Schedule |
| SQL view | 0 | 1 read-only ACE view | SELECT only under DP-05; party keys and statuses, no personal value in the payload |
| File, Nexus | 0 | 0 | No file and no Nexus operation: the rendered body and the file custody are rwb-document's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `documentset` and `web`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the set: the record and the `treatment` row commit together, and a failed record leaves nothing behind. DP-05 is the read of `v_ace_customer`, taken as this service's own read-only view, which is the form that adds no dependency; the alternative, the contract read of rwb-source-data, would be a C dependency and is not taken here (ASM-4426). DP-13 moves the base of the operations the screens use and nothing else. DP-19 is how SCR-15 and SCR-14 reach this service, one hop through the gateway, so no screen reads a view or a table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` set branch | Workflow | One execution per case per stage; the treatment facts, the package in force, the generation result and the stage outcome |
| `composeDocumentSet` | Activity | The treatment type, the catalogue template code and version in force, and the party set of the view |
| `evaluateSetRules` | Activity | The completeness test of the set and the DEEDINLIEU and RESTRUCTURE outcomes with the rule version |
| `recordAndApply` | Activity | The `DecisionRecord` and the `treatment` row in one transaction through RWB-PLT-E1027-CON |
| `DocumentSetRepository` | Repository | The outcome columns of `treatment` in `rwb_treatment`, with the optimistic lock of `version` |
| `AceCustomerReader` | Repository, read only | The SELECT of the party set against `v_ace_customer` by `case_id` |
| `StageOutcomeReporter` | Signal reporter | The outcome the parent `CaseWorkflow` uses to move the case and raise the officer task; it reports, it never changes a case row |

**Database.** `treatment` holds the columns of DF-TRT-003, DF-TRT-013 and DF-TRT-014 and the standard record columns of T3.0, with the optimistic lock on `version`. No new table and no new column: the set status, the template versions and the document references have no field in the source, and the rendered reference is the column RWB-S2-E2026-APP already holds on the same row (GAP-2684; ASM-4427, ASM-4428). `decision_record` is the library object applied by the per-service Flyway sequence, written only through the library.

**Configuration and reference data.** The capability area "Treatment and offer" and the rights C and R are access rows of rwb-access, read through its guard. The four document types, the template codes and the approved template versions are the catalogue's values in force, read at their version by the rendering activity and checked here against the same value; the offer validity, the approval clock and the escalation limit are values in force in the rule set (BR-S2-018). They are read under the reference-data contract (DP-06, DP-07); their parameter keys are Not specified in the source documents (DOR-RWB-S2-E3018-APP-20). The grant on `v_ace_customer` is a DB story's, not this one's: this story reads it under the login it is given (DP-05; ASM-4426).

**Build steps**

1. The set branch of `TreatmentWorkflow` and its input record, registered on `rwb-treatment` as the stage child of `CaseWorkflow`, with the case signal and the treatment facts (AC2, AC3).
2. `composeDocumentSet` against the catalogue value and the set contract, with the four document types and the template version in force (AC1, AC2).
3. `AceCustomerReader` and the party set of the request, against the view fixture, read only (AC1).
4. The hand-off to the `generateContractDocument` activity of RWB-S2-E2026-APP and the receipt of its result, with the refusal and timeout path (AC1, X4).
5. `evaluateSetRules` with the completeness test and the R-DIL-14, R-RES-10 and R-RES-13 outcomes (AC2, AC3).
6. `recordAndApply` with the `DecisionRecord`, the `MANDATORY` transaction and the `treatment` row, plus the failed-write path (AC4).
7. The set section of the answer with the guard check and the error mapping of section 12.1 (AC1).
8. `StageOutcomeReporter` and the parent signal, with the two rule outcomes of AC2 and AC3 and the officer task of an incomplete set.
9. Tests for AC1 to AC4 against the fakes and the view fixture, plus the two component cases of section 16.

**Feature flag.** `rwb.treatment.document-set`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT, a deed-in-lieu case inside the floor gets its three documents with the pinned versions, a restructure offer outside the range routes to credit approval with its agreement, a refused template leaves the treatment unchanged and raises the officer task, a repeated signal returns the same set from the recorded decision, the decision record and the `treatment` row commit or roll back together, and SCR-15 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, or the set is missing a type the treatment requires | Enter {field}. |
| MSG-S2-001 | The offer is below the floor of {floor} and has been sent for approval | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | The offer reaches its validity end | The offer to the customer ends on {date}. |
| MSG-S2-002 | The payoff figure is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-P4-002 | The role does not hold the right on the capability area | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. |

The seven texts are the legacy texts carried unchanged and no message identifier is added or renamed. MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the three offer messages of the same module and are raised by RWB-S2-E3002-APP and RWB-S2-E3003-APP; they are kept here because the legacy validation table of RWB-E3-018 carries them, and the set raises none of them. MSG-P4-002 is the access answer of the guard library, and MSG-P7-003 and MSG-P7-009 are raised by RWB-PLT-E1027-CON and shown here. The message shown when a template is withdrawn or a type has no template has no text in any source and is Not specified in the source documents (GAP-2684; ASM-4428). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-15 Settlement offer (Draft; below floor; approved; sent; accepted; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8812)) and SCR-14 Treatment record (Draft; submitted; approved; booked; broken; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8811)) are the two legacy screens of this story and keep their legacy state lists, with the missing states marked as not specified. SCR-15 is where the officer reads the set that the offer will carry: the type, the template code, the pinned template version, the document reference, the set status and the rule version; SCR-14 is where the set of the treatment is read beside its terms and its booking. Both screens reach the service through the gateway-bff composite route, one hop each (DP-19); the screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-018-01 | AC1 | End to end | Generate the treatment document set |
| TC-E3-018-02 | AC2 | End to end | Rule R-DIL-14 |
| TC-E3-018-03 | AC3 | End to end | Rule R-RES-10 |
| TC-E3-018-04 | AC4 | End to end | Not recorded |
| TC-E3-018-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-018-06 | Principle 5 | Component | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E3-018-07 | Section 12 contract | Component | The operations, events and activities of section 12 match the shapes published in RWB-S2-E3018-CON and the activities of section 12.5 |
| TC-E3-018-08 | Section 12.7 boundary (ASM-3438) | Component | Only the `treatment` row of `rwb_treatment` is written; `v_ace_customer` is read with SELECT only and no table of another service is read (DP-01) |
| TC-E3-018-09 | AC5 | Component | Not specified in the source documents (NEWAC-RWB-S2-E3018-APP-AC5) |
| TC-E3-018-10 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-S2-E3018-APP-AC6) |
| TC-E3-018-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S2-E3018-APP-AC7) |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" and "Principle 5" map to "Component", as in the other stories of this run. The set fake, the decision-record writer fake, the route fake, the generation result fake and the rwb-source-data contract fake of section 12.8 stand behind every case, and the case-status mock supplies the two statuses of AC2 and AC3. The full test, with its Given, When and Then, is in the legacy test document under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the four document types, the template codes and versions, the offer validity, the approval clock and the escalation limit are values in force, read with their version (BR-S2-018).
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry case and treatment identifiers, document identifiers, type codes, template codes and versions, statuses and dates only, and the test data is synthetic.
- No personal value in the set request or the set answer: the party set is read as keys and a count, and the merged values on a document body are the rendering engine's (ASM-4426, ASM-4427).
- No read of another service's table and no write to an ACE object: the party set comes from the one read-only view and the case rows are never touched (DP-01; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only through the view, with SELECT granted to this service's login.
- No set, template-version or set-status column in `rwb_treatment`; a schema change that adds one fails the guardrail test (GAP-2684; ASM-4428).
- No event of this story and no outbox row: the outcome is reported to the parent, so a replay of the stage produces no second message.
- The decision record and the `treatment` row commit in one transaction through the `MANDATORY` rule of the library; an action that commits without its record is a build failure, not a defect (DP-03).
- An applied migration is never edited: any correction to the `treatment` table is a new version on the service sequence.
- No screen calls a service directly and no screen reads a view: SCR-15 and SCR-14 go through the gateway-bff composite route (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-006 | The credit application, contract and mortgage documents for a deed in lieu are generated from templates | Program 5.9 | FEAT-TRT-18 | 07 Route, settle and claim | R-DIL-14; BR1, BR3, BR4 | TC-E3-018-01, TC-E3-018-02 |
| REQ-S2-006 | The same set carries the restructure agreement through the approval route and its escalation | Program 5.9 | FEAT-TRT-18 | 07 Route, settle and claim | R-RES-10, R-RES-13 | TC-E3-018-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3018-CON | Contract | H: declares the set section, the set request, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record writer called in the caller's transaction with the `MANDATORY` rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that SCR-14 and SCR-15 use |
| RWB-S2-E2026-APP | App development | Sibling: owns the `generateContractDocument` activity and the one-hop call to RWB-P5-E2026-CON; no build dependency is recorded (ASM-4427) |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON | App development, Contract | Sibling: the treatment record and the treatment read whose answer carries the set section |
| RWB-S2-E3012-APP, RWB-S2-E3016-APP | App development | Sibling: the deed-in-lieu offer, its transfer price, its floor and its second signature, which precede this set |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP | App development | Sibling: the settlement offer and the approval below the floor, which raise the three offer messages |
| P5 rwb-document, P6 rwb-comms | Service, wave 1 | Own the rendering engine, the document rows, the template catalogue and the Legal approval of a version (ASM-4427) |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status, its tasks and its timers; the stage reports and never moves or raises (ASM-4425) |
| rwb-decision (P7) | Service, wave 1 | Owns the rule packages and the central ledger; the local record is written through RWB-PLT-E1027-CON (DP-03) |
| rwb-deviation (S8) | Service, wave 2 | Owns `rwb.deviation.DeviationRaised.v1`, consumed here so the stage holds while the case clock is paused |
| Wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners, with the `-ITG` copies of the six test cases |

### 19. Out of scope

- The published shape of the set section, the set request, the error set and the fakes: RWB-S2-E3018-CON.
- The rendering engine, the template selector, the merge-field resolver, the rendered body, the PDF, the file custody, the retention and the e-signature: RWB-S2-E2026-APP, RWB-P5-E2026-APP and RWB-P5-E2018-APP.
- The template catalogue, the merge-field definitions and the Legal approval of a template version: P6 rwb-comms and P5 rwb-document (ASM-4427).
- The offer, its terms, the transfer price, the floor, the second signature and the validity timer: RWB-S2-E3012-APP, RWB-S2-E3016-APP and RWB-S2-E3002-APP to RWB-S2-E3005-APP.
- The treatment record, the treatment read and the treatment resource body: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The case, its CMMN status, the parent `CaseWorkflow`, the case signal, the task and its clock: rwb-case (P3), so no case table is read or written here (ASM-4425).
- The ACE views themselves, their grant and their ingestion: P1 rwb-source-data, P2 rwb-integration and the ACE DB stories; this story reads what the view carries (ASM-4426).
- The decision-record library, its chain, its envelope and the central ledger of P7: RWB-PLT-E1027-CON, RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The RESTRUCTURE and DEEDINLIEU rule packages, their authoring, their approval and their promotion: P7 rwb-decision, with the embedded runtime as a service-template capability (ASM-4429).
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-15: RWB-PLT-N001-CON and the screen owners (DP-19).
- The deployment, the flag switch and the runbook: the platform DevOps stories of wave 2; the real cross-service proof: the wave 2 integration harness.
