# RWB-ITG-DM010-ITG Migrate documents and extracted fields

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM010-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement |
| Depends on (build) | RWB-P1-DM010-APP (not done yet) |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-DM010-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-010 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM010-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 7 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **RW-DATASTEW, data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated document and document field records resolves to its ACE view row and lists every orphan with its reason and two owners, against the owning services' published contracts and their fakes**, so that **the case file is complete on the first day after cutover and no document is extracted twice**.

This story builds the harness and the evidence, and nothing else. The real document and document field records are loaded by P1's own cutover migration on its own Flyway sequence (DP-15), and the reconciliation that produces the breaks is RWB-P1-DM010-APP's. The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes one report per business date. The documents themselves live in Blob with WORM through rwb-document only (DP-01): the harness reads them through that service's contract and never touches the store, so a run can neither copy a file nor start an extraction.

### 2. Business rationale

A case file served on the first day with a document whose person_key resolves to no ACE row is a case file that cannot be evidenced. The officer opens the case, sees the document listed, and finds nothing behind the party it names; the data steward sees a break only after a complaint or an audit question. The failure is quiet, because the cutover load can report a clean run while the keys it wrote point at rows the ACE views do not hold, and a break that nobody lists is a silent data loss that surfaces as a gap in the file at the moment it is needed most. DL25 puts zero tolerance on that, so the migrated document and field records are proven against the views before the cutover is called done, and every orphan is on a list with a reason and two owners.

The second half of the risk is cost and trust in the extracted text. A document that is extracted a second time at migration holds a second confidence and a second confirming officer against the same field, and an officer who confirmed a value on the first day sees it change under them for no reason they can see. The legacy story therefore states that no document is re-extracted and no scan is repeated at migration, and the harness asserts that clause on the fields the migrated record carries: its storage reference, its extraction stamp, and the confidence and confirmed_by of each extracted field.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the documents, their custody and their extracted fields are read from rwb-document, which owns `rwb_document`; the case behind them is read from rwb-case, which owns `recovery_case`; the cutover load runs on P1's own Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and this legacy story states that no screen exists; every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries REQ-RDF-007, REQ-RDF-008 and DL25 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of P5 rwb-document (case documents, document and content), P3 rwb-case (case), P1 rwb-source-data (DP02 records, freshness and the JOB-04 rerun) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP02 Customer and party with one system of record, so person_key has one named owner before a key is resolved (FSD P1 v3, A2.2).
- The cutover load of P1's own Flyway sequence (DP-15) has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM010-APP owns the reconciliation and the break list; until it lands, the reconciliation extract fixture stands in for its output.
- The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, and the pass or fail gate with its seeding set: Not specified in the source documents (GAP-0450; ASM-0642).
- The synthetic case, the synthetic documents, the synthetic keys, the field values and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM010-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30: case RW-2026-000710 with primary_person_key PERS-SYN-000710; document DOC-SYN-0010 of document_type "ID_CARD" with person_key PERS-SYN-000710, storage_ref "blob://rwb-document/DOC-SYN-0010", source "LEGACY_WORKBENCH" and extraction stamp 2026-09-30T02:14:00Z; document DOC-SYN-0011 of document_type "PROMISE_LETTER" with person_key PERS-SYN-000711 and extraction stamp 2026-10-01T03:05:00Z; and the three extracted fields, field_name "ID_NUMBER", "ID_EXPIRY" and "LETTER_DATE", each with its field_value, its confidence and its confirmed_by. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: triggers JOB-04 reconciliation on rwb-source-data with one Idempotency-Key per business date, through `POST /api/recovery/source-data/v1/admin/jobs/JOB-04/rerun`.
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and takes primary_person_key from it.
4. Harness: reads the case document list through `GET /api/recovery/document/v1/cases/{caseId}/documents` and each document through `GET /api/recovery/document/v1/documents/{documentId}`, and asserts document_type, person_key, storage_ref, the extraction stamp and the extracted fields with their field_name, field_value, confidence and confirmed_by against the fixture.
5. Harness: performs the claim-check read `GET /api/recovery/document/v1/documents/{documentId}/content` for one document and asserts that the bytes and the checksum equal the fixture and that the answer is a link and a manifest rather than a copy held in the Workbench.
6. Harness: resolves person_key through `GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP02` for the business date and the load time, and names each key that does not resolve.
7. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan and its reason; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen.
8. Harness: reruns JOB-04 for the same business date with the same Idempotency-Key, compares the break list and the counts of documents, extracted fields, resolved keys and breaks with the first run, and re-reads one document to prove its storage_ref, its extraction stamp and its confirmed fields are unchanged and that no intake operation was called.
9. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002, no reconciliation run started and no break row written.
10. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the six criteria.
11. Harness pack for the wave 4 entry check: SIT environment and base hosts Not specified in the source documents (GAP-0450); the cutover extract fixture of steps 1 and 7 with case, document and document field rows plus source, migrated_at, storage_ref and extraction stamp; a reconciliation extract with one row per orphan and its reason; one report per business date; retention Not specified in the source documents (GAP-0450); a gate that fails on any unresolved key, any suppressed break or any re-extraction; and the data seeding set Not specified in the source documents (GAP-0450).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-010-01-ITG (ITG AC1) | ITG AC1 |
| X2 | The cutover extract fixture lacks a required key on a migrated document or extracted field | The run fails and the report names the document and the missing field; a record without a key is never reported as reconciled | None | TC-DM-010-01-ITG (ITG AC1) | ITG AC1 |
| X3 | A key has no view row and the extract does not list it | The run fails on AC2 and the report names the document, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-010-02-ITG (ITG AC2) | ITG AC2 |
| X4 | A rerun lists the same break twice | The run fails on AC3 and the report names the two rows and the business date | None | TC-DM-010-03-ITG (ITG AC3) | ITG AC3 |
| X5 | JOB-04 is refused because the ACE batch is late | The run fails before any assertion and the report names the product, the date and the message; a stale product is never treated as an empty result | MSG-P1-001 | TC-DM-010-01-ITG (ITG AC1) | ITG AC1 |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC4 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-010-04-ITG (ITG AC4) | ITG AC4 |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC3 and the report names each count and its two values | None | TC-DM-010-03-ITG (ITG AC3) | ITG AC3 |
| X8 | A storage reference or an extraction stamp has changed, or an intake operation was called | The run fails on AC3 and the report names the document, the field, its two values and the operation that was called; a re-extracted document is never reported as migrated | None | TC-DM-010-03-ITG (ITG AC3) | ITG AC3 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM010-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The migrated document and field keys are proven against the ACE views, nothing is re-extracted, and every orphan is on a list with two owners before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one no-re-extraction assertion, one break-list assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate documents and extracted fields - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds case "RW-2026-000710" with primary_person_key "PERS-SYN-000710"
    Given the case holds document "DOC-SYN-0010" of document_type "ID_CARD" with storage_ref "blob://rwb-document/DOC-SYN-0010" and extraction stamp "2026-09-30T02:14:00Z"
    Given document "DOC-SYN-0010" holds field_name "ID_NUMBER" with confidence "0.98" and confirmed_by "RW-DATASTEW"
    Given the ACE views hold one row for person_key "PERS-SYN-000710"
    Given JOB-04 has run for business date "2026-11-30"

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-010 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC2 An orphan person_key on a document is listed with its reason and its two owners (new, D-RCV-60)
    Given a migrated document "DOC-SYN-0011" on case "RW-2026-000710" carries person_key "PERS-SYN-000711"
    And the ACE views hold no row for person_key "PERS-SYN-000711"
    When the harness reads the reconciliation result for business date "2026-11-30"
    Then the break list holds one row for document "DOC-SYN-0011" with key type "PERSON" and key value "PERS-SYN-000711"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the migrated document and its extracted fields stay readable through the rwb-document contract
    And the run report names the ACE team as the second owner of the break

  Scenario: AC3 Nothing is re-extracted and a rerun lists the same break once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When JOB-04 is rerun for the same business date
    Then document "DOC-SYN-0010" keeps storage_ref "blob://rwb-document/DOC-SYN-0010" and extraction stamp "2026-09-30T02:14:00Z"
    And its field_name "ID_NUMBER" keeps confidence "0.98" and confirmed_by "RW-DATASTEW"
    And no OCR run starts, because the run calls no document intake operation and the claim-check content read returns the same bytes
    And the break list holds exactly one row for person_key "PERS-SYN-000711"
    And the counts of documents, extracted fields, resolved keys and breaks equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC4 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When the harness calls the reconciliation run for business date "2026-11-30"
    Then the answer is 403 with "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC5 Each business rule of section 8 holds on the reconciled records (new, D-RCV-60)
    Given the migrated records for business date "2026-11-30"
    When the harness reads the reconciliation result and the rwb-document answers
    Then BR1 and BR2 hold, every break is listed, and no break is suppressed
    And BR3 holds the publish while any break row exists
    And BR4 and BR6 hold, the document is read through rwb-document only and no ACE row is copied
    And BR5 and BR7 hold, with no re-extraction and each service on its own Flyway sequence
    And the harness changes none of these rules

  Scenario: AC6 A consumed call that fails or does not answer is reported and never passed as a success (new, D-RCV-60)
    Given the harness calls a consumed contract hop for business date 2026-11-30
    When the hop fails or does not answer
    Then the run report names the hop, its contract version and the failure
    And no count is reported as passed and no break row is suppressed
```

Legacy AC1 and AC3 belong to RWB-P1-DM010-APP, and the six criteria above are the ones this ITG story owns. P1 produces the cutover extract of the legacy document and document_field rows with their case, person_key, type, storage reference and confidence and hands it over to rwb-document (P5); the extract's source, format and handover mechanism are Not specified in the source documents (GAP-0540). rwb-document (P5) loads it into rwb_document through its own cutover migration on its own Flyway sequence.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated document or document field record resolves to an ACE view row before the case file is served | REQ-RDF-007; DL25 |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 |
| BR3 | Zero tolerance holds the publish: wave 4 does not open while one migrated record has an unresolved key | DL25 |
| BR4 | Documents live in Blob with WORM and are reached through rwb-document only; no service and no harness holds a copy | DP-01; ADR-010 |
| BR5 | No document is re-extracted and no scan is repeated at migration: the storage reference, the extraction stamp and the confidence of each extracted field stand as they were confirmed | Legacy RWB-DM-010 AC1; DL25 |
| BR6 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | Legacy RWB-DM-010 guardrail; D-RCV-35 (U1) |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 |

The harness asserts these rules and changes none of them.

Originals are held in Blob WORM through rwb-document only; metadata and every custody movement are rows in rwb_document, written only by rwb-document. Files already on shared drives and in the mailroom are not covered by this story: Not specified in the source documents (GAP-0242).

DL25 is open. Its assumptions ASM-0728, ASM-0735, ASM-0743 and ASM-2602 are confirmed by the programme directive and apply until the decision closes.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Document stored with an extraction stamp, as migrated | Reconciliation for the business date with every key resolved | JOB-04 completes and every person_key on a migrated document has a DP02 row | Unchanged, with the storage reference and the extraction stamp as they were |
| Document stored with an extraction stamp, as migrated | Reconciliation for the business date with one orphan | person_key PERS-SYN-000711 on document DOC-SYN-0011 has no DP02 row | Unchanged, and the orphan is listed |
| Document stored with an extraction stamp, as migrated | A listed orphan resolves and is reconciled | A DP02 row appears for the key and JOB-04 is rerun for the same business date | The break is no longer listed; the document, its storage reference and its extraction stamp are unchanged |

The harness changes no state. Every change in the table is made by the owner: P5 rwb-document holds the document, its storage reference, its extraction stamp and its extracted fields, P1 rwb-source-data writes the reconciliation result and the break list, P3 rwb-case holds the case, and P4 rwb-access answers the authorisation. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts. The legacy story names no document status value and the sources read supply none, so the table states the condition the harness asserts, its storage reference and its extraction stamp, rather than an enumerated status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Runs and reads the reconciliation for a business date; holds Platform administration R; owns the break list with the ACE team |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 and writes the reconciliation result, P5 rwb-document holds the documents and their extracted fields, P3 rwb-case holds the case, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 and DF-DOC-025 to DF-DOC-033 | document | case_id, person_key, document_type, source, storage_ref, extraction stamp | Read through the rwb-document contract |
| DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 | document_field | document_id, field_name, field_value, confidence, confirmed_by | Read through the rwb-document contract |
| DF-CAS-001 to DF-CAS-023 and DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, primary_person_key | Read through the rwb-case contract |
| No BR Field ID (ACE data product) | DP02 Customer and party | person_key | Read through the rwb-source-data data-product contract |
| Standard column | document, document_field | source, migrated_at | Read through the rwb-document contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and each range in the table lists only the IDs that the Logical Data Model gives to that entity: the legacy story names DF-DOC-001 to DF-DOC-033 for the document and DF-DOC-012 to DF-DOC-035 for the extracted field, and those spans overlap and include IDs of other entities. The two document tables are P5's and the harness reads them only through the rwb-document contract, which also serves the claim-check content read; the case is P3's and is read through the rwb-case contract. The ACE side of the key is DP02 Customer and party for person_key, read through the rwb-source-data data-product contract (FSD P1 v3, line 284), never from a view and never from a table. The document itself is never read from Blob by the harness: it reads the published document resource and the claim-check link, and the store stays behind rwb-document (DP-01). The harness owns no table and writes no row.

Lists and parameters: the harness reads them only through the owning contracts, and the reference-data contract is DP-06 and DP-07. Parameters named: Not specified in the source documents (DOR-RWB-ITG-DM010-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The documents of the case behind the migrated records (AC1, AC2) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | document_type, person_key, storage_ref, the extraction stamp and the extracted fields with confidence and confirmed_by (AC1, AC2, AC3) |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | P5 rwb-document | The claim-check read: the link and the manifest of the stored document, with no copy taken (AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case behind the documents and its primary_person_key (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP02 rows that resolve person_key (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP02` | P1 rwb-source-data | The business date and the load time of the product (AC1) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Run JOB-04 reconciliation for the business date, with one Idempotency-Key (AC1, AC3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The harness calls no write operation on rwb-document, so no upload, no new version, no custody change and no intake can be started by a run.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness triggers JOB-04 through the owner's rerun operation, not through an event, and reads the result through the same contract rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04 reconciliation, the event-triggered reconciliation workflow on rwb-source-data (Architecture v5 slides 15 and 44), is exercised through its rerun operation. P5's DocumentIntakeWorkflow, which runs the OCR, the classification and the extraction on rwb-document (Architecture v5 slides 16 and 44, JOB-12), is out of scope: this harness neither starts it nor asserts it, and its not being started is what AC3 proves. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. JOB-04 is event-triggered; the harness reruns it for the business date under test and sets no cron. The rwb-document retention schedule is P5's and is not touched.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the documents, their custody and their extracted fields are P5's, the case is P3's, the reconciliation result is P1's, and the files stay in Blob with WORM behind rwb-document.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | The three P1 operations of §12.2 | DP02 returns one row for PERS-SYN-000710, freshness returns business date 2026-11-30 with a load time, and the rerun is accepted once per Idempotency-Key |
| Stub for rwb-document | `GET /cases/{caseId}/documents`, `GET /documents/{documentId}`, `GET /documents/{documentId}/content` | The two documents of case RW-2026-000710 with their document_type, person_key, storage_ref and extraction stamp, their three extracted fields with confidence and confirmed_by, and the content link with its manifest and checksum; the stub exposes no write operation, so no intake can start |
| Stub for rwb-case | `GET /cases/{caseId}` | The case behind the documents with primary_person_key PERS-SYN-000710 |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The case, the two documents, the orphan person_key PERS-SYN-000711 on document DOC-SYN-0011, the three extracted fields with their confidence and confirmed_by, and the source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row for document DOC-SYN-0011 with key type PERSON, key value PERS-SYN-000711, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The contract version this story builds against is 5.0.0, the info.version of rwb-source-data.yaml, rwb-document.yaml, rwb-case.yaml and rwb-access.yaml in API Specification v5. The harness pack is listed in section 4, step 11. The harness environment and base hosts, the field layout of the synthetic cutover extract fixture, the break-list fields, the extract format and retention, and the data seeding set are Not specified in the source documents (GAP-0450; ASM-0642).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contract |
| Temporal | None added; JOB-04 reconciliation, the event-triggered workflow on rwb-source-data, is exercised, and P5's DocumentIntakeWorkflow is neither started nor asserted |
| File | The cutover extract fixture and the reconciliation extract fixture are read as files, and the claim-check content read on rwb-document returns a link and a manifest, never a copy held in the Workbench |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are recorded here and are not repeated in the metadata H field of this story, which stays empty as the plan requires. The one blocking dependency is the I story RWB-P1-DM010-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The four stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic case, its two documents, their extracted fields, the orphan person_key and the source and migrated_at of each record |
| KeyResolver | Service | Resolves person_key through DP02 with the freshness read, and names each key that does not resolve |
| NoReExtractionAssertion | Service | Compares the storage_ref, the extraction stamp and the confidence and confirmed_by of each field across the two runs and checks the call log for any document write operation and any intake start |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a rerun |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic case RW-2026-000710 with primary_person_key PERS-SYN-000710, document DOC-SYN-0010 of document_type ID_CARD with storage_ref `blob://rwb-document/DOC-SYN-0010` and extraction stamp 2026-09-30T02:14:00Z, document DOC-SYN-0011 of document_type PROMISE_LETTER with person_key PERS-SYN-000711, the extracted fields ID_NUMBER, ID_EXPIRY and LETTER_DATE with their confidence and confirmed_by, and business date 2026-11-30. In SIT the records come from the cutover load of P1's own Flyway sequence (DP-15), and the documents sit in Blob with WORM behind rwb-document. The harness environment and base hosts, the fixture layout, the break-list fields, the extract format and retention, and the gate with its seeding set are Not specified in the source documents (GAP-0450; ASM-0642). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the four stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-11-30 (X2).
3. Build the JourneyRunner for AC1: trigger JOB-04 with one Idempotency-Key, read the case, the case document list and each document through rwb-document, resolve person_key through DP02 with the freshness read, and list each orphan (X5).
4. Add the KeyResolver assertion that every key on a migrated document or extracted field resolves, and that each orphan is on the list for the data steward and the ACE team (X3).
5. Add BreakListAssertion for AC2: one row for document DOC-SYN-0011 with key type PERSON, key value PERS-SYN-000711, reason NO_ACE_ROW and owner role RW-DATASTEW, the ACE team named as second owner in the report, and the document and its fields still readable through the rwb-document contract.
6. Add NoReExtractionAssertion for AC3: the claim-check content read takes a link and a manifest and no copy, the storage_ref, the extraction stamp and the confirmed field values are unchanged across the rerun, the call log holds no document write operation, then the rerun with one break row, equal counts of documents, extracted fields, resolved keys and breaks, and one report entry per business date (X4, X7, X8).
7. Add the access path for AC4 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM010-APP when it lands, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

The legacy story names no screen, and neither does this harness: the breaks are listed on the reconciliation extract, which the data steward and the ACE team read as a file. The states the harness asserts on that extract are small.

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of documents, extracted fields, resolved keys and breaks, and no break row |
| Break | One row per orphan with the case number, the document, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen and the legacy story builds none. What the wave entry check looks at instead is the run report, which lists per document the storage reference, the extraction stamp and the confidence of each field so that a reader can see that nothing was extracted twice; its environment, layout and retention are Not specified in the source documents (GAP-0450; ASM-0642).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-010-01-ITG | AC1 (legacy); ITG AC1 | Integration | Synthetic case RW-2026-000710 with two documents, three extracted fields and a DP02 row for PERS-SYN-000710 |
| TC-DM-010-02-ITG | AC2 (legacy); ITG AC1, ITG AC2 | Integration | One person_key PERS-SYN-000711 on document DOC-SYN-0011 with no view row |
| TC-DM-010-03-ITG | AC3 (legacy, owned by RWB-P1-DM010-APP); ITG AC3 | Integration | Two JOB-04 runs for business date 2026-11-30, one storage_ref and extraction stamp held across both, and no intake operation in the call log |
| TC-DM-010-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |
| TC-DM-010-05-ITG | AC5 (new, D-RCV-60); ITG AC5; BR1 to BR7 | Integration | Synthetic case RW-2026-000710 with the migrated records and the reconciliation result for business date 2026-11-30 |
| TC-DM-010-06-ITG | AC6 (new, D-RCV-60); ITG AC6 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-DM010-ITG-AC6) |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. TC-DM-010-03-ITG is the cutover copy and names RWB-P1-DM010-APP as the owner of the cutover assertions it derives from.

### 17. Guardrails

- No business value in code: the synthetic keys, the business date, the fixture contents, the break reasons and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic, every document is a synthetic file and no customer record is read at all.
- No read of another service's schema, no direct view read and no direct read of the Blob store: the documents come from rwb-document, the case from rwb-case and the ACE side from the rwb-source-data contract (DP-01, DP-05).
- No document is re-extracted, no scan is repeated and no copy of a document is written into the Workbench or into a fixture; the claim-check read returns a link and a manifest (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand and never calls a document write operation.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-010 Migrate documents and extracted fields | Recovery Workbench Data Migration Stories v3, lines 635 to 712 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 660 to 664 | Section 7, AC1, marked (legacy RWB-DM-010 AC2) |
| Legacy AC1 Extract the Workbench records and its no-re-extraction clause | The same, lines 654 to 658 | Section 7, AC3, the no-re-extraction assertion; AC1 itself stays with RWB-P1-DM010-APP (section 19) |
| Legacy AC3 Cut over, and the four legacy test cases TC-DM-010-01 to TC-DM-010-04 | The same, lines 666 to 670 and 703 to 710 | AC3 stays with RWB-P1-DM010-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-DOC-001 to DF-DOC-011 and DF-DOC-025 to DF-DOC-033 for document; DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 for document_field | The same, lines 675 to 679; Logical Data Model and Data Dictionary v9 | Section 11 |
| DF-CAS-001 to DF-CAS-023 and DF-CAS-046 to DF-CAS-055 for recovery_case, and DP02 Customer and party | Logical Data Model and Data Dictionary v9; FSD P1 v3, line 284 | Section 11 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| REQ-RDF-007 and REQ-RDF-008 | BRD Program v4 and Epic 1 v4 | Section 8, BR1 and BR2 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR6; sections 12.2 and 12.8 |
| Documents in Blob with WORM through rwb-document only | Architecture v5 Text Extract v1 slides 16 and 41, and the physical and data notes | Sections 1, 12.7 and 17 |
| Job map JOB-04 reconciliation, owner rwb-source-data; JOB-12 DocumentIntakeWorkflow, owner rwb-document | Architecture v5 Text Extract v1 slides 15, 16 and 44 | Section 12.5, the JOB-04 reconciliation this harness exercises, and the DocumentIntakeWorkflow it does not start |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM010-APP: the extraction of the legacy records and legacy AC1, and the cutover of legacy AC3, together with the REC-05 reconciliation and the break list. The cutover load of the records into `rwb_document` is P1's own Flyway sequence.
- P5 rwb-document production code and its CON, APP and DB stories: the document contract, the metadata, the custody, the retention and the Blob store are built there. The DocumentIntakeWorkflow, the OCR, the classification and the extraction are not started or asserted here.
- P5 document writes: upload, a new version, a custody change, a field correction and a generated document are not called by this story.
- The document fields other than the three the fixture carries, and any field level review or confirmation workflow.
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration.
- The other four data migration keys of this wave.
