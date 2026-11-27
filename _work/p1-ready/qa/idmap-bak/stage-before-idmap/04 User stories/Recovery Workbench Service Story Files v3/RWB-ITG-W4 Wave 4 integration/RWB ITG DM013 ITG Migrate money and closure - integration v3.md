# RWB-ITG-DM013-ITG Migrate money and closure

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- JOB-04 is started by the readiness call as a child of `AceIngestCheck`; the invalid rerun call is removed (RD-P1-012, RD-P1-040; findings #1, #13).
- The write-off decision is read from rwb-writeoff, whose read is pending (NEW-GAP-F07-02; #3); posting_ref and posted_date are ACE data and are not carried (RD-P1-027; #4).
- Owners load their own records, money key orphans come from the orphan list of RWB-P1-DM013-APP, and there is no publish status (RD-P1-022, RD-P1-024; #2, #6, #9, #11).
- Freshness, readiness, rights, messages, provenance and contract version aligned to rwb-source-data.yaml 5.1.0; AC8 added (#5, #7, #8, #10, #12, #14).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- A repeated readiness call answers 202 and starts nothing once every due source is stamped and the run has ended (RD-P1-065, register XD-11).
- The legacy proceeds `amount` and `received_date` are carried as the value at act time (RD-P1-068).
- The reconciliation result reads are cited as published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, RD-P1-063).

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM013-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-DM013-ITG-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-DM013-ITG-14) |
| Contract fake library version | rwb-source-data: `fakes/rwb-source-data/5.1.0/` (RD-P1-011), not yet recorded as published; other services: Not specified in the source documents (DOR-RWB-ITG-DM013-ITG-22) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); rwb-payment, rwb-case, rwb-writeoff and rwb-access 5.1.0 |
| Depends on (build) | RWB-P1-DM013-APP, RWB-P8-DM013-APP (not done yet) |
| Contract dependencies | RWB-P1-E1015-CON (readiness and freshness), RWB-P1-E1011-CON (reconciliation result reads, published in the yaml file), RWB-P1-E1016-CON (data product records); the CON stories of rwb-payment, rwb-case, rwb-writeoff and rwb-access: Not specified in the source documents (DOR-RWB-ITG-DM013-ITG-21) |
| Integration dependencies | RWB-P1-DM013-APP, RWB-P8-DM013-APP |
| External dependencies | None |
| Open decisions | DL25 (open; assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-022, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-065, RD-P1-068, RD-P1-063 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-013 for the wave 4 cutover reconciliation harness for money and closure. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM013-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 13 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; cutover reconciliation harness aligned to the readiness chain, the migration field mapping and the published reads.

### 1. Story

As a **RW-DATASTEW** (data steward), I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated money and closure records resolves to its ACE view row, lists every orphan for the data steward and the ACE team, and proves the closure facts survived cutover, against the owning services' published contracts and their fakes**, so that **money already received stays matched to its case and a closed case keeps its closure date and its closure reason from the first day after cutover**.

This story builds the harness and the evidence, and nothing else. The real records are extracted by RWB-P1-DM013-APP and loaded by their owners on their own Flyway sequences (DP-15): P8 rwb-payment for proceeds, S7 rwb-writeoff for the write-off decisions and P3 rwb-case for the closure facts (RD-P1-027). P1 loads no money or closure record, and DP13 is read through the ACE views with no copy. The reconciliation is JOB-04 of RWB-P1-E1011-APP (RD-P1-022). The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes one report per business date.

### 2. Business rationale

A proceeds row served against a case with a payment_code that resolves to no ACE payment row is money whose match nobody can defend. The customer has paid, the case still shows the item open, the collection officer chases a payment that ACE booked weeks ago, and the difference surfaces only in a reconciliation nobody ran. The failure is quiet in the same way as a lost key: the cutover load reports a clean run while the references it wrote point at rows the ACE views do not hold. A closed case that loses its closed date or its closure reason is worse, because the next cycle reads the case as live, re-ages it, and either re-notices the customer or keeps a provision that the write-off already released.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's DP13 Money and closure data product (DP-05), never from another service's schema and never by a direct view read (DP-01); proceeds and their match are read from rwb-payment, which owns payment and proceeds matching; the closure is read from rwb-case, which owns recovery_case; the write-off decision is read from rwb-writeoff, which loads and holds it; the cutover loads run on each owning service's Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and this legacy story states that no screen exists; every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries REQ-RDF-007, REQ-RDF-008, REQ-RDF-013, NFR-018 and DL25 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of P1 rwb-source-data (rwb-source-data.yaml 5.1.0: DP13, DP01 and DP02 records, freshness, readiness call and status, reconciliation result reads), P8 rwb-payment (proceeds and their match), P3 rwb-case (the case and its closure), S7 rwb-writeoff (the write-off decision) and P4 rwb-access (the caller's rights) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP13 Money and closure with one system of record, ACE from ALS and GL, daily at 08:00, so payment_code has one named owner before a key is resolved (FSD P1 v3, line 295).
- The reconciliation result reads are published (`getAdminReconciliationResults`, RD-P1-063). Pending: rwb-writeoff.yaml publishes no read of a write-off decision, owner rwb-writeoff contract owner (NEW-GAP-F07-02).
- The harness caller of the readiness call holds Platform administration U; the caller of the record and freshness reads holds Case record R, and of the readiness status and reconciliation result reads Platform administration R. A key field that the record read returns with `masked` true fails the run and is reported.
- The data product catalog also holds DP01 Account and arrears and DP02 Customer and party, so account_key and person_key have one named owner before a key is resolved (FSD P1 v3, A2.2).
- The cutover load of each owning service's Flyway sequence (DP-15) has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM013-APP owns the extract, its key resolution and the clean-day count, JOB-04 of RWB-P1-E1011-APP owns the reconciliation (RD-P1-022), and RWB-P8-DM013-APP owns the proceeds match; until they land, the reconciliation extract fixture stands in for the reconciliation output and the payment stub stands in for the match.
- The harness environment, the cutover extract fixture layout, the break-list fields and the evidence retention: Not specified in the source documents (GAP-0453; ASM-0645).
- The synthetic case, the synthetic keys, the dates, the amounts and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the two waits are RWB-P1-DM013-APP and RWB-P8-DM013-APP, which replace their stubs and never block the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30: case RW-2026-000913, closed on 2026-11-30 with closure_reason WRITTEN_OFF; proceeds row PAY-SYN-000913 on that case with source INSURER, amount 12500.00, received_date 2026-11-18 and matched_to empty; write-off decision with tax_criteria_met true and committee_date 2026-11-20; the ACE posting_ref POST-SYN-000913 and posted_date 2026-11-30, which are served by DP13 and are not carried; account_key ACC-SYN-000913 and person_key PERS-SYN-000913. On Day 1, before the cutover loads are in SIT, the stub of §12.8 returns the same records.
2. Harness: starts the chain for business date 2026-11-30 with `POST /api/recovery/source-data/v1/business-days/{date}/ready` and a UUID `Idempotency-Key` (202), and waits until `AceIngestCheck` has stamped the ALS batch and its child `ReconciliationWorkflow` (`recon-2026-11-30`, JOB-04) has completed, after rwb-case answers its allocation or at 07:15 (RD-P1-040). The harness never reruns JOB-04: `POST /admin/jobs/{jobId}/rerun` takes the run uuid of a FAILED run only (RD-P1-012).
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts closed_date 2026-11-30 and closure_reason WRITTEN_OFF (DF-CAS-022, DF-CAS-023).
4. Harness: reads the proceeds through `GET /api/recovery/payment/v1/proceeds?caseId={caseId}` and asserts payment_code PAY-SYN-000913, source, amount 12500.00, received_date 2026-11-18, matched_to empty, `migration_source` and `migrated_at` (DF-FIN-001 to DF-FIN-008); posting_ref (DF-FIN-009) is not carried (RD-P1-027).
5. Harness: reads the write-off decision through the rwb-writeoff read, whose path is pending (NEW-GAP-F07-02) and which the stub answers until then, and asserts committee_date 2026-11-20 and tax_criteria_met true (DF-FIN-014, DF-FIN-015). posted_date (DF-FIN-016) is ACE data and is asserted only on the DP13 read of step 6.
6. Harness: resolves each business key. payment_code is resolved through `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}`, account_key through `.../DP01/records?caseId={caseId}` and person_key through `.../DP02/records?caseId={caseId}`, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP13` for `status`, `businessDate` and `loadedAt` of the product. The record read returns rows of `fields` with `fieldName`, `value` and `masked`. A key with a matching row resolves; a key with none does not.
7. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan, its key type, its key value, its reason and its two owners, and reads the REC rows through `GET /api/recovery/source-data/v1/admin/reconciliation/results?from=2026-11-30&to=2026-11-30`; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen. The REC-05 scope holds no payment_code (RD-P1-022): on the real services the money key orphans are read from the resolution stamp and orphan list that the AceKeyResolver of RWB-P1-DM013-APP records.
8. Harness: repeats the readiness call for the same business date with a new UUID `Idempotency-Key`, asserts no second set of result rows and compares the break list and the counts of proceeds rows, closed cases and write-off decisions with the first run. The repeated call answers 202 with the stored state and starts nothing; a second run of the date exists only through the rerun of a FAILED run (RD-P1-065 rule 3, register XD-11).
9. Harness: reads the caller's rights through `GET /api/recovery/access/v1/me/session` as a synthetic caller with role RW-OFF and no Platform administration right, then sends the readiness call as that caller and asserts 403 with `messageCode` MSG-P4-002, no run started and no break row written.
10. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the criteria of section 7.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-013-02-ITG (ITG AC1) |
| X2 | The cutover extract fixture lacks a required key or a required date on a migrated record | The run fails and the report names the case and the missing field; a record without a key is never reported as reconciled | None | TC-DM-013-02-ITG (ITG AC1) |
| X3 | A payment_code resolves to no DP13 row and the extract does not list it | The run fails on AC1 and the report names the case, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-013-02-ITG (ITG AC1, ITG AC2) |
| X4 | A repeated run lists the same break twice | The run fails on AC3 and the report names the two rows and the business date | None | TC-DM-013-03-ITG (ITG AC3) |
| X5 | The ALS batch is late (no ALS stamp, so JOB-04 is not started), or the product read answers `status` `STALE` | The readiness status reads `LATE`, or the freshness read answers `STALE` (`businessDate` null when never stamped); the run is reported as not run, never as passed | MSG-P1-001 | Test Cases v9: TC-DM-013-02-ITG, TC-DM-013-08-ITG (ITG AC1, ITG AC8) |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC5 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-013-04-ITG (ITG AC5) |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC3 and the report names each count and its two values | None | TC-DM-013-03-ITG (ITG AC3) |
| X8 | A closure date, a closure reason or a committee date on a read answer differs from the cutover extract | The run fails on AC4 and the report names the case, the field and the two values; a fact that moved in cutover is never reported as kept | None | TC-DM-013-01-ITG (ITG AC4) |

The report text is for the wave entry check and is not part of the message standard. The fixture layout, the break-list fields, the report shape, the evidence retention and the pass or fail gate are held as configuration and agreed at the wave 4 entry check; their values are Not specified in the source documents (GAP-0453). The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only waits are RWB-P1-DM013-APP and RWB-P8-DM013-APP, and their stubs answer until they land |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The migrated payment codes and the closure facts are proven against the ACE views, and every orphan is on a list with a reason and two owners, before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one closure assertion, one break-list assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I stories land |

### 7. Acceptance criteria

```gherkin
Feature: Migrate money and closure - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds case "RW-2026-000913" closed on "2026-11-30" with closure_reason "WRITTEN_OFF"
    Given the case holds proceeds row with payment_code "PAY-SYN-000913" and matched_to empty
    Given the case holds account_key "ACC-SYN-000913" and person_key "PERS-SYN-000913"
    Given ReconciliationWorkflow "recon-2026-11-30" (JOB-04) has completed for business date "2026-11-30" as the child of AceIngestCheck

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-013 AC2)
    Given the migrated records
    When the harness resolves the keys of the migrated records for business date "2026-11-30"
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team
    And no payment_code is expected from the REC-05 step of JOB-04, whose scope does not hold it (RD-P1-022)

  Scenario: AC2 An orphan payment_code is listed and the money stays unmatched (new, D-RCV-60)
    Given a migrated proceeds row for case "RW-2026-000913" carries payment_code "PAY-SYN-000913"
    And the rwb-source-data DP13 contract returns no row for payment_code "PAY-SYN-000913"
    When the harness reads the reconciliation outcome for business date "2026-11-30"
    Then the break list of the reconciliation extract fixture holds one row with key type "PAYMENT", key value "PAY-SYN-000913", reason "NO_ACE_ROW" and owner role "RW-DATASTEW"
    And the proceeds row still shows matched_to empty through the rwb-payment contract
    And the run report names the ACE team as the second owner of the break
    And on the real services the orphan is read from the orphan list of RWB-P1-DM013-APP in the cutover record

  Scenario: AC3 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When POST /business-days/2026-11-30/ready is called again with a new UUID Idempotency-Key and answers 202
    Then the repeated call starts nothing: no second ReconciliationWorkflow run for "2026-11-30", because every due source of the date is stamped and the run has ended
    And no second set of reconciliation result rows exists for 2026-11-30
    And the break list holds exactly one row for payment_code "PAY-SYN-000913"
    And the counts of proceeds rows, closed cases and write-off decisions equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC4 The closure keeps its date and reason and no posting is copied (new, D-RCV-60)
    Given the closed case "RW-2026-000913", its write-off decision and its proceeds row
    When the harness reads them through the rwb-case, rwb-writeoff and rwb-payment contracts and the DP13 record read
    Then the case keeps closed_date "2026-11-30" and closure_reason "WRITTEN_OFF" (DF-CAS-022, DF-CAS-023)
    And the write-off keeps committee_date "2026-11-20" (DF-FIN-015) and tax_criteria_met true (DF-FIN-014)
    And the proceeds row keeps payment_code "PAY-SYN-000913" as a reference, amount "12500.00" and received_date "2026-11-18"
    And posting_ref and posted_date are not carried and are answered by the DP13 record read (RD-P1-027)
    And on the real services the write-off assertions are pending the rwb-writeoff read (NEW-GAP-F07-02)
    And DP13 holds no copy of a v_ace_payment or a v_ace_write_off row

  Scenario: AC5 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When that user calls POST /business-days/2026-11-30/ready with a UUID Idempotency-Key
    Then the answer is 403 with a problem body whose messageCode is "MSG-P4-002"
    And no run starts and no break row is written

  Scenario: AC6 The zero-tolerance rule, the per-service Flyway sequence and the retention rule are asserted (new, D-RCV-60)
    Given one migrated money or closure record has an unresolved business key
    When the harness reads the cutover record and the reconciliation outcome for business date "2026-11-30"
    Then the clean-day count is 0, sign-off is not open and wave 4 stays closed while that record is unresolved (BR3)
    And no publish status is read, because rwb-source-data holds none
    And each service applies its own Flyway sequence in its own schema (BR7)
    And each Workbench recovery record class carries a retention and archive rule, and ACE data is retained by ACE (BR9)

  Scenario: AC7 A consumed call that fails or does not answer is reported and no record is served (new, D-RCV-60)
    Given the DP13 record read fake answers 503 with messageCode "MSG-GEN-006", or does not answer within 2 s, for business date "2026-11-30"
    When the harness calls it
    Then the run report names the failed hop and its contract
    And no record of the failed hop is served

  Scenario: AC8 A late or never stamped batch is reported as not run (new, RD-P1-040, RD-P1-041)
    Given the readiness status fake answers status "LATE" for business date "2026-11-30"
    And the freshness fake answers DP13 with status "STALE" and businessDate null
    When the harness runs for business date "2026-11-30"
    Then the run report records "not run" with DP13, the business date and "MSG-P1-001"
    And no key is resolved, no break row is asserted and the run is not marked passed
```

Legacy AC1 and AC3 belong to RWB-P1-DM013-APP and RWB-P8-DM013-APP, and the eight criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated proceeds, closure or write-off decision record resolves to an ACE view row before the record is served | REQ-RDF-007; DL25 |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 |
| BR3 | Zero tolerance: wave 4 does not open while one migrated money or closure record has an unresolved key or a closure fact that moved | DL25; NFR-018; DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00; no P1 publish status (RD-P1-024) |
| BR4 | ACE data is read only through the DP13 Money and closure product of rwb-source-data, and never into a Workbench table as a copy | D-RCV-35; ADR-010 |
| BR5 | A migrated record keeps its `migration_source` and `migrated_at`, and never a copy of an ACE row; a payment_code is a reference, and posting_ref and posted_date are ACE data that is not carried | Legacy RWB-DM-013 AC1; D-RCV-35 (U1); RD-P1-027 |
| BR6 | A closed case keeps its closed date and its closure reason, and a write-off decision keeps its committee date | Legacy RWB-DM-013 AC1; DL25 |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 |
| BR8 | A reconciliation break changes no money: an unmatched proceeds row stays unmatched until the ACE row appears or the business decides the match | REQ-RDF-008; legacy RWB-DM-013 AC2 |
| BR9 | Workbench recovery records carry a retention and archive rule by record class, and ACE data is retained by ACE | REQ-RDF-013; NFR-031 |

The harness asserts these rules and changes none of them.

Criterion coverage: BR1 AC1; BR2 AC1 and AC2; BR4, BR5 and BR6 AC4; BR8 AC2. BR3, BR7 and BR9 AC6.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| CLOSED | Reconciliation for the business date with every key resolved | `recon-2026-11-30` completes and every payment_code, account_key and person_key has a DP13, DP01 or DP02 row | CLOSED |
| CLOSED | Reconciliation for the business date with one orphan payment_code | The rwb-source-data DP13 contract returns no row for payment_code PAY-SYN-000913 | CLOSED |
| CLOSED | A listed orphan resolves and is reconciled | The rwb-source-data DP13 contract returns a row for the key and the reconciliation of a later business date runs, or a FAILED run of the date is rerun | CLOSED |

The closure is unchanged on every row. An orphan is listed and its matched_to stays empty; once the key resolves and is reconciled, the break is no longer listed.

The harness changes no state. Every value in the table is held by its owner: P3 rwb-case holds the case, its closed date and its closure reason, P8 rwb-payment holds the proceeds and their match, S7 rwb-writeoff holds the write-off decision, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the reconciliation result for a business date; holds Platform administration R and Case record R; owns the break list with the ACE team. Does not start or rerun a run |
| Harness caller | Holds Platform administration U for the readiness call, Platform administration R for the status and result reads and Case record R for the record and freshness reads |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 as a child of `AceIngestCheck` and writes the reconciliation result, P8 rwb-payment holds the proceeds and their match, P3 rwb-case holds the closure, S7 rwb-writeoff holds the write-off decision, and P4 rwb-access answers the rights; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the caller's rights are answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-022, DF-CAS-023 | recovery_case | closed_date, closure_reason | Read through the rwb-case contract |
| DF-FIN-001 to DF-FIN-009 | proceeds | payment_code, source, amount, received_date, matched_to (carried; `amount` DF-FIN-006 and `received_date` DF-FIN-007 as CARRY "value at act time" with `migration_source` and `migrated_at`, RD-P1-068 rule 2); posting_ref (DF-FIN-009) is ACE_READ and never carried (RD-P1-027) | Read through the rwb-payment contract; posting_ref through the DP13 record read |
| DF-FIN-010 to DF-FIN-020 | write_off | tax_criteria_met, committee_date (carried); amount (DF-FIN-013) and posted_date to gl_product (DF-FIN-016 to DF-FIN-019) are ACE_READ | Read through the rwb-writeoff contract, path pending (NEW-GAP-F07-02); ACE fields through the DP13 record read |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code and the ACE facts behind it | Read through the rwb-source-data DP13 contract |
| DF-ACE-261 to DF-ACE-269 | v_ace_write_off | write_off_key and the ACE facts behind it | Read through the rwb-source-data DP13 contract |
| Standard column | recovery_case, proceeds, write_off | migration_source, migrated_at (RD-P1-027) | Read through the owning contracts |
| Not specified in the source documents (DOR-RWB-ITG-DM013-ITG-20) | reference data: parameters and lists | parameter name | Read through the reference-data contract (DP-06, DP-07) |

Field IDs are those in the Logical Data Model and Data Dictionary v9. recovery_case is P3's, proceeds is P8's and write_off is S7's; the harness reads the closure through the rwb-case contract, the proceeds and their match through the rwb-payment contract, and the write-off decision through the rwb-writeoff contract, never from a table. The ACE side is DP13 Money and closure, whose system of record is ACE from ALS and GL and which loads daily at 08:00 (FSD P1 v3, line 295), read through the rwb-source-data data-product contract, never from a view and never from a table. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Start `AceIngestCheck`, whose child is JOB-04, with a UUID `Idempotency-Key`; 202 (AC1, AC3, AC5) |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data | `RUNNING`, `DONE` or `LATE` for the business date (AC8) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | The REC rows of the business date (AC1, AC6); pending in the yaml file (RWB-P1-E1011-CON) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The payment and write-off ACE rows that resolve payment_code and write_off_key (AC1, AC2, AC4) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The account rows that resolve account_key (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | The party rows that resolve person_key (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP13` | P1 rwb-source-data | `status`, `businessDate` and `loadedAt` of DP13 (AC1, AC3, AC8) |
| GET | `/api/recovery/payment/v1/proceeds?caseId={caseId}` | P8 rwb-payment | The proceeds rows, their payment_code, their match and matched_to (AC1, AC2, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case and its closure, closed_date and closure_reason (AC1, AC4) |
| GET | Path pending (NEW-GAP-F07-02) | S7 rwb-writeoff | The write-off decision, its committee_date and tax_criteria_met (AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's rights, and the absence of Platform administration R (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). Every error of rwb-source-data is an `application/problem+json` body with `messageCode` (RD-P1-004). No operation is invented in this story: each stated path is the owner's published operation, a missing one is marked pending, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness starts JOB-04 through the readiness call, not through an event, and reads the result through the same contract rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04, `ReconciliationWorkflow` on rwb-source-data (Architecture v5 slides 15 and 44), workflow ID `recon-{businessDate}`, runs as the child of `AceIngestCheck` (RD-P1-040) and is exercised through the readiness call. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. The harness starts the chain for the business date under test with the readiness call and sets no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the closure is P3's, proceeds is P8's, the write-off row is S7's and the reconciliation result is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | `fakes/rwb-source-data/5.1.0/`: the P1 operations of §12.2 | DP13 returns the payment and write-off ACE rows of the case except payment_code PAY-SYN-000913, DP01 returns one row for ACC-SYN-000913, DP02 returns one row for PERS-SYN-000913, freshness returns `status` LOADED, business date 2026-11-30 and a load time for DP13, DP13 returns posting_ref POST-SYN-000913 and posted_date 2026-11-30, the readiness call answers 202, the status answers DONE, and the result read returns the REC rows of the date |
| Stub for rwb-payment | `GET /proceeds?caseId={caseId}` | One proceeds row PAY-SYN-000913 with source INSURER, amount 12500.00, received_date 2026-11-18 and matched_to empty |
| Stub for rwb-case | `GET /cases/{caseId}` | Case RW-2026-000913, closed 2026-11-30 with closure_reason WRITTEN_OFF, holding account_key ACC-SYN-000913 and person_key PERS-SYN-000913 |
| Stub for rwb-writeoff | Read of the write-off decision, path pending (NEW-GAP-F07-02) | One write-off decision of the case, with committee_date 2026-11-20 and tax_criteria_met true |
| Stub for rwb-access | `GET /me/session` | Allows RW-DATASTEW with Platform administration R; returns RW-OFF without it |
| Cutover extract fixture | The migrated records of the legacy story | The closed case with closed_date and closure_reason, the proceeds row with payment_code, source, amount, received_date and matched_to, the write-off decision with committee_date and tax_criteria_met, the account_key and the person_key, and the migration_source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row with key type PAYMENT, key value PAY-SYN-000913, reason NO_ACE_ROW, owner role RW-DATASTEW, the ACE team as second owner, and the counts of proceeds rows, closed cases and write-off decisions for the business date |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment, the fixture layout, the break-list fields and the evidence retention are Not specified in the source documents (GAP-0453; ASM-0645).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 11 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contract |
| Temporal | None added; `ReconciliationWorkflow` (JOB-04) is exercised as the child of `AceIngestCheck` |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The two blocking dependencies are the I stories RWB-P1-DM013-APP and RWB-P8-DM013-APP, which replace their stubs; until they are live the run uses the stubs, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the criteria of section 7 in order for a business date and holds the run lock |
| StubSet | Fake | The five stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic closed case, its proceeds row, its write-off decision, its account_key and person_key, with migration_source and migrated_at |
| MoneyKeyResolver | Service | Resolves payment_code through DP13, account_key through DP01 and person_key through DP02 with the freshness read, and names each key that does not resolve |
| ClosureFactAssertion | Service | Compares the case closure, the write-off committee date, tax_criteria_met and the payment_code reference with the cutover extract, and proves no ACE row is copied |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its key type, key value, reason and its two owners, and one row only on a repeated run |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the two I stories land, on the synthetic case RW-2026-000913, closed on 2026-11-30 with closure_reason WRITTEN_OFF, proceeds PAY-SYN-000913 with source INSURER, amount 12500.00, received_date 2026-11-18 and matched_to empty, the write-off decision with committee_date 2026-11-20 and tax_criteria_met true, the ACE posting_ref POST-SYN-000913 and posted_date 2026-11-30 on the DP13 fake, account_key ACC-SYN-000913, person_key PERS-SYN-000913 and business date 2026-11-30. In SIT the records come from the cutover load of each owning service's own Flyway sequence (DP-15). The environment and the base hosts are Not specified in the source documents (GAP-0453; ASM-0645). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the five stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-11-30, with every required key and date present (X2).
3. Build the JourneyRunner for AC1: send the readiness call with a UUID Idempotency-Key, wait for `recon-2026-11-30`, read the case, the proceeds and the write-off decision through their owners, resolve payment_code through DP13 and account_key and person_key through DP01 and DP02 with the freshness read, and list each orphan (X5).
4. Add the MoneyKeyResolver assertion that every key on a migrated record resolves, and that each orphan is on the list for the data steward and the ACE team (X3).
5. Add BreakListAssertion for AC2: one row with key type PAYMENT, key value PAY-SYN-000913, reason NO_ACE_ROW and owner role RW-DATASTEW, the ACE team named as second owner in the report, and matched_to still empty through the rwb-payment contract.
6. Add AC3: repeat the readiness call for the same business date with a new Idempotency-Key, assert one break row, equal counts of proceeds rows, closed cases and write-off decisions, and one report entry per business date (X4, X7).
7. Add ClosureFactAssertion for AC4, then the access path for AC5 through `GET /api/recovery/access/v1/me/session` and the refused readiness call, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6, X8).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM013-APP and RWB-P8-DM013-APP when they land, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-P1-001 is asserted with {product} DP13 and {date} the business date under test, so a late ACE batch is never read as an empty product. MSG-P1-012 is raised by rwb-source-data only for a REC-01 or REC-02 BREAK (RD-P1-042); the harness asserts it only against a BREAK fixture, with the {date}, {product}, {variance} and {pct} that fixture carries. MSG-GEN-001 is asserted with {field} the name of the missing fixture field. MSG-P4-002 is asserted with {action} the readiness call and the caller's role named in the report.

### 15. Screens and states

The legacy story has no screen, and neither does this harness: the breaks are listed on the reconciliation extract, which the data steward and the ACE team read as a file. The states the harness asserts on that extract are small.
SCR-45 is not built or changed by this story; its loading state is taken from Screen Specifications v1 section SCR-45, and its empty, error and no-access states are Not specified in the source documents (DOR-RWB-ITG-DM013-ITG-10).

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of proceeds rows, closed cases and write-off decisions, and no break row |
| Break | One row per orphan with the case number, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. The SCR-45 Data quality console is not part of this legacy key: it is the screen of RWB-AD-019 and this story neither builds it nor reads it. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0453; ASM-0645).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-013-01-ITG | AC4 (legacy AC1); ITG AC4 | Integration | The closed case, the write-off decision and the proceeds row with their dates |
| TC-DM-013-02-ITG | AC1 (legacy); ITG AC1, ITG AC2 | Integration | The proceeds row with payment_code PAY-SYN-000913; the rwb-source-data stub returns no DP13 payment row for it (§12.8) |
| TC-DM-013-03-ITG | AC2 (legacy, owned by RWB-P1-DM013-APP); ITG AC3 | Integration | Two readiness calls for one business date |
| TC-DM-013-04-ITG | Access; ITG AC5 | Component | RW-OFF caller without Platform administration R |
| TC-DM-013-05-ITG | AC6 (BR3, BR7, BR9) | Not specified in the source documents (NEWAC-RWB-ITG-DM013-ITG-AC6) | One migrated record with an unresolved business key; the cutover record |
| TC-DM-013-06-ITG | AC7 | Not specified in the source documents (NEWAC-RWB-ITG-DM013-ITG-AC7) | A consumed contract that fails or gives no answer for business date 2026-11-30 |
| TC-DM-013-02-ITG, TC-DM-013-07-ITG, TC-DM-013-03-ITG, TC-DM-013-01-ITG, TC-DM-013-04-ITG, TC-DM-013-05-ITG, TC-DM-013-06-ITG, TC-DM-013-08-ITG | New ITG AC8 and the changed assertions of ITG AC1 to AC7 | Integration | Values of section 7 |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic keys, the dates, the amounts, the business date, the fixture contents, the break reasons and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the closure comes from rwb-case, the proceeds from rwb-payment, the write-off decision from rwb-writeoff, and the ACE side only through the rwb-source-data DP13 contract (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-013 Migrate money and closure | Recovery Workbench Data Migration Stories v4, lines 882 to 963 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 907 to 911 | Section 7, AC1, marked (legacy RWB-DM-013 AC2) |
| Legacy AC1 and AC3, and the four legacy test cases TC-DM-013-01 to TC-DM-013-04 | The same, lines 901 to 918 and 955 to 960 | AC1 and AC3 stay with RWB-P1-DM013-APP and RWB-P8-DM013-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-CAS-022, DF-CAS-023, DF-FIN-001 to DF-FIN-009, DF-FIN-010 to DF-FIN-020, DF-ACE-043 to DF-ACE-054, DF-ACE-261 to DF-ACE-269 | Logical Data Model and Data Dictionary v9 | Section 11 |
| REQ-RDF-007 and REQ-RDF-008, the daily reconciliation and the reported breaks | Business Requirements Program v5, lines 120 and 121 | Section 8, BR1 to BR3 and BR8 |
| REQ-RDF-013 and NFR-031, retention and archive by record class | Business Requirements Program v5, lines 126 and 508 | Section 8, BR9 |
| NFR-018, the daily reconciliation to the ACE account view | Business Requirements Program v5, line 482 | Section 8, BR3 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 and BR6 |
| D-RCV-35 and ADR-010, ACE data only through the views and never copied | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR5; sections 12.2 and 12.8 |
| DP13 Money and closure, ACE from ALS and GL, daily at 08:00 | FSD P1 Recovery data engine v3, line 295 | Sections 11 and 12.2 |
| RWB-E1-011 Reconciliation and data quality report | Epic 1 story master; Build Notes Epic 1 v7 | Section 12.5, the JOB-04 reconciliation this harness exercises; its build and its screen RWB-AD-019 are out of scope |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM013-APP and RWB-P8-DM013-APP: their criteria, the extract with its key resolution and the proceeds match. The reconciliation is JOB-04 of RWB-P1-E1011-APP (RD-P1-022). The cutover loads of the records are each owning service's own Flyway sequence.
- P1 and P8 production code and their CON, APP and DB stories: the data-product contract, the case contract, the proceeds tables and the reconciliation are built there.
- The SCR-45 Data quality console (RWB-AD-019).
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration.
- The other data migration keys of the wave.

### 20. Remaining delivery steps

- Size the story (RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish the rwb-source-data 5.1.0 fake and add the reconciliation result reads to the yaml file (rwb-source-data contract owner).
- Settle the break-detail store (rwb-source-data data architect; GAP-1508, NEW-GAP-S2B-03).
- Publish a read of the write-off decision (rwb-writeoff contract owner; NEW-GAP-F07-02).
- Add the authorise path to the rwb-access yaml (rwb-access contract owner).
- Provide the stubs and synthetic fixtures in DEV (integration lead).
- Add the new and changed test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).
