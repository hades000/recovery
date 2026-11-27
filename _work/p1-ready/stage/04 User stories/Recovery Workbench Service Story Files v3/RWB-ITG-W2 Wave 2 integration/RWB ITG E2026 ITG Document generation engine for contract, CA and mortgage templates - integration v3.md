# RWB-ITG-E2026-ITG Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2026-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Size | Set by the squad at refinement |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-P4-E1037-CON, RWB-P5-E2026-CON |
| Contract dependencies | RWB-P4-E1037-CON (authorise schema); RWB-P5-E2026-CON (generation stub); H RWB-PLT-E1027-CON; H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON; H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1044-CON; H RWB-PLT-N001-CON |
| Integration dependencies | RWB-P6-E1046-APP, RWB-P6-E1034-APP, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-S2-E2026-APP, RWB-P4-E2026-APP, RWB-P7-E2026-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-026 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 18 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; finishing pass.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service harness that generates a contract, a credit approval and a mortgage document from Legal-approved template versions and case facts, and proves the rendered file, the template version and the decision record agree across the five owning services**, so that **the deed in lieu and restructure document set is proven end to end, with evidence and a pass or fail gate, before the wave 2 release is accepted**.

This is an integration harness story. It builds no production endpoint, no screen, no table and no migration. It runs the real cross-service journey across rwb-document (P5, which generates and stores the document), rwb-comms (P6, which owns the template catalog and the merge fields), rwb-treatment (S2, which owns the treatment and its decision log reference), rwb-access (P4, which answers the session and scope question) and rwb-decision (P7, which holds the decision ledger and the shared topic). Until each I story of the metadata list lands, its contract fake stands in; the harness keeps a seed pack, an evidence pack and a pass or fail gate, and its only output is the run report.

### 2. Business rationale

RWB-E2-026 splits into seven app stories and this integration story. The app stories build the generation operation, the template and merge field catalog, the version rules, the treatment checks, the decision record and the access question inside their own services. No single app story can prove the thing the business signs off on: a rendered, Legal-approved set whose decision record, template version and merge snapshot all agree, across five services, for one case and one business date. That proof is this story.

Deed in lieu and restructure documents are typed today from the case file into word processor templates, and a wrong amount or an old template wording reaches the customer. The target engine fills each Legal-approved version from the case facts, refuses to produce a document with a missing value or an unapproved version, and records which version and which inputs produced each document (REQ-DCM-012). The version itself carries the Legal approval record (REQ-OCC-002), and control CTL-14 applies to the deed in lieu and restructure set. The harness is where those two requirements meet: one run proves the set is generated, formatted, versioned and recorded, so a broken boundary is found in SIT and not by a customer holding a contract with the wrong transfer price.

The architecture changes the path, not the business. The monolith wrote the document, the decision and the input snapshot in one module. In the target, rwb-document owns the document metadata, the merge snapshot and the file, in its own schema `rwb_document` with its own Flyway sequence (DP-01, DP-15); the template catalog and the merge field catalog belong to rwb-comms (DP-06, DP-07 for the parameter and reference values it needs); the case and treatment facts come through the owner's contract, and the ACE case, party and collateral facts come through rwb-source-data, never from an ACE view of the caller's own (DP-05); every service writes its decision record to the local decision-record library and publishes on the shared topic `rwb.decision-record.v1` (DP-03); the document events leave through the outbox (DP-09); every call is one hop inside 2 s (DP-11); and the journey runs through the gateway route the real screens use (DP-19). The harness exercises exactly those boundaries together, with the contract fakes of section 12.8 in front of them until the real services land.

The measure is the journey evidence: for each owned criterion, one pass or fail with the request, the response, the document metadata, the rendered file values, the template code and version, the merge snapshot reference and the decision record, captured in one report keyed by story key and business date.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available, with the gateway route for `/api/recovery/*`, the Kafka topics of rwb-document, rwb-comms, rwb-treatment, rwb-decision and rwb-access, the shared topic `rwb.decision-record.v1`, and the object storage container the drafts are written to. The harness environment, its seed pack and its evidence format: Not specified in the source documents (GAP-0408; ASM-0583).
- The seven integration dependencies have published their contracts, or their contract fakes of section 12.8 stand in for them: RWB-P6-E1046-APP (template and merge field catalog), RWB-P6-E1034-APP (template versions with the Legal approval record), RWB-P5-E2026-APP (generation), RWB-P6-E2026-APP (template catalog read), RWB-S2-E2026-APP (treatment), RWB-P4-E2026-APP (session and scope) and RWB-P7-E2026-APP (decision log).
- The case "RW-2026-000301" with product group "MORTGAGE" is seeded, and treatment "TRT-0301" of type "DEED_IN_LIEU" on that case has decision_log_id set (approved at D6.4) and no outcome yet (legacy section 7 Background).
- Template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" is seeded with approved_by_legal true, and its merge fields are case_no, borrower_name, title_doc_no, transfer_price and contract_date.
- The case facts of the Background are seeded: transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10.
- Templates "DIL-CA", "DIL-MORTGAGE" and "RES-AGREEMENT" are seeded with the template-to-document-type mapping of legacy section 3: DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL, DIL-MORTGAGE to MORTGAGE_DOCUMENT and RES-AGREEMENT to CONTRACT.
- The parameter rows GEN_IDEMPOTENCY_HOURS 24, GEN_MAX_TEMPLATES 10 and GEN_FONT "TH Sarabun New" are loaded as data through the parameters contract, never in the harness code (legacy section 13).
- The caller holds Documents C: a test user of role RW-RESTRUCT or RW-CASEOWN with the case in scope, and the service identity SY-CASEWF where a scenario names it.
- Synthetic values only: no real customer record, no real national ID number and no real template body enters the harness, its fakes or its evidence (legacy section 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the seven contracts it is about to exercise.
2. Harness: seeds the case, the treatment, the four templates with their versions and Legal approval state, the case facts and, per scenario, the deviation of the template or treatment state the scenario names.
3. Harness: calls the P4 session operation `GET /api/recovery/access/v1/me/session` for the test user and records the role, the scope and the Documents right it will exercise.
4. Harness: calls the P7 treatment operation `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and records type, decision_log_id and outcome.
5. Harness: reads the template through the P6 admin template operation and records template code, version, language, product group and approved_by_legal.
6. Harness: calls `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` with the treatment, the template codes and the language, and the header Idempotency-Key "K-0301"; records the status and the body.
7. Harness: reads the generated documents through `GET /api/recovery/document/v1/cases/{caseId}/documents` and records type, source, state, write_once, template code, template version and treatment ID.
8. Harness: opens the rendered file of each document through `GET /api/recovery/document/v1/documents/{documentId}` and asserts the formatted values: the amount with two decimals and in Thai words, and the Thai long date in Buddhist Era.
9. Harness: reads the template code and version carried on the document row and compares them with the version that was current, approved and valid on the request date (AC3).
10. Harness: reads the decision log through `GET /api/recovery/decision/v1/decision-log` and records the decision code "D6.4", the inputs reference to the merge snapshot and, for a set, the three template codes and versions.
11. Harness: subscribes to `rwb.document.events.v1` and `rwb.decision-record.v1` for the run window and records the `DocumentStored` event per document and the `DecisionRecorded` event of the case.
12. Harness: asserts the draft container holds the file of each stored document and holds no file of a refused document, writes the per-scenario evidence to one run report keyed by story key and business date, evaluates the gate, releases the run lock and restores the seeded data.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A required merge field has no value | 422; nothing stored; no file; no decision record; the field and template are named in the answer | MSG-P5-009 | AC2, TC-E2-026-02-ITG |
| X2 | The current template version is not approved by Legal | 422; nothing of the set stored; the template code is named | MSG-P5-010 | AC5, TC-E2-026-04-ITG, TC-E2-026-14-ITG |
| X3 | The template is withdrawn with no approved successor | 422; generation held; a task to the restructuring officer is recorded by the owner | MSG-P6-003 | AC9, TC-E2-026-05-ITG |
| X4 | The treatment is not approved, is closed or is of another type | 409; nothing stored | MSG-P5-011 | AC6, TC-E2-026-06-ITG |
| X5 | The decision log write fails | 503; no document row; the draft file is removed; no decision event; an incident | MSG-P7-003 | AC7, TC-E2-026-07-ITG |
| X6 | The same request is repeated with the same Idempotency-Key | 201 with the first result; no second document and no second decision record | None | AC8, TC-E2-026-08-ITG |
| X7 | Two requests for the same treatment and template run at once | One succeeds with 201; the other gets 409 | MSG-GEN-004 | AC10, TC-E2-026-09-ITG |
| X8 | A template body cannot be rendered | 503; nothing stored; an incident; the draft file removed | MSG-GEN-006 | AC11, TC-E2-026-10-ITG |
| X9 | No template exists for the product group or language | 422; the template and the product group are named | MSG-P5-010 | AC12, TC-E2-026-11-ITG |
| X10 | One template of a set fails its check | Nothing of the set is stored; no decision record | MSG-P5-010 | AC5, TC-E2-026-14-ITG |
| X11 | The case is outside the caller's scope | 404 | MSG-P4-003 | AC13, TC-E2-026-12-ITG |
| X12 | The caller lacks Documents C | 403 | MSG-P4-002 | AC14, TC-E2-026-15-ITG |
| X13 | The seed pack cannot be loaded, or a seeded template is not approved or a treatment has no decision_log_id where the scenario needs one | The run refuses to start and names the missing seed item; no scenario is reported | None | AC15, TC-E2-026-17-ITG |
| X14 | Another run holds the environment lock | The run refuses to start | None | AC16, TC-E2-026-18-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the seven published contracts or their fakes; it builds no service feature and has no build dependency, so it starts on Day 1 |
| Negotiable | Scenarios, seeded values, template codes, merge field names and formats are data files, never code |
| Valuable | The generation journey is proven once across five services, with the decision record and the template version agreeing, before the app stories claim Done |
| Estimable | One journey runner, one fake registry, one seed pack, one set of assertions, one evidence collector, one gate |
| Small | Fits in one sprint with its assertions and its fake sets |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded result per business date |

### 7. Acceptance criteria

No legacy acceptance criterion is owned by this story. The seventeen criteria below are new and test only the integration deliverable.

```gherkin
Feature: Document generation engine for contract, CA and mortgage templates

  Background:
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the merge fields of "DIL-CONTRACT" version 2 are case_no, borrower_name, title_doc_no, transfer_price and contract_date
    Given a restructuring officer with role RW-RESTRUCT in scope of the case

  Scenario: AC1 One CONTRACT generated across five boundaries (new, D-RCV-60)
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    When the harness calls POST /api/recovery/document/v1/cases/RW-2026-000301/generated-documents with treatment "TRT-0301", template "DIL-CONTRACT" and Idempotency-Key "K-0301"
    Then the response is 201 with one document of document_type "CONTRACT", source "GENERATED", state "DRAFT" and write_once false
    Then the document carries template_code "DIL-CONTRACT", template_version 2 and treatment_id "TRT-0301"
    Then the rendered file shows "1,250,000.00 baht (one million two hundred fifty thousand baht)" and "10 December 2569 BE"
    Then one decision record exists with decision code "D6.4" and an inputs reference to the merge snapshot
    Then one DocumentStored event for the document is on rwb.document.events.v1 inside the run window

  Scenario: AC2 A missing merge field refuses the document (new, D-RCV-60)
    Given the case has no title_doc_no
    When the harness calls generated-documents for template "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no"
    Then no document row exists, no file is in the draft container and no decision record exists

  Scenario: AC3 A new template version leaves the earlier document on its version (new, D-RCV-60)
    Given template "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15
    Given document "DOC-0310" was generated on 2026-12-10 from version 2
    When the harness generates on 2026-12-15
    Then the new document carries template_version 3
    Then "DOC-0310" keeps template_version 2 and its rendered file still opens
    Then template version 2 stays readable in the template catalog

  Scenario: AC4 A set of three documents in one request (new, D-RCV-60)
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    When the harness requests the three template codes for treatment "TRT-0301"
    Then three documents are stored with types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"
    Then one decision record names the three template codes and their versions

  Scenario: AC5 A set is stored whole or not at all (new, D-RCV-60)
    Given templates "DIL-CONTRACT" and "DIL-MORTGAGE" are current and approved
    Given template "DIL-CA" has no version approved by Legal
    When the harness requests the three template codes for treatment "TRT-0301"
    Then the response is 422 with MSG-P5-010 naming "DIL-CA"
    Then none of the three documents is stored, no file is in the draft container and no decision record is written

  Scenario: AC6 A treatment that is not approved is refused (new, D-RCV-60)
    Given treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id
    When the harness requests generation for treatment "TRT-0302"
    Then the response is 409 with MSG-P5-011
    Then nothing is stored

  Scenario: AC7 The decision log is unavailable (new, D-RCV-60)
    Given the decision log store does not accept writes
    When the harness generates for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 503 with MSG-P7-003
    Then no document row exists for "TRT-0301" and the draft file is removed from the container
    Then no decision event for the case is on rwb.decision-record.v1 and the run records an incident as in R-UNI-39

  Scenario: AC8 A repeated request returns the first result (new, D-RCV-60)
    Given a request with Idempotency-Key "K-0301" generated document "DOC-0311"
    When the same request with Idempotency-Key "K-0301" arrives again
    Then the response is 201 with document "DOC-0311"
    Then no second document and no second decision record exist

  Scenario: AC9 A withdrawn template with no approved successor holds generation (new, D-RCV-60)
    Given template "DIL-MORTGAGE" is withdrawn and has no approved successor
    When the harness calls generated-documents for treatment "TRT-0301" and template "DIL-MORTGAGE"
    Then the response is 422 with MSG-P6-003
    Then generation is held and a task to the restructuring officer is recorded by the owner

  Scenario: AC10 Two parallel requests for one treatment and template (new, D-RCV-60)
    When the harness sends two requests for treatment "TRT-0301" and template "DIL-CONTRACT" at the same time
    Then one request gets 201 and the other gets 409 with MSG-GEN-004

  Scenario: AC11 A template body that cannot be rendered is refused (new, D-RCV-60)
    Given the body of template "DIL-CONTRACT" version 2 cannot be rendered
    When the harness calls generated-documents for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 503 with MSG-GEN-006
    Then nothing is stored, the draft file is removed and an incident is recorded

  Scenario: AC12 No template exists for the product group or language (new, D-RCV-60)
    Given a hire purchase case with no template for its product group or language
    When the harness calls generated-documents for the case and template "DIL-MORTGAGE"
    Then the response is 422 with MSG-P5-010 naming the template and the product group

  Scenario: AC13 A case outside the caller's scope is not found (new, D-RCV-60)
    Given the case "RW-2026-000301" is outside the scope of the caller
    When the caller calls generated-documents for treatment "TRT-0301"
    Then the response is 404 with MSG-P4-003

  Scenario: AC14 A caller without Documents C is refused (new, D-RCV-60)
    Given a user with role RW-TEAMMGR who holds Documents R only
    When the user calls generated-documents for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 403 with MSG-P4-002

  Scenario: AC15 A seed pack that cannot be loaded stops the run (new, D-RCV-60)
    Given the seed pack cannot be loaded, or a seeded template is not approved, or a treatment has no decision_log_id where the scenario needs one
    When the harness starts the run
    Then the run refuses to start and names the missing seed item
    Then no scenario is reported

  Scenario: AC16 A run is refused while another run holds the lock (new, D-RCV-60)
    Given another run holds the environment lock
    When the harness starts the run
    Then the run refuses to start

  Scenario: AC17 The national ID number is filled at render time (new, D-RCV-60)
    Given the template requires the borrower national ID number
    When the harness generates the document for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the national ID number is filled from the token service at render time
    Then the clear value exists only inside the stored PDF
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is generated only from the current template version: approved by Legal, active and valid on the request date; the most specific product group match wins over a template for all products | DF-REF-047, DF-REF-049, DF-REF-051; CTL-14; R-LIT-03 |
| BR2 | A withdrawn template with no approved successor holds generation and raises a task | R-LIT-04; R-LIT-06 |
| BR3 | Every required merge field must have a value; otherwise nothing is generated and the field is named | Merge field catalog (P6 rwb-comms, RWB-P6-E1046-CON); FEAT-OCC-07 |
| BR4 | Values are formatted by the catalog format: Thai long date in Buddhist Era, amounts with two decimals and in Thai words | Merge field catalog (P6 rwb-comms, RWB-P6-E1046-CON); Principle 1 |
| BR5 | Generation is allowed only for an approved, open treatment of type DEED_IN_LIEU or RESTRUCTURE | DF-TRT-003, DF-TRT-004, DF-TRT-013; R-DIL-14; R-DIL-16 |
| BR6 | A generated document carries the template code and version, the treatment and the source GENERATED; it is a DRAFT and not write-once until it is sent (RWB-E2-017) | DF-DOC-005, DF-DOC-010; CTL-12 |
| BR7 | Generation that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | A set is generated whole or not at all | Events rule "Transactions" |
| BR9 | A repeat with the same Idempotency-Key returns the first result | R-UNI-40 |
| BR10 | A new template version applies to documents generated from its valid-from date; earlier documents keep their version | R-UNI-38 |
| BR11 | A national ID number is filled from the token service at render time; the clear value exists only inside the stored PDF | DF-PTY-007; CTL-11; DL26 |

The rules are unchanged by the split. The harness asserts them across the five service boundaries and restates none of them in code; each rule stays owned by RWB-P5-E2026-APP or RWB-P6-E2026-APP.

Open decisions: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355) are still open; each assumption stands until its decision closes.

### 9. State transitions

None. This story changes no case status. The only business state it observes is the created document in state DRAFT.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Generation requested | BR1, BR3 and BR5 pass and the decision record is written | document state DRAFT |

The harness adds a run state of its own only: Not started, Running, Passed, Failed. The latest run for a build decides the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | The generation caller of the journey; holds Documents C on a case in scope |
| RW-CASEOWN, case owner | The second generation caller of the journey; holds Documents C on a case in scope |
| SY-CASEWF, case workflow module | Supplies the service identity the harness uses for the rule-driven caller path; the same P5 operation answers it |
| SY-DECLOG, decision log writer | Supplies the decision record the harness asserts, through rwb-decision's contract only |
| RW-LEGAL, legal counsel | Owns the approved_by_legal state of each template version the harness seeds; the approval itself is a precondition of RWB-E1-034 and not part of this story |
| RW-TEAMMGR, team manager | Reads generated documents (Documents R); the harness asserts that this role cannot generate |
| Integration lead | Agrees the fake set, the contract versions and the boundary assertions with the service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision; the treatment was approved at D6.4 before generation |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-004 | recovery_case | id, case_no, product_group, primary_person_key | Read through the P3 case operation |
| DF-TRT-001 | treatment | id | Read through the S2 treatment operation |
| DF-TRT-003 | treatment | decision_log_id | Read through the S2 treatment operation |
| DF-TRT-004 | treatment | treatment_type | Read through the S2 treatment operation |
| DF-TRT-007 | treatment | offer_amount | Read through the S2 treatment operation |
| DF-TRT-013 | treatment | outcome | Read through the S2 treatment operation |
| DF-ACE-057, DF-ACE-058 | v_ace_customer | first_name, last_name | Read through the P1 source-data contract by rwb-document; asserted in the merge snapshot |
| DF-ACE-197 | v_ace_collateral_detail | title_doc_no | Read through the P1 source-data contract by rwb-document; asserted in the merge snapshot |
| DF-REF-045 to DF-REF-051 | template | all fields | Read through the P6 admin template operation |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Read through the P5 document operations; written by rwb-document, never by the harness |
| DF-DOC-032 | document | template_id | Read through the P5 document operations |
| DF-DOC-033 | document | treatment_id | Read through the P5 document operations |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation |

The harness owns no table and no schema (DP-01, DP-15); it reads only through the operations of section 12.2, and its evidence holds identifiers, statuses and timestamps only, never personal data. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | The generation request under test (AC1 to AC8), with the Idempotency-Key header |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The generated documents and their type, source, state, template code and version (AC1, AC3, AC4, AC5) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The document metadata, the merge snapshot reference and the rendered file the harness opens (AC1, AC2, AC3, AC7) |
| GET | `/api/recovery/comms/v1/admin/templates` | P6 rwb-comms | The template code, version, language, product group and approved_by_legal state the journey starts from (AC1, AC3, AC4, AC5) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Treatment type, decision_log_id and outcome (AC1, AC6) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision record with decision code "D6.4", the inputs reference and, for a set, the three codes and versions (AC1, AC4, AC5, AC7, AC8) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, the scope and the Documents right the generation runs under (TC-E2-026-15-ITG) |

Every POST carries an Idempotency-Key kept for the parameter row GEN_IDEMPOTENCY_HOURS of 24 (BR9). The merge field values themselves are resolved inside rwb-document through the providers owned by rwb-case, rwb-treatment and rwb-source-data; the harness never calls those providers and asserts the values only through the merge snapshot and the rendered file.

#### 12.3 Events published

None. The harness publishes no Kafka event; the evidence goes to the release record through its pipeline integration.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | One event per stored document, inside the run window (AC1, AC4), and no event for a refused document (AC2, AC5, AC7) |
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | Confirms the seeded treatment the generation runs on reached its approved state (AC1, AC6) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); every service publishes its own record | Asserts that the record of the generation reached the shared topic inside the run window, alongside the ledger read of section 12.2 (AC1, AC4, AC7) |

The harness subscribes with its own consumer group and asserts the events, never the producer's table.

#### 12.5 Workflows and activities

Observed only. JOB-12 Document intake is the workflow `DocumentIntakeWorkflow` on queue `rwb-document`, and its `generate` and `seal` activities are the ones that render and store the file the harness opens (Architecture v5 slide 16; job map slide 44). JOB-11 Outbox sender is observed on its every-minute window for the `DocumentStored` and `DecisionRecorded` events.

The harness starts no workflow, adds no activity and writes no schedule. Both jobs are owner-built by P5 and by the platform outbox library.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None. The harness owns no table in any schema. rwb-document writes `rwb_document` through its own Flyway sequence (DP-01, DP-15); the harness reads the result through the operations of section 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-document | generated-documents, cases/{caseId}/documents, documents/{documentId} | OpenAPI of P5 | 201 with the generated document set, 422 with MSG-P5-009, MSG-P5-010 or MSG-GEN-001, 409 with MSG-P5-011 or MSG-GEN-004, 503 with MSG-P7-003 or MSG-GEN-006, per scenario; keeps the request journal for the idempotency and counter assertions |
| WireMock rwb-comms | admin/templates | OpenAPI of P6 | DIL-CONTRACT version 2 in Thai for MORTGAGE with approved_by_legal true; DIL-CONTRACT version 3 valid from 2026-12-15; DIL-CA with version 1 not approved; DIL-MORTGAGE withdrawn; the HIRE_PURCHASE refusal |
| WireMock rwb-treatment | treatments/{treatmentId} | OpenAPI of S2 | TRT-0301 of type DEED_IN_LIEU with decision_log_id set and no outcome; TRT-0302 with no decision_log_id |
| WireMock rwb-access | me/session | OpenAPI of P4 | RW-RESTRUCT and RW-CASEOWN in scope with Documents C; RW-TEAMMGR with Documents R refused with MSG-P4-002; the out-of-scope case with MSG-P4-003 |
| WireMock rwb-decision | decision-log | OpenAPI of P7 | The decision record with decision code "D6.4", the inputs reference and the three codes and versions; 503 for AC7 |
| Renderer shares of the P5 contract | The `generate` and `seal` activities of `DocumentIntakeWorkflow` | The P5 activity contract | A PDF/A-2b file with the Thai fonts embedded, and a damaged body for the render failure case |

The PDF/A-2b conformance check and the embedded Thai font check are harness assertions, not new business rules. The draft document path is `{container}/{caseId}/{documentId}/v1`, as in RWB-P5-E1024-APP. The font parameter GEN_FONT is "TH Sarabun New" (assumed). The seed pack and the evidence format: Not specified in the source documents (GAP-0408; ASM-0583).

Each fake is replaced by the real service as its I story lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop on the owner's base with the 2 s timeout of DP-11 |
| Kafka | 3 events consumed on three topics; none published |
| Temporal | Observed only: JOB-12 `DocumentIntakeWorkflow` on queue `rwb-document` and JOB-11 outbox relay; no workflow, activity or schedule added |
| File | The rendered file of each document is opened and asserted against the draft container; the harness writes no file of its own outside its evidence pack |

### 13. Solution plan

**Package.** Folder `integration/recovery-document-generation` in the ACE repository, package `<ACE base package>.recovery.integration.documentgeneration`. Not part of any deployed service and not in any service schema.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness owns no table and reads no schema; every document, template, treatment and decision fact comes from an operation of section 12.2 |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The generation record is read through rwb-decision and the `DecisionRecorded` event is read on the shared topic; the harness writes no ledger entry |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | Party and collateral facts reach the file through rwb-source-data and rwb-document; the harness asserts them in the merge snapshot and the rendered file only |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | GEN_IDEMPOTENCY_HOURS, GEN_MAX_TEMPLATES and GEN_FONT are seeded parameter rows read through the contract, never values in the harness code |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The document types and the template-to-document-type mapping are seeded reference data, asserted through the operation that returns them |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group to the three topics and asserts the events, never the outbox table |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | Each of the seven consumed operations is called once from the harness with a 2 s timeout and a breaker, and the generation POST carries the Idempotency-Key |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The harness runs no migration; it reads the document columns the P5 Flyway sequence added through the operation, and fails the run on any direct schema read in the trace |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the real screens use, on the same owner bases, so the route is exercised and not bypassed |

The platform H dependencies in the table are delivered by the platform wave and are not repeated in the metadata; the harness converges on them and has no build dependency of its own. The blocking dependencies are the seven I stories, which replace the fakes one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date, and stops at the first failed assertion with the trace |
| FakeRegistry | Configuration | WireMock mapping sets for the five services and the renderer shares, one set per contract version |
| TemplateFixturePack | Data | Templates, versions, Legal approval state, merge field lists, document types and the type mapping per scenario, as data files |
| MergeSnapshotAssertion | Assertion | Compares the merge snapshot reference with the case facts and the values that reached the file |
| PdfAssertion | Assertion | Opens the rendered file and compares the formatted amount, the Thai words, the Buddhist Era date and the PDF/A-2b and font conformance |
| DecisionAssertion | Assertion | Reads the decision log and the shared topic and compares decision code "D6.4", the inputs reference and the template codes and versions |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with request, response, document metadata, file values, snapshot reference and decision record |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached to the wave 2 release record |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, synthetic case "RW-2026-000301" and synthetic treatment "TRT-0301" with the seeded templates and case facts of section 3. No production record is copied, and no real national ID number is seeded (BR11). The draft container path is `{container}/{caseId}/{documentId}/v1`. The harness environment, its seed pack and its evidence format: Not specified in the source documents (GAP-0408; ASM-0583). Each run starts from the seeded state, so a repeated run is deterministic and produces the same report.

**Build steps**

1. Write the TemplateFixturePack and the SeedPack from the Background and the eight scenarios, with the template codes, versions, approval states, merge fields, document types and parameter rows as data; test that a bad seed stops the run (X13).
2. Write FakeRegistry with the five WireMock sets and the renderer shares, published from the same OpenAPI documents the services publish.
3. Write JourneyRunner for AC1 and assert the document metadata, the merge snapshot, the rendered values and the decision record across the five boundaries.
4. Add the refusal paths AC2, AC5 and AC6 with the counter assertions: no document row, no file and no decision record on a refusal.
5. Add AC3 with the two versions and the document generated before the valid-from date, and assert that the earlier file still opens.
6. Add AC4 with the three-template set, then AC7 with the decision log unavailable and the draft file removed.
7. Add AC8 with the repeated key and the request journal, then X8, X9 and the access and scope failures through the fakes.
8. Write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record, and rerun the eight scenarios on the release build.

**Feature switch.** The production switch the journey exercises is `rwb.dochub.generation-engine`, owned by RWB-P5-E2026-APP: off, the operation answers 404 and nothing is generated; on, the journey runs. The harness itself is a pipeline stage selected by the run profile, not by a business flag, and has no production switch.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all seventeen owned scenarios and their evidence, and each fake has been replaced by the real service where its I story has landed in SIT. The seed pack and the evidence format wait for the values of GAP-0408.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-009 | A required merge field has no value (new) | {template} cannot be generated. {field} has no value on the case. |
| MSG-P5-010 | No current template version approved by Legal (new) | {template} has no version approved by Legal for {product} in {language}. |
| MSG-P5-011 | The treatment is not approved or not open (new) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | templateCodes is empty | Enter {field}. |
| MSG-GEN-004 | A concurrent request for the same treatment and template | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The renderer fails | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | Caller lacks Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |

Thai text for each message follows decision DL10. The harness asserts these messages and never rewrites them; its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-30 Case documents shows the generated documents in the list state, with state DRAFT, before review. No screen is built by this story: the harness drives the operations behind SCR-30 and asserts the DRAFT state and the document metadata through the contracts. The screen itself belongs to RWB-E2-017, and the generation, review and send screens are out of scope here.

Loading state of SCR-30: as Screen Specifications v1 gives it. Empty, error and no access states: Not specified in the source documents (CG-ALL-717).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15-ITG | Access, X12, AC14 | Component | RW-TEAMMGR user (Documents R) calls POST generated-documents; refused with MSG-P4-002 |
| TC-E2-026-01-ITG | AC1, BR1, BR4, BR6 | Integration | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 |
| TC-E2-026-02-ITG | AC2, BR3 | Integration | Case with no title deed number |
| TC-E2-026-03-ITG | AC3, BR10 | Integration | Template v3 valid from 2026-12-15 |
| TC-E2-026-04-ITG | AC5, BR1 | Integration | DIL-CA v1 not approved |
| TC-E2-026-05-ITG | BR2, X3, AC9 (owned by RWB-P6-E2026-APP) | Integration | DIL-MORTGAGE withdrawn |
| TC-E2-026-06-ITG | AC6, BR5 | Integration | Treatment with no decision_log_id |
| TC-E2-026-07-ITG | AC7, BR7 | Integration | Decision log stub refusing writes |
| TC-E2-026-08-ITG | AC8, BR9 | Integration | Same Idempotency-Key twice |
| TC-E2-026-09-ITG | BR8, X7, AC10 (owned by RWB-P5-E2026-APP) | Integration | Two parallel requests |
| TC-E2-026-10-ITG | BR8, X8, AC11 (owned by RWB-P5-E2026-APP) | Integration | Damaged template body |
| TC-E2-026-11-ITG | BR1, X9, AC12 (owned by RWB-P6-E2026-APP) | Integration | Hire purchase case, mortgage-only template |
| TC-E2-026-12-ITG | BR1, X11, AC13 (owned by RWB-P4-E2026-APP) | Integration | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-17-ITG | X13, AC15 | Integration | Seed pack missing an item or a seeded template not approved |
| TC-E2-026-18-ITG | X14, AC16 | Integration | Environment lock held by another run |
| TC-E2-026-19-ITG | BR11, AC17 | Integration | National ID filled at render time from the token service |
| TC-E2-026-13-ITG | AC4 | Integration | Three current templates |
| TC-E2-026-14-ITG | AC5, BR8 | Integration | Three templates, DIL-CA not approved |
| TC-E2-026-16-ITG | Principle 5 | NFR | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |

Each `-ITG` case is the journey copy of the legacy case: the same Given, When and Then, run across the five contracts and the fakes of section 12.8. The unit and component copies of the same cases stay with the app stories that own the rule, and this story keeps the integration copy only.

### 17. Guardrails

- No business value in code: template codes, merge field names, value formats, the template-to-document-type mapping and the font are data files and parameter rows, never constants in the harness.
- No personal data in events, workflow inputs, logs, evidence or prompts. Merge values and the merge snapshot are never logged in clear; the evidence keeps identifiers, statuses and timestamps only, and the clear national ID number stays inside the stored file (BR11).
- No read of another service's tables and no schema of the harness's own: every read goes through the operations of section 12.2 (DP-01, DP-15), and a cross-schema reference found in the trace fails the run.
- No document is produced from a template version without approved_by_legal true, and no scenario may seed one to make a run pass.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and an exception is never added to a scenario; a value that must change changes in the seed pack through a reviewed change.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01-ITG, TC-E2-026-02-ITG, TC-E2-026-06-ITG, TC-E2-026-07-ITG, TC-E2-026-08-ITG, TC-E2-026-09-ITG, TC-E2-026-10-ITG, TC-E2-026-11-ITG, TC-E2-026-12-ITG, TC-E2-026-13-ITG, TC-E2-026-14-ITG, TC-E2-026-15-ITG, TC-E2-026-16-ITG |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03-ITG, TC-E2-026-04-ITG, TC-E2-026-05-ITG, TC-E2-026-11-ITG |

### 19. Out of scope

- The generation, review and send screens (RWB-E2-017).
- The e-signature flow (RWB-E2-018).
- Rule-driven generation when the deed in lieu route reaches TRANSFER_PRICE_SET (Epic 3).
- Template upload and Legal approval (RWB-E1-034) and the merge field catalog (RWB-E1-046).
- Debt sale agreements and notices (Epic 6).
- The production code of any service: rwb-document, rwb-comms, rwb-treatment, rwb-access and rwb-decision are built by their own I stories, and this story only calls them or their fakes.
s.
