# RWB-P10-E1060-APP Extraction evaluation [E1c]

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1060-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-060 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP13, DP15, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP (build dependency not done yet; start waits for its completion) |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E1058-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-013) |
| Status | Draft (directive resolutions) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P10-E1060-APP-14) |
| Size | Not specified in the source documents (DOR-RWB-P10-E1060-APP-16); the squad sizes it |
| Contract fake published | Not specified in the source documents (DOR-RWB-P10-E1060-APP-22) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-060 for rwb-agent. The behaviour of the legacy story is unchanged; the four evaluation tables move into schema `rwb_agent` (DP-01), the three admin operations move to the base `/api/recovery/agent/v1` (DP-13), the proposal column arrives with the service's own migration `V10_003__evaluation_proposal.sql` (DP-15), the document and its stored fields are read through the rwb-document contract instead of an in-process call (DP-11 behind DP-01), the document types are read from the rwb-case reference-data contract (DP-07), the measurement values are read from the approved policy row through the parameters contract (DP-06), and the admin reads are reached through the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E1060-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 5 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **centre of excellence analyst (RW-COE)**, I want **the extraction evaluation built inside rwb-agent - the four evaluation tables in schema `rwb_agent`, the three approaches scored field by field, the score rows and the proposal per document type, the migration that adds the proposal column and the three admin operations on the base `/api/recovery/agent/v1`, reading the documents and their stored fields through the rwb-document contract, the document types through the rwb-case reference-data contract and the right through rwb-access**, so that **field extraction for the six document types is scored against the labelled sample for the three approaches (OCR template, model, and OCR checked by the model) and the approach and the confidence threshold for each document type are chosen on measured precision and recall, on the same values the legacy story fixed, before wave 1 exits**.

### 2. Business rationale

Fields read wrongly from a court notice or a title deed send a case down the wrong step, and fields sent to review without need take officer time. The legacy story measured the three approaches on the same reviewed documents, field by field, and proposed for each document type the approach and the confidence threshold below which a field goes to the review queue. It served REQ-DCM-006 (fields extracted for the agreed types) and REQ-DCM-005 (a confidence score and a review queue below the threshold).

In the legacy delivery the sample, the shadow runs, the scorer, the proposal and the stored OCR fields sat in one module and one schema, the document was read through an in-process `DocumentQueryService`, the document types were taken from a list held beside the code, and the proposal was a column on the evaluation run row written by the same deployment. The behaviour is unchanged, so the disposition is Moved (no impact). What changes is where each fact lives and how it is reached:

- The documents, their content and the stored `document_field` values with their confidence are P5 rwb-document, schema `rwb_document`, and are read only through the P5 contract, as the service identity SY-AGENT (DP-01; BR7).
- The sample, the shadow runs, the score rows and the proposal are P10 rwb-agent, schema `rwb_agent`, and this story builds them as the four tables agent_sample, agent_run, agent_evaluation_run and agent_evaluation (DP-01; BR10).
- The document types and LOV-DOC-TYPE are P3 rwb-case reference data and are read through the reference-data contract; the legacy route that named P4 is dropped (DP-07; BR9).
- The target precision, the minimum labelled documents per type and the tie order stay values of the approved agent_policy row EXTRACT version "P1", read at run time through the parameters contract and never written in code (DP-06; BR8).
- The three admin operations are served on the base `/api/recovery/agent/v1` of rwb-agent, and the legacy monolith base is retired for them (DP-13; AC9).
- The proposal column is added by the service's own Flyway sequence, in its own schema (DP-15; AC11).
- RW-COE and RW-RISK reach the reads through the gateway-bff route, which is the only route a screen will use (DP-19; AC14).

The cross-service behaviour of this key - that the stored-field read and the content read are two different operations of the owner, that the three approaches are comparable on one sample, and that the shadow run changes nothing in force across the P5 boundary - is proved by RWB-ITG-E1060-ITG, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes, and it owns the eight legacy acceptance criteria AC1 to AC8 and adds six of its own for the service change.

### 3. Preconditions

- RWB-P10-E1058-APP is done: the agent platform, the orchestrator, the model gateway client, the prompt and policy store and the admin configuration operations exist in rwb-agent, agent "EXTRACT" exists, and a business run can be made in mode SHADOW.
- RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-E1044-CON are published: the parameters client library, the reference-data client library and the per-service Flyway sequence with parameterized schema names. RWB-PLT-N001-CON is published: the gateway-bff route contract and its stub.
- The `rwb_agent` schema baseline exists with the standard record columns and the Flyway history table of the service; the four evaluation tables of this story are created by its own migrations.
- The rwb-document contract is published and versioned: `GET /api/recovery/document/v1/documents/{documentId}` returns the document and its stored `document_field` values with their confidence, and `GET /api/recovery/document/v1/documents/{documentId}/content` returns the content. This story builds against that contract and its fake and never reads `rwb_document`.
- The rwb-case contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the parameters contract for the policy values and `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-DOC-TYPE.
- The rwb-access contract is available for the right check: `POST /api/recovery/access/v1/authorise` granting Rules and parameters C to RW-COE and R to RW-RISK and refusing a role without the right.
- Agent "EXTRACT" has policy version "P1" approved (mode SHADOW, allowed tools read_document_content and read_document_fields, output schema "extract-fields-v1") and prompt version "PR1" approved, both loaded through the configuration operations of RWB-P10-E1058-APP.
- Policy version "P1" holds the target precision 0.95, the minimum labelled documents per type 30 and the tie order OCR_TEMPLATE before OCR_AND_MODEL before MODEL (legacy values; the legacy story marks the first two as assumed at DL19 and DL11).
- The six document types and LOV-DOC-TYPE are in force in rwb-case and are read through the reference-data contract (ASM-1048).
- Labelled sample "EXTRACT-S1" version 1 is loaded through this story's sample operation: 40 court notices of type "COURT_NOTICE" with labels for court_name, case_number and hearing_date, and 12 documents of type "TITLE_DEED"; personal label values are held as SHA-256 hashes.
- The service identity SY-AGENT holds Documents R on rwb-document, so the field read and the content read are answered under the same role check as a person. SY-OCR produced the stored fields earlier through the P5 intake workflow and is not called by this story.
- RW-COE holds Rules and parameters C and RW-RISK holds Rules and parameters A; the refusals of MSG-P4-002 are proved through the rwb-access contract fake.
- The login of this service is the rwb-agent login (DP-02; GAP-0644; ASM-0869).
- The release date 30 November 2026 is tentative and is copied unchanged.
- Open decisions DL10, DL11 and DL19 carry their assumptions: DL10 on ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL11 on ASM-0553, ASM-0703, ASM-1051 and ASM-1104; DL19 on ASM-1051, ASM-1164, ASM-1809 and ASM-1810. The programme directive confirms every assumption, so each decision stands on its assumed value.

### 4. Flow

1. RW-COE uploads sample "EXTRACT-S1" version 1 through `POST /api/recovery/agent/v1/admin/agent-samples`: one row per document and field, subject_type DOCUMENT, subject_id, label_key and expected_value, with the personal label values hashed (BR1, BR11).
2. SampleRowValidator checks every row before any row is stored: the document ID is read through `GET /api/recovery/document/v1/documents/{documentId}` and the document type is read through `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-DOC-TYPE. One bad row refuses the whole file with 422 and MSG-P10-001, and the sample version in force is unchanged (BR9; AC6, AC13).
3. A load that passes is stored as a new sample version in agent_sample in `rwb_agent`, and the operation answers 201 with the sample code and version.
4. RW-COE starts the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations` with agent "EXTRACT", sampleCode "EXTRACT-S1", sampleVersion 1 and the approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL; the answer is 202 with the evaluation run in status RUNNING (AC8).
5. The start is refused with 422 and MSG-P10-002 when the sample holds no labelled rows for the agent, and with 409 and MSG-P10-003 when an evaluation of the same agent on the same sample version is already RUNNING. In both cases no run row and no score row is written (AC8; legacy section 9).
6. The run reads its inputs: the approved policy version "P1", its prompt version "PR1", the target precision 0.95, the minimum labelled documents 30 and the tie order come through the parameters contract and the approved policy row, never from code (BR8; AC12).
7. For OCR_TEMPLATE the runner reads the stored `document_field` values and their confidence through `GET /api/recovery/document/v1/documents/{documentId}` and makes no model call (BR6; AC1).
8. For MODEL the runner reads the content through `GET /api/recovery/document/v1/documents/{documentId}/content` as SY-AGENT, calls agent "EXTRACT" in shadow through the agent platform of RWB-P10-E1058-APP and takes the fields from its answer; the run row records the model version and the prompt version "PR1" (AC1, AC4).
9. For OCR_AND_MODEL the runner passes the stored OCR fields with the content to agent "EXTRACT" and takes its checked values, again in shadow with the model version and "PR1" on the run row (AC1).
10. FieldMatchScorer compares each value with the label - trim and case folding for text, dates as dates, personal values by SHA-256 - and writes one agent_evaluation row per field and approach with sample_size, true_positive, false_positive, false_negative, precision_value and recall_value at four decimals (BR1, BR2; AC1).
11. A time-out or a guardrail failure on one document counts every labelled field of that document as a false negative for the model approach and raises the failure count on the run, TIMED_OUT 1 for document 7 of 40 (AC4).
12. ExtractionProposalBuilder builds the proposal in one `rwb_agent` transaction: for each document type it names the approach with the highest mean F1, its precision and recall per field and the lowest confidence at which every chosen field reaches precision 0.95; a type under the sample floor is marked "insufficient sample" and gets no approach and no threshold; a field that never reaches the target is marked review-only; a tie goes to the approach with fewer model calls (AC2, AC3, AC5, AC7).
13. The run moves RUNNING to DONE with finished_at, the failure counts and the proposal, and each score row and the proposal row are readable through the service and only through it (section 9).
14. RW-COE reads the result through `GET /api/recovery/agent/v1/admin/agent-evaluations` with query agent, from and to, and exports it with Accept text/csv, which returns the proposal rows, one row per document type, with no personal value in it (AC2; section 15).
15. Both reads reach the service through the gateway-bff route in front of the admin path, one hop each, so a screen never calls rwb-agent directly (DP-19; AC14).
16. The run changes no `document_field` value and no review threshold in force: it writes only the four tables of `rwb_agent` (BR6, BR10; section 17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A document type has fewer than 30 labeled documents | The type is scored and marked "insufficient sample"; no approach is proposed for it | None to a user | AC3 |
| X2 | The model times out or fails a guardrail on a document | The MODEL value counts as empty (false negative); the failure is counted on the run | None to a user | AC4 |
| X3 | Two approaches have the same F1 for a type | The approach with fewer model calls is proposed (OCR_TEMPLATE before OCR_AND_MODEL before MODEL) | None to a user | AC5 |
| X4 | A sample row names a document or field that does not exist | The sample load is refused in full | MSG-P10-001 | AC6 |
| X5 | No approach reaches precision 0.95 on a field at any confidence | The field is proposed as review-only | None to a user | AC7 |
| X6 | Evaluation started while the same one is running | Refused with 409 | MSG-P10-003 | AC8 |
| X7 | A role without the right | Refused with 403 | MSG-P4-002 | AC15, TC-E1-060-09, TC-E1-060-17 |
| X8 | The rwb-document contract does not answer inside the 2 s budget, or answers for a document the sample does not name | The read is counted as a failed read of the run, no score row is written for the documents that could not be read, and the run ends FAILED; RW-COE starts it again | None to a user | AC10, AC18 |
| X9 | A sample row names a type that is not in LOV-DOC-TYPE in force | The sample load is refused in full with the same check as X4, and no row of the file is stored | MSG-P10-001 | AC13 |
| X10 | The approved policy row holds no value for the target precision, the sample floor or the tie order | The proposal is not built, the missing policy value is named on the run, and no value in code is used as a default | None to a user | AC12 |
| X11 | The migration `V<next>__evaluation_proposal.sql` fails in the service's Flyway sequence | The new version does not start and the version in force keeps serving; no run row is created | None | AC11 |

X1 to X7 are the legacy exception paths of RWB-E1-060 carried onto the service; X8 to X11 are the failures that appear when the read leaves the service and when the schema and the policy row become the service's own responsibility. X7 is reached by criterion AC15 and proved by the access test case TC-E1-060-09 and by RWB-ITG-E1060-ITG across services, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the platform contracts and the published P5, P3 and P4 contracts with their fakes; it waits only for the in-lane story RWB-P10-E1058-APP and owns its own schema objects |
| Negotiable | The package layout, the component names, the export column order and the poll of the read are design; the agent, the policy and prompt versions, the approaches, the sample, the fields, the target precision, the sample floor, the counts and the message IDs are fixed by the legacy story |
| Valuable | Sets the review threshold that decides how many documents an officer checks by hand, on measured precision and recall per field and approach |
| Estimable | Four tables, one migration, three admin operations, five components, three contract clients and access guard |
| Small | Under two weeks with one developer and its tests, as in the legacy estimate |
| Testable | Each of the fourteen criteria of section 7 is one automated test on an observable: a REST answer, a stored row, a proposal field, a failure count, a migration record or a scan of the source |

### 7. Acceptance criteria

```gherkin
Feature: Extraction evaluation [E1c]

  Background:
    Given sample "EXTRACT-S1" version 1 holds 40 court notices of type "COURT_NOTICE" with labels for fields court_name, case_number and hearing_date
    Given the target precision is 0.95 and the minimum labeled documents per type is 30
    Given agent "EXTRACT" has policy version "P1" approved in mode SHADOW with prompt version "PR1" and output schema "extract-fields-v1"

  Scenario: AC1 Scores per field (legacy RWB-E1-060 AC1)
    Given the rwb-document contract mock returns the stored document_field values with their confidence for the 40 "COURT_NOTICE" documents
    Given the labeled sample
    When the three approaches run
    Then one score row exists per field and approach: 3 fields x 3 approaches for "COURT_NOTICE"
    Then for field hearing_date with approach OCR_TEMPLATE, 34 true positives, 2 false positives and 4 false negatives give precision 0.9444 and recall 0.8947
    Then each score row holds the model version and the prompt version "PR1" where the approach calls the model

  Scenario: AC2 Decision recorded (legacy RWB-E1-060 AC2)
    Given the rwb-document contract mock returns the stored document_field values with their confidence for the 40 "COURT_NOTICE" documents
    Given the scores for "COURT_NOTICE"
    When the proposal is built
    Then the evaluation run names, for "COURT_NOTICE", the approach with the highest mean F1 and its precision and recall per field
    Then it names the proposed confidence threshold: the lowest confidence at which every chosen field reaches precision 0.95
    Then the export lists one row per document type for the solution architect's architecture decision

  Scenario: AC3 A type with too few labels (legacy RWB-E1-060 AC3)
    Given the rwb-document contract mock returns the stored document_field values with their confidence for the 12 "TITLE_DEED" documents
    Given type "TITLE_DEED" has 12 labeled documents
    When the evaluation runs
    Then the system scores "TITLE_DEED" and marked "insufficient sample"
    Then no approach and no threshold are proposed for "TITLE_DEED"

  Scenario: AC4 A model failure counts against the model approaches (legacy RWB-E1-060 AC4)
    Given the rwb-document contract mock returns the content of the 40 "COURT_NOTICE" documents, including document 7
    Given the model stub times out on document 7 of 40
    When the approach MODEL runs
    Then each labeled field of document 7 counts as a false negative for MODEL
    Then the evaluation run holds failure count TIMED_OUT 1

  Scenario: AC5 Equal F1 (legacy RWB-E1-060 AC5)
    Given OCR_TEMPLATE and OCR_AND_MODEL both have mean F1 0.9310 for "COURT_NOTICE"
    When the proposal is built
    Then the system proposes OCR_TEMPLATE

  Scenario: AC6 A sample row for a document that does not exist (legacy RWB-E1-060 AC6)
    Given the rwb-document contract mock returns no document for the document ID named by the sample row under test
    Given the sample file has a row for a document ID that the P5 interface does not return
    When RW-COE loads the file
    Then the system refuses the load with 422 and MSG-P10-001 naming the row number
    Then the system stores no row of the file

  Scenario: AC7 A field that never reaches the target (legacy RWB-E1-060 AC7)
    Given the rwb-document contract mock returns the stored document_field values with their confidence for the 40 "COURT_NOTICE" documents
    Given field case_number reaches at most precision 0.91 for every approach and confidence
    When the proposal is built
    Then the system proposes case_number as review-only for "COURT_NOTICE"

  Scenario: AC8 The same evaluation twice (legacy RWB-E1-060 AC8)
    Given the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 is running
    When RW-COE starts it again
    Then the system refuses the request with 409 and MSG-P10-003

  Scenario: AC9 The admin operations answer on the agent base (new, D-RCV-60)
    Given rwb-agent is deployed with the four evaluation tables in schema "rwb_agent"
    When RW-COE calls POST /api/recovery/agent/v1/admin/agent-samples, POST /api/recovery/agent/v1/admin/agent-evaluations and GET /api/recovery/agent/v1/admin/agent-evaluations
    Then the three operations answer on the base /api/recovery/agent/v1 with 201, 202 and 200
    Then GET on the same path with Accept text/csv returns the proposal rows, one row per document type
    Then no one of the three operations is served on the legacy monolith base

  Scenario: AC10 The evaluation writes four tables in its own schema and reads no other (new, D-RCV-60)
    Given rwb-agent runs with its own login on schema "rwb_agent"
    When the sample load and the evaluation run complete
    Then the rows are written to agent_sample, agent_run, agent_evaluation_run and agent_evaluation in "rwb_agent" only
    Then the service makes no query against another schema and holds no foreign key across services
    Then the document, its content and its stored fields are read through the rwb-document contract and the document types through the rwb-case reference-data contract
    Then a pipeline scan finds no table name of another service in the rwb-agent sources

  Scenario: AC11 The proposal column arrives with the service's own migration (new, D-RCV-60)
    Given rwb-agent starts against an empty "rwb_agent" schema
    When the Flyway sequence of rwb-agent runs
    Then V<next>__evaluation_proposal.sql applies in order after the earlier P10 migrations
    Then agent_evaluation_run holds the column proposal, type jsonb, in "rwb_agent"
    Then no other schema is touched and no manual step is needed

  Scenario: AC12 The target precision, the sample floor and the tie order are read, not coded (new, D-RCV-60)
    Given policy version "P1" of agent "EXTRACT" holds the target precision 0.95, the minimum labeled documents 30 and the tie order OCR_TEMPLATE before OCR_AND_MODEL before MODEL
    When the proposal is built for "COURT_NOTICE"
    Then the three values are read through the parameters contract of rwb-case and the approved policy row at run time
    Then a pipeline scan finds no 0.95, no 30 and no tie order in the rwb-agent source
    Then an approved policy version with other values changes the proposal with no rebuild

  Scenario: AC13 The document types come from the reference-data contract of rwb-case (new, D-RCV-60)
    Given the six document types and LOV-DOC-TYPE are in force in rwb-case and are read through the rwb-case contract mock
    When RW-COE loads sample "EXTRACT-S1" version 1 and starts the evaluation
    Then the types are read through GET /api/recovery/case/v1/admin/lists/{listCode}
    Then a row whose type is not in the list in force is refused at the load and gets no score row and no proposal
    Then no reference row of rwb-case is read as a table

  Scenario: AC14 The admin reads are reached through the gateway-bff route (new, D-RCV-60)
    Given the gateway-bff route stub serves the admin operations of rwb-agent
    When RW-COE reads GET /api/recovery/agent/v1/admin/agent-evaluations through the route with Accept text/csv
    Then the route makes one hop to rwb-agent and returns the response unchanged
    Then no screen calls rwb-agent directly and the agent monitor screen SCR-46 is not changed by this story

  Scenario: AC15 A role without the right is refused (new, D-RCV-60)
    Given the rwb-access contract refuses a role without the right
    When RW-CASEOWN calls POST /api/recovery/agent/v1/admin/agent-evaluations
    Then the system refuses the request with 403 and MSG-P4-002

  Scenario: AC16 The approaches read the stored fields or call the model as the rule states (new, D-RCV-60)
    Given agent "EXTRACT" has policy version "P1" approved in mode SHADOW with prompt version "PR1"
    When the three approaches run on the labeled sample "EXTRACT-S1" version 1
    Then OCR_TEMPLATE reads the stored fields only and makes no model call
    Then MODEL and OCR_AND_MODEL call agent "EXTRACT" in shadow under policy "P1" with prompt "PR1"

  Scenario: AC17 The admin operations answer 401, 403 and 404 on their error paths (new, D-RCV-60)
    Given rwb-agent is deployed with the three admin operations on the base /api/recovery/agent/v1
    When a caller calls POST /api/recovery/agent/v1/admin/agent-samples, POST /api/recovery/agent/v1/admin/agent-evaluations or GET /api/recovery/agent/v1/admin/agent-evaluations without a valid login, without the right, or for a resource that does not exist
    Then the operation answers 401 when the caller is not authenticated
    Then the operation answers 403 when the caller holds no right
    Then the operation answers 404 when the named resource does not exist

  Scenario: AC18 A consumed contract that does not answer inside its budget fails the run (new, D-RCV-60)
    Given the rwb-document contract mock does not answer inside the 2 s budget
    When the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 reads a document through the rwb-document contract
    Then the read is counted as a failed read of the run
    Then no score row is written for the documents that could not be read
    Then the evaluation run ends FAILED
```

**Target reading.** The agent, its policy and prompt versions, the output schema, the three approaches, the sample, the three fields of the measurement, the target precision, the sample floor, the counts, the tie rule and the message IDs are the legacy values of RWB-E1-060, copied character for character; the scenario lines of AC1 to AC8 keep their legacy titles and every legacy Given, When and Then, and each one carries the origin tag of its legacy criterion. Six of the eight carry one inserted line as their first Given, `Given the rwb-document contract mock returns ...`, because the legacy criterion reads a document, its content or its stored fields across the P5 boundary: AC1, AC2, AC3 and AC7 read the stored fields and their confidence, AC4 reads the content, and AC6 reads a document that the contract does not return. AC5 and AC8 need none: AC5 asserts only the tie rule on given F1 values and AC8 only the refusal of a second start while the first run is RUNNING. The in-process `DocumentQueryService.getFields` and `getContent` of the legacy section 12 become the two operations of the rwb-document contract behind one hop and a 2 s client budget (DP-11 behind DP-01), so a score row of this story is built from a value the owner served and not from a table read. The four tables are P10's own, in `rwb_agent` (DP-01); the proposal column is added by P10's own migration `V<next>__evaluation_proposal.sql` in its own Flyway sequence (DP-15); the base of the three operations is `/api/recovery/agent/v1` (DP-13); the document types come from the rwb-case reference-data contract instead of the list the legacy section 13 named (DP-07, ASM-1048); the target precision, the sample floor and the tie order are read from the approved policy row through the parameters contract and appear nowhere in the source (DP-06, ASM-1051); and the reads are reached through the gateway-bff route (DP-19). The exact admin operation set of this story is the three legacy operations, and the evaluation report operation and the configuration operations stay with RWB-P10-E1058-APP (ASM-1049). The score rows and the proposal are read only through the evaluation read GET /api/recovery/agent/v1/admin/agent-evaluations; the promotion flag of the legacy RWB-E1-061 is not read by this story; and the three approaches are proved on the recorded model stub as set out in ASM-B-ITG-W1-08-E1060-1 to -5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A value is a true positive when it equals the label after trim and case folding; dates compare as dates; personal fields compare by SHA-256 hash | agent_sample.expected_value (DF-AGT-068); CTL-11; legacy BR1 |
| BR2 | Precision = TP / (TP + FP); recall = TP / (TP + FN); F1 = 2PR / (P + R); 4 decimals | agent_evaluation (DF-AGT-091 to DF-AGT-096); legacy BR2 |
| BR3 | A type with fewer labeled documents than the minimum (30, the approved policy value read through the parameters contract, ASM-1051; DL19) gets no proposal | agent_policy row EXTRACT (DF-AGT-001 to DF-AGT-025, read through the parameters contract); legacy BR3 |
| BR4 | The proposed threshold is the lowest confidence where precision reaches the target (0.95, assumed; DL11); a field that never reaches it is review-only | REQ-DCM-005; document_field.confidence (DF-DOC-016); legacy BR4 |
| BR5 | Ties go to the approach with fewer model calls: OCR_TEMPLATE before OCR_AND_MODEL before MODEL | agent_policy row EXTRACT (DF-AGT-001 to DF-AGT-025, read through the parameters contract); legacy BR5 |
| BR6 | The OCR_TEMPLATE approach reads stored fields only and makes no model call; MODEL and OCR_AND_MODEL call agent "EXTRACT" in shadow under policy "P1" with prompt "PR1" | DT06; legacy BR6; agent_run (DF-AGT-036 to DF-AGT-057) |
| BR7 | rwb-agent reads no table of another service: the document, its content and the stored fields come through the rwb-document contract as SY-AGENT, and no foreign key crosses a schema | DP-01; DP-11; Arch v5 slide 16 |
| BR8 | The target precision, the minimum labelled documents and the tie order are values of the approved policy row, read through the parameters contract at run time; a code default is a defect, and a missing value stops the proposal | DP-06; Principle 1; FSD P10 v3 BR-P10-004 |
| BR9 | The document types and LOV-DOC-TYPE are read from the rwb-case reference-data contract, and a type outside the list in force is refused at the sample load and never scored | DP-07; ASM-1048 |
| BR10 | The story writes four tables only - agent_sample, agent_run, agent_evaluation_run and agent_evaluation - all in `rwb_agent`, and adds the proposal column by its own migration `V<next>__evaluation_proposal.sql` in its own Flyway sequence | DP-01; DP-15; Ownership Map (P10 owns the four tables) |

### 9. State transitions

The state transitions of an evaluation run:

| From | Event | Condition | To |
|---|---|---|---|
| None | Evaluation started through `POST /admin/agent-evaluations` | The sample has labelled rows and no run for the same agent and sample version is RUNNING | RUNNING (agent_evaluation_run.status, DF-AGT-077) |
| None | Evaluation started | The sample has no labelled rows for the agent | No row; 422 MSG-P10-002 |
| None | Evaluation started | One for the same agent and sample version is RUNNING | No row; 409 MSG-P10-003 |
| RUNNING | Last sample row scored and the proposal written | None | DONE with finished_at (DF-AGT-079) and the proposal (DF-AGT-084) |
| RUNNING | A document read through the P5 contract fails for a document the sample names | None | FAILED; no score row for the documents that could not be read |

The state of each score row and of the proposal:

| From | Event | Condition | To |
|---|---|---|---|
| None | A field scored for an approach | A labelled value compared with the approach value | One row per field and approach with TP, FP, FN, sample_size, precision and recall |
| None | A type proposed | The type reaches the sample floor of 30 and an approach reaches the target | Proposal row with the approach, the per-field precision and recall and the threshold |
| None | A type proposed | The type is under the sample floor | Marked "insufficient sample", no approach and no threshold |
| None | A field proposed | The field never reaches precision 0.95 at any confidence | Field marked review-only |

No case state transition. This story does not change a case status and touches no case of record. It writes one evaluation run (RUNNING to DONE or FAILED) and its score rows and proposal in `rwb_agent`. The threshold it proposes takes effect only when P5 loads it as a new reference data version, which is RWB-E1-054 and is out of scope here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, centre of excellence analyst | Loads the sample, starts the evaluation, reads and exports the results (Rules and parameters C) |
| RW-RISK, risk and model risk officer | Approves the policy and prompt versions and reads the results (Rules and parameters A and R) |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the evaluation, writes the four tables in `rwb_agent`, reads the P5 and P3 contracts and calls the agent in shadow |
| SY-AGENT, agent platform | Reads the document content and the stored fields through the rwb-document contract (Documents R) |
| SY-OCR | Produced the stored OCR fields earlier through the P5 intake workflow; not called here |
| rwb-access (P4) | Answers the right check `POST /api/recovery/access/v1/authorise` and refuses a role without the right with MSG-P4-002 |
| No role | Reads `rwb_document`, `rwb_case` or any other service's schema, changes a `document_field` value, changes a threshold in force, or reads production data |

The login of the service is the rwb-agent login (DP-02; GAP-0644). Approval levels: no delegation of authority level applies; the approval of the policy and prompt versions is the Rules and parameters A right, as in the legacy story.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-061 to DF-AGT-069 | agent_sample | id, agent_code, sample_code, sample_version, subject_type, subject_id, label_key, expected_value, labeled_by | Write, and read back as counts; personal label values are held as SHA-256 hashes |
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at, evaluation_run_id | Write for the shadow runs of the model approaches |
| DF-AGT-070 to DF-AGT-083 | agent_evaluation_run | id, agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, started_at, finished_at, requested_by, total_cost_thb, p95_latency_ms, failure_counts | Write |
| DF-AGT-084 | agent_evaluation_run | proposal | Write, in the column added by `V10_003__evaluation_proposal.sql` |
| DF-AGT-087 to DF-AGT-096 | agent_evaluation | evaluation_run_id, approach, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Write |
| DF-DOC-001 | document | id | Read through the rwb-document contract |
| DF-DOC-004 | document | document_type | Read through the rwb-document contract |
| DF-DOC-006 | document | storage_ref | Read through the rwb-document contract (the content operation) |
| DF-DOC-013 | document_field | document_id | Read through the rwb-document contract |
| DF-DOC-014 | document_field | field_name | Read through the rwb-document contract |
| DF-DOC-015 | document_field | field_value | Read through the rwb-document contract |
| DF-DOC-016 | document_field | confidence | Read through the rwb-document contract |
| DF-DOC-017 | document_field | confirmed_by | Read through the rwb-document contract, as a count of confirmed labels; no person is named |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value (rwb_case, owner P3) | the target precision, the minimum labelled documents and the tie order of the approved policy row, with their versions in force | Read through the parameters contract |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case, owner P3) | the six document types and LOV-DOC-TYPE with the version in force | Read through the reference-data contract |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E1-060. document, document_field and document_text are the P5 tables of schema `rwb_document`; agent_sample, agent_run, agent_evaluation_run and agent_evaluation are the P10 tables of schema `rwb_agent` in the Ownership Map. No field of agent_alert, agent_feedback, agent_prompt or agent_policy is written here: the policy and prompt versions are read as versions through the operations of RWB-P10-E1058-APP. Every read of another service's data in this table goes through that service's contract and never through its table.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

Contract version: this story builds against version 5.0.0 of the OpenAPI documents in Recovery Workbench API Specification v5, both for the operations it provides (`rwb-agent.yaml`) and for the contracts it consumes.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/admin/agent-samples` | Load a labelled evaluation sample for an agent: multipart file (CSV with subject_type DOCUMENT, subject_id, label_key and expected_value), agent "EXTRACT", sampleCode; 201 AgentSample; each load is a new sample version | Rules and parameters C, scope applied | Idempotency-Key header |
| POST | `/admin/agent-evaluations` | Start the extraction evaluation for an agent on a labelled sample: AgentEvaluationRequest with agent "EXTRACT", sampleCode "EXTRACT-S1", sampleVersion 1 and approaches ["OCR_TEMPLATE", "MODEL", "OCR_AND_MODEL"]; 202 AgentEvaluationRun; one RUNNING run per agent and sample version | Rules and parameters C, scope applied | Idempotency-Key header |
| GET | `/admin/agent-evaluations` | List evaluation runs with their score rows and the proposal per document type: query agent, from, to; 200 AgentEvaluationRun[]; with Accept text/csv the proposal rows, one row per document type | Rules and parameters R, scope applied | Not applicable: the call writes nothing |

Errors: 401 no session (message ID Not specified in the source documents (CG-ALL-2585)), 403 no Rules and parameters right (MSG-P4-002), 404 the named resource does not exist (message ID Not specified in the source documents (NEWAC-RWB-P10-E1060-APP-AC17)), 409 a same evaluation already RUNNING (MSG-P10-003), 422 a sample row that fails a check (MSG-P10-001) or a sample with no labelled rows (MSG-P10-002), 503 the store or a consumed contract unavailable (MSG-GEN-006, with {system} naming what is unavailable). The legacy in-process interfaces `DocumentQueryService.getFields` and `DocumentQueryService.getContent` are no longer provided by rwb-agent; the owner serves them. The evaluation report operation and the configuration operations are provided by RWB-P10-E1058-APP and are not re-declared here (ASM-1049).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | AC1, AC2, AC3, AC6, AC7 and AC10: the document and its stored `document_field` values with their confidence, for the sample check and for the OCR_TEMPLATE approach | One hop, 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | P5 rwb-document | AC4 and AC10: the document content read as SY-AGENT by MODEL and OCR_AND_MODEL | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC13: the six document types and LOV-DOC-TYPE in force, read before a sample row is stored and before a type is scored | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters right and the scope before a load, a start or a read, cached by the guard library | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent calls no service through another service and holds no schema client of another service. The model budget belongs to the agent platform of RWB-P10-E1058-APP and is never a REST budget of this story.

#### 12.3 Events published

None. The evaluation is started on the admin request path and publishes no business event of its own: the score rows and the proposal are read through `GET /admin/agent-evaluations`. `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` is published by a business run of an agent and belongs to RWB-P10-E1058-APP, not here.

#### 12.4 Events consumed

None. The evaluation consumes no topic: it is started by RW-COE through `POST /admin/agent-evaluations` and reads its inputs through the contracts of section 12.2. The events the agent runtime consumes - DocumentStored and CaseCreated - belong to the business runs of RWB-P10-E1058-APP.

#### 12.5 Workflows and activities

None. The extraction evaluation runs inside rwb-agent on the admin request path and starts no workflow. `AgentRunWorkflow` and the agent runtime client belong to RWB-ITG-TE013-ITG and to the E1058 sibling, and the run of an agent in shadow is called by this story through that runtime, not as a workflow of its own.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the evaluation is started by RW-COE on request and never on a cadence, and the legacy Quartz entry of the evaluation does not exist in the target.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_sample | P10 (rwb_agent) | One labelled subject in a versioned evaluation sample; written at the load, read back as counts |
| agent_evaluation_run | P10 (rwb_agent) | One evaluation of an agent version against a sample; this story adds the column proposal jsonb by `V<next>__evaluation_proposal.sql` |
| agent_evaluation | P10 (rwb_agent) | The score of one approach on one label key: TP, FP, FN, sample_size, precision and recall |
| agent_run | P10 (rwb_agent) | The shadow runs of the model approaches, with the model version, the prompt version "PR1" and the evaluation run reference |

rwb-agent reads no table of another service and holds no foreign key across services (DP-01). The document, `document_field` and OCR text rows of schema `rwb_document` are P5's and are read through its operations; the document types and the parameter values are P3's and are read through its contracts; the right is P4's and is read through its contract. `V<next>__evaluation_proposal.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15). The version number that <next> stands for is Not specified in the source documents (CG-ALL-2588).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The P5 contract of RWB-P5-E1053-CON | The 40 "COURT_NOTICE" documents with stored `document_field` values and a confidence per field, including the hearing_date counts 34, 2 and 4; the 12 "TITLE_DEED" documents; the content of every document; no document for the sample row of AC6; a delay beyond 2 s |
| rwb-case WireMock | The P3 reference-data contract of RWB-P3-E1043-CON | LOV-DOC-TYPE with the six document types and its version; a list version that lacks a type the sample uses; and the parameters contract of RWB-P3-E1042-CON with the approved policy values 0.95, 30 and the tie order |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Rules and parameters C to RW-COE and R to RW-RISK, and refusing a role without the right |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the three admin operations, one hop, with the CSV media type preserved |

The agent model endpoint INT-23 is never called by a test of this story: the model answer is the stub of the agent platform owned by RWB-P10-E1058-APP and of RWB-ITG-TE013-ITG, and no test calls a live model endpoint with real prompts.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The sample load, the evaluation start and the evaluation read or CSV export provided; the P5 document read, the P5 content read, the P3 list read and the P4 authorise consumed; one hop, 2 s |
| Kafka | None | The evaluation publishes no event and consumes no topic |
| Temporal | None | No workflow and no schedule in this story |
| File | None | The sample arrives in the multipart body of the load operation and the proposal leaves as the body of the read with Accept text/csv; no file path is used |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.evaluation`, module `evaluation`, Java package `th.co.scb.ace.workbench.recovery.agent.evaluation` inside the rwb-agent service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are the ones in the metadata rows: the three platform contract stories and RWB-PLT-N001-CON are build dependencies, and RWB-P3-E1042-CON and RWB-P3-E1043-CON are contract dependencies built against their fakes. DP-11 sits behind DP-01 on the two document reads (one hop, 2 s) and adds no dependency of its own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractionApproachRunner | Service | Produces field values per document for each of the three approaches: OCR_TEMPLATE from the stored fields, MODEL and OCR_AND_MODEL from the content and the model answer in shadow |
| FieldMatchScorer | Service | Applies BR1 and BR2 per field and approach and writes one agent_evaluation row with four decimals |
| ExtractionProposalBuilder | Service | Applies BR3 to BR5 and writes the proposal JSON on the evaluation run and the CSV rows of the export |
| SampleRowValidator | Service | Checks each sample row against the P5 contract and the P3 type list before any row is stored; hashes personal label values |
| DocumentContractClient | Client | Calls the two rwb-document operations with one hop and the 2 s budget as SY-AGENT (DP-01, DP-11) |
| PolicyValueReader | Client | Reads the target precision, the sample floor and the tie order of the approved policy row through the parameters contract and the configuration read (DP-06) |
| DocumentTypeReader | Client | Reads LOV-DOC-TYPE and the six document types through the reference-data contract (DP-07) |
| AgentEvaluationRepository | Repository | Writes and reads agent_sample, agent_run, agent_evaluation_run and agent_evaluation in `rwb_agent` only (DP-01) |
| SampleController, EvaluationController | Controller | The three admin operations on `/api/recovery/agent/v1`, the access check and the CSV media type (DP-13) |
| EvaluationAccessGuard | Library adapter | Calls `POST /api/recovery/access/v1/authorise` before a load, a start or a read and maps the refusal to MSG-P4-002 |

**Database and migrations**

- `V10_003__evaluation_proposal.sql` adds the column `proposal` jsonb to `agent_evaluation_run` in `rwb_agent`, runs in the rwb-agent Flyway sequence after the earlier P10 migrations, and touches no other schema (DP-15; AC11).
- The four tables agent_sample, agent_run, agent_evaluation_run and agent_evaluation are created in `rwb_agent` by the P10 migrations of RWB-P10-E1058-APP and this story's own migration set; this story adds no table outside its four and no foreign key across services (DP-01; BR10).
- One index for the read: `ix_agent_evaluation_run_agent_sample ON agent_evaluation_run (agent_code, sample_code, sample_version, status)`, so the running-check of X6 and the read are answered without a scan.

**Configuration and reference data**

- Policy version "P1" of agent "EXTRACT" (mode SHADOW, allowed tools read_document_content and read_document_fields, output schema "extract-fields-v1") with the target precision 0.95, the minimum labelled documents 30 and the tie order OCR_TEMPLATE before OCR_AND_MODEL before MODEL: loaded by RW-COE, approved by RW-RISK, read at run time (DP-06; ASM-1051).
- Prompt version "PR1" and the output schema "extract-fields-v1", read as versions through the configuration read of RWB-P10-E1058-APP.
- LOV-DOC-TYPE with the six document types, in force in rwb-case and read through its reference-data contract (DP-07; ASM-1048).
- The list code of LOV-DOC-TYPE, the 2 s client budget and the CSV column order as service configuration.
- The legacy feature flag `rwb.agent.extraction-eval` is kept as the legacy reference: off, the approaches list accepts only AGENT and the extraction approaches are refused with 422.

**Build steps**

1. Flyway migration `V10_003__evaluation_proposal.sql` and the four repositories in `rwb_agent` (AC10, AC11).
2. DocumentContractClient against the rwb-document contract fake: the field read, the content read, the 2 s budget, the SY-AGENT identity and the no-document answer (AC1, AC4, AC6, AC10).
3. PolicyValueReader and DocumentTypeReader against the P3 contract fakes, with the missing-policy-value path (AC12, AC13).
4. SampleRowValidator with the hash of personal label values and the row-number refusal (AC6, AC13).
5. ExtractionApproachRunner for OCR_TEMPLATE over the stored fields, then the MODEL and OCR_AND_MODEL paths through the agent runtime in shadow, with the failure count (AC1, AC4).
6. FieldMatchScorer with a fixture of 40 court notices and the known counts 34, 2 and 4 (AC1).
7. ExtractionProposalBuilder with the highest mean F1, the threshold at 0.95, the "insufficient sample" mark, the review-only field and the tie rule, plus the CSV export (AC2, AC3, AC5, AC7).
8. SampleController, EvaluationController and the access guard on `/api/recovery/agent/v1`, with the running-check of AC8 (AC8, AC9).
9. Pipeline scans for another service's table name, for a cross-schema foreign key and for the values 0.95, 30 and the tie order in the source (AC10, AC12).
10. gateway-bff route contract test in front of the admin path (AC14).

**Done when.** The fifteen test cases of section 16 pass, the three admin operations answer on `/api/recovery/agent/v1`, a DEV run over the six types produces one proposal row per type with the counts of the legacy fixture, the migration applies cleanly on an empty `rwb_agent` schema, no value of the measurement appears in the source, and no `document_field` value and no threshold in force has changed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A sample row fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The sample has no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | The store or a consumed contract is unavailable (503) | {system} is not available. Try again in a few minutes. |

The texts of MSG-P10-001, MSG-P10-002, MSG-P10-003 and MSG-P4-002 are copied unchanged from RWB-E1-060, MSG-GEN-006 is the core message of Error and Message Standard v4, and this story adds no new message ID. Thai text for each message follows decision DL10. In AC6 and AC13 the {kind} value is "sample", the {agent} value is "EXTRACT" and the {check} value names the row number and the document ID or the type that failed. In AC8 the {sample} value is "EXTRACT-S1" version 1. In the access test the {action} value is "load a sample, start an evaluation or read the scores".

### 15. Screens and states

No screen in this story. RW-COE loads the sample, starts the evaluation and reads the scores and the proposal through the three admin operations, and exports the proposal rows as CSV with Accept text/csv. The reads are reached through the gateway-bff route in front of the admin path, so a screen never calls rwb-agent directly (DP-19; AC14). The agent monitor screen SCR-46 - the screen that shows runs, fallback, latency and cost per agent and comes with RWB-E2-031 - is not changed by this story, and the review queue screen, the document screens and the architecture decision record belong to other stories and are out of scope. The exact path of the gateway-bff route in front of the admin operations is Not specified in the source documents (GAP-0644; ASM-1050).

SCR-46 states: Screen Specifications v1 gives SCR-46 the states Shadow, live and paused, with MSG-P4-002 for an action outside the role's permission (no access) and MSG-GEN-004 for a record changed by someone else. This story builds and changes no SCR-46 state. The empty, loading and error states of SCR-46 are Not specified in the source documents (DOR-RWB-P10-E1060-APP-10). States of SCR-46 as this story reads them: empty, loading and error are each Not specified in the source documents (CG-ALL-2589); no access shows MSG-P4-002, as Screen Specifications v1 gives it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-060-01 | AC1, BR1, BR2 | Component | 40 "COURT_NOTICE" documents; hearing_date with OCR_TEMPLATE counts 34, 2 and 4, precision 0.9444 and recall 0.8947 |
| TC-E1-060-02 | AC2, BR4 | Component | Scores for "COURT_NOTICE" across the three approaches; the chosen approach and the threshold at precision 0.95; the export rows |
| TC-E1-060-03 | AC3, BR3 | Component | "TITLE_DEED" with 12 labeled documents; marked "insufficient sample" with no approach and no threshold |
| TC-E1-060-04 | AC4 | Component | The model stub times out on document 7 of 40; false negatives for MODEL and failure count TIMED_OUT 1 |
| TC-E1-060-05 | AC5, BR5 | Component | Equal mean F1 0.9310 for OCR_TEMPLATE and OCR_AND_MODEL; OCR_TEMPLATE proposed |
| TC-E1-060-06 | AC6 | Component | A sample row with an unknown document ID; 422 with MSG-P10-001 naming the row number and no row stored |
| TC-E1-060-07 | AC7, BR4 | Component | case_number at most precision 0.91 for every approach and confidence; proposed as review-only |
| TC-E1-060-08 | AC8 | Component | Evaluation of "EXTRACT" on "EXTRACT-S1" version 1 already RUNNING; 409 with MSG-P10-003 and no second run row |
| TC-E1-060-09 | Access | Component | RW-CASEOWN calls POST /admin/agent-evaluations; refused with 403 and MSG-P4-002 |
| TC-E1-060-10 | AC9, BR10 | Contract | The three admin operations on `/api/recovery/agent/v1` answering 201, 202 and 200, the CSV media type, and no answer on the legacy monolith base |
| TC-E1-060-11 | AC10, BR7 | Component | A full run writing only the four tables in `rwb_agent`; the scan for another service's table name, for a cross-schema foreign key and for a schema client |
| TC-E1-060-12 | AC11, BR10 | Component | An empty `rwb_agent` schema; the Flyway sequence applies `V<next>__evaluation_proposal.sql`; agent_evaluation_run holds proposal jsonb |
| TC-E1-060-13 | AC12, BR8 | Component | Approved policy "P1" with 0.95, 30 and the tie order; the scan of the rwb-agent source for the three values; an approved policy version with other values |
| TC-E1-060-14 | AC13, BR9 | Contract | LOV-DOC-TYPE through the rwb-case contract mock; a row whose type is not in force refused with MSG-P10-001 |
| TC-E1-060-15 | AC14, DP-19 | Contract | The gateway-bff route stub in front of GET /admin/agent-evaluations with Accept text/csv, one hop, response unchanged |
| TC-E1-060-16 | AC10, BR7, §12.7 | Component | Boundary: a full run reads and writes only the four tables of §12.7 in `rwb_agent`; a read or write of a fifth table, or of a table of another schema, fails |
| TC-E1-060-17 | AC15 | Component | RW-CASEOWN calls POST /api/recovery/agent/v1/admin/agent-evaluations; refused with 403 and MSG-P4-002 |
| TC-E1-060-18 | AC16, BR6 | Component | Approved policy "P1" in mode SHADOW; OCR_TEMPLATE run with no model call; MODEL and OCR_AND_MODEL calls to agent "EXTRACT" with policy "P1" and prompt "PR1" |
| TC-E1-060-19 | AC17 | Contract | Requests to the three admin operations without a valid login, without the right, or for an unknown resource; answers 401, 403 and 404 |
| TC-E1-060-20 | AC18, X8 | Component | rwb-document contract stub that does not answer inside the 2 s budget; failed read counted, no score row for the unread documents, run FAILED |

TC-E1-060-01 to TC-E1-060-09 are the legacy test cases of RWB-E1-060, kept with their legacy IDs and their legacy data; the legacy System level maps to Component and the legacy Access level maps to Component, because the cross-service behaviour of this key is proved by RWB-ITG-E1060-ITG and its `-ITG` copies. TC-E1-060-10 to TC-E1-060-20 are new (D-RCV-60) and test only the deliverables of this story: the base of the three operations, the four tables and the no-cross-schema rule, the migration, the values read from the policy row, the reference-data origin of the types, the route in front of the reads, the access refusal, the reads and model calls of the approaches, the error answers of the admin operations and the failed contract read. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the target precision 0.95, the minimum sample 30, the tie order, the approach names and the model version are policy and configuration values read at run time, and a missing value stops the proposal instead of falling back to a default (BR8).
- No personal data in logs, tests or prompts: personal label values are stored and compared as SHA-256 hashes, documents in tests are synthetic, and no prompt carries a national ID number, a name or an account number (BR1, legacy section 17).
- No read of another service's tables and no schema client: the document, its content and its stored fields come through the rwb-document contract as SY-AGENT, the document types through the rwb-case reference-data contract, the policy values through the parameters contract and the right through rwb-access (DP-01, DP-06, DP-07).
- The four tables agent_sample, agent_run, agent_evaluation_run and agent_evaluation are the only tables this story writes, all in `rwb_agent`, and the proposal column arrives only by `V10_003__evaluation_proposal.sql` (BR10, DP-15).
- The evaluation runs in shadow and changes nothing in force: it writes no `document_field` value and no review threshold, and the threshold it proposes takes effect only through the P5 reference-data change of RWB-E1-054 (BR6).
- One hop and a 2 s client budget on every consumed REST call; the model budget belongs to the agent platform and is never a REST budget of this story (DP-11, ADR-020).
- The admin reads are reached through the gateway-bff route and never from a screen to the service (DP-19).
- The evaluation publishes no event of its own and writes no decision record: the score rows and the proposal are internal to rwb-agent and are read through its own contract.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified with a confidence score; below the threshold goes to review | Business Requirements Program, section 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-02, TC-E1-060-03, TC-E1-060-05, TC-E1-060-07 |
| REQ-DCM-006 | Fields extracted for the agreed types | Business Requirements Program, section 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | R-UNI-32 | TC-E1-060-01, TC-E1-060-04, TC-E1-060-06, TC-E1-060-08, TC-E1-060-09 |
| D-RCV-60 DP-01 | The four evaluation tables are owned by rwb-agent in schema `rwb_agent`, and the documents and their fields are read only through the rwb-document contract | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-11, TC-E1-060-01, TC-E1-060-04, TC-E1-060-16 |
| D-RCV-60 DP-06 | The target precision, the sample floor and the tie order are policy and parameter values read at run time | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-13, TC-E1-060-02, TC-E1-060-05, TC-E1-060-07 |
| D-RCV-60 DP-07 | The document types and LOV-DOC-TYPE are read from the rwb-case reference-data contract | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-14, TC-E1-060-03 |
| D-RCV-60 DP-13 | The three admin operations are served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-10 |
| D-RCV-60 DP-15 | The proposal column arrives with the service's own migration in its own Flyway sequence | Template and Rules §R5.5; ADR-021 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-12, TC-E1-060-02 |
| D-RCV-60 DP-19 | The admin reads are reached through the gateway-bff route, and SCR-46 is unchanged here | Template and Rules §R5.5; ADR-019 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-15 |
| R-UNI-32 | An agent that does not answer inside its budget falls back and the failure is counted | Business Requirements Program, section 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | R-UNI-32 | TC-E1-060-04, TC-E1-060-13 |
| RWB-E1-060 (legacy story) | Extraction evaluation [E1c]: the eight criteria AC1 to AC8 and the access test | Business Requirements Epic 1, section 3.9 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | The nine legacy test cases of section 16 |
| RWB-ITG-E1060-ITG (integration copy) | The same behaviour proved across rwb-document and rwb-agent on the real services, with the `-ITG` test cases | Business Requirements Epic 1, section 3.9 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | The fourteen test cases of that story |

The gap GAP-0644 records the areas the sources leave open for this story - the service login, the owner of the document types, the exact admin operation set, the route path in front of the reads and the read path of the score rows - and each default it raises is settled by ASM-0869 to ASM-1051.

### 19. Out of scope

- The cross-service behaviour of this key: RWB-ITG-E1060-ITG, and the harness RWB-ITG-W1J01-ITG.
- The agent platform, the model gateway client, the prompt and policy store, the sample and configuration operations and the report operation of RWB-P10-E1058-APP.
- The documents, their content and the stored `document_field` values: P5 rwb-document, RWB-P5-E1053-APP, reached only through its contract.
- Applying the chosen threshold to the review queue (P5, RWB-E1-054): this story proposes the threshold and changes nothing in force.
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- Writing the architecture decision record itself (solution architect, outside the code).
- The agent monitor screen SCR-46 and its dashboard (RWB-E2-031), the review queue screen and the document screens.
- The contract, database, operations and infrastructure stories of the legacy key, and the deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
