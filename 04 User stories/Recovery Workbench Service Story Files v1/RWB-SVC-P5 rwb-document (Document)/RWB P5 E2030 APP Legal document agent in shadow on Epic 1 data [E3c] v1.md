# RWB-P5-E2030-APP Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2030-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP13, DP19 |
| Parallel lane | L-P5-Z |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2030-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-012) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-030 for rwb-document, carrying the checklist evidence read the legal document agent makes on the officers' Epic 1 packs and the availability answer the agent's contract maps to a shadow run that is not scored. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **rwb-document to answer the pack evidence read for one litigation case — the checklist items at the checklist version in force, with the document IDs of the case held against each item and the present or missing mark of the case's completeness record — as one atomic answer on the per-service API base**, so that **the legal document agent's shadow run scores every checklist item against the same evidence the litigation officers built their packs from, and a document service that does not answer leaves the case unscored instead of half-scored**.

This story is the rwb-document part of legacy RWB-E2-030. The legacy flow step 2 has the agent read "the case, the legal action, the documents with their fields and the checklist for the case type" (legacy section 4), its precondition loads "the document checklist per case type as reference data (RWB-E1-040)", BR2 states that "checklist items come from the document checklist for the case type" (REQ-DCM-011), AC1 requires "a pack listing document IDs for each of the 9 items", and AC6 turns a failure of "the P5 document interface" into run status TOOL_UNAVAILABLE with fallback true and the case listed as not run. Three of those facts are rwb-document's: the checklist items of the version in force, the document IDs of the case against each item, and one answer that either arrives whole or fails whole.

Inside `rwb-document` this is the pack evidence capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1` (DP-13), topic `rwb.document.events.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The answer is assembled from five tables of `rwb_document` only: `document` and `case_document_check` for the evidence, `document_checklist_item` and `document_type` for the items at the version in force, and nothing else (DP-01). No `rwb_case`, `rwb_litigation` or ACE table is read.
- The checklist version in force and the lists are resolved through the reference-data contract of rwb-case (DP-07); the page size and the read timeout are parameters of the same owner (DP-06).
- The completeness record is the row that RWB-P5-E1040-APP writes inside its inbox transaction from `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`; this story reads that row and returns its `lastEventId`, so a shadow run names the document event its evidence reflects and no event is invented here (DP-09).
- The agent is never called by this service. It is the caller of the read, which is why the only contract dependency of the story is RWB-P10-E2030-CON.

The rest of legacy RWB-E2-030 is owned elsewhere and is not answered here: the agent runtime, policy "LEGAL_DOC" version "P1", prompt "PR1", output schema "legal-pack-v1", the SCHEMA and SCHEMA_RULE guardrails, the agreement scorer, sample "LEGAL-S1", the minimum of 50 scored cases, the review date and the promotion proposal belong to rwb-agent in RWB-P10-E2030-APP; the legal action read is rwb-litigation's; the approver separation of duty is rwb-access's and rwb-agent's; the pack, its retrieval requests and the officer verification are Epic 5 and rwb-litigation's. Legacy AC1 to AC9 stay there and none of their text is copied into section 7.

### 2. Business rationale

A litigation pack that reaches the law firm with a missing or defective document is returned and the filing waits (legacy section 2; R-LIT-16, R-LIT-17, CTL-19). The agent is run in shadow on 50 Epic 1 cases whose packs the officers already built, scored per checklist item, so that the decision to promote it to Epic 5 rests on an accuracy per item and not on an impression. That measurement is only worth something if the agent is scored against the document evidence the officers worked from: the items of the checklist version in force, and the document IDs the hub holds against each item.

rwb-document is the system of record for that evidence. The checklist per stage and route is reference data of this service (`document_checklist_item`, FSD P5 A2.16, FEAT-DCM-16, REQ-DCM-011); the types, their fields and their sign-offs are `document_type` (A2.3); the documents and their versions are `document` (A2.19, A2.20); and the completeness record of a case is `case_document_check`, with `required_count`, `present_count`, `missing_types`, `complete` and `last_event_id` (TSD P5 T3.1). The published form of that record is API-P5-008 `GET /cases/{caseId}/document-checklist`, "the required document types for the case with present counts" (TSD P5 T-A.2).

Four target facts shape this slice.

1. **One version in force.** The items, their order and their required flag are rows of the checklist version the reference-data route reports in force; nothing about an item is written in code (DP-07, FSD P5 BR-P5-016). A new version changes the answer with no deployment.
2. **One hop, two seconds.** The read is synchronous on the caller's thread, one hop, with a 2 s budget and a breaker per downstream (Architecture v5 slides 9 to 11). For the agent the hop is its tool gateway, which calls this service directly and never chains; for a screen the hop is the gateway-bff composite route of DP-19.
3. **One answer, whole or none.** A pack assembled from half an answer scores every item wrongly and looks like an accuracy problem of the model rather than of the evidence. The read therefore answers one document per request: either the full per-item answer, or a 503 with MSG-GEN-006 and nothing else, which the agent's contract turns into TOOL_UNAVAILABLE, fallback true and a case that is listed as not run (legacy X3, R-UNI-33).
4. **Read only.** No document, version, checklist row, completeness row, legal action, pack or case field is written by this call, and no user-facing endpoint returns a pack (legacy BR1; TSD P5 NFR-029, write-once legal documents). The pack itself is the agent's output row and is never stored here.

The slice answers REQ-DCM-011 for the pack that checks completeness against data rather than memory, and serves the document half of legacy REQ-S4-002, whose pack assembly, defect list and promotion decision stay with rwb-agent and Epic 5.

### 3. Preconditions

- The `rwb_document` baseline is in place: `document`, `document_type`, `document_checklist_item` and `case_document_check` exist at the platform migration version, and the outbox, inbox and idempotency tables of DP-09 are created in the schema by the event library.
- RWB-P5-E1040-APP is done: the checklist rows and the completeness record are written, API-P5-008 answers, and `case_document_check` is recomputed inside the inbox transaction of `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`, with `last_event_id` set to the event that produced the row.
- RWB-P5-E1025-APP is done: `document_type` holds the type versions in force with their field definitions and their Legal and NPA sign-offs.
- RWB-P10-E2030-CON is published: the rwb-agent contract of this legacy key, which fixes the tool call the agent makes for the pack, the item codes of output schema "legal-pack-v1", and the mapping of an unavailable document read to run status TOOL_UNAVAILABLE with fallback true. Its operation name, per-item field names and error mapping are Not specified in the source documents (GAP-2358; ASM-3913), and the story builds against its fake.
- The checklist version in force, LOV-STAGE, LOV-ROUTE, LOV-DOC-TYPE and LOV-REVIEW are read through the reference-data contract of rwb-case (DP-07, C RWB-P3-E1043-CON, which arrives with the baseline); no list value is copied into `rwb_document`.
- The page size and the read timeout are parameter values of the parameters contract of rwb-case (DP-06, C RWB-P3-E1042-CON); no page size and no timeout is written in code.
- The checklist is keyed by `stage_code` and `route_code` (LOV-STAGE, LOV-ROUTE) while the legacy story asks for the checklist "for the case type" and names case type "MORTGAGE_CIVIL". No source gives a case-type key, a case-type to stage and route mapping, or the 9 items of that case type, so the story reads the version in force by stage and route and the mapping is Not specified in the source documents (GAP-2359; ASM-3914).
- The authorisation and masking decision is served by rwb-access and consumed as the cached permission of the service (baseline); the field mask format is not part of this answer, which carries codes, references, counts and marks only.
- The case "RW-2026-000901", its 14 documents and its open legal action are rwb-case's and rwb-litigation's; this story needs only the case ID and reads neither service's rows.
- The sample "LEGAL-S1" version 1, the policy "LEGAL_DOC", the minimum of 50 scored cases, the review date and the agreement rate are rwb-agent's rows and its policy values; this story reads none of them.

### 4. Flow

1. RW-COE starts the evaluation of "LEGAL_DOC" on sample "LEGAL-S1" in rwb-agent (RWB-P10-E2030-APP). This story receives no trigger of its own.
2. For each sample case, the agent's tool gateway calls `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` with the identity of SY-AGENT.
3. `PackEvidenceReader` authorises the call through the cached decision of rwb-access (Documents right R, scope applied) and refuses with 403 and MSG-P4-002 before reading a row when the right is absent, or with MSG-P4-003 when the case is outside the caller's scope.
4. The reader resolves the checklist version in force for the case's stage and route through `ChecklistVersionResolver` and the reference-data contract (DP-07), and the page size and timeout through the parameters contract (DP-06).
5. `PackEvidenceReader` reads the items of that version from `document_checklist_item` with their `document_type`, `required` flag and `sort_order`, and the type row of each item from `document_type` at the version in force.
6. For each item it reads the active documents of the case of that type from `document` — `id`, `document_type`, `source`, `doc_version`, `write_once`, `review_status` — restricted to `case_id` equal to the requested case, and marks the item present when at least one such document exists.
7. It reads the completeness record of the case from `case_document_check` — `checklist_version`, `required_count`, `present_count`, `missing_types`, `complete`, `checked_at`, `last_event_id` — and returns it with the items.
8. `PackEvidenceAnswerer` assembles the single answer: the case ID, the checklist version and its `lastEventId`, the counts of the completeness record, and the item list with the document IDs of each item, inside the 2 s budget, one hop, with no call to another service after the two contract reads.
9. The agent scores the pack against the officers' pack per item and stores the agreement (RWB-P10-E2030-APP). Nothing of that is written here: the answer is served and discarded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller's identity holds no Documents right R | Refused before any row is read; nothing is returned | MSG-P4-002 | AC5 |
| X2 | The case is outside the caller's scope | Refused before any row is read; no item and no document ID is returned | MSG-P4-003 | AC2 |
| X3 | The case holds no completeness record and no checklist row for its stage and route | The answer holds the version in force with an empty item list, `complete` empty and counts of 0; nothing else changes | None | AC1, AC3 |
| X4 | The reference-data read of the version in force does not answer | The call answers 503 with MSG-GEN-006 naming "Reference data"; no partial answer | MSG-GEN-006 | AC4 |
| X5 | The parameters read does not answer | The call answers 503 with MSG-GEN-006 naming "Parameters"; no answer with a default page size | MSG-GEN-006 | AC6 |
| X6 | The store does not answer inside the 2 s budget | The call answers 503 with MSG-GEN-006 naming "Document service"; the breaker opens; the agent's contract turns the answer into TOOL_UNAVAILABLE, fallback true and a case listed as not run | MSG-GEN-006 | AC4 |
| X7 | A stored type of a document has left the version in force | The document is returned under the type stored on its row and is never re-typed by this story; the item keeps the type of the checklist row | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Answers from `rwb_document` only, builds against the RWB-P10-E2030-CON fake, the reference-data and parameters routes of rwb-case and the authorisation decision of rwb-access; no build dependency of its own, and no rwb-agent, rwb-litigation or Epic 5 workflow is needed |
| Negotiable | The version in force, the items, the order, the page size and the timeout are rows, parameters or configuration; the story fixes only the answer and its failure |
| Valuable | The legal document agent is scored per checklist item against the evidence the officers used, and an unavailable hub leaves the case unscored instead of wrongly scored |
| Estimable | One published operation already on the P5 contract, one reader, one resolver, one answerer and one failure path |
| Small | Fits one sprint as a secondary slice of the legacy key, with the checklist and completeness rows of RWB-P5-E1040-APP already in place |
| Testable | Each criterion in section 7 is one automated test over synthetic documents and checklist rows, with every cross-service answer stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Legal document agent in shadow on Epic 1 data [E3c] — the rwb-document pack evidence read

  Background:
    Given the rwb-agent contract mock returns the legal-pack tool call of agent "LEGAL_DOC", the item codes of output schema "legal-pack-v1" and the mapping of an unavailable document read to run status "TOOL_UNAVAILABLE" with fallback true
    Given the rwb-case reference-data contract mock returns the checklist version in force for case type "MORTGAGE_CIVIL" with 9 items, including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF"
    Given the rwb-case parameters contract mock returns page size 100 and read timeout 2 s
    Given case "RW-2026-000901" holds 14 active documents and an open legal action

  Scenario: AC1 The items of the version in force with the document IDs of the case (new, D-RCV-60)
    Given the rwb-access contract mock returns Documents right R for actor "SY-AGENT" on case "RW-2026-000901"
    When "SY-AGENT" calls GET /api/recovery/document/v1/cases/RW-2026-000901/document-checklist
    Then the answer holds the checklist version in force and its 9 items in sort order, each with its item code, its type code and its required flag
    And each item carries the document IDs of case "RW-2026-000901" whose type is the item's type, with each document's source, doc_version, write_once and review_status
    And an item with no active document of its type is marked missing and carries an empty document ID list
    And the answer carries the completeness record of the case with its required count, present count, missing types, complete flag, checked time and lastEventId

  Scenario: AC2 Only the documents of the requested case, inside the caller's scope (new, D-RCV-60)
    Given document "D-7001" belongs to case "RW-2026-000902" and document "D-7011" of case "RW-2026-000901" is inactive
    When "SY-AGENT" calls the checklist read for case "RW-2026-000901"
    Then "D-7001" and "D-7011" appear in no item of the answer
    And the rwb-access contract mock refusing the case scope answers 403 with MSG-P4-003 and returns no item and no document ID
    And the read is authorised with the caller's own identity and no request carries a case ID the caller may not see

  Scenario: AC3 The items are data of the version in force (new, D-RCV-60)
    Given the reference-data contract mock reports a second checklist version in force in which one item is added and one item is withdrawn
    When the read answers for the same case before and after the version changes
    Then the item list follows the version in force, with the added item present and the withdrawn item absent
    And no item code, sort order, required flag, page size or timeout appears in the Java source or the module configuration
    And a document whose stored type has left the version in force is returned under its stored type and is never re-typed

  Scenario: AC4 A read that cannot be completed answers nothing (new, D-RCV-60)
    Given the document store of case "RW-2026-000903" does not answer inside the read timeout, or the reference-data read does not answer
    When "SY-AGENT" calls the checklist read for case "RW-2026-000903"
    Then the call answers 503 with MSG-GEN-006 naming the system that failed
    And the answer holds no item, no document ID, no count and no completeness record
    And the RWB-P10-E2030-CON fake maps that answer to run status "TOOL_UNAVAILABLE" with fallback true and lists the case as not run
    And the breaker opens for that downstream and the next call answers 503 without waiting for the timeout again

  Scenario: AC5 The read changes nothing and no screen returns a pack (new, D-RCV-60)
    Given the tables `document`, `document_field`, `document_checklist_item`, `case_document_check` and `document_type` hold their rows before the call
    When the checklist read answers for case "RW-2026-000901"
    Then no row is inserted, updated or deleted in any table of `rwb_document` by the read
    And no legal action, case field, agent run, evaluation row or pack is written by this service
    And no endpoint of this service returns a pack, a completeness list or an agreement score

  Scenario: AC6 One hop, inside the budget, with parameters from their owner (new, D-RCV-60)
    Given the parameters contract mock returns page size 100 and read timeout 2 s
    When the checklist read answers for a case with 14 documents and 9 items
    Then the answer is assembled in one request with calls only to the reference-data and parameters contracts
    And no service of another owner is called on the read path and no call chains a second hop
    And the page size and the timeout are the values of the mock and no default is used when it does not answer
```

The six criteria above are new and test only this slice: the per-item checklist evidence the legal document agent reads, the same-case restriction, the version in force, the atomic failure, the read-only guarantee and the one-hop budget. Legacy AC1 to AC9 of RWB-E2-030 are owned by RWB-P10-E2030-APP — the shadow pack, the agreement rate, the promotion proposal, the same-case guardrail, the item without a status, the unavailable document interface on the run, the sample minimum, the review date and the loader who cannot approve — and no legacy criterion text is copied here.

Three cross-service facts are read from the mocks named in the Background: the rwb-agent contract of RWB-P10-E2030-CON returns the tool call, the item codes of "legal-pack-v1" and the mapping of a failed read to TOOL_UNAVAILABLE; the rwb-case reference-data contract returns the checklist version in force and the lists; the rwb-case parameters contract returns the page size and the timeout. The operation name and per-item field names of that tool call are Not specified in the source documents (GAP-2358; ASM-3913), and the per-item fields of the answer are Not specified in the source documents (GAP-2360; ASM-3915): the names used above are the columns of TSD P5 T3.1 (`document_checklist_item`, `case_document_check`, `document`) and the purpose of API-P5-008 in T-A.2.

The 9 items of case type "MORTGAGE_CIVIL", including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF", are the values of the legacy story (its Background and AC1) and are held as rows of a checklist version in the story's fixtures only; which stage and route that version belongs to is Not specified in the source documents (GAP-2359; ASM-3914), because `document_checklist_item` is keyed by `stage_code` and `route_code` and carries no case type.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The items, their type, their required flag and their order are rows of the checklist version the reference-data route reports in force; nothing about an item is written in code | REQ-DCM-011; FSD P5 A2.16 BR-P5-016; TSD P5 T3.1 |
| BR2 | The read names only documents whose `case_id` is the requested case and whose row is active; a document of another case is never named, also when its type matches an item | Legacy BR4 and AC1 on the document side; TSD P5 T3.1 `document.case_id` |
| BR3 | An item is present when the case holds at least one active document of the item's type, and missing otherwise; the counts and the missing types of the answer are the ones of `case_document_check` and are not recomputed differently | FSD P5 A2.16 AC-ALT-P5-016-02 and AC-EXC-P5-016-01; TSD P5 T3.1 |
| BR4 | A readability failure of any dependency produces one 503 with MSG-GEN-006 and no partial answer, so a case is either scored on whole evidence or listed as not run | Legacy X3 and AC6; R-UNI-33; RWB-P10-E2030-CON |
| BR5 | The read writes no row and changes no document, no checklist row, no completeness row, no legal action, no case field and no pack | Legacy BR1; TSD P5 NFR-029 |
| BR6 | The evidence is pinned to the document event that produced it: the answer carries `lastEventId` and `checked_at` of the completeness record, and a second identical call returns the same pair | TSD P5 T3.1 DF-DOC-044; DP-09 |
| BR7 | A document whose stored type has left the version in force is returned under the type stored on its row and is never re-typed, and an item whose type is absent from the type version is returned with the code on the checklist row | FSD P5 AC-EXC-P5-001-01 (store-time refusal only); TSD P5 T3.1 |

The rules hold in `rwb_document` as follows. BR1 is executed by `ChecklistVersionResolver`, which takes the version from the reference-data route and the rows from `document_checklist_item` at that version, plus a build check that fails on an item code or a sort order in the source. BR2 and BR3 are executed by `PackEvidenceReader` as two predicates on the same query: `case_id` equals the requested case, `is_active` is true, and the item's presence is the existence of at least one such row; the counts are read from `case_document_check` and never recalculated by the answerer, so the answer and the case list agree. BR4 is executed by `PackEvidenceAnswerer`, which builds the answer in memory and returns it only when every part of it has been read, so an exception leaves nothing to serialise. BR5 is executed by the read-only transaction of the reader and by a test that compares table counts before and after the call. BR6 is executed by returning `last_event_id` and `checked_at` unchanged from the row. BR7 is executed by joining `document_type` at the version in force for the label only and never for the stored type of a document.

### 9. State transitions

None for the case. This story changes no case status, starts no workflow and moves no document: it reads the rows the store, the checklist and the completeness evaluation wrote.

| Row | Written by | Read here as |
|---|---|---|
| `document_checklist_item` | RWB-P5-E1040-APP and the reference-data maintenance of P5 | The items of the version in force |
| `case_document_check` | RWB-P5-E1040-APP, inside the inbox transaction of `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` | The completeness record of the case, with `last_event_id` |
| `document` | RWB-P5-E1024-APP (store) and the intake path of RWB-P5-E1049-APP | The document IDs of each item and their `review_status` |

The agent run states — PENDING, RUNNING, TIMED_OUT, GUARDRAIL_FAILED, COMPLETED — and the policy states LOADED and APPROVED are rwb-agent's rows and rwb-agent's transitions (RWB-P10-E2030-APP); no state of them is written or read here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Reads the checklist evidence of a case in its scope with Documents right R (TSD P5 T6.1) |
| RW-COE, center of excellence analyst | Reads the scores and the evidence references through the agent's export; this story serves the agent, not the analyst |
| RW-LITOFF, litigation officer | Supplies the officers' packs for the sample; reads no pack through this answer |
| rwb-document service identity (the rwb-document login, DP-02) | Serves the read and reads five tables of `rwb_document` only; writes nothing |
| RW-PLATADM, platform administrator | Platform administration right R: reads the operational views of the service, no document content |
| RW-AUDIT, internal audit | Platform administration right R: reads the access entries written by the ACE common module |

The authorisation decision is not taken here. It comes from rwb-access, which owns Recovery roles as data, scope and the masking policy, consumed as the cached permission of the service; the refusal shapes are 403 with MSG-P4-002 for a missing right and 403 with MSG-P4-003 for a case outside the scope, both raised before any row is read. Each read uses the caller's own identity: the agent's tool gateway presents SY-AGENT, and no shared identity exists for the agent's reads.

### 11. Data

| BR Field ID | Entity in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-REF-234 to DF-REF-243 | `document_checklist_item` | id, stage_code, route_code, document_type, required, sort_order, table_version, valid_from, valid_to, reference_version_id | Read (the items of the version in force) |
| DF-REF-219, DF-REF-220, DF-REF-222, DF-REF-229 | `document_type` | doc_type_code, label_en, write_once, table_version | Read (the type row at the version in force, for the label and the write-once flag of the item) |
| DF-DOC-001, DF-DOC-002, DF-DOC-004, DF-DOC-005, DF-DOC-008, DF-DOC-010, DF-DOC-011 | `document` | id, case_id, document_type, source, review_status, write_once, doc_version | Read (the document IDs of each item; `case_id` is the same-case predicate) |
| DF-DOC-036 to DF-DOC-044 | `case_document_check` | id, case_id, checklist_version, required_count, present_count, missing_types, complete, checked_at, last_event_id | Read (the completeness record and the event the evidence is pinned to) |
| DF-OPS-178 to DF-OPS-183 | `processed_event` (inbox of the platform event library) | the inbox columns of the library | Not written: the consumer is RWB-P5-E1040-APP; this story reads `last_event_id` only |

Field IDs are those of the Logical Data Model and Data Dictionary and the TSD P5 T3.1 tables. Nothing is written here: no document, no document field, no checklist row, no completeness row and no pack. The case, the legal action, the sample, the policy and the agreement rate arrive only through contracts or not at all: the case is a reference carried on the rows, the legal action is rwb-litigation's and is read by the agent itself, and the policy and sample rows are rwb-agent's. No `v_ace_*` view and no `public` table is read, and no row of another service's schema is copied (DP-01).

### 12. Contract

#### 12.1 REST operations provided

One operation of the document hub contract on base `/api/recovery/document/v1`, owner rwb-document (P5). This story adds no path: it answers API-P5-008 for the pack reader and adds the per-item document IDs and the completeness reference to its answer, which is Not specified in the source documents (GAP-2360; ASM-3915).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P5-008 | GET | `/cases/{caseId}/document-checklist` | Read the required document types for the case with present counts, and for the pack reader the document IDs held against each item and the completeness reference of the case | Documents right R, scope applied | Not applicable |

**API-P5-008.** Request: none. Response: DocumentChecklist — `caseId`, `checklistVersion`, `complete`, `requiredCount`, `presentCount`, `missingTypes`, `checkedAt`, `lastEventId`, and `items[]` with `itemCode` (the document type of the checklist row), `typeLabel`, `required`, `sortOrder`, `present`, and `documents[]` with `documentId`, `source`, `docVersion`, `writeOnce`, `reviewStatus`. Errors: 401 no Workbench identity, 403 Documents right R absent (MSG-P4-002) or case outside the scope (MSG-P4-003), 404 no such case, 503 the store, the reference data or the parameters do not answer (MSG-GEN-006). The answer is assembled in one transaction and is never partial.

#### 12.2 REST operations consumed

Two contracts are called at run time, both owned by rwb-case, and one contract is consumed as a shape and never called.

| Contract | What is consumed | Note |
|---|---|---|
| DP-07 reference data of rwb-case (C RWB-P3-E1043-CON) | The checklist version in force for the case's stage and route, and the lists LOV-STAGE, LOV-ROUTE, LOV-DOC-TYPE and LOV-REVIEW | Read through the reference-data client library; no list value is copied into `rwb_document` |
| DP-06 parameters of rwb-case (C RWB-P3-E1042-CON) | The page size and the read timeout of API-P5-008 | Read through the parameters client library; no page size and no timeout in code |
| RWB-P10-E2030-CON | The agent's tool call for the pack, the item codes of "legal-pack-v1" and the mapping of a 503 to TOOL_UNAVAILABLE with fallback true | The agent is the caller of 12.1; the contract fixes what the answer must satisfy. Its operation name and field names are Not specified in the source documents (GAP-2358; ASM-3913) |

#### 12.3 Events published

None. This story publishes no event: it serves a synchronous read, and the document events of this service (`rwb.document.DocumentStored.v1`, `rwb.document.DocumentFieldsExtracted.v1`) are published by the store and the extraction path of RWB-P5-E1024-APP and RWB-P5-E1053-APP on `rwb.document.events.v1`.

DP-09 applies to this slice on the consumer side and as a read of its result: the completeness record that the answer returns was written by RWB-P5-E1040-APP inside its inbox transaction, and `last_event_id` (DF-DOC-044) names the outbox event it was computed from. The answer therefore pins the evidence to one document event, and a shadow run can name the event its scores reflect without this service publishing anything.

#### 12.4 Events consumed

None in this story. The inbox consumer of `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` is RWB-P5-E1040-APP; this story holds no consumer group, subscribes to no topic and writes no inbox row. The inbox table of DP-09 is present in `rwb_document` for the consumers that other P5 stories add.

#### 12.5 Workflows and activities

None. The read is a synchronous REST call in the caller's thread, one hop, inside the 2 s budget. `DocumentIntakeWorkflow` and its activities belong to RWB-P5-E1049-APP, the agent's run workflow is rwb-agent's on queue `rwb-agent`, and this story starts neither and contributes no activity.

#### 12.6 Schedules

None. The 15-minute document intake Schedule (legacy JOB-12) belongs to RWB-P5-E1049-APP and the retention Schedule (legacy JOB-17) to the retention story; this slice adds no Schedule and no timer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_checklist_item` | P5 (`rwb_document`) | Read only: the items of the version in force, with their type, required flag and order |
| `document_type` | P5 (`rwb_document`) | Read only: the type row at the version in force, for the label and the write-once flag of an item |
| `document` | P5 (`rwb_document`) | Read only: the document IDs held against each item, and the same-case predicate |
| `case_document_check` | P5 (`rwb_document`) | Read only: the counts, the missing types, the complete flag, `checked_at` and `last_event_id` |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_document` | Present for the store and the consumer of RWB-P5-E1040-APP; not written by this story |

rwb-document reads no table of another service and holds no foreign key across services (DP-01). The case is not copied: its ID arrives on the request and on the rows. The version in force, the lists and the parameters arrive through the contracts of 12.2.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P10-E2030-CON fake | The agent contract of this legacy key | The pack tool call with its field names (as the fake fixes them), the item codes of "legal-pack-v1", and the mapping of a 503 to TOOL_UNAVAILABLE with fallback true (AC4) |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | DP-07 | The checklist version in force with 9 items for case type "MORTGAGE_CIVIL", a second version in force that adds one item and withdraws one (AC3), LOV-STAGE, LOV-ROUTE, LOV-DOC-TYPE and LOV-REVIEW, and a failing read for X4 |
| rwb-case parameters fake (RWB-P3-E1042-CON) | DP-06 | Page size 100 and read timeout 2 s, and a failing read for X5 |
| rwb-access authorise fake (RWB-P4-E1037-CON) | The guard of the service template | A granted decision for SY-AGENT with Documents right R, a refused decision without it (AC5), and a refused scope decision for a case outside the scope (AC2) |
| Store test double | The read path of AC4, AC6 and X6 | A store that answers in 40 ms, a store that never answers, and a store that answers after the timeout |
| Topic test double for `rwb.document.events.v1` | The events whose result the answer carries | Records the event ID written by RWB-P5-E1040-APP so `lastEventId` can be asserted character for character (AC1, BR6) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | API-P5-008 on `/api/recovery/document/v1`, one hop with a 2 s budget and a breaker per downstream; the reference-data and parameters reads of rwb-case through their client libraries |
| Kafka | None | No event published and none consumed in this story; the events of the topic are the store's and the consumer's (DP-09 read as `last_event_id`) |
| Temporal | None | No workflow, no activity and no Schedule in this slice |
| File | None | No blob is read: the answer carries document references and no content, and the content read API-P5-004 is the store's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `packevidence`, Java package `th.co.scb.ace.workbench.recovery.document.packevidence`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PackEvidenceController | Controller | `GET /cases/{caseId}/document-checklist`, request validation, the scope check and the problem responses of section 14 |
| PackEvidenceReader | Service | Reads the items of the version in force, the type rows, the active documents of the case per item and the completeness record, from `rwb_document` only |
| ChecklistVersionResolver | Service | Resolves the checklist version in force and the lists through the reference-data contract of rwb-case, cached per request |
| PackEvidenceAnswerer | Service | Assembles the one answer and returns it only when every part is read, so a failure yields 503 and no partial answer |
| SameCaseGuard | Service | Applies the `case_id` and `is_active` predicates of BR2 and asserts that no document ID outside the case is serialised |

**Database and migrations.** No migration. The five tables are created and loaded by RWB-P5-E1040-APP, RWB-P5-E1025-APP and RWB-P5-E1024-APP in the per-service Flyway sequence of `rwb_document`; this slice adds no table, no column and no index. No migration of this service touches another service's schema or the shared baseline.

**Configuration and reference data.**

- The checklist version, the lists and the page size are read at run time (DP-07, DP-06); a change of version changes the answer with no deployment.
- The item codes, the sort order, the required flags, the 9 items of case type "MORTGAGE_CIVIL" and the type and stage lists are rows or list values, never literals: a build check fails on an item code, a sort order or a list value in the source.
- The stage and route used to find the version in force for a case come from the case's stage as rwb-case reports it and from the route of the version in force. No case-type key exists on `document_checklist_item`, and the mapping from case type to stage and route is Not specified in the source documents (GAP-2359; ASM-3914).
- The feature switch `rwb.document.pack-evidence` is read as a parameter: off means API-P5-008 answers 404 to the agent's identity and the document estate itself is unchanged.
- The read timeout is the parameter value of DP-06 and the breaker is per downstream, in the service template.

**Build steps**

1. `ChecklistVersionResolver` over the reference-data fake, with the version in force and the 9-item fixture; unit tests for AC3.
2. `PackEvidenceReader` over the four tables with the `case_id` and `is_active` predicates and the completeness record; unit tests for AC1, AC2 and X3.
3. `SameCaseGuard` and a property test that places a document of another case in each item and asserts that it appears in no answer.
4. `PackEvidenceAnswerer` with the all-or-nothing assembly and the 503 paths of X4, X5 and X6; component tests for AC4.
5. The controller with the authorisation guard, the scope refusal and the problem responses; API tests for AC2, AC5 and the 401 and 403 shapes.
6. The read-only test that compares table counts before and after the call, and the build check that fails on an item code, a sort order or a list value in the source; tests for AC5 and AC3.
7. A contract-fake run of RWB-P10-E2030-CON, rwb-case reference data and parameters, and rwb-access, so the slice proves every criterion before rwb-agent is live in DEV.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P10-E2030-CON` exactly as the Work Package fixes them; the platform contract libraries of DP-06, DP-07, DP-09 and DP-19 arrive with the baseline, not with this story.

- **DP-01** keeps the whole answer inside `rwb_document`: the items, the types, the documents and the completeness record are this service's own, no `rwb_case` or `rwb_litigation` table and no ACE view is read, and the case is only a reference carried on the rows.
- **DP-06** is the parameter read: the page size and the read timeout come from the parameters contract and client library of rwb-case, cached per request, so neither is a constant of the module.
- **DP-07** is the version read: the checklist version in force, the item rows at that version and the four lists are taken from the reference-data route, so a new checklist version changes the pack evidence with no deployment.
- **DP-09** is read here and not published: the completeness record is written by RWB-P5-E1040-APP in its inbox transaction on the owner's topic `rwb.document.events.v1`, and the answer returns its `lastEventId` and `checked_at`, so the evidence of a shadow run is pinned to one document event.
- **DP-13** gives the read its base `/api/recovery/document/v1`, so the agent's tool gateway and the gateway-bff call one owner and never a monolith path.
- **DP-19** is the gateway-bff composite route on which the Documents tab of a screen reads the same operation; the agent reaches it through its tool gateway, one hop, and no route calls a service that calls another.

**Done when.** The tests in section 16 pass, the contract test of RWB-P10-E2030-CON stays green, case "RW-2026-000901" is read by SY-AGENT as 9 items with the document IDs held against each, a document of another case never appears, a failing store answers 503 with MSG-GEN-006 and no partial answer, and the read writes no row.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | The store, the reference data or the parameters do not answer inside the budget (X4, X5, X6) | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The caller's identity holds no Documents right R (X1) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope (X2) | This case is not in your scope. |
| MSG-P10-001 | Not in this story: the promotion checks belong to RWB-P10-E2030-APP | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Not in this story: the evaluation on an empty sample belongs to RWB-P10-E2030-APP | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |

For MSG-GEN-006 the {system} value is "Document service" on the store read, "Reference data" on the version read and "Parameters" on the parameter read. For MSG-P4-002 the {action} value names the action — for example "read the document checklist of this case" — and never a case fact, a document ID or a role name. Errors are RFC 9457 problem responses with `messageId`, `detail` with the placeholders filled and `instance` naming the request; the HTTP mapping is 403 for MSG-P4-002 and MSG-P4-003, 404 for a case that does not exist, and 503 for MSG-GEN-006.

### 15. Screens and states

No new screen. The read is a service-to-service call: the agent's tool gateway calls rwb-document, one hop, and no person is in the loop. SCR-30 Case documents shows the same checklist panel it showed before, read through the gateway-bff composite route of DP-19 and served by API-P5-008, and the pack, the missing-label and the completeness wording of that panel are the screen's and RWB-P5-E1026-APP's, not this story's.

The run monitor and the evaluation scores are rwb-agent's: SCR-46 Agent monitor shows LEGAL_DOC in state Shadow with its runs, fallbacks and the evaluation score, and the center of excellence analyst reads them there (RWB-P10-E2030-APP). This story serves that screen nothing and holds no state of it. No screen shows a pack, a completeness list or an agreement score.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-030-01 | AC1, AC3 and AC5 for the per-item evidence and the read-only guarantee; the shadow run and the pack belong to RWB-P10-E2030-APP | Contract | Case RW-2026-000901, 14 documents, 9 checklist items; API-P5-008 answers 9 items with their document IDs and writes no row |
| TC-E2-030-02 | No criterion here; the agreement per item and the rate 0.9200 belong to RWB-P10-E2030-APP | Component | Sample LEGAL-S1 version 1, 50 cases; 46 agree on DEMAND_NOTICE_PROOF |
| TC-E2-030-03 | No criterion here; the promotion proposal and the review date belong to RWB-P10-E2030-APP | Component | Version P2 SHADOW with review date 2027-03-15 |
| TC-E2-030-04 | AC2 for the same-case restriction on the document side; the guardrail status GUARDRAIL_FAILED is the agent's | Contract | Document D-7001 of case RW-2026-000902 requested in the evidence of case RW-2026-000901; it appears in no item |
| TC-E2-030-05 | No criterion here; the item without a status and the SCHEMA guardrail belong to RWB-P10-E2030-APP | Component | No status for MORTGAGE_DEED |
| TC-E2-030-06 | AC4 and X6: the document interface down for one case | Contract | Store of case RW-2026-000903 never answers; API-P5-008 answers 503 with MSG-GEN-006 naming "Document service" and no partial answer; the agent fake maps it to TOOL_UNAVAILABLE with fallback true |
| TC-E2-030-07 | No criterion here; the sample minimum of 50 belongs to RWB-P10-E2030-APP | Component | 49 scored cases, proposal L1 |
| TC-E2-030-08 | No criterion here; the review-date check of a SHADOW version belongs to RWB-P10-E2030-APP | Component | SHADOW version with no review date |
| TC-E2-030-09 | No criterion here; the separation of duty between loader and approver belongs to RWB-P10-E2030-APP and rwb-access | Component | Loader approves version P2 |
| TC-E2-030-10 | AC2 and AC5 for the refusal of a caller without the right on the evidence read; the agent evaluation call is the agent's | Component | An identity without Documents right R calls API-P5-008 of case RW-2026-000903; refused with 403 and MSG-P4-002; SY-AGENT is granted the same read |
| TC-P5-E2030-01 | AC1, AC3 and BR3 for the version in force and the present and missing marks | Component | Two checklist versions in force, one item added and one withdrawn; the counts of case_document_check are returned unchanged |
| TC-P5-E2030-02 | AC6 and BR6 for the budget, the parameters and the pinned event | NFR | Page size 100, timeout 2 s, store answering in 40 ms; the answer carries lastEventId and checked_at, and a second call returns the same pair |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to Contract or Component here, because the end-to-end shadow run is the agent's. Every legacy test case of this key is listed above with the slice of behaviour this story answers — the per-item evidence for TC-E2-030-01, the same-case restriction for TC-E2-030-04, the unavailable document interface for TC-E2-030-06 and the access refusal for TC-E2-030-10 — and no criterion for the cases whose behaviour is the agent's or the policy's. The -ITG copies of these cases are not here: they belong to RWB-ITG-E2030-ITG, which proves the same values across rwb-document, rwb-agent, rwb-litigation and rwb-case end to end.

### 17. Guardrails

- No business value in code: the item codes, the sort order, the required flags, the counts, the page size and the timeout are rows, parameters or configuration. A build check fails on an item code, a sort order, a page size or a list value in the source.
- No personal data in events, workflow inputs, logs or error messages: the answer carries a case ID, document IDs, type and source codes, versions, flags and counts, and no document value and no content. Nothing is logged beyond the case ID and the outcome, and no personal field is read by this slice.
- No cross-schema read: `rwb_document` holds no foreign key into another schema and no copy of a case, a legal action, a rule row or a list value (DP-01). ACE data is not read at all, and no `v_ace_*` view is touched.
- Read only: the answer writes no document, version, review status, checklist row, completeness row, legal action, case field or pack, and the transaction is read only so a write fails the build (BR5).
- The evidence is what the hub holds: the answer never invents a document, never re-types a stored document and never recomputes the counts differently from `case_document_check`, so the case list and the pack agree.
- One evaluator per concern: this story evaluates no rule package, holds no Drools dependency and reads no rule row. The guardrails, the policy and the scorer of the legal document agent stay with rwb-agent and rwb-decision.
- The failure is the evidence: a dependency that does not answer produces one 503 with no partial answer, so a case is unscored rather than wrongly scored, and the agent's contract turns it into TOOL_UNAVAILABLE with fallback true.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-011 | A document checklist per case type is held as reference data so that a missing document is visible | Not specified in the source documents (GAP-2362; ASM-3917) | FEAT-DCM-16, FEAT-DCM-03 | Not specified in the source documents (GAP-2362; ASM-3917) | R-LIT-16, R-LIT-17, CTL-19 | TC-E2-030-01, TC-E2-030-04, TC-P5-E2030-01, TC-P5-E2030-02 |

The legacy requirement of the key, REQ-S4-002 (a litigation pack assembled and checked against the document checklist, with the missing documents named), is answered here only for its document half — the items and the documents held against them — and its pack assembly, defect list and promotion decision are carried by RWB-P10-E2030-APP under the same requirement. The supporting features of the document estate are FEAT-DCM-16 (the checklist as reference data), FEAT-DCM-03 (types, fields and checklist membership) and A2.16 of the FSD P5; this slice changes neither the checklist design nor its maintenance.

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E2-030 — flow step 2 (documents and checklist per case type), BR2, AC1, AC6, X3 | Sections 1, 2, 4, 7, 8, 14 |
| Legacy case type "MORTGAGE_CIVIL" with 9 items including LOAN_CONTRACT, MORTGAGE_DEED and DEMAND_NOTICE_PROOF | Background, sections 7, 13, 16 |
| Case RW-2026-000901 with 14 documents, case RW-2026-000902 with document D-7001, case RW-2026-000903 | Background, sections 5, 7, 16 |
| Run status TOOL_UNAVAILABLE with fallback true and the case listed as not run | Sections 1, 2, 5, 7, 12.2, 12.8 |
| MSG-GEN-006, MSG-P4-002, MSG-P4-003 | Section 5, section 14 |
| TC-E2-030-01 to TC-E2-030-10 | Section 16 |

### 19. Out of scope

- The agent runtime, policy "LEGAL_DOC", prompt "PR1", output schema "legal-pack-v1", the SCHEMA and SCHEMA_RULE guardrails, the agreement scorer, sample "LEGAL-S1", the minimum of 50 scored cases, the review date and the promotion proposal: RWB-P10-E2030-APP and the contract RWB-P10-E2030-CON.
- The DEFECT status of an item and its reason: the hub holds no defect concept, the pack's defect list is the agent's output, and the evidence a defect needs is Not specified in the source documents (GAP-2361; ASM-3916).
- The legal action read, the litigation pack, its retrieval requests and the officer verification: rwb-litigation and the Epic 5 stories.
- The checklist rows, their maintenance, the completeness evaluation and its event-driven recompute: RWB-P5-E1040-APP.
- The type table, its field definitions and its Legal and NPA sign-offs: RWB-P5-E1025-APP.
- The store, the version rule, the write-once container and the custody of an original: RWB-P5-E1024-APP and the custody and retention stories of P5.
- The access and the masking policy themselves, and the separation of duty between the loader and the approver: rwb-access and RWB-P4-E2030-APP.
- The gateway-bff composite route, the case documents screen and the document search screen: RWB-PLT-N001-CON, RWB-P5-E1026-APP and the edge stories.
- The end-to-end proof of these values across rwb-document, rwb-agent, rwb-litigation and rwb-case: RWB-ITG-E2030-ITG.
- The `rwb_document` schema baseline, the `rwb.document.events.v1` topics and consumer groups, the observability and the runbook of this service.
