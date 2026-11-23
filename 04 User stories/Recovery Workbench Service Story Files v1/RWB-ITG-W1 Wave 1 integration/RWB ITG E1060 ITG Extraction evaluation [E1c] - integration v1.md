# RWB-ITG-E1060-ITG Extraction evaluation [E1c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1060-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-060 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E1053-APP, RWB-P10-E1060-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-005, REQ-DCM-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-060 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer** proving the extraction evaluation end to end on the real SIT services of rwb-document (P5) and rwb-agent (P10) and their published contracts, I want **one suite that loads the labelled sample, runs the three approaches on the same court notices, scores every field and approach, builds the proposal per document type and exports it**, so that **the approach and the confidence threshold proposed for a document type are measured across the document boundary between P5 and P10, with the model versions, the prompt version and the policy version in force recorded on the evidence, before wave 1 exits**.

### 2. Business rationale

Fields read wrongly from a court notice or a title deed send a case down the wrong step, and fields sent to review without need take officer time. RWB-E1-060 measured the three approaches - OCR template, model, and OCR checked by the model - on the same reviewed documents, field by field, and proposed for each document type the approach and the confidence threshold below which a field goes to the review queue. It served REQ-DCM-006 (fields extracted for the agreed types) and REQ-DCM-005 (a confidence score and a review queue below the threshold).

In the legacy delivery all of that lived inside one module: the stored OCR fields sat beside the scorer, the model was called in process, the sample was loaded into the same schema and the proposal was a column on the same evaluation run row. In the target the facts the measurement stands on belong to different owners. The stored document and its extracted fields are P5 rwb-document, schema `rwb_document`, and are readable only through the P5 contract (DP-01, ASM-0515). The sample, the shadow runs, the score rows and the proposal are P10 rwb-agent, schema `rwb_agent`, and are readable and writable only through the P10 admin contract (ASM-0517). The document types and LOV-DOC-TYPE are P3 rwb-case reference data, not P4 (DP-07, ASM-0514). The right that lets a person load a sample and start an evaluation is P4 rwb-access, and the session that proves the absence of that right is read through P4. The model is reached only by P10, through its gateway client, and the only thing the suite may stand in for is the enterprise model endpoint INT-23, which no suite may call with real prompts (ASM-0516).

The component copy of the behaviour is RWB-P10-E1060-APP. That story builds and unit-tests the four evaluation tables, the sourcer, matcher and proposal components, the proposal column added by P10's own migration `V10_003__evaluation_proposal.sql`, and the four admin operations inside rwb-agent, against the published contracts of its neighbours. This integration story exists because the four facts that make the proposal trustworthy cannot be proved inside one service:

- The OCR_TEMPLATE approach is a statement about a read that now crosses a service boundary: it must make no model call and must read the stored `document_field` values through the P5 contract, while MODEL and OCR_AND_MODEL must read the document content through the same contract under the identity SY-AGENT. Whether the run read a value or a table is only visible when the two services are real (AC9).
- The three approaches must be comparable on the same documents. A document that P5 no longer returns, a type whose list version moved, or a content read that answers for a different document breaks the comparison, and each of those is a fact about two services, not one (AC6, AC10).
- The proposal is a decision instrument. It must name the approach, the precision and recall per field and the proposed threshold, mark a type with too few labels as "insufficient sample", propose a field that never reaches the target as review-only and break a tie on model calls - and the numbers must be read back through the P10 contract and exported without a personal value (AC2, AC3, AC5, AC7, AC13).
- The evaluation runs agent EXTRACT in shadow and changes nothing in force: no `document_field` value and no review threshold in P5 before and after the run, and only P10 rows written (AC11, AC14).

The suite therefore carries no legacy criterion: every criterion of this story is new (D-RCV-60) and is written to prove the deliverable in the title on real services, with the legacy values of RWB-E1-060 kept character for character - agent "EXTRACT", policy "P1", prompt "PR1", output schema "extract-fields-v1", approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL, sample "EXTRACT-S1" version 1 with 40 court notices of type "COURT_NOTICE", fields court_name, case_number and hearing_date, target precision 0.95, minimum 30 labelled documents per type, 34 true positives, 2 false positives and 4 false negatives for hearing_date under OCR_TEMPLATE (precision 0.9444, recall 0.8947), mean F1 0.9310 on the tie, "TITLE_DEED" with 12 labelled documents, case_number at most 0.91, the model stub timeout on document 7 of 40, and the message IDs MSG-P10-001, MSG-P10-002, MSG-P10-003 and MSG-P4-002 - so that a reader can follow the legacy story beside this one.

The only thing faked is the outside world: INT-23 is reached through a recorded external stub of its OpenAPI 3.1 contract with a timeout switch and a deterministic answer set, because no suite may call a live model endpoint with real prompts and the timeout and tie paths must be reproducible. P5 rwb-document and P10 rwb-agent are the real SIT services of the integration dependency list, P3 rwb-case and P4 rwb-access are the real wave-1 services on their published contracts, and a run that needs a fake for any of them fails the preflight, because a fake would defeat the purpose of the run.

The measures the story is read against are the legacy ones: precision, recall, F1 and sample size per field and approach, the failure count per code on the evaluation run, the proposal per document type, and the absence of any personal value in the export. The proposal a reader compares with is the legacy one: the approach with the highest mean F1 per type and the lowest confidence at which every chosen field reaches precision 0.95, with the tie order and the sample floor taken from the approved policy row and not from code (ASM-0518).

### 3. Preconditions

- RWB-P5-E1053-APP is done: rwb-document is deployed with schema `rwb_document`, the document, `document_field` and OCR text rows are in place for the six document types, and the three read operations of section 12.2 answer on the published contract.
- RWB-P10-E1060-APP is done: rwb-agent is deployed with schema `rwb_agent`, the agent_sample, agent_run, agent_evaluation_run and agent_evaluation tables, the extraction evaluation components, the proposal column added by `V10_003__evaluation_proposal.sql`, and the four admin operations of section 12.2.
- The published contracts of P5 rwb-document and P10 rwb-agent are versioned in the registry, and the suite consumes only those contracts; the P3 reference-data and P4 session contracts are consumed as wave-1 published-contract preconditions and are not integration dependencies of this story.
- Agent "EXTRACT" exists with policy version "P1" approved (mode SHADOW, allowed tools read_document_content and read_document_fields, output schema "extract-fields-v1", prompt "PR1") and holds the target precision 0.95, the minimum labelled sample 30 and the tie order as policy values, loaded by RW-COE and approved by RW-RISK (ASM-0518).
- Labelled sample "EXTRACT-S1" version 1 is loaded through `POST /api/recovery/agent/v1/admin/agent-samples`: 40 documents of type "COURT_NOTICE" with labels for court_name, case_number and hearing_date, and 12 documents of type "TITLE_DEED"; personal label values are held as SHA-256 hashes.
- The six document types and LOV-DOC-TYPE are in force in P3 rwb-case and are read through `GET /api/recovery/case/v1/admin/lists/{listCode}` (ASM-0514).
- The service identity SY-AGENT exists with Documents R on rwb-document, so the content and field reads of the model approaches are answered under the same role check as a person.
- RW-COE holds Rules and parameters C; RW-RISK holds Rules and parameters A and reads the scores; synthetic user "RW-CASEOWN" holds no Rules and parameters right, and the fact is proved through `GET /api/recovery/access/v1/me/session`.
- The INT-23 stub is deployed with its OpenAPI 3.1 document, its deterministic answer set and its timeout switch, and the W1J01 synthetic document fixture is loaded (ASM-0516).
- The harness RWB-ITG-W1J01-ITG is available with the synthetic documents, the synthetic identities and the wiring of wave 1.
- The SIT environment is available with the P5 and P10 endpoints, the reference-data endpoint of P3 and the session endpoint of P4.
- No production data is read, copied or connected to; every court notice, title deed, case number, party, national ID number, phone number and account number used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: runs the preflight, which reads the OpenAPI documents of P5 and P10 and the published contracts of P3 and P4, and fails before any assertion if a path, a field, a status code or a media type has drifted; it also confirms that no fake is configured for P5, P10, P3 or P4.
2. Harness: reads the document types in force through `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-DOC-TYPE and compares them with the types the sample uses; a difference stops the run before any row is scored (AC10).
3. Harness: reads the documents of the sample through `GET /api/recovery/document/v1/cases/{caseId}/documents` and each document through `GET /api/recovery/document/v1/documents/{documentId}`, and confirms that every row of the sample names a document P5 returns; a row for a document that P5 does not return is loaded as the refusal case of AC6 (AC6).
4. Harness: reads the approved policy and prompt versions of agent "EXTRACT" through `GET /api/recovery/agent/v1/admin/agent-configs` and takes the target precision 0.95, the minimum sample 30 and the tie order from the policy row, never from suite code (AC2, AC7).
5. Harness: loads labelled sample "EXTRACT-S1" version 1 through `POST /api/recovery/agent/v1/admin/agent-samples` as RW-COE, with the personal label values hashed, and reads the sample back as counts.
6. Harness: starts the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 for the approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL through `POST /api/recovery/agent/v1/admin/agent-evaluations` as RW-COE (AC8).
7. P10: for OCR_TEMPLATE, reads the stored `document_field` values and their confidence through `GET /api/recovery/document/v1/documents/{documentId}` and makes no model call; the suite counts the P5 calls of this approach (AC9).
8. P10: for MODEL, reads the document content through `GET /api/recovery/document/v1/documents/{documentId}/content` as SY-AGENT, calls agent "EXTRACT" in shadow through its gateway client to INT-23 and reads the fields from its answer; for OCR_AND_MODEL it passes the stored OCR fields with the content and takes the checked values (AC1, AC9).
9. P10: compares each value with the label (trim and case folding for text, dates as dates, personal values by SHA-256) and stores true positives, false positives, false negatives, precision and recall per field and approach, with the model version and prompt version "PR1" on every row where the approach calls the model (AC1).
10. Harness: switches the INT-23 stub to its timeout for document 7 of 40 and asserts that every labelled field of document 7 counts as a false negative for MODEL and that the run holds failure count TIMED_OUT 1 (AC4).
11. P10: builds the proposal per document type - the approach with the highest mean F1, its precision and recall per field, and the lowest confidence at which every chosen field reaches precision 0.95 - marks a type under the sample floor as "insufficient sample", proposes a field that never reaches the target as review-only and breaks a tie on model calls (AC2, AC3, AC5, AC7).
12. Harness: polls `GET /api/recovery/agent/v1/admin/agent-evaluations` to status "DONE" and reads the score rows and the proposal per document type through the same operation, never through a table (AC1, AC2, AC3, AC5, AC7).
13. Harness: asserts the shadow guarantee across the boundary - each model approach run row holds policy "P1", prompt "PR1" and the model version, and the `document_field` values and the review threshold in force read through P5 before and after the run are identical (AC11, AC14).
14. Harness: repeats the evaluation start while it is RUNNING and asserts 409 with MSG-P10-003; loads a sample row naming a document P5 does not return and asserts 422 with MSG-P10-001 naming the row number; calls the two evaluation operations as synthetic user "RW-CASEOWN" and asserts 403 with MSG-P4-002 (AC6, AC8, AC12).
15. Harness: exports the proposal through `GET /api/recovery/agent/v1/admin/agent-evaluations` with Accept text/csv and asserts one row per document type and no national ID number, phone number, name or account number in it (AC13); then cleans up the sample, the evaluation run and the loaded sample version and writes the evidence report with one verdict per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A document type has fewer labelled documents than the minimum of 30 | The type is scored and marked "insufficient sample"; no approach and no threshold are proposed for it | None to a user | AC3 |
| X2 | The model stub times out on a document | Every labelled field of that document counts as a false negative for the model approaches; the failure is counted on the run as TIMED_OUT | None to a user | AC4 |
| X3 | Two approaches reach the same mean F1 for a type | The approach with fewer model calls is proposed (OCR_TEMPLATE before OCR_AND_MODEL before MODEL) | None to a user | AC5 |
| X4 | A sample row names a document that the P5 contract does not return | The sample load is refused in full, no row of the file is stored, the row number is named | MSG-P10-001 | AC6 |
| X5 | No approach reaches precision 0.95 on a field at any confidence | The field is proposed as review-only for the type | None to a user | AC7 |
| X6 | An evaluation is started while the same one on the same sample version is RUNNING | Refused with 409, no second run row | MSG-P10-003 | AC8 |
| X7 | The sample holds no labelled rows for the agent | Refused with 422, no evaluation run and no run row | MSG-P10-002 | Section 14 |
| X8 | A role without Rules and parameters calls the evaluation operations | Refused with 403, nothing changes | MSG-P4-002 | AC12 |
| X9 | The type list in force in P3 differs from the types the sample uses | The suite stops before any row is scored and names the type that is not in force; no score row exists | None to a user | AC10 |
| X10 | A consumed contract drifts from the published one (path, field, status or media type) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X11 | A fake is configured for P5, P10, P3 or P4 | The preflight refuses the run: only INT-23 and the W1J01 fixture may be stubbed | None | Section 12.8 |
| X12 | The INT-23 stub drifts from its OpenAPI 3.1 document | The preflight fails on the stub contract test, so no assertion is made against an endpoint that no longer matches | None | AC1, AC4 |
| X13 | The W1J01 synthetic document fixture, or a synthetic identity it carries, is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC6, AC12 |

X1 to X8 are the legacy exception paths of RWB-E1-060 carried onto the real services; X9 to X13 are the failures that only appear when the run leaves one service. X7 is not reached by a criterion of this story because the empty-sample refusal is proved by RWB-P10-E1060-APP at the component level and by the E1058 sibling at the platform level; the message is kept here so a reader finds the legacy set complete. X8 is proved by the access criterion AC12 rather than by an exception path of its own, as in the legacy story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the two integration dependencies and the published contracts of P5, P10, P3 and P4, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval, the report layout and the stub switch names are configuration; the agent, the policy and prompt versions, the approaches, the sample, the fields, the target precision, the sample floor, the counts, the message IDs and the migration name are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: the stored-field read against the content read, three approaches on one sample, the score rows and the proposal read back through the contract, the shadow no-change guarantee across P5, and the export with no personal value |
| Estimable | One suite module, one external stub control, one sample and document fixture builder, four contract probes, one evaluation driver, one CSV export check and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a score row read through the contract, the proposal row of a type, a failure count, a P5 call count, a before-and-after field read, or the CSV body |

### 7. Acceptance criteria

```gherkin
Feature: Extraction evaluation [E1c], proven across rwb-document and rwb-agent

  Background:
    Given sample "EXTRACT-S1" version 1 holds 40 documents of type "COURT_NOTICE" with labels for fields court_name, case_number and hearing_date
    Given the target precision is 0.95 and the minimum labelled documents per type is 30
    Given agent "EXTRACT" has policy version "P1" approved in mode SHADOW with prompt version "PR1" and output schema "extract-fields-v1"
    Given the INT-23 model endpoint is reached only through the recorded external stub of its OpenAPI 3.1 contract
    Given rwb-document (P5) and rwb-agent (P10) are the real SIT services on their published contracts, with P3 rwb-case and P4 rwb-access on theirs
    Given the RWB-ITG-W1J01-ITG synthetic document fixture is loaded and no production value is used

  Scenario: AC1 Scores per field across the three approaches (new, D-RCV-60)
    Given sample "EXTRACT-S1" version 1 holds 40 "COURT_NOTICE" documents with labels for court_name, case_number and hearing_date
    When the three approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL run
    Then one score row exists per field and approach: 3 fields x 3 approaches for "COURT_NOTICE"
    Then for field hearing_date with approach OCR_TEMPLATE, 34 true positives, 2 false positives and 4 false negatives give precision 0.9444 and recall 0.8947
    Then each score row holds the model version and the prompt version "PR1" where the approach calls the model

  Scenario: AC2 The proposal names the approach and the confidence threshold (new, D-RCV-60)
    Given the scores for "COURT_NOTICE" are complete for the three approaches
    When the proposal is built
    Then the evaluation run names, for "COURT_NOTICE", the approach with the highest mean F1 and its precision and recall per field
    Then it names the proposed confidence threshold, the lowest confidence at which every chosen field reaches precision 0.95
    Then the export through GET /api/recovery/agent/v1/admin/agent-evaluations with Accept text/csv lists one row per document type

  Scenario: AC3 A type with too few labels gets no proposal (new, D-RCV-60)
    Given type "TITLE_DEED" has 12 labelled documents
    When the evaluation runs
    Then "TITLE_DEED" is scored and marked "insufficient sample"
    Then no approach and no threshold are proposed for "TITLE_DEED"

  Scenario: AC4 A model failure counts against the model approaches (new, D-RCV-60)
    Given the model stub times out on document 7 of 40
    When the approach MODEL runs
    Then each labelled field of document 7 counts as a false negative for MODEL
    Then the evaluation run holds failure count TIMED_OUT 1

  Scenario: AC5 Equal F1 goes to the approach with fewer model calls (new, D-RCV-60)
    Given OCR_TEMPLATE and OCR_AND_MODEL both have mean F1 0.9310 for "COURT_NOTICE"
    When the proposal is built
    Then OCR_TEMPLATE is proposed for "COURT_NOTICE"

  Scenario: AC6 A sample row for a document that does not exist is refused (new, D-RCV-60)
    Given the sample file has a row for a document ID that the P5 contract does not return
    When RW-COE loads the file through POST /api/recovery/agent/v1/admin/agent-samples
    Then the load is refused with 422 and MSG-P10-001 naming the row number
    Then no row of the file is stored

  Scenario: AC7 A field that never reaches the target is review-only (new, D-RCV-60)
    Given field case_number reaches at most precision 0.91 for every approach and confidence
    When the proposal is built
    Then case_number is proposed as review-only for "COURT_NOTICE"

  Scenario: AC8 The same evaluation twice is refused (new, D-RCV-60)
    Given the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 has status "RUNNING"
    When RW-COE starts it again
    Then the request is refused with 409 and MSG-P10-003

  Scenario: AC9 OCR_TEMPLATE reads stored fields only and the model approaches read content through P5 (new, D-RCV-60)
    Given the three approaches run on the 40 "COURT_NOTICE" documents
    When each approach reads its input
    Then OCR_TEMPLATE makes no model call and reads the stored document_field values through GET /api/recovery/document/v1/documents/{documentId}
    Then MODEL and OCR_AND_MODEL read the content through GET /api/recovery/document/v1/documents/{documentId}/content as SY-AGENT
    Then the P5 call count of the run is one field read per document for OCR_TEMPLATE and one content read per document for each model approach
    Then no document_field table is read by the run or by the suite

  Scenario: AC10 The document types come from the P3 reference-data contract (new, D-RCV-60)
    Given the six document types and LOV-DOC-TYPE are read through GET /api/recovery/case/v1/admin/lists/{listCode}
    When the suite starts the evaluation of "EXTRACT" on "EXTRACT-S1" version 1
    Then the type list in force is compared with the types the sample uses before any row is scored
    Then the suite refuses to start if the two differ and names the type that is not in force

  Scenario: AC11 The evaluation runs agent EXTRACT in shadow and changes nothing in force (new, D-RCV-60)
    Given the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 runs in the SHADOW mode of policy "P1"
    When the three approaches complete
    Then each model approach run row holds policy "P1", prompt "PR1" and the model version of the stub
    Then the evaluation changes no document_field value and no review threshold in force, checked through the P5 contract before and after the run

  Scenario: AC12 A role without the right is refused (new, D-RCV-60)
    Given synthetic user "RW-CASEOWN" holds no Rules and parameters right, proved through GET /api/recovery/access/v1/me/session
    When "RW-CASEOWN" calls POST and GET /api/recovery/agent/v1/admin/agent-evaluations
    Then both calls are refused with 403 and MSG-P4-002
    Then no evaluation run row and no score row change

  Scenario: AC13 The proposal export holds no personal value (new, D-RCV-60)
    Given the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 ended with status "DONE"
    When RW-COE calls GET /api/recovery/agent/v1/admin/agent-evaluations with Accept text/csv
    Then the response holds the proposal rows, one row per document type
    Then it holds no national ID number, phone number, name or account number
    Then personal label values compare by SHA-256 only, in the sample and in the export

  Scenario: AC14 The evaluation changes no document field and no threshold in force (new, D-RCV-60)
    Given the document_field values and the review threshold in force are read through the P5 contract before the run
    When the shadow run of "EXTRACT" on "EXTRACT-S1" version 1 completes
    Then the same P5 reads return the same values after the run
    Then the run writes only P10 rows and no P5 value
```

**Target reading.** The agent, its policy and prompt versions, the output schema, the three approaches, the sample, the three fields of the measurement, the target precision, the sample floor, the counts, the tie rule and the message IDs are the legacy values of RWB-E1-060, copied character for character. The evaluation tables are the P10 tables in schema `rwb_agent` (DP-01), the proposal column is added by P10's own migration `V10_003__evaluation_proposal.sql` in its own Flyway sequence (DP-15), and the base is `/api/recovery/agent/v1` (DP-13). The in-process `DocumentQueryService` of the legacy section 12 becomes the P5 contract read across one hop with a 2 s client budget (DP-11 behind DP-01), so AC9 asserts the field read and the content read as two different operations of the owner instead of two methods of one class. The document types leave P4 and are read from P3's reference-data contract (DP-07, ASM-0514); the score rows and the proposal stay in P10 and are read and exported through `GET /admin/agent-evaluations` (ASM-0517); the target precision, the sample floor and the tie order stay policy values of agent_policy EXTRACT P1 and no threshold of P5 is written by the run (ASM-0518).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A value is a true positive when it equals the label after trim and case folding; dates compare as dates; personal fields compare by SHA-256 hash | agent_sample.expected_value (DF-AGT-068); CTL-11; legacy BR1 |
| BR2 | Precision = TP / (TP + FP); recall = TP / (TP + FN); F1 = 2PR / (P + R); four decimals | agent_evaluation (DF-AGT-091 to DF-AGT-096); legacy BR2 |
| BR3 | A type with fewer labelled documents than the minimum of 30 gets no proposal and is marked "insufficient sample" | agent_policy row EXTRACT (DF-AGT-006 to DF-AGT-016); legacy BR3 |
| BR4 | The proposed threshold is the lowest confidence at which precision reaches the target of 0.95; a field that never reaches it is review-only | REQ-DCM-005; document_field.confidence (DF-DOC-016); legacy BR4 |
| BR5 | Ties go to the approach with fewer model calls: OCR_TEMPLATE before OCR_AND_MODEL before MODEL | agent_policy row EXTRACT; legacy BR5 |
| BR6 | OCR_TEMPLATE reads stored fields only and makes no model call; MODEL and OCR_AND_MODEL call agent EXTRACT in shadow through the P10 gateway client under policy "P1" | DT06; ASM-0516 |
| BR7 | Every document and every stored field the run reads comes through the P5 contract as SY-AGENT; no service and no suite reads `rwb_document`, `document_field` or any other service's schema | DP-01; DP-11; Arch v5 slide 16 |
| BR8 | The document types and LOV-DOC-TYPE are read from the P3 reference-data contract, and a type outside the list in force is not scored and gets no proposal | DP-07; ASM-0514 |
| BR9 | A sample row is validated against the P5 contract before any row is stored; one bad row refuses the whole file and the sample version in force is unchanged | Legacy BR10; CTL-08; MSG-P10-001 |
| BR10 | The evaluation runs the agent in shadow and writes only agent_sample, agent_run, agent_evaluation_run and agent_evaluation; it changes no `document_field` value and no review threshold in P5 | Legacy section 17; RWB-P10-E1060-APP; ASM-0518 |
| BR11 | Every model approach run row records policy "P1", prompt "PR1" and the model version, so a score can be reproduced against the versions that produced it | agent_run (DF-AGT-036 to DF-AGT-057); agent_evaluation_run (DF-AGT-070 to DF-AGT-083) |
| BR12 | No business value (target precision, sample floor, tie order, approach names, counts) is written in code or in the suite; every one of them is read through the P10 or P3 contract at run time | Principle 1; DT02; ASM-0518 |
| BR13 | One RUNNING evaluation per agent and sample version; a second start is refused with 409 | MSG-P10-003; legacy X6 |
| BR14 | No personal value appears in a score row, a proposal row, the CSV export or the suite log; label values are compared as SHA-256 hashes and every document of the run is synthetic | CTL-11; Legacy section 17 |
| BR15 | Every REST call of the run is one hop to the owning service with a 2 s client budget; the model budget belongs to the P10 gateway client and is never a REST budget of the suite | ADR-020; DP-11 |
| BR16 | The suite holds no schema client: every fact is read through a contract of section 12.2, and a pipeline scan fails any change that adds a database connection | DP-01; section 17 |

### 9. State transitions

The state transitions of an evaluation run:

| From | Event | Condition | To |
|---|---|---|---|
| None | Evaluation started through `POST /admin/agent-evaluations` | The sample has labelled rows and no run for the same agent and sample version is RUNNING | RUNNING (agent_evaluation_run.status) |
| None | Evaluation started | The sample has no labelled rows for the agent | No row; 422 MSG-P10-002 |
| None | Evaluation started | One for the same agent and sample version is RUNNING | No row; 409 MSG-P10-003 |
| RUNNING | Last sample row scored | None | DONE |
| RUNNING | The run aborted by an operator or a failed stub contract | None | No transition in this story; the run is cleaned up and no criterion of this story reads it |

The state of each score row and of the proposal:

| From | Event | Condition | To |
|---|---|---|---|
| None | A field scored for an approach | A labelled value compared with the approach value | One row per field and approach with TP, FP, FN, precision and recall |
| None | A type proposed | The type reaches the sample floor of 30 and an approach reaches the target | Proposal row with the approach, the per-field precision and recall and the threshold |
| None | A type proposed | The type is under the sample floor | Marked "insufficient sample", no approach and no threshold |
| None | A field proposed | The field never reaches precision 0.95 at any confidence | Field marked review-only |

The states the run observes across the services:

| Item | States |
|---|---|
| INT-23 stub | Deterministic answer set, timeout on document 7 of 40 |
| Evaluation run | RUNNING, DONE |
| Sample | Loaded as a new version through the P10 contract, or refused in full with MSG-P10-001 |
| `document_field` in P5 | Read only; the same values before and after the run |
| Suite run | Not started, preflight failed, running, passed, failed with the failing test case named |

The threshold a proposal names takes effect only when P5 loads it as a new reference-data version, which is RWB-E1-054 and is out of scope here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the stub control and its timeout switch, the P5 call counter, the cleanup and the evidence report |
| RW-COE, centre of excellence analyst | Loads the sample, starts the evaluation, reads and exports the scores and the proposal (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves the policy and prompt versions and reads the scores and the proposal (Rules and parameters A) |
| RW-CASEOWN, case owner | Holds no Rules and parameters right in this story; is used as the refused synthetic user of AC12 |
| SY-AGENT, agent platform | Reads document content and stored fields through the P5 contract (Documents R) |
| SY-OCR | Produced the stored fields earlier through `DocumentIntakeWorkflow`; not called here |
| Service owner of rwb-document (P5) | Owns document, `document_field`, OCR text, the three read operations and the review threshold in force |
| Service owner of rwb-agent (P10) | Owns the four evaluation tables, the extraction evaluation components, the proposal column of `V10_003__evaluation_proposal.sql`, the four admin operations and the gateway client to INT-23 |
| Service owner of rwb-case (P3) | Owns the document types and LOV-DOC-TYPE and the reference-data read |
| Service owner of rwb-access (P4) | Owns the session read, the right check and the refusal of MSG-P4-002 |
| No role | Reads a service schema directly, writes a P5 field or a threshold from the evaluation, or takes production data into the run |

Approval levels: no delegation of authority level applies; the approval of the policy and prompt versions is the Rules and parameters A right, as in the legacy story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read through the P5 contract |
| DF-DOC-004 | document | document_type | Read through the P5 contract |
| DF-DOC-006 | document | storage_ref | Read through the P5 contract (content through the content operation) |
| DF-DOC-013 | document_field | document_id | Read through the P5 contract |
| DF-DOC-014 | document_field | field_name | Read through the P5 contract |
| DF-DOC-015 | document_field | field_value | Read through the P5 contract |
| DF-DOC-016 | document_field | confidence | Read through the P5 contract |
| DF-DOC-017 | document_field | confirmed_by | Read through the P5 contract, as a count of confirmed labels; no person is named |
| DF-AGT-063 to DF-AGT-069 | agent_sample | sample_code, sample_version, subject_type, subject_id, label_key, expected_value, labeled_by | Loaded through the P10 contract; read back as counts only; written by rwb-agent (owner P10, schema `rwb_agent`) |
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, model_version, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at, evaluation_run_id | Read through the P10 contract, except output and subject_id, which no listing returns; written by rwb-agent (owner P10) |
| DF-AGT-070 to DF-AGT-083 | agent_evaluation_run | id, agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, started_at, finished_at, requested_by, total_cost_thb, p95_latency_ms, failure_counts | Read through the P10 contract; written by rwb-agent (owner P10) |
| DF-AGT-084 | agent_evaluation_run | proposal | Read through the P10 contract and the CSV export; written by rwb-agent in the column added by `V10_003__evaluation_proposal.sql` |
| DF-AGT-087 to DF-AGT-096 | agent_evaluation | evaluation_run_id, approach, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Read through the P10 contract; written by rwb-agent (owner P10) |
| DF-REF fields of the document types | reference_row, reference_version | the codes of LOV-DOC-TYPE and their version | Read through the P3 reference-data contract; never read as a table |

Field IDs are those of RWB-E1-060 and are copied unchanged. document, document_field and document_text are the P5 tables of schema `rwb_document`; agent_sample, agent_run, agent_evaluation_run and agent_evaluation are the P10 tables of schema `rwb_agent` in the ownership map. The suite owns no field and no table: it reads every row of this table through a contract of section 12.2 and writes only through the admin operations of rwb-agent, with synthetic values. No field ID of agent_alert, agent_feedback, agent_prompt or agent_policy is written here; the policy and prompt versions are read as versions through `GET /admin/agent-configs`.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are not used, and no `rwb_integration` table is written. The evaluation belongs to P10 rwb-agent, base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, queue `rwb-agent` and schema `rwb_agent`; the documents and their stored fields belong to P5 rwb-document, base `/api/recovery/document/v1` and schema `rwb_document`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| POST | `/api/recovery/agent/v1/admin/agent-samples` | P10 rwb-agent | Flow step 5 and AC6: the load of sample "EXTRACT-S1" version 1 and the refusal of a row naming a document P5 does not return | 2 s + load time |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | Flow step 6 and AC8: the start of the evaluation for the three approaches and the second-start refusal | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC1, AC2, AC3, AC5, AC7 and AC13: the evaluation run with its score rows and the proposal per document type, polled to status "DONE", and the CSV export with Accept text/csv | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | Flow step 4: the approved policy "P1" and prompt "PR1" versions of agent "EXTRACT" and the values the measurement is read against | 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | AC1, AC6, AC9 and AC14: the document facts and the stored `document_field` values with their confidence, read for OCR_TEMPLATE and for the sample check | 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | P5 rwb-document | AC4, AC9, AC11 and AC14: the document content read as SY-AGENT by MODEL and OCR_AND_MODEL | 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Flow step 3 and AC6: the documents of the synthetic case, to confirm that every sample row names a document P5 returns | 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC3 and AC10: the six document types and LOV-DOC-TYPE in force, read before any row is scored | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC12: the rights of the caller, which prove that RW-CASEOWN holds no Rules and parameters right | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service. The model budget belongs to the P10 gateway client and is never a REST budget of the suite. The P3 and P4 reads are the wave-1 published-contract preconditions of section 3, not integration dependencies of this story.

#### 12.3 Events published

None. The suite publishes no business event. The evaluation run is internal to P10 and publishes no business event of its own: the score rows and the proposal are read through `GET /admin/agent-evaluations`.

#### 12.4 Events consumed

None. The evaluation run is internal to P10 and publishes no business event to consume; the suite reads the run, its scores and its proposal through the operation of section 12.2 and consumes no topic. `rwb.agent.AgentRunCompleted.v1` is published by a business run of an agent and is proved by the E1058 sibling, not here.

#### 12.5 Workflows and activities

None. The suite starts no workflow and observes none: it starts the evaluation through `POST /admin/agent-evaluations`, and the extraction evaluation runs inside P10 on the admin request path, not as a Temporal workflow of its own. `AgentRunWorkflow` and the agent runtime client belong to RWB-ITG-TE013-ITG and to the E1058 sibling.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The evaluation is started by RW-COE through `POST /api/recovery/agent/v1/admin/agent-evaluations` and never on a cadence, and the suite starts no schedule of its own.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The four evaluation tables of schema `rwb_agent` are owned by P10 rwb-agent and are read through the operations of section 12.2; the document, `document_field` and OCR text rows of schema `rwb_document` are owned by P5 rwb-document and are read through its three operations; the document types are read through P3; the session is read through P4. The proposal column is added by P10's own migration `V10_003__evaluation_proposal.sql` in the P10 Flyway sequence, and the suite neither runs nor edits a migration (DP-15).

#### 12.8 Contract fakes

None for a service contract. The only fakes are outside the nineteen services:

| Stub | Purpose |
|---|---|
| INT-23 WireMock stub with its OpenAPI 3.1 contract | Stands in for the enterprise model endpoint that no suite may call with real prompts; returns the deterministic answer set of the 40 court notices and the 12 title deeds, and holds the recorded request and the call count |
| INT-23 fault switch: timeout | Makes the stub silent for document 7 of 40, for AC4 |

P5 rwb-document, P10 rwb-agent, P3 rwb-case and P4 rwb-access are the real SIT services on their published contracts and are not faked in the normal path; a run configured with a fake for any of them fails the preflight (X11). The synthetic documents, the synthetic case and the synthetic identities come from the harness RWB-ITG-W1J01-ITG, not from a mock of P5 or P4.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 9 | The four P10 admin and read operations, the three P5 document reads, the P3 reference-data read and the P4 session read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | None | The evaluation run is internal to P10 and publishes no business event |
| Temporal | None | None | No workflow and no schedule in this story |
| File | None | None | The sample is loaded through the admin operation and the proposal is exported from the same operation with Accept text/csv; no file path is used |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a stub control for INT-23 with its deterministic answer set and its timeout switch, a fixture builder for the synthetic documents and the labelled sample, contract probes over P5, P10, P3 and P4, an evaluation driver that starts the run and reads the scores and the proposal, a P5 call counter, a CSV export check and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts of P5, P10, P3 and P4, run order, report and exit code |
| ModelStubControl | Test harness | Deploys the INT-23 stub from its OpenAPI 3.1 document, serves the deterministic answer set, sets the timeout on document 7 of 40, and exports the recorded request and the call count |
| DocumentFixture | Test harness | Seeds the 40 synthetic "COURT_NOTICE" documents and the 12 "TITLE_DEED" documents with their stored fields and confidence through the P5 and W1J01 boundary; holds no production value |
| SampleProbe | Test harness | Loads sample "EXTRACT-S1" version 1, asserts the row-number refusal with MSG-P10-001 and that no row of a refused file is stored |
| TypeProbe | Test harness | Reads LOV-DOC-TYPE through the P3 contract and compares the list in force with the types the sample uses before any row is scored |
| FieldReadProbe | Test harness | Counts the P5 calls per approach, asserts the field read of OCR_TEMPLATE and the content read of the model approaches as SY-AGENT, and scans for any schema client |
| EvaluationDriver | Test harness | Starts the evaluation for the three approaches, polls it to DONE, reads the score rows and the proposal, and proves the already-running and empty-sample refusals |
| ShadowProbe | Test harness | Reads the `document_field` values and the review threshold through P5 before and after the run and compares them; asserts that only P10 rows were written |
| ExportProbe | Test harness | Reads the proposal with Accept text/csv, asserts one row per document type and scans the body for personal patterns |
| AccessProbe | Test harness | Reads the caller session through P4 and asserts that RW-CASEOWN is refused with 403 and MSG-P4-002 |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table, no schema object and no migration; the proposal column and the four evaluation tables are P10's, and the document and field rows are P5's.

**Configuration and reference data**

- The SIT endpoints of P5, P10, P3 and P4, the list code of LOV-DOC-TYPE and the 2 s client budget, all as configuration.
- The synthetic case of the W1J01 set, the 40 "COURT_NOTICE" documents and the 12 "TITLE_DEED" documents, the synthetic users RW-COE, RW-RISK and RW-CASEOWN and the identity SY-AGENT, all from the harness.
- The agent "EXTRACT", the policy version "P1", the prompt version "PR1", the output schema "extract-fields-v1", the three approach names, the target precision 0.95, the minimum sample 30 and the tie order, read through the P10 contract and never written in the suite code (BR12; ASM-0518).
- The sample code EXTRACT-S1 and its version 1, and the poll interval of the evaluation driver.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of the table stay with the service, platform and operations stories that own them; this story carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7).

- **DP-01** sits on every read of the story: the document, its stored fields and its content are read through `/api/recovery/document/v1` and the evaluation rows through `/api/recovery/agent/v1`, and the suite holds no schema client and no `recovery.` table name. The P5 call counter of AC9 is the observable that a value was read and a table was not.
- **DP-06** sits on the four values the measurement is read against - target precision 0.95, minimum sample 30, tie order and the approach set: they are parameters of the approved policy row of agent "EXTRACT" and are read through the P10 admin configuration contract, so a change of threshold is a version change and not a release. The parameters client library and the P3 parameters contract serve the owning service stories, and their H and C rows stay there.
- **DP-07** sits on AC10: the six document types and LOV-DOC-TYPE are read from `GET /api/recovery/case/v1/admin/lists/{listCode}`, and the legacy route through P4 is dropped (ASM-0514).
- **DP-13** sits on the four bases the suite consumes: `/api/recovery/agent/v1`, `/api/recovery/document/v1`, `/api/recovery/case/v1` and `/api/recovery/access/v1`; no path of the legacy monolith base appears outside a quotation of the legacy story.
- **DP-15** sits on `V10_003__evaluation_proposal.sql`: the proposal column is added in `rwb_agent` by P10's own Flyway sequence, and the suite neither runs nor edits a migration; it asserts the column through the contract that reads it.
- **DP-19** sits on the absence of a screen: RW-COE and RW-RISK read and export the scores through the admin operations, which stand in for the evaluation screen of a later epic, and gateway-bff carries the composite route in front of them.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Document fixture | 40 synthetic "COURT_NOTICE" documents with stored `document_field` values and a confidence per field, and 12 synthetic "TITLE_DEED" documents, all seeded through the W1J01 boundary with no production value | AC1 to AC14 |
| Labelled sample set | Sample "EXTRACT-S1" version 1 with labels for court_name, case_number and hearing_date, personal values held as SHA-256, loaded through the P10 contract | AC1 to AC8, AC11 to AC14 |
| Model stub answers | The deterministic answer set behind the 34/2/4 hearing_date counts and the 0.9310 tie, and the timeout on document 7 of 40, held by ModelStubControl | AC1, AC4, AC5 |
| Identity set | RW-COE with Rules and parameters C, RW-RISK with A, RW-CASEOWN without the right, and SY-AGENT with Documents R | AC6, AC8, AC12 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5, P10, P3 and P4 and to the list code of LOV-DOC-TYPE, with the contract preflight that fails on any drift and refuses a fake for P5, P10, P3 or P4 (DP-13).
2. Build DocumentFixture and ModelStubControl over the INT-23 OpenAPI 3.1 document, with the deterministic answer set, the recorded request, the call count and the timeout switch (AC1, AC4).
3. Build TypeProbe and SampleProbe: the type list in force against the sample types, the sample load, the row-number refusal with MSG-P10-001 and the no-row-stored assertion (AC6, AC10).
4. Build FieldReadProbe: the P5 call counter, the field read of OCR_TEMPLATE with no model call, and the content read of the model approaches as SY-AGENT (AC9).
5. Build EvaluationDriver: start for the three approaches, poll to DONE, and read the score rows per field and approach with precision, recall and the model and prompt versions (AC1, AC2).
6. Add the proposal assertions: the highest mean F1 per type, the threshold of 0.95, the "insufficient sample" mark, the review-only field and the tie rule (AC2, AC3, AC5, AC7).
7. Add the failure path: the stub timeout on document 7 of 40, the false negatives and the failure count TIMED_OUT 1 (AC4).
8. Build ShadowProbe: the `document_field` and threshold reads through P5 before and after the run, and the assertion that only P10 rows were written (AC11, AC14).
9. Build ExportProbe: the CSV export with one row per document type and the personal-pattern scan (AC13).
10. Add the already-running refusal, AccessProbe and ReportWriter, clean up the sample, the evaluation run and the loaded sample version, and write the evidence report with one verdict per test case (AC8, AC12).

**Done when.** The fourteen test cases of section 16 pass on the real services in SIT, the fourteen criteria of section 7 are signed off against the contracts, the proposal holds one row per document type, the P5 field and threshold reads return the same values before and after the run, the export holds no personal value, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A sample row fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The sample has no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from RWB-E1-060 and this story adds no message ID. Thai text for each message follows decision DL10. In AC6 the {kind} value is "sample", the {agent} value is "EXTRACT" and the {check} value names the row number and the document ID that P5 does not return. In AC8 the {sample} value is "EXTRACT-S1" version 1. In AC12 the {action} value is "start or read an evaluation".

### 15. Screens and states

No screen in this story. RW-COE and RW-RISK read the scores and the proposal through `GET /api/recovery/agent/v1/admin/agent-evaluations` and export the proposal rows as CSV with Accept text/csv. The states the suite asserts through that operation are: a run in status RUNNING with the sample version it was started on, a run in status DONE with one score row per field and approach, a proposal row per document type with the chosen approach, its precision and recall per field and its threshold, a type marked "insufficient sample" with no approach and no threshold, and a field marked review-only. The empty state of an agent with no evaluation is read as an empty result. The review queue screen, the document screens and the architecture decision record belong to other stories and are out of scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-060-01-ITG | AC1, BR1, BR2 | Integration | 40 "COURT_NOTICE" documents; hearing_date with OCR_TEMPLATE counts 34, 2 and 4, precision 0.9444 and recall 0.8947; end to end on the real services |
| TC-E1-060-02-ITG | AC2, BR4 | Integration | Scores for "COURT_NOTICE" across the three approaches; the chosen approach and the threshold at precision 0.95; end to end on the real services |
| TC-E1-060-03-ITG | AC3, BR3 | Integration | "TITLE_DEED" with 12 labelled documents; marked "insufficient sample"; end to end on the real services |
| TC-E1-060-04-ITG | AC4 | Integration | The model stub times out on document 7 of 40; false negatives for MODEL and failure count TIMED_OUT 1; end to end on the real services |
| TC-E1-060-05-ITG | AC5, BR5 | Integration | Equal mean F1 0.9310 for OCR_TEMPLATE and OCR_AND_MODEL; OCR_TEMPLATE proposed; end to end on the real services |
| TC-E1-060-06-ITG | AC6, BR9 | Contract | A sample row naming a document P5 does not return; 422 with MSG-P10-001 naming the row number and no row stored; end to end on the real services |
| TC-E1-060-07-ITG | AC7, BR4 | Integration | case_number at most precision 0.91 for every approach and confidence; proposed as review-only; end to end on the real services |
| TC-E1-060-08-ITG | AC8, BR13 | Integration | Evaluation of "EXTRACT" on "EXTRACT-S1" version 1 already RUNNING; 409 with MSG-P10-003; end to end on the real services |
| TC-E1-060-09-ITG | AC12 | Integration | Synthetic user RW-CASEOWN calls the two evaluation operations; 403 with MSG-P4-002 in both; end to end on the real services |
| TC-ITG-E1060-ITG-10 | AC9, BR6, BR7 | Integration | 40 documents; one field read per document for OCR_TEMPLATE with no model call, one content read per document for each model approach as SY-AGENT; no document_field table read; end to end on the real services |
| TC-ITG-E1060-ITG-11 | AC10, BR8 | Contract | LOV-DOC-TYPE read through the P3 reference-data contract; a type list that differs from the sample types stops the run before any score row; end to end on the real services |
| TC-ITG-E1060-ITG-12 | AC11, BR10, BR11 | Integration | Each model approach run row holds policy "P1", prompt "PR1" and the model version; no field and no threshold in force changes; end to end on the real services |
| TC-ITG-E1060-ITG-13 | AC13, BR14 | NFR | Proposal export with Accept text/csv over the "EXTRACT-S1" run; personal-pattern scan over the CSV body and the score rows; labels compared by SHA-256 |
| TC-ITG-E1060-ITG-14 | AC14, BR10 | Integration | `document_field` values and the review threshold read through P5 before and after the shadow run; identical values and only P10 rows written; end to end on the real services |

TC-E1-060-01-ITG to TC-E1-060-09-ITG are the copies of the legacy test cases of RWB-E1-060, kept with their legacy IDs and given the `-ITG` suffix, one for each criterion AC1 to AC8 and AC12. TC-ITG-E1060-ITG-10 to -14 are new (D-RCV-60): 10 carries the field read against the content read of AC9, 11 the reference-data origin of the types of AC10, 12 the shadow versions of AC11, 13 the personal-data scan of the export of AC13, and 14 the no-change guarantee across P5 of AC14. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the two contract-shaped refusals and the type list become Contract, and the personal-data scan over the export is NFR.

### 17. Guardrails

- No business value in code or in the suite: the agent, the policy and prompt versions, the output schema, the approaches, the target precision, the sample floor, the tie order and the model version are the approved P10 rows, read through the contract at run time (BR12).
- No personal data in logs, scores, the proposal, the CSV export or the report: label values are held and compared as SHA-256 hashes, and every document of the run is synthetic (BR14).
- No read of another service's table and no schema client in the suite: the document, its fields and its content are read through P5, the scores and the proposal through P10, the types through P3 and the session through P4 (DP-01).
- The evaluation changes no `document_field` value and no review threshold in force: the run writes only P10 rows, and P5 is read before and after to prove it (BR10, ASM-0518).
- The model is reached only by P10 through its gateway client, and by the suite only through the recorded stub of the INT-23 OpenAPI 3.1 contract; a live model endpoint is never called from SIT.
- One hop and a 2 s client budget on every REST call; the model budget belongs to the P10 gateway client and is never a REST budget of the suite (ADR-020, DP-11).
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment.
- Clean-up in the same run: the sample version, the evaluation run and the seeded documents are removed or retired, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-005 | Classified with a confidence score; below the threshold goes to review | The proposal and its threshold through `GET /api/recovery/agent/v1/admin/agent-evaluations`, the review-only field, the P5 threshold read of AC14 | TC-E1-060-02-ITG, TC-E1-060-03-ITG, TC-E1-060-05-ITG, TC-E1-060-07-ITG, TC-ITG-E1060-ITG-14 |
| REQ-DCM-006 | Fields extracted for the agreed types | The three approaches, the score rows, the sample load and its refusal, the type list, the P5 field and content reads, the shadow versions, the export | TC-E1-060-01-ITG, TC-E1-060-04-ITG, TC-E1-060-06-ITG, TC-E1-060-08-ITG, TC-E1-060-09-ITG, TC-ITG-E1060-ITG-10, TC-ITG-E1060-ITG-11, TC-ITG-E1060-ITG-12, TC-ITG-E1060-ITG-13 |
| DP-01 | Owner's schema per service; no cross-service table read | `rwb_document` behind the P5 contract, `rwb_agent` behind the P10 contract, no schema client in the suite | TC-E1-060-01-ITG, TC-ITG-E1060-ITG-10, TC-ITG-E1060-ITG-14 |
| DP-06 | Parameters contract of rwb-case | The policy values the measurement is read against, read as the approved P10 parameter rows and never as code | TC-E1-060-02-ITG, TC-E1-060-05-ITG, TC-E1-060-07-ITG |
| DP-07 | Reference-data contract of rwb-case | `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-DOC-TYPE | TC-ITG-E1060-ITG-11 |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/agent/v1`, `/api/recovery/document/v1`, `/api/recovery/case/v1`, `/api/recovery/access/v1` | Every test case, at the preflight |
| DP-15 | Per-service Flyway and migration ownership | The proposal column of `V10_003__evaluation_proposal.sql` in `rwb_agent`; the suite owns no migration | TC-E1-060-02-ITG, TC-ITG-E1060-ITG-12 |
| DP-19 | Screen route through gateway-bff | No screen in this story; the admin reads and the CSV export stand in for the future evaluation screen | TC-ITG-E1060-ITG-13 |
| ASM-0514 | LOV-DOC-TYPE and the six document types are read through the P3 reference-data contract | `GET /api/recovery/case/v1/admin/lists/{listCode}` and the list version in force | TC-E1-060-03-ITG, TC-ITG-E1060-ITG-11 |
| ASM-0515 | P5 serves the document, its content and the stored fields to P10 and to the suite, never a table | `GET /documents/{documentId}`, `GET /documents/{documentId}/content`, `GET /cases/{caseId}/documents` | TC-E1-060-01-ITG, TC-E1-060-04-ITG, TC-E1-060-06-ITG, TC-ITG-E1060-ITG-10, TC-ITG-E1060-ITG-14 |
| ASM-0516 | All three approaches run inside P10 and the model is reached only through the recorded INT-23 stub | The INT-23 stub of section 12.8, the deterministic answer set and the timeout switch | TC-E1-060-01-ITG, TC-E1-060-04-ITG, TC-E1-060-05-ITG, TC-ITG-E1060-ITG-12 |
| ASM-0517 | The score rows and the proposal stay in P10, `V10_003` is a P10 migration, and the export goes through GET /admin/agent-evaluations | `GET /admin/agent-evaluations` with Accept text/csv, and the proposal column of the run | TC-E1-060-02-ITG, TC-E1-060-03-ITG, TC-E1-060-05-ITG, TC-E1-060-07-ITG, TC-ITG-E1060-ITG-13 |
| ASM-0518 | The target precision, the sample floor and the tie order stay agent_policy values, and no P5 threshold changes | The approved policy "P1" read through `GET /admin/agent-configs`, and the P5 threshold read of AC14 | TC-E1-060-02-ITG, TC-E1-060-05-ITG, TC-E1-060-07-ITG, TC-ITG-E1060-ITG-14 |
| RWB-E1-060 (legacy story) | Extraction evaluation [E1c]: the eight criteria AC1 to AC8 and the access test | The nine REST operations and the stub of section 12 | The fourteen test cases of section 16 |
| RWB-P10-E1060-APP (component copy) | The extraction evaluation inside rwb-agent: the four tables, the components, the proposal column and the four admin operations | The P10 contract itself | The fourteen test cases of section 16, run here on the real services |

The gap GAP-0370 records the area the sources leave open - the document-type reference-data owner, the extraction field reads and the proposal column - and every default it raises is settled by ASM-0514 to ASM-0518, each of which is a row above.

### 19. Out of scope

- The application builds this run depends on: RWB-P5-E1053-APP and RWB-P10-E1060-APP.
- The contract, database, operations and infrastructure stories of the legacy key, and the harness RWB-ITG-W1J01-ITG itself.
- Applying the chosen threshold to the review queue in P5 (RWB-E1-054): this story proposes the threshold and changes nothing in force.
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- Writing the architecture decision record that records the choice: it is signed outside the code, and this story delivers the proposal rows it is read from.
- The business run of an agent, `AgentRunWorkflow`, the agent runtime client and `rwb.agent.AgentRunCompleted.v1`, which belong to RWB-ITG-TE013-ITG and to the E1058 sibling.
- The monitoring dashboard and the cost alert (RWB-E1-063, RWB-E2-031), the review queue screen and the document screens.
- The non-functional epic RWB-ITG-NFR and the choice of model endpoint: the run reads the model version of the policy and never selects an endpoint.
