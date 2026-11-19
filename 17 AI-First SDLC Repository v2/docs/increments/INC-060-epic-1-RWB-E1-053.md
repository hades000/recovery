# Increment Card — INC-060-epic-1-RWB-E1-053

**RWB-E1-053 — Field extraction for the six types into the index**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-060` |
| Title | Field extraction for the six types into the index |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-053` |
| RUN_ID | `INC-060-epic-1-RWB-E1-053` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 60 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-049, RWB-E1-050, RWB-E1-025 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **case owner**, I want **the key fields of each of the six document types extracted and written to the document index with a confidence per field**, so that **documents are searchable by their content**.

**Business outcome:** Court dates, case numbers, appraisal values and title numbers are typed by hand from paper today, and a document is found only by the person who filed it. This story reads the agreed fields of each classified intake item and each uploaded document into the index with a confidence score, so the case owner and the litigation officer find a document by its content, the attach step finds the case from the extracted case number, and the low-confidence values go to a person. It meets REQ-DCM-006 and REQ-DCM-001 and feeds the module measure "fields extracted without review", which is to rise each month.

**Main flow:**
1. JOB-12 Document intake: runs extractStep after classifyStep and before matchStep.
2. ExtractStep: selects intake items with ocr_status DONE and extract_status PENDING that are classified with no review_reason, or that carry a document ID with a given type (uploads), locking each row.
3. ExtractStep: reads the field definitions of the type from the version of DocumentTypeCatalog in force, the threshold and the attempts.
4. ExtractStep: reads the page text and layout through OcrOutputReader.
5. FieldExtractor: the extractor named by extraction_method returns a raw value and a confidence per field, with the extractor version.
6. ValueNormalizer: converts each value to its data type: Thai and English dates to ISO dates, Buddhist Era years less BE_YEAR_OFFSET, Thai digits to Arabic digits, amounts to numeric(18,2) baht.

**Acceptance criteria:**
- AC1: Fields extracted
- AC2: Precision and recall
- AC3: A field below the threshold goes to review
- AC4: A review-only field always goes to review
- AC5: Confidence equal to the threshold passes
- AC6: A value that cannot be converted goes to review
- AC7: The extracted case number and account number are given to matchStep
- AC8: The extractor does not answer
- AC9: A repeated run has no effect
- AC10: Two workers on the same item
- AC11: A new version of an uploaded document
- AC12: An English document is extracted
- AC13: A document outside the caller's scope

**Out of scope:**
- The review queue screen and correction of fields (RWB-E1-054).
- Matching the item to its case and storing the document (RWB-E1-032, RWB-E1-024).
- Search by extracted field (RWB-E1-033).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- The choice of extraction approach per type (RWB-E1-060).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-053-field-extraction-for-the-six-types-into-the-index-v1.md` |
| Requirement IDs | REQ-DCM-006, REQ-DCM-001 |
| BRD section | Business Requirements Epic 1, section 3.5 |
| Decision | D7.2 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs extractStep; writes extracted fields and document_field rows (Documents CRU) |
| RW-CASEOWN, case owner | Reads the document and its fields in scope (Documents R) |
| RW-LITOFF, litigation officer | Reads the document and its fields in scope (Documents R) |
| RW-COE, center of excellence analyst | Reads the evaluation report; prepares the review-only proposal |
| RW-REFADM, reference data administrator | Loads a new DOCTYPE version (Reference data CRUD) |
| Business lead with Legal | Approves the type and field list (DL19) |

## Contract extract

**Job step** | Item | Value | |---|---| | Job name | JOB-12 Document intake; this story adds extractStep after classifyStep | | Schedule | Every 15 minutes in business hours | | Input | Intake items with ocr_status DONE and extract_status PENDING that are classified with no review_reason, or that carry a document with a given type | | Output | extracted_fields and extract_status on the item; document_field rows and review_status for attached documents; counts on the job record | | Events published | DocumentFieldsExtracted (EV-17) for attached documents, payload documentId, field names and confidence; no values | | Idempotency key | Intake item ID and table version; an item with extract_status DONE or FAILED is not read again | | Restart | Unfinished items stay PENDING and are taken by the next run | **Published interface (P5, used by RWB-E1-032 and RWB-E1-054)** ```java package recover…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset come from the type table and document_hub_parameter. - No personal data in logs, tests or prompts: logs and the job record hold item IDs, field names and confidence only; text sent to the model is masked as in RWB-E1-050. - No read of another module's tables: the model is reached through the P10 gateway. - Extraction never writes to a stored file or a container.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-053-field-extraction-for-the-six-types-into-the-index-v1.md` |
| Specification | `output/INC-060-epic-1-RWB-E1-053/specify/spec.md` |
| Compliance validation | `output/INC-060-epic-1-RWB-E1-053/specify/compliance-validation.md` |
| Agent run log | `output/INC-060-epic-1-RWB-E1-053/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-060-epic-1-RWB-E1-053/plan/` |
| Implementation evidence | `output/INC-060-epic-1-RWB-E1-053/implement/` |
| API / functional test reports | `output/INC-060-epic-1-RWB-E1-053/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-060-epic-1-RWB-E1-053/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 13 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-053-field-extraction-for-the-six-types-into-the-index-v1.md` |
| Output run | `output/INC-060-epic-1-RWB-E1-053/` |

