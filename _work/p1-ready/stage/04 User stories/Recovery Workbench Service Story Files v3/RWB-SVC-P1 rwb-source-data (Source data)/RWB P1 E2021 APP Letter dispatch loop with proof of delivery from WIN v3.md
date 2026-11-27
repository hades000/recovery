# RWB-P1-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not set in this story; the squad sizes it at refinement (DOR-RWB-P1-E2021-APP-16) |
| Epic design | Not specified in the source documents (DOR-RWB-P1-E2021-APP-14) |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P1-W |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2021-CON; RWB-P1-E1066-CON (extended in this service); RWB-P1-E1016-CON (record read) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), base path /api/recovery/source-data/v1 |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-009, RD-P1-011, RD-P1-021, RD-P1-023, RD-P1-045, RD-P1-064 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (no FR mapped to REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- One ledger path family and the full `InteractionRequest` 5.1.0; delivery entries are appended by rwb-comms, not by a P1 story (RD-P1-007). Findings #1, #5.
- The DP02 contact row is published as `fields: FieldValue[]` on the record read (RD-P1-005); finding #1.
- The barcode fold groups by `externalRef` and breaks a tie on `caseSeq`. The dispatch entry and the delivery entry share the WIN barcode (RD-P1-064; GAP-3520 closed). Finding #2.
- RD-P1-064: the dispatch entry carries `sourceRef` INT-14 WIN and the business key `LETTER-<caseNo>-<yyyyMMdd>-<noticeId>` (AC2); rwb-comms is the one writer of delivery and hand-recorded proof entries. Test case IDs follow Test Cases v9; message texts follow Error and Message Standard v6.
- Shared Problem body, status codes and idempotency rules (RD-P1-001, RD-P1-004); time limits pending (finding #3).
- ACs rewritten with uuid case identifiers and keys, AC20 to AC22 added, test case references corrected. Finding #4.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-source-data. The legacy dispatch loop read the borrower's postal contact point and its consent, ran the conduct check, wrote the letter into the INT-14 file, read the INT-15 proof back and appended the outcome to the interaction ledger as one mutable entry, in one deployable and one transaction. Under D-RCV-60 that loop is rwb-comms' and rwb-case's: the notice, the template, the conduct check, the WIN file, the proof read, the notice state and the notice-period timer belong to P6, P3, P2 and P1's own proof-of-delivery story. This story answers the one fact the conduct check needs from this service — the postal contact point and its consent, as rows of data product DP02 on the record read of `/api/recovery/source-data/v1` (DP-05, DP-13) — and it owns the two ledger facts of the letter: the dispatch entry with its conduct check and its barcode, and the fold that makes one barcode read as its latest outcome, on `POST` and `GET /cases/{caseId}/interactions` of the interaction ledger this service owns (DP-01, DP-18). No WIN file, no conduct check, no notice state, no decision record, no notice-period timer, no `NoticeDispatched` or `NoticeDelivered` event and no `notice` or `template` table is delivered here. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P1-E2021-APP-L64, X20 RWB-P1-E2021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 44 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **dispatch loop of rwb-comms (service actor)**, I want **the postal contact point of a person and its consent to come back as data-product rows of rwb-source-data that carry the contact key, the type, the consent status, the verified date and the data date and never the address, and the dispatched letter to be appended to this service's interaction ledger with its conduct check and its barcode so that the barcode reads as its latest proof outcome, in order and never rewritten**.

This is the rwb-source-data slice of legacy RWB-E2-021. The legacy story read the contact point, ran the conduct check, wrote the file, read the proof and appended the outcome in one step. Under D-RCV-60 that step has four owners, and this story delivers the fact it consumes and the ledger it owns, and nothing else:

- **the contact-and-consent branch of the record read** on base `/api/recovery/source-data/v1`: `GET /data-products/DP02/records?caseId=` (case uuid) answers, for the case's parties, one row per contact point as `fields` entries `contactKey` (the token of `v_ace_contact`), `contactType`, `consentStatus` resolved from `contact_point_ext` as data (GIVEN, WITHDRAWN or UNKNOWN) and `verifiedAt`, with the page's `dataAsOf` (the DP02 business date). It answers no address, no name and no identity number: the contact point is a reference and is never copied;
- **the letter append** on `POST /cases/{caseId}/interactions` of the ledger this service owns, with the members the loop holds: `eventCode` `LETTER`, `channel` `LETTER`, `conductCheck` (PASSED or BLOCKED), `deliveryStatus` from `LOV-SEND-STATUS`, `externalRef` (the barcode) and `occurredAt`, written through the writer, its `case_seq` allocator, its `Idempotency-Key` rule and its append-only trigger;
- **the case ledger read** `GET /cases/{caseId}/interactions`, which answers every entry as stored and, where an entry carries an `externalRef`, the governing status of that barcode — the `deliveryStatus` of the entry with the latest `occurredAt` among the entries of the same `externalRef`, the higher `caseSeq` winning a tie — so a caller reading the dispatch entry sees the outcome the proof entry later recorded;
- **no loop**: no WIN file, no INT-14 or INT-15 handling, no conduct check implementation, no notice state, no notice-period timer, no event, no decision record and no `notice`, `template` or `merge_field` table. The `v_ace_pod` read is RWB-P1-E1055-APP's, the proof entry is appended by rwb-comms (RWB-P6-E1055-APP), and the proof window, the transfer and the case timer are RWB-P6-E2021-APP's and RWB-P3-E2021-APP's.

It owns no screen: the states of SCR-04 (empty, loading, error and no access) are rwb-case's (RWB-P3-E2021-APP) and those of SCR-18 are rwb-comms'. It owns no legacy acceptance criterion. AC1 to AC12 of RWB-E2-021 are proved in RWB-P6-E2021-APP (AC1, AC2, AC4, AC5, AC6, AC7, AC8, AC10, AC12), RWB-P3-E2021-APP (AC2, AC3, AC6, AC7), RWB-P7-E2021-APP (AC9), RWB-P4-E2021-APP (AC11) and RWB-ITG-E2021-ITG (the cross-service proof of the whole key). This story is written with new criteria tagged D-RCV-60, each one testing only the read, the append and the fold above.

The shapes the loop consumes are declared by RWB-P6-E2021-CON: it names the rwb-source-data answers of the loop — the postal contact point with its consent fact, and the interaction ledger write with its channel, its summary and its conduct check — and fakes them. This story implements them and publishes its fragment with the service baseline.

### 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent while a contact stop or a legal hold is in force is a conduct breach. Legacy RWB-E2-021 exists to make one thing true: the day a letter is served is the day the proof says it was served, and the conduct check that allowed it is on the record (REQ-OCC-003, REQ-OCC-005; CTL-15, CTL-16).

Two facts carry that promise in the target, and both are this service's. The first is the consent of the postal contact point: the Workbench holds the decision about a contact point (`contact_point_ext`) and ACE holds the contact point itself (`v_ace_contact`), and the conduct check must read the pair without either being copied into the other (D-RCV-35 U1; ADR-010; REQ-OCC-006). The second is the ledger entry of the letter: one ordered, append-only history per case, written in the same transaction as the action it records (REQ-ILG-010; NFR-070). The letter that says "sent on 2026-12-15, barcode RR223344556TH" and the proof that says "undeliverable on 2026-12-21" are two facts about one barcode, and a history that overwrites the first with the second cannot answer the question a conduct review asks — what was known, and when.

**What D-RCV-60 changes.** Not one business value. The notice `N-0101`, the case `RC-2026-000321`, the notice type `DEMAND`, the template `DEMAND-SSME` `TH` version 1, the barcode `RR223344556TH`, the sent date 2026-12-15, the call-back date 2026-12-18, the proof window of 7 days and the rule ids R-LIT-05, R-LIT-07, R-LIT-08 and R-LIT-09 keep their meaning and their values. What changes is where the fact is read and who owns it: a read of DP02 over `/api/recovery/source-data/v1`, one hop and 2 s (DP-05, DP-11, DP-13), and an append to this service's own ledger instead of an in-process call into the monolith (DP-01, DP-18).

**One read, one append, no copy.** No table of this service holds the address, the name or an identity value of the borrower, and none is answered, logged or put in an event (§12.3, §17). The contact point is a token, the barcode is a reference, and the entry carries codes and dates.

### 3. Preconditions

Nothing in this list is a build dependency: this story is Day 1 and builds against the published baseline, the published view contract, the ledger writer and the RWB-P6-E2021-CON fake, which is why its build dependency list is empty.

- The service baseline of rwb-source-data is published: schema `rwb_source_data`, the per-service Flyway sequence at its baseline version, `data_product` with DP01 to DP14 and `data_product_load` with its unique key on `(product_code, business_date)` (DP-01, DP-15; the baseline of RWB-P1-E1001-APP and RWB-P1-E1015-APP, adopted as published artefacts).
- The record read `GET /data-products/{productCode}/records` of API-P1-010 is published with its DP01 and DP04 branches (RWB-P1-E1016-APP, RWB-P1-E2010-APP), and this story adds the DP02 contact-and-consent row type to it.
- `contact_point_ext` exists at the baseline with `contact_key`, `contact_type` (PHONE, EMAIL, ADDRESS), `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` and the standard record columns (TSD P1 T3.5, DF-EXT-013 to DF-EXT-019).
- The view contract of RWB-P1-E1069-APP is published and `recovery.v_ace_contact` is readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on `public` (DP-02, DP-05; TSD P1 T3.3, T3.4, T6.3; ADR-010).
- The interaction ledger of RWB-P1-E1066-APP is published: the append, the case read, the entry read, the `Interaction` and `InteractionRequest` 5.1.0 schemas, the `case_seq` allocator, the unique key on `idempotency_key`, the append-only trigger `tr_interaction_append_only` (a database trigger object of the writer's migration in RWB-P1-E1066-APP, not an LDM entity or field), and the four ledger columns this story writes, `conduct_check` (DF-INT-012), `delivery_status` (DF-INT-028), `external_ref` (DF-INT-029) and `source_ref` (DF-INT-017), which are already in the service schema. No migration is needed.
- RWB-P6-E2021-CON is published with its fake: the postal contact point with its consent fact and the ledger write with its channel, its summary and its conduct check. This story builds against that contract and its fake and against no second draft of it (C).
- rwb-comms (RWB-P6-E1055-APP) reads the proof rows from `GET /proof-of-delivery?businessDate=` of RWB-P1-E1055-APP and appends one `LETTER` entry per matched row through `POST /cases/{caseId}/interactions`; this story reads that entry, folds it and writes no proof row (RD-P1-007 rule 7 as amended by RD-P1-064). A proof recorded by hand is also appended by rwb-comms only.
- The reference lists this story validates against — `LOV-LEDGER-EVENT`, `LOV-CONDUCT`, `LOV-SEND-STATUS` and the contact types — reach this service through the reference-data client library of DP-07; the Work Package lists no reference-data contract for this story, so the lists are read with a fixture until it is published (ASM-3533).
- The caller is the dispatch loop of rwb-comms with a workload identity token; officers read the outcome on SCR-18 and SCR-04 through gateway-bff and never call this service directly (DP-19).
- No approval is needed to build against a Draft contract baseline; RWB-P6-E2021-CON tags its baseline when its tests pass. This story starts on Day 1 and waits for nothing it builds.
- The DP02 row is `fields: FieldValue[]` of the published record read (RD-P1-005 rule 4); the consent vocabulary GIVEN, WITHDRAWN and UNKNOWN is built as ASM-3527 (GAP-2181); the ledger paths are the case-scoped family only (RD-P1-007 rule 2; GAP-2182; ASM-3528).

### 4. Flow

1. The dispatch loop of rwb-comms starts its 16:00 run for business date D and selects the notices whose conduct check it has still to take (the run, its Schedule and its workflow are RWB-P6-E2021-APP's; DP-10).
2. Before the check of notice `N-0101`, the loop calls `GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321` (case number `RC-2026-000321`), one hop with a 2 s budget (DP-11; C RWB-P6-E2021-CON).
3. The record read of RWB-P1-E1016-APP resolves the case's parties; the DP02 branch reads `recovery.v_ace_contact` for them, left joins `contact_point_ext` on `contact_key` and orders the rows by `contact_key` (DP-05).
4. `ConsentStatusResolver` resolves `consentStatus` from the extension row — `consent_given` true is GIVEN, `consent_given` false with a `consent_at` is WITHDRAWN, no row or no `consent_at` is UNKNOWN — and from no value of its own (ASM-3527).
5. `FreshnessStampReader` answers `dataAsOf` and `productStatus` from the DP02 row of `data_product_load` for D; the rows carry no contact value, no address, no name and no identity number (AC1, AC7; BR2).
6. The loop takes its four conduct-check branches on its own facts and on this answer, and decides PASSED or BLOCKED with the reason and the rule id; this story takes no part in that decision and makes no statutory decision (RWB-P6-E2021-APP; R-LIT-05, R-UNI-10).
7. For a letter it dispatches, the loop appends `POST /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000321/interactions` with its own UUID in the `Idempotency-Key` header and the body of section 12.1: `eventCode` `LETTER`, `occurredAt` 2026-12-15, `actorType` `SERVICE`, `actorRef` `rwb-comms`, `sourceRef` `INT-14 WIN`, the business `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd of the sent date>-<noticeId>`, `channel` `LETTER`, `direction` `OUTBOUND`, `conductCheck` `PASSED`, `deliveryStatus` `SENT`, `externalRef` `RR223344556TH` and a summary naming notice type `DEMAND` and the barcode; the append runs the validation, the case check, the `case_seq` allocator and the insert of the writer (AC2; DP-18; RD-P1-007).
8. A letter the check held is appended the same way with `conductCheck` `BLOCKED`, the reason `CONTACT_STOP_X1` in its summary, no `deliveryStatus` and no `externalRef` (AC3).
9. The writer answers 201 with the stored entry, so what the loop holds is what was stored (AC2).
10. When the proof of the letter arrives, rwb-comms reads it from the proof-of-delivery read and appends a `LETTER` entry with the delivery result through the same operation; no P1 story appends it, and nothing of the dispatch entry is rewritten. The delivery entry carries `externalRef` = the `barcode` of the proof row, else its `noticeRef` when the barcode is null (a row with neither writes no entry), `occurredAt` = the call-back date at 00:00 Asia/Bangkok and the business key `LETTER-<caseNo>-<yyyyMMdd of the call-back date>-<UUID version 5 of podKey>`, so the dispatch and delivery entries fold together (AC4; RD-P1-064). Pending: the mapping of WIN `delivery_status` to SENT, DELIVERED, READ and FAILED, owner rwb-comms owner with the WIN interface owner, tracked as GAP-3285; interim the values of the RWB-P6-E1055-APP fixture.
11. A read of the case ledger answers both entries as stored and, on each, `barcodeStatus` as the governing status of the `externalRef`: the entry with the latest `occurredAt`, the higher `caseSeq` winning a tie (the read order of RD-P1-009 rule 7) (AC4, AC20).
12. A repeat with the same `Idempotency-Key` and body replays the stored 201; a new header key with an existing business `idempotencyKey` answers 200 with the existing entry; neither writes a second row (AC5). A refused `LETTER` entry (AC6) writes nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `productCode` is not served by this service or does not match its pattern, or `caseId` is missing or not a uuid | 400 `Problem` naming the field (for an unserved product, naming the owning service); no row | MSG-GEN-001 (caseId); MSG-GEN-007 (pattern); unserved product Pending (GAP-3272) | AC8 |
| X2 | A caller without the right calls the read or the append | 403, and the refusal is logged without a key value | MSG-P4-002 | AC9, AC14 |
| X3 | A view, `contact_point_ext` or the stamp does not answer inside 5 s, or answers an error | 503 with a problem body naming the ACE database; no row is guessed from a cache | MSG-GEN-006 | AC10, AC15 |
| X4 | A `LETTER` entry arrives with no `conductCheck` | 422 with the problem body naming the field; no entry is written | MSG-GEN-001 | AC6 |
| X5 | A `LETTER` entry arrives with a `deliveryStatus` and no `externalRef` | 422 with the problem body naming the field; no entry is written | MSG-GEN-001 | AC6 |
| X6 | The case of the append does not exist or is outside the caller's scope | 404 as the case check of the writer answers it, passed on unchanged; no entry is written | MSG-P4-003 | AC11, AC16 |
| X7 | The same `Idempotency-Key` header, or the same business key, arrives with a different body | 409; the stored entry is not overwritten | MSG-PLT-N009-05 | AC5 |
| X8 | The ledger cannot be written | The transaction rolls back, the caller receives 503, and no entry exists | MSG-P1-022 | AC12, AC17 |
| X9 | `externalRef` is longer than the 60 characters of DF-INT-029 | 422 with `field` `/externalRef`; the barcode is never truncated | MSG-GEN-002 | AC6 |
| X10 | No valid credential | 401; nothing is read or written | MSG-P4-001 | AC19 |
| X11 | The `Idempotency-Key` header is missing or not a UUID | 400; nothing is written | MSG-PLT-N009-03 | AC21 |
| X12 | Flag `rwb.source-data.ledger-letter` is off | The DP02 contact rows are answered 404 and the loop holds the notice; the append and the case read behave as before this story | Pending: message ID of the flag-off 404 (GAP-3506) | AC22 |

X1 and X3 are the read paths this story adds; X4 to X6 and X9 are the validation of the append; X7, X8, X10 and X11 are the refusals and the rollback the writer already ships and this story inherits unchanged. Pending: alignment of the 5 s statement timeout of X3 with the caller's 2 s budget, owner solution architect (GAP-3566); X3 is proved with a caller that has no shorter deadline. The conduct check, the contact stop, the legal hold, the withdrawn template, the proof window, the transfer and the decision record are the exception paths of RWB-P6-E2021-APP, RWB-P3-E2021-APP and RWB-P7-E2021-APP and are not carried here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E2021-CON and its fake, on the published baseline, the view contract of RWB-P1-E1069-APP, the record read of RWB-P1-E1016-APP and the writer of RWB-P1-E1066-APP; needs no live rwb-comms, rwb-case or WIN to start |
| Negotiable | The class split, the fold rule and the summary wording are the squad's choice behind the contract; the contact token, the consent vocabulary, the two operation paths and the barcode are fixed |
| Valuable | The conduct check runs on a consent fact that is read and not copied, and the letter and its proof are two facts in one ordered history that no later write can rewrite |
| Estimable | One row type on an existing read, one extended append with its read-back, one resolver and one fold |
| Small | Finished inside one sprint with its tests |
| Testable | Each criterion is one call against the contract fake, the ACE contact fixture, the extension fixture and the ledger fixture, with no second service and no file |
| Day 1 | The story has no build dependency; it is reachable on the first day of wave 2 and its tests run against the published baseline and the fake |

### 7. Acceptance criteria

```gherkin
Feature: Letter dispatch loop with proof of delivery from WIN — the source-data slice

  Background:
    Given the dispatch-eligible notice states are "APPROVED"
    Given the proof window is 7 days
    Given case "c0000000-0000-4000-8000-000000000321" has case number "RC-2026-000321"
    Given notice "N-0101" for case "RC-2026-000321" is "Approved" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1 Approved
    Given data product "DP02" is "LOADED" for business date 2026-12-14
    Given v_ace_contact holds one "ADDRESS" contact point "ADDRESS:ADDR-0001" for person "P0000123"
    Given contact_point_ext holds the row of "ADDRESS:ADDR-0001" with consent_given false, consent_at 2026-11-20 and verified_at 2026-10-02

  Scenario: AC1 The postal contact point and its consent come back as DP02 rows (new, D-RCV-60)
    When the dispatch loop calls GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321
    Then the answer is status 200 with dataAsOf 2026-12-14 and productStatus "LOADED"
    Then the answer holds 1 row whose fields are contactKey "ADDRESS:ADDR-0001", contactType "ADDRESS", consentStatus "WITHDRAWN" and verifiedAt 2026-10-02
    Then the answer holds no contact value, no address text, no person name and no identity number
    Then the answer states the consent fact only, and the statutory decision on notice type "DEMAND" stays with rwb-comms under R-UNI-10

  Scenario: AC2 A dispatched letter is one LETTER entry with its conduct check and barcode (new, D-RCV-60)
    Given the rwb-comms contract mock returns the conduct check "PASSED" for notice "N-0101"
    When the dispatch loop posts to the case with Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000001" a body with eventCode "LETTER", occurredAt 2026-12-15T16:00:00+07:00, actorType "SERVICE", actorRef "rwb-comms", sourceRef "INT-14 WIN", idempotencyKey "LETTER-RC-2026-000321-20261215-9e000000-0000-4000-8000-000000000101", channel "LETTER", direction "OUTBOUND", conductCheck "PASSED", deliveryStatus "SENT", externalRef "RR223344556TH" and a summary naming "DEMAND" and "RR223344556TH"
    Then the answer is status 201 with the stored entry, its caseSeq and sourceSystem "WORKBENCH"
    Then one interaction row holds those values and no decision record and no event is written
    Then the entry carries no address, no person name and no identity number

  Scenario: AC3 A letter held by the conduct check is one BLOCKED entry with no barcode (new, D-RCV-60)
    Given the rwb-comms contract mock returns the conduct check "BLOCKED" for notice "N-0101" with the reason "CONTACT_STOP_X1"
    When the dispatch loop appends the letter of notice "N-0101" of case "RC-2026-000321" with conduct check "BLOCKED", the reason "CONTACT_STOP_X1" in its summary and occurred time 2026-12-14 with Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000002" and its own business key
    Then the answer is status 201 and the entry carries conduct check "BLOCKED", no delivery status and no external ref
    Then the entry carries no address, no person name and no identity number
    Then no notice state, no hold reason on the notice, no decision entry and no case task is written here, and those stay with rwb-comms and rwb-decision

  Scenario: AC4 The proof is a second entry and the read folds the barcode to its latest status (new, D-RCV-60)
    Given the letter of "RR223344556TH" is on the ledger of case "RC-2026-000321" with delivery status "SENT" and occurred time 2026-12-15
    Given the proof entry of "RR223344556TH" is on the same ledger with delivery status "FAILED", the ACE proof result "UNDELIVERABLE" in its source ref and occurred time 2026-12-21, appended by rwb-comms through the same operation with externalRef "RR223344556TH" in this fixture
    When the dispatch loop calls GET /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000321/interactions
    Then the ledger holds 2 entries for "RR223344556TH" and no entry is updated
    Then both entries answer barcodeStatus "FAILED", folded by external ref "RR223344556TH" on the latest occurred time
    Then no notice state, no decision entry, no case transfer and no notice-period timer is written here, and those stay with rwb-comms, rwb-decision and rwb-case under R-LIT-07 and R-LIT-09

  Scenario: AC5 A repeated append writes one entry (new, D-RCV-60)
    Given the dispatch loop appended the letter of AC2 with Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000001"
    When the same body is sent again with the same Idempotency-Key
    Then the answer is the stored status 201 with the same entry and caseSeq
    When the same body is sent with Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000009"
    Then the answer is status 200 with the existing entry, because the business idempotencyKey exists
    Then the ledger holds one LETTER entry for "RR223344556TH"
    Then the first header key with a different body, and the business key with a different body, are each refused with status 409 and MSG-PLT-N009-05 and the stored entry is unchanged

  Scenario: AC6 A LETTER entry that breaks the letter rules is refused and nothing is written (new, D-RCV-60)
    Given the dispatch loop appends a letter with deliveryStatus "SENT" and no conductCheck
    And a letter with deliveryStatus "SENT" and no externalRef
    And a letter with an externalRef of 61 characters
    When all three calls are answered
    Then the first answer is status 422 with MSG-GEN-001 and field "/conductCheck"
    Then the second answer is status 422 with MSG-GEN-001 and field "/externalRef"
    Then the third answer is status 422 with MSG-GEN-002 and field "/externalRef"
    Then the ledger of the case holds no entry for any of the three calls

  Scenario: AC7 No address, name or identity value is stored, logged or answered (new, D-RCV-60)
    Given the letter of "RR223344556TH" is on the ledger of case "RC-2026-000321"
    When the DP02 answer, the case ledger answer and their log lines are inspected
    Then none carries a contact value, an address text, a person name or an identity number
    Then v_ace_contact.contact_value and contact_value_masked are never selected, and no table of this service holds a copy of either
    Then this story publishes no event, starts no workflow and writes no row outside the interaction ledger

  Scenario: AC8 A read of an unserved product or without a usable case is refused with 400 (new, D-RCV-60)
    When the record read is called for productCode "DP03" with the case uuid
    Then the answer is status 400, the problem names the owning service and no row is answered
    When it is called for productCode "DP99", for DP02 without caseId and for DP02 with caseId "RC-2026-000321"
    Then the answers are status 400 with MSG-GEN-007 for the first and MSG-GEN-001 naming "caseId" for the other two

  Scenario: AC9 A caller without the right is refused with 403 and the refusal is logged without a key value (new, D-RCV-60)
    Given the caller's role carries no right on the read of case "RC-2026-000321"
    When the dispatch loop calls GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321
    Then the answer is status 403 with MSG-P4-002
    Then the refusal is logged with no key value

  Scenario: AC10 A view that does not answer inside 5 s gives 503 and no guessed row (new, D-RCV-60)
    Given v_ace_contact does not answer inside 5 s for case "RC-2026-000321"
    When the dispatch loop calls GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321
    Then the answer is status 503 with MSG-GEN-006 naming the ACE database
    Then no row is answered from a cache or guessed

  Scenario: AC11 An append to a case that does not exist is refused with 404 and nothing is written (new, D-RCV-60)
    Given the case of the append does not exist
    When the dispatch loop appends the letter of notice "N-0101" to that case with conduct check "PASSED" and a valid Idempotency-Key
    Then the answer is status 404 with MSG-P4-003, passed on unchanged from the case check
    Then no entry is written to the ledger

  Scenario: AC12 A ledger that cannot be written rolls back, answers 503 and leaves no entry (new, D-RCV-60)
    Given the interaction ledger cannot be written
    When the dispatch loop appends the letter of notice "N-0101" of case "RC-2026-000321" with conduct check "PASSED", delivery status "SENT" and external ref "RR223344556TH" with a valid Idempotency-Key
    Then the transaction rolls back and the answer is status 503 with MSG-P1-022
    Then no entry exists for "RR223344556TH"

  Scenario: AC13 This service starts no notice-period timer and takes the proof date as given (new, D-RCV-60)
    Given the proof entry of "RR223344556TH" is on the ledger of case "RC-2026-000321", appended by rwb-comms with occurred time 2026-12-21
    When the dispatch loop calls GET /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000321/interactions
    Then the proof entry answers the occurred time 2026-12-21 as given
    Then no notice-period timer, no notice-period end date and no case task is written here

  Scenario: AC14 A caller without the right is refused with 403 on the append and the refusal is logged without a key value (new, D-RCV-60)
    Given the caller's role carries no right on the append to case "RC-2026-000321"
    When the dispatch loop appends the letter of notice "N-0101" to case "RC-2026-000321" with conduct check "PASSED" and Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000001"
    Then the answer is status 403 with MSG-P4-002
    Then the refusal is logged with no key value
    Then no entry is written to the ledger

  Scenario: AC15 A contact_point_ext or DP02 stamp that does not answer inside 5 s, or answers an error, gives 503 and no guessed row (new, D-RCV-60)
    Given contact_point_ext or the DP02 stamp does not answer inside 5 s or answers an error for case "RC-2026-000321"
    When the dispatch loop calls GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321
    Then the answer is status 503 with MSG-GEN-006 naming the ACE database
    Then no row is answered from a cache or guessed

  Scenario: AC16 An append to a case outside the caller's scope gives the same 404 as a case that does not exist (new, D-RCV-60)
    Given the case "RC-2026-000321" is outside the scope of the caller
    When the dispatch loop appends the letter of notice "N-0101" to case "RC-2026-000321" with conduct check "PASSED" and a valid Idempotency-Key
    Then the answer is status 404 with MSG-P4-003, the same answer as for a case that does not exist
    Then no entry is written to the ledger

  Scenario: AC17 An append rolled back on an unwritable ledger writes one entry when the same key is retried (new, D-RCV-60)
    Given the append of the letter of "RR223344556TH" with Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000001" was rolled back because the interaction ledger could not be written
    When the same append is sent again with Idempotency-Key "a1b2c3d4-0000-4000-8000-000000000001" once the interaction ledger can be written
    Then the answer is status 201 with the stored entry
    Then the ledger of case "RC-2026-000321" holds one LETTER entry for "RR223344556TH"

  Scenario: AC18 The DP02 read selects no contact value (new, D-RCV-60)
    When the dispatch loop calls GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321
    Then the SELECT of the read names neither contact_value nor contact_value_masked

  Scenario: AC19 A call without a session is refused with 401, and a case outside scope is refused with 404 on the case read (new, D-RCV-60)
    Given the caller has no session
    When the dispatch loop calls GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=c0000000-0000-4000-8000-000000000321
    Then the answer is status 401 with messageCode MSG-P4-001
    Then the same 401 is answered for the append and for GET /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000321/interactions
    When a caller with a session reads the case ledger of a case outside that caller's scope
    Then the answer is status 404 with MSG-P4-003

  Scenario: AC20 Equal occurred times are decided by case sequence (new, D-RCV-60)
    Given two LETTER entries of externalRef "RR223344556TH" with the same occurredAt, caseSeq 5 with deliveryStatus "DELIVERED" and caseSeq 6 with "FAILED"
    When the case ledger is read twice
    Then both reads answer barcodeStatus "FAILED" on both entries
    And an entry with the same externalRef and a different sourceRef is in the same fold

  Scenario: AC21 A missing or malformed Idempotency-Key is refused (new, D-RCV-60)
    When the letter of AC2 is posted without an Idempotency-Key header, and with the value "a1b2c3d4"
    Then each answer is status 400 with MSG-PLT-N009-03 and nothing is written

  Scenario: AC22 With the flag off the contact rows are not served (new, D-RCV-60)
    Given flag "rwb.source-data.ledger-letter" is off
    When the DP02 record read of the case is called
    Then the answer is status 404 and v_ace_contact is not read

```

**Target reading.** Every assertion above is new, because this story owns no legacy criterion; each one tests only the read of §1, the append and the fold. What the legacy story asserted of the notice, the barcode on the notice, the proof read, the notice period, the transfer, the decision record and the scope is proved in RWB-P6-E2021-APP, RWB-P3-E2021-APP, RWB-P7-E2021-APP, RWB-P4-E2021-APP and RWB-ITG-E2021-ITG, and the legacy values are kept here: notices `N-0101`, `N-0102`, `N-0103` and `N-0200`, cases `RC-2026-000321`, `RC-2026-000654`, `RC-2026-000655`, notice type `DEMAND`, template `DEMAND-SSME` `TH` version 1, barcode `RR223344556TH`, the sent date 2026-12-15, the call-back date 2026-12-18, the proof window of 7 days, the hold reason `CONTACT_STOP_X1`, the rule ids R-LIT-05, R-LIT-07, R-LIT-08, R-LIT-09 and R-UNI-10, the messages MSG-P6-001, MSG-P6-003, MSG-P6-008, MSG-P3-004 and MSG-GEN-001 and the `Idempotency-Key` `a1b2c3d4-0001`. AC1 answers the consent fact and takes no statutory decision, because the statutory branch of the legacy check is rwb-comms' under R-UNI-10. AC2 and AC3 fix the members of the append: `conductCheck` is required on a `LETTER` entry whose `deliveryStatus` is `SENT` or absent (the dispatch or held letter; a proof entry carries `DELIVERED` or `FAILED` and no conduct check, ASM-5714), `externalRef` is required whenever a `deliveryStatus` is stated, a blocked entry carries neither, and the notice type and the hold reason travel in the summary because `interaction` has no column for either (GAP-2181; ASM-3529; ASM-3530). AC4 records the one conflict of this story: the legacy loop moved one entry from Sent to Delivered or Unserved, the target ledger is append-only, and the proof is therefore a second row of the same barcode whose status governs the read (ASM-3531). AC5 to AC8 and AC19 to AC22 follow the shared idempotency, error and status rules (RD-P1-001, RD-P1-004). The proof entry carries the same `externalRef` as the dispatch entry, the WIN barcode of the notice, so the two fold together (RD-P1-064; GAP-3520 closed). The fold and AC4 are built and proved on entries that share one `externalRef`. The unserved outcome has no value in `LOV-SEND-STATUS`, so it is written as FAILED with the ACE result code in `source_ref` and the point is recorded (GAP-2181; ASM-3532).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The letter is dispatched by rwb-comms after the conduct check, and the result of that check is a value on the ledger entry of the letter. The conduct and consent checks are one versioned rule package governed in rwb-decision and run in the owning service, rwb-comms; the package name is Not specified in the source documents (GAP-1610) | REQ-OCC-005; FEAT-OCC-05; legacy BR1 |
| BR2 | The contact point the check reads is an ACE reference — its token, its type and its Workbench consent — and is never copied, stored or answered as a value | D-RCV-35 U1; BR-P1-001-5; DP-05; legacy BR5 |
| BR3 | Withdrawn consent is a fact of the contact point; whether a statutory notice is still sent is rwb-comms' statutory decision and never a rule of this service | R-UNI-10; REQ-OCC-006; legacy BR4 |
| BR4 | Entries of the interaction ledger are append only; a correction or a later outcome is a new entry, never an update | append-only trigger of RWB-P1-E1066-APP (database object, not an LDM field); BR4 of RWB-P1-E1066-APP; legacy BR5 |
| BR5 | The letter and its proof are two facts about one barcode, and the governing delivery status of an `externalRef` is the one with the latest `occurred_at`, the higher `case_seq` winning a tie | REQ-ILG-010; FEAT-ILG-07; legacy BR5, BR6; RD-P1-009 |
| BR6 | The notice period starts from the delivery date on the proof, and the timer is rwb-case's; this service writes the date it is given and starts nothing | R-LIT-07; CTL-15; legacy BR5; AC13 |
| BR7 | A dispatch entry carries its conduct check and its barcode; a held entry carries its conduct check, its reason and no barcode | REQ-OCC-003, REQ-OCC-005; legacy BR1, BR2 |
| BR8 | No address, name or identity value is read into an answer, written to the ledger, logged or put in an event | BR-P1-001-5; legacy BR5, §17; AC7, AC18 |
| BR9 | A value a business person may change — the consent vocabulary, the contact types, the ledger event codes, the conduct results and the send statuses — is reference data with a version, never a constant in the code | Principle 1; BR-P1-001; legacy BR10 |

**Where each rule lives in the target.** BR1 is split by ownership: the check and the dispatch are rwb-comms' and the entry that carries the result is this service's, written through the writer of RWB-P1-E1066-APP (DP-18). BR2 is the shape of the read: `contact_key`, `contact_type`, `consent_given` and `verified_at` are selected, `contact_value` and `contact_value_masked` are not, and nothing is stored. BR3 is why AC1 answers WITHDRAWN and stops: the statutory list is rwb-comms' and the decision does not cross the contract. BR4 is the trigger `tr_interaction_append_only` and the absent update method, which is why the proof of AC4 is a second insert. BR5 is the fold: one barcode, two rows, the latest `occurred_at` wins on the read. BR6 keeps its wording and moves the clock to rwb-case. BR7 is the validation of the append. BR8 is asserted by AC7 and by an architecture test on the SELECT list. BR9 is the reference-data client library with a fixture until its contract is published (ASM-3533; DP-07).

### 9. State transitions

None in the case and none in the notice: this story changes no case status, no notice state and no timer. The notice states Approved, Sent, Delivered, Unserved and Held are rwb-comms', the case status and the transfer are rwb-case's, and the decision record is rwb-decision's. What this story has is the shape of its own ledger, which has no state to move because it is append only; the barcode's governing status is a fold and not a stored state. The values of LOV-SEND-STATUS, LOV-CONDUCT and LOV-LEDGER-EVENT are data read as the list holds them, so a new value adds no transition to this table.

| From | Event | Condition | To |
|---|---|---|---|
| a case at case_seq n | the letter of a notice is appended | The case check answers, the body validates and the `Idempotency-Key` is new | The case is at case_seq n+1 and one `LETTER` entry exists |
| a `LETTER` entry with a barcode | rwb-comms appends the proof entry of that letter | The entry shares the `externalRef`, the WIN barcode (RD-P1-064) | A second entry exists; the governing status is the later one; no row is updated |
| a barcode with a proof entry | the same append is replayed | The same header key and body, or a new header key with the same business key | No new entry; the stored entry is answered with the same case_seq |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The dispatch loop of rwb-comms, with a workload identity token | Reads the DP02 contact rows of a case in scope and appends the `LETTER` entries; writes nothing else |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads `recovery.v_ace_contact`, `contact_point_ext` and `data_product_load`; holds no privilege outside its schema and the views |
| RW-LITOFF, litigation officer | Sees the entry on SCR-18 and the case timeline through rwb-comms and rwb-case (Litigation R); calls nothing of this service directly |
| RW-CONDUCT, Conduct and QA officer | Reads the blocked and unserved entries of a case through the ledger read interface (Case record R) |
| RW-DATASTEW, data steward and data product owner | Reads the DP02 stamp the answer names and the consent rows of `contact_point_ext` (Platform administration R) |
| RW-PLATADM, platform administrator | Reads a refused read and a refused append with their problem bodies for the deployment |
| rwb-comms (P6) | Owns the conduct check, the statutory list, the notice, the WIN file, the proof and the timer; consumes this read and this append through RWB-P6-E2021-CON |
| rwb-case (P3) | Owns the case, its scope, its status, the transfer and the NOTICE_PERIOD timer; answers the case check the append takes |

Roles and their rights are held as data in rwb-access and reached through its authorise contract, never by a table read (DP-01; TSD P1 T6.2). No credential and no personal value appears in an answer, a log line or a test: the answers carry a person key, a contact token, a consent status, dates, a barcode, codes and a case sequence.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-EXT-013 | contact_point_ext | contact_key | Read |
| DF-EXT-014 | contact_point_ext | contact_type | Read |
| DF-EXT-015 | contact_point_ext | consent_given | Read |
| DF-EXT-016 | contact_point_ext | consent_at | Read (to resolve the status; not answered) |
| DF-EXT-017 | contact_point_ext | verified_at | Read |
| DF-OPS-002 | data_product_load | product_code | Read (the DP02 stamp) |
| DF-OPS-004 | data_product_load | business_date | Read (the `dataAsOf` of the answer) |
| DF-OPS-007 | data_product_load | status | Read (the `productStatus` of the answer) |
| DF-INT-002 | interaction | case_id | Write, through the writer of RWB-P1-E1066-APP |
| DF-INT-004 | interaction | occurred_at | Write, through the writer |
| DF-INT-005 | interaction | channel | Write, through the writer |
| DF-INT-006 | interaction | direction | Write, through the writer |
| DF-INT-011 | interaction | summary | Write, through the writer |
| DF-INT-012 | interaction | conduct_check | Write, through the writer |
| DF-INT-013 | interaction | source_system | Write, through the writer (WORKBENCH, unchanged) |
| DF-INT-014 | interaction | event_code | Write, through the writer (`LETTER`) |
| DF-INT-017 | interaction | source_ref | Write, through the writer (the ACE proof result code on a proof entry) |
| DF-INT-018 | interaction | idempotency_key | Write, through the writer |
| DF-INT-019 | interaction | case_seq | Allocated and written by the writer |
| DF-INT-028 | interaction | delivery_status | Write, through the writer (`LOV-SEND-STATUS`) |
| DF-INT-029 | interaction | external_ref | Write, through the writer (the barcode) |

Field IDs are those in the Logical Data Model and Data Dictionary. Every `DF-ACE-` row is read in this service's own `recovery.v_ace_contact` view and never from a `public` table, and `contact_value` (DF-ACE-078) and `contact_value_masked` (DF-ACE-079) are never selected, because the contact point is a reference and not a value (DP-01, DP-05). `contact_point_ext` is this service's table by the ownership map, and this story only reads it: the row is written by the extension-table operations, not here. `data_product_load` is read for `dataAsOf` and written by RWB-P1-E1015-APP. The `DF-INT-` rows are written by the writer of RWB-P1-E1066-APP; this story extends what it accepts and stores and adds no second writer and no column. `notice.notice_type` (DF-LEG-018) is never read: the notice is rwb-comms' table and the notice type reaches this service as text of the summary (ASM-3530).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). One row type on the published record read, and the append and the case read of the interaction ledger this service owns.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/data-products/{productCode}/records` | The rows of one data product for a case (API-P1-010), extended here with the DP02 contact-and-consent row; never a contact value, an address, a name or an identity number. Query `caseId` required, uuid | The dispatch loop of rwb-comms (workload identity) with Case record R on the named case, scope applied | Idempotent read |
| POST | `/cases/{caseId}/interactions` | Appends one `LETTER` ledger entry: 201 new, 200 existing business key | Case record C on the case | Header `Idempotency-Key` (UUID) required; body `idempotencyKey` is the permanent business key |
| GET | `/cases/{caseId}/interactions` | Reads the ledger of one case in `case_seq` order; each entry as stored, plus `barcodeStatus` where the entry carries an `externalRef` | Case record R on the case, scope applied | Idempotent by case and page |

The DP02 answer is the published `DataProductRecordPage` (`dataAsOf`, `productStatus`, rows of `fields: FieldValue[]` with `fieldName`, `value`, `masked`); a contact row has the fields `contactKey`, `contactType`, `consentStatus` (GIVEN, WITHDRAWN or UNKNOWN) and `verifiedAt` (RD-P1-005 rule 4; GAP-2181; ASM-3527). `consent_at` is read to resolve the status and is not answered.

The append body is `InteractionRequest` 5.1.0 (RD-P1-007 rule 3). Required: `eventCode` (`LETTER`), `occurredAt`, `actorType` (`SERVICE`), `actorRef` (`rwb-comms`), `sourceRef` (at most 60 characters; `INT-14 WIN` on a dispatch entry), `idempotencyKey` (at most 120, form `<code>-<caseNo>-<yyyyMMdd>-<actionId>`: `LETTER`, the sent date and the notice record UUID for a dispatch (RD-P1-064), `LETTER` and the notice record UUID for a held letter). Also sent: `channel` (`LETTER`), `direction` (`OUTBOUND`), `conductCheck` (`LOV-CONDUCT`), `deliveryStatus` (`LOV-SEND-STATUS`), `externalRef` (the barcode, at most 60) and `summary`. This story adds two letter checks to the writer: `conductCheck` is required when `deliveryStatus` is `SENT` or absent, and `externalRef` is required when `deliveryStatus` is present. The case check (Case record C through `GET /api/recovery/case/v1/cases/{caseId}`, 2 s), the allocator, the list validation, the trigger and the idempotency rules are the writer's. The append writes no decision record.

The case read adds `barcodeStatus` to an `Interaction` that has an `externalRef`.

The ledger operations are the case-scoped family `POST` and `GET /cases/{caseId}/interactions` and `GET /cases/{caseId}/interactions/{entryId}`; the flat `/interactions` family is withdrawn (RD-P1-007 rule 2; GAP-2182 closed). Build contract: rwb-source-data.yaml 5.1.0 (API Specification v7).

Errors are `application/problem+json` with the shared `Problem` schema (RD-P1-004): 400 MSG-GEN-001 for a missing or non-uuid `caseId`, MSG-GEN-007 for a `productCode` outside its pattern, MSG-PLT-N009-03 for a bad `Idempotency-Key`, and for a product this service does not serve a problem naming the owning service (message ID pending, GAP-3272); 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 for a case that does not exist or is out of scope; 409 MSG-PLT-N009-05; 422 MSG-GEN-001 (missing member), MSG-GEN-002 (too long) or MSG-GEN-007 (not in its list) with `field`; 503 MSG-GEN-006 naming the ACE database, or MSG-P1-022 when the ledger cannot be written.

#### 12.2 REST operations consumed

None of its own. The conduct check, the case state, the legal hold, the open deviation and its contact stop, the template state, the statutory list and the proof window are facts the caller holds: rwb-comms takes the check on its own notice and its own reference data, rwb-case answers the case state and the scope to the case check of the writer, and rwb-deviation holds the stop. This story calls none of them, and the append adds no hop to the one the writer already takes (DP-11; C RWB-P6-E2021-CON). The reference lists of §13 reach this service through the reference-data client library of DP-07 and not as a run-time call of its own.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` (EV-26, EV-27) belong to RWB-P1-E1015-APP. `NoticeDispatched` (event 14) and `NoticeDelivered` (event 15) are rwb-comms' on `rwb.comms.events.v1` (RWB-P6-E2021-CON), and `DecisionRecorded` is the decision-record library's on the shared `rwb.decision-record.v1`. This story publishes no event, writes no outbox row of its own and adds no message schema: the append of the letter is a fact of the ledger, and the event that announces a dispatch is raised by the service that dispatches.

#### 12.4 Events consumed

None. The dispatch loop is started by its own Schedule and reaches this service over REST after its events (DP-09, DP-10; RWB-P6-E2021-APP). Consuming a `rwb.comms` event here would create a second writer of the same entry and a second path to the same barcode; the inbox of the platform library absorbs a redelivery of anything this service is later asked to consume.

#### 12.5 Workflows and activities

None. The read and the append are synchronous REST steps: the read answers in one call and the append writes one row in one transaction, both inside the 2 s budget (DP-11). JOB-10, its 16:00 Schedule and its dispatch workflow are rwb-comms' (RWB-P6-E2021-CON §12.5), and the task queue of this service is `rwb-source-data` in namespace `rwb-recovery` and belongs to other P1 stories (DP-10).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the read is called when the loop needs the fact and the append when the loop has something to record, and neither runs on a clock of its own (DP-10).

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 rwb-source-data; shape and writer of RWB-P1-E1066-APP | Insert and read through the writer. The columns it fills are already in the schema (DF-INT-012, DF-INT-017, DF-INT-028, DF-INT-029), so this story adds no migration; the append-only trigger `tr_interaction_append_only` and the index `ix_interaction_case_time` are kept |
| `contact_point_ext` | `rwb_source_data` | P1 rwb-source-data (ownership map) | Read only: the consent and verification facts of a contact point are selected and the row is written by the extension-table operations, not here |
| `v_ace_contact` | `recovery` | ACE, read through the view contract of RWB-P1-E1069-APP | SELECT only on `contact_type`, `contact_key` and `person_key`; `contact_value` and `contact_value_masked` are never selected and never copied (DP-05; ADR-010) |
| `data_product_load` | `rwb_source_data` | P1, written by RWB-P1-E1015-APP | Read for `dataAsOf` and the DP02 `productStatus`; no row is written here |
| `processed_event` | `rwb_source_data` | PLT library object, created in this service's schema | The inbox of DP-09; not used by this story, which consumes no event, and never redefined |
| `idempotency_key` | `rwb_source_data` | PLT library object, created in this service's schema | The stored response of the append; read and written by the library and never redefined |
| `outbox_event` | `rwb_source_data` | PLT library object, created in this service's schema | The outbox the decision-record library writes through; this story adds no row of its own and never redefines it |

No table of another service is read and no foreign key crosses a schema (DP-01). `notice`, `template`, `merge_field` and `recovery_case` are never named in this story's code or tests except as the objects it must not touch, and `v_ace_pod` is not read here: the pod read and the proof entry are RWB-P1-E1055-APP's.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Provider fake of rwb-source-data.yaml 5.1.0, path `fakes/rwb-source-data/5.1.0/` | The DP02 record read, the append and the case read, for rwb-comms | One mapping per documented status; a WITHDRAWN contact row; a 201, a 200 repeat, a BLOCKED letter and a 422. Pending: the P1 contract story that lists the DP02 row and letter fixtures |
| ACE contact fixture | `recovery.v_ace_contact` | One `ADDRESS` row `ADDRESS:ADDR-0001` for `P0000123`, one `PHONE` row for the same person, and a person with no postal row |
| Extension fixture | `contact_point_ext` | The row of `ADDRESS:ADDR-0001` with `consent_given` false, `consent_at` 2026-11-20 and `verified_at` 2026-10-02; a key with no row, so the status is UNKNOWN; a key with `consent_given` true, so GIVEN |
| Ledger fixture | `rwb_source_data` at the baseline plus the writer's migration | The `LETTER` entry, the proof entry of the same barcode, the unique key on `idempotency_key` and the append-only trigger, so AC4, AC5, AC6 and AC20 run on the real keys and the real trigger; the proof entry fixtures are written as rwb-comms writes them, sharing the `externalRef` |

The test fixtures are local: no live rwb-comms, rwb-case, WIN interface or ACE database is needed for the tests of §16, and no production row or file is copied into a fixture.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations on `/api/recovery/source-data/v1` (the DP02 branch of the record read, the append and the case read) | None of its own | OpenAPI 3.1; one hop, 2 s budget, breaker per client (DP-11) |
| Kafka | None | None | The topic and both events belong to RWB-P1-E1015-APP; the dispatch events are rwb-comms' (DP-14) |
| Temporal | None | None | No workflow, activity or Schedule in this story; the 16:00 run is rwb-comms' (DP-10) |
| File | None | None | No file is read or written; the WIN file is rwb-integration's and rwb-comms' |
| SQL view | None | 1 view of `recovery`, SELECT only | `v_ace_contact`, in-process, read-only login, 5 s statement timeout, never copied (DP-05; ADR-010) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `comms`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here). The build starts on Day 1 against four published artefacts and no build dependency: the service baseline, the view contract of RWB-P1-E1069-APP, the record read and the writer of RWB-P1-E1066-APP, and the fake of RWB-P6-E2021-CON.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**One sentence per pattern.** DP-01 is the boundary of this story: the ledger and the extension table are written in `rwb_source_data`, and `notice` and `template` are rwb-comms' and never read, not even for the notice type, which arrives as summary text. DP-03 is a statement: this story writes no decision record, and the D7.1 entry of a held or unserved notice is rwb-comms' and rwb-decision's under R-LIT-05 and R-LIT-09. DP-05 is the read path: `v_ace_contact` is read through this service's own view with SELECT on three fields, and no ACE column is copied. DP-07 is the consent vocabulary, the contact types and the three value lists as reference data with a version, read through the client library with a fixture until the contract is published (ASM-3533). DP-09 is a statement: the read and the append publish no event and write no outbox row of their own. DP-10 is a statement: no Schedule, workflow or activity starts here, because the 16:00 run is rwb-comms'. DP-11 is the hop: the loop calls the read and the append over REST, one hop with a 2 s budget and a breaker, against the shapes of RWB-P6-E2021-CON and its fake. DP-13 is the base: every path sits under `/api/recovery/source-data/v1`. DP-18 is this story's own pattern: the ledger entry of a dispatched letter and the fold of its barcode are P1's answer to an outcome that no longer fits in one mutable row. DP-19 is a statement: this story serves no screen; SCR-18 and SCR-04 reach it through gateway-bff.

This secondary slice adds no new build dependency of its own (metadata H = None). The platform contracts the DP rows name — RWB-PLT-E1027-CON for the decision record, RWB-PLT-E1043-CON for the reference data, RWB-PLT-TE006-CON for the outbox and inbox, RWB-PLT-E1071-CON for the workflow kit and RWB-PLT-N001-CON for the composite route — are pulled by the rwb-source-data baseline stories of Epic 1 and Epic 2, and this story builds against their published versions.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `Dp02ContactRowHandler` | Handler | The DP02 branch of the record read: one row per contact point of the case's persons, ordered by `contact_key`, with no contact value selected |
| `ConsentStatusResolver` | Resolver | GIVEN, WITHDRAWN or UNKNOWN from `consent_given` and `consent_at`; no value of its own (DP-07) |
| `FreshnessStampReader` | Reader | The DP02 business date and status of `data_product_load`, answered as `dataAsOf` and `productStatus` |
| `ContactPointRepository` | Repository | SELECT over `recovery.v_ace_contact` left joined to `contact_point_ext`; no write method exists |
| `LetterEntryValidator` | Validator | Added to the writer's validation for `LETTER`: `conductCheck` required when `deliveryStatus` is `SENT` or absent, `externalRef` required with a `deliveryStatus`, the 60-character length, the reference lists (DP-07) |
| `BarcodeStatusFold` | Fold | Adds `barcodeStatus` on the case read: per `externalRef`, the `deliveryStatus` of the latest `occurredAt`, then the highest `caseSeq`; no window |
| `Dp02ContactRow`, `ContactPage`, `LetterEntry` | Published types | The records of 12.1 in `...sourcedata.api`; no address, name or identity field |

**Database.** This story adds no table and no column: `interaction` already carries `conduct_check` (DF-INT-012), `source_ref` (DF-INT-017), `delivery_status` (DF-INT-028) and `external_ref` (DF-INT-029) in Physical Schema v6, and the writer's own migration created the ledger columns, the unique key on `idempotency_key`, the index `ix_interaction_case_time` and the trigger `tr_interaction_append_only`. It reads `contact_point_ext`, three fields of `v_ace_contact` and the DP02 stamp. It creates no foreign key across a schema and writes no extension row (DP-01, DP-05). No Flyway version is added, so no applied version can be edited.

**Configuration and reference data**

- `LOV-LEDGER-EVENT` (`LETTER`), `LOV-CONDUCT` (PASSED, BLOCKED, NOT_APPLICABLE), `LOV-SEND-STATUS` (SENT, DELIVERED, READ, FAILED), the contact types and the consent vocabulary are reference data read through the client library, with a fixture until the reference-data contract is published (ASM-3533; DP-07).
- The consent mapping — `consent_given` true is GIVEN, false with a `consent_at` is WITHDRAWN, absent is UNKNOWN — is configuration of the read and not a value a business person changes (ASM-3527).
- The unserved outcome maps to `FAILED` of `LOV-SEND-STATUS`, and the ACE proof result code travels in `source_ref`; no value is added to the list (GAP-2181; ASM-3532).
- The 2 s client budget, the 5 s statement timeout and the breaker are configuration of the read and of the append (DP-11; TSD P1 T6.3).
- The flag `rwb.source-data.ledger-letter` gates the DP02 contact row, the two letter checks and `barcodeStatus` at deployment.

**Build steps**

1. The published types and the fragment of 12.1 in rwb-source-data.yaml 5.1.0, with the provider fake (RD-P1-005, RD-P1-011).
2. `ContactPointRepository` and `Dp02ContactRowHandler`: the three view fields, the left join to `contact_point_ext`, the order by `contact_key` and the DP02 branch of the record read (AC1).
3. `ConsentStatusResolver` and `FreshnessStampReader`: the three-value status from two columns and the DP02 date and status (AC1, X3).
4. `LetterEntryValidator`: `conductCheck` required, `externalRef` required with a `deliveryStatus` and refused without one, the 60-character length, MSG-GEN-001 naming the field and nothing written on a refusal (AC6).
5. The letter checks inside the writer of RWB-P1-E1066-APP, so 201 carries the stored entry and `caseSeq`, and the repeats of AC5 behave as the writer's rules (AC2, AC3, AC5, AC21).
6. `BarcodeStatusFold` on the case read, with the tie-break (AC4, AC20).
7. An architecture test that the `comms` module selects no `contact_value`, names no table of another service and holds no update or delete method (AC7, DP-01).
8. Tests for AC1 to AC22 against the fixtures of 12.8, and provider verification of every fake mapping.

**Feature flag.** `rwb.source-data.ledger-letter`. Off, the DP02 contact rows are answered 404, so the loop has no consent fact and holds the notice; the append and the case read behave as before this story (RD-P1-045; EDD v6 flags table).

**Done when.** The tests in §16 pass, the contact point of `P0000123` answers WITHDRAWN with no address in the payload, the letter of `RR223344556TH` is one `LETTER` entry with conduct check PASSED and its barcode, a held letter is one BLOCKED entry with no barcode, the proof entry of the same barcode governs both reads, a repeated `Idempotency-Key` writes no second entry, and a missing conduct check or barcode is refused with nothing written.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the read or of the append is missing or `caseId` is not a uuid | Enter {field}. |
| MSG-GEN-002 | `externalRef` longer than 60 characters | As Error and Message Standard v6 |
| MSG-GEN-007 | A value not in its list or pattern | As Error and Message Standard v6 |
| MSG-PLT-N009-03 | `Idempotency-Key` missing or not a UUID | As Error and Message Standard v6 |
| MSG-PLT-N009-05 | Key reused with another body | As Error and Message Standard v6 |
| MSG-P4-001 | No valid credential | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | The caller's role carries no right on the read or the append | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case of the append does not exist or is out of scope | This case is not in your scope. |
| MSG-P1-022 | The interaction ledger could not be written | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-006 | A view or the database does not answer inside 5 s | {system} is not available. Try again in a few minutes. |
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window, in the loop that holds the notice | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P6-001 | A contact stop blocks the letter, in the loop that holds the notice | Contact with this customer is stopped for {reason}. |
| MSG-P6-003 | Carried from the legacy story (Target reading, §7); not raised by this service | Not specified in the source documents (DOR-RWB-P1-E2021-APP-9) |
| MSG-P3-004 | Carried from the legacy story (Target reading, §7); not raised by this service | Not specified in the source documents (DOR-RWB-P1-E2021-APP-9) |
| MSG-P6-005 | The template of the notice is not approved (409 on the notice POST of rwb-comms); not raised by this service | Not specified in the source documents (GAP-1096) |
| MSG-P3-005 | A notice of this type is already in progress for the case (409 on the notice POST of rwb-comms); not raised by this service | Not specified in the source documents (GAP-1096) |

The messages this story raises are MSG-GEN-001, MSG-GEN-002, MSG-GEN-007, MSG-PLT-N009-03, MSG-PLT-N009-05, MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P1-022 and MSG-GEN-006; MSG-P4-003 is raised by the case check and passed on unchanged, and MSG-P1-022 and the idempotency messages are the writer's and the platform's texts. MSG-P6-008 and MSG-P6-001 are carried here character for character because this story stores the conduct check result and the barcode they name, and this story raises neither: the dispatch loop of rwb-comms does. Thai text for each message follows decision DL10, which stays open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by programme directive D-RCV-60. No message carries a person name, an identity number, a phone number or an address.

### 15. Screens and states

No screen in this story. SCR-18 Notice approval shows the Sent, Delivered and Unserved states of the notice and is rwb-comms'; SCR-04 Case timeline shows each ledger entry with its conduct check result and is rwb-case's; the conduct officer reads the blocked and dispatched entries through the ledger read interface of RWB-P1-E1068-APP. Both screens arrive through the gateway-bff composite route, which calls this service for the record read and the case ledger read of §12.1 (DP-19; RWB-PLT-N001-CON). This story renders none of it, fixes no field, state or mask of any screen, and answers a 400, a 422 or a 503 in the error state of whoever asked. SCR-04 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-2451). SCR-18 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-2452).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E2021-APP-04 | AC2, BR1, BR7 | Contract | `N-0101` Approved; acknowledgement `RR223344556TH`; the ledger entry is asserted here, the notice state in RWB-P6-E2021-APP |
| TC-P1-E2021-APP-05 | AC4, BR5 | Contract | INT-15 DELIVERED, call-back 18122026; the fold is asserted here, the timer in RWB-P3-E2021-APP |
| TC-P1-E2021-APP-06 | AC4, BR5 | Component | INT-15 UNDELIVERABLE; the second entry and the FAILED status with the result code in `source_ref` |
| TC-P1-E2021-APP-07 | AC3, BR7 | Contract | Open X1 with contact stop; the BLOCKED entry is asserted here, the hold and the transfer in RWB-P6-E2021-APP |
| TC-P1-E2021-APP-08 | AC1, BR3, BR9 | Component | Postal consent WITHDRAWN, DEMAND notice; the consent fact is answered here, the statutory decision is not |
| TC-P1-E2021-APP-09 | AC4, BR5 | End to end | `N-0102` sent 2026-12-15 and `N-0103` sent 2026-12-16; the proof window and the unserved state stay with rwb-comms |
| TC-P1-E2021-APP-10 | AC2, BR7 | End to end | Legal hold true; the hold of the notice is rwb-comms' and this story asserts no entry for the held notice |
| TC-P1-E2021-APP-11 | AC2, BR7 | End to end | `DEMAND-SSME` TH v1 withdrawn 2026-12-13; the template state is rwb-comms' |
| TC-P1-E2021-APP-12 | AC3, BR1 | NFR | Open X2 with stop; decision log stubbed unavailable; the refusal is rwb-decision's and this story writes no entry |
| TC-P1-E2021-APP-13 | AC5, BR4 | Contract | The append repeated with one `Idempotency-Key`: the first answer, one entry, the same `caseSeq` |
| TC-P1-E2021-APP-14 | AC1, BR2 | Component | `N-0200` and its case outside the scope of the caller; 404 with MSG-P4-003 and no row answered |
| TC-P1-E2021-APP-15 | AC6, BR7 | Component | An append with no conduct check; 422 with MSG-GEN-001 naming "conduct check" |
| TC-P1-E2021-APP-16 | AC9 | Component | A caller without the right is refused with 403 MSG-P4-002. The refusal log carries no key value. |
| TC-P1-E2021-APP-17 | AC6, BR4 | NFR | The ledger write forced to time out on 10 dispatch entries; ten entries after the retry and no notice fact marked recorded early |
| TC-P1-E2021-APP-18 | AC7 | See Test Cases v9 | No address, name or identity value |
| TC-P1-E2021-APP-26 | AC8 | See Test Cases v9 | DP03, DP99, no caseId, case number |
| TC-P1-E2021-APP-27 | AC9 | See Test Cases v9 | No right |
| TC-P1-E2021-APP-28 | AC10 | See Test Cases v9 | View delayed past 5 s |
| TC-P1-E2021-APP-29 | AC11 | See Test Cases v9 | Missing case |
| TC-P1-E2021-APP-30 | AC12 | See Test Cases v9 | Ledger not writable |
| TC-P1-E2021-APP-31 | AC13 | See Test Cases v9 | No timer; proof date as given |
| TC-P1-E2021-APP-20 | AC14 | See Test Cases v9 | No right on the append |
| TC-P1-E2021-APP-21 | AC15 | See Test Cases v9 | Extension table or stamp delayed |
| TC-P1-E2021-APP-22 | AC16 | See Test Cases v9 | Out-of-scope case |
| TC-P1-E2021-APP-23 | AC17 | See Test Cases v9 | Retry after a rolled-back append |
| TC-P1-E2021-APP-24 | AC18 | See Test Cases v9 | DP02 selects no contact value |
| TC-P1-E2021-APP-25 | AC19 | See Test Cases v9 | No session |
| TC-P1-E2021-APP-01 | AC20 | See Test Cases v9 | Equal occurred times |
| TC-P1-E2021-APP-02 | AC21 | See Test Cases v9 | Missing or malformed Idempotency-Key |
| TC-P1-E2021-APP-03 | AC22 | See Test Cases v9 | Flag off |
| TC-P1-E2021-APP-19 | Section 12.7 tables | See Test Cases v9 | Table boundary |

The legacy level "System" maps to End to end, "Access" to Component and "Resilience" to NFR, as in the other stories of this run. TC-P1-E2021-APP-04 to TC-P1-E2021-APP-17 keep their legacy order and data; TC-P1-E2021-APP-16 is the access case and TC-P1-E2021-APP-17 the Principle 5 case. The IDs and the criterion each row proves follow Test Cases v9. Each legacy case asserts only this slice's read, entry or fold; the criteria they once proved in the monolith are proved in the stories that now own them and in RWB-ITG-E2021-ITG, which carries the `-ITG` copies. The full test of each case, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the consent vocabulary, the contact types, `LOV-LEDGER-EVENT`, `LOV-CONDUCT` and `LOV-SEND-STATUS` are reference data with a version; the consent mapping, the 2 s budget and the 5 s statement timeout are configuration; no barcode, notice type, person key or case number is written in code.
- No personal data in logs, events, tests or prompts: the answers carry a person key, a contact token, a consent status, dates, codes and a barcode; a contact value, an address, a name and an identity number are never selected, logged, echoed in a problem body or stored, and the test data is synthetic.
- ACE data only through this service's own `recovery.v_ace_*` views and the owner's contract, and only the three reference fields of `v_ace_contact`; `contact_value` and `contact_value_masked` are excluded by an architecture test and not only by review (DP-05; ADR-010).
- No read of another service's tables: the notice check, the case state, the deviation list, the proof window and the decision record are consumed through RWB-P6-E2021-CON and its fake and never read (DP-01, DP-11).
- No entry is ever updated or deleted by application code: the trigger `tr_interaction_append_only` refuses the statement and the repository has no such method, which is why the proof is a second entry and not a change (BR4; DP-18).
- The append is the writer's: this story extends the members it accepts and adds no second writer, no second `case_seq` allocator and no direct insert into `interaction`.
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and adds no version to the sequence (DP-02, DP-15; ADR-021).
- The platform library objects stay the library's: `processed_event`, `idempotency_key` and `outbox_event` are created in this schema and are never redefined by this story (DP-09).
- `contactKey` and `person_key` are personal data: every read of them is access logged, 100 percent (NFR-P1-009), and they are never written to application logs.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-P1-E2021-APP-04 to TC-P1-E2021-APP-06, TC-P1-E2021-APP-09, TC-P1-E2021-APP-13 to TC-P1-E2021-APP-15 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-05, R-UNI-20, R-LIT-04, R-UNI-39 | TC-P1-E2021-APP-07, TC-P1-E2021-APP-10 to TC-P1-E2021-APP-12, TC-P1-E2021-APP-17 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-P1-E2021-APP-08 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-P1-E2021-APP-04 to TC-P1-E2021-APP-06, TC-P1-E2021-APP-16 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P6-E2021-CON | Contract | C: declares the rwb-source-data answers the loop consumes — the postal contact point with its consent fact and the ledger write — and fakes them; this story implements them |
| RWB-P6-E2021-APP | App development | The dispatch loop, its conduct check, the notice, the WIN file, the proof and the two notice events; it calls this read and this append |
| RWB-P3-E2021-APP | App development | The case state, the transfer and the NOTICE_PERIOD timer that this story never writes |
| RWB-P7-E2021-APP | App development | The D7.1 decision record of a held or unserved notice, which this story never writes |
| RWB-P4-E2021-APP | App development | The scope of a notice, which this story never decides |
| RWB-ITG-E2021-ITG | Integration | The cross-service proof of the legacy key with real services and the `-ITG` test copies |
| RWB-P1-E1066-APP | App development | Sibling in this service: the ledger writer, its schema, its allocator, its trigger and its reads, which this story extends |
| RWB-P1-E1066-CON | Contract | The `Interaction` and `InteractionRequest` schemas, the `Idempotency-Key` rule and the error envelope this story extends |
| RWB-P1-E1016-APP | App development | Sibling in this service: the record read of API-P1-010 whose DP02 branch this story adds |
| RWB-P1-E1015-APP | App development | Sibling in this service: `data_product_load`, the DP02 stamp and the two P1 events |
| RWB-P1-E1069-APP | App development | Sibling in this service: the views and the `rwb_source_data` grant this story reads through |
| RWB-P1-E1055-APP | App development | Sibling in this service: the read of `v_ace_pod` that rwb-comms uses before it appends the proof entry |

### 19. Out of scope

- Alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5).
- SMS and LINE dispatch (RWB-E2-022 and its rwb-source-data slice).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Notice approval (RWB-E2-014) and the notice states, the proof window, the transfer and the timer of RWB-P6-E2021-APP and RWB-P3-E2021-APP.
- The `v_ace_pod` read (RWB-P1-E1055-APP), the delivery and hand-recorded proof entries (rwb-comms only, RD-P1-064) and any delivery event (rwb-comms, RWB-P6-E1055-APP); rwb-source-data publishes no delivery result event (RD-P1-003, RD-P1-007).

### 20. Remaining delivery steps

- Size the story (DOR-RWB-P1-E2021-APP-16): delivery lead with the squad.
- Sign off the epic design (DOR-RWB-P1-E2021-APP-14): solution architect.
- Settle the mapping of WIN `delivery_status` to the ledger delivery status (GAP-3285): rwb-comms owner with the WIN interface owner.
- Publish rwb-source-data.yaml 5.1.0 with the DP02 contact row, the letter members and `barcodeStatus`, and mark the contract Done: API contract owner.
- Publish the provider fake with these fixtures: contract story owner.
- Load the synthetic contact, extension and ledger fixtures in DEV: data engineer.
- Align the data of the AC2 test cases to the dispatch `sourceRef` and business key of RD-P1-064 and carry the story-level IDs into the traceability matrix: test lead.
