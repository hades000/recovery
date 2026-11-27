# RWB-P1-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- RD-P1-007 with X-19 and X-20: this story only reads; rwb-comms alone appends delivery entries, so the idempotency key, channel, delivery status and occurred-time rules are rwb-comms' (findings #1, #2, #4, #6, #7, #15, #16, #20, #21).
- RD-P1-005: the read, its field names and errors are those of `GET /proof-of-delivery` in `rwb-source-data.yaml` 5.1.0 (findings #3, #8, #11, #22).
- RD-P1-041 and RD-P1-043: freshness pass-through, single stamp writer, repeat metric and the flag-closed answer (findings #5, #12, #13, #14).
- Criteria restated with concrete values and AC14 and AC15 added; messages follow Error and Message Standard v6 (findings #9, #10, #17, #18, #19). Open items, including paging, the read right and metric details, are in section 20 (findings #23, #24).
- Batch D (RD-P1-064): rwb-comms stays the one caller of the read and the one appender of delivery entries, hand-recorded proof included; delivery entries pair with the dispatch entry on the barcode, else the notice reference; rwb-asset does not call the read. Test case IDs of Test Cases v9 cited.

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
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-004; RD-P1-005; RD-P1-007; RD-P1-023; RD-P1-041; RD-P1-043, RD-P1-064 |
| Parallel lane | L-P1-M |
| Ready to start | Day 1 |
| Size | Not specified; pending refinement |
| Depends on (build) | None |
| Contract dependencies | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-source-data. The proof of delivery from WIN is read from `v_ace_pod` through `GET /proof-of-delivery?businessDate=`. Under RD-P1-007, rwb-comms appends matched delivery entries; this story reads only. The read stays behind its flag until the Section B views are available (DL43).

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1055-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 28 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-004; RD-P1-005; RD-P1-007; RD-P1-023; RD-P1-041; RD-P1-043.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the proof of delivery that ACE ingests from WIN to be read from the Workbench source-data service for a business date whose WIN batch is COMPLETED**, so that **the delivery date a notice period is counted from is the one the bank's own record holds, stated with its age**.

This is the rwb-source-data slice of legacy RWB-E1-055, and it owns no legacy criterion: the criteria of the key are owned by the rwb-comms slice (RWB-P6-E1055-APP: AC2 to AC8 and AC10 to AC11), by the rwb-case, rwb-document and rwb-comms slices between them, and by the cross-service proof RWB-ITG-E1055-ITG (AC1 and AC9). What this story delivers is the source side of that loop, and it is worth a story of its own because it is the only door in the Workbench to the proof of a delivery:

- **the read** — `GET /proof-of-delivery?businessDate=` on base `/api/recovery/source-data/v1`, one row per `v_ace_pod` row of the business date, in pod-key order, carrying the ten columns of the view under the contract names `podKey`, `accountKey`, `noticeRef`, `sentDate`, `barcode`, `callbackDate`, `deliveryStatus`, `sentType`, `sourceSystem` and `dataAsOf`;
- **the WIN batch gate** — a row of the date is returned only when the WIN row in `v_ace_batch_status` is COMPLETED for that date; otherwise the answer holds no row, nothing of an earlier date is served in its place and the DP07 freshness stamp in use is passed through, from which the consumer shows MSG-P1-001 when its status is STALE;
- **the writer boundary** - this story only reads. After rwb-comms matches a row to a case, rwb-comms alone appends a delivery entry over REST under RD-P1-007 (X-20); this story does not write `interaction` or `data_product_load`;
- **the Section B discipline** — `v_ace_pod` is a Section B view over the ACE table `pod_receipt`, so the read stays behind its flag until RWB-ACE-001 lands and answers no row with DP07 STALE until then (DL43).

It does **not** match a row to a notice by barcode or by `notice_ref`, append a delivery entry, change a notice state, start the `NOTICE_PERIOD` timer, hold a row with an unknown reference, open a WIN connection, or send or acknowledge a file. The caller is rwb-comms. rwb-asset does not call it: its notice step (RWB-S5-E3022-APP) reads delivery state from `GET /cases/{caseId}/interactions` (`latestDeliveryStatus` of the LETTER entry) or from rwb-comms `GET /notices/{noticeId}` (RD-P1-064).

### 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from a print date can be challenged in court. The Workbench writes no WIN delivery fact of its own: ACE ingests the WIN proof-of-delivery file (INT-15) into `pod_receipt`, and the Workbench reads the result through the view `recovery.v_ace_pod` (D-RCV-35 U1; Architecture v5 slide 41; TSD P1 T5.1). One reader of ACE's views is the whole point of ADR-010: rwb-source-data holds the grant, and every other service asks it (REQ-DRI-006). So the delivery fact a notice period rests on must leave this service in a shape that says how old it is and never in a shape that silently serves yesterday's rows.

The batch gate is the part that has to survive the move. In the monolith the read ran inside one job beside the ACE batch record; in the target the read is on demand and may be asked at any hour, so the date's completeness is checked at the door. A WIN batch that is late, failed at its record count check or absent yields no row of that date, no earlier date in its place, DP07 STALE and MSG-P1-001: a notice period that starts one day early is a legal defect, and a period that starts from an earlier delivery is worse than a period that starts late and says so (FSD P1 A2.14 BR-P1-014-2 and BR-P1-014-3; TSD P1 T3.7).

The interaction ledger is owned by rwb-source-data, but this story is a reader only. After rwb-comms matches the returned row to a case, rwb-comms appends the delivery entry through `POST /cases/{caseId}/interactions` under RD-P1-007. P1 does not append, maintain a delivery key, or change the freshness stamp. DP07 delivery repeats are counted by `rwb_source_data_win_delivery_repeat_total` under RD-P1-041; the metric trigger and labels remain Pending, owner data architect, tracked as GAP-0580. This read supports REQ-OCC-003 and REQ-DRI-006; the append belongs to the rwb-comms story.

### 3. Preconditions

- The wave-1 service baseline of rwb-source-data is in place: schema `rwb_source_data`, the `interaction` table with its ledger columns, the running per-service Flyway sequence with its own history table, the REST base `/api/recovery/source-data/v1`, the task queue name `rwb-source-data` in namespace `rwb-recovery` and the login `rwb_source_data` with SELECT on the 30 `recovery.v_ace_*` views and no privilege on any ACE table (DP-01, DP-02, DP-13, DP-15).
- **No build dependency of its own.** This is a read over `v_ace_pod`, `v_ace_batch_status` and the DP07 freshness answer. It does not require an interaction append component, a ledger migration or a freshness write.
- `GET /proof-of-delivery` and the schemas `ProofOfDeliveryAnswer` and `ProofOfDeliveryRow` are published in `rwb-source-data.yaml` 5.1.0; this story is the provider and publishes the fake. RWB-P6-E1055-CON consumes it. This story calls no operation of rwb-comms.
- RWB-P1-E1066-CON publishes the shared interaction append contract. Under RD-P1-007, rwb-comms (RWB-P6-E1055-APP) is the only appender of delivery entries and calls `POST /cases/{caseId}/interactions` after matching; this story makes no append call and does not write `interaction`.
- RWB-P1-E1015-APP owns and writes the DP07 freshness stamp in `data_product_load`; this story reads the stamp only. Under RD-P1-041, DP07 delivery repeats use metric `rwb_source_data_win_delivery_repeat_total`; this story does not change `duplicate_count`.
- The feature flag of this read is a data row of the platform library and is closed until RWB-ACE-001 has created `v_ace_pod` and `v_ace_batch_status` (DL43; TSD P1 T3.2 and T3.7; GAP-0579; ASM-0821).
- The caller is the service identity of rwb-comms, holding a workload identity token, and never a person: a person reaches the delivery through the notice panel of rwb-comms and the gateway-bff composite route (DP-19).
- Pending: page parameters and response paging shape, owner data architect, tracked as GAP-0577; the Section B unavailable answer remains tracked as GAP-0579; metric trigger and labels for `rwb_source_data_win_delivery_repeat_total`, owner data architect, tracked as GAP-0580; MSG-P1-001 rendering, owner product owner, tracked as GAP-0581; the capability area and right of the read, which the yaml does not declare, owner security architect, tracked as NEW-GAP-S5-15.

### 4. Flow

1. rwb-comms calls `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30` once per business date, after the WIN file window, as the service identity of rwb-comms; one hop, 2 s budget, one GET retry with jitter and a breaker (DP-11).
2. `SectionBGuard` reads the flag `rwb.dataengine.pod-read`: closed, the read answers 200 with `businessDate` as requested, `productCode` DP07, `rows` empty and `freshness` with status STALE and `businessDate` null, and reads no view (RD-P1-043; AC5, X3). The published answer has no member for the reason SECTION_B_NOT_DEPLOYED (ASM-0821); Pending, owner contract owner, GAP-0579.
3. `WinBatchGate` reads `v_ace_batch_status` for source WIN and the requested business date. The row is unique on `(source_system, business_date)` with `source_system` = 'WIN'; complete means `is_complete` = true, which is status COMPLETED. When the row is absent or not complete, no `v_ace_pod` row of that date is read, nothing of an earlier date is served in its place, and the answer is 200 with `rows` empty and the DP07 stamp in use, STALE once RWB-P1-E1015-APP has marked it (AC2, X1, X2).
4. `ProofOfDeliveryRepository` reads `v_ace_pod` for that business date. A Section B view carries `source_system` and `data_as_of` from the Tier 2 `business_date`, so the filter is the business date and `data_as_of` travels on the row as the age of the fact (TSD P1 T3.3).
5. The rows are mapped to `podKey`, `accountKey`, `noticeRef`, `sentDate`, `barcode`, `callbackDate`, `deliveryStatus`, `sentType`, `sourceSystem` and `dataAsOf` and returned in ascending `podKey` order; the two dates are the view's date columns, returned unchanged including null, with no conversion (AC1, AC6, AC11). Every `deliveryStatus` is returned; which status writes a delivery entry is rwb-comms' rule.
6. Nothing is matched and nothing is resolved: a `notice_ref` that names no notice is returned like any other row, because the notice is rwb-comms' and the unknown-reference hold and the barcode break are rwb-comms' behaviour (RWB-P6-E1055-APP). Pending: the published read of held proof-of-delivery rows, tracked as NEW-GAP-F03-1.
7. The read returns the view rows and DP07 freshness stamp only. It does not receive a case identifier, match rows to a case, or call the interaction ledger.
8. rwb-comms matches returned rows and is the only appender of delivery entries, using `POST /cases/{caseId}/interactions` after matching (RD-P1-007). Repeated DP07 delivery facts are counted by metric `rwb_source_data_win_delivery_repeat_total` (RD-P1-041); P1 does not update `duplicate_count`.
9. The answer is `{businessDate, productCode, freshness, rows}`; `freshness` is the `DataProductFreshness` of DP07 in use (`status`, `businessDate`, `sourceExtractedAt`, `loadedAt`), because every source-data answer states the age of what it carries (TSD P1 T3.7 Display). DP07 is fed by LIT and WIN, so a complete WIN date can be answered with rows while the stamp is STALE for a late LIT (RD-P1-041; AC15).
10. A view or database failure answers 503 with MSG-GEN-006 and presents no partial answer. This read has no ledger write that could fail (X6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The WIN batch for the business date is not COMPLETED in `v_ace_batch_status` | 200 with no row; no `v_ace_pod` row of that date is read; no earlier date is served in its place; the DP07 stamp in use is passed through | MSG-P1-001, shown by the consumer for a STALE stamp | AC2 |
| X2 | The WIN batch for the business date is FAILED at its record count check | As X1; the latest DP07 stamp in use remains the one written by RWB-P1-E1015-APP and is returned with status STALE | MSG-P1-001 | AC2 |
| X3 | `v_ace_pod` or `v_ace_batch_status` does not exist yet, or the flag is closed | No row is invented and no date is guessed: 200 with no row and DP07 STALE with a null date | MSG-P1-001, shown by the consumer | AC5 |
| X4 | The same `v_ace_pod` row is read twice | The same source row is returned; P1 writes no ledger entry or freshness stamp; the DP07 repeat metric is used under RD-P1-041 | Pending metric details (GAP-0580) | AC4 |
| X5 | A row names a notice reference that resolves to no notice | The row is returned unchanged; the read neither holds nor drops it; the check and the hold are rwb-comms' | None | AC14 (the check is RWB-P6-E1055-APP) |
| X6 | A required view or the database does not answer | 503 with the platform problem envelope; no partial answer; no entry or stamp is written | MSG-GEN-006 | AC7 |
| X7 | `businessDate` is missing (422) or cannot be read as a date (400) | Problem with `field` businessDate; nothing is read | MSG-GEN-001 | AC10 |
| X8 | No valid token, or a caller without the read right | 401 or 403; no row | MSG-P4-001, MSG-P4-002 | AC9 |

X1 and X2 are the source-read exception paths. X4 is a repeated read; P1 makes no ledger or stamp write and DP07 delivery repeats use the metric ruled by RD-P1-041. X3 is the Section B unavailable path. X5 and X6 remain with the read boundary; row-to-notice matching and unknown-reference handling are rwb-comms behavior.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency: two views, one freshness stamp and the operation published in `rwb-source-data.yaml` 5.1.0 |
| Negotiable | The class split is the squad's choice behind the contract; the ten fields, the envelope and the gate are fixed; paging is Pending (GAP-0577) |
| Valuable | One read-only door to ACE proof of delivery, stated with its age |
| Estimable | One read controller, gate and repository, plus a provider fake and read metrics |
| Small | Fits one sprint with its tests, as the source slice of the legacy key |
| Testable | Every criterion is one read against `v_ace_pod`, `v_ace_batch_status` and DP07 freshness fixtures |

### 7. Acceptance criteria

```gherkin
Feature: Read proof of delivery from WIN

  Scenario: AC1 Read a completed WIN business date
    Given the WIN row for business date 2026-11-30 has status COMPLETED and is_complete true
    And v_ace_pod holds POD-0002 and POD-0001 for that date and one row of 2026-11-25
    When rwb-comms calls GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30
    Then the answer is 200 with businessDate "2026-11-30", productCode "DP07", the DP07 freshness and rows POD-0001 then POD-0002 only
    And rwb-source-data writes no delivery entry, freshness stamp, outbox row or decision record
    TC: TC-P1-E1055-APP-01; TC-E1-055-13

  Scenario: AC2 Do not serve rows for a WIN date that is not complete
    Given the WIN row for 2026-11-30 is FAILED, not COMPLETED, or absent
    And the DP07 stamp in use is business date 2026-11-27, marked STALE by RWB-P1-E1015-APP
    When rwb-comms reads businessDate=2026-11-30
    Then the answer is 200 with rows empty and no row of 2026-11-30 or an earlier date
    And freshness holds status "STALE" and businessDate "2026-11-27"
    And rwb-source-data does not change the stamp
    TC: TC-E1-055-05; TC-E1-055-11

  Scenario: AC3 Return delivery facts without appending them
    Given v_ace_pod holds a row of 2026-11-30 with delivery_status "DELIVERED", barcode "RR123456789TH", notice_ref "N-0001" and callback_date 2026-11-28
    When rwb-comms reads that business date
    Then the row is returned with deliveryStatus "DELIVERED" and callbackDate "2026-11-28"
    And this story does not call InteractionLedgerWriter and the count of interaction rows is unchanged
    TC: TC-P1-E1055-APP-02; TC-E1-055-20

  Scenario: AC4 A repeated read remains read only
    Given rwb-comms has already read the row with pod_key POD-0001
    When rwb-comms reads the same business date again
    Then the read returns the same source row
    And rwb-source-data does not create or change an interaction entry or duplicate_count
    And DP07 delivery repeats are counted by metric rwb_source_data_win_delivery_repeat_total under RD-P1-041
    And the metric trigger and labels remain Pending, owner data architect, tracked as GAP-0580
    TC: TC-E1-055-07; TC-E1-055-10

  Scenario: AC5 The Section B views are not available
    Given rwb.dataengine.pod-read is closed and the schema holds no v_ace_pod view
    When rwb-comms reads businessDate=2026-11-30
    Then the answer is 200 with businessDate "2026-11-30", productCode "DP07" and rows empty
    And freshness holds status "STALE" and businessDate null
    And no view is read, no ACE fallback or earlier date is used and nothing is written
    TC: TC-E1-055-05; TC-P1-E1055-APP-03

  Scenario: AC6 Return only the ten published view fields
    Given a completed WIN batch and a v_ace_pod row
    When the proof-of-delivery read succeeds
    Then each row has only the members podKey, accountKey, noticeRef, sentDate, barcode, callbackDate, deliveryStatus, sentType, sourceSystem and dataAsOf
    And the answer has the members businessDate, productCode "DP07", freshness and rows
    And the body validates against ProofOfDeliveryAnswer of rwb-source-data.yaml 5.1.0
    TC: TC-E1-055-14

  Scenario: AC7 A read dependency fails
    Given v_ace_pod, v_ace_batch_status, or the database does not answer
    When rwb-comms reads a business date
    Then the response is 503 application/problem+json with messageCode MSG-GEN-006 naming the failed source, and no rows
    And no interaction entry or freshness stamp is written
    TC: TC-E1-055-15

  Scenario: AC8 Keep the read within the source-data boundary
    Given the service handles a proof-of-delivery request
    When its database access is inspected
    Then it reads recovery.v_ace_pod, recovery.v_ace_batch_status and the DP07 freshness stamp only
    And it opens no WIN connection and writes no interaction or data_product_load row
    TC: TC-P1-E1055-APP-04; TC-E1-055-18

  Scenario: AC9 Reject an unauthorised read
    Given a request with no valid token, and one from a workload identity other than rwb-comms
    When GET /api/recovery/source-data/v1/proof-of-delivery is called
    Then the first answers 401 with MSG-P4-001 and the second 403 with MSG-P4-002
    And no row is returned and no write occurs
    TC: TC-P1-E1055-APP-05; TC-E1-055-19

  Scenario: AC10 Validate the businessDate parameter
    Given one request without businessDate and one with businessDate "30-11-2026"
    When the proof-of-delivery read is called
    Then the first answers 422 and the second 400, each with MSG-GEN-001 and field "businessDate"
    And no view is read and no write occurs
    TC: TC-P1-E1055-APP-06

  Scenario: AC11 Preserve source dates and nulls
    Given a v_ace_pod row with sent_date, callback_date and notice_ref null
    When the proof-of-delivery read succeeds
    Then sentDate, callbackDate and noticeRef are null in that row
    And no date is substituted or converted by this story
    TC: TC-P1-E1055-APP-07

  Scenario: AC12 Do not log delivery identifiers
    Given a proof-of-delivery response contains pod_key, account_key, notice_ref or barcode
    When application logs and metrics are inspected
    Then those identifiers are absent from logs and metric labels
    TC: TC-P1-E1055-APP-08

  Scenario: AC13 Return every row of the date once without changing source data
    Given the completed WIN date has 30 v_ace_pod rows
    When rwb-comms reads the date (page parameters and paging shape are Pending, GAP-0577)
    Then every podKey is returned once in ascending order
    And no read changes interaction or data_product_load
    TC: TC-P1-E1055-APP-09

  Scenario: AC14 Return every status and an unknown notice reference unchanged
    Given rows of 2026-11-30 with delivery_status DELIVERED, REFUSED, UNDELIVERABLE and PENDING, one of them with notice_ref "N-9999" that names no notice
    When rwb-comms reads that business date
    Then all four rows are returned with their stored deliveryStatus and noticeRef
    And none is dropped, held or changed by this service
    TC: TC-P1-E1055-APP-10

  Scenario: AC15 A complete WIN date with a late LIT source
    Given the WIN row of 2026-11-30 is COMPLETED, the LIT row is not, and the DP07 stamp in use is 2026-11-27 with status STALE
    When rwb-comms reads businessDate=2026-11-30
    Then the rows of 2026-11-30 are returned
    And freshness holds status "STALE" and businessDate "2026-11-27"
    TC: TC-E1-055-17; TC-P1-E1055-APP-11
```

**Target reading.** The GET operation reads `recovery.v_ace_pod` only after the WIN row in `recovery.v_ace_batch_status` is COMPLETED and `is_complete` is true. It returns the ten view fields and the DP07 freshness stamp. The latest DP07 stamp in use is passed through; this story does not mark it STALE or write it. AC1 to AC13 keep the IDs that Test Cases v9 maps. rwb-comms matches the rows to cases and is the only writer-caller for delivery entries, appending over REST after matching (RD-P1-007; RD-P1-041; X-19; X-20). The metric `rwb_source_data_win_delivery_repeat_total` counts DP07 delivery repeats; its trigger and labels remain Pending under GAP-0580. P1 reads ACE only through Section B views and writes neither the interaction ledger nor the freshness table.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A `v_ace_pod` row is read only when the ACE batch for source WIN is COMPLETED for its business date | Legacy RWB-E1-055 BR4; ACE batch record; INT-15 error handling |
| BR2 | The proof of delivery is read from ACE through `recovery.v_ace_pod`; the Workbench writes no WIN delivery fact and opens no WIN connection | REQ-DRI-006; D-RCV-35 U1; FSD P1 A2.1 BR-P1-001-2 |
| BR3 | Freshness is read from `v_ace_batch_status` only and never inferred from `data_as_of`, a row count or a file | FSD P1 A2.14 BR-P1-014-2 |
| BR4 | A product fed by more than one source carries the oldest business date among its sources and is STALE while any of them is late; DP07 is fed by LIT and WIN | FSD P1 A2.14 BR-P1-014-3; FSD P1 A2.2 DP07 row |
| BR5 | A notice period starts only from the delivery date on the proof of delivery, so the delivery date is carried unchanged and never derived | CTL-15; R-LIT-07; legacy BR2 |
| BR6 | This story is read only; rwb-comms appends delivery entries after matching, and DP07 repeats use `rwb_source_data_win_delivery_repeat_total` | RD-P1-007; RD-P1-041; X-19; X-20 |
| BR7 | DP07 is STALE when no stamp exists for the expected business date at its expected time, as RWB-P1-E1015-APP sets it | RD-P1-041; MSG-P1-001; legacy BR7 |
| BR8 | rwb-source-data owns the ledger, but only rwb-comms appends delivery entries over REST; this story only reads proof-of-delivery facts | RD-P1-007; X-20 |

**Where each rule lives in the target.** BR1 and BR3 remain read behavior: the WIN completeness gate controls whether rows are returned, and RWB-P1-E1015-APP owns the freshness stamp. BR2 is the schema boundary: P1 reads ACE only through the Section B views and has no privilege on `public`. BR4 passes through the DP07 stamp without changing it. BR5 preserves the callback date as a source field without deriving an interaction timestamp. BR6 and BR8 follow RD-P1-007: this story only reads, and rwb-comms alone appends delivery entries over REST after matching. DP07 delivery repeats use `rwb_source_data_win_delivery_repeat_total` under RD-P1-041; trigger and labels remain Pending under GAP-0580.

### 9. State transitions

This story changes no notice state or delivery entry. It reads the source row and freshness stamp only; rwb-comms owns matching and appending.

| From | Event | Condition | To |
|---|---|---|---|
| DP07 stamp in use, any status | `GET /proof-of-delivery` | WIN complete for the date | Unchanged; rows returned |
| DP07 stamp in use, any status | `GET /proof-of-delivery` | WIN row late, failed or absent | Unchanged; no row returned |
| Flag `rwb.dataengine.pod-read` closed | Flag opened after RWB-ACE-001 | `v_ace_pod` deployed | The read serves rows |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The service identity of rwb-comms | The only caller the contract names: DP07 rows for one business date; no case identifier is sent |
| The service identity of rwb-asset | Not a caller (RD-P1-064) |
| RW-LITOFF, litigation officer | Reads the delivery date, the barcode and the delivery status on the notice panel of rwb-comms; calls nothing of this service directly (Litigation R) |
| RW-CASEOWN, case owner | Reads the delivery on the case record view; calls nothing of this service directly (Litigation R) |
| RW-DATASTEW, data steward and data product owner | Reads the DP07 freshness stamp, the stale flag and the repeat count |
| RW-PLATADM, platform administrator | Opens and closes the flag of the read and reads the series of the deployment |
| rwb-source-data | Runs as its own login, holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on any ACE table (DP-02; Architecture v5 slides 11 and 29) |
| rwb-comms (P6) | Owns the notice, the row-to-notice matching, the unknown-reference hold, the two events and the displayed message; answers the case of the delivery it names (C RWB-P6-E1055-CON) |

The read carries the rwb-comms workload identity token. It calls the rwb-access authorise check for the proof-of-delivery read right before returning rows; the capability area and right are Pending (NEW-GAP-S5-15). It takes no case identifier, so no case scope applies and no 404 is answered. Missing or invalid credentials answer 401 (MSG-P4-001); a caller without the read right answers 403 (MSG-P4-002); an unavailable authorise check answers 503 (MSG-GEN-006).

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
| DF-INT-002 | interaction | case_id | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-004 | interaction | occurred_at | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-005 | interaction | channel | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-006 | interaction | direction | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-011 | interaction | summary | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-014 | interaction | event_code | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-018 | interaction | idempotency_key | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-INT-019 | interaction | case_seq | Not accessed by this story; rwb-comms is the only delivery-entry appender (RD-P1-007) |
| DF-OPS-007 | data_product_load | status | Read (the DP07 stamp the answer states) |

Field IDs are those in the Logical Data Model and Data Dictionary.

**Which side is this story's.** `DF-ACE-251` to `DF-ACE-260` are read through `v_ace_pod`; `DF-ACE-178` to `DF-ACE-186` are read through `v_ace_batch_status`. These view fields are treated as personal or customer data under the Data Classification and Personal Data Inventory; they are not written by this story, must not appear in logs or metric labels, and are masked in UAT data. The wire types are those of `ProofOfDeliveryRow`: `podKey` string up to 255 (required), `accountKey` up to 255, `noticeRef` up to 60, `barcode` up to 40, `deliveryStatus` up to 15, `sentType` up to 10, `sourceSystem` up to 20, and `sentDate`, `callbackDate`, `dataAsOf` as dates; all but `podKey` may be null or absent. The dictionary type integer of DF-ACE-251 to DF-ACE-260 does not match and is raised for correction. This story reads the DP07 stamp through RWB-P1-E1015-APP and writes neither `interaction` nor `data_product_load`. rwb-comms appends delivery entries under RD-P1-007.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1` (DP-13). One operation, the proof-of-delivery read of the DP07 product.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proof-of-delivery?businessDate=` | Reads proof-of-delivery rows for one business date from `v_ace_pod`, ordered by `pod_key`, only when the WIN row in `v_ace_batch_status` has status COMPLETED and `is_complete=true`; returns rows and the DP07 freshness stamp; performs no write | rwb-comms workload identity with the published read right; one hop, 2 s budget | Read only; repeated reads do not append entries or change the freshness stamp |

The operation is `getProofOfDelivery` in `rwb-source-data.yaml` 5.1.0. Its answer `ProofOfDeliveryAnswer` has `businessDate`, `productCode` (`DP07`), `freshness` (`DataProductFreshness`) and `rows`; each `ProofOfDeliveryRow` has `podKey`, `accountKey`, `noticeRef`, `sentDate`, `barcode`, `callbackDate`, `deliveryStatus`, `sentType`, `sourceSystem` and `dataAsOf`. Errors are 400 for an unreadable `businessDate` and 422 for a missing one (MSG-GEN-001), 401 (MSG-P4-001), 403 (MSG-P4-002) and 503 when a required view, the database or the authorise check does not answer (MSG-GEN-006). Pending: page parameter names, defaults, maximum and response paging shape, owner data architect, tracked GAP-0577. The endpoint has no caseId parameter.

This story does not call the interaction append operation. After matching a returned row to a case, rwb-comms appends over REST to `POST /cases/{caseId}/interactions` with the shared P1 contract (RD-P1-007), one entry per matched row with `externalRef` = `barcode`, else `noticeRef`; a row with neither is not matched, and proof recorded by hand also writes its entry through rwb-comms (RD-P1-064).

Until RWB-ACE-001 lands and `v_ace_pod` is available, the read stays behind its feature flag and answers as AC5. The fallback is proof entered by hand against the barcode, to be agreed with the litigation business owner before wave 2 (GAP-1608). The WIN dispatch file layout is a versioned interface definition owned by rwb-integration and is held as a contract item before wave 2; the dispatch is built against a fake of that definition until the layout is agreed with the WIN owner (GAP-1602).

#### 12.2 REST operations consumed

rwb-access authorise check, 2 s, before rows are returned. rwb-comms calls this read using its workload identity. This story calls no rwb-comms, rwb-case or ledger operation; it reads ACE only through the Section B views and reads the DP07 freshness stamp through RWB-P1-E1015-APP. It does not read another service's table or write a foreign key (DP-01).

#### 12.3 Events published

None. The topic `rwb.source-data.events.v1` and its `AceDataReady` and `AceDataLate` events belong to RWB-P1-E1015-APP. This story publishes no event and writes no outbox row. `rwb.comms.NoticeDelivered.v1` is published by RWB-P6-E1055-APP (DP-09).

#### 12.4 Events consumed

None. No event starts this read: rwb-comms calls it after the WIN file window, and Architecture v5 slide 15 gives this service no consumed event. `AceDataReady` and `AceDataLate` are on this service's producing side, and the batch completeness the gate needs is read from `v_ace_batch_status` and not waited for as a message.

#### 12.5 Workflows and activities

None. The read is a synchronous, read-only step. The task queue of this service is `rwb-source-data` in namespace `rwb-recovery`; this story registers no workflow, activity or Schedule.

#### 12.6 Schedules

None. The 06:00 daily read of the legacy story (`v_ace_pod` read path, RWB-E1-055 section 12) is not a Schedule of this story. In the target the pod read is started by the slice that owns the run: the DP07 cut-off Schedule of RWB-P1-E1015-APP marks the product and the pod step of RWB-P6-E1055-APP calls this read after the WIN file window; this operation answers on demand and holds no state, so no Temporal Schedule is registered here and DP-10 applies as a statement only — no Quartz trigger and no row of a shared job table survives the move (Architecture v5 slide 44).

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_pod` | `recovery` | ACE team (Tier 2 Section B view over ACE `pod_receipt`); SELECT to `rwb_source_data` only | Read only, the ten fields of AC6; a view and not a table, and the table behind it is ACE's and outside the 19 schemas; it exists only after RWB-ACE-001 |
| `v_ace_batch_status` | `recovery` | ACE team (Tier 2 Section B view over ACE `ace_batch_run`); SELECT to `rwb_source_data` only | Read only: `source_system`, `business_date`, `status` and `is_complete`, the gate of AC2 |
| `interaction` | `rwb_source_data` | P1 rwb-source-data (Ownership Map) | Not read or written by this story; rwb-comms appends delivery entries under RD-P1-007 |
| `data_product_load` | `rwb_source_data` | P1 rwb-source-data (Ownership Map) | DP07 freshness stamp read only; RWB-P1-E1015-APP owns all writes, including `duplicate_count` |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_source_data` | PLT library objects, created in this service's schema | Not read or written by this story |

`v_ace_pod` and `v_ace_batch_status` are views, not tables. ACE owns `pod_receipt` and `ace_batch_run`; P1 reads only the published views. This story does not read the notice or case and does not write `interaction`, `data_product_load`, or a foreign key. rwb-comms owns the match and delivery-entry append (DP-01, DP-05; RD-P1-007).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data provider fake, version 5.1.0 | `getProofOfDelivery` in `rwb-source-data.yaml` 5.1.0 | Completed, failed and absent WIN batch answers; rows of all four statuses; DP07 freshness pass-through; flag-closed answer; 400, 401, 403, 422 and 503 |
| View fixture | `recovery.v_ace_pod` and `recovery.v_ace_batch_status` in a container | One pod row of 2026-11-30 with `RR123456789TH`, notice `N-0001` and callback date 2026-11-28; a second row of 2026-11-25; batch rows for WIN COMPLETED, FAILED at its record count check and absent; LIT not COMPLETED beside a complete WIN |
| Flag-closed fixture | The service with `rwb.dataengine.pod-read` closed | The AC5 answer, with no view present in the schema |
| rwb-access authorise fake | The read right | Allow, refuse, timeout |

No WIN connection is opened and no production payload is copied into a fake: the pod values are the legacy synthetic values of RWB-E1-055.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 read operation on `/api/recovery/source-data/v1` | rwb-access authorise | One hop, 2 s budget for rwb-comms; no ledger append or freshness write occurs here (DP-11) |
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
| DP-09 | Application event, EV-nn, outbox | Not used: the read publishes nothing | none |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Not used: this story adds no migration | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**How each pattern applies here.**

- **DP-01.** P1 reads ACE data only through `v_ace_*` Section B views. This story reads `v_ace_pod`, `v_ace_batch_status` and the freshness stamp; it writes no ledger or stamp row.
- **DP-05.** This is one of the two views DP-05 is about: `v_ace_pod` is read here and nowhere else in the Workbench, and `v_ace_batch_status` beside it. The read is the service's own `v_ace_*` read, which is why the pattern adds no dependency; the published read exists so that no other service needs the grant.
- **DP-07.** Product code and freshness status are read from the catalog and stamp. rwb-comms supplies ledger values when it appends after matching. DP07 delivery repeats use `rwb_source_data_win_delivery_repeat_total` under RD-P1-041; details remain Pending under GAP-0580.
- **DP-09.** This story publishes no event and writes no outbox row. The delivery append is rwb-comms' REST operation under RD-P1-007.
- **DP-10.** Applies as a statement: the 06:00 job of the legacy story is gone with Quartz, and no Schedule, no workflow and no activity of this read is registered here (12.6). The cut-off that decides when the pod read may run is RWB-P1-E1015-APP's Schedule and the run itself is rwb-comms'.
- **DP-11.** Applies from the caller's side: the read is a REST contract with one hop and a 2 s budget; its one call out is the rwb-access authorise check. Its 503 answers carry the platform problem envelope so that a caller's breaker sees a plain failure.
- **DP-15.** This story adds no migration, table, column or index; all interaction appends are owned by rwb-comms under RD-P1-007.
- **DP-18.** rwb-source-data owns the interaction ledger. This story only reads proof-of-delivery data; rwb-comms is the only appender of delivery entries over REST (RD-P1-007; X-20).
- **DP-19.** Applies as a statement for the person: the litigation officer and the case owner see the delivery on the notice panel and the case record view, which arrive through the gateway-bff composite route, and never call this operation. The only caller of this operation is a service identity.

The platform H rows of the pattern table are delivered by the wave-0 platform. The contract is `rwb-source-data.yaml` 5.1.0 (API Specification v7); the provider fake for this read is published with it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ProofOfDeliveryController` | Controller | The operation of 12.1 on `/api/recovery/source-data/v1`; parameter validation; RFC 9457 problem details |
| `SectionBGuard` | Guard | Reads the flag `rwb.dataengine.pod-read` and answers the ten fields as not available when the Section B views are not deployed (AC5) |
| `WinBatchGate` | Service | Reads `v_ace_batch_status` for `source_system` 'WIN' and the business date; returns no rows unless `is_complete=true` (status COMPLETED); passes through freshness from RWB-P1-E1015-APP (AC1, AC2) |
| `ProofOfDeliveryRepository` | Repository | Reads `v_ace_pod` for the business date in ascending `pod_key` order; no write method exists |
| `PodReceipt` | Record | Immutable mapping of the ten view fields |
| `ProofOfDeliveryPage` | Record | The answer: business date, product code, freshness stamp and rows |
| `DeliveryRepeatMetric` | Metric | Counts DP07 delivery repeats as `rwb_source_data_win_delivery_repeat_total` under RD-P1-041; trigger and labels are Pending under GAP-0580 |

**Migrations and sequence (DP-15).** This story adds no ledger index, column, table or migration. Delivery entries are appended by rwb-comms over REST and written by rwb-source-data's ledger writer (RD-P1-007). The metric `rwb_source_data_win_delivery_repeat_total` is telemetry; its trigger and labels remain Pending under GAP-0580.

**Database.** This story reads `v_ace_pod`, `v_ace_batch_status` and the DP07 freshness stamp only. It does not write `interaction`, `data_product_load`, or any library table. It reads ACE only through the two Section B views (DP-01, DP-05).

**Configuration and reference data**

- The flag `rwb.dataengine.pod-read` is a data row of the platform library and gates the read until RWB-ACE-001 lands (DL43; GAP-0579; ASM-0821).
- The product code `DP07` and the freshness status values come from the catalog and the stamp, not from the code; the product name rendered in MSG-P1-001 ("DP07 Legal") is the catalog value and the date is the last complete business date of the stamp (GAP-0581; ASM-0823).
- rwb-comms supplies ledger event, channel, direction and business-key values when it appends after matching (RD-P1-007); this story writes none of them.
- The 2 s budget and caller retry are edge configuration. Page parameters remain Pending, owner data architect, tracked as GAP-0577.
- DP07 delivery repeats use metric `rwb_source_data_win_delivery_repeat_total` (RD-P1-041); trigger and labels remain Pending under GAP-0580.

**Build steps**

1. The read operation on the base, with the parameter validation of X7 and the problem envelope of 12.1.
2. `SectionBGuard` and the "not available" answer, with the flag fixture of 12.8 (AC5).
3. `WinBatchGate`: the batch row of source WIN and the business date, the FAILED path, the absent row and the no-earlier-date rule (AC2).
4. `ProofOfDeliveryRepository` and the ten-field mapping, passing published dates and null values unchanged (AC1, AC6).
5. The ordering of the rows and the answer envelope; paging waits for GAP-0577.
6. Verify the read-only boundary: no ledger append, freshness write, or migration is part of this story.
7. Expose `rwb_source_data_win_delivery_repeat_total` for DP07 delivery repeats under RD-P1-041; keep the trigger and labels Pending under GAP-0580.
8. Test the published read contract against the provider fake and synthetic view fixtures.
9. Add changed and new AC coverage to Test Cases v9 (W2-tests).

**Feature flag.** `rwb.dataengine.pod-read`, default off. Off, the read answers 200 with no row and DP07 STALE with a null date, and writes nothing (RD-P1-043).

**Done when.** Changed acceptance criteria and new cases have entries in Test Cases v9 (W2-tests); the read returns the ten fields for a COMPLETED WIN business date, passes through the latest DP07 freshness stamp, returns no rows for a failed or absent batch, answers as AC5 while flagged off, and performs no ledger or freshness writes.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The DP07 stamp passed through has status STALE; shown by the consumer, not a member of the answer | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A view, the database or the authorise check does not answer (503) | {system} is not available. Try again in a few minutes. |
| MSG-GEN-001 | `businessDate` missing (422) or unreadable (400) | Enter {field}. |
| MSG-P4-001 | No valid token (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | The caller lacks the read right (403) | You cannot {action} here. Your role does not include it. |

Texts are those of Error and Message Standard v6. The product and date of MSG-P1-001 come from the catalog and the DP07 stamp; the rendering, including a null date, is Pending under GAP-0581. This story does not emit MSG-P1-022 or call an interaction writer. Thai text follows DL10.

### 15. Screens and states

No screen in this story. The litigation officer and the case owner see the delivery date, the barcode and the delivery status on the notice panel and on SCR-03 Case record, both served by rwb-comms and reached through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and the data steward sees the DP07 freshness stamp, the stale flag and the repeat count on SCR-45 Data quality (RWB-P1-E1015-APP). This operation has no screen: it is called by a service. When the read answers "not available" or no row, the notice panel shows MSG-P1-001 with the age of the product, and the delivery state of the notice is left as it was; this story renders none of it. The states of SCR-03 Case record are loading, as Screen Specifications v1 section SCR-03 gives them; empty, error and no access: Not specified in the source documents (CG-ALL-2230). The states of SCR-45 Data quality are loading, as Screen Specifications v1 section SCR-45 gives them; empty, error and no access: Not specified in the source documents (CG-ALL-2231).

### 16. Test cases

| TC ID | Covers | Level |
|---|---|---|
| TC-E1-055-05 | AC2, AC5 | Component |
| TC-E1-055-07 | AC4, AC7 | Component |
| TC-E1-055-10 | AC4 | Component |
| TC-E1-055-11 | AC2 | Component |
| TC-E1-055-14 | AC6 | Component |
| TC-E1-055-15 | AC7 | Component |
| TC-E1-055-16 | BR2, BR8: schema boundary and one ledger | Component |
| TC-E1-055-17 | BR4, BR5, AC15 | Component |
| TC-E1-055-13 | AC1 | Contract |
| TC-E1-055-18 | AC8 | Component |
| TC-E1-055-19 | AC9 | Contract |
| TC-E1-055-20 | AC3 | Component |
| TC-P1-E1055-APP-01 | AC1 | Component |
| TC-P1-E1055-APP-02 | AC3 | Component |
| TC-P1-E1055-APP-03 | AC5 | Component |
| TC-P1-E1055-APP-04 | AC8 | Component |
| TC-P1-E1055-APP-05 | AC9 | Component |
| TC-P1-E1055-APP-06 | AC10 | Component |
| TC-P1-E1055-APP-07 | AC11 | Component |
| TC-P1-E1055-APP-08 | AC12 | Component |
| TC-P1-E1055-APP-09 | AC13 | Component |
| TC-P1-E1055-APP-10 | AC14 | Component |
| TC-P1-E1055-APP-11 | AC15 | Component |

TC-E1-055-01 to -04, -06, -08, -09 and -12 are legacy regression evidence of the rwb-comms, rwb-case, rwb-document and integration slices; they are not part of Done when for this story.

### 17. Guardrails

- No business value in code: the product code, the product name, the freshness status values, the `LETTER` event code and the channel come from the catalog, the stamp and the lists; the page size, the retry, the 2 s budget and the flag are configuration.
- The view fields include indirect identifiers and customer data. Do not put pod_key, account_key, notice_ref, barcode or other row values in logs or metric labels; mask synthetic UAT data per the Data Classification and Personal Data Inventory.
- No read of another service's tables and no `public.*` read: ACE data is reached only through the 30 `recovery.v_ace_*` views, which is why this read exists at all (DP-01, DP-05; FSD P1 A2.1 BR-P1-001-2).
- No WIN connection and no file: INT-14 and INT-15 are rwb-integration's and ACE's, and this service opens neither (REQ-DRI-006; legacy guardrail 4).
- Read only: this story writes no delivery entry. rwb-comms is the only appender of delivery entries over REST (RD-P1-007; X-20).
- No invented date and no earlier date: a date whose WIN batch is not COMPLETED answers no row, and a Section B view that is not there answers "not available" — never an empty list that reads as "no delivery" and never a fallback to `data_as_of` (BR3; DL43).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).
- The platform library objects stay the library's: `outbox_event`, `processed_event` and `idempotency_key` are created in this schema and are never redefined by this story (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post; proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07 | Test Cases v9 (W2-tests) |
| REQ-DRI-006 | Source data is read through read-only views | Business Requirements Program, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | CTL-15 | Test Cases v9 (W2-tests) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P6-E1055-CON | Contract | Consumer contract of this read; it follows `rwb-source-data.yaml` 5.1.0; no operation of rwb-comms is called |
| RWB-P1-E1066-APP | App development | Same-service sibling: owns the interaction ledger contract; this story does not call its append operation |
| RWB-P1-E1015-APP | App development | Same-service sibling: owns all DP07 freshness stamp writes; this story reads the stamp only |
| RWB-P6-E1055-APP | App development | Consumer of this read: the WIN file, the acknowledgment, the row-to-notice matching, the unknown-reference hold, the two events and the displayed message |
| RWB-P3-E1055-APP | App development | The notice state and the `NOTICE_PERIOD` timer started from the delivered date |
| RWB-P5-E1055-APP | App development | The stored letter behind a notice, read by rwb-comms |
| RWB-ITG-E1055-ITG | Integration | Proves the whole loop, AC1 and AC9 included, on the live services and the live ACE batch record |
| RWB-S5-E3022-APP | App development | Reads delivery state from the case ledger or rwb-comms, not from this read (RD-P1-064) |

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

### 20. Remaining delivery steps

- Size: Not specified; pending refinement. Owner: squad.
- Epic design sign-off: Pending. Owner: solution architect.
- CON Done: Pending. Owner: contract owner.
- Fake published: Pending. Owner: contract owner.
- Test data in DEV: Pending. Owner: QA.
- Page parameters and paging shape: Pending, GAP-0577. Owner: data architect.
- Member for the reason SECTION_B_NOT_DEPLOYED in the answer: Pending, GAP-0579. Owner: contract owner.
- Repeat metric trigger and labels: Pending, GAP-0580. Owner: data architect.
- MSG-P1-001 rendering: Pending, GAP-0581. Owner: product owner.
- Capability area and right of the read, and registration of the flag rwb.dataengine.pod-read: Pending, NEW-GAP-S5-15. Owner: security architect with the platform architect.
- Published read of held proof-of-delivery rows: Pending, NEW-GAP-F03-1. Owner: solution architect.
- Requirements matrix rows of REQ-DRI-006 and REQ-OCC-003: correction requested. Owner: QA.
