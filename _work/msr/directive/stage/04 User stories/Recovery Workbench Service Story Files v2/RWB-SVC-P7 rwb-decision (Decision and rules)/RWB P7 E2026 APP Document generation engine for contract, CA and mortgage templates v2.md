# RWB-P7-E2026-APP Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P7-E2026-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P7-AG |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2026-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-026 for rwb-decision; the generation decision record in the central ledger and its two reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 19 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (FCR), a case owner and an internal audit reader**, I want **the decision record of every generated contract, credit approval and mortgage document set written once in the central decision ledger of `rwb-decision` — decision code D6.4 with final call GENERATED, the template codes and versions, the treatment, the merge snapshot reference, the case and the requesting role — append only, hash chained and readable by case and by entry**, so that **every generated set can be traced to the decision that produced it, a generation whose record cannot be written does not proceed, and the record that explains a customer document can never be quietly changed**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-026:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record path of DP-03.
- One deliverable and nothing else: the generation decision record in the ledger. On the record of a generation — decision code D6.4 with final call GENERATED, the template codes and versions, the treatment reference, the merge snapshot reference, the case and the requesting role — the service appends one `decision_log_entry` in `rwb_decision` through the decision-record path of DP-03, hash chained and append only, written in the same transaction as the generation it records, and it serves the two decision-log reads so an officer and an auditor can read it by case and by entry.
- What stays with `rwb-document` (P5, RWB-P5-E2026-APP and RWB-P5-E2026-CON): the template selection, the merge field resolution, the value formatting, the render to PDF/A-2b, the draft store, the `document` row, the `DocumentStored` event and the call into the record path inside its own transaction. None of it is rebuilt here.
- What stays with `rwb-comms` (P6, RWB-P6-E1046-APP and RWB-P6-E1034-APP): the template catalog, the template versions, the Legal approval of a version and the merge field catalog.
- What stays with `rwb-treatment` (S2, RWB-S2-E2026-APP): the treatment, its approval at D6.4 before generation, its `decision_log_id` and its outcome.
- What stays with `rwb-access` (P4, RWB-P4-E2026-APP): the session, the role, the scope, the Documents right C and the Decision log right R behind the two reads.
- The record and the generation are one pair under DP-03: the producing service writes the record through the record path inside the generation transaction, and this service appends it to the ledger in one atomic transaction of its own, so a generation with no record is refused with MSG-P7-003 and a record with no generation is never appended. Where the sources read the two writes differently the conflict is GAP-1289 and the reading applied is ASM-2288.
- The service records and exposes the decision; it selects no template, resolves no merge field, formats no value, renders no file and writes no document, no treatment and no case (BR9).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1287; ASM-2282); this story uses the phrase "the rwb-decision login (DP-02)" and never the shared monolith login.

The legacy behaviour carried into the decision service is unchanged in meaning: one record for the generated set and no exception, the template code and version of every generated document on that record, the inputs reference so the set can be reproduced, a record that cannot be altered once written, and no generation standing without its record (legacy RWB-E2-026 AC1, AC7, AC13, AC14 and BR7).

### 2. Business rationale

Deed in lieu and restructure document sets are typed today from the case file into word processor templates, and a wrong amount or an old template wording reaches the customer. The generation engine of `rwb-document` now fills each Legal-approved template version from the case facts and refuses a missing value or an unapproved version. That engine is only defensible if the decision behind the set is recorded: which template codes and which versions produced the three documents, on which treatment, from which merge snapshot, for which case and under which requesting role. The monolith wrote that record with the document rows in one process and one schema, so the two could not drift apart. In the target the generation is `rwb-document`'s and the evidence of every decision is collected in `rwb-decision` (Architecture v5 slides 14, 28 and 41), so the record has to be appended there, chained and unchangeable, and readable by the officer who asked for the documents and by the auditor who later asks why.

Under Architecture v5 the central decision ledger, the rule registry and the approvals are `rwb-decision` (slides 14, 27, 28 and 41); each service writes its decision record through the local library in the same transaction as the change it records and publishes `DecisionRecorded` on `rwb.decision-record.v1` (slide 20, "every service"); `rwb-decision` collects the records into the ledger and seals it daily in write-once storage (slide 28); and the ledger is read through the decision-log operations (slide 14). The realignment changes the mechanism, not the business rule:

1. The in-process decision-log write of the generation engine becomes the decision-record path of DP-03: the record is written where the generation commits and is appended here on the shared topic `rwb.decision-record.v1`, with the append-only rule and the hash chain the FSD already carries (FEAT-DRI-01, FEAT-DRI-03).
2. The record is not a copy of the document and not a copy of the values: it names the case, the treatment, the template codes and versions, the requesting role and a reference to the merge snapshot. The transfer price, the title deed number, the borrower name, the Thai long date and the file itself stay in `rwb_document` (BR5, BR12).
3. The decision code D6.4 and the final call GENERATED are data: the code is a value of LOV-DECISION read through the reference-data contract of `rwb-case` (DP-07), and the final call is a row of this service's own vocabulary, never a literal (BR8).
4. The template catalog and the Legal approval stay with `rwb-comms`, the treatment with `rwb-treatment`, the generation with `rwb-document` and the authorise answer with `rwb-access`; this story reads none of their tables (DP-01, DP-11) and rebuilds none of their rules.
5. The one decision-log read of the monolith becomes two operations on the service's own base (DP-13): search the ledger by case, decision code, rule, approver and date, and read one entry with its inputs reference and its chain fields.
6. The data-lake copy of the log is retired with the data lake (DP-17); the ingest of `rwb.decision-record.v1` is continuous Kafka and the daily chain check JOB-14 at 02:00 covers these entries like any other.
7. The record is append only and hash chained, so a refused generation leaves no entry, a repeated record leaves one entry, and a break in the chain is a reportable event rather than a silent edit.

This story meets REQ-DCM-012 and REQ-OCC-002 on the record side: it proves which approved template version produced each document of the set and that the set's decision is recorded before anything reaches the customer, and it carries control CTL-14 (only an approved template version leaves) and the principle that no action proceeds unlogged (CTL-06, R-UNI-39). It puts the generation half of REQ-DRI-001, REQ-DRI-002, REQ-DRI-003 and REQ-DRI-005 in place and leaves the template approval, the merge fields, the render, the store, the treatment and the access answer where their owners have them.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2026-CON | The published generation contract of `rwb-document` (P5): the generation request for case `RW-2026-000301`, treatment `TRT-0301` and template `DIL-CONTRACT` version 2 under request key `K-0301`, the declaration of the record on `rwb.decision-record.v1` with decision code D6.4, final call GENERATED and a reference to the merge snapshot, and the contract fakes. Which fields of the generation record this service consumes is Not specified in the source documents (GAP-1287; ASM-2282), and the field set this story assumes is that of ASM-2282 |
| RWB-PLT-E1027-CON | The decision-record path and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule and the idempotency key the record carries |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the page-size bound of the search and the completeness target of the ingest; the parameter names are Not specified in the source documents (GAP-1287; ASM-2283) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION, which holds D6.4, and the final-call list, with the version in force on the business date; the final-call list has no name in the sources (GAP-1287; ASM-2284) |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one entry under a repeated record, the inbox dedupe and the outbox row of the append |
| RWB-PLT-E1044-CON | The per-service Flyway sequence of `rwb_decision` (DP-15), in which this story adds one index step and no table |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which SCR-38 Decision log query and the reader's view reach the two operations |
| The `rwb-decision` decision-log store baseline | `decision_log_entry` with the columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE, the unique key on the idempotency key and the chain check JOB-14 at 02:00. The baseline is the service's own earlier work and is in no H row of this story: the dependency is carried in GAP-1288 and ASM-2287 |
| The authorise answer of `rwb-access` (P4) | `POST /api/recovery/access/v1/authorise` (Architecture v5 slide 14) for the Decision log right R and the caller's scope behind the two reads; consumed, faked and in no C row of this story (GAP-1288; ASM-2287) |

Business preconditions carried from RWB-E2-026:

- Case `RW-2026-000301` with product group `MORTGAGE`; treatment `TRT-0301` of type `DEED_IN_LIEU` on that case with `decision_log_id` set (approved at D6.4) and no outcome yet; treatment `TRT-0302` of the same type with no `decision_log_id`, which reaches no record at all.
- Templates `DIL-CONTRACT` version 2 in Thai for `MORTGAGE` with `approved_by_legal` true, `DIL-CA`, `DIL-MORTGAGE` and `RES-AGREEMENT` for restructure are loaded; the template codes are assumed (DL28) and their field-level identity is `rwb-comms`'s.
- The template-to-document-type mapping is data: `DIL-CONTRACT` to CONTRACT, `DIL-CA` to CREDIT_APPROVAL, `DIL-MORTGAGE` to MORTGAGE_DOCUMENT and `RES-AGREEMENT` to CONTRACT (assumed; DL19). This story reads none of it.
- The case facts of the merge fields are `transfer_price` 1250000.00, `title_doc_no` "12345" and `contract_date` 2026-12-10. They stay in `rwb-source-data` and `rwb-document` and never enter an entry of this story (BR5).
- The caller holds Documents C (RW-RESTRUCT or RW-CASEOWN) on the case in scope, or is the service identity `SY-CASEWF`; and every role of TSD P7 v2 T6.1 holds R on the decision log.
- The record under test is produced by the generation contract fake of RWB-P5-E2026-CON with request key `K-0301` for the single template and for the three-template set.
- No build dependency. Day 1: the story builds against RWB-P5-E2026-CON and its fakes.
- Open decisions (each still open, each with an assumption): DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL19 (ASM-1051, ASM-1164, ASM-1809, ASM-1810); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355); DL28 (ASM-1861, ASM-1925, ASM-2093, ASM-2727).

### 4. Flow

1. `rwb-document` (P5): generates the requested set for case `RW-2026-000301`, treatment `TRT-0301` and the template codes of the request, and in the same transaction writes its document rows, its outbox row and, through the decision-record path of DP-03, the D6.4 record with final call GENERATED, the template codes and versions, the treatment reference, the merge snapshot reference, the case and the requesting role `RW-RESTRUCT` (RWB-P5-E2026-APP; Architecture v5 slide 28).
2. The record path publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID, with the record's entry ID and idempotency key `K-0301` (DP-09; slide 42, event 08).
3. `rwb-decision` `GenerationRecordListener`: reads the fact into the inbox of DP-09, deduplicates by event ID and by the record's idempotency key (R-UNI-40), keeps the facts whose decision code is D6.4 and whose final call is GENERATED, and passes them to `DecisionLogAppendService`. Every other decision code is the decision-log baseline's general ingest and not this story's.
4. `DecisionLogAppendService`: reads the decision code list and the final-call list through the reference-data contract of DP-07 at the version in force, requires the decision code, the final call and, for a D6.4 record, at least one template code with its version; a record that fails the check is refused with MSG-P7-003 naming the missing field and nothing is written (BR8, BR11).
5. `DecisionLogAppendService`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash` (64 zeros for the first), computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with `inputs_ref` pointing at the merge snapshot, and writes the inbox row of the fact and the idempotency row of the key. A failed append changes nothing: no entry, no chain position and no inbox row (BR3, BR13).
6. A repeated fact with the same idempotency key returns the first entry's ID, adds one to the repeat count for R-UNI-40 and appends nothing (BR7). A second append for the same treatment, template and version is refused with 409 and MSG-GEN-004, so a set has one entry and not two (BR6).
7. A restructuring officer, a case owner or an internal audit reader reads the ledger with `GET /api/recovery/decision/v1/decision-log` by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; each row of the page holds `entryId`, `chainSeq`, the case, the decision code, the template codes and versions, the treatment reference, the requesting role, the inputs reference, the final call, `decidedAt`, `prevHash` and `entryHash` (BR10).
8. The same reader reads one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, with the same fields and the merge snapshot reference, never the snapshot and never a merge value.
9. A caller whose authorise answer carries no Decision log right is refused with 403 and MSG-P4-002; a case outside the caller's scope is refused with 404 and MSG-P4-003, and no entry of that case is returned (BR10).
10. Nothing in this story moves a document, a treatment, a case or a template: the entry is written beside the generation and the readers of `rwb-case`, `rwb-document` and the auditor's screen keep their own state (BR9). The daily chain check JOB-14 at 02:00 covers these entries like any other and is the baseline's, not rebuilt here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record names no template code, or a template code with no version | The append is refused, nothing is written and no chain position is used | MSG-P7-003 | AC4, AC9 |
| X2 | The decision code is not a value of LOV-DECISION at the version in force | The append is refused and the fact stays on the topic for redelivery; nothing is written | MSG-P7-003 | AC4 |
| X3 | The decision log store is unavailable, or the chain position cannot be taken | The generation is not recorded: `rwb-document` answers 503, its set is rolled back and its draft files are removed; an incident is raised as in R-UNI-39 | MSG-P7-003 | AC4 |
| X4 | The same record is delivered again, or replayed from the topic | One entry exists; the inbox dedupe and the idempotency key both hold, and the repeat is counted for R-UNI-40 | None | AC6 |
| X5 | A second append arrives for the same treatment, template and version | The second append is refused and the first entry stands | MSG-GEN-004 | AC6 |
| X6 | A generation is refused by its own checks: a missing merge value, a template version not approved by Legal, a withdrawn template, no template for the product group, a treatment that is not approved | The record path is never called, so no entry is appended for the refused request and no chain position is used | MSG-P5-010, MSG-P6-003 (produced by the owners of the checks) | AC9 |
| X7 | A correction of an entry is needed | A new entry is appended with `corrects_entry_id` naming the entry it corrects; the corrected entry is unchanged | None | AC5 |
| X8 | An UPDATE or a DELETE is attempted, through the service role or the schema owner | The statement is refused by the missing grant and by `tr_declog_append_only`; the entry is unchanged and the attempt is audited | None | AC5 |
| X9 | The caller holds no Decision log right, or asks for a case outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; no entry is returned | MSG-P4-002, MSG-P4-003 | AC7 |
| X10 | The reference list or the parameters cannot be read at the version in force | The append or the read is refused rather than assumed, and the fact is retried; no entry is written with an assumed code or an assumed final call | MSG-P7-003 | AC4 |

An entry is only ever appended beside the generation that caused it: the entry, its chain position, its inbox row and its idempotency row are written in one transaction, so a generation can never leave a half record and a record can never exist for a generation that was refused (BR13).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the generation contract RWB-P5-E2026-CON, the decision-record path of DP-03, the reference-data and parameters libraries and the fakes; no template selection, merge resolution, render, store, treatment or access behaviour is rebuilt here |
| Negotiable | The decision code, the final-call set, the payload field set, the parameter names and the message ids are data or parameters of their owners; the story fixes only the record, the append-only rule, the chain and the two reads |
| Valuable | Every generated document set can be traced to the decision that produced it, with its template versions and its merge snapshot reference, and that explanation cannot be quietly changed |
| Estimable | One listener, one appender with the chain, one query controller with two operations, one index step and one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the nine criteria in section 7 runs as one automated test against the contract fakes, with a fixed business date and a fixed chain |

### 7. Acceptance criteria

No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E2-026, and every legacy criterion of the key changes a document, a template or a treatment, which belongs to RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-S2-E2026-APP or RWB-P4-E2026-APP. The eleven criteria below are new for the `rwb-decision` slice and test only the generation record and its two reads; each keeps the legacy values of RWB-E2-026 and adds no business value.

```gherkin
Feature: The generation decision record of rwb-decision

  Background:
    Given the environment is SIT
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given a restructuring officer with role RW-RESTRUCT in scope of the case
    Given the rwb-document contract mock returns the generation of template "DIL-CONTRACT" version 2 for treatment "TRT-0301" under request key "K-0301"
    Given the rwb-comms template catalog fake returns template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the rwb-treatment fake returns treatment "TRT-0301" of type "DEED_IN_LIEU" with decision_log_id set and no outcome
    Given the rwb-access fake returns the authorise answer allowing role RW-RESTRUCT the Decision log right R on case "RW-2026-000301"
    Given the decision-record library fake returns the D6.4 record of the generation with final call "GENERATED"

  Scenario: AC1 One chained D6.4 GENERATED entry for a generated set (new, D-RCV-60)
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    Given the rwb-document contract mock returns the D6.4 record of case "RW-2026-000301" for treatment "TRT-0301" and template "DIL-CONTRACT" version 2, with request key "K-0301", the merge snapshot reference and the requesting role "RW-RESTRUCT"
    When the ledger consumes rwb.decision-record.DecisionRecorded.v1 for that record
    Then one decision_log_entry exists with decision code "D6.4", final call "GENERATED", case reference "RW-2026-000301", treatment reference "TRT-0301", requesting role "RW-RESTRUCT", template code "DIL-CONTRACT" and template version 2
    Then the entry carries the merge snapshot reference and no merge value: neither "1250000.00", nor "12345", nor "2026-12-10" as a case fact appears in it
    Then the entry carries a chain_seq, a prev_hash equal to the entry_hash of the entry before it, and an entry_hash equal to the SHA-256 of its canonical form
    Then GET /api/recovery/decision/v1/decision-log/{entryId} returns that entry with finalCall "GENERATED" and the same prevHash and entryHash

  Scenario: AC2 A three-document set is one record naming three template codes and versions (new, D-RCV-60)
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    Given the rwb-document contract mock returns one D6.4 record for treatment "TRT-0301" under request key "K-0301" naming "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1
    When the ledger consumes that record
    Then exactly one decision_log_entry is appended for request key "K-0301", and not three
    Then the one entry names the three template codes with their versions
    Then GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000301&decision=D6.4 returns that entry once and no second entry for treatment "TRT-0301"
    Then the entry carries no document identifier, because the document rows are rwb-document's

  Scenario: AC3 A later template version leaves the earlier entry on its version (new, D-RCV-60)
    Given template "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15
    Given document "DOC-0310" was generated on 2026-12-10 from version 2 and the ledger holds the D6.4 entry of that generation with template version 2
    When the ledger consumes the D6.4 record of a generation on 2026-12-15 for template "DIL-CONTRACT" version 3
    Then the new entry carries template version 3
    Then the entry of 2026-12-10 still carries template version 2 and its decidedAt is unchanged
    Then the two entries are read in decidedAt order by GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000301
    Then template version 2 stays readable in the template catalog, which is rwb-comms's and is not copied into the ledger

  Scenario: AC4 A record that cannot be appended stops the generation (new, D-RCV-60)
    Given the decision log store does not accept writes
    Given the rwb-document contract mock holds the generation of treatment "TRT-0301" and template "DIL-CONTRACT" open in one transaction with the decision-record path of rwb-decision
    When the decision-record path refuses the append
    Then the record path answers the generation with status 503 and MSG-P7-003
    Then no entry exists for "TRT-0301" and no chain_seq is consumed
    Then no document row, no draft file and no DocumentStored event exist for the request, and an incident is raised as in R-UNI-39
    When the same request key "K-0301" is retried and the store accepts the append
    Then one entry is appended and it takes the chain_seq the refused write did not use

  Scenario: AC5 The ledger is append only and hash chained (new, D-RCV-60)
    Given an entry for case "RW-2026-000301" with chain_seq 1 and final call "GENERATED" is stored
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the rwb-decision login and again through the schema owner role
    Then all four statements are refused: by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged
    Then the refused attempts are written to the ACE audit log with the table, the operation and the entry ID
    When a correction of the entry is taken
    Then a new entry is appended with corrects_entry_id naming it, and the corrected entry is still unchanged

  Scenario: AC6 A repeated record gives one entry and a duplicate append is refused (new, D-RCV-60)
    Given the record of request key "K-0301" was appended and the ledger returned its entry ID
    When the same record with request key "K-0301" arrives again
    Then one entry exists for the request, the first entry ID is returned and the repeat count of R-UNI-40 is raised by one
    Then no second entry and no second chain position are written
    When a second append arrives for treatment "TRT-0301" and template "DIL-CONTRACT" version 2 under a different key at the same time
    Then the second append is refused with status 409 and MSG-GEN-004 and the first entry stands

  Scenario: AC7 The two reads return the entry with its chain fields and are scoped (new, D-RCV-60)
    Given the entry of AC1 is stored for case "RW-2026-000301"
    When an authorised reader sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 200 with the decision code "D6.4", the final call "GENERATED", the template code "DIL-CONTRACT", the template version 2, the treatment reference "TRT-0301", the merge snapshot reference, the requesting role "RW-RESTRUCT", decidedAt, prevHash and entryHash
    Then the response carries no merge value, no borrower name and no national ID number
    When the same reader sends GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000301&decision=D6.4 with page 1 and the page-size bound in force
    Then the page holds that entry and the total count of the case
    Given case "RW-2026-000306" is in team "HP-NE" and the officer's scope is team "FCR-BKK"
    When the officer sends GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000306
    Then the response is 404 with MSG-P4-003 and no entry of that case is returned
    Given the rwb-access fake returns MSG-P4-002 for the caller's Decision log right R
    When that caller sends GET /api/recovery/decision/v1/decision-log
    Then the response is 403 with MSG-P4-002 and no entry is returned

  Scenario: AC8 The entry carries codes, versions and references and no value (new, D-RCV-60)
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    Given the rwb-document contract mock returns the D6.4 record of the three-template set of treatment "TRT-0301" with the merge snapshot reference "inputs/2026-12-03/7f3a" and the case facts transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10 behind it
    When the ledger consumes and appends the record
    Then the entry holds the three template codes with their versions, the treatment reference "TRT-0301", the case reference "RW-2026-000301", the requesting role "RW-RESTRUCT" and the merge snapshot reference "inputs/2026-12-03/7f3a"
    Then the entry, its event payload and its audit line hold neither "1250000.00", nor "1,250,000.00 baht (one million two hundred fifty thousand baht)", nor "12345", nor "10 December 2569 BE", nor "DOC-0310", nor "DOC-0311"
    Then the file, its bytes and the merge snapshot itself stay in rwb_document

  Scenario: AC9 A refused generation leaves no entry and the chain stays unbroken (new, D-RCV-60)
    Given template "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved
    Given template "DIL-CA" has only version 1 with approved_by_legal false
    Given case "RW-2026-000305" has product group "HIRE_PURCHASE" and template "DIL-CONTRACT" exists only for product group "MORTGAGE"
    Given treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id
    When the generation of each of those requests is refused with MSG-P6-003 naming "DIL-MORTGAGE", with MSG-P5-010 naming "DIL-CA" version 1 and naming "DIL-CONTRACT" for "HIRE_PURCHASE", and with the treatment refusal of "TRT-0302"
    Then the record path is never called and no entry names "TRT-0302", "DIL-CA" or "DIL-MORTGAGE" for those requests
    Then the last entry of the ledger keeps its entry_hash
    When the generation of treatment "TRT-0301" and template "DIL-CONTRACT" version 2 then succeeds
    Then its entry takes the next chain_seq and its prev_hash equals the entry_hash of the last entry

  Scenario: AC10 A record missing a required field is refused and the personal data and boundary rules hold (new, D-RCV-60)
    Given the rwb-document contract mock returns the D6.4 record of treatment "TRT-0301" with no template version
    When the ledger consumes rwb.decision-record.DecisionRecorded.v1 for that record
    Then the record path answers the generation with MSG-P7-003 and appends no entry
    When the same record arrives with the decision code, the final call and the template code "DIL-CONTRACT" with version 2
    Then one decision_log_entry is appended and it holds no personal value, no borrower name and no national ID number
    Then the ingest of rwb.decision-record.v1 is continuous Kafka and the daily seal of the ledger is the baseline's, not this story's
    Then the ledger reads come one hop from the gateway-bff composite route and the service reads no table of another service

  Scenario: AC11 A caller without an authenticated session gets 401 from the two reads (new, D-RCV-60)
    Given the entry of AC1 is stored for case "RW-2026-000301"
    When a caller without an authenticated session sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 401 and no entry is returned
    When the same caller sends GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000301&decision=D6.4
    Then the response is 401 and no entry is returned
```

The eleven criteria are new, and `acs` is empty for this story: no legacy criterion of RWB-E2-026 is owned verbatim here, because each of them changes a document, a template version, a treatment or an access answer and belongs to its own slice. The values are the legacy values — case `RW-2026-000301` with product group `MORTGAGE`, cases `RW-2026-000305` and `RW-2026-000306`, treatments `TRT-0301` and `TRT-0302` of type `DEED_IN_LIEU`, templates `DIL-CONTRACT` version 2, `DIL-CA`, `DIL-MORTGAGE` and `RES-AGREEMENT`, product groups `MORTGAGE` and `HIRE_PURCHASE`, teams `FCR-BKK` and `HP-NE`, `transfer_price` 1250000.00, `title_doc_no` "12345", `contract_date` 2026-12-10 and "10 December 2569 BE", "1,250,000.00 baht (one million two hundred fifty thousand baht)", documents `DOC-0310` and `DOC-0311`, request key "K-0301", role `RW-RESTRUCT`, decision code D6.4, and the messages MSG-P7-003, MSG-GEN-004, MSG-P5-010, MSG-P6-003, MSG-P4-002 and MSG-P4-003 — and no new business value is introduced. The merge snapshot reference shape, the payload field set of the record, the request and answer shape of the two reads, the decision code and final-call value set, the message id set of this slice and a panel id for the record have no source and are carried in GAP-1287 with ASM-2282 to ASM-2286. The `-ITG` copies of the test cases belong to RWB-ITG-E2026-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One entry per generation request: a single-template generation and a three-template set each leave exactly one entry, and the entry of a set names every template code and version of it | Legacy RWB-E2-026 AC1, AC13, AC14; FSD P7 v3 A2.2; REQ-DRI-001 |
| BR2 | The entry carries decision code D6.4 and final call GENERATED, written through the decision-record path of DP-03; the decision code is read from LOV-DECISION at the version in force and is never a literal | Legacy RWB-E2-026 AC1; TSD P7 v2 T3.1 and T3.2; BR-P7-002; DP-07 |
| BR3 | Every entry is hash chained: a `chain_seq`, a `prev_hash` equal to the previous entry's `entry_hash` (64 zeros for the first) and an `entry_hash` equal to the SHA-256 of the entry's canonical form; the daily check JOB-14 at 02:00 covers it | REQ-DRI-003; FSD P7 v3 AC-ALT-P7-001-01; Architecture v5 slide 28 |
| BR4 | The log is append only: an entry is never changed and never deleted, and a correction is a new entry naming the one it corrects in `corrects_entry_id` | REQ-DRI-002; FSD P7 v3 AC-P7-001-01 and A2.1 |
| BR5 | The entry names the case, the treatment reference, the template codes and versions, the requesting role and a reference to the merge snapshot; it never carries a merge value, a formatted value, a file byte or a personal value | Legacy RWB-E2-026 BR11 and section 17; DF-PTY-007; CTL-11; DL26; §R7.2 s17 |
| BR6 | A set is recorded whole or not at all: a refused set leaves no entry, and a second append for the same treatment, template and version is refused | Legacy RWB-E2-026 BR8; R-UNI-39 |
| BR7 | One entry under a repeated record: the inbox dedupe and the idempotency key make a second entry impossible, and the repeat is counted | Legacy RWB-E2-026 BR9; FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40 |
| BR8 | The final call is a data row, not a constant; the value set is this service's vocabulary and a change to it is a reference-data change and not a release | BR-P7-002; TSD P7 v2 T3.2; GAP-1287 with ASM-2284 |
| BR9 | The story records and exposes; it selects no template, resolves no merge field, formats no value, renders no file, stores no document and changes no treatment, case or template | Architecture v5 slides 14 and 41; DP-01 |
| BR10 | The two reads declare the Decision log right R with the scope applied; a role without it is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003 | TSD P7 v2 T-A.1, T6.1 and T6.2; REQ-DRI-012 |
| BR11 | A record that lacks its decision code, its final call or, for D6.4, a template code with its version is refused with MSG-P7-003 and appends nothing; no entry is written from an assumed value | FSD P7 v3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05 read on this slice; REQ-DRI-001 |
| BR12 | No personal data in the entry, the inputs reference, the event, the audit line, the tests or the logs, and no template body or merge snapshot anywhere but in `rwb_document` | Architecture v5 slide 11; REQ-DRI-001; legacy RWB-E2-026 section 17 |
| BR13 | The entry, its chain position, its inbox row and its idempotency row commit in one transaction; a failed append leaves nothing and the fact is redelivered, and a generation that cannot be recorded does not proceed | Principle 5; R-UNI-39; FSD P7 v3 A2.5; DP-03 |
| BR14 | The ingest of `rwb.decision-record.v1` is continuous Kafka and the entries reach the ledger inside the completeness target of Architecture v5 slide 28; the daily seal of the ledger to write-once storage is the baseline's | Architecture v5 slides 28 and 44 (JOB-13); TSD P7 v2 T5.3 |
| BR15 | The ledger reads are one hop from the gateway-bff composite route and the service reads no table of another service: the template, the treatment, the case and the authorise answer arrive on their contracts or as facts | Architecture v5 slides 13 and 41; DP-01; DP-11; DP-19 |

### 9. State transitions

None for a document, a template, a treatment or a case. The states below are the states of an entry of this story, and the entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | `DecisionRecorded` arrives with decision code D6.4 and final call GENERATED | The code is in LOV-DECISION, at least one template code carries its version, and the chain head is known | Appended at the next `chain_seq`, with its `prev_hash`, its `entry_hash`, its inbox row and its idempotency row in one transaction |
| Absent | `DecisionRecorded` arrives with a decision code outside the list, or with no template version | The record fails the check of BR11 | Absent: refused with MSG-P7-003, no chain position used, the fact redelivered |
| Absent | `DecisionRecorded` arrives, and the store or the chain is unavailable | The append cannot commit | Absent: MSG-P7-003, nothing written, the generation rolled back and an incident raised |
| Appended | The same record arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A duplicate append for the same treatment, template and version arrives | The first entry of that set stands | Unchanged: the second append is refused with MSG-GEN-004 |
| Appended | A correction is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`, and the corrected entry stays unchanged |
| Appended | An UPDATE or a DELETE is attempted | Any caller, including the schema owner | Unchanged: the statement is refused by the append-only rule |
| Appended | The daily chain check and the daily seal run | JOB-14 and the seal of the baseline | Sealed: the entry is unchanged and the chain is verified |

The generated document stays in state DRAFT in `rwb_document`, the treatment stays approved and open in `rwb_treatment` and the template version stays in force in `rwb_comms`; this story changes none of them (BR9).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Requests the generation that produces the record (Documents C on a case in scope) and reads the entry of that case (Decision log R) |
| RW-CASEOWN, case owner | The same, for the treatment of the case in scope |
| SY-CASEWF, case workflow identity | Requests the rule-driven generation of Epic 3 as a service identity, under the same checks as a person (NFR-051); the record it causes names the role as the requesting role |
| SY-DECLOG, decision record writer | Writes the D6.4 record inside the generation transaction at the producer and appends it to the ledger here; the append is the service identity's and not a person's |
| RW-AUDIT, internal audit | Reads the ledger by case, by decision code and by date range, and one entry with its merge snapshot reference and its chain fields (Decision log R, scope ALL) |
| RW-COMPLY, Compliance and PDPA officer | Reads the same and never a merge value, which the entry never carries |
| Every role of TSD P7 v2 T6.1 | Holds R on the decision log and reads the entries of the cases in its scope |
| A role outside the matrix, or a case out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, and appends the entry, its inbox row and its idempotency row (DP-02) |
| `rwb-document` | Owns the generation, the template selection, the render, the store, the document rows and the write of the record in its own transaction; this story holds no authority over any of them |
| `rwb-comms`, `rwb-treatment`, `rwb-access` | Own the template version and its Legal approval, the treatment and its `decision_log_id`, and the role, scope and right answer; this story writes none of them |
| No approval level from the delegation of authority applies | The treatment itself was approved at D6.4 before generation; this story records the generation and reads no `delegation_limit` row |

The authorisation decision behind the two reads is `rwb-access`'s role, scope and right data, taken through the authorise answer the service already holds; this story adds no guard of its own and holds no role, scope or delegation row (ASM-2287). The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1287; ASM-2282); the story refers to "the rwb-decision login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id (the case reference `RW-2026-000301`) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code (D6.4, a value of LOV-DECISION) | Write |
| DF-DEC-004 | `decision_log_entry` | rule_id | Not written by the generation record: no rule fires at generation; the treatment approval that allowed it is its own entry |
| DF-DEC-005 | `decision_log_entry` | rule_version | Not written, for the same reason |
| DF-DEC-006 | `decision_log_entry` | model_version | Not written: no model takes part in a generation |
| DF-DEC-007 | `decision_log_entry` | agent_version | Not written: no agent takes part in a generation |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the merge snapshot reference, with the freshness of each input) | Write |
| DF-DEC-009 | `decision_log_entry` | recommendation | Not written: a generation follows an approved treatment and proposes nothing |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Not written: the approval of the treatment is the D6.4 entry of the decision center and another story's |
| DF-DEC-011 | `decision_log_entry` | approval_level | Not written, for the same reason |
| DF-DEC-012 | `decision_log_entry` | final_call (GENERATED) | Write |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written: a generation is not an override |
| DF-DEC-014 | `decision_log_entry` | actions (the template codes with their versions, the treatment reference and the requesting role) | Write; the container is TSD P7 v2 T3.1 and its content for this record is Not specified in the source documents (GAP-1287; ASM-2282) |
| DF-DEC-015 | `decision_log_entry` | outcome | Write where the generation names one (the stored document set), as identifiers only |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017 | `decision_log_entry` | prev_hash | Write |
| DF-DEC-018 | `decision_log_entry` | entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id (the service identity of the append) | Write |
| DF-DEC-031 | `decision_log_entry` | idempotency_key (`K-0301`) | Write |
| DF-CAS-001, DF-CAS-002, DF-CAS-003 | `recovery_case` (P3) | id, case_no, product_group | Read through the generation contract answer, never a table |
| DF-TRT-001, DF-TRT-003, DF-TRT-004, DF-TRT-013 | `treatment` (S2) | id, decision_log_id, treatment_type, outcome | Read as facts of the record, never a table |
| DF-REF-045 to DF-REF-051 | `template` (P6) | template_code, template_version, language, approved_by_legal | Read as facts of the record; the catalog itself is never read here |
| DF-DEC-019 to DF-DEC-021 | `approval` (P7) | not touched | Not read and not written by this story; DF-DEC-019 and DF-DEC-021 are not in LDM v9 and are not used by this story |
| (reference lists) | reference data (P3) | LOV-DECISION and the final-call list, with the version in force | Read through the reference-data contract of DP-07, never a table |
| (parameters) | `parameter_value` (P3) | the page-size bound and the completeness target | Read through the parameters contract of DP-06, never a table |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_decision` | the outbox row of the append where the service publishes one | Write |
| (idempotency) | `idempotency_key` | the record's key `K-0301` and the first entry ID | Write |

No row of `recovery_case`, `treatment`, `template`, `merge_field`, `document`, `document_hub_parameter` or `delegation_limit` is copied into `rwb_decision`: the case, the treatment and the template arrive as facts of the record, and the merge snapshot and the file stay in `rwb_document` (DP-01). The transfer price 1250000.00, the title deed number "12345", the contract date 2026-12-10, the Thai long date "10 December 2569 BE" and the documents `DOC-0310` and `DOC-0311` are named in this document as legacy values only and are written in no entry of this story (BR5). Field IDs are those of the Logical Data Model and Data Dictionary v9; the container of the template list and the requesting role inside `actions` is the reading of ASM-2282 and is Not specified in the source documents (GAP-1287; ASM-2282).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007) and the Ownership Map gives to P7. The request and response field set of a generation entry is Not specified in the source documents (GAP-1287; ASM-2283).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | API-P7-006: search the ledger by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | API-P7-007: read one entry with its decision code, its final call, its template codes and versions, its treatment reference, its merge snapshot reference, its requesting role and its chain fields; 200 with the DecisionLogEntry | Decision log, right R, scope applied | Not applicable, read only |

The DecisionLogEntry body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `finalCall`, `inputsRef`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`, and for a generation entry the template codes with their versions, the treatment reference and the requesting role. The DecisionLogPage body carries `items`, `page`, `size` and `total`. The field-level shape is the reading of ASM-2283.

Errors: 401 no session (messageId Not specified in the source documents (CG-ALL-7310)); 403 the role lacks the Decision log right (MSG-P4-002); 404 the entry or the case is absent or outside the scope (MSG-P4-003); 422 a query value is outside its list (messageId Not specified in the source documents (CG-ALL-7310)); 503 the ledger is unavailable (messageId Not specified in the source documents (CG-ALL-7310)). Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001) is a P7 operation of the decision center and belongs to the approval and recommendation stories of this service; this story declares it neither as provided nor as consumed.

Screen states of SCR-38 Decision log query and SCR-30 Case documents are in the state table of section 15 (CG-ALL-7317; CG-ALL-7316); this story builds no screen.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access (Architecture v5 slide 14) | The cached role, scope and Decision log right decision behind the two reads; consumed, faked, one hop with a 2 s timeout and a breaker (DP-11), and in no C row of this story (GAP-1288; ASM-2287) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION, which holds D6.4, and the final-call list, at the version in force (DP-07); faked |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The page-size bound of the search and the completeness target of the ingest (DP-06); faked |

The six fakes of this slice stand behind those rows and behind the record under test: the **rwb-document generation contract fake** (RWB-P5-E2026-CON) poses the generation and its D6.4 record, the **rwb-comms template catalog fake** supplies the template code and version the record names, the **rwb-treatment fake** supplies the treatment with its `decision_log_id`, the **rwb-access fake** answers the authorise call, the **decision-record library fake** (RWB-PLT-E1027-CON) supplies the append, the chain and the append-only refusal, and the **central ledger fake** supplies the ledger reference and the completeness reading. The generation record itself arrives on `rwb.decision-record.v1` and not over REST. The contract dependency recorded on the story is RWB-P5-E2026-CON; the platform and published contracts the DP table adds are listed in section 13 and carried in GAP-1288.

#### 12.3 Events published

None. This story publishes no event of its own: the generation record is a fact of `rwb-document` on `rwb.decision-record.v1` and the entries of the ledger are read through the operations of 12.1. `rwb.decision.DecisionRecorded.v1` is published by the owning service of each decision and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42, event 08). The `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` events of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger and its shared topic; published by `rwb-document` for the generation decisions | `GenerationRecordListener`: inbox dedupe by event ID and by the record's idempotency key, then `DecisionLogAppendService` for the decision code, the final call, the template codes and versions, the treatment reference, the merge snapshot reference, the case and the requesting role |

The fact carries IDs, codes, versions and a snapshot reference only; no merge value, no formatted value, no party name and no file byte travels on the topic (BR5, BR12). Which fields of the fact this service requires is Not specified in the source documents (GAP-1287; ASM-2282); the reading this story applies is that of ASM-2282.

#### 12.5 Workflows and activities

None. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09; the generation's own activity runs on queue `rwb-document` and is neither started nor signalled here. This story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit.

#### 12.6 Schedules

None. The ingest of `rwb.decision-record.v1` is continuous Kafka, as JOB-13 states (Architecture v5 slide 44), and the daily chain check JOB-14 at 02:00 is the decision-log baseline's and covers these entries like any other; the daily seal of the ledger to write-once storage is the baseline's too. This story creates no Temporal Schedule and starts nothing on a clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The generation entry, its template codes and versions, its treatment reference, its inputs reference, its final call and its chain position; append only |
| `approval` | P7 (`rwb_decision`) | Not read and not written here: the approval of the treatment is the decision center's |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read in this story: the generation evaluates no rule package |
| decision record (local library) | P7 rows in `rwb_decision`, written through the decision-record path | The append of DP-03 and its hash chain |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `document`, `document_type` and `document_hub_parameter` (P5), `template` and `merge_field` (P6), `treatment` (S2), `recovery_case`, `parameter_value`, `lov_value` and `reference_row` (P3), `role`, `permission`, `masking_rule` and `delegation_limit` (P4). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document generation contract fake | RWB-P5-E2026-CON | The generation of case `RW-2026-000301`, treatment `TRT-0301` and template `DIL-CONTRACT` version 2 under request key `K-0301`; the three-template set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1; the later version 3 valid from 2026-12-15; the withdrawn `DIL-MORTGAGE`; `DIL-CA` version 1 not approved; case `RW-2026-000305` with product group `HIRE_PURCHASE`; treatment `TRT-0302` with no `decision_log_id`; the refused render |
| rwb-comms template catalog fake | RWB-P6-E1046-CON | Template `DIL-CONTRACT` version 2 in Thai for `MORTGAGE` with approved_by_legal true, version 3 valid from 2026-12-15, `DIL-CA` version 1 not approved, `DIL-MORTGAGE` withdrawn, and no template for `HIRE_PURCHASE` |
| rwb-case contract fake | P3 rwb-case (§12.2) | The admin lists `LOV-DECISION` and the final-call list at the version in force, and the admin parameters (the page-size bound and the completeness target); fake library version Not specified in the source documents (DOR-RWB-P7-E2026-APP-22) |
| rwb-treatment fake | The S2 treatment contract | Treatment `TRT-0301` of type `DEED_IN_LIEU` with `decision_log_id` set and no outcome; treatment `TRT-0302` with no `decision_log_id` |
| rwb-access fake | The P4 authorise contract of Architecture v5 slide 14 | The allow answer for role `RW-RESTRUCT` and for `SY-CASEWF` with the Decision log right R and the case in scope; the refusal of MSG-P4-002 for a caller without the right; case `RW-2026-000306` in team `HP-NE` against scope `FCR-BKK` for MSG-P4-003 |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the idempotency key `K-0301`, and a forced failure for AC4 |
| central ledger fake | The ledger side of `rwb.decision-record.v1` | The ledger reference of the entry, the completeness reading of the ingest, the replay of the same fact and the duplicate append of AC6, and the chain head AC9 asserts against |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 3 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the authorise answer and the two `rwb-case` reads consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the generation activity is `rwb-document`'s and the chain check is the baseline's |
| File | None | No file input and no file output; the rendered file and the merge snapshot never leave `rwb-document` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/generation`, Java package `th.co.scb.ace.workbench.recovery.decision.generation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which pattern has an instance in this slice: DP-03 is the record itself — the append through the decision-record path, the `prev_hash` and `entry_hash` chain, the append-only rule and the shared topic `rwb.decision-record.v1`, with its H RWB-PLT-E1027-CON. DP-01 is the boundary — the entry lives in `rwb_decision`, and the template, the treatment, the case and the document are never read as tables. DP-06 is the page-size bound and the completeness target read as parameters; DP-07 is LOV-DECISION and the final-call list read as reference data with the version in force; DP-09 is the inbox dedupe, the idempotency key and the outbox row of the append; DP-11 is the one hop with a 2 s timeout and a breaker on the authorise call and on the two `rwb-case` reads; DP-15 is the index step this story adds in the service's own Flyway sequence; DP-19 is the gateway-bff route through which SCR-38 Decision log query reaches the two operations.

DP-05 has an instance only as an absence: this service reads no `v_ace_*` view and no ACE table, and the party, the collateral and the case facts behind the merge fields never enter it, because the record carries the case and treatment references and a merge snapshot reference and no value (BR5). The engine that fills those fields is RWB-P5-E2026-APP.

The platform H dependencies of the DP table — H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON — and the C dependencies of the published contracts of other services — C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the authorise contract of P4 — are not in the metadata rows of this story, which name None and RWB-P5-E2026-CON; they are the dependencies the DP table adds and they are recorded in GAP-1288 and ASM-2287. The decision-log store baseline of this service (`decision_log_entry`, its append-only trigger and its JOB-14 check) is not in the metadata H row either and is carried in the same gap and assumption. None of them blocks the build beyond Day 1: they are platform and store contracts of waves 0 and 1 and the published contracts of `rwb-case` and `rwb-access`, built against their fakes. The six platform H dependencies, the two rwb-case C dependencies, the store baseline and the rwb-access authorise contract are carried in the dependency map as DP-added; Ready to start stays Day 1 because each H is a platform CON story or the service's own baseline and each C is built against its published contract and fake; the metadata rows are corrected at the next version of the story set.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GenerationRecordListener | Kafka consumer with the inbox | Reads `DecisionRecorded` on `rwb.decision-record.v1`, deduplicates by event ID and by the record's idempotency key, keeps the D6.4 and GENERATED facts and hands them to the appender; every other decision code stays with the baseline's general ingest |
| DecisionLogAppendService | Service | Checks the decision code, the final call and the template code and version of the record, and writes the entry, its chain position, its inbox row and its idempotency row in one transaction (BR2, BR11, BR13) |
| ChainHasher | Service | The canonical form of an entry and its SHA-256, the first `prev_hash` of 64 zeros and the `prev_hash` of every later entry (BR3) |
| DecisionLogQueryController | Controller | The two operations of 12.1 with the declared right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogQueryService | Service | The search and the single read, the row shape of a generation entry, and the total count of the page |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, insert only, with the search indexes and the idempotency key |
| ReferenceListClient | Client | LOV-DECISION and the final-call list through the reference-data contract of DP-07 with the version in force |
| ParameterClient | Client | The page-size bound and the completeness target through the parameters contract of DP-06 |
| AuthoriseClient | Client | The cached authorise answer of `rwb-access` behind the two reads, one hop with a 2 s timeout and a breaker (DP-11) |

**Database and migrations**

- Writes `decision_log_entry`, its inbox and idempotency rows and its outbox row, all in schema `rwb_decision`; reads no other schema (DP-01).
- The table, its columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE and the unique key on the idempotency key belong to the decision-log store baseline of the service and are not rebuilt here (GAP-1288). The trigger `tr_declog_append_only` is a database object of that baseline, not a field of the data dictionary.
- One migration step in the per-service Flyway sequence (DP-15): `V2026_1__decision_log_generation_index.sql` adds the composite index `ix_declog_generation_case ON decision_log_entry (case_id, decision_code, decided_at DESC)` that the generation search uses. The index name is Not specified in the source documents (GAP-1287; ASM-2283).
- No row of `document`, `template`, `treatment`, `recovery_case` or `parameter_value` is written here: those tables are their owners' and arrive as facts or through their contracts. The schemas rwb_case, rwb_comms, rwb_document and rwb_treatment belong to rwb-case, rwb-comms, rwb-document and rwb-treatment; this story reads and writes none of them.

**Configuration and reference data**

- LOV-DECISION, which holds D6.4, and the final-call list are reference data read through DP-07 with the version in force; the value D6.4 is the legacy decision code and the final-call list has no name in the sources (GAP-1287; ASM-2284).
- The page-size bound of the search and the completeness target of the ingest are parameters of DP-06; their names are Not specified in the source documents (GAP-1287; ASM-2283), and the story holds no default.
- The merge snapshot reference is an opaque string of the shape `inputs/<businessDate>/<hash>`, following the inputs reference of FSD P7 v3 AC-ALT-P7-001-02; this story validates nothing of its content and never resolves the snapshot (GAP-1287; ASM-2282).
- The outbox retry policy and the inbox retention are the platform's (RWB-PLT-TE006-CON).
- No feature switch of this story's own is named by a source; the capability is present wherever a generation record arrives and the record path of the producer is the only switch, which is `rwb.document.generation-engine` of RWB-P5-E2026-APP (GAP-1287; ASM-2286).

**Build steps**

1. `DecisionLogRepository` and the index step; test the search by case and by decision code and the single read, and that an INSERT outside a transaction is refused (AC7).
2. `ChainHasher` and the canonical form: `chain_seq`, `prev_hash` from the previous entry, the first `prev_hash` of 64 zeros and `entry_hash` as the SHA-256 of the canonical form (AC1, AC5).
3. `GenerationRecordListener` with the inbox and the dedupe by event ID and idempotency key; test the replay of the same fact and the duplicate append of AC6.
4. `DecisionLogAppendService` with the checks of BR11 and the fail-closed transaction; test the forced failure of AC4 and the chain position the refused write does not use.
5. The append-only rule: the trigger and the grant, with the four statements of AC5 refused and the audit line written.
6. `ReferenceListClient` and `ParameterClient` with the version in force, and the refusal rather than an assumed code or final call (BR11, X10).
7. `DecisionLogQueryController` with the declared right, the scope, the paging and the problem mapping; tests for AC7, MSG-P4-002 and MSG-P4-003 (TC-E2-026-15).
8. `AuthoriseClient` against the authorise fake, and the contract-fake run of the whole slice: the document, catalog, treatment, access and ledger fakes green from Day 1.
9. The boundary test: no write to `rwb_document`, `rwb_comms`, `rwb_treatment` or `rwb_case`, and no merge value, formatted value or file byte in any entry, event payload or log line (AC8, BR5).

**Done when.** The tests of section 16 pass, the chain of a SIT day verifies from the first entry with no break, a three-document set leaves one entry naming the three template codes and versions, a refused generation leaves none and does not consume a chain position, a repeated record leaves one entry, both reads answer inside the 2 s budget of the frame, and no document, template, treatment or case was changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | A generation record cannot be appended, or the record lacks a value the entry requires | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record path, on the append; the generation answers it with 503 and rolls its set back |
| MSG-GEN-004 | A second append arrives for the same treatment, template and version | Someone else changed this record. Reload it to see their change. | This story, on the duplicate append of AC6 |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of the read |
| MSG-P4-003 | The case or the entry is outside the caller's scope | This case is not in your scope. | This story, through the authorise answer of the read |
| MSG-P5-010 | No current template version approved by Legal, or no template for the product group | {template} has no version approved by Legal for {product} in {language}. | `rwb-document` on the generation; this story asserts it and never rewrites it |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-comms` through the generation; this story asserts it and never rewrites it |

MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-GEN-004, MSG-P5-010 and MSG-P6-003 are copied unchanged from RWB-E2-026 section 14 and the FSD P7 v3 message set. The message id set of this slice beyond these six has no source and is carried in GAP-1287 with ASM-2285. Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one: 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-GEN-004, and 503 with MSG-P7-003 on the record path.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by SCR-38 Decision log query, which searches the log by case, rule, approver and date with export (FSD P7 v3 Screens), and by the auditor's view of the ledger; both are reached through the gateway-bff composite route of DP-19 and are another story's. SCR-30 Case documents and the generation screens stay `rwb-document`'s and RWB-E2-017's, and this story feeds neither of them.

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The D6.4 entries of the case in decidedAt order, each with its template codes and versions, its treatment reference, its requesting role and its final call |
| SCR-38 Decision log query (P7) | Empty | Not specified in the source documents (CG-ALL-7317) |
| SCR-38 Decision log query (P7) | Loading | Not specified in the source documents (CG-ALL-7317) |
| SCR-38 Decision log query (P7) | Error | Not specified in the source documents (CG-ALL-7317) |
| SCR-38 Decision log query (P7) | No access | Not specified in the source documents (CG-ALL-7317) |
| The entry read | One entry | The same row with its merge snapshot reference, its `decidedAt`, its `prevHash` and its `entryHash` |
| The entry read | An entry with `correctsEntryId` | The correction beside the entry it corrects, and the corrected entry unchanged |
| The read | 403, or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for a case outside the scope; no row is returned |
| SCR-30 Case documents (rwb-document) | Empty | Not specified in the source documents (CG-ALL-7316) |
| SCR-30 Case documents (rwb-document) | Loading | Not specified in the source documents (CG-ALL-7316) |
| SCR-30 Case documents (rwb-document) | Error | Not specified in the source documents (CG-ALL-7316) |
| SCR-30 Case documents (rwb-document) | No access | Not specified in the source documents (CG-ALL-7316) |

A panel or screen id for showing the generation record beside the documents on SCR-30, and the field list of SCR-38, are Not specified in the source documents (GAP-1287; ASM-2286). The screen field list and the composite route specification belong to RWB-PLT-N001-CON and to the story that owns SCR-38.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15 | Access, AC7, BR10; legacy Covers "Access" | Component | RW-TEAMMGR user (Documents R) calls the generate operation; refused with MSG-P4-002 |
| TC-E2-026-01 | AC1, BR1, BR3; legacy Covers "AC1, BR1, BR4, BR6" | Component | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 |
| TC-E2-026-02 | AC9, BR3; legacy Covers "AC2, BR3" | Component | Case with no title deed number |
| TC-E2-026-03 | AC3, BR2; legacy Covers "AC3, BR10" | Contract | Template v3 valid from 2026-12-15 |
| TC-E2-026-04 | AC9, BR6; legacy Covers "AC4, BR1" | Component | DIL-CA v1 not approved |
| TC-E2-026-05 | AC9, BR6; legacy Covers "AC5, BR2" | Component | DIL-MORTGAGE withdrawn |
| TC-E2-026-06 | AC9, BR6; legacy Covers "AC6, BR5" | Component | Treatment with no decision_log_id |
| TC-E2-026-07 | AC4, BR13; legacy Covers "AC7, BR7" | NFR | Decision log stub refusing writes |
| TC-E2-026-08 | AC6, BR7; legacy Covers "AC8, BR9" | Component | Same Idempotency-Key twice |
| TC-E2-026-09 | AC9, BR6 | Component | Two parallel requests |
| TC-E2-026-10 | AC9, BR6; legacy Covers "AC10" | Component | Damaged template body |
| TC-E2-026-11 | AC9, BR6; legacy Covers "AC11, BR1" | Component | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC7, BR10; legacy Covers "AC12" | Component | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-13 | AC2, BR1; legacy Covers "AC13" | Component | Three current templates |
| TC-E2-026-14 | AC2, AC9, BR6; legacy Covers "AC14, BR8" | Component | Three templates, DIL-CA not approved |
| TC-E2-026-16 | AC4, BR13; legacy Covers "Principle 5" | NFR | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |
| TC-E2-026-17 | AC8, BR5; section 12.7 tables | Component | Write attempted to rwb_document, rwb_comms, rwb_treatment and rwb_case, and a merge value in an entry; refused, nothing written |
| TC-E2-026-18 | AC10, BR11, BR12, BR14, BR15 | Component | Record with no template version; refused with MSG-P7-003 and no entry; personal value check; ingest and gateway-bff boundary check |
| TC-E2-026-19 | AC11; BR10 | Component | Unauthenticated caller of the two reads; 401 and no entry returned |

The sixteen legacy test cases of RWB-E2-026 are kept in the order of the work package, and each is answered here on the record side: the entry, its template versions, its chain, its two reads and its refusals. The generation, the render, the store, the template status and the treatment state are the contract fakes' and their own services'. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The `-ITG` copies of these cases end in `-ITG` and belong to RWB-ITG-E2026-ITG, which runs the same values across the five contracts. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision code, the final-call set, the page-size bound, the completeness target and the message ids are reference or parameter rows, and the template codes, treatment types and document types are facts of their owners; nothing of them is a constant here.
- No personal data in the entry, the inputs reference, the event, the audit line, the tests or the logs: the case reference, the treatment reference, the template codes and versions, the decision code, the final call, the hashes and dates only. The borrower name, the national ID number, the transfer price, the title deed number and the file byte stay in `rwb_document` (BR5, BR12).
- No read of another service's tables (DP-01): the template and the treatment arrive as facts of the record, the case and the reference lists through the `rwb-case` contracts, the authorise answer through `rwb-access`, and the document never at all.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- One appender and no mover: this story changes no document, no template, no treatment and no case, so a decision record can never move a case (BR9).
- No entry without its record and no record without its generation: the entry, its chain position, its inbox row and its idempotency row commit in one transaction, and a generation whose record cannot be written is rolled back with an incident (BR13, R-UNI-39).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the chain is verifiable from `chain_seq` 1 (BR3, BR4).
- One entry per generation: the inbox dedupe, the idempotency key and the refusal of a duplicate append make a second entry impossible (BR6, BR7).
- One base and one topic: `/api/recovery/decision/v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no monolith base and no other service's base or topic is declared here as this service's own.
- One hop and 2 s with a breaker per downstream on the authorise call and the two `rwb-case` reads; an unreadable list or parameter refuses the append rather than writing an assumed value (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-17 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11 |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the versions, the inputs snapshot, the recommendation, the approval, the actions and the outcome | Business Requirements Program, section 5.6; Epic 1 | FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-03 | 17 Run the decision center | BR1, BR2, BR5, BR11 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-13 |
| REQ-DRI-002 | The decision log is append only; a correction is a new record naming the one it corrects | Business Requirements Program, section 5.6; Epic 1 | FEAT-DRI-01 | 17 Run the decision center | BR4 | TC-E2-026-01, TC-E2-026-13 |
| REQ-DRI-003 | The decision log is hash chained and the chain is checked every day | Business Requirements Program, section 5.6; Epic 1 | FEAT-DRI-01 | 17 Run the decision center | BR3 | TC-E2-026-01, TC-E2-026-03 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.6; Epic 1 | FEAT-DRI-05 | 17 Run the decision center | BR13 | TC-E2-026-07, TC-E2-026-16 |
| REQ-DRI-012 | Audit can query the decision log for a population of cases with the inputs, the versions and the final call | Epic 2, section 3.7; Program, section 5.7 | FEAT-APD-01 | 17 Run the decision center | BR10 | TC-E2-026-12, TC-E2-026-15 |

REQ-DRI-001, REQ-DRI-002, REQ-DRI-003, REQ-DRI-005 and REQ-DRI-012 are carried on this story only for the generation record and its two reads; the rest of the ledger, the approvals and the rule registry belong to the other P7 stories of this service.

| Legacy reference | Where it is kept |
|---|---|
| One decision log entry for the generated set, with the template code and version of each document | Sections 1, 2, 4, 7 (AC1, AC2), 8 (BR1, BR2), 11 |
| The three-template set recorded as one entry, and the set whole or not at all | Sections 1, 5, 7 (AC2, AC9), 8 (BR1, BR6) |
| Decision code D6.4 and the treatment approved before generation | Metadata, sections 1, 3, 7, 8 (BR2), 11, 13 |
| The merge snapshot reference and the rule that no merge value is copied | Sections 1, 4, 7 (AC1, AC8), 8 (BR5), 11, 17 |
| A generation that cannot be recorded does not proceed (legacy AC7) | Sections 5 (X3), 7 (AC4), 8 (BR13), 14 |
| Append only and hash chained, with the first `prev_hash` of 64 zeros | Sections 4, 7 (AC5), 8 (BR3, BR4), 9 |
| The repeat with the same Idempotency-Key "K-0301" (legacy AC8) | Sections 5 (X4), 7 (AC6), 8 (BR7) |
| The template version applies from its valid-from date and earlier documents keep theirs (legacy AC3, BR10) | Section 7 (AC3), 8 (BR2) |
| Template codes DIL-CONTRACT, DIL-CA, DIL-MORTGAGE and RES-AGREEMENT, product groups MORTGAGE and HIRE_PURCHASE, documents DOC-0310 and DOC-0311 | Sections 3, 7, 11, 16 |
| Teams FCR-BKK and HP-NE, cases RW-2026-000301, RW-2026-000305 and RW-2026-000306, treatments TRT-0301 and TRT-0302 | Sections 3, 7, 11, 16 |
| Messages MSG-P7-003, MSG-GEN-004, MSG-P5-010, MSG-P6-003, MSG-P4-002 and MSG-P4-003 | Section 14, exception paths |
| Rules R-DIL-14, R-DIL-16, R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38, R-UNI-39 and R-UNI-40 | Sections 2, 8, 18 |
| Legacy key RWB-E2-026, story RWB-P7-E2026-APP, contract RWB-P5-E2026-CON | Metadata, sections 3, 12 |
| Test cases TC-E2-026-01 to TC-E2-026-16 | Section 16 |
| Decoupling patterns DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P5-E2026-APP and RWB-P5-E2026-CON the selection, the merge resolution, the formatting, the render, the store, the document rows and the `DocumentStored` event; RWB-P6-E1046-APP and RWB-P6-E1034-APP the template catalog, the versions and the Legal approval; RWB-S2-E2026-APP the treatment and its `decision_log_id`; RWB-P4-E2026-APP the session, the scope and the rights; and RWB-ITG-E2026-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope

- The generation engine: the template selection, the merge field resolution, the value formatting, the render to PDF/A-2b and the draft write. RWB-P5-E2026-APP, with the contract in RWB-P5-E2026-CON.
- The `document` row, the `DocumentStored` event (EV-16) and the write-once switch on send: RWB-P5-E2026-APP and RWB-P5-E2017-APP.
- The template catalog, the merge field catalog, the template versions and their Legal approval: RWB-P6-E1046-APP, RWB-P6-E1034-APP and `rwb-comms`.
- The treatment, its approval at D6.4 and its `decision_log_id`: RWB-S2-E2026-APP and `rwb-treatment`; the approval entry itself is the decision center's and another P7 story's.
- The session, the role, the scope, the Documents right C and the Decision log right R: RWB-P4-E2026-APP and `rwb-access`.
- The recommendation read `GET /cases/{caseId}/recommendation`, the approval operations, the approval queue SCR-10, the decision screen SCR-11 and the rule registry: the other P7 stories of this service. This story evaluates no rule package and loads no Drools kit.
- The general ingest of every other decision code into the ledger, the append-only table itself, the daily chain check JOB-14 at 02:00 and the daily seal: the decision-log baseline of this service.
- The data-lake copy of the log, JOB-13 and lake retention: retired with the data lake (DP-17); the ingest of the ledger is continuous Kafka.
- SCR-38 Decision log query as a built screen, the SCR-30 panel and the composite route: the screen stories and RWB-PLT-N001-CON.
- The e-signature flow (RWB-E2-018), the generation, review and send screens (RWB-E2-017), rule-driven generation at TRANSFER_PRICE_SET (FEAT-TRT-18, Epic 3) and debt sale agreements and notices (FEAT-DBS-10, Epic 6), as the legacy story left them.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E2026-ITG.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
