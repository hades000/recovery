# RWB-P1-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1055-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P1-M |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1055-CON; RWB-P1-E1055-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-source-data. The proof of delivery that ACE ingests from WIN is read from `v_ace_pod` on this service's own base `/api/recovery/source-data/v1` as one named read, `GET /proof-of-delivery?businessDate=` (DP-05, DP-11, DP-13), gated on the WIN batch row of `v_ace_batch_status` so that no row of a date whose batch is not COMPLETE is ever returned (the gate of FSD P1 A2.14 and BR9 of this story); the delivery is recorded once on this service's own interaction ledger `interaction` in schema `rwb_source_data` through the ledger writer, keyed on the pod key and the notice with its callback date (DP-01, DP-18), with the lookup index on the per-service Flyway sequence (DP-15); the read stays behind its flag until `v_ace_pod` and `v_ace_batch_status` arrive with RWB-ACE-001 (DL43; TSD P1 T3.2 and T3.7). The WIN file, the acknowledgment, the notice, the row-to-notice matching and the notice period timer are rwb-comms, rwb-integration and rwb-case and are not in this story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1055-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 27 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the proof of delivery that ACE ingests from WIN to be read from the Workbench source-data service for a business date whose WIN batch is COMPLETE, with the delivery recorded once on the interaction ledger of the case**, so that **the delivery date a notice period is counted from is the one the bank's own record holds, stated with its age, and a second look at the same row never writes a second entry**.

This is the rwb-source-data slice of legacy RWB-E1-055, and it owns no legacy criterion: the criteria of the key are owned by the rwb-comms slice (RWB-P6-E1055-APP: AC2 to AC8 and AC10 to AC11), by the rwb-case, rwb-document and rwb-comms slices between them, and by the cross-service proof RWB-ITG-E1055-ITG (AC1 and AC9). What this story delivers is the source side of that loop, and it is worth a story of its own because it is the only door in the Workbench to the proof of a delivery:

- **the read** — `GET /proof-of-delivery?businessDate=` on base `/api/recovery/source-data/v1`, one row per `v_ace_pod` row of the business date, in pod-key order, carrying `pod_key`, `account_key`, `notice_ref`, `sent_date`, `barcode`, `callback_date`, `delivery_status`, `sent_type`, `source_system` and `data_as_of`;
- **the WIN batch gate** — a row of the date is returned only when the WIN row in `v_ace_batch_status` is COMPLETE for that date; otherwise no row of that date is returned, nothing of an earlier date is served in its place, DP07 is STALE and MSG-P1-001 is answered;
- **the delivery entry** — one outbound `LETTER` entry per delivery on this service's interaction ledger, through the ledger writer, carrying the delivery date and the notice reference and keyed on the pod key with the notice and its callback date, so a repeat read writes no second entry and the repeat is counted under R-UNI-40;
- **the Section B discipline** — `v_ace_pod` is a Section B view over the ACE table `pod_receipt`, so the read stays behind its flag until RWB-ACE-001 lands and answers "not available" until then (DL43).

It does **not** match a row to a notice by barcode or by `notice_ref`, does not change a notice state, does not start the `NOTICE_PERIOD` timer, does not hold a row with an unknown reference, opens no WIN connection and sends or acknowledges no file. Those are RWB-P6-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP and the integration slice of this key.

### 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from a print date can be challenged in court. The Workbench writes no WIN delivery fact of its own: ACE ingests the WIN proof-of-delivery file (INT-15) into `pod_receipt`, and the Workbench reads the result through the view `recovery.v_ace_pod` (D-RCV-35 U1; Architecture v5 slide 41; TSD P1 T5.1). One reader of ACE's views is the whole point of ADR-010: rwb-source-data holds the grant, and every other service asks it (REQ-DRI-006). So the delivery fact a notice period rests on must leave this service in a shape that says how old it is and never in a shape that silently serves yesterday's rows.

The batch gate is the part that has to survive the move. In the monolith the read ran inside one job beside the ACE batch record; in the target the read is on demand and may be asked at any hour, so the date's completeness is checked at the door. A WIN batch that is late, failed at its record count check or absent yields no row of that date, no earlier date in its place, DP07 STALE and MSG-P1-001: a notice period that starts one day early is a legal defect, and a period that starts from an earlier delivery is worse than a period that starts late and says so (FSD P1 A2.14 BR-P1-014-2 and BR-P1-014-3; TSD P1 T3.7).

The ledger entry is the second half. REQ-ILG-004 asks that what happens in an interaction is recorded against that interaction, and R-UNI-40 asks that the same fact twice produces one effect and a counted repeat. A delivery is a fact with a natural key that ACE already holds — the pod key, the notice reference and the callback date — so the entry is written under exactly that key, and the repeat is a no-op that is counted rather than a second line in the history of a case. Serves REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006.

### 3. Preconditions

- The wave-1 service baseline of rwb-source-data is in place: schema `rwb_source_data`, the `interaction` table with its ledger columns, the running per-service Flyway sequence with its own history table, the REST base `/api/recovery/source-data/v1`, the task queue name `rwb-source-data` in namespace `rwb-recovery` and the login `rwb_source_data` with SELECT on the 30 `recovery.v_ace_*` views and no privilege on any ACE table (DP-01, DP-02, DP-13, DP-15).
- **No build dependency of its own.** The metadata row *Depends on (build)* is None and the story starts on Day 1: it is a read over a view plus one entry on a table this service already owns, and the pipeline baseline it builds on is the service template, the schema, the sequence, the reference-data client library and the ledger writer interface of this service. The H rows the pattern table names (DP-07, DP-09, DP-10, DP-15, DP-19) are the wave-0 platform libraries and are not repeated in the metadata row (Template and Rules §R5.7 rules 1 and 2; §13).
- RWB-P6-E1055-CON is published with its fake: the proof-of-delivery record shape of this key, the delivery fact and the answers of the consumer's fake. This story is the provider side of that shape and builds against the fake from Day 1; it calls no operation of rwb-comms.
- The ledger writer of this service is delivered by RWB-P1-E1066-APP and published in RWB-P1-E1066-CON: the append operation `POST /api/recovery/source-data/v1/interactions`, its `InteractionRequest` schema, its `Idempotency-Key` rule, the `LETTER` event code of the list **LOV-LEDGER-EVENT**, the `case_seq` allocator and the unique key on the idempotency key. This story writes its delivery entry through that writer and never inserts into `interaction` directly; the build order of the two same-service stories is settled at sprint planning and is not a build dependency of this one (GAP-0578; ASM-0820).
- The freshness stamp and the DP07 status are delivered by RWB-P1-E1015-APP: `data_product_load` with one row per product and business date, the status list **LOV-FRESHNESS** and the repeat counter `duplicate_count`. This story reads the stamp and adds one to the counter of a repeat; it writes no stamp of its own.
- The feature flag of this read is a data row of the platform library and is closed until RWB-ACE-001 has created `v_ace_pod` and `v_ace_batch_status` (DL43; TSD P1 T3.2 and T3.7; GAP-0579; ASM-0821).
- The caller is the service identity of rwb-comms, holding a workload identity token, and never a person: a person reaches the delivery through the notice panel of rwb-comms and the gateway-bff composite route (DP-19).
- The read's page parameters, its error statuses and the per-field "not available" answer are not fixed by any source document (GAP-0577; ASM-0819; GAP-0579; ASM-0821), and neither is the home of the repeat counter (GAP-0580; ASM-0822) nor the exact wording render of MSG-P1-001 (GAP-0581; ASM-0823).

### 4. Flow

1. rwb-comms calls `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30` once per business date, after the WIN file window, as the service identity of rwb-comms; one hop, 2 s budget, one GET retry with jitter and a breaker (DP-11).
2. `SectionBGuard` reads the flag `rwb.dataengine.pod-read`: closed, the read answers with no row and the ten field names marked *not available* with the reason "Section B view not deployed" (AC5, X3).
3. `WinBatchGate` reads `v_ace_batch_status` for source WIN and the requested business date. The row is unique on `(source_system, business_date)`; when it is absent, or `is_complete` is false, or the status is FAILED, no `v_ace_pod` row of that date is read, nothing of an earlier date is served in its place, DP07 is STALE and MSG-P1-001 is answered (AC2, X1, X2).
4. `ProofOfDeliveryRepository` reads `v_ace_pod` for that business date. A Section B view carries `source_system` and `data_as_of` from the Tier 2 `business_date`, so the filter is the business date and `data_as_of` travels on the row as the age of the fact (TSD P1 T3.3).
5. The rows are mapped to the ten fields of the record and returned in ascending `pod_key` order; `sent_date` and `callback_date` arrive as dates through `recovery.ace_to_date`, so a dirty ACE text date is a null and never an error (TSD P1 T3.2, BR-P1-001-7).
6. Nothing is matched and nothing is resolved: a `notice_ref` that names no notice is returned like any other row, because the notice is rwb-comms' and the barcode break on the notice is rwb-comms' check (RWB-P6-E1055-APP); the held unknown row is kept on this service's References exception list and read through its data-quality read.
7. When the caller names the case of the notice the rows belong to, `DeliveryLedgerWriter` appends one delivery entry per row through the ledger writer, with the delivery date as the occurred time, the `LETTER` event code and outbound direction, the notice reference in the summary and `pod_key` as the source reference (AC3, DP-18).
8. The writer derives the idempotency key from the pod key, the notice reference and the callback date, so a second read of the same row finds the stored entry and writes no second one; `DuplicateCounter` adds one to `duplicate_count` of the DP07 stamp of that business date and writes nothing else (AC4, R-UNI-40).
9. The answer carries the rows and the freshness stamp of DP07 for the business date — its status, its source business date and the time the stamp was written — because every source-data answer states the age of what it carries (TSD P1 T3.7 Display).
10. A view or database failure answers 503 with MSG-GEN-006 and writes nothing; a ledger failure rolls the entry back, the read answers 503 with MSG-P1-022 and no row of the answer is presented as recorded (X6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The WIN batch for the business date is not COMPLETE in `v_ace_batch_status` | No `v_ace_pod` row of that date is read; no earlier date is served in its place; DP07 is STALE; the answer carries no row | MSG-P1-001 | AC2 |
| X2 | The WIN batch for the business date is FAILED at its record count check | As X1, and the stale flag is set at once; the stamp of the last complete business date stays the one in use | MSG-P1-001 | AC2 |
| X3 | `v_ace_pod` or `v_ace_batch_status` does not exist yet, or the flag is closed | No row is invented and no date is guessed: the answer names the ten fields as not available with the reason, and nothing else | None | AC5 |
| X4 | The same `v_ace_pod` row is read twice | One delivery entry exists; the repeat is counted; no notice and no entry changes | None | AC4 |
| X5 | A row names a notice reference that resolves to no notice | The row is returned unchanged; the read neither holds nor drops it; the check is the consumer's, and the held unknown row is kept on this service's References exception list | None | AC6 (the check is RWB-P6-E1055-APP) |
| X6 | The view, the database or the ledger does not answer | 503 with the platform problem envelope; no entry is written and no partial answer is presented | MSG-GEN-006; MSG-P1-022 | AC7 |
| X7 | The request names no business date | 422 with the field name; nothing is read | MSG-GEN-001 | AC1 |

X1 and X2 are the legacy exception paths of RWB-E1-055 this slice owns (X2 of the legacy story, and the failed batch of AC5); X4 is the repeated read of the legacy story (X4, AC7 and AC10) carried as one counted repeat. X3 is the path DL43 and TSD P1 T3.7 add: a Section B view that is not there yet must answer "not available" rather than an empty list that reads as "no delivery". X5 and X6 keep their legacy shape but cross no boundary: the unknown reference is no longer held here, and a failure of the view is now a failure of a service call.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency: one view, one table this service owns and one published shape of RWB-P6-E1055-CON with its fake |
| Negotiable | The class split, the page size and the exact envelope members are the squad's choice behind the contract; the ten fields, the gate and the delivery key are fixed |
| Valuable | One door to ACE's proof of delivery, stated with its age, and one recorded delivery per row |
| Estimable | One controller, one gate, one repository, one writer client, one counter, one index |
| Small | Fits one sprint with its tests, as the source slice of the legacy key |
| Testable | Every criterion is one read against a fixture of `v_ace_pod`, `v_ace_batch_status` and the ledger |

### 7. Acceptance criteria

```gherkin
Feature: Proof of delivery read and delivery entry of rwb-source-data

  Background:
    Given the WIN batch for source "WIN" and business date 2026-11-30 is COMPLETE in v_ace_batch_status
    Given v_ace_pod holds one row for 2026-11-30 with pod_key "POD-0001", account_key "ACC-0001", notice_ref "N-0001", sent_date 2026-11-26, barcode "RR123456789TH", callback_date 2026-11-28, delivery_status "DELIVERED", sent_type "NPL", source_system "WIN" and data_as_of 2026-11-30
    Given case "RC-2026-000123" holds the delivery of notice "N-0001" on contract "CT-77001"

  Scenario: AC1 The read returns the ten fields of a COMPLETE business date (new, D-RCV-60)
    When rwb-comms calls the proof-of-delivery read for business date 2026-11-30
    Then the answer holds 1 row with pod_key "POD-0001", account_key "ACC-0001", notice_ref "N-0001", sent_date 2026-11-26, barcode "RR123456789TH", callback_date 2026-11-28, delivery_status "DELIVERED", sent_type "NPL", source_system "WIN" and data_as_of 2026-11-30
    Then the rows are in ascending pod_key order and one row is returned per v_ace_pod row of the date
    Then the answer states the business date, the product code DP07 and the freshness stamp of DP07
    Then a request that names no business date is refused with 422 and MSG-GEN-001

  Scenario: AC2 A WIN batch that is not COMPLETE returns no row and marks DP07 stale (new, D-RCV-60)
    Given the WIN row for business date 2026-11-30 is FAILED at its record count check, or is not COMPLETE, or no WIN row exists for that date
    When rwb-comms calls the proof-of-delivery read for business date 2026-11-30
    Then the answer holds no row of 2026-11-30
    Then no row of 2026-11-25 or of any earlier business date is returned in its place
    Then the DP07 stamp of 2026-11-30 is STALE and MSG-P1-001 names "DP07 Legal" and 2026-11-23

  Scenario: AC3 A delivery recorded once gives one outbound LETTER entry (new, D-RCV-60)
    Given the WIN batch of 2026-11-30 is COMPLETE and the delivery of the row has not been recorded
    When rwb-comms reads the rows of 2026-11-30 naming case "RC-2026-000123"
    Then the interaction ledger of case "RC-2026-000123" holds 1 entry
    Then the entry carries event code "LETTER", direction outbound, the occurred time 2026-11-28 and the notice reference "N-0001"
    Then the entry carries the pod key "POD-0001" as its source reference and the delivery key as its idempotency key
    Then the entry carries no name, address, contact value or identity number

  Scenario: AC4 A second read of the same pod_key writes no second entry and counts the repeat (new, D-RCV-60)
    Given the delivery of pod_key "POD-0001" for notice "N-0001" with callback date 2026-11-28 is on the ledger of case "RC-2026-000123"
    When the rows of 2026-11-30 are read again for the same case
    Then the ledger of case "RC-2026-000123" still holds 1 entry for that delivery
    Then no second entry and no second case_seq are written
    Then the repeat is counted under R-UNI-40 and duplicate_count of the DP07 stamp of 2026-11-30 is 1

  Scenario: AC5 Before RWB-ACE-001 the read answers not available and invents nothing (new, D-RCV-60)
    Given v_ace_pod and v_ace_batch_status do not exist in the schema, or the flag rwb.dataengine.pod-read is closed
    When rwb-comms calls the proof-of-delivery read for business date 2026-11-30
    Then the answer holds no row and no business date is guessed
    Then each of pod_key, account_key, notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type, source_system and data_as_of is answered as not available with no value
    Then DP07 is STALE and MSG-P1-001 is answered, and no default, no placeholder date and no earlier row is written

  Scenario: AC6 The row carries the ten view fields and nothing else (new, D-RCV-60)
    Given the rows of business date 2026-11-30 are returned
    When the answer is compared with the v_ace_pod column list
    Then each row carries exactly pod_key, account_key, notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type, source_system and data_as_of
    Then no row carries a notice state, a case attribute, an address, a name, a contact value or an identity number
    Then the answer envelope carries the business date, the product code DP07 and the freshness stamp only

  Scenario: AC7 The view, the database or the ledger does not answer returns 503 and writes no entry (new, D-RCV-60)
    Given v_ace_pod, the database or the interaction ledger does not answer for business date 2026-11-30
    When rwb-comms calls the proof-of-delivery read for business date 2026-11-30 for case "RC-2026-000123"
    Then the answer is 503 with the platform problem envelope and presents no partial answer
    Then no entry is written to the interaction ledger of case "RC-2026-000123"
    Then MSG-GEN-006 names the failed source, and a failed ledger write is answered with MSG-P1-022

  Scenario: AC8 The business rules BR2, BR4, BR5 and BR8 hold in the read and the entry (new, D-RCV-60)
    Given the DP07 stamp of 2026-11-30 has LIT late and WIN COMPLETE, and the interaction ledger of case "RC-2026-000123" holds the delivery of notice "N-0001"
    When rwb-comms calls the proof-of-delivery read for business date 2026-11-30 for case "RC-2026-000123"
    Then the rows are read from recovery.v_ace_pod only, granted to rwb_source_data with no privilege on public, and this service does not open the WIN file
    Then DP07 is STALE because LIT is late, and the read states the stamp it found
    Then the entry's occurred time is the callback date 2026-11-28 and never the time the read ran
    Then the delivery is recorded once on the interaction ledger of case "RC-2026-000123"

  Scenario: AC9 Errors of the proof-of-delivery operation answer 401, 403 and 404 (new, D-RCV-60)
    When rwb-comms calls GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30 without a valid credential
    Then the answer is 401 with the platform problem envelope, holds no row and writes no entry
    When rwb-comms calls GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30 holding no permission on the operation
    Then the answer is 403 with the platform problem envelope, holds no row and writes no entry
    When rwb-comms calls a path of base /api/recovery/source-data/v1 that names no operation
    Then the answer is 404 with the platform problem envelope and holds no row
```

**Target reading.** Every value above is the legacy synthetic value of RWB-E1-055 and none of it is new: notice `N-0001`, case `RC-2026-000123`, contract `CT-77001`, barcode `RR123456789TH`, the sent date `26112026` read as 2026-11-26, the callback date 2026-11-28, the business dates 2026-11-25 and 2026-11-30 and the product "DP07 Legal". What changes is where each step runs. The read is a named operation of this service, `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=`, on base `/api/recovery/source-data/v1` (DP-11, DP-13; the address is this read, the record carries the ten view fields in ascending pod_key order, the generic API-P1-010 data-product read is the catalog read of its own story, and the envelope members and the page parameters are not specified in the source documents (GAP-0577; ASM-0819)). The rows come from `v_ace_pod`, a Section B view over ACE's `pod_receipt` (TSD P1 T3.3 row 24), read behind the flag until RWB-ACE-001 lands (DL43; open decision, assumptions ASM-0193, ASM-0737, ASM-0748 and ASM-0816). The gate is `v_ace_batch_status`, one row per source and business date, and its `is_complete` (TSD P1 T3.7; FSD P1 A2.14 BR-P1-014-2: freshness is read from the batch record only and never inferred from `data_as_of`, a row count or a file). The delivery entry is written through the ledger writer of this service, on `interaction` in `rwb_source_data`, which the R-PREC default ruling makes P1's ledger (DP-01, DP-18; Ownership Map, `interaction` owner P1); the entry is written by this service inside the same transaction as the read, for the case the caller names on the read as caseId; a read without caseId writes nothing, and rwb-comms writes only the dispatch entry (GAP-0578; ASM-0820). The repeat counter is `data_product_load.duplicate_count` of DP07 for the business date (TSD P1 T3.6; T3.7 Repeat), which is the counter the sources name for a repeated read; one increment per repeat read, with no ledger row and no log-only hit (GAP-0580; ASM-0822). The "not available" answer of AC5 is a 200 with no row, the ten field names marked not available with the reason SECTION_B_NOT_DEPLOYED, DP07 STALE and MSG-P1-001, behind the platform flag rwb.dataengine.pod-read; never an empty list alone and never a fallback to data_as_of (GAP-0579; ASM-0821). The message render of AC2 is recorded with GAP-0581 and ASM-0823. Legacy AC1 to AC11 are not claimed here: the matching, the notice state, the events, the timer and the file are RWB-P6-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP and RWB-ITG-E1055-ITG. JOB-10 runs as the Airflow file window with the P6 NoticeDispatchWorkflow; P2 rwb-integration delivers the INT-14 file on queue rwb-integration; this story reads pod rows and freshness through P1 and writes the delivery entry through P1; the P3 notice period timer starts from NoticeDelivered (GAP-0366).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A `v_ace_pod` row is read only when the ACE batch for source WIN is COMPLETE for its business date | Legacy RWB-E1-055 BR4; ACE batch record; INT-15 error handling |
| BR2 | The proof of delivery is read from ACE through `recovery.v_ace_pod`; the Workbench writes no WIN delivery fact and opens no WIN connection | REQ-DRI-006; D-RCV-35 U1; FSD P1 A2.1 BR-P1-001-2 |
| BR3 | Freshness is read from `v_ace_batch_status` only and never inferred from `data_as_of`, a row count or a file | FSD P1 A2.14 BR-P1-014-2 |
| BR4 | A product fed by more than one source carries the oldest business date among its sources and is STALE while any of them is late; DP07 is fed by LIT and WIN | FSD P1 A2.14 BR-P1-014-3; FSD P1 A2.2 DP07 row |
| BR5 | A notice period starts only from the delivery date on the proof of delivery, so the delivery date is carried unchanged and never derived | CTL-15; R-LIT-07; legacy BR2 |
| BR6 | The same proof-of-delivery fact twice produces one effect and the repeat is counted | R-UNI-40; legacy BR6 |
| BR7 | The notice data product is stale one business day after the WIN batch was due | v_ace_batch_status; MSG-P1-001; legacy BR7 |
| BR8 | One ledger holds every interaction on a case, and the delivery is recorded there once, on the case the delivery belongs to | REQ-ILG-001; REQ-ILG-004; DP-18 |

**Where each rule lives in the target.** BR1 and BR3 are one statement in this story and one in the freshness story: the gate is read from `v_ace_batch_status` at the door of the read, and the stamp is written by RWB-P1-E1015-APP; this story never computes a business date from a row and never trusts `data_as_of` as a completeness signal (BR3). BR2 is the schema boundary: `rwb_source_data` holds the grant on the view and no privilege on `public`, and the WIN file moves through rwb-integration only (DP-01, DP-02, DP-05; REQ-DRI-006). BR4 is why a DP07 stamp can be STALE because LIT is late while WIN is complete, and the read states the stamp it found rather than a status of its own. BR5 is why the entry's occurred time is the callback date of the row and never the time the read ran. BR6 becomes the delivery key plus the repeat counter, both inside this service. BR7 is the stale flag and the message of AC2. BR8 is the ledger's ownership: the entry is written through the writer of this service and no other service holds a copy of the ledger (DP-18).

### 9. State transitions

This story changes no notice state and starts no timer; both are rwb-comms and rwb-case. It writes a ledger entry, and it moves the DP07 freshness stamp by reading it.

| From | Event | Condition | To |
|---|---|---|---|
| DP07 with no stamp for the business date | a COMPLETE WIN row is read | `is_complete` is true for the requested date | A DP07 stamp for the business date, LOADED, as the freshness story writes it |
| DP07 at an earlier business date | the WIN batch of the requested date is late, failed or absent | The gate finds no complete row | DP07 STALE with the earlier business date still in use |
| A case at case_seq n | the delivery of a pod row is recorded | The WIN batch is COMPLETE and the caller names the case | The case is at case_seq n+1 and one outbound LETTER entry exists |
| A delivery already on the ledger | the same row is read again | The same pod key, notice reference and callback date | No change to the ledger; the repeat is counted |
| An applied migration version | a correction of the delivery lookup index | The index needs a fix | A new version on the service sequence; the applied version is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The service identity of rwb-comms | The only caller of the read: the DP07 rows of one business date and the delivery entries of the case it names (Case record R on that case) |
| RW-LITOFF, litigation officer | Reads the delivery date, the barcode and the delivery status on the notice panel of rwb-comms; calls nothing of this service directly (Litigation R) |
| RW-CASEOWN, case owner | Reads the delivery on the case record view; calls nothing of this service directly (Litigation R) |
| RW-DATASTEW, data steward and data product owner | Reads the DP07 freshness stamp, the stale flag and the repeat count |
| RW-PLATADM, platform administrator | Opens and closes the flag of the read and reads the series of the deployment |
| rwb-source-data | Runs as its own login, holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on any ACE table (DP-02; Architecture v5 slides 11 and 29) |
| rwb-comms (P6) | Owns the notice, the row-to-notice matching, the unknown-reference hold, the two events and the displayed message; answers the case of the delivery it names (C RWB-P6-E1055-CON) |

The read carries the caller's token and the case it names, and the ledger entry is written for that case. Before any row is read, the read calls the rwb-access authorise check of DP-08 on the caller's token and the case it names; a refusal returns MSG-P4-002 and no row. This service decides no right of its own on a notice: it answers source data to an authenticated service identity, and the right on the notice is enforced where the notice lives.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-251 | v_ace_pod | pod_key | Read |
| DF-ACE-252 | v_ace_pod | account_key | Read |
| DF-ACE-253 | v_ace_pod | notice_ref | Read |
| DF-ACE-254 | v_ace_pod | sent_date | Read |
| DF-ACE-255 | v_ace_pod | barcode | Read |
| DF-ACE-256 | v_ace_pod | callback_date | Read |
| DF-ACE-257 | v_ace_pod | delivery_status | Read |
| DF-ACE-258 | v_ace_pod | sent_type | Read |
| DF-ACE-259 | v_ace_pod | source_system | Read |
| DF-ACE-260 | v_ace_pod | data_as_of | Read |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | source_system, business_date, status, is_complete | Read (the gate) |
| DF-INT-002 | interaction | case_id | Write, through the ledger writer |
| DF-INT-004 | interaction | occurred_at | Write, through the ledger writer |
| DF-INT-005 | interaction | channel | Write, through the ledger writer |
| DF-INT-006 | interaction | direction | Write, through the ledger writer |
| DF-INT-011 | interaction | summary | Write, through the ledger writer |
| DF-INT-014 | interaction | event_code | Write, through the ledger writer |
| DF-INT-018 | interaction | idempotency_key | Write, through the ledger writer |
| DF-INT-019 | interaction | case_seq | Allocated and written by the ledger writer |
| DF-OPS-007 | data_product_load | status | Read (the DP07 stamp the answer states) |
| DF-OPS-009 | data_product_load | duplicate_count | Write (plus one on a repeat read) |

Field IDs are those in the Logical Data Model and Data Dictionary.

**Which side is this story's.** `DF-ACE-251` to `DF-ACE-260` are ACE's own columns, read through `v_ace_pod` and never written; the ten of them are the whole row this story answers, and the view carries no name, address or contact value, so no personal field of ACE enters the answer (TSD P1 T3.3). `DF-ACE-178` to `DF-ACE-186` are ACE's batch record, read through `v_ace_batch_status` for the gate only. `DF-INT-002` to `DF-INT-019` are this service's own ledger rows: this story supplies the values and the writer allocates `case_seq` and stores the idempotency key; no field is inserted directly. `DF-OPS-007` is read and `DF-OPS-009` is incremented on the stamp of RWB-P1-E1015-APP, which owns the row and its keys.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1` (DP-13). One operation, the proof-of-delivery read of the DP07 product.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proof-of-delivery?businessDate=` | Reads the WIN proof-of-delivery rows of one business date from `v_ace_pod`, one row per ACE row in ascending `pod_key` order, only when the WIN row in `v_ace_batch_status` is COMPLETE for that date; with `caseId` it also records the delivery entries of that case through the ledger writer | Service identity of rwb-comms, Case record R on the named case; one hop, 2 s budget | Idempotent: a repeat returns the same rows, and with the same `caseId` it writes no second ledger entry (R-UNI-40) |

The answer is `ProofOfDeliveryPage` of RWB-P6-E1055-CON: the business date, the product code `DP07`, the freshness stamp of DP07 (status, source business date and the time the stamp was written) and the rows. Each row is the ten-field record of AC6, mapped one to one from `v_ace_pod` with `sent_date` and `callback_date` in the ISO form on the wire. Errors are 401 without a session, 403 for a case outside the caller's scope (MSG-P4-002), 422 for a missing or invalid field (MSG-GEN-001), and 503 when the views or the ledger do not answer (MSG-GEN-006, MSG-P1-022). The page parameters, the element types, the exact error set and the second query parameter `caseId` are a target choice and are not specified in the source documents (GAP-0577; ASM-0819; GAP-0578; ASM-0820).

The ledger entry is not a second operation of this story: it is written through the append operation of the interaction ledger, `POST /api/recovery/source-data/v1/interactions`, inside this service and in the same transaction as the read, so the writer's rule on the time, the actor, the list and the allocator is applied once, in one place (DP-18; RWB-P1-E1066-CON).

Until RWB-ACE-001 lands and `v_ace_pod` is available, the read stays behind its feature flag. The fallback is proof entered by hand against the barcode, to be agreed with the litigation business owner before wave 2 (GAP-1608). The WIN dispatch file layout is a versioned interface definition owned by rwb-integration and is held as a contract item before wave 2; the dispatch is built against a fake of that definition until the layout is agreed with the WIN owner (GAP-1602).

#### 12.2 REST operations consumed

None at run time. This story is the provider side of the shape RWB-P6-E1055-CON publishes: rwb-comms calls this read, and this story calls nothing of rwb-comms. The only calls it makes are inside its own service — the ledger writer of RWB-P1-E1066-CON and the DP07 stamp of RWB-P1-E1015-APP — and neither is a hop of the 2 s budget that DP-11 governs. No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slides 15 and 43). The delivery entry is a same-service write on this service's own ledger and no event announces it; the business event a notice period rests on, `rwb.comms.NoticeDelivered.v1`, is rwb-comms' and is published by RWB-P6-E1055-APP (DP-09). This story adds no message schema.

#### 12.4 Events consumed

None. No event starts this read: rwb-comms calls it after the WIN file window, and Architecture v5 slide 15 gives this service no consumed event. `AceDataReady` and `AceDataLate` are on this service's producing side, and the batch completeness the gate needs is read from `v_ace_batch_status` and not waited for as a message.

#### 12.5 Workflows and activities

None. The read is a synchronous step and writes one row per delivery in one transaction. The task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and this story registers no workflow and no activity on it: the activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` of Architecture v5 slide 15 are RWB-P1-E1015-APP's and the case-list stories'.

#### 12.6 Schedules

None. The 06:00 daily read of the legacy story (`v_ace_pod` read path, RWB-E1-055 section 12) is not a Schedule of this story. In the target the pod read is started by the slice that owns the run: the DP07 cut-off Schedule of RWB-P1-E1015-APP marks the product and the pod step of RWB-P6-E1055-APP calls this read after the WIN file window; this operation answers on demand and holds no state, so no Temporal Schedule is registered here and DP-10 applies as a statement only — no Quartz trigger and no row of a shared job table survives the move (Architecture v5 slide 44).

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_pod` | `recovery` | ACE team (Tier 2 Section B view over ACE `pod_receipt`); SELECT to `rwb_source_data` only | Read only, the ten fields of AC6; a view and not a table, and the table behind it is ACE's and outside the 19 schemas; it exists only after RWB-ACE-001 |
| `v_ace_batch_status` | `recovery` | ACE team (Tier 2 Section B view over ACE `ace_batch_run`); SELECT to `rwb_source_data` only | Read only: `source_system`, `business_date`, `status` and `is_complete`, the gate of AC2 |
| `interaction` | `rwb_source_data` | P1 rwb-source-data (Ownership Map) | The ledger of the delivery: inserted through the writer only, with the lookup index of section 13; this story updates and deletes nothing |
| `data_product_load` | `rwb_source_data` | P1 rwb-source-data (Ownership Map) | The DP07 stamp of the business date: status read, `duplicate_count` incremented by one on a repeat; the stamp itself is RWB-P1-E1015-APP's write |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_source_data` | PLT library objects, created in this service's schema | The writer's stored response and the idempotency key of the delivery; read and written by the library, not by this story |

`v_ace_pod` and `v_ace_batch_status` are views, not tables: the Ownership Map names tables of the 19 schemas, and an ACE table is ACE's, so no ownership row is invented for `pod_receipt` or `ace_batch_run`. The notice is `rwb_comms`' and the case is `rwb_case`'; both are reached through rwb-comms' own answer and never read here. No table of another service is read and no foreign key crosses a schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P6-E1055-CON fake | The proof-of-delivery record and page shape, and the delivery fact of the key | The ten-field record of AC6 for business date 2026-11-30, the empty answer of AC2, the "not available" answer of AC5, and the repeat answer of AC4 |
| View fixture | `recovery.v_ace_pod` and `recovery.v_ace_batch_status` in a container | One pod row of 2026-11-30 with `RR123456789TH`, notice `N-0001` and callback date 2026-11-28; a second row of 2026-11-25; batch rows for WIN COMPLETE, FAILED at its record count check and absent; LIT not COMPLETE beside a complete WIN |
| Ledger fixture | `rwb_source_data` | A container at the baseline plus the ledger columns, the unique key on the idempotency key and this story's index, so the repeat of AC4 runs on the real key and the real allocator |
| Flag-closed fixture | The service with `rwb.dataengine.pod-read` closed | The AC5 answer, with no view present in the schema |

No WIN connection is opened and no production payload is copied into a fake: the pod values are the legacy synthetic values of RWB-E1-055.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation on `/api/recovery/source-data/v1` | None | One hop, 2 s budget for the caller; the ledger write and the stamp read are same-service calls (DP-11) |
| Kafka | None | None | The topic belongs to RWB-P1-E1015-APP; `NoticeDelivered` is rwb-comms' and belongs to RWB-P6-E1055-APP |
| Temporal | None | None | No workflow, activity or Schedule in this story (DP-10 as a statement) |
| File | None | None | INT-15 is ACE's inbound file and INT-14 is rwb-integration's outbound file; this service opens neither |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `pod`, with the published types in `...sourcedata.api`. Base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**How each pattern applies here.**

- **DP-01.** `interaction`, `data_product_load` and the library tables live in `rwb_source_data`; the notice, the case and the calendar are not copied and not joined. A delivery row holds ACE business keys — `pod_key`, `account_key`, `notice_ref` — as references and never as foreign keys, so nothing crosses a schema.
- **DP-05.** This is one of the two views DP-05 is about: `v_ace_pod` is read here and nowhere else in the Workbench, and `v_ace_batch_status` beside it. The read is the service's own `v_ace_*` read, which is why the pattern adds no dependency; the consumer answers of RWB-P6-E1055-CON exist so that no other service needs the grant.
- **DP-07.** This story enumerates no list value of its own: the product code `DP07`, the freshness status and the threshold of a late batch are read as data — the stamp and its status from RWB-P1-E1015-APP, and any run-time list through the reference-data client library of the platform baseline, which is the wave-0 side of the DP-07 row. The `LETTER` event code and the channel of the ledger entry are values of the lists the ledger writer reads, never constants in this story.
- **DP-09.** No event is published and none is consumed: the delivery entry is a same-service ledger write and `NoticeDelivered` is rwb-comms'. The pattern applies as the prohibition that keeps this read out of the event path — the outbox and inbox library of the ledger writer is the only event-adjacent machinery this story touches, and it touches it through the writer.
- **DP-10.** Applies as a statement: the 06:00 job of the legacy story is gone with Quartz, and no Schedule, no workflow and no activity of this read is registered here (12.6). The cut-off that decides when the pod read may run is RWB-P1-E1015-APP's Schedule and the run itself is rwb-comms'.
- **DP-11.** Applies from the caller's side: the read is a REST contract with one hop and a 2 s budget, and the two things this story calls are inside its own service, so the read adds no hop to the chain. Its 503 answers carry the platform problem envelope so that a caller's breaker sees a plain failure.
- **DP-15.** This story adds one version to the service's own Flyway sequence, in schema `rwb_source_data`, for the delivery lookup index, and it reuses the ledger columns the ledger story created rather than re-creating them (see Migrations below).
- **DP-18.** The ledger is this service's own (R-PREC default ruling; Ownership Map, `interaction` owner P1), and this story is a consumer of its own writer: the delivery entry is written there and read back from there, and no other service holds or writes a delivery line.
- **DP-19.** Applies as a statement for the person: the litigation officer and the case owner see the delivery on the notice panel and the case record view, which arrive through the gateway-bff composite route, and never call this operation. The only caller of this operation is a service identity.

The platform H rows of the pattern table are delivered by the wave-0 platform and are not repeated in the metadata H field of this story, which stays empty by rule (Template and Rules §R5.7 rule 2): the story is Day 1 on the pipeline baseline, and the one contract it builds against as a dependency is RWB-P6-E1055-CON with its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ProofOfDeliveryController` | Controller | The operation of 12.1 on `/api/recovery/source-data/v1`; parameter validation; RFC 9457 problem details |
| `SectionBGuard` | Guard | Reads the flag `rwb.dataengine.pod-read` and answers the ten fields as not available when the Section B views are not deployed (AC5) |
| `WinBatchGate` | Service | Reads `v_ace_batch_status` for source WIN and the business date and decides whether a row of that date may be read; marks DP07 STALE and renders MSG-P1-001 (AC2) |
| `ProofOfDeliveryRepository` | Repository | Reads `v_ace_pod` for the business date in ascending `pod_key` order; no write method exists |
| `PodReceipt` | Record | Immutable mapping of the ten view fields |
| `ProofOfDeliveryPage` | Record | The answer: business date, product code, freshness stamp and rows |
| `DeliveryLedgerWriter` | Client, in-service | Appends the delivery entry through the ledger writer of RWB-P1-E1066-CON, with the delivery key as the idempotency key (AC3, AC4) |
| `DuplicateCounter` | Service | Adds one to `duplicate_count` of the DP07 stamp when the delivery key is already stored (AC4) |
| `V<next>__rwb_e1_055_pod_delivery_index.sql` | Migration | The delivery lookup index on `interaction`, on the service's own sequence |

**Migrations and sequence (DP-15).** One version on rwb-source-data's own Flyway sequence, after the ledger version and after the freshness version it depends on at run time: the index `ix_interaction_pod_delivery` on `(event_code, source_ref)` of `interaction` in `rwb_source_data`, so that the read can tell a recorded delivery from a new one without a second key. The columns the entry needs — `event_code`, `direction`, `source_ref`, `idempotency_key` and `case_seq` — are created by the ledger version of RWB-P1-E1066-APP and are not re-created here; this story adds no table and no column. The exact version number is assigned by the sequence owner at build time, no monolith version number is reused, and an applied version is never edited.

**Database.** This story owns no table shape: it inserts into `interaction` through the writer and increments one column of `data_product_load`. It creates no table of another service, adds no foreign key across a schema, and reads ACE only through the two Section B views (DP-01, DP-05).

**Configuration and reference data**

- The flag `rwb.dataengine.pod-read` is a data row of the platform library and gates the read until RWB-ACE-001 lands (DL43; GAP-0579; ASM-0821).
- The product code `DP07` and the freshness status values come from the catalog and the stamp, not from the code; the product name rendered in MSG-P1-001 ("DP07 Legal") is the catalog value and the date is the last complete business date of the stamp (GAP-0581; ASM-0823).
- The ledger `LETTER` event code, the channel and the direction are values of the lists the ledger writer reads, and no list value is written in this story's code (DP-07).
- The 2 s budget, the single GET retry and the breaker of the caller are configuration of the edge; the page size and the maximum page of this read are configuration of this service (GAP-0577; ASM-0819).
- The delivery key of the ledger entry — pod key, notice reference and callback date — is a rule of this story and not a configuration value; a change of it is a new version of the writer's contract.

**Build steps**

1. The read operation on the base, with the parameter validation of X7 and the problem envelope of 12.1.
2. `SectionBGuard` and the "not available" answer, with the flag fixture of 12.8 (AC5).
3. `WinBatchGate`: the batch row of source WIN and the business date, the FAILED path, the absent row and the no-earlier-date rule (AC2).
4. `ProofOfDeliveryRepository` and the ten-field mapping, with `ace_to_date` on the two dates and the null-on-dirty rule (AC1, AC6).
5. The ordering and the paging of the rows, and the page element of the answer.
6. `DeliveryLedgerWriter`: one entry per row for the named case, the delivery key as the idempotency key, and the read-back that proves one entry (AC3).
7. `DuplicateCounter` and the repeat path, on the real unique key of the ledger fixture (AC4).
8. The migration of the lookup index on the service sequence, with a repeated run that changes nothing.
9. Tests for AC1 to AC6 with the fakes of 12.8, and the regression rows of section 16 where the fixture of the owning slice is available.

**Feature flag.** `rwb.dataengine.pod-read`. Off, the read answers the ten fields as not available and no row, no stamp and no entry are written.

**Done when.** The tests of section 16 pass, the read answers the ten fields for a COMPLETE WIN business date against the view fixture, a FAILED or absent batch answers no row with DP07 STALE and MSG-P1-001, one delivery yields one outbound `LETTER` entry with the delivery date and the notice reference, a second read yields no second entry and counts the repeat, the flag-closed answer invents nothing, and the index is applied on the service sequence.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The WIN batch is late, failed or not COMPLETE for the business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | The source views or the database do not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-022 | The delivery entry could not be written | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | The request names no business date, or names an invalid one | Enter {field}. |
| MSG-P4-002 | The caller names a case outside its scope | You cannot {action} here. Your role does not include it. |

The wording of MSG-P1-001 is the FSD P1 v3 rendering, which names the ACE batch rather than a load (FSD P1 OQ-P1-07). {product} is the catalog name DP07 and {date} is the last complete business date of the DP07 stamp; the test fixture keeps "DP07 Legal" and 2026-11-23. The wording is left to OQ-P1-07 (GAP-0581; ASM-0823). MSG-GEN-006 takes the name of what failed; MSG-P1-022, MSG-GEN-001 and MSG-P4-002 are passed on unchanged from the ledger writer and from the case check, and the field name of MSG-GEN-001 is filled from the validation failure and is never a data value. Thai text for each message follows decision DL10 (open decision, assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863).

### 15. Screens and states

No screen in this story. The litigation officer and the case owner see the delivery date, the barcode and the delivery status on the notice panel and on SCR-03 Case record, both served by rwb-comms and reached through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and the data steward sees the DP07 freshness stamp, the stale flag and the repeat count on SCR-45 Data quality (RWB-P1-E1015-APP). This operation has no screen: it is called by a service. When the read answers "not available" or no row, the notice panel shows MSG-P1-001 with the age of the product, and the delivery state of the notice is left as it was; this story renders none of it. The states of SCR-03 Case record are loading, as Screen Specifications v1 section SCR-03 gives them; empty, error and no access: Not specified in the source documents (CG-ALL-2230). The states of SCR-45 Data quality are loading, as Screen Specifications v1 section SCR-45 gives them; empty, error and no access: Not specified in the source documents (CG-ALL-2231).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1 — regression evidence: the dispatch, the notice state and the outbox belong to the rwb-comms slice | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2 — regression evidence: the notice state, the callback date and the timer belong to the rwb-comms and rwb-case slices | End to end | v_ace_pod row for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 — regression evidence: the sample file ingestion and its batch row are ACE's and RWB-ITG-E1055-ITG's | End to end | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4 — regression evidence: the file retry and the task on the third failure belong to the rwb-comms slice | End to end | No acknowledgment on three runs |
| TC-E1-055-05 | AC2, BR1, BR3 — the gate of this story, with AC2's legacy origin AC5 | Component | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6 — regression evidence: the unknown reference is returned here and held on the exception list by the rwb-comms slice; the rwb-document slice carries the letter | Component | 30 rows, 1 unknown |
| TC-E1-055-07 | AC4, BR6 — the repeat of this story, with AC4's legacy origin AC7 | Component | v_ace_pod rows of 2026-11-30 read twice |
| TC-E1-055-08 | Legacy AC8 — regression evidence: the repeated dispatch file is the rwb-comms slice and JOB-10 | End to end | JOB-10 rerun on 2026-11-25 |
| TC-E1-055-09 | Legacy AC9 — regression evidence: the barcode reconciliation break REC-09 belongs to the rwb-comms slice | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC4, BR6 — the second delivery row of this story, with AC4's legacy origin AC10 | Component | Repeat of RR123456789TH on 2026-12-07 |
| TC-E1-055-11 | AC2, BR7 — the late batch of this story, with AC2's legacy origin AC11 | Component | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access — regression evidence: the notice dispatch detail and its refusal belong to the rwb-comms slice | Component | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |
| TC-E1-055-13 | AC1, AC6 — contract of the proof-of-delivery operation of §12: the ten fields of the view in the answer | Contract | Operation GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30 against the RWB-P1-E1055-CON fake |
| TC-E1-055-14 | AC6, §12.7 — boundary of the ten columns of v_ace_pod and the four columns of v_ace_batch_status (ASM-3438) | Component | v_ace_pod row with the ten columns; v_ace_batch_status row with source_system, business_date, status and is_complete |
| TC-E1-055-15 | AC7, X6 — the view, the database or the ledger does not answer: 503, no partial answer and no entry | Component | v_ace_pod, database or ledger not answering for 2026-11-30 |
| TC-E1-055-16 | BR2, BR8 — the schema boundary and the one ledger of the delivery entry | Component | interaction fixture of case RC-2026-000123; grant on recovery.v_ace_pod to rwb_source_data and no privilege on public |
| TC-E1-055-17 | BR4, BR5 — DP07 stamp fed by LIT and WIN with LIT late; the delivery date carried unchanged | Component | DP07 stamp of 2026-11-30 with LIT late and WIN COMPLETE; callback_date 2026-11-28 |
| TC-E1-055-18 | AC8, BR2, BR4, BR5, BR8 — the schema boundary, DP07 fed by two sources, the callback date and the one ledger | Component | Not specified in the source documents (NEWAC-RWB-P1-E1055-APP-AC13) |
| TC-E1-055-19 | AC9 — error answers 401, 403 and 404 of the proof-of-delivery operation | Contract | Not specified in the source documents (NEWAC-RWB-P1-E1055-APP-AC14) |

The twelve are the legacy test cases of RWB-E1-055 in their legacy order, with the Level column added and System mapped to End to end and Access to Component, as in the other stories of this run. TC-E1-055-13 and TC-E1-055-14 are the contract and boundary tests of §12 and §12.7; TC-E1-055-15 is the error criterion AC7; TC-E1-055-16 and TC-E1-055-17 cover the rules BR2, BR4, BR5 and BR8 that had no test; TC-E1-055-18 and TC-E1-055-19 cover AC8 and AC9. TC-E1-055-05, TC-E1-055-07, TC-E1-055-10 and TC-E1-055-11 are four of the criteria this story owns — the gate, the repeated read, the second delivery row and the late batch — and they run here against the view fixture, the ledger fixture and the fakes of 12.8. The other eight rows are kept as regression evidence for the slices of this legacy key that own those criteria, and they run again against the live services in RWB-ITG-E1055-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the product code, the product name, the freshness status values, the `LETTER` event code and the channel come from the catalog, the stamp and the lists; the page size, the retry, the 2 s budget and the flag are configuration.
- No personal data in an answer, a log, a test or a prompt: the ten view fields carry no name, address, contact value or identity number, the log holds the business date, the pod count, the case ID and the error class, and no field of `v_ace_customer` or `v_ace_contact` is touched by this story.
- No read of another service's tables and no `public.*` read: ACE data is reached only through the 30 `recovery.v_ace_*` views, which is why this read exists at all (DP-01, DP-05; FSD P1 A2.1 BR-P1-001-2).
- No WIN connection and no file: INT-14 and INT-15 are rwb-integration's and ACE's, and this service opens neither (REQ-DRI-006; legacy guardrail 4).
- No second delivery line: the entry is written through the writer with the delivery key, and the ledger's unique key on the idempotency key is what makes the repeat a no-op rather than a hope (R-UNI-40).
- No invented date and no earlier date: a date whose WIN batch is not COMPLETE answers no row, and a Section B view that is not there answers "not available" — never an empty list that reads as "no delivery" and never a fallback to `data_as_of` (BR3; DL43).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).
- The platform library objects stay the library's: `outbox_event`, `processed_event` and `idempotency_key` are created in this schema and are never redefined by this story (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, and proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-UNI-40 | TC-E1-055-02, TC-E1-055-05, TC-E1-055-07, TC-E1-055-10, TC-E1-055-11 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-07, TC-E1-055-10 |
| REQ-DRI-006 | No component calls a system of record directly; source data is read through the read-only views and leaves only through paths ACE already has | Business Requirements Program, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | CTL-15 | TC-E1-055-05, TC-E1-055-11, TC-E1-055-14, TC-E1-055-16 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P6-E1055-CON | Contract | C: the proof-of-delivery record and page shape this read answers, and its fake; no operation of rwb-comms is called |
| RWB-P1-E1066-APP | App development | Same-service sibling: the ledger store and the writer through which the delivery entry is written, with its allocator and its idempotency key |
| RWB-P1-E1015-APP | App development | Same-service sibling: the DP07 stamp, the stale flag and the repeat counter this read states and increments |
| RWB-P6-E1055-APP | App development | Consumer of this read: the WIN file, the acknowledgment, the row-to-notice matching, the unknown-reference hold, the two events and the displayed message |
| RWB-P3-E1055-APP | App development | The notice state and the `NOTICE_PERIOD` timer started from the delivered date |
| RWB-P5-E1055-APP | App development | The stored letter behind a notice, read by rwb-comms |
| RWB-ITG-E1055-ITG | Integration | Proves the whole loop, AC1 and AC9 included, on the live services and the live ACE batch record |

### 19. Out of scope

- The outbound WIN file, the trailer and the dispatch (INT-14, JOB-10) and the acknowledgment that sets the sent date, the barcode and the sent type (RWB-P6-E1055-APP and RWB-ITG-E1055-ITG).
- The row-to-notice matching by barcode and then by `notice_ref`, the notice state, and the hold of a row whose reference names no notice (RWB-P6-E1055-APP).
- `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1`, and the `NOTICE_PERIOD` timer that rwb-case starts from the delivered date (RWB-P6-E1055-APP, RWB-P3-E1055-APP; R-LIT-07).
- The WIN inbound interface INT-15, its file layout, its ingestion checks and its batch row: ACE's and the ACE team's (RWB-ACE-001; INT-15 owner ACE team).
- The freshness stamp itself, the cut-off Schedule, the stale flag and `AceDataReady` and `AceDataLate` (RWB-P1-E1015-APP).
- The notice period clock (GAP-2247): this story is a secondary slice and owns no legacy criterion. RWB-P3-E1055-APP starts the NOTICE_PERIOD timer from NoticeDelivered and RWB-P3-E5002-APP from the S4 delivery answer, both on one clock keyed on notice and delivered date; a second fact is a repeat under R-UNI-40. Revisit at the wave 3 refinement of RWB-P3-E5002-APP.
- The ledger read interface and its filters, and the case timeline built on the ledger (RWB-P1-E1068-APP and rwb-case).
- The refused and undeliverable letters, the proof window and the queue transfer (RWB-E2-021, R-LIT-08, R-LIT-09).
- The gateway-bff composite route, the notice panel and the case record view (RWB-PLT-N001-CON and the screen owners).
- The deployment, the flag row, the dashboards, the alerts and the runbook of this read (the P1 deployment story of this wave).
