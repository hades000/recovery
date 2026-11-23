# RWB-ITG-E1050-ITG Document classification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1050-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-050 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP10, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E1050-APP, RWB-P3-E1050-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-050 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-050 classification step across P5 rwb-document (the intake item, the classification fields, the text) and P3 rwb-case (the case of the item and the access check), with the model call served by the P10 agent run on its own queue**, so that **each document is filed under the right type and a document below the threshold reaches a person, proved on the real services before wave 1 exits**.

### 2. Business rationale

The legacy story runs classifyStep inside JOB-12 and calls the classifier through the P10 model gateway. The target keeps document_intake and document_text in rwb_document under P5 rwb-document as their owner (Architecture v5 slides 16 and 41), runs the classify step inside DocumentIntakeWorkflow on the rwb-document task queue, and calls the classifier as a child run of P10 rwb-agent: AgentRunWorkflow runs on the rwb-agent task queue for 60 seconds and then returns the rule result (Architecture v5 slide 16). P5 reads its three parameters as data — CLASSIFY_THRESHOLD, CLASSIFY_MAX_PAGES and CLASSIFY_TIMEOUT_SECONDS — and stores the model version returned by the run on the intake item in classifier_version.

The legacy split for this key is therefore: P5 rwb-document owns the intake item, its classification fields, the text and the type table; P3 rwb-case owns the case of the item and the access decision that guards the read. This story is the integration proof across both owners and the agent run. The types, the threshold, the pages read and the timeout stay data and are never compiled in (DP-06, DP-07).

Where the sources do not name the route that serves the model call, the home of the three parameters in the target or the agent run evidence the pack may read, the suite asserts through the owners' contracts and records the open point as `Not specified in the source documents (GAP-0363; ASM-0479)`.

The legacy measures are kept unchanged: REQ-DCM-005 for the classified type and the confidence, FSD P5 A2.8 and A2.8.1 for the step and the fields extracted without review, and the 90 percent accuracy target on the labelled sample before the step is used in production (FEAT-AGT-04).

### 3. Preconditions

- RWB-P5-E1050-APP is done: the classification columns on document_intake, the classify step inside DocumentIntakeWorkflow and the evaluation runner are in SIT.
- RWB-P3-E1050-APP is done: the case of the item and the Documents right check are in SIT.
- The published contracts of P5 rwb-document and P3 rwb-case are deployed under their own per-service bases behind gateway-bff, and P10 rwb-agent publishes its own.
- P10 rwb-agent serves AgentRunWorkflow on task queue rwb-agent in namespace rwb-recovery, with the 60-second budget then the rule result (Architecture v5 slide 16).
- The document type table DOCTYPE-2026.11 is in force.
- CLASSIFY_THRESHOLD 0.80, CLASSIFY_MAX_PAGES 3 and CLASSIFY_TIMEOUT_SECONDS 60 are loaded as rows in the document hub parameter table; the three values are the legacy values and all three are assumed (GAP-0363; ASM-0480).
- The labelled sample of 180 synthetic documents, 30 per type, is in the harness RWB-ITG-W1J01-ITG, with the true type of each document.
- The classifier stub behind the agent run is available, returns fixed scores per file, and its model version is known.
- The feature flag `rwb.dochub.classify` is on.
- No production data is used and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a precondition of this story.
- The story has no build dependency: it is ready on Day 1 and waits only on its two integration dependencies.

### 4. Flow

1. QA integration engineer: seeds the labelled sample of 180 synthetic documents, 30 per type, through DocumentIntakeWorkflow on queue rwb-document, and waits until ocr_status is DONE and rwb.document.DocumentStored.v1 arrives for each stored file.
2. Harness: posts the five classifier cases — the low-confidence case, the at-threshold case, the silence case, the unknown-type case and the upload case — as fixed scores per file in the classifier stub behind the agent run.
3. Harness: lets the classify step of DocumentIntakeWorkflow run for each case, and waits for the child run of AgentRunWorkflow on queue rwb-agent and for rwb.agent.AgentRunCompleted.v1.
4. Harness: reads each intake item through GET /api/recovery/document/v1/intake-items/{intakeItemId} and asserts predicted_type, classification_confidence, type_candidates, review_reason, classify_fallback and classifier_version; reads the text sent for classification through the content path of the same item.
5. Harness: reads the type stored at attach through GET /api/recovery/document/v1/documents/{documentId}, and reads the document type table in force to prove the type returned by the run is one of the agreed types.
6. Harness: reads the agent runs of the sample through GET /api/recovery/agent/v1/admin/agent-runs and asserts one run per classification, the fixed model version and the 60-second budget of the run.
7. Harness: runs the labelled sample through the classify step and reads the evaluation report from the standard container: the accuracy, the 6 by 6 confusion matrix and the model version; asserts at least 162 of the 180 documents carry the labelled type.
8. Harness: reruns the step over the 20 classified items and asserts no new agent run is started and no result changed.
9. Harness: changes CLASSIFY_THRESHOLD to 0.90 as a data row and reruns one case; asserts review_reason LOW_CONFIDENCE and that no code or deployment changed between the two values.
10. Harness: reads the masked text received by the classifier stub, posts the access refusal by a role without the Documents right, reads the case of the item through GET /api/recovery/case/v1/cases/{caseId}, writes the evidence report and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The top score is below CLASSIFY_THRESHOLD | The item is marked LOW_CONFIDENCE with its two candidates and is passed to attach marked for type review | MSG-P5-003 | AC2 |
| X2 | The top score is exactly at CLASSIFY_THRESHOLD | The item is classified with no review_reason | None | AC3 |
| X3 | The classifier does not answer within CLASSIFY_TIMEOUT_SECONDS | The item goes to review with reason MODEL_UNAVAILABLE, holds no predicted_type and records the fallback | MSG-P5-003 | AC4 |
| X4 | The run returns a type code outside the type table in force | The item goes to review with reason UNKNOWN_TYPE and the two highest agreed types as its candidates | MSG-P5-003 | AC5 |
| X5 | The item already carries a type (an upload) | The classifier receives no call and the given type is kept | None | AC6 |
| X6 | The item is in RESCAN or FAILED | The classifier receives no call; the item stays as it is | None | AC7 |
| X7 | The step runs again over an item that already carries a classification | No second model call and no change of the result | None | AC8 |
| X8 | A role without the Documents right reads the classification | Refused with status 403 and the message; the case read is unchanged | MSG-P4-002 | AC11 |
| X9 | A consumed contract call exceeds the 2 s timeout or returns a server error | The step is retried under the run policy; the evidence report records the call and the response; no classification assertion is made on unverified data | None | AC1, AC5 |
| X10 | The synthetic fixture set does not match the harness RWB-ITG-W1J01-ITG expectations, or the classifier stub returns no fixed score for a file | The suite fails as a fixture or stub fault and names the file; no service defect is raised | None | AC1, AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the two APP stories and the published contracts of P5, P3 and P10, not their source code |
| Negotiable | The threshold, the pages read, the timeout and the fixed stub scores are data rows of the harness; the story fixes the assertions and the call set |
| Valuable | The classified type, the review routing and the agent run are proved on real services before wave 1 exits |
| Estimable | One suite module, one labelled fixture pack, one classifier stub with its silence control, one threshold clock and one evidence report |
| Small | Eleven scenarios over two services and one agent run; no service code and no schema change |
| Testable | Every scenario asserts a contract response, an agent run, a stored file in the standard container or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Document classification, end-to-end across the P5, P3 and P10 wave 1 services

  Background:
    Given the wave 1 services rwb-document, rwb-case and rwb-agent are deployed in SIT with their published contracts
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used
    Given document type table version "DOCTYPE-2026.11" is in force
    Given parameter CLASSIFY_THRESHOLD is 0.80
    Given CLASSIFY_MAX_PAGES is 3 and CLASSIFY_TIMEOUT_SECONDS is 60

  Scenario: AC1 Accuracy on the labelled sample through the agent run (new, D-RCV-60)
    Given the labelled sample of 180 synthetic documents, 30 of each type, with ocr_status "DONE"
    When the classify step runs on the sample and the model call is served by AgentRunWorkflow on queue rwb-agent
    Then at least 162 of the 180 documents get the labelled type as predicted_type on the intake item
    Then the report "evaluation/classification/2026-11-20.json" in the standard container holds the accuracy, the 6 by 6 confusion matrix and the model version

  Scenario: AC2 A low-confidence document is routed to review with its two candidates (new, D-RCV-60)
    Given a scanned intake item whose scores are COURT_NOTICE 0.62, DEMAND_LETTER 0.21 and the rest below 0.10
    When classification runs
    Then the item has predicted_type "COURT_NOTICE", classification_confidence 0.6200 and review_reason "LOW_CONFIDENCE"
    Then type_candidates holds COURT_NOTICE 0.62 and DEMAND_LETTER 0.21
    Then the system passes the item to attach marked for type review, with write_once to be set false on the stored document

  Scenario: AC3 A score exactly at the threshold is classified (new, D-RCV-60)
    Given a scanned intake item whose top score is APPRAISAL_REPORT 0.80
    When classification runs
    Then the system classifies the item as "APPRAISAL_REPORT" with no review_reason

  Scenario: AC4 A classifier that does not answer within 60 seconds falls back to review (new, D-RCV-60)
    Given the classifier stub behind the agent run does not answer within 60 seconds
    When classification runs for one item
    Then the item has review_reason "MODEL_UNAVAILABLE" and no predicted_type
    Then the item records that the fallback was used

  Scenario: AC5 A type outside the table in force goes to review (new, D-RCV-60)
    Given the classifier returns "LOAN_CONTRACT" 0.91 for an item
    When classification runs
    Then the item has review_reason "UNKNOWN_TYPE"
    Then type_candidates holds the two highest agreed types

  Scenario: AC6 An upload that already carries a type is not classified (new, D-RCV-60)
    Given an intake item created from an upload of type "TITLE_DEED"
    When classification runs
    Then the classifier receives no call for it and its type stays "TITLE_DEED"

  Scenario: AC7 An item waiting for rescan is not classified (new, D-RCV-60)
    Given an intake item with ocr_status "RESCAN"
    When classification runs
    Then the classifier receives no call for it

  Scenario: AC8 A repeat run over classified items calls nothing (new, D-RCV-60)
    Given 20 items already classified
    When the classify step runs again
    Then the classifier receives no call for those 20 items and their results are unchanged

  Scenario: AC9 The threshold is data and a change needs no deployment (new, D-RCV-60)
    Given parameter CLASSIFY_THRESHOLD is changed to 0.90 in the document hub parameter table
    Given a scanned item whose top score is COURT_NOTICE 0.85
    When classification runs
    Then the item has review_reason "LOW_CONFIDENCE"
    Then no code or deployment changed between the two values

  Scenario: AC10 Personal identifiers are masked before the model call (new, D-RCV-60)
    Given a scanned page holding the synthetic national ID number "0000000000000" and account number "TEST-ACC-0001"
    When classification runs
    Then the text received by the classifier stub holds tokens in place of both values

  Scenario: AC11 A role without the Documents right is refused (new, D-RCV-60)
    Given a user holds role RW-CAPACITY without the Documents right
    When the user reads the classification of a document of a case
    Then the service refuses the call with status 403 and MSG-P4-002
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is classified into one of the agreed types with a confidence score | REQ-DCM-005; FEAT-DCM-08; RWB-E1-050 BR1 |
| BR2 | Below the threshold the document goes to the review queue; the threshold is inclusive | REQ-DCM-005; CLASSIFY_THRESHOLD as a data row; DL11; RWB-E1-050 BR2 |
| BR3 | The types come from the type table in force and the threshold from the document hub parameter table | DL19; RWB-E1-050 BR3 |
| BR4 | A model that does not answer within the timeout falls back to review and the fallback is recorded | R-UNI-32; RWB-E1-050 BR4 |
| BR5 | Accuracy on the labelled sample is at least 90 percent before the step runs in production | FEAT-AGT-04; RWB-E1-050 BR5 |
| BR6 | Personal identifiers are masked before text leaves the document hub | CTL-11; DL26; DL33; RWB-E1-050 BR6 |
| BR7 | An item classified once is not classified again | R-UNI-40; RWB-E1-050 BR7 |
| BR8 | P5 rwb-document owns document_intake, document_text, document_type and document_hub_parameter, and the model call runs as a child run of P10 rwb-agent on queue rwb-agent with the 60-second budget then the rule result | Architecture v5 slide 16; Ownership Map; ASM-0479 |

### 9. State transitions

None for the case status: this story reads the case of the item and never changes it. It changes the classification state of the intake item, which belongs to P5 rwb-document.

| Object | State | Meaning |
|---|---|---|
| document_intake | OCR DONE | The item holds OCR text and no classification; the classify step may pick it up |
| document_intake | CLASSIFIED | The top score met the threshold, the type is in the table in force, and predicted_type, classification_confidence and classifier_version are set |
| document_intake | Review, LOW_CONFIDENCE | The top score was below the threshold; the two candidates are held and the item goes to a person |
| document_intake | Review, MODEL_UNAVAILABLE | The run did not answer within CLASSIFY_TIMEOUT_SECONDS; no predicted_type, and the fallback is recorded |
| document_intake | Review, UNKNOWN_TYPE | The run returned a type outside the table in force; the two highest agreed types are held as candidates |

The suite reads these states through the P5 contract and writes none of them itself.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| SY-OCR, document intake and OCR pipeline | Writes the intake item and its classification result (Documents CRU) |
| SY-AGENT, agent runtime | Serves the model call as a run on queue rwb-agent |
| RW-CASEOWN and roles with Documents R | Read the type and the confidence of documents in their scope |
| RW-COE, center of excellence analyst | Runs the evaluation and reads the report |
| RW-RISK, risk and model risk officer | Reviews the evaluation report before production use |

No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-063 | document_intake (P5 rwb-document) | ocr_status | Read |
| DF-DOC-070 | document_intake (P5 rwb-document) | predicted_type | Read |
| DF-DOC-071 | document_intake (P5 rwb-document) | classification_confidence | Read |
| DF-DOC-072 | document_intake (P5 rwb-document) | type_candidates | Read |
| DF-DOC-073 | document_intake (P5 rwb-document) | classifier_version | Read |
| DF-DOC-080 | document_intake (P5 rwb-document) | review_reason | Read |
| DF-DOC-074 | document_intake (P5 rwb-document) | classify_fallback | Read |
| DF-DOC-061 | document_intake (P5 rwb-document) | document_id | Read |
| DF-DOC-089 | document_text (P5 rwb-document) | text_content | Read |
| DF-REF-219 | document_type (P5 rwb-document) | doc_type_code | Read |
| DF-REF-246 | document_hub_parameter (P5 rwb-document) | param_value | Read |
| DF-DOC-004 | document (P5 rwb-document) | document_type | Read |
| Model route, parameter home and agent run evidence | Classification run, document hub parameters and the agent run | Route of the model call, home of the three classify parameters and the run evidence the suite may read | Not specified in the source documents (GAP-0363; ASM-0479) |

The legacy story marks the classification fields as writes; in this suite the write is performed by P5 rwb-document inside its own workflow and the suite only reads the result through the P5 contract (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/document/v1/intake-items/{intakeItemId} | P5 rwb-document | Read the predicted type, the confidence, the candidates, the review reason, the fallback and the classifier version |
| GET /api/recovery/document/v1/intake-items/{intakeItemId}/content | P5 rwb-document | Read the text of the pages sent for classification |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the document type stored at attach |
| GET /api/recovery/agent/v1/admin/agent-runs | P10 rwb-agent | Read the agent runs of the sample and their model version |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the case of the item and prove the access refusal |

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.agent.AgentRunCompleted.v1 | rwb.agent.events.v1 | P10 rwb-agent | The classify run finished; the suite reads the run and its model version before it asserts the item |
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | The synthetic document is stored; the suite waits for it before the classify step is asserted |

No event is produced by the suite.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Holds the classify step under test; the step selects, masks, calls and applies the threshold |
| AgentRunWorkflow | P10 rwb-agent | rwb-agent | Serves the model call as the classify run of the item: 60 seconds then the rule result |

The suite starts and observes the workflows through their published interfaces and asserts only through the contracts of section 12.2. No workflow, activity or the suite reads another service's schema.

#### 12.6 Schedules

None. JOB-12 Document intake is described as an event-started workflow with workers scaled by KEDA (Architecture v5 slide 44) and is owned by RWB-P5-E1049-APP; this suite starts the step through the published workflow interface and waits for no Schedule.

#### 12.7 Tables owned

None (DP-01). document_intake, document_text, document_type and document_hub_parameter are P5 tables, and the suite owns no table and never reads another service's schema.

#### 12.8 Contract fakes

| Stub | Use |
|---|---|
| Classifier stub behind the agent run | Returns fixed scores per file and one 60-second silence; the model version is fixed |
| Azurite Blob standard container | Holds the evaluation report and the synthetic file set |

No service contract is faked: every call in section 12.2 goes to the real SIT service.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 5 |
| Kafka | 0 | 2 |
| Temporal | 0 | 2 workflows (DocumentIntakeWorkflow, AgentRunWorkflow) |
| File | 0 | 1 standard container |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the eleven scenarios against SIT and holds no service code |
| Labelled sample fixture pack | Test data | The 180 synthetic documents, 30 per type, with the true type of each |
| Classifier stub and silence control | Stub control | Fixed scores per file, one 60-second silence, one fixed model version |
| Threshold clock control | Harness control | Changes CLASSIFY_THRESHOLD as a data row and restores the previous value after the scenario |
| Evidence report | Report | Records per scenario the item id, the agent run id, the contract responses, the accuracy, the messages and the model version |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | document_intake, document_text, document_type and document_hub_parameter stay in rwb_document under P5 rwb-document; the suite asserts through the P5 and P3 contracts only |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On the APP stories; the three classify values remain data rows and business parameters go through the P3 contract (ASM-0480) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories; the suite reads the document type table in force to prove the returned type is an agreed one |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-12 becomes DocumentIntakeWorkflow on queue rwb-document, and the classify step runs inside it; the suite observes the run through Temporal visibility |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The five consumed REST operations of section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P5-E1050-APP; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | No screen in this story; the review queue route is built with RWB-E1-054 |

The dependency-added column records the build dependency of the owning story. This story has no build dependency: an ITG story waits on no build of its own, and its I dependencies are the APP stories listed in the metadata table.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5, P3 and P10.
2. Build the labelled sample fixture pack: 180 synthetic documents, 30 per type, with the true type as a data row.
3. Add the classifier stub behind the agent run with fixed scores per file, one 60-second silence and one fixed model version.
4. Implement the eleven scenarios of section 7 in TC order and assert only through the contracts of section 12.2, the events of section 12.4 and Temporal visibility.
5. Add the skip cases — the upload with a given type, the item in RESCAN and the repeat run — and assert that no agent run is started.
6. Add the threshold clock control and the change to 0.90, and assert that no code and no deployment changed.
7. Add the masking assertion on the text the classifier stub receives, the evaluation report assertion and the access refusal with its status and message.
8. Write the evidence report with the item ids, the agent run ids, the accuracy, the confusion matrix, the model version and the messages; run the suite in SIT against the wave 1 release candidate and keep the report with the wave exit evidence.

Done when: all eleven test cases pass in SIT against the published wave 1 contracts, the evaluation report shows at least 162 of 180 correct, the evidence report is attached to the wave exit pack, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | The item is sent to the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | A role without the Documents right reads the classification | You cannot {action} here. Your role does not include it. |

The evaluation report line is `evaluation/classification/{runDate}.json` in the standard container, holding the accuracy, the 6 by 6 confusion matrix and the model version of the run.

The message IDs and wording are copied from RWB-E1-050. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. Items sent to review are listed on SCR-31 Document review queue, with the two candidate types and MSG-P5-003, when RWB-E1-054 is built; the suite asserts the review state through the P5 contract and does not render the screen. The evaluation report is read from the standard container by the center of excellence analyst.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-050-01-ITG | AC1 | Integration | Labelled sample of 180 synthetic documents, 30 per type; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-02-ITG | AC2 | Integration | Stub scores COURT_NOTICE 0.62, DEMAND_LETTER 0.21; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-03-ITG | AC3 | Integration | Stub score APPRAISAL_REPORT 0.80; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-04-ITG | AC4 | NFR | Stub with no answer for 60 seconds; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-05-ITG | AC5 | Integration | Stub returns LOAN_CONTRACT 0.91; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-06-ITG | AC6 | Integration | Upload of type TITLE_DEED; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-07-ITG | AC7 | Integration | Item in RESCAN; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-08-ITG | AC8 | Integration | 20 classified items; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-09-ITG | AC9 | Contract | Parameter CLASSIFY_THRESHOLD changed to 0.90, stub score COURT_NOTICE 0.85; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-10-ITG | AC10 | Component | Synthetic page with a national ID number and an account number; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-050-11-ITG | AC11 | Component | RW-CAPACITY holds no Documents right and reads the classification; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts; no numeric business values added |

The legacy full test text is in Recovery Workbench Test Cases v7.xlsx under the legacy test case id.

### 17. Guardrails

- No business value in code: the types, the threshold, the pages read and the timeout are data rows, not constants.
- No personal data in logs, events, evidence or fixtures: text is masked before the model call, prompts and responses are not logged, and every test document is synthetic.
- No cross-service table read: every assertion goes through the owner's contract and the suite owns no table.
- One hop and a 2 s timeout on every consumed call (ADR-020).
- The model endpoint is inside the SCB tenant and no document text leaves the bank (DL33).
- Synthetic data only; the harness RWB-ITG-W1J01-ITG loads the fixtures and no production data is read, copied or connected to.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | GET /api/recovery/document/v1/intake-items/{intakeItemId}; predicted_type, classification_confidence, type_candidates, review_reason; MSG-P5-003 | TC-E1-050-01-ITG to TC-E1-050-11-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed REST operations of section 12.2 | TC-E1-050-01-ITG, TC-E1-050-08-ITG, TC-E1-050-11-ITG |
| DP-01 | Owner's schema, never another service's tables | document_intake, document_text, document_type and document_hub_parameter stay in rwb_document; the suite asserts through contracts | All |
| DP-06 | Parameters as data through the contract | CLASSIFY_THRESHOLD, CLASSIFY_MAX_PAGES and CLASSIFY_TIMEOUT_SECONDS as rows; no deployment on a change | TC-E1-050-03-ITG, TC-E1-050-09-ITG |
| DP-10 | Temporal workflow replaces Quartz | DocumentIntakeWorkflow on queue rwb-document; the classify step inside it | TC-E1-050-01-ITG, TC-E1-050-08-ITG |
| ASM-0479 | The classify step runs inside DocumentIntakeWorkflow and calls the classifier as a child run of P10 rwb-agent on queue rwb-agent | AgentRunWorkflow, 60 seconds then the rule result; rwb.agent.AgentRunCompleted.v1 | TC-E1-050-01-ITG, TC-E1-050-04-ITG |
| ASM-0480 | The three classify values stay rows in the P5 document hub parameter table | CLASSIFY_THRESHOLD 0.80, CLASSIFY_MAX_PAGES 3, CLASSIFY_TIMEOUT_SECONDS 60 as data | TC-E1-050-03-ITG, TC-E1-050-09-ITG |
| ASM-0481 | The labelled sample stays 180 synthetic documents, 30 per type, and the report is written to the standard container | evaluation/classification/{runDate}.json; classifier_version on the item | TC-E1-050-01-ITG |

The legacy story is RWB-E1-050. The integration dependencies are RWB-P5-E1050-APP and RWB-P3-E1050-APP; the legacy AC1 to AC10 at component level belong to those stories, not to this one.

### 19. Out of scope

- The APP and OPS builds of P5 rwb-document and P3 rwb-case, and their unit and component tests.
- The CON story RWB-P5-E1050-CON.
- The legacy AC1 to AC10 at component level, which the sibling APP stories own.
- The review queue screen and the correction fed back to the labelled set (RWB-E1-054).
- Field extraction and its evaluation (RWB-E1-053, RWB-E1-060).
- Attach to the case (RWB-E1-032).
- Stage 2 and 3 document types (RWB-E2-025).
- The P10 agent runtime build.
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing.
