# RWB-P1-DM010-APP Migrate documents and extracted fields

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split out of RWB-DM-010 for the P1 cutover extract of the documents and the extracted fields of the open cases, its handover to rwb-document and its cutover evidence. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-DM010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **the P1 cutover extract of the legacy Workbench document and document field records for the open cases at cutover, mapped to their case, their `person_key`, their document type and their storage reference, handed over to rwb-document for its own cutover load and evidenced by the reconciliation results of this service**, so that **the case file is complete on the first day, with the storage reference it already had and no document re-extracted and no scan repeated**.

The legacy key is not withdrawn. What D-RCV-60 changes is who holds the records.

- **Extract, in rwb-source-data (this story):** the cutover run reads the legacy Workbench cutover dump once for the documents and the extracted fields of the open cases, maps every row to the keys it already holds, checks each `person_key` against `v_ace_customer`, and hands the extract over as a file with its checksum and per-entity counts. The extract is a boundary of this story, not a table: it lands nothing in `rwb_source_data` (ASM-3504).
- **Load, in P5 rwb-document:** rwb-document loads the handed-over rows into `rwb_document` on its own Flyway sequence, so the metadata, the custody record and the extracted fields are served by the service that owns them (DP-15; RWB-ITG-DM010-ITG).
- **The storage reference is carried, never re-made:** no byte of a document is read, nothing is re-OCR'd, re-scanned or re-uploaded, and custody stays with rwb-document (ASM-3505).
- **Cutover evidence (this story):** ten consecutive business dates whose reconciliation results are PASS with no unexplained variance and no new REC-05 orphan on a migrated record; a break resets the count. The count is derived from `reconciliation_result` rows that JOB-04 writes; this story builds neither the job nor a counter table (ASM-3506).
- **Sign-off:** held in the cutover record of the release pipeline; the legacy tables then stay read-only for their retention period while the migrated records are served from `rwb_document` (legacy AC3; ASM-3506).
- **Per-service migration (DP-15):** one version on the sequence of `rwb_source_data` that creates no document object and records the extract, its field list and the read-only window in its history description.
- **No screen, no REST operation, no event, no workflow of its own:** the cutover is a release-pipeline command; the result is read on SCR-44 and SCR-45 through the gateway-bff composite routes (DP-19).

### 2. Business rationale

A case file is the evidence of the recovery: the letter of demand, the restructure request, the appraisal, the identity document and the proof of delivery. Each document's content already exists in the bank's document store and its meaning has already been extracted into fields — the amount on a request, the date of an appraisal, the name on a notice. The legacy story states its own purpose: "so that the case file is complete on the first day." On the morning after cutover an officer must find the documents that belong to the case and the fields read out of them, with the same confidence and the same confirmation as the day before. The legacy story quotes its own data, copied character for character:

> | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
> | document | id, case_id, person_key, document_type, source, storage_ref and 14 more | DF-DOC-001 to DF-DOC-033 |
> | document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

Its guardrails fix the boundary this story keeps: "No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row."

**Why P1 extracts and P5 loads.** DP10 Documents and extracted fields names the Workbench as its system of record and `document`, `document_field` and `document_custody` as its tables (FSD P1 v3 A2.2). The Ownership Map puts those three entities with rwb-document, and gives rwb-source-data the ACE view contract, the extension tables, freshness and reconciliation. A service writes only its own schema, and the architecture makes that build-breaking rather than a preference (DP-01; Architecture v5 slide 45). So this story does what only the data engine can do — read the dump once, check the one ACE key a document carries, hand the extract over — and leaves the insert with the owner of the schema and the custody record (GAP-2174; ASM-3504).

**Why nothing is re-extracted.** Re-reading the content would cost a scan, an OCR run and a second copy of personal data the bank has no reason to make, and it would break the custody chain: an officer or a court would have to ask which of two objects is the document that was received. The extract therefore carries `storage_ref` and no content (legacy AC1; ASM-3505).

### 3. Preconditions

- The 30 read-only `recovery.v_ace_*` views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`. This story reads `v_ace_customer` (DF-ACE-055 to DF-ACE-074) and nothing else of ACE (TSD P1 v3 T3.3, T3.4, T6.3).
- The data product catalogue of `RWB-P1-E1001-APP` is live, with DP10 Documents and extracted fields naming the Workbench as its system of record, so the migrated rows have one named owner (FSD P1 v3 A2.2).
- `RWB-PLT-E1044-CON` is in place with the sequence of `rwb_source_data` and its baseline, so this story takes the next free version and writes one history row (TSD P1 v3 T3.2; DP-15).
- JOB-04 runs for every business date and writes `reconciliation_result` with REC-01, REC-02 and REC-05; it is the build of `RWB-P1-E1011-APP`. This story reads those rows and changes none (FSD P1 v3 A2.11).
- The gateway-bff composite routes of `RWB-PLT-N001-CON` are in place, so the cutover result is read on SCR-44 and the migrated document data quality on SCR-45 without a screen of this story (DP-19).
- The document cutover extract fixture, the `v_ace_customer` fixture and the rwb-document contract mock exist before the first build, so the story needs no production data and no real document content (section 12.8).
- The source and format of the legacy dump, the handover location and the retention period of the legacy tables are given by no source document: the extract is read once from the legacy Workbench cutover dump, the handover location is agreed with rwb-document, and the sign-off is held in the cutover record of the release pipeline — Not specified in the source documents (GAP-2174; ASM-3504).

### 4. Flow

1. The release pipeline starts the cutover run for the cutover business date under the `rwb_source_data` service identity, with one Idempotency-Key per run. It is a pipeline step, not an API call (section 12.1).
2. DocumentCutoverExtractReader reads the legacy cutover dump once, for the open cases at cutover, and selects the `recovery_case`, `document` and `document_field` rows with the fields of the legacy Data table. No document content is opened and nothing is requested from the running legacy application.
3. DocumentKeyMapper maps each row to the keys it already holds: a document keeps its case, its `person_key`, its `document_type`, its `source` and its `storage_ref`; a field keeps its `document_id`, its `field_name`, its `field_value`, its `confidence` and its `confirmed_by` (legacy AC1).
4. The mapper copies no content and re-makes no reference: `storage_ref` is carried character for character, no byte is read, and no OCR, scan, classification or upload starts (legacy AC1; ASM-3505).
5. The mapper carries no ACE field: a customer name, identity number, address or contact point in the dump is dropped, so the extract holds no copy of an ACE row (legacy guardrails; DP-05).
6. DocumentKeyResolver checks every carried `person_key` against `v_ace_customer` on the same login. A key with no view row does not stop the run: the document is handed over with its key as it stands and the orphan is listed for the data steward and the ACE team.
7. DocumentExtractHandover writes the extract to the handover location agreed with rwb-document and records its checksum, its per-entity counts and its business date in the cutover record. Nothing is inserted into `rwb_source_data` (ASM-3504).
8. rwb-document loads the handed-over extract into `rwb_document` through its own migration on its own sequence, which sets `source` and `migrated_at` and adopts the carried `storage_ref` in the custody record. This story runs no part of it and holds no grant on `rwb_document` (DP-01; DP-15).
9. From the business date after the load, JOB-04 reconciles the Workbench business keys to the views and writes its results. CutoverEvidenceCounter reads the `reconciliation_result` rows of each business date and counts a clean day when every result is PASS with no unexplained variance and no REC-05 orphan on a migrated record (ASM-3506).
10. A break of either kind resets the count to zero and the date is listed with its rows, so the next clean day starts a new run of ten. No table holds the count.
11. At ten consecutive business dates the cutover record moves to ready for sign-off; the data steward signs off in that record, which is a release artefact and not a Workbench row (ASM-3506; legacy AC3).
12. After the sign-off the legacy tables stay read-only for their retention period and the migrated records are served from `rwb_document` through the rwb-document contract (legacy AC3).
13. The story's version applies on the sequence of `rwb_source_data`: no table, no column, no index for a document, a field or a custody record, and a description that records the extract, its field list and the read-only window.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The cutover dump is absent, unreadable, or not the dump of the cutover business date | The run stops before any extract is produced; nothing is handed over, the pipeline step is FAILED and the cutover record names the dump and the date | None | AC1 |
| X2 | A document row lacks its case, its `document_type` or its `storage_ref` | The row is refused and listed for the data steward; no partial document is handed over and no value is invented | MSG-GEN-001 | AC1 |
| X3 | A field row lacks its `document_id` or its `field_name` | The row is refused and listed; the document is handed over without that field and the missing name is reported | MSG-GEN-001 | AC1, TC-DM-010-01 |
| X4 | A `person_key` resolves to no `v_ace_customer` row | The document is handed over with its key unchanged and the orphan is listed for the data steward and the ACE team; nothing is deleted or rewritten | None | AC1, AC3 |
| X5 | The dump carries a customer name, an identity number or an address | The column is dropped; the extract holds no ACE field and `rwb_source_data` stores no copy | None | AC1, TC-DM-010-01 |
| X6 | A `storage_ref` names no object, or the dump carries document content | The reference is carried as it stands and the document goes to rwb-document for custody; no content is copied, fetched or re-uploaded here | None | AC1; ASM-3505 |
| X7 | rwb-document rejects the handed-over extract | No row is loaded by that run; the mismatch is listed with its entity and count, and the cutover record shows the handover FAILED | None | AC3, TC-DM-010-03 |
| X8 | A business date of the ten clean days has a BREAK result or a new REC-05 orphan | The count resets to zero and the date and its rows are listed; the cutover record shows the break | None | AC3, TC-DM-010-03 |
| X9 | The ACE batch of a business date is not COMPLETE, so reconciliation cannot run for it | The date counts as no clean day and the product is named with its last completed business date; a stale product is never a clean day | MSG-P1-001 | AC3 |
| X10 | A caller without the Platform administration right asks for the cutover result or starts the run | The call is refused before any file is read or any record handed over | MSG-P4-002 | TC-DM-010-04 |
| X11 | The story's version is applied a second time | Flyway reports it as already applied; no row is written twice and no version is edited in place | None | AC1 |

Message texts are the legacy ones, unchanged (section 14). X1, X2, X3, X5, X6 and X11 carry no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One reader over the dump, one key mapper, one key resolver over one view, one handover writer, one evidence counter and one no-op version; the load and JOB-04 belong to other stories |
| Negotiable | The handover format, the cutover record's layout and the legacy retention period are agreed at the wave 4 entry check; this story fixes the three entities, the carried keys and the no-re-extraction rule |
| Valuable | Every open case has its documents and their extracted fields on the first day, with the reference it already had and no second copy of any content |
| Estimable | One reader, one mapper, one resolver, one handover, one counter, one version and four test cases |
| Small | Fits one sprint; the load, the reconciliation, the document intake and the screens are other stories |
| Testable | Every criterion runs against synthetic fixtures with no legacy data, no ACE data and no real document content |

### 7. Acceptance criteria

```gherkin
Feature: Migrate documents and extracted fields

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-010 AC1)
    Given the legacy Workbench document and document field records for the open cases at cutover
    Given the rwb-document contract mock returns the migrated document with its case, its person_key, its type and its storage reference
    When the migration reads them
    Then each document keeps its case, its person_key, its type and its storage reference, and each extracted field its document and its confidence
    And no document is re-extracted and no scan is repeated at migration

  Scenario: AC3 Cut over (legacy RWB-DM-010 AC3)
    Given ten clean days on the migrated records
    Given the rwb-document contract mock returns the migrated records served from schema "rwb_document"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
```

AC1 and AC3 are copied character for character from legacy RWB-DM-010. The two added Givens are the answers of the rwb-document contract — the load and the served schema are P5's — and they change no legacy value. AC2 Reconcile the business keys is owned by `RWB-ITG-DM010-ITG`; this story only reads the reconciliation results that AC3 counts (ASM-3507).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `document`, `document_field` and `document_custody` are P5's and `recovery_case` is P3's: this story extracts and hands over, and writes no row of `rwb_document`, of `rwb_case` or of any other service's schema | Ownership Map v1; DP-01; ASM-3504 |
| BR2 | The extract carries each document's case, `person_key`, `document_type`, `source` and `storage_ref`, and each field's document, name, value, confidence and confirmer, keeping every field the legacy Data table names | Legacy RWB-DM-010 AC1 |
| BR3 | `storage_ref` is carried unchanged; no content enters the extract and nothing is re-OCR'd, re-scanned or re-uploaded at migration | Legacy RWB-DM-010 AC1; DP-05; ASM-3505 |
| BR4 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, with SELECT only | BR-P1-001-2; ADR-010; TSD P1 v3 T6.3 |
| BR5 | The only ACE fact a document carries is its `person_key`, a business key with no foreign key into ACE, checked against `v_ace_customer` before the handover | BR-P1-001-3; TSD P1 v3 T3.9; DF-ACE-055 to DF-ACE-074 |
| BR6 | A migrated record keeps its source and its migration date and never a copy of an ACE row; the load sets both, and this story reads them back through the rwb-document contract | Legacy guardrails; BR3 |
| BR7 | A REC-05 orphan never deletes or changes a Workbench record: it is listed for the data steward and, where the ACE row is missing, for the ACE team | FSD P1 v3 BR-P1-011-3 |
| BR8 | The cutover evidence is ten consecutive business dates of PASS results with no unexplained variance and no new REC-05 orphan; a break resets the count and no counter table is created | Legacy RWB-DM-010 AC3; DL25; ASM-3506 |
| BR9 | The sign-off is held in the cutover record of the release pipeline; no Workbench table holds it | ASM-3506 |
| BR10 | The service runs its own Flyway sequence in its own schema; this story's version creates no document object and records the extract, its field list and the read-only window in its description | DP-15; ADR-021; TSD P1 v3 T3.2 |

BR1, BR5 and BR10 are the boundary, proved in the schema, in the history and in the refusal to write `rwb_document`. BR2 and BR3 are the extract's content. BR4 is the grant, proved by the boundary test. BR6 is what the load sets. BR7 is an orphan, which is listed and never repaired in place. BR8 and BR9 are the cutover gate.

### 9. State transitions

None for the document: the document lifecycle lives in rwb-document and is moved there after the load. The moves below are the states of the cutover itself, as the cutover record and SCR-44 show them.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The run reads the legacy dump | The dump is the dump of the cutover business date | Extract ready: every document holds its case, its `person_key`, its type and its `storage_ref`, every field its document and its confidence, nothing written to `rwb_source_data` |
| Extract ready | rwb-document loads the extract through its own migration | The extract is accepted with its checksum | Loaded: the records are served from `rwb_document` with `source` and `migrated_at`, custody adopts the carried reference, the count is zero |
| Loaded | JOB-04 writes a PASS result set for a business date | No unexplained variance and no new REC-05 orphan | Ten clean days running: the count moves to the next business date |
| Ten clean days running | JOB-04 writes a BREAK result or raises a REC-05 orphan | The business date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days running | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy tables stay read-only for their retention period and the records are served from `rwb_document` |

The record of each move is the cutover record and the `reconciliation_result` rows for the business date. This story publishes no event announcing a move, because a cutover is not a business event of the case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the clean-day count, signs off in the cutover record (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the resolver, the handover and the counter; applies the version on the per-service sequence |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result and the reconciliation results; each holds Platform administration R |
| The ACE team lead | Receives every listed orphan whose customer row is missing in ACE, and answers for the view row |
| The rwb-document service identity | Loads the handed-over rows and adopts the carried `storage_ref`; this story never uses that login |
| The rwb-source-data service identity | Reads the dump and `v_ace_customer` and writes one history row; no write on `rwb_document`, on `rwb_case` or on any `public` table |
| No delegation of authority level applies | The cutover takes no credit decision, releases no document and changes no case fact |

The role codes are rows of rwb-access, and the read of the cutover result authorises through the guard of the published operation. The legacy permission row is Platform administration R for the six roles above and is kept unchanged; the document rights of rwb-document are that service's, and this story grants none of them.

### 11. Data

| BR Field ID | Entity | Field | Read, extract or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code` and the rest of the 55 fields | Read from the dump to key each document to its case; P3's table, never written here |
| DF-DOC-001 to DF-DOC-033 | `document` | `id`, `case_id`, `person_key`, `document_type`, `source`, `storage_ref` and the rest of the 33 fields | Extracted and handed over; P5's table, never written here |
| DF-DOC-012 to DF-DOC-035 | `document_field` | `id`, `document_id`, `field_name`, `field_value`, `confidence`, `confirmed_by` and the rest of the 24 fields | Extracted and handed over; P5's table, never written here |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` | `person_key` and the 19 other fields of the view | Read only, to check a `person_key`; never extracted |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | `rec_code`, `business_date`, `product_group`, `result`, `variance_count`, `variance_pct` and the rest of the 12 fields | Read as the cutover evidence, written by JOB-04; never written here |
| None: framework table | `flyway_schema_history` | Version, description, checksum | Write, one row, at deploy only |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P1 v3 T3.4 and T3.6. `rwb_source_data` holds no document, document field or custody table, and this story's version creates none: the extract is a file with a checksum. The legacy Data table gives `document_field` as DF-DOC-012 to DF-DOC-035, overlapping the `document` range DF-DOC-001 to DF-DOC-033; that overlap is copied as the legacy story states it and is not corrected here (GAP-2174).

The migrated record keeps its `source` and its `migrated_at`, both set by the load in rwb-document and read back here through that contract (BR6). The carried `storage_ref` is a pointer and not a copy: the object stays in the store rwb-document governs under WORM (BR3). `document_custody` is not extracted, because the custody record of a migrated document is created by the service that holds the custody.

### 12. Contract

**12.1 REST operations provided**

None. The cutover is a release-pipeline command: it reads a dump and hands over a file, so no caller could address it, and no path of `/api/recovery/source-data/v1` is added here. The legacy story states the position itself: "No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract." The result is read through operations other RWB-SVC-P1 stories publish and this story neither claims nor changes:

| Operation | Base | Owner story | What it shows of this story |
|---|---|---|---|
| `GET /admin/reconciliation/results` (API-P1-003) | `/api/recovery/source-data/v1` | RWB-P1-E1011-APP | The PASS and BREAK rows the clean-day count is read from, REC-05 orphans included |
| `GET /admin/jobs` (API-P1-001) | `/api/recovery/source-data/v1` | RWB-P1-AD018-APP | The run of the cutover step, with its status and its business date |

API-P1-003 keeps its legacy ID and lists the daily reconciliation results and the REC-05 orphan keys, which is the evidence of AC3; the extract itself has no endpoint, because no source gives one (GAP-2174). The document paths — `POST /documents`, `GET /documents/{id}`, `GET /cases/{caseId}/documents` — sit under `/api/recovery/document/v1` and belong to rwb-document.

**12.2 REST operations consumed**

None at run time. The run reads its dump, checks its keys against its own view on its own login and writes its own history row; it calls no service and holds no C dependency. Two contract mocks are fixtures only (section 12.8): the rwb-document read of the migrated document and the rwb-case read of the case a document is keyed to.

**12.3 Events published**

None. The cutover publishes no Kafka event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`; EV-26 and EV-27 belong to `RWB-P1-E1013-APP`. `rwb.document.events.v1`, with DocumentStored and DocumentFieldsExtracted, is rwb-document's.

**12.4 Events consumed**

None. No event starts the cutover: the release pipeline does. The reconciliation that produces the evidence is started by EV-26 AceDataReady in `RWB-P1-E1011-APP`, and the intake that JOB-12 drives runs in rwb-document after the load.

**12.5 Workflows and activities**

None added. JOB-04, whose results are counted, is the event-triggered workflow of `RWB-P1-E1011-APP` on task queue `rwb-source-data`; JOB-12 Document intake and JOB-17 Retention are rwb-document's. This story creates, changes and starts no workflow, activity or child workflow.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job sits here: the cutover is a one-off pipeline run and the daily counting is a read over rows another story's trigger writes.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the cutover evidence, written by JOB-04 (`RWB-P1-E1011-APP`) |
| `document`, `document_field`, `document_custody` | `rwb_document` | P5 | **Not owned, not written**: extracted to a file and loaded by rwb-document's own migration |
| `recovery_case` | `rwb_case` | P3 | **Not owned, not written**: read from the dump to key a document to its case |

No document, document field or custody table is added to `rwb_source_data`; TSD P1 v3 T3.6 lists P1's own tables (18 in the ownership pack) and no document table is among them. No statement of the story names a table in `public` or in another service's schema, and the only cross-schema read is the granted `recovery.v_ace_*` view (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | Synthetic `recovery_case`, `document` and `document_field` rows of the open cases at cutover: case "RW-2026-000601", document "DOC-SYN-000601" of type "RESTRUCTURE_REQUEST" with storage reference "blob://syn/DOC-SYN-000601", person key "PERS-SYN-000601", one field "requested_amount" at confidence 0.94, and a second document "DOC-SYN-000777" | AC1, AC3 and paths X2, X3, X5 from Day 1 |
| View fixture (`v_ace_customer`) | The view as synthetic rows in a container, with one row for "PERS-SYN-000601" and none for "PERS-SYN-000777" | AC1 key resolution and the orphan path X4 |
| rwb-document contract mock (`GET /documents/{id}`, `GET /cases/{caseId}/documents`) | The migrated document with its case, `person_key`, type, `storage_ref` and extracted fields, served from schema `rwb_document` | AC1, AC3 and the load report |
| rwb-case contract mock (`GET /cases/{caseId}`) | The case a document is keyed to, with its case number and state, as a fixture only | AC1 read-back of the case key; no run-time call |
| Reconciliation extract fixture (`reconciliation_result` rows) | PASS sets for ten consecutive business dates and one BREAK set for the counter reset | AC3 and paths X8, X9 |

Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change fails a test rather than passing silently. The source and format of the real legacy dump, the handover location and the retention period are Not specified in the source documents (GAP-2174; ASM-3504).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | A pipeline command; the result is read through API-P1-003 and API-P1-001, which other stories own |
| Kafka | None | None | Nothing published or consumed here; `rwb.document.events.v1` is rwb-document's |
| Temporal | None | None | No workflow, activity or schedule; JOB-04 is `RWB-P1-E1011-APP`'s |
| File | None | One | The legacy cutover dump, read once per run, and the handed-over extract with its checksum and per-entity counts; no document content |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Schema `rwb_source_data`, login `rwb_source_data`, base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1` and queue `rwb-source-data` (the last two named for completeness and used by no part of this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentCutoverExtractReader | Repository | Reads the dump once and selects the three entities with the legacy field list; no write, no `public` table, no other schema, no content |
| DocumentKeyMapper | Service | Maps each row to the keys it carries, carries `storage_ref` unchanged, and drops every ACE field and content column |
| DocumentKeyResolver | Service | Checks each `person_key` against `v_ace_customer` on the service login and names every key with no row |
| DocumentExtractHandover | Service | Writes the extract with its checksum and per-entity counts and records them in the cutover record; inserts nothing |
| CutoverEvidenceCounter | Service | Reads `reconciliation_result` per business date and counts ten consecutive PASS dates with no new REC-05 orphan; a break resets the count, which no table holds |
| `V000x__dm010_document_extract.sql` | Migration | The next free version of the per-service sequence: creates no table, column, index or grant and records the extract, its field list and the read-only window |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the 30 views, so the `person_key` check is its own SQL on its own login and adds no contract hop. DP-15 gives this story its one version and history row and gives rwb-document the sequence that loads the rows, so the load needs no cross-schema write (GAP-2174; ASM-3504). DP-19 applies to the read of the result on SCR-44 and of the document data quality on SCR-45 and adds no screen. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of its own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16), no schedule (DP-10).

**Database and migrations**

- Reads the dump and `v_ace_customer` and writes no row at run time; the only write is the history row of its own version.
- The version creates no table, column, index or constraint, grants nothing on `rwb_document` or `rwb_case`, and records the extract, its field list and the read-only window in its description (BR1, BR10).
- The version number is the next free one on the sequence, after the baseline and the Section A and Section B versions of TSD P1 v3 T3.2. No source names the legacy migration file, so the story asserts only that no version of the sequence names a document extract, a load or a custody record.
- The load's migration and sequence are rwb-document's and are neither described nor applied here (DP-15; ASM-3505).

**Configuration and reference data**

- No parameter and no reference list is read: DP-06 and DP-07 are not in the pattern set. The cutover date, the handover location and the retention period are configuration of the release pipeline, agreed at the wave 4 entry check, and no value is written in code (FSD P1 v3 BR-P1-002); where no source gives one, the story names the assumption rather than a number (ASM-3504).
- The view, its field IDs and its types are the view contract's; the story consumes `person_key` and re-implements no view rule.
- Feature switch `rwb.source-data.document-cutover-extract` from the platform flag library: off, the run does not start, no extract is produced and the cutover record stays at Not started.
- Login `rwb_source_data`: SELECT on the 30 views, USAGE on `rwb_source_data`, no privilege in `public`, in `rwb_document` or in `rwb_case` (T6.3).

**Build steps**

1. DocumentCutoverExtractReader over the dump fixture: one read per run, no write, no content column read (AC1).
2. DocumentKeyMapper: the carried keys, `storage_ref` proven character for character, every ACE field and content column dropped; tests X2, X3, X5, X6 (AC1).
3. DocumentKeyResolver over `v_ace_customer` with a resolvable and an unresolvable key and the orphan list for the two owners (AC1, X4).
4. DocumentExtractHandover with the checksum and the per-entity counts, and the assertion that `rwb_source_data` holds zero rows of the three entities before and after (AC1).
5. CutoverEvidenceCounter over the reconciliation fixture: ten PASS dates, a BREAK on the sixth, a missing ACE batch and a new REC-05 orphan (AC3, X8, X9).
6. The read-back of the load through the rwb-document mock: the served schema, `source`, `migrated_at` and the adopted `storage_ref` (AC3).
7. The refusal path through the guard of the published operations, with no file read after a deny (TC-DM-010-04).
8. The no-op migration with its description and the repeated-apply check (AC1, X11).

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no document table, the extract is handed over with a checksum and lands nothing, the carried `storage_ref` is proven unchanged with no content read, the counter reads ten clean days from the reconciliation results and resets on a break, and no class writes `rwb_document`, writes `rwb_case` or names a `public` table.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | The ACE batch for a business date of the ten clean days is not COMPLETE, so reconciliation cannot run for that date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | A document row lacks its case, its type or its storage reference, or a field row lacks its document or its field name | Enter {field}. |
| MSG-P4-002 | Error | The caller's Platform administration right R or U is absent | You cannot {action} here. Your role does not include it. |

The three messages are copied character for character from the legacy story and the module FSD. For MSG-P1-001, {product} is the product code under test ("DP01" or "DP02") and {date} its last completed business date. For MSG-GEN-001, {field} is the field name of the refused row ("case_id", "document_type", "storage_ref", "document_id" or "field_name"). For MSG-P4-002, {action} is "run the document cutover" or "read the cutover result", never a case fact, a document fact or a field value. No other message is raised by this story.

### 15. Screens and states

No screen in this story, and the legacy story states the same: "No screen in this story." The cutover result is read on SCR-44 Interface and job monitor, the administration screen that shows a run with its status and its reruns, and the migrated document data and its breaks on SCR-45 Data quality; both are gateway-bff composite routes (DP-19; H `RWB-PLT-N001-CON`). The count and the results it is read from are also shown on the reconciliation result list of API-P1-003, published by `RWB-P1-E1011-APP`. The document screens of the case file are rwb-document's.

| State | What the cutover record, SCR-44 and SCR-45 show |
|---|---|
| Extract ready | The dump read once, the per-entity counts, the checksum, and the orphan list of any `person_key` with no view row |
| Loaded | The handover accepted by rwb-document, the load reported through that contract, and a clean-day count of zero |
| Ten clean days running | The business dates counted so far, each with the PASS results of its reconciliation |
| Break | The date of the break, its BREAK rows or its REC-05 orphan, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy tables read-only for their retention period |

A run that cannot start shows on SCR-44 in its failed state, with the dump and the business date named and no extract produced, so a cutover that did not happen is never read as one that did.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-010-01 | AC1; BR1, BR2, BR3, BR4, BR5, BR6, BR10 | End to end | The extract fixture with case "RW-2026-000601", document "DOC-SYN-000601" of type "RESTRUCTURE_REQUEST" with storage reference "blob://syn/DOC-SYN-000601" and person key "PERS-SYN-000601", one field "requested_amount" at confidence 0.94, and a second document "DOC-SYN-000777"; the `v_ace_customer` fixture with one row for the first person and none for the second; a dump row carrying a customer name and a content column to prove both are dropped; `storage_ref` compared character for character with no content read; the row count of the three entities in `rwb_source_data` before and after; the version applied once and again |
| TC-DM-010-02 | AC2 read side only: the REC-05 result rows AC3 counts; BR7 | Component | The reconciliation fixture with two REC-05 orphan rows on migrated records and a PASS row on the same business date; the counter read over the same rows; the orphan list naming the data steward and the ACE team; the assertion that no migrated record is deleted or changed. The cross-service proof of AC2 itself is `TC-DM-010-02-ITG` in `RWB-ITG-DM010-ITG` |
| TC-DM-010-03 | AC3; BR5, BR7, BR8, BR9 | End to end | The reconciliation fixture with PASS sets for ten consecutive business dates, then one BREAK set and one new REC-05 orphan on a later date; a business date whose ACE batch is absent; the rwb-document mock answering the migrated documents with `source`, `migrated_at` and the adopted `storage_ref` from schema "rwb_document" |
| TC-DM-010-04 | Access refusal; BR4 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present for the contrast; a row count of `rwb_source_data` before and after the refusal |

TC-DM-010-01 and TC-DM-010-03 are End to end because the run leaves the service's own boundary: it reads a file, checks a key against a view and reports a load another service performed. TC-DM-010-02 and TC-DM-010-04 are Component because they exercise the counter over the service's own rows and the guard at the boundary of a published operation. The ITG copies of the four legacy cases are `TC-DM-010-01-ITG` to `TC-DM-010-04-ITG` in `RWB-ITG-DM010-ITG`, where AC2 is owned (ASM-3507).

### 17. Guardrails

- No business value in code: the cutover date, the handover location and the retention period are configuration of the release pipeline; the story writes no threshold, percentage, amount or date.
- No personal data in logs, tests or prompts: the fixtures are synthetic, the `person_key` is a business key and not an identity, no name, identity number, contact point or address enters the extract, and no document content is read into a log, a test or a prompt.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service owns the views: one login, SELECT only, no `public` table named in any statement (BR4).
- No copy of an ACE row: no customer field enters the extract, and `rwb_source_data` holds no document, field or custody table before or after this story (BR1).
- `storage_ref` is carried, never re-made: no byte of a document is read, no OCR run, scan, classification or upload starts, and WORM custody stays with rwb-document (BR3; ASM-3505).
- No cross-schema write: the rows are loaded by rwb-document through its own migration, and this story holds no grant on `rwb_document` or `rwb_case` (DP-01).
- An orphan is listed and never repaired: no migrated record is deleted or changed to make a key resolve (BR7).
- A break is never waived: a BREAK result or a new REC-05 orphan resets the count, and a stale product is never a clean day (BR8; MSG-P1-001).
- The sign-off is an artefact of the release, not a Workbench row, and no counter table is invented for the ten days (BR9; ASM-3506).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).

### 18. Traceability

| Legacy RWB-DM-010 item | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, epic RWB-SVC-P1; `document`, `document_field` and `document_custody` are P5's and are loaded by rwb-document |
| Epic | E1, release 30 November 2026 | Wave 4 from EP08; release 30 November 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | RWB-P1-E1001-APP (data products and catalogue) and RWB-P1-E1069-APP (views and grant) |
| Decision | DL25 | BR8, BR9: the ten clean days and the zero-tolerance cutover gate |
| Data | recovery_case DF-CAS-001 to DF-CAS-055; document DF-DOC-001 to DF-DOC-033; document_field DF-DOC-012 to DF-DOC-035 | Section 2 quotation; section 11; AC1; TC-DM-010-01 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Section 12.1; API-P1-003 is the read of the breaks, owned by RWB-P1-E1011-APP |
| Screen and states | No screen in this story. | Section 15; the result is read on SCR-44 and the document data quality on SCR-45 |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR3, BR6; AC1; section 17 |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Section 7; TC-DM-010-01 and TC-DM-010-03 |
| AC2 and TC-DM-010-02 | Reconcile the business keys, REC-05 | AC2 owned by RWB-ITG-DM010-ITG as its AC1, with `TC-DM-010-02-ITG`; this story reads the rows only |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_customer` is read by this service on its own login, to check the one key a document carries and copy nothing (section 13) |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence for the extract's record, and the load on rwb-document's own sequence (section 13; AC1, AC3) |
| DP-19 | Template and Rules §R5.5 | The cutover result and the document data quality are read on SCR-44 and SCR-45 through the gateway-bff composite routes (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H build dependency: the gateway-bff composite routes that serve SCR-44 and SCR-45 |
| RWB-P1-E1001-APP | App development | H build dependency: the data products and the catalogue DP10 is named in |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 read-only views, the login and the grant |
| RWB-P1-E1011-APP | App development | Builds JOB-04 and writes `reconciliation_result`, the cutover evidence |
| RWB-ITG-DM010-ITG | Integration | Owns AC2 and asserts the migrated keys and the break list across the services; its I dependency is this story |
| The rwb-document cutover load (P5) | App development | Loads the handed-over extract into `rwb_document` and adopts the carried `storage_ref`; the boundary and the contract are P5's |
| The rwb-case case read (P3) | App development | Reads the case a document is keyed to; a fixture here, and this story holds no grant on `rwb_case` |

External dependencies: None. The load in rwb-document is another service's work and not an external dependency (ASM-3504).

### 19. Out of scope

- The load of the documents, the extracted fields and the custody record into `rwb_document`, its migration, its sequence, its rollback and its reconciliation to the extract: P5 rwb-document's own cutover work (GAP-2174; ASM-3504).
- The document content itself — Azure Blob, WORM, the OCR text, the classification agent, intake JOB-12 and retention JOB-17: rwb-document (ASM-3505).
- AC2 Reconcile the business keys, REC-05, the break list and its report: `RWB-ITG-DM010-ITG` owns AC2 and `RWB-P1-E1011-APP` builds the reconciliation (ASM-3507).
- JOB-04, its workflow, its activity, its rerun operation and the `reconciliation_result` rows: `RWB-P1-E1011-APP`.
- The 30 read-only views, the `rwb_source_data` login, its grant and the boundary test: `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`.
- The data product catalogue, the dictionary, the data contracts and the access rows, DP10 included: `RWB-P1-E1001-APP`.
- SCR-44 Interface and job monitor and SCR-45 Data quality with their routes: `RWB-P1-AD018-APP`, `RWB-P1-AD019-APP`, their CON stories and the gateway-bff composite route.
- The case, its owner and its links, which the document is keyed to: `RWB-P1-DM003-APP` extracts them and P3 rwb-case loads them.
- The retention period itself, the archival of the legacy tables and the decommissioning of the legacy Workbench: the cutover plan and the data steward, and no source gives the period (GAP-2174).
- The extract of the scores and route economics, of the decision log and of money and closure, which share this pattern: `RWB-P1-DM011-APP`, `RWB-P1-DM012-APP` and `RWB-P1-DM013-APP`.
- The data lake, INT-19 and INT-20: removed, and no story of this key needs lake data (DP-17).
