# RWB-ITG-AD019-ITG Data quality and reconciliation console

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-AD019-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP10, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-AD019-ITG-16) |
| Depends on (build) | RWB-P1-AD019-APP, RWB-P3-AD019-APP (both not done yet; also listed under Integration dependencies) |
| Contract dependencies | Provider CON stories of rwb-source-data and rwb-case that publish the reads of section 12.2; IDs not specified in the source documents (DOR-RWB-ITG-AD019-ITG-21) |
| Reference data | Parameters and lists read: Not specified in the source documents (DOR-RWB-ITG-AD019-ITG-20); reference-data contract (DP-06, DP-07): Not specified in the source documents (DOR-RWB-ITG-AD019-ITG-20) |
| Integration dependencies | RWB-P1-AD019-APP, RWB-P3-AD019-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-019 as the wave 4 integration proof of the data quality and reconciliation console, from the JOB-04 reconciliation break and the REC-05 referential orphan in rwb-source-data through the three console reads of rwb-case, the annotation of every break key with its case, queue and owner, and the stale product refreshed by the rwb-case Schedule, to the refused read and the run report; the console itself is RWB-P3-AD019-APP and the run and the freshness are RWB-P1-AD019-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-AD019-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 23 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that the data quality console shows the reconciliation break, the referential orphan and the stale data product exactly as rwb-source-data computes them, annotated with the case, queue and owner that rwb-case holds, in the same run and with no value recomputed on the way**, so that **a break, an orphan or a stale product is fixed before it reaches a decision**.

This story builds the harness and the evidence, and nothing else. rwb-source-data (P1) owns the JOB-04 reconciliation, the `reconciliation_result` table, the `data_product_load` table, the freshness read `GET /api/recovery/source-data/v1/data-products/freshness`, the reconciliation read and the business-key resolution read. rwb-case (P3) owns its three read operations on `/api/recovery/case/v1/data-quality/...`, the annotation of every break key with the case number, the queue and the owner held in `rwb_case`, and the `DataQualityFreshnessCheck` Temporal Schedule (DP-10). SCR-45 Data quality is the gateway-bff composite route that composes the three reads (DP-19). The harness drives those published operations, observes their answers and writes a run report; it builds no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

The P3 slice of this legacy key, RWB-P3-AD019-APP, is already written and is the I story behind the console. Its three operations are `GET /data-quality/reconciliation-breaks`, `GET /data-quality/referential-completeness` and `GET /data-quality/stale-products`, each read only, each one hop from the composite route, and each answering with the business date on every row. This story proves that composition against the owners.

### 2. Business rationale

The legacy story was written against a failure that has not gone away: the reconciliation result is seen only by the team that runs the job, and a product that is a day behind reaches a route decision before anyone notices. Under D-RCV-35 the Workbench loads no source data, so the reconciliation of the case list to ACE is the JOB-04 step of rwb-source-data and the console only shows its result; the console cannot repair the break any more than the job can. That is exactly why the wiring has to be proved once, end to end, rather than assumed from two service stories that each pass on their own stubs. Legacy AC1 and AC2 are copied verbatim in section 7 and stay the business facts: 2,903 SSME accounts at 90 days past due or more less the exclusions against a case list of 2,891, a REC-01 break with variance 12 and 0.41 percent, and a `case_party` row on case "RW-2026-000140" whose `person_key` "P0099881" has no row in `v_ace_customer`. What this story adds is the proof of the composition: that the break, the orphan and the stale product arrive on the console exactly as the owner computed them, and that no number is recomputed anywhere on the way.

The decoupling is what makes the console cheap to change and hard to get wrong. The ACE rows, the reconciliation result and the freshness arrive only through the rwb-source-data contract and never through a view read by the consumer (DP-05, ADR-010), so the twelve account keys, their days past due and the last complete ACE business date are the owner's values and not the screen's. The stale set is refreshed by a Temporal Schedule in rwb-case through the workflow kit (DP-10), which is the replacement for the JOB-05-era polling of a shared job table, and the Schedules belong to each service (Architecture v5 slide 44). The screen is a gateway-bff composite route, not a page that calls four services (DP-19). Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget and no call chain (ADR-020).

The second half of the rationale is the part only an integration proof can carry. Variance 12 and 0.41 percent are correct only if they are the numbers the P1 run wrote; a screen that divides one count by another arrives at a different figure the moment a rounding rule changes, and a screen that counts its own annotations reports a break that is really an annotation gap. The same is true of the orphan: a key is unresolved only because the owner's key resolution says so, not because the console could not find a row in a table it is not allowed to read. The harness holds the ACE row set, the case set and the stale set in the fixture as data, asserts the legacy values are unchanged, and compares every displayed value with the owner's own answer. Under D-RCV-60 the placement, the login, the route and the read shapes are recorded as GAP-0441 with ASM-0633.

### 3. Preconditions

- RWB-P1-AD019-APP and RWB-P3-AD019-APP are the I stories of this legacy key, and each has a stub generated from its published contract from Day 1; a stub pass is reported as a stub pass and never as a real pass.
- The rwb-source-data contract is published with `GET /api/recovery/source-data/v1/data-products/freshness` behind the base `/api/recovery/source-data/v1` (Ownership Map row `GET /data-products/freshness`, Architecture v5 slide 15), plus the reconciliation read that answers the REC-01 to REC-05 rows and the business-key resolution read that answers whether a `person_key` or an `account_key` resolves to a source row.
- The rwb-case service contract is published with the three console reads of RWB-P3-AD019-APP under `/api/recovery/case/v1`, each annotated from schema `rwb_case` and each returning the business date on every row.
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-45 and composes the three reads (DP-19). The exact route specification, its path, its merge rules and its per-call timeout ownership are Not specified in the source documents (GAP-0441; ASM-0633).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the Schedule template (overlap policy SKIP, catch-up window) and the typed activity contract that P3's Schedule is built on (DP-10). The two platform stories are the H dependencies of the pattern rows of section 13 and are not repeated in the metadata H field of this story, which stays None.
- The harness runs in SIT. It uses a synthetic ACE row set, a synthetic case set and a synthetic stale set; no production data, no real `person_key` and no real account key is used, and the run never touches UAT or production.
- The P1 reconciliation and key-resolution paths, their paging and their field shapes, the P3 console route specification and its merge rules, the freshness read's field shape and the refresh cadence are Not specified in the source documents (GAP-0441; ASM-0633).
- The caller of the console holds Platform administration R in rwb-access with scope All, and the read is recorded by rwb-access on its own contract.
- No build dependency. Day 1, with the stubs of section 12.8 in place from the first run; the two I stories replace their stubs as they land and never block this lane.

### 4. Flow

1. Harness: loads the fixture: business date `2027-06-30`, the synthetic row set that the rwb-source-data contract fake (section 12.8) answers, with 2,903 SSME accounts at 90 days past due or more less the exclusions, the synthetic case set with a case list of 2,891 and the twelve break keys it does and does not hold, case "RW-2026-000140" with `case_party` `person_key` "P0099881", and one data product past its expected business date. It reads the console once before the run and keeps that snapshot for the comparison.
2. Harness: reads the three console blocks for the business date through the P3 operations behind the gateway-bff route stub: `GET /api/recovery/case/v1/data-quality/reconciliation-breaks`, `GET /api/recovery/case/v1/data-quality/referential-completeness` and `GET /api/recovery/case/v1/data-quality/stale-products`.
3. Harness: asserts the break block carries source count 2,903, case list count 2,891, variance 12 and variance percent 0.41, exactly the values the P1 reconciliation stub answered, and that every row carries its business date.
4. Harness: compares the break block field for field with the raw answer of the P1 reconciliation read for the same date, and asserts no value differs and that no service read another service's table or an ACE view in the run (the DB user of each call is observed from the stub and the service log).
5. Harness: asserts the twelve account keys on the break, each annotated with the case number, the queue and the owner that `rwb_case` holds for that `account_key`, and each carrying its days past due as the P1 answer returned them.
6. Harness: asserts a break key that no case holds shows the key alone, with an empty case number, queue and owner, and that no zero, dash-as-zero or placeholder case is invented for it.
7. Harness: asserts the referential block names the orphan with its table `case_party`, its column `person_key` and its key "P0099881", and that the key is unresolved only because the P1 key-resolution stub answered that no `v_ace_customer` row exists.
8. Harness: re-reads the case and its `case_party` row through the P3 console and compares with the pre-run snapshot, and asserts the case and its `case_party` row are unchanged by the console.
9. Harness: asserts the stale block shows the data product past its expected business date with its last complete ACE business date, its status and MSG-P1-001, and shows no product with unknown freshness as fresh.
10. Harness: asserts the P3 Schedule refresh: `DataQualityFreshnessCheck` on the task queue `rwb-case` runs its `refreshStaleSet` activity, takes one freshness read per data product, replaces the stale set in the api and worker pods, and writes no table; it then restarts the pods and asserts the empty stale set shows the business date of its last refresh instead of a fresh console.
11. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller with role RW-OFF and no Platform administration R, then calls each of the three console reads, and asserts 403 with MSG-P4-002 at the gateway and at the owner, and that no block was rendered and no row was read.
12. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the three counts and the two variance figures observed, the twelve keys and their annotation, the orphan, the stale product and its last complete ACE business date, the Schedule run and its refresh date, the refused read, and the criterion verdicts.

Screen states of SCR-45 asserted in the run: empty (the stale block with an empty stale set shows its last refresh date, not a fresh console), loading (the Loading state of the composition), error (the per-block error state, with MSG-GEN-001 on a missing business date) and no access (403 with MSG-P4-002, no block rendered).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | The P1 reconciliation read does not answer inside the 2 s budget | The break block shows its own error state and the referential and stale blocks still show; the run fails AC3 on that hop and the report names the service, the operation, the contract version and the elapsed time. No message ID exists for an unreachable P1 read, so the harness asserts the problem response and never a text | None | TC-AD-019-01-ITG (AC3) | AC3 |
| X2 | No reconciliation result exists for the requested business date | The break block shows its empty sentence and the last business date that has a result; a break is never shown as zero and the run does not read the missing date as a pass | None | TC-AD-019-01-ITG (AC1) | AC1 |
| X3 | A business key on a case table has no source row | The orphan shows with its table, its column and its key, and the case and its `case_party` row are unchanged before and after the read | None | TC-AD-019-02-ITG (AC2) | AC2 |
| X4 | A data product is past its expected business date | The stale row shows its last complete ACE business date, its status and MSG-P1-001, and the run fails AC6 if the row is shown as fresh | MSG-P1-001 (expected) | TC-AD-019-03-ITG (AC6) | AC6 |
| X5 | The case list count does not reconcile to ACE for a product group | The REC-01 row shows as a break with variance 12 and variance percent 0.41 and carries MSG-P1-012, and the run fails AC1 if the figures differ from the P1 answer by any digit | MSG-P1-012 (expected) | TC-AD-019-01-ITG (AC1) | AC1 |
| X6 | A role without Platform administration R opens the console | The gateway refuses the composite call and the owner refuses the read, both with 403 and MSG-P4-002, and nothing shows; a 200 is a failure even when no data is returned | MSG-P4-002 (expected, and missing) | TC-AD-019-04-ITG (AC5) | AC5 |
| X7 | A break names an account key that no case holds | The row shows the key with an empty case, queue and owner, and the run fails AC4 if a placeholder case is invented | None | TC-AD-019-01-ITG (AC4) | AC4 |
| X8 | The freshness Schedule has not run since a restart | The stale block shows the business date of its last refresh and marks nothing as fresh; the run fails AC6 if any product is reported fresh without a P1 answer for the date | None | TC-AD-019-03-ITG (AC6) | AC6 |
| X9 | The business date parameter is missing or malformed | The call is refused before any read, at the owner and at the route, with MSG-GEN-001 naming the field | MSG-GEN-001 (expected) | TC-AD-019-04-ITG (AC5) | AC5 |
| X10 | The freshness read answers for a product with no complete ACE batch and no last complete date | The product is not shown as fresh; the run fails AC6 if it is, and the report names the product and the answer it read | None | TC-AD-019-03-ITG (AC6) | AC6 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values. An unreachable read has no message ID of its own, so it is asserted as a failed criterion and never as a message.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs of section 12.8 from Day 1; the only wait is RWB-P1-AD019-APP and RWB-P3-AD019-APP, and their stubs answer until they land |
| Negotiable | The fixture layout, the synthetic keys, the business date, the report shape, the refresh cadence and the pass or fail gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The break, the orphan and the stale product are proved to arrive on the console exactly as the owner computed them and annotated with the case that holds them, so a bad row is fixed before a decision uses it |
| Estimable | One runner, one stub set, three console probes, one schedule observer, one session probe and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against RWB-P1-AD019-APP and RWB-P3-AD019-APP as they land, and every displayed value is compared with the owner's own answer |

### 7. Acceptance criteria

```gherkin
Feature: Data quality and reconciliation console - wave 4 integration harness

  Scenario: AC1 A reconciliation break (legacy RWB-AD-019 AC1)
    Given the rwb-source-data contract fake (section 12.8) answers 2,903 SSME accounts at 90 days past due or more less the exclusions and the case list holds 2,891
    When the reconciliation workflow of rwb-source-data runs for the business date
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    And the 12 account keys are on the break list with their days past due from the rwb-source-data contract fake answer

  Scenario: AC2 Referential completeness (legacy RWB-AD-019 AC2)
    Given case_party on case "RW-2026-000140" carries person_key "P0099881" and the key-resolution read of the rwb-source-data contract fake (section 12.8) answers that no customer row exists for it
    When the REC-05 step runs
    Then the orphan shows with its table, its column and its key
    And the case and its case_party row are unchanged

  Scenario: AC3 The console composes the break and stale blocks from the owners in one hop each and recomputes nothing (new, D-RCV-60)
    Given the rwb-source-data stub answers REC-01 for SSME with source count 2,903, case list count 2,891, variance 12 and variance percent 0.41 for business date "2027-06-30"
    When the harness reads the break block and the stale block through GET /api/recovery/case/v1/data-quality/reconciliation-breaks and GET /api/recovery/case/v1/data-quality/stale-products
    Then every displayed variance and variance percent is the value the P1 reconciliation read answered for that date, and every row carries its business date
    And no service in the run reads another service's table or an ACE view, and the elapsed hop of each read is inside the 2 s budget

  Scenario: AC4 Each break key carries the case, queue and owner from rwb_case (new, D-RCV-60)
    Given the case set holds cases, queues and owners for some of the twelve break keys and no case for at least one of them
    When the harness reads the break block for the business date
    Then every key that a case holds carries that case number, its queue and its owner
    And the key that no case holds shows the key alone, with an empty case, queue and owner
    And no zero-filled or placeholder case, queue or owner is shown for it

  Scenario: AC5 A role without Platform administration R is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Platform administration R
    When the caller reads the console through the gateway-bff route and then reads each console operation directly
    Then the route answers 403 with "MSG-P4-002" and each owner operation answers 403 with "MSG-P4-002"
    And no block is rendered and no break, orphan or stale row is read

  Scenario: AC6 The stale block is refreshed by the P3 Schedule and unknown freshness is never fresh (new, D-RCV-60)
    Given a data product past its expected business date and a second product whose freshness the P1 read does not answer
    When DataQualityFreshnessCheck runs on the task queue "rwb-case" and its refreshStaleSet activity reads GET /api/recovery/source-data/v1/data-products/freshness for every product
    Then the stale product shows its last complete ACE business date, the business date of the refresh and "MSG-P1-001"
    And the product whose freshness is unknown is not shown as fresh
    And the run writes no table, and after a restart the stale block shows the business date of its last refresh

  Scenario: AC7 A retried or timed-out freshness activity never shows a product as fresh (new, D-RCV-60)
    Given the refreshStaleSet activity of DataQualityFreshnessCheck on the task queue "rwb-case" calls GET /api/recovery/source-data/v1/data-products/freshness and the call fails or exceeds its timeout
    When the activity is retried under its retry policy and the retries are exhausted
    Then the retries and the timeout follow the activity contract of section 12, with the values Not specified in the source documents (NEWAC-RWB-ITG-AD019-ITG-AC8)
    And every product whose freshness was not answered is not shown as fresh, and the run writes no table
    And the stale block shows the business date of its last successful refresh
```

Legacy AC1 and AC2 keep their legacy values and outcomes, with their source data answered by the rwb-source-data contract fake (section 12.8), and are the two criteria this story owns. The legacy AC3 of RWB-AD-019 (a stale data product shows with its last complete ACE business date) stays with RWB-P1-AD019-APP and RWB-P3-AD019-APP; AC6 asserts only that the stale reading reaches the console unchanged as part of the composition, and claims no ownership of that criterion. The legacy Given, When and Then stay the business facts; what this story proves is that the owners' answers reach the console unchanged, so the run asserts the legacy values against the P1 stub and against the real P1 service when it lands, and never computes them. AC1 is the business outcome RWB-P1-AD019-APP has to reach and AC2 is the referential criterion of RWB-P3-AD019-APP; the copies here assert the same behaviour across the service boundary.

Pass or fail gate (GAP-0447): all seven criteria, AC1 to AC7, pass on the stubs and again on the real owners. The environment, base hosts, fixture layout, extract format and retention are Not specified in the source documents (GAP-0447) and are fixed at the wave 4 entry check with the data steward. The SCR-45 route path and the break-list fields are taken from the gateway-bff contract once published. Until the rwb-source-data and rwb-case contracts publish the reconciliation, key-resolution and freshness reads, the harness pins the operation and the shape it uses and fails the hop on a mismatch (GAP-0441).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A break, an orphan or a stale product never deletes or changes a Workbench record or an ACE row; the console is read only and the harness writes nothing | Legacy RWB-AD-019 guardrails; AC2 | AC2, AC6 |
| BR2 | The REC-01 to REC-05 rows are read as the JOB-04 reconciliation of rwb-source-data produced them, and the variance and the variance percent are never recomputed at the screen or in the harness | Legacy AC1; Architecture v5 slide 44 (JOB-04 owner rwb-source-data); MSG-P1-012 | AC1, AC3 |
| BR3 | A break row carries the product group, the business date, the source count, the workbench count, the variance and the variance percent, and the account keys on the break with their days past due | Legacy AC1; `reconciliation_result` (DF-OPS-118 to DF-OPS-129) | AC1 |
| BR4 | A business key held on a case table with no row in the source contract is listed with its table, its column and its key, and the case and its row are unchanged | Legacy AC2; REC-05 | AC2 |
| BR5 | The referential check covers the keys rwb-case itself holds: `case_party.person_key`, `case_account.account_key` and `recovery_case.primary_person_key`; it reads no other service's table | DP-05; Ownership Map rows `case_party`, `case_account`, `recovery_case` all P3 | AC2 |
| BR6 | A data product is stale when the ACE batch for its expected business date is not complete, and it is shown with its last complete ACE business date and MSG-P1-001 | Legacy AC3; `data_product_load` (DF-OPS-001 to DF-OPS-008); MSG-P1-001 | AC6 |
| BR7 | Freshness is read through the rwb-source-data freshness operation; no service reads `data_product_load` by table and no service reads an ACE view but rwb-source-data | DP-05; ADR-010; Architecture v5 slide 41 (P1 owns freshness) | AC6 |
| BR8 | A break row shows the case number, the queue and the owner of a key from schema `rwb_case` only, and shows the key alone when no case holds it | DP-05; AC1; Ownership Map rows `recovery_case` and `case_account` P3, `case_list_row` P1 | AC4 |
| BR9 | The stale set is refreshed by a Temporal Schedule in rwb-case through the workflow kit; no Quartz job table and no shared job table is read, because JOB-05 is retired and the Schedules belong to each service; JOB-04 is an event-started workflow in rwb-source-data and runs no Schedule for this console | DP-10; Architecture v5 slide 44 (JOB-05 durable timers, retired; JOB-04 event-triggered) | AC6 |
| BR10 | SCR-45 is served by a gateway-bff composite route that composes the three reads in parallel, one hop each, and never a page that calls four services itself; the route is fixed with the platform edge story RWB-PLT-N001-CON | DP-19; Architecture v5 slide 44 note; RWB-PLT-N001-CON | AC3 |
| BR11 | Every call is one REST hop on `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream, never an in-process call and never a second hop | ADR-020; DP-11; DP-13 | AC3 |
| BR12 | A product whose freshness is unknown is never shown as fresh; a stale block that has not been refreshed shows the business date of its last refresh and nothing else | BR6; Legacy AC3 pattern | AC6, AC7 |

The harness asserts these rules and changes none of them. The run and the freshness are P1's, the console reads and the Schedule are P3's, and the platform stories named in section 13 supply the kit and the route.

### 9. State transitions

None. This story changes no case status, no break status and no data product status, and it is read only throughout: it reads the REC-01 to REC-05 rows of the JOB-04 reconciliation, the business keys the case tables hold, the freshness of the data products and the three console blocks, and it compares them. The Schedule refresh it observes changes only the stale set held in the memory of the rwb-case api and worker pods and writes no table, no business record and no event; the reconciliation run and the freshness stamps are rwb-source-data's and are untouched by the run.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW | Opens SCR-45 with Platform administration R, scope All, and reads the breaks, the orphans and the stale products; is the role the console is written for |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold Platform administration R and read the three blocks; the run asserts the right for all of them and the answer for RW-OFF |
| RW-OFF | Has no Platform administration R; is the refused caller of AC5 |
| QA lead | Owns the harness configuration, the fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| rwb-source-data (P1) identity | Owns the JOB-04 reconciliation run, the `reconciliation_result` and `data_product_load` tables, the ACE views, the freshness and the two reads; answers every reconciliation, key-resolution and freshness call in this story |
| rwb-case (P3) identity | Owns the three console reads, the annotation from schema `rwb_case` and the `DataQualityFreshnessCheck` Schedule with its `refreshStaleSet` activity; writes no table for them |
| rwb-access (P4) identity | Answers the authorise check, holds the roles and the scope, and records the read in the access log |
| ACE team | Owns the rows behind the break and the orphan and fixes them at source; the console and the harness change nothing |
| No delegation of authority level applies | The harness takes no business decision and approves nothing; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | rec_code, business_date, product_group, source_count, workbench_count, the variance and the variance percent | Read through the P1 reconciliation read only (owner P1) |
| DF-OPS-001 to DF-OPS-008 | data_product_load | product_code, source_system, business_date, loaded_at, status, stale_flagged_at | Read through the P1 freshness read only (owner P1) |
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code | Read through the P3 console reads |
| DF-CAS-024 to DF-CAS-029 | case_account | account_key, is_primary, linked_from, linked_to | Read through the P3 console reads |
| DF-CAS-030 to DF-CAS-035 | case_party | person_key and the party role | Read through the P3 console reads |
| DF-RPT-001 to DF-RPT-019 | case_list_row | business_date, case_no, account_key, product_group | Read through the P1 reconciliation read only (owner P1) |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, days_past_due, total_balance, data_as_of | Never read directly: behind the P1 reconciliation read only |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | person_key and the masked identity behind an orphan | Never read directly: behind the P1 key-resolution read only |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The reconciliation result, the data product load and the case list row belong to rwb-source-data (P1) and the case, the account link and the party row belong to rwb-case (P3); each is read only through its owner's published operation (DP-05). The harness writes no field and inserts no row; the only record written in the run is the access record of rwb-access on its own contract, and the report it writes is a run artefact outside every schema. Data Classification and Personal Data Inventory v5 classes `recovery_case.primary_person_key`, `case_account.account_key` and `case_party.person_key` as personal data (Indirect identifier, Confidential; shown within the role's scope, masked in UAT). The fixture and the run report hold synthetic values of these keys only, and a log carries the id of the read only, never the clear key.

### 12. Contract

Contract version pinned by this story: Not specified in the source documents (DOR-RWB-ITG-AD019-ITG-23). Each hop's contract version is pinned in the run report (section 4, step 12).

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The business date and the batch state behind the stale block, behind every break row and behind the Schedule refresh; the field shape is Not specified in the source documents (GAP-0441; ASM-0633) | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/<reconciliation read>` | P1 rwb-source-data | The REC-01 to REC-05 rows of the business date, with source count, workbench count, variance, variance percent and the account keys on the break; the exact path, the paging and the field shape are Not specified in the source documents (GAP-0441; ASM-0633) | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/<key-resolution read>` | P1 rwb-source-data | Whether a `person_key` or an `account_key` held on a case table resolves to a source row (REC-05); the exact path and the batch shape are Not specified in the source documents (GAP-0441; ASM-0633) | One hop, 2 s |
| GET | `/api/recovery/case/v1/data-quality/reconciliation-breaks` | P3 rwb-case | The break block: the REC-01 to REC-05 rows of the business date with each key annotated with its case number, queue and owner (AC1, AC3, AC4) | One hop, 2 s |
| GET | `/api/recovery/case/v1/data-quality/referential-completeness` | P3 rwb-case | The referential block: the business keys of the case tables that do not resolve, with table, column and key (AC2, AC3) | One hop, 2 s |
| GET | `/api/recovery/case/v1/data-quality/stale-products` | P3 rwb-case | The stale block: the data products past their expected business date with their last complete ACE business date and MSG-P1-001 (AC6) | One hop, 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read, and the refusal of a caller without Platform administration R (AC5) | One hop, 2 s |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13, ADR-020), and the composite call the browser makes is the gateway-bff route of RWB-PLT-N001-CON, which the harness replaces with the route stub of section 12.8 (DP-19). No operation is invented in this story: the freshness path is the Ownership Map row `GET /data-products/freshness` on the P1 base, the three console reads are the operations RWB-P3-AD019-APP publishes, and the session read is P4's own. The two P1 reads whose paths a source read does not state are written here with a shape placeholder and are raised as GAP-0441; the harness pins the operation it uses in its report and fails the hop if the owner publishes a different shape.

#### 12.3 Events published

None. The harness publishes no Kafka event; a read-only console publishes and consumes nothing, and there is no `rwb.integration.events.v1` topic for a test runner.

#### 12.4 Events consumed

None. No event is observed as a criterion of this story: the console is a read, the stale set is refreshed by a Schedule and not by an event, and a break or an orphan produces no event. Where an event happens to be on a topic in the run environment it is not asserted, counted or replayed, so no Kafka dependency is claimed here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Observed in the run for |
|---|---|---|---|
| DataQualityFreshnessCheck | Workflow started by a Schedule | `rwb-case` | The refresh of the stale set the console shows (AC6) |
| refreshStaleSet | Activity | `rwb-case` | One freshness read per data product, with the 2 s budget and one GET retry; returns the stale rows and writes no table (AC6) |
| reconciliation | Workflow | `rwb-source-data` | The JOB-04 reconciliation run behind the break, started by `AceIngestCheck` when the ACE business date is ready; it is observed as the producer of the result, never started or changed here (AC1) |

None added. The three are observed as they run in the SIT environment: P3's Schedule and its activity are built by RWB-P3-AD019-APP through the workflow kit, and the reconciliation workflow is P1's in RWB-P1-AD019-APP. The harness creates no workflow, activity or Schedule, changes none and owns none.

#### 12.6 Schedules

| Schedule | Cadence | Trigger | Observed for |
|---|---|---|---|
| DataQualityFreshnessCheck | Every 15 minutes during the business window | Temporal Schedule on the P3 service, overlap policy SKIP, catch-up window, workflow ID `data-quality-freshness-<env>`; the Schedule itself belongs to RWB-P3-AD019-APP | AC6, the refresh of the stale set and the refresh business date on the stale block |

The 15-minute cadence is a design default and is Not specified in the source documents (GAP-0441; ASM-0633); the harness drives the refresh by starting the Schedule once and by reading the refresh business date it stamps, and it never relies on the wall clock for a criterion. No scheduled job table and no Quartz row is read, because JOB-05 is retired in favour of durable timers and the Schedules belong to the services (Architecture v5 slide 44).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): `reconciliation_result`, `data_product_load` and `case_list_row` are P1's, `recovery_case`, `case_account` and `case_party` are P3's, and the ACE views belong to ACE and are read only by rwb-source-data (DP-05, ADR-010). The run report is a file outside every schema; the keys it holds are synthetic and it holds no real personal data.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | The P1 freshness read, the reconciliation read and the key-resolution read | `GET /data-products/freshness` answers business date `2027-06-30` with one product past its expected business date and its last complete ACE business date, and one product with no answer; the reconciliation read answers REC-01 for SSME with source count 2,903, case list count 2,891, variance 12, variance percent 0.41 and the twelve account keys with their days past due; the key-resolution read answers that `person_key` "P0099881" has no `v_ace_customer` row and that the other keys resolve; a slow answer variant breaks the 2 s budget (X1) |
| Stub for rwb-case | The three console reads | The break block with the same twelve keys annotated with a case number, queue and owner for all but one, and the one shown alone; the referential block with table `case_party`, column `person_key` and key "P0099881"; the stale block with the stale product, its last complete ACE business date and MSG-P1-001, and the unknown product not shown; a missing business date answers MSG-GEN-001 |
| gateway-bff composite route stub | The SCR-45 route of RWB-PLT-N001-CON (DP-19) | The parallel three-call composition, the Loading state and the per-block error state; the refusal of a caller without Platform administration R with 403 before any owner call |
| Stub for rwb-access | `GET /me/session` | Allows RW-DATASTEW with Platform administration R, scope All; refuses RW-OFF with 403 and MSG-P4-002 |

Each stub is generated from the published contract, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic keys and business date, the P1 read shapes, the P3 route specification and merge rules, the freshness read shape, the refresh cadence and the pass or fail gate are Not specified in the source documents (GAP-0441; ASM-0633).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; a read-only console, and no event is asserted (section 12.4) |
| Temporal | None added; `DataQualityFreshnessCheck`, `refreshStaleSet` and the P1 `reconciliation` workflow observed in the SIT environment |
| File | None. The run report is a harness artefact and transfers no claim-check file; the console has no export |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies of DP-10 and DP-19, RWB-PLT-E1071-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave; they are named here and in sections 3 and 12.6 and are not repeated in the metadata H field of this story, which stays None. DP-05 adds nothing. The two blocking dependencies are the I stories RWB-P1-AD019-APP and RWB-P3-AD019-APP, which replace their stubs; until they are live the run uses the stubs and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ConsoleProbe | Service | Reads the three console blocks through the P3 operations behind the route stub for a business date and holds the block states |
| BreakProbe | Service | Compares the break block field for field with the P1 reconciliation answer and asserts variance 12 and 0.41 percent as the owner returned them, with no recompute |
| OrphanProbe | Service | Asserts the orphan row with table, column and key, and the case and `case_party` row before and after the read |
| StaleProbe | Service | Asserts the stale product with its last complete ACE business date and MSG-P1-001, and that a product with unknown freshness is never fresh |
| ScheduleObserver | Service | Starts the P3 Schedule once, observes `DataQualityFreshnessCheck` and `refreshStaleSet`, reads the refresh business date and asserts that no table was written |
| SessionProbe | Service | Reads the session and asserts the refusal of RW-OFF with MSG-P4-002 at the route and at the owner, and MSG-GEN-001 for a malformed business date |
| StubSet | Fake | The four stubs of section 12.8, generated from the published contracts with the version pinned, plus the ACE row set, the case set and the stale set as data |
| EvidenceReport | Service | Writes one report per business date keyed by story, with the owner answers beside the displayed values, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real owners as RWB-P1-AD019-APP and RWB-P3-AD019-APP land, on business date `2027-06-30`, the synthetic ACE row set with 2,903 SSME accounts at 90 days past due or more less the exclusions, the synthetic case set with a case list of 2,891 and case "RW-2026-000140", `person_key` "P0099881", the twelve break keys of which one has no case, and one stale product with its last complete ACE business date. The harness seeds nothing by hand and never writes a schema row. The fixture layout, the keys, the read shapes, the route specification, the cadence and the gate are Not specified in the source documents (GAP-0441; ASM-0633).

**Build steps**

1. Generate the four stubs of section 12.8 from the published contracts, pin each contract version in the run report and fail the run on a mismatch (X1).
2. Build the ConsoleProbe: one read of the three blocks through the P3 operations behind the route stub, the Loading state and the per-block error state, with the business date on every row (AC3).
3. Add the BreakProbe for AC1 and AC3: source count 2,903, case list count 2,891, variance 12 and variance percent 0.41 compared field for field with the P1 answer, with the empty state of X2 and the slow answer of X1.
4. Add the annotation check for AC4: the twelve keys with case, queue and owner from the case set, and the one key that no case holds shown alone (X7).
5. Add the OrphanProbe for AC2 and AC3: table `case_party`, column `person_key`, key "P0099881", with the case and its `case_party` row read before and after and unchanged.
6. Add the StaleProbe for AC6: the stale product with its last complete ACE business date and MSG-P1-001, and the product with unknown freshness never shown fresh (X4, X10).
7. Add the ScheduleObserver for AC6: start the P3 Schedule once, observe `DataQualityFreshnessCheck` and `refreshStaleSet`, assert the freshness read per product and the refresh business date, assert no table write, and restart the pods for the X8 path.
8. Add the SessionProbe for AC5: RW-OFF refused with 403 and MSG-P4-002 at the route and at each owner operation, and a missing or malformed business date refused with MSG-GEN-001 (X6, X9).
9. Add the EvidenceReport and the pass or fail gate, and swap each stub for the real owner as RWB-P1-AD019-APP and RWB-P3-AD019-APP land.

**Feature switch.** None. The harness has no production flag and runs in the test environment only; it reads the console behind the route stub and takes no flag of its own.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-AD019-APP and RWB-P3-AD019-APP when they land, the run report holds the P1 answers beside the displayed values for every block, the legacy counts and variance are unchanged in every report, and no report claims a value the owner did not answer.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads and owns no message text. MSG-P1-012 is asserted on the REC-01 break with the date, the product, 12 accounts and 0.41 percent (AC1, X5). MSG-P1-001 is asserted on the stale product with its product code and its last complete ACE business date (AC6, X4). MSG-GEN-001 is asserted with the missing field name when the business date is missing or malformed (X9). MSG-P4-002 is asserted with the refused read for a caller without Platform administration R (AC5, X6). No message ID exists for an unreachable P1 read: the harness asserts the problem response and the failed criterion, never a text.

### 15. Screens and states

SCR-45 Data quality is not built or rendered here: the P3 slice owns it as the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), and the exact route specification is Not specified in the source documents (GAP-0441; ASM-0633). The harness calls the route stub and the three operations behind it, and reads the states through the owners.

| State | Read through | What the run asserts |
|---|---|---|
| Loading | The route stub and the three console reads | The three calls go out in parallel, one hop each, and no block waits for another |
| Breaks | `GET /api/recovery/case/v1/data-quality/reconciliation-breaks` and the P1 reconciliation read | 2,903 against 2,891, variance 12, variance percent 0.41, the twelve keys with their days past due and their case, queue and owner, and the key with no case shown alone |
| Referential completeness | `GET /api/recovery/case/v1/data-quality/referential-completeness` and the P1 key-resolution read | The orphan with table `case_party`, column `person_key` and key "P0099881", and the case and its `case_party` row unchanged |
| Stale | `GET /api/recovery/case/v1/data-quality/stale-products` and the P1 freshness read | The stale product with its last complete ACE business date, its status, the refresh business date and MSG-P1-001, and no product of unknown freshness shown fresh |
| A refused read | `GET /api/recovery/access/v1/me/session` and each console answer | 403 with MSG-P4-002 at the route and at the owner, no block rendered and no row read |
| Empty | `GET /api/recovery/case/v1/data-quality/stale-products` | The stale block with an empty stale set shows its last refresh date, not a fresh console (section 4) |
| Error | Each console answer | The per-block error state, with MSG-GEN-001 on a missing business date (section 4) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-019-01-ITG | AC1, AC3, AC4 | End to end | The synthetic row set that the rwb-source-data contract fake (section 12.8) answers, with 2,903 SSME accounts at 90 days past due or more less the exclusions, the case list at 2,891, REC-01 variance 12 and 0.41 percent, the twelve break keys with their days past due, their case, queue and owner, and one key with no case |
| TC-AD-019-02-ITG | AC2, AC3 | End to end | `case_party` on case "RW-2026-000140" with `person_key` "P0099881" and the key-resolution read of the rwb-source-data contract fake (section 12.8) answering that no customer row exists for it, with the case and its row read before and after |
| TC-AD-019-03-ITG | AC6 | Integration | A data product past its expected business date with its last complete ACE business date, a second product with unknown freshness, and the P3 Schedule started once |
| TC-AD-019-04-ITG | AC5, Access | Component | A synthetic caller with role RW-OFF and no Platform administration R, and a read with a missing or malformed business date |
| TC-AD-019-05-ITG | Section 12 contracts | Contract | The published contract of each operation, event and activity of section 12, with the stub of each hop generated from it and its version pinned in the run report |
| TC-AD-019-06-ITG | AC7 | Integration | The refreshStaleSet activity of DataQualityFreshnessCheck on the task queue "rwb-case" with the P1 freshness read stubbed to fail and then to exceed its timeout, and the stale block read before and after the activity retries |

The legacy TC IDs TC-AD-019-01 to TC-AD-019-04, their legacy Covers (AC1, AC2, AC3 and Access) and their legacy Test wording are kept as the `-ITG` copies of this story; the legacy level System maps to End to end and Access maps to Component. AC3 and AC4 have no legacy test case of their own in this key, so they are asserted as the ordered checks of TC-AD-019-01-ITG and TC-AD-019-02-ITG, and legacy AC3 is asserted with the stale checks of TC-AD-019-03-ITG. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the counts, the variance, the variance percent, the product groups, the last complete ACE business dates, the business date, the case and person keys and the cadence are data in the fixture, never a constant.
- Personal data: `person_key`, `primary_person_key` and `account_key` are Indirect identifier, Confidential (Data Classification and Personal Data Inventory v5). The fixture uses synthetic values only, the report carries synthetic keys and counts and never a name, an address or an identity number, and a log carries the id of the read only, never the clear key.
- ACE data only through the owner: the ACE rows, the reconciliation result and the freshness arrive through the rwb-source-data contract, and no service in the run reads `recovery.v_ace_*` but rwb-source-data (DP-05, ADR-010).
- No cross-schema read: every value is read through its owner's published operation, and the harness opens no connection to any schema (DP-01).
- A break changes nothing: no run step deletes, edits or acknowledges a Workbench record or an ACE row, and the console has no write operation.
- One hop and a 2 s budget per call with a circuit breaker per downstream, so the harness fails where a screen would (ADR-020, DP-11, DP-13).
- A product with unknown freshness is never fresh: an unrefreshed stale block shows the business date of its last refresh and nothing else.
- SIT only: the harness never runs against UAT or production, and a failing criterion is fixed in the owning service or raised as a gap, never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-AD-019 Data quality and reconciliation console | `04 User stories/Recovery Workbench Administration Stories v3.md`, lines 1552 to 1633 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 1571 to 1575 | Section 7, AC1, marked (legacy RWB-AD-019 AC1) |
| Legacy AC2, verbatim | The same, lines 1577 to 1581 | Section 7, AC2, marked (legacy RWB-AD-019 AC2) |
| Legacy AC3, the stale data product | The same, lines 1583 to 1586 | Section 7, AC6, with its value unchanged |
| Legacy test cases TC-AD-019-01 to TC-AD-019-04 and their Covers | The same, lines 1626 to 1631 | Copied as `-ITG` in section 16 |
| Legacy endpoints, screen states, permission check and messages | The same, lines 1599 to 1622 | Sections 12.2, 15 and 14 |
| The P3 slice of this legacy key, its three console operations and its Schedule | `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 AD019 APP Data quality and reconciliation console v1.md` | Sections 1, 3, 12.2, 12.5, 12.6 and 13 |
| The five assumptions recorded with that P3 slice | The same file, sections 3 and 12 | Section 3 of this file, restated in the harness default of ASM-0633 and not re-cited by id |
| rwb-source-data owns the ACE view contract, extension tables, freshness and reconciliation; topic `rwb.source-data.events.v1`; task queue `rwb-source-data` | Architecture v5 slide 41; slide 15 (`GET /freshness`, `AceIngestCheck`, reconciliation) | Sections 2, 10, 12.2 and 12.5 |
| JOB-04 Reconciliation, owner rwb-source-data, event-triggered workflow; JOB-05 durable timers retired | Architecture v5 slide 44 | Sections 2, 8 (BR2, BR9) and 12.6 |
| Events carry IDs and facts only, and each service owns its topic | Architecture v5 slide 42 | Sections 12.3 and 12.4 |
| `reconciliation_result`, `data_product_load` and `case_list_row` owned by P1; `recovery_case`, `case_account` and `case_party` owned by P3; `GET /data-products/freshness` and `GET /admin/jobs` on the P1 base | `_work/msr/plan/ownership.json`, table rows and API rows | Sections 10, 11 and 12.2 |
| The workflow kit, its Schedule template and the typed activity contract; Schedules replace Quartz jobs in the owning service | Temporal and Drools Design slide 12 notes; the `Scheduled job` template and the platform note that Quartz jobs become Temporal Schedules | Sections 2, 8 (BR9), 12.5 and 12.6 |
| DP-05, DP-10, DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-010 (only rwb-source-data reads the ACE views) and ADR-020 (contract-first REST, one hop, 2 s) | Architecture Decision Records, as added by Template and Rules v1 §R8.4 | Sections 2, 8 and 17 |
| Legacy key, disposition, business epic, wave and release | Ownership and split plan of this run | Metadata table: Split (rework), EP08, wave 4, 30 June 2027 (tentative), copied unchanged |
| Gaps and assumptions | This WP | GAP-0441; ASM-0633 |

### 19. Out of scope

- RWB-P1-AD019-APP and RWB-P1-AD019-OPS: the JOB-04 reconciliation run, the REC-01 to REC-05 rules, the `reconciliation_result` table, the freshness stamp in `data_product_load`, the key-resolution read, the ACE views and the deployment of the run.
- RWB-P3-AD019-APP: the three console operations, the annotation query, the `DataQualityFreshnessCheck` Schedule and its `refreshStaleSet` activity, and the screen component.
- The freshness stamp and the `data_product_load` row: written by rwb-source-data and only read here.
- The data quality exception endpoint and its table, withdrawn by D-RCV-35; there is no exception table in the target and none is read.
- The interface and job monitor, legacy RWB-AD-018 and its own integration story RWB-ITG-AD018-ITG, and the `GET /admin/jobs` row it reads.
- SCR-45 Data quality as a built screen and the gateway-bff composite route itself, RWB-PLT-N001-CON: the harness calls a stub of the route and builds neither.
- The stale-set refresh cadence as a service configuration, and the platform stories RWB-PLT-E1071-CON and RWB-PLT-N001-CON.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service, and no deployment.
