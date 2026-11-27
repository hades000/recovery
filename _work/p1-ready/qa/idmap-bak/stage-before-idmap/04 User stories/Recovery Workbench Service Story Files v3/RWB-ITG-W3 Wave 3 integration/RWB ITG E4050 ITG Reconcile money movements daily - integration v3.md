# RWB-ITG-E4050-ITG Reconcile money movements daily

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- JOB-04 is `ReconciliationWorkflow` (`recon-{businessDate}`), a child of `AceIngestCheck` after the ALS stamp; `AceDataReady` does not start it, and the job rerun serves only a FAILED run (RD-P1-002, RD-P1-012, RD-P1-040; findings 1 and 2, new AC9 and AC10).
- P1 reconciliation covers REC-01, REC-02 and REC-05; REC-04 and REC-06 have no owner yet and are marked pending (finding 3).
- The batch record is read through the freshness answer and `AceDataReady`; the record read needs the case UUID; the result read is named (RD-P1-003, RD-P1-005, RD-P1-041; findings 4 and 5).
- Decision record content, contract version and dependencies updated (findings 6 and 7). Remaining delivery steps are in section 20.
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- REC-04 and REC-06 belong to the rwb-payment daily reconciliation and the batch record fields come from `getBatchStatus` (RD-P1-069); no completed run is rerun (RD-P1-065).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E4050-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-050 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E4050-ITG-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E4050-ITG-14) |
| Depends on (build) | RWB-P8-E4050-APP (build not done; the Day-1 run uses the fakes of section 12.8) |
| Contract dependencies | RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P1-AD018-CON; others: Not specified in the source documents (DOR-RWB-ITG-E4050-ITG-21) |
| Contract version | /v1; rwb-source-data: rwb-source-data.yaml 5.1.0 and asyncapi/rwb-source-data.asyncapi.yaml (API Specification v7); other services: not specified in the source documents (DOR-RWB-ITG-E4050-ITG-23) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-ITG-E4050-ITG-22) |
| Integration dependencies | RWB-P8-E4050-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-002, RD-P1-003, RD-P1-005, RD-P1-012, RD-P1-040, RD-P1-041, RD-P1-065, RD-P1-069 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-050 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E4050-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a role not specified in the source documents (DOR-RWB-ITG-E4050-ITG-1), I want **one repeatable cross-service harness that takes a seeded account with three payments in `v_ace_payment` and one posting in `v_ace_write_off` at one ACE batch date, drives the daily reconciliation step through the service that owns it, and proves that every payment is matched to the proceeds on its case, every posting is matched to the approved write-off, every unresolved `account_key` and `payment_code` is listed, and the outcome is on record with the rule version, against the owning services' published contracts and their fakes**, so that **the daily money position can be shown to reconcile before anyone reads it, a break is shown to be listed for the data steward and not hidden, and no reconciliation is ever computed by the harness on a rule that lives in code**.

### 2. Business rationale

A daily reconciliation that a person cannot reproduce is a number nobody can defend. The bank reconciles what it has matched against what ACE holds, and the legacy key states the work in four moves: REC-04 matches the payments in `v_ace_payment` to the proceeds matched to the case, REC-06 matches the posting in `v_ace_write_off` to the approved write-off, REC-05 lists every `account_key` and `payment_code` that does not resolve in the view, and the outcome is written to `reconciliation_result` by `rec_code` and business date (legacy RWB-E4-050 AC1; D-RCV-35 U4). None of those four moves belongs to the harness. Every one of them belongs to a service that already owns the data and the rule behind it, and the harness exists to prove that the four moves agree across those services on one business date.

The ownership is the substance of this story, and it moves under the legacy key. The legacy story sits in module P8 Payments and posting and says the work runs inside the recovery module, so it wrote `reconciliation_result` where the P8 code lived. In the Ownership Map the table is P1 rwb-source-data's: the map records `reconciliation_result` under P1 on Architecture v5 slide 41, where rwb-source-data owns the ACE view contract, the extension tables, the freshness and the reconciliation, and on slide 44, where JOB-04 Reconciliation is a workflow of rwb-source-data, started by `AceIngestCheck` after the ALS stamp (RD-P1-040). The proceeds and the payment and proceeds matching stay with P8 rwb-payment in `rwb_payment`; the approved write-off stays with S7 rwb-writeoff in `rwb_writeoff`; the record and the rule rows stay with P7 rwb-decision; the role, scope and DoA data stay with P4 rwb-access; and the three ACE views stay ACE's, read through P1's data product. The harness therefore reads `reconciliation_result` through the owner's contract and never as a table, and it computes no reconciliation of its own: it triggers the owner's step and asserts the result the owner wrote. That position is carried as a gap and an assumption (GAP-0434; ASM-0611).

The harness is decoupled the same way the services are, and it serves the same three requirements the loop already serves. It owns no schema and reads no other service's table (DP-01): the ACE position comes from rwb-source-data's data product, the proceeds and the match from rwb-payment, the case from rwb-case, the approved write-off from rwb-writeoff, the record from rwb-decision and the authority from rwb-access. It reads `v_ace_payment`, `v_ace_write_off` and `v_ace_batch_status` through rwb-source-data's contract and never through a view of its own (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). It calls each owner's base `/api/recovery/<short>/v1`, one hop per call with a 2 s timeout and a circuit breaker per downstream, and it calls the gateway-bff composite route where a screen would (DP-19). It carries REQ-CHO-009 and REQ-RDF-007 into evidence, reports the breaks REQ-RDF-008 asks to be reported, and proves the record REQ-DRI-001 requires, on the completeness duty the write-off posting carries in REQ-S7-005.

### 3. Preconditions

- The published contracts of rwb-source-data, rwb-payment, rwb-case, rwb-writeoff, rwb-decision and rwb-access are in the contract registry, and a stub set is generated from each published OpenAPI or AsyncAPI document with its version pinned.
- An account `A-0001` with three payments in `v_ace_payment` and one posting in `v_ace_write_off` is present at the ACE batch date 2026-12-14, and the case that holds the matching proceeds and the approved write-off is seeded through the owning services' published operations only. The seeding set, the harness environment specification and the fixture contents are not specified in the source documents (GAP-0434; ASM-0610).
- The ACE batch record for 2026-12-14 is present in `v_ace_batch_status` with its `business_date`, `status`, `record_count`, `checksum` and `is_complete` held by ACE (published as `status`, `isComplete`, `recordCount` and `checksum` by `GET /batch-status` for the rwb-payment and rwb-integration workload identities, RD-P1-066 and RD-P1-069; `status` and the business date also show in the freshness answer and `AceDataReady`), because the business date the run is keyed by is the one that record carries and not a date in the script (legacy RWB-E4-050; DF-ACE-178 to DF-ACE-186).
- The data product code that serves the `v_ace_payment`, `v_ace_write_off` and `v_ace_batch_status` rows through the source-data products operation is not specified in the source documents (GAP-0434; ASM-0610).
- The `reconciliation_result` rows are read through `GET /admin/reconciliation/results` (RWB-P1-E1011-CON); the harness triggers the step through the ready call and asserts the outcome through that read and the JOB-04 run.
- The operation in rwb-writeoff that reads the approved write-off on the case, and the field names that carry its amount and its approval, are not specified in the source documents (GAP-0434; ASM-0612).
- The rule set that carries REC-04, REC-05 and REC-06 as the owner evaluates them is in force in the service that runs the step, and the rule ID and the rule version of each are readable on the decision record that cites them. REC-04 and REC-06 are named only in the legacy key and no rule set read in this WP defines them (GAP-0434; ASM-0610).
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the roles that hold the case record R and for a caller whose role does not include the right.
- The harness test identity holds Platform administration R and U for the job reads, the ready call and the rerun, and Case record R for the record reads.
- No build dependency; the contract dependencies are those of the header. Day 1, with the fakes of section 12.8 in place from the first run, and the rwb-payment fake replaced by the real service when RWB-P8-E4050-APP lands.

### 4. Flow

1. Harness: seeds the case, the proceeds matched to it, the approved write-off and the one posting it must reconcile against, through the owning services' published operations only; the seeding set and its environment are not specified in the source documents (GAP-0434; ASM-0610).
2. Harness: pins the business date the run is keyed by from the owner's published facts: `GET /api/recovery/source-data/v1/data-products/freshness` with `status` LOADED and `businessDate` 2026-12-14, and the `AceDataReady` event keyed `ALS:2026-12-14` with `status` COMPLETED (legacy RWB-E4-050). The record count, checksum and completeness of the ACE batch record are the `recordCount`, `checksum` and `isComplete` of `getBatchStatus` (RD-P1-069 rule 2).
3. Harness: reads the three payments of `A-0001` in `v_ace_payment` through `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId=` (the case UUID; the product code is not specified in the source documents, GAP-0434; ASM-0610) and asserts the `payment_code` list, the `account_key`, the `payment_date` and the `payment_amount` of each, so the source side of REC-04 is the ACE position for 2026-12-14 and not a row in the script (DP-05; DF-ACE-043 to DF-ACE-054).
4. Harness: reads the one posting in `v_ace_write_off` for `A-0001` and asserts `write_off_key`, `amount`, `posted_date` and `responsibility_center`, so the source side of REC-06 is the ACE posting and not a figure copied into the harness (DF-ACE-261 to DF-ACE-269).
5. Harness: reads the Workbench side through the owners' contracts: the case identity through `GET /api/recovery/case/v1/cases/{caseId}`, the proceeds matched to the case through `GET /api/recovery/payment/v1/proceeds`, the payments and bookings on the case through `GET /api/recovery/payment/v1/cases/{caseId}/payments`, and the approved write-off through the rwb-writeoff contract (legacy RWB-E4-050; DF-FIN-001 to DF-FIN-009, DF-FIN-010 to DF-FIN-020; GAP-0434; ASM-0612).
6. Harness: triggers the readiness run of the business date with `POST /api/recovery/source-data/v1/business-days/2026-12-14/ready` and a new `Idempotency-Key` (202). `AceIngestCheck` stamps the ALS batch and starts `ReconciliationWorkflow` (`recon-2026-12-14`, job type JOB-04) as its child, so the reconciliation is computed by the service that owns it and never by the harness. The job rerun is used only on a FAILED run, by its run ID (AC10).
7. Harness: reads the owner's job record through `GET /api/recovery/source-data/v1/admin/jobs?type=JOB-04&from=2026-12-14&to=2026-12-14` (one item per run; `status` COMPLETE; `checks` keyed REC-01, REC-02 and REC-05) and asserts that the run for the business date completed, with the business date the batch record carried in step 2 and no other (legacy RWB-E4-050; REQ-RDF-008).
8. Harness (blocked, NEW-GAP-F05-5): asserts REC-04 on the outcome: every `payment_code` read in step 3 resolves to a proceeds row on the case read in step 5, the count the owner recorded for REC-04 agrees with the source count, and nothing is left unmatched (legacy RWB-E4-050 AC1; REQ-CHO-009).
9. Harness (blocked, NEW-GAP-F05-5): asserts REC-06 on the outcome: the `write_off_key` read in step 4 resolves to the approved write-off on the case read in step 5, the amount and the posting date agree with the posting, and the count the owner recorded for REC-06 agrees with the source count (legacy RWB-E4-050 AC1; REQ-S7-005).
10. Harness: asserts REC-05 on the same outcome: every `account_key` and `payment_code` read in steps 3 and 4 resolves in its view, and where one does not, the key is listed with the reason the owner gives it, as a break for the data steward and not as a silent exclusion (legacy RWB-E4-050 AC1; REQ-RDF-007; REQ-RDF-008).
11. Harness: asserts that the outcome is recorded "by rec_code and business date" as AC1 states it, by reading the owner's result for each `rec_code` the run exercised against the one business date through `GET /api/recovery/source-data/v1/admin/reconciliation/results` (filters `recCode`, `from`, `to`; `result` PASS or BREAK), never as a table (legacy RWB-E4-050 AC1; DF-OPS-118 to DF-OPS-129; ASM-0611).
12. Harness: reads `GET /api/recovery/decision/v1/decision-log` and asserts exactly one record for the reconciliation step, carrying the business date, the check codes, the result indicators, the counts and the orphan count and no account number or name (RWB-P1-E1011-APP); the rule ID and rule version of REC-04 and REC-06 follow NEW-GAP-F05-5 (REQ-DRI-001).
13. Harness: subscribes to `rwb.source-data.events.v1`, `rwb.payment.events.v1`, `rwb.writeoff.events.v1` and `rwb.decision-record.v1` and asserts `AceDataReady` keyed `ALS:2026-12-14` for the business date, one `ProceedsMatched` per payment matched, one `WriteOffApproved` for the write-off reconciled, and `DecisionRecorded` for the record, reaching the ledger within 5 minutes, each with no personal data on it (DP-03).
14. Harness: repeats the ready call for the same business date with a new `Idempotency-Key` (unchanged batch rows commit no stamp, so no second reconciliation run starts) and asserts that the second run adds no second match, no second result and no second record, and records the idempotency hit instead (R-UNI-40).
15. Harness: repeats the run with the decision record forced to fail and asserts that nothing moves: no match, no result row, no case change, and the message the owner returns. This is the negative path of AC2, whose criterion belongs to RWB-P8-E4050-APP.
16. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a role that does not include the right.
17. Harness: publishes one evidence report per story and business date, naming the criterion, the assertions, the contract versions, the business date the ACE batch record carried and whether each hop was a stub or the owner. The evidence format and its retention are not specified in the source documents (GAP-0434; ASM-0610).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The freshness answer is STALE or has no `businessDate` for the date the run was seeded with, or no `AceDataReady` for `ALS` with COMPLETED arrives | The run fails on AC1 before any reconciliation and the report names the batch record it looked for | None | AC1, BR4 |
| X3 | The three payments read from `v_ace_payment` do not carry the `payment_code` list, the `account_key` or the amounts the case was seeded with | The run fails on AC1 and the report names the payment row and what it found | None | AC1 |
| X4 | The posting read from `v_ace_write_off` does not carry the `write_off_key`, the amount or the posting date the case was seeded with | The run fails on AC1 and the report names the posting and what it found | None | AC1 |
| X5 | The owner's reconciliation step for the business date did not complete | The run fails on AC1 and the report names the job record, its status and the business date it covered | None | AC1 |
| X6 | REC-04 leaves a payment in `v_ace_payment` unmatched to the proceeds on the case, and the owner recorded no break for it | The run fails on AC1 and the report names the `payment_code` and the proceeds it compared | None | AC1, BR1 |
| X7 | REC-06 leaves the posting unmatched to the approved write-off, and the owner recorded no break for it | The run fails on AC1 and the report names the `write_off_key` and the write-off it compared | None | AC1, BR2 |
| X8 | REC-05 does not list an `account_key` or a `payment_code` that does not resolve in its view, or lists it with no reason | The run fails on the REC-05 assertion and the report names the orphan key and its view | None | AC1, BR3 |
| X9 | The outcome is not recorded by `rec_code` and business date, or the business date on the result is not the one the batch record carried | The run fails on AC1 and the report names the result rows it found and their business date | None | AC1, BR5 |
| X10 | More than one record exists for the reconciliation step, or its rule ID or rule version is missing | The run fails on AC1 and the report names the records it found | None | AC1, BR6 |
| X11 | The record does not reach `rwb.decision-record.v1` inside 5 minutes | The run fails on AC1 and the report names the record and its arrival time | None | AC1 |
| X12 | The run is repeated for the same business date and a second match, a second result row or a second record appears | The run fails on the repeatability assertion and the report names what doubled | None | AC3, BR7 |
| X13 | The decision record is forced to fail but a match, a result row or a case change still moves | The run fails on the negative path and the report names what moved | MSG-P7-003 | AC2 path, BR8 |
| X14 | A role that does not include the right is authorised, or a caller outside the case scope passes | The run fails on the access check and the report names the operation | MSG-P4-002 | AC5, TC-E4-050-03-ITG |
| X15 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. Screen SCR-28's empty, loading, error and no-access states are Not specified in the source documents (DOR-RWB-ITG-E4050-ITG-10); the no-access outcome is asserted by AC5 and X14. REC-04, REC-05 and REC-06 carry no message ID in the rule set read, so the harness asserts the match, the break list, the result row and the decision record, and names a message ID only where an owning service returns one of the three in section 14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-P8-E4050-APP |
| Negotiable | The seeding set, the report shape, the evidence retention and the composite route are configuration agreed at the wave entry check, not business values in code; the business date is the ACE batch record's and never configuration |
| Valuable | The four reconciliation moves, the break list and their record are proven end to end before wave 3 opens |
| Estimable | One harness runner, one stub set, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-P8-E4050-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Reconcile money movements daily

  Background:
    Given the seeded account "A-0001" carries three payments and one posting at the ACE batch date 2026-12-14, served by the rwb-source-data contract fake of section 12.8
    And the contract fakes of section 12.8 are published with their versions pinned

  Scenario: AC1 Reconcile money movements daily (legacy RWB-E4-050 AC1)
    Given the payments and the posting are read through the rwb-source-data contract (DP-01, DP-05), and the rwb-source-data contract fake returns three payments for account "A-0001" at the ACE batch date 2026-12-14 and one posting for it
    When the daily reconciliation runs
    # REC-04 and REC-06 are computed by the daily reconciliation of rwb-payment into rwb_payment (RD-P1-069 rule 2). Pending: the published read of their results, owner rwb-payment contract owner, tracked as NEW-GAP-F05-5. Break and orphan detail is pending, so counts are asserted (GAP-1508, RD-P1-069 rule 1)
    Then REC-04 matches the payments in v_ace_payment to the proceeds matched to the case
    Then REC-06 matches the posting in v_ace_write_off to the approved write-off, and REC-05 lists every account_key and payment_code that does not resolve
    Then the outcome is written to reconciliation_result by rec_code and business date
    Then the system writes the result to the decision log with the rule version

  Scenario: AC3 Reconcile money movements daily twice for one business date (new, D-RCV-60)
    Given the reconciliation for the business date 2026-12-14 has completed and one record exists for the step
    When the harness posts /business-days/2026-12-14/ready again with a new Idempotency-Key
    Then GET /admin/jobs with type "JOB-04" for 2026-12-14 still answers one run
    And no second proceeds match, no second reconciliation_result row and no second record appears
    And every read and every call in both runs went to an owner's published operation, one hop per call, with no read of any table

  Scenario: AC4 Reconcile money movements daily with one evidence report (new, D-RCV-60)
    Given the run has completed against the fakes of section 12.8
    When the evidence report is written for the story and the business date
    Then it names each criterion and each assertion, the contract version of every hop, the business date the ACE batch record carried, and whether each hop was a stub or the owner
    And a stub pass is never reported as a real-service pass

  Scenario: AC5 A role without the right, or a caller outside the case scope, is refused (new, D-RCV-60)
    Given the rwb-access contract fake of section 12.8 is published with its version pinned
    When a role that does not include the right, or a caller outside the case scope, calls an operation of section 4
    Then the call is refused at POST /api/recovery/access/v1/authorise and the report names the operation
    And the message MSG-P4-002 is returned

  Scenario: AC6 A repeated event with the same key is ignored, and a payment with no plan, settlement or fee goes to the exception list (new, D-RCV-60)
    Given the reconciliation for the business date 2026-12-14 has completed
    When the same event arrives a second time with the same key
    Then the second event is ignored and the idempotency hit is recorded
    And no second rwb-source-data reconciliation run starts, because rwb-source-data does not consume "rwb.source-data.events.v1"
    And each payment that does not match a plan, a settlement or a fee by its payment_code is listed on the exception list

  Scenario: AC7 A consumed call that fails or does not answer stops the run and nothing moves (new, D-RCV-60)
    Given the contract fake of section 12.8 for one consumed call is set to fail or not to answer
    When the daily reconciliation runs
    Then the run fails at that hop, the report names the service, the operation and the contract version, and no result row or decision record is written

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case whose model does not allow the status change requested
    When the status change is requested for the case
    Then the change is refused, nothing moves and the report names the operation

  Scenario: AC9 The reconciliation is one JOB-04 run started after the ALS stamp (new, RD-P1-040, RD-P1-012)
    Given the ALS batch of 2026-12-14 is COMPLETED and not yet stamped
    When the harness posts /business-days/2026-12-14/ready with a new Idempotency-Key
    Then the answer is status 202 with businessDate 2026-12-14
    And GET /admin/jobs with type "JOB-04", from 2026-12-14 and to 2026-12-14 answers one run with workflowId "recon-2026-12-14", status "COMPLETE" and checks keyed REC-01, REC-02 and REC-05, each with expected, actual and passed

  Scenario: AC10 Only a failed reconciliation run is rerun (new, RD-P1-012)
    Given the reconciliation run of 2026-12-14 has status "FAILED" and the cause is removed
    When the harness posts /admin/jobs/{jobId}/rerun with that run ID, no body and a new Idempotency-Key
    Then the answer is status 202 with a job of type "JOB-04", status "PENDING" and runNo 2
    And after it ends COMPLETE, a rerun of that run with another Idempotency-Key answers 409 MSG-P1-011
```

AC2 of the legacy key ("Not recorded", the refusal when the decision log cannot be written) is owned by RWB-P8-E4050-APP and is not restated here; the harness exercises it only as the negative path of the same loop, in step 15 of section 4 and in TC-E4-050-02-ITG. AC9 and AC10 were added in version 3 (TC-E4-050-09-ITG, TC-E4-050-10-ITG). AC3 and AC4 are the harness-only criteria new to D-RCV-60: they test repeatability, the one-hop read discipline and the evidence report, and add no business value of their own.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | REC-04 matches the payments in `v_ace_payment` to the proceeds matched to the case | Legacy RWB-E4-050 AC1; REC-04 as the legacy key names it |
| BR2 | REC-06 matches the posting in `v_ace_write_off` to the approved write-off, and the posting's amount and date agree with it | Legacy RWB-E4-050 AC1; REC-06 as the legacy key names it; REQ-S7-005 |
| BR3 | REC-05 lists every `account_key` and `payment_code` that does not resolve in its view, with a reason for the data steward, and never deletes or changes a Workbench record | Legacy RWB-E4-050 AC1; REC-05; REQ-RDF-007; REQ-RDF-008 |
| BR4 | The business date the reconciliation runs for is the one the ACE batch record carries in `v_ace_batch_status`, seen through the freshness answer and `AceDataReady`; a missing or incomplete batch record is not reconciled against a guessed date | Legacy RWB-E4-050 story; DF-ACE-178 to DF-ACE-186; Architecture v5 slide 15 (freshness of the ACE position); Ownership Map JOB-04 |
| BR5 | The outcome is written to `reconciliation_result` by `rec_code` and business date, and the table is P1 rwb-source-data's | Legacy RWB-E4-050 AC1; Ownership Map `reconciliation_result` owner P1 |
| BR6 | The result is written to the decision record with the rule ID and the rule version of each rule the step fired, with the change, in one transaction | Legacy RWB-E4-050 AC1; REQ-DRI-001; R-UNI-39 |
| BR7 | The same event arrives twice with the same key is ignored and the idempotency hit recorded, so a repeated run for one business date adds no second result | R-UNI-40 |
| BR8 | No reconciliation action proceeds if its record cannot be written; the action is blocked and an incident raised | R-UNI-39 |
| BR9 | Payments are matched to the plan, the settlement or the fee they belong to by the ACE `payment_code`, and anything unmatched goes to an exception list | REQ-CHO-009 |

REC-04 and REC-06 are named only in the legacy key: no rule set read in this WP defines them, and the rule package that carries them is not named either (GAP-0434; ASM-0610). REC-05 is P1's reconciliation duty over the ACE views. The harness holds no copy of any of the three and asserts them through the owner that evaluates them.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Idle | `AceIngestCheck` commits the ALS stamp of the business date, or an admin rerun of a FAILED run | the ALS batch for the date is COMPLETED | Loading, the JOB-04 reconciliation step runs in rwb-source-data |
| Loading | REC-04 and REC-06 resolve every payment and every posting | every `payment_code` finds its proceeds and the `write_off_key` finds its approved write-off | matched (SCR-28), with the outcome recorded by `rec_code` and business date |
| Loading | REC-05 finds an `account_key` or a `payment_code` with no row in its view | any orphan key | unmatched (SCR-28), with the key and its reason listed as a break |
| unmatched | the step is run again for the same business date after the cause is fixed (by the next daily run: a COMPLETE run is not rerun, RD-P1-065) | the orphan resolves | matched (SCR-28), with the earlier break kept on record |

These are the owner's states and the screen's states, not the harness's: rwb-source-data runs the reconciliation step and writes `reconciliation_result` in its own schema, rwb-payment holds the proceeds and the match, and rwb-writeoff holds the approved write-off (ASM-0611). The harness changes none of them itself. It seeds through the owning services' published operations, triggers the owner's step through the ready call, and then asserts the state the owner reached, naming the owner and the operation behind each move in the report. A state the harness set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and the further roles that hold the case record R | Read the run evidence for their case: the payments, the proceeds, the write-off posting, the break list and the record |
| QA lead | Owns the harness configuration, the seeding set, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| Data steward (role, not a person) | Receives the REC-05 breaks the run proves are listed, and is the second owner of a key that has no row in ACE |
| The owning services' identities | rwb-source-data, rwb-payment, rwb-case, rwb-writeoff, rwb-decision and rwb-access make every change the harness asserts |
| No approval level from the delegation of authority applies to the harness | The harness takes no business decision; the reconciliation duty and any tolerance behind it belong to the owner of the step and to the data product owner |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code | Read, through the rwb-case contract |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | source_system, business_date, status, record_count, checksum, is_complete | `business_date` and `status` are seen through the freshness read and `AceDataReady`; `record_count`, `checksum` and `is_complete` through `getBatchStatus` (RD-P1-069 rule 2) |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount | Read, through the rwb-source-data data product (DP-05) |
| DF-ACE-261 to DF-ACE-269 | v_ace_write_off | write_off_key, account_key, amount, posted_date, responsibility_center, gl_product | Read, through the rwb-source-data data product (DP-05) |
| DF-FIN-001 to DF-FIN-009 | proceeds | id, case_id, treatment_id, payment_code, source, amount | Read, through the rwb-payment contract |
| DF-FIN-010 to DF-FIN-020 | write_off | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date | Read, through the rwb-writeoff contract |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | id, rec_code, business_date, product_group, source_count, workbench_count | Read through `GET /admin/reconciliation/results` (RWB-P1-E1011-CON) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. Reference data: the run reads the decision rule rows (DF-REF-001 to DF-REF-015) through the rwb-decision contract, under the reference-data contract (DP-06, DP-07); the parameter names and the reference-data contract version are not specified in the source documents (DOR-RWB-ITG-E4050-ITG-20). `v_ace_account` (DF-ACE-001 to DF-ACE-042) is in the legacy data table but is not read by this run, because the reconciliation the story owns is over payments, postings and their matches. The test data of section 7 is served by the rwb-source-data contract fake of section 12.8 and is not written to any ACE view. The harness owns no table and writes no row directly: every read and every seed goes through the API of the owning service (DP-01, DP-05), and the three ACE views are ACE's, so the Workbench holds no payment or posting copy (legacy RWB-E4-050; D-RCV-35 U4).

`reconciliation_result` is the row this story turns on, and it is P1 rwb-source-data's in the Ownership Map, while the legacy key wrote it inside the P8 module. The harness therefore reads it through the owner's contract and never as a table, and it computes no reconciliation itself: it drives the owner's step and asserts the result the owner wrote. The operation that reads the row and the result codes it carries are not named by any source read in this WP (GAP-0434; ASM-0611). The approved write-off row (DF-FIN-010 to DF-FIN-020) is read through the rwb-writeoff contract, whose read operation and field names are likewise unnamed, so the harness asserts REC-06 on the key, the amount and the approval that contract returns and reads no `rwb_writeoff` table (GAP-0434; ASM-0612).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Rerun a FAILED JOB-04 run by run ID: no body, `Idempotency-Key`, 202; 409 MSG-P1-011 or MSG-P1-001 (AC10) |
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Trigger `AceIngestCheck`, which starts the reconciliation after the ALS stamp; 202 with `businessDate` and `status` (AC3, AC9) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | Result rows by `recCode`, `product`, `result`, `from`, `to` (RWB-P1-E1011-CON; AC1) |
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | The JOB-04 runs of the business date: `status`, `workflowId`, `runNo`, `checks` keyed REC-01, REC-02, REC-05 (AC1, AC9) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The `v_ace_payment` and `v_ace_write_off` rows of a case: `caseId` (UUID) required, rows as `fields` (AC1, DP-05) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The business date the ACE position is complete for: `status` LOADED or STALE, `businessDate`, `staleSince` (AC1) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The proceeds matched to the case (AC1, REC-04) |
| POST | `/api/recovery/payment/v1/proceeds/{proceedsId}/match` | P8 rwb-payment | The match the Workbench side of REC-04 is asserted against (AC1) |
| GET | `/api/recovery/payment/v1/cases/{caseId}/payments` | P8 rwb-payment | The payments and bookings on the case; Architecture v5 slide 17 names this path for rwb-payment (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case identity the proceeds and the write-off belong to (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record with the rule ID and the rule version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope, including the refusal path (AC1) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream. Where a screen would compose them, the harness calls the gateway-bff composite route (DP-19).

Three names are not given by any source read in this WP and are not invented here. The `{productCode}` that carries the three ACE views is left as a path variable (GAP-0434; ASM-0610). The result rows of REC-01 and REC-02 are read from `GET /admin/reconciliation/results`; the REC-05 orphan count is on the run (its detail store is pending in RWB-P1-E1011-CON). REC-04 and REC-06 are computed by the daily reconciliation of rwb-payment (RWB-P8-E4050-APP) into `rwb_payment`; `ReconciliationWorkflow` writes REC-01, REC-02 and REC-05 only (RD-P1-069 rule 2). Pending: the published read of the REC-04 and REC-06 results, owner rwb-payment contract owner, tracked as NEW-GAP-F05-5. The read of the approved write-off on the case is through the rwb-writeoff contract, whose read operation and field names are likewise unnamed (GAP-0434; ASM-0612). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it triggers the reconciliation through the rwb-source-data ready call and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 rwb-source-data | Key `{sourceSystem}:{businessDate}`, data `sourceSystem`, `businessDate`, `status`, `completedAt`; the run uses `ALS` with COMPLETED. The event starts nothing inside rwb-source-data (AC1, AC6, BR4) |
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | P8 rwb-payment | One match per payment, matching the REC-04 count for the business date (AC1) |
| `rwb.writeoff.WriteOffApproved.v1` (EV-24) | `rwb.writeoff.events.v1` | S7 rwb-writeoff | The approved write-off the posting in `v_ace_write_off` is matched against (AC1, REC-06) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | every service, through its own local decision-record library | The record written with the reconciliation reaching the ledger within 5 minutes (AC1, DP-03) |

All four carry IDs and business facts only (`AceDataReady` keyed `{sourceSystem}:{businessDate}`, the others by caseId or payment code), and the harness asserts that no personal data is present. The catalogue names each event and the topic names it, while the versioned event name in the form `rwb.<short>.<Event>.v1` is read from the service's published AsyncAPI document, which is the contract the stub is generated from (GAP-0434; ASM-0610).

#### 12.5 Workflows and activities

None added. The harness exercises `ReconciliationWorkflow` (`recon-{businessDate}`, one activity `reconciliation`) of rwb-source-data, started by `AceIngestCheck` as a child workflow (ParentClosePolicy ABANDON) after the ALS stamp, and the `matchPayments` and `confirmBookings` activities on queue rwb-payment (JOB-07 and JOB-08) that produce the proceeds match REC-04 is asserted against. It asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. JOB-04 is a child workflow of `AceIngestCheck` and not a Temporal Schedule of its own, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). `reconciliation_result` is P1 rwb-source-data's; the proceeds and the payment and proceeds matching are P8 rwb-payment's; `write_off` is S7 rwb-writeoff's; `decision_log_entry` and `rule_row` are P7 rwb-decision's; the role, scope and DoA data are P4 rwb-access's; the case is P3 rwb-case's; and `v_ace_payment`, `v_ace_write_off` and `v_ace_batch_status` are ACE's, read through rwb-source-data's contract (DP-05). The legacy key wrote `reconciliation_result` inside the P8 module; the Ownership Map moves it to P1, so the harness reads it through the owner's contract and never as a table (GAP-0434; ASM-0611).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-source-data | `POST /business-days/{date}/ready`, `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, `GET /admin/reconciliation/results`, `GET /data-products/{productCode}/records`, `GET /data-products/freshness`, `rwb.source-data.events.v1` | Day-1 run of AC1, AC3 and AC4: the ACE position, the business date, the owner's step and its job record |
| Stub for rwb-payment | `POST /proceeds/{proceedsId}/match`, `GET /proceeds`, `GET /cases/{caseId}/payments`, `rwb.payment.events.v1` | Day-1 assertion of the proceeds and the match REC-04 is measured against, before RWB-P8-E4050-APP is live |
| Stub for rwb-writeoff | The read of the approved write-off on the case, `rwb.writeoff.events.v1` | Day-1 assertion of the approved write-off REC-06 is measured against; the operation is not named by a source read (ASM-0612) |
| Stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertion of the case identity the money movements belong to |
| Stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record for the step with its rule versions |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| AceDataReady event stub | `rwb.source-data.AceDataReady.v1` | The ready signal of the business date (key `ALS:2026-12-14`), where the environment does not run the source-data step |
| ProceedsMatched event stub | `rwb.payment.ProceedsMatched.v1` | The match per payment, where the environment does not run the payment match |
| DecisionRecorded event stub | `rwb.decision.DecisionRecorded.v1` | The 5-minute arrival assertion of the record |

Each fake is generated from the published OpenAPI or AsyncAPI document of its service, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The data product code, the write-off read operation and its field names, the harness environment, the seeding set and the evidence format are not specified in the source documents (GAP-0434; ASM-0610; ASM-0612). The harness environment, the seeding set and its seeded identifiers, the business date and ACE batch for the journey, the product codes, the three unnamed operations, the evidence format and the gate thresholds are to be agreed at the wave 3 entry check with the integration and QA leads (GAP-0436).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 12 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s timeout and a circuit breaker per downstream, composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `AceDataReady`, `ProceedsMatched`, `WriteOffApproved` and `DecisionRecorded` consumed (DP-03) |
| Temporal | Exercised only: the rwb-source-data `ReconciliationWorkflow` (JOB-04), a child of `AceIngestCheck`, and the `matchPayments` and `confirmBookings` activities on queue rwb-payment (JOB-07, JOB-08); none added |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependency is the one I story, RWB-P8-E4050-APP: until it is live the run uses the rwb-payment stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour, and it changes one thing. The legacy key states no endpoint, says the work runs inside the recovery module, and writes `reconciliation_result` in the P8 module. In the target the reconciliation step and its result row belong to P1 rwb-source-data (Ownership Map; Architecture v5 slides 41 and 44), so the step is the owner's workflow and not something the harness computes, and the result is read through the owner's contract and never as a table. The harness owns no schema (DP-01) and reads the ACE position, the proceeds, the case, the write-off, the record and the authority from their owners only. The three ACE views are read through rwb-source-data's data product (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). The composed reads a screen would make are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ReconciliationRunner | Job | Runs the owned criterion, the repeatability run, the negative path and the evidence step in order for a business date and holds the run lock |
| StubSet | Fake | The six service stubs and the three event stubs of section 12.8, each generated from the published contract with the version pinned |
| AcePositionProbe | Service | Reads the freshness answer, the three payments and the one posting from the ACE position through rwb-source-data, and asserts the business date and the values the run was seeded with |
| WorkbenchSideProbe | Service | Reads the case, the proceeds and the match from rwb-payment, the case from rwb-case and the approved write-off from rwb-writeoff |
| ReconciliationResultProbe | Service | Drives the owner's step and asserts REC-04, REC-05 and REC-06 against the owner's outcome and job record, by `rec_code` and business date |
| EventProbe | Service | Consumes `rwb.source-data.events.v1`, `rwb.payment.events.v1`, `rwb.writeoff.events.v1` and `rwb.decision-record.v1` and asserts the facts for the business date |
| EvidenceReport | Service | Writes the report keyed by story and business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, with account `A-0001` carrying three payments in `v_ace_payment` and one posting in `v_ace_write_off` at the ACE batch date 2026-12-14, one case holding the three matching proceeds, one approved write-off, and one seeded orphan key for the REC-05 path. The environment, the seeding set, the data product code and the evidence retention are not specified in the source documents (GAP-0434; ASM-0610). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the six service stubs and the three event stubs from the published contracts, pin each version in the report and fail the run on a version mismatch (X1, X15).
2. Build the AcePositionProbe to read the freshness answer, the three payments and the one posting from rwb-source-data, and to fail where the date is not LOADED or has no ALS completed event (X2, X3, X4).
3. Build the WorkbenchSideProbe to read the case, the proceeds and the match from their owners, and to fail where the write-off read is not through rwb-writeoff's contract.
4. Build the ReconciliationRunner to trigger the owner's step through the ready call and assert the JOB-04 run for the business date (X5, AC9, AC10).
5. Add the REC-04 assertion: every `payment_code` read from ACE resolves to a proceeds row on the case, and the owner's count for the business date agrees (X6).
6. Add the REC-06 assertion: the `write_off_key` resolves to the approved write-off, with the amount and the posting date agreeing (X7).
7. Add the REC-05 assertion on the seeded orphan key: the key is listed with its reason and the case is unchanged (X8).
8. Add the result assertion: one outcome per `rec_code` exercised, keyed by `rec_code` and the business date the batch record carried (X9).
9. Assert one record for the step through the rwb-decision contract, naming the rule ID and version of each rule fired and the counts, and fail where either is absent (X10).
10. Add the EventProbe for the four events, and assert the key, the 5-minute arrival and the absence of personal data (X11).
11. Add the repeatability run for the same business date and assert nothing doubles, recording the idempotency hit (X12); add the negative path with the record forced to fail (X13); add the access path through `POST /api/recovery/access/v1/authorise` (X14).
12. Add the EvidenceReport and the gate, then swap the rwb-payment stub for the real service when RWB-P8-E4050-APP lands and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it; the flag key is not specified in the source documents (GAP-0434; ASM-0610).

**Done when.** The tests of section 16 pass; the criterion passes against the fakes on Day 1 and again against the real owners as RWB-P8-E4050-APP lands; and the wave entry check holds a report keyed by story and business date with the contract and fixture versions and the business date named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the reconciliation step cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

REC-04, REC-05 and REC-06 carry no message ID in the rule set read, so the harness asserts the match, the break list, the result row and the decision record, and names a message ID only where an owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-28 Proceeds matching is the screen the legacy key names for this behaviour:

| State | What the user sees and does |
|---|---|
| Loading | The daily reconciliation for the business date is running, and the payments and the posting are being matched |
| matched | The payments are aligned to the proceeds on the case, the posting is aligned to the approved write-off, and no key is unresolved |
| unmatched | A payment, a posting or a key does not resolve, and an officer or the data steward has to resolve it on the break list |
| Empty | Not specified in the source documents (CG-ALL-911) |
| Loading | Not specified in the source documents (CG-ALL-911) |
| Error | Not specified in the source documents (CG-ALL-911) |
| No access | Not specified in the source documents (CG-ALL-911); the no-access outcome is asserted by AC5 and X14 |

The harness renders no screen. It reads these states through the rwb-source-data, rwb-payment, rwb-writeoff, rwb-case and rwb-decision contracts, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0434; ASM-0610).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-050-01-ITG | AC1, AC3, AC4, BR1, BR2, BR3, BR4, BR5, BR6 | Integration | Account `A-0001` with three payments and one posting served by the rwb-source-data contract fake of section 12.8 at the ACE batch date 2026-12-14 |
| TC-E4-050-02-ITG | AC2 negative path (run by RWB-P8-E4050-APP), BR8 | Integration | Decision log forced to fail; MSG-P7-003 |
| TC-E4-050-03-ITG | AC5, Access | Component | A role without the right, or a caller outside the case scope; MSG-P4-002 |
| TC-E4-050-04-ITG | Principle 5 | NFR | Forced decision-log write failure; nothing moves |
| TC-E4-050-05-ITG | AC6, BR7, BR9 | Integration | Account `A-0001` with three payments and one posting served by the rwb-source-data contract fake of section 12.8 at the ACE batch date 2026-12-14; the same event sent twice with the same key; one payment whose `payment_code` matches no plan, settlement or fee |
| TC-E4-050-06-ITG | AC7 | Integration | The contract fake of section 12.8 for one consumed call set to fail or not to answer |
| TC-E4-050-07-ITG | AC8 | Integration | A status change the model does not allow, requested for a case |

AC9, AC10 and the changed assertions of AC3 and AC6: Test Cases v9: TC-E4-050-08-ITG, TC-E4-050-05-ITG, TC-E4-050-09-ITG, TC-E4-050-10-ITG.

These are the ITG copies of TC-E4-050-01 to TC-E4-050-04 and carry the legacy data unchanged, with the component and NFR copies keeping the legacy levels. AC3 and AC4 are asserted inside TC-E4-050-01-ITG as the repeatability run and the evidence step, and add no legacy data. The Given, When and Then for these IDs are not yet in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases; they are to be added in the next version, copied from the criterion each row covers.

### 17. Guardrails

- No business value in code: the business date, the tolerance behind any reconciliation rule, the rule versions, the seeding set and the result mappings are data, and the harness holds no copy of any of them.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the three ACE views are ACE's, read through rwb-source-data's data product (DP-05).
- The harness computes no reconciliation: `reconciliation_result` and its `rec_code` and business date are P1 rwb-source-data's, and the harness drives the owner's step and asserts the owner's outcome.
- The Workbench holds no payment or posting copy and writes no result row outside the owning service (legacy RWB-E4-050; D-RCV-35 U4).
- One hop and a 2 s timeout per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a match, a break, a result row or a decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments received, read from ACE through `v_ace_payment`, are matched to the plan, the settlement or the fee they belong to by the ACE `payment_code`, and anything unmatched goes to an exception list | Business Requirements Program v5, section 5.3 | FEAT-PAY-11 | L1 19 Manage payments and reconciliation (D3, D5, D6) | REC-04 | TC-E4-050-01-ITG |
| REQ-RDF-007 | The case list reconciles daily to the count of accounts at 90 or more days past due in `v_ace_account`, with no variance, and every business key on a Workbench table resolves to an ACE row | Business Requirements Program v5, section 5.1 | FEAT-PAY-11 | L1 19 Manage payments and reconciliation (D3, D5, D6) | REC-05 | TC-E4-050-01-ITG |
| REQ-RDF-008 | The Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner | Business Requirements Program v5, section 5.1 | FEAT-PAY-11 | L1 19 Manage payments and reconciliation (D3, D5, D6) | REC-05 | TC-E4-050-01-ITG |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published | Business Requirements Program v5, section 5.14 | FEAT-PAY-11 | L1 19 Manage payments and reconciliation (D3, D5, D6) | REC-06 | TC-E4-050-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Business Requirements Program v5, section 5.7 | FEAT-PAY-11 | L1 19 Manage payments and reconciliation (D3, D5, D6) | R-UNI-39, R-UNI-40 | TC-E4-050-01-ITG, TC-E4-050-02-ITG, TC-E4-050-04-ITG |

The feature is FEAT-PAY-11 Reconcile money movements daily, owned by P8 in the Epics 3 to 8 Specification v3 and delivered here as an integration harness across P1, P8, S7, P3, P7 and P4.

### 19. Out of scope

- AC2 of the legacy key, the refusal when the decision log cannot be written, which is owned by RWB-P8-E4050-APP; this story exercises it only as a negative path.
- The reconciliation step itself, its workflow and the `reconciliation_result` row, which are P1 rwb-source-data's: the matching rules, the tolerance, the break list and the job that writes the outcome.
- The payment and proceeds matching inside rwb-payment, which is RWB-P8-E4050-APP: the proceeds, the match and the payment and booking records.
- The approved write-off and its posting completeness, which are S7 rwb-writeoff's and are consumed here through the published contract.
- The ACE views `v_ace_payment`, `v_ace_write_off` and `v_ace_batch_status`, which are ACE's and are read only through rwb-source-data's contract and its data product (DP-05).
- The contract baselines of rwb-source-data, rwb-payment, rwb-case, rwb-writeoff, rwb-decision and rwb-access, which are their CON stories and are consumed here through the published documents and their fakes.
- The platform configuration: the decision-record library, the gateway-bff composite route, the feature-flag library and the observability set.
- The data steward's break handling, the tolerance behind REC-05 and any Power BI report over the reconciliation results (RWB-E1-011), which belong to the data product owner and to reporting.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the data product code, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.

### 20. Remaining delivery steps

- Size the story at refinement (owner: squad).
- Publish the rwb-source-data 5.1.0 fake with the ready, job, result, record and freshness answers, and add the reconciliation reads to the yaml (owner: rwb-source-data contract owner).
- Deploy `AceIngestCheck` and `ReconciliationWorkflow` to SIT, seed the ACE rows and grant the test identity (owner: integration and QA team with the bank platform team).
- Pending: data product code, write-off read, harness environment and evidence format, owner integration and QA team, tracked as GAP-0434 and GAP-0436.
- Pending: the published read of the REC-04 and REC-06 results of rwb-payment (NEW-GAP-F05-5), owner rwb-payment contract owner. A completed run is not rerun (RD-P1-065).
