# RWB-ITG-DM007-ITG Migrate legal events and cases

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- JOB-04 is started by the readiness call as a child of `AceIngestCheck`; the invalid rerun call and the event-start wording are removed (RD-P1-012, RD-P1-040; findings #1, #9).
- Court and delivery facts are read from ACE and not carried; migrated rows carry `migration_source` and `migrated_at` (RD-P1-027; #3, #8).
- The key listing on the real services is pending (GAP-1508, NEW-GAP-S2B-03; #2); the court record link is pending (NEW-GAP-S12-6).
- Freshness, readiness, rights, error body, message use and contract version aligned to rwb-source-data.yaml 5.1.0; AC9 added (RD-P1-004, RD-P1-005, RD-P1-041, RD-P1-042; #4 to #7, #10).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- A repeated readiness call answers 202 and starts nothing once every due source is stamped and the run has ended (RD-P1-065, register XD-11).
- `lawsuit_no` (DF-LEG-005) is carried as the linking key to the court record, so NEW-GAP-S12-6 is closed (RD-P1-068).
- The reconciliation result reads are cited as published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, RD-P1-063).

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM007-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1015-CON (readiness and freshness), RWB-P1-E1011-CON (reconciliation result reads), RWB-P1-E1016-CON (data product records); the CON stories of rwb-litigation, rwb-comms, rwb-partner, rwb-case and rwb-access: Not specified in the source documents |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); rwb-litigation, rwb-comms, rwb-partner, rwb-case and rwb-access 5.1.0 |
| Integration dependencies | RWB-P1-DM007-APP (not done yet; owns the cutover and legacy AC3) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-022, RD-P1-027, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-065, RD-P1-068, RD-P1-063 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-007 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM007-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 10 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; cutover reconciliation harness aligned to the readiness chain, the migration field mapping and the published reads.

### 1. Story

As a **RW-DATASTEW**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated legal action, notice and instruction records resolves to its ACE view row, that the court record is read and never copied, and that every orphan is listed for the data steward and the ACE team, against the owning services' published contracts and their fakes**, so that **litigation continues at cutover while the court case and hearing records are read from ACE**.

This is a harness story only. It builds no production endpoint, table, workflow, schedule or screen, and it changes no business state. The migration itself, including the cutover and the sign-off that closes legacy AC3, is RWB-P1-DM007-APP. The records the harness reads are placed by each owner's own cutover load: the legal action by S4 rwb-litigation, the notice by P6 rwb-comms, the partner instruction by S9 rwb-partner, each through its own Flyway sequence (DP-15). The case is held by P3 rwb-case and is migrated under RWB-DM-003, not by this package, which excludes `recovery_case` (RD-P1-027). On Day 1 the stubs of section 12.8 return the same records; in SIT the owners' cutover loads provide them.

### 2. Business rationale

A legal action that loses its lawsuit_no loses the court case it belongs to. A notice that loses its person_key cannot be shown to have reached the right person. An instruction that loses its firm or its due date leaves a panel firm working without a clock, or working on a case that has moved on. Each of those three is a data fault that surfaces months later as an adjourned hearing, a service challenge or an unpaid firm, and by then the legal clock has run. Because the court case and the hearing record are read from ACE and never copied, a defect in the key resolution shows up where it can still be fixed: as an orphan on the break list, not as a copy that drifts quietly away from ACE.

The harness is decoupled the way the services are. ACE data is read through rwb-source-data's contract and never from a view held by another service (DP-05, ADR-010). Each owner migrates its own records in its own schema and its own Flyway sequence (DP-15), so the harness proves the cutover each owner actually runs and not a load it staged itself. Where a screen would compose the reconciliation answer, the harness calls the gateway-bff composite route and not the services one by one (DP-19).

The prescription clock is a legal deadline and it never pauses, not for a deviation and not for a cutover (R-DEV-01). An unresolved lawsuit key does not stop it. The programme therefore puts zero tolerance on this key set (DL25), and the reporting duty is explicit: every business key on a Workbench table resolves to an ACE row, and every break carries a reason that the data product owner can see (REQ-RDF-007, REQ-RDF-008).

### 3. Preconditions

- The published contracts of S4 rwb-litigation (`GET /legal-actions/{legalActionId}`), P6 rwb-comms (`GET /notices/{noticeId}`) and S9 rwb-partner (`GET /partner/instructions`) are in the contract registry, and a stub set is generated from each one.
- The P3 rwb-case case contract (`GET /cases/{caseId}`) is in the registry, with its stub.
- The P1 rwb-source-data contract (rwb-source-data.yaml 5.1.0: DP02 and DP07 record reads, freshness read, readiness call and status, reconciliation result reads) is in the registry, with its fake `fakes/rwb-source-data/5.1.0/`. The reconciliation result reads are published (`getAdminReconciliationResults`, RD-P1-063).
- The harness caller of the readiness call holds Platform administration U; the caller of the record and freshness reads holds Case record R, and of the readiness status and reconciliation result reads Platform administration R. A key field that the record read returns with `masked` true fails the run and is reported.
- The data product catalog holds DP02 Customer and party and DP07 Legal events and cases, with their systems of record and their refresh: both DAILY, expected by 08:00.
- RWB-P1-DM007-APP is in build, and the wave 4 cutover loads of S4 legal_action, P6 notice, S9 partner_instruction and P3 recovery_case are scheduled.
- The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list contract, the evidence format and retention, the pass or fail gate and the data seeding set: Not specified in the source documents (GAP-0447; ASM-0639).
- No build dependency. Day 1, with the stubs in place from the first run, and each stub replaced by the real owner as RWB-P1-DM007-APP and that owner's story land.

### 4. Flow

1. Harness: on Day 1 the stub set of section 12.8 returns the migrated records for business date 2026-12-31, namely legal action `LA-0607` on case `RW-2026-000607`, notice `N-0607`, instruction `PI-0607` with firm `FIRM-SYN-0607` and due date 2026-12-15, the DP07 lawsuit and hearing rows and the DP02 person row. In SIT the cutover load of each owner's own Flyway sequence provides the same records, each with `migration_source` and `migrated_at`. The harness seeds nothing by hand.
2. Harness: starts the chain for business date 2026-12-31 with `POST /api/recovery/source-data/v1/business-days/{date}/ready` and a UUID `Idempotency-Key` (202), and waits until `AceIngestCheck` has stamped the ALS batch and its child `ReconciliationWorkflow` (`recon-2026-12-31`, JOB-04) has completed, after rwb-case answers its allocation or at 07:15 (RD-P1-040). The harness never reruns JOB-04: `POST /admin/jobs/{jobId}/rerun` takes the run uuid of a FAILED run only (RD-P1-012).
3. Harness: reads legal action `LA-0607` with `GET /api/recovery/litigation/v1/legal-actions/{legalActionId}` and asserts its id, its case, its law firm, its action_type `LAWSUIT`, its status, `migration_source` and `migrated_at`, and that no hearing row was created by the migration; lawsuit_no is carried as the linking ACE business key to `v_ace_lawsuit` (DF-LEG-005 KEY, RD-P1-068 rule 4) and is asserted on the record; court, claim and judgment are not carried and are asserted only on the DP07 record read of step 7 (RD-P1-027) (AC1).
4. Harness: reads notice `N-0607` with `GET /api/recovery/comms/v1/notices/{noticeId}` and asserts its case, its person_key `PERS-SYN-0607`, `migration_source` and `migrated_at`; sent date and barcode are read from ACE and are not carried (RD-P1-027) (AC1).
5. Harness: reads instruction `PI-0607` with `GET /api/recovery/partner/v1/partner/instructions` and asserts it is open, with firm `FIRM-SYN-0607` and due date 2026-12-15 (AC1, AC3).
6. Harness: reads the case with `GET /api/recovery/case/v1/cases/{caseId}` for its status and its stage, before and after the run (AC2).
7. Harness: reads the court record with `GET /api/recovery/source-data/v1/data-products/DP07/records?caseId={caseId}` and resolves the person key with the DP02 record read (rows of `fields` with `fieldName`, `value`, `masked`), and reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP07` for `status` (`LOADED` or `STALE`), `businessDate` and `loadedAt`, so that a late batch is reported and not assumed. The court record of a migrated legal action is found by its carried lawsuit_no (RD-P1-068 rule 4) (AC2, X5).
8. Harness: reads the breaks from the reconciliation extract fixture and the SCR-45 Data quality composite route, reads the REC rows through `GET /api/recovery/source-data/v1/admin/reconciliation/results?from=2026-12-31&to=2026-12-31`, and asserts one row for legal action `LA-0607` with key type `LAWSUIT`, key value `LIT-SYN-0777`, reason `NO_ACE_ROW` and owner role `RW-DATASTEW`; it also asserts that no hearing exists and that `PI-0607` is not recalled, and both records stay readable through their owners' contracts (AC3). P1 stores no key-level break row and the REC-05 scope holds no legal action or notice key (RD-P1-022): on the real services the key listing is pending the break-detail store (GAP-1508, NEW-GAP-S2B-03).
9. Harness: repeats the readiness call for the same business date with a new UUID `Idempotency-Key` and asserts no second set of reconciliation result rows, one break row for `LIT-SYN-0777`, counts of legal actions, notices and instructions equal to the first run, and one report entry per business date; then it calls `POST /api/recovery/access/v1/authorise` for a caller with role `RW-OFF` and no Platform administration right and asserts the refusal, then sends the readiness call as that caller and asserts 403 with `messageCode` MSG-P4-002, no run started and no break row written (AC4, AC5); it writes one evidence report per business date. The repeated call answers 202 with the stored state and starts nothing; a second run of the date exists only through the rerun of a FAILED run (RD-P1-065 rule 3, register XD-11).

Gate: AC1 to AC9 all pass on the stubs and again on the real owners, with the key listing of AC3 on the real services pending (GAP-1508, NEW-GAP-S2B-03). The environment, base hosts, cutover fixture layout, SCR-45 composite route and break-list fields are fixed at the wave 4 entry check from the gateway-bff contract once RWB-AD-019 publishes; the extract format and retention are agreed with the data steward (GAP-0447).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version, and the run is not marked passed | None | AC1, AC2 |
| X2 | The fixture lacks a required key, for example no legal action, notice or instruction for the case | The run fails before any assertion; the report names the entity and the missing key | None | AC1 |
| X3 | A migrated business key has no view row and is not listed as a break | The run fails on AC3; the report names the key type and the key value | None | AC3 |
| X4 | A break row appears twice after a repeated run, or the counts move between runs | The run fails on AC4; the report names the two rows and the business date | None | AC4 |
| X5 | The ALS batch is late (no ALS stamp, so JOB-04 is not started), or DP07 reads `status` `STALE` | The readiness status reads `LATE`, or the freshness read answers `STALE` (`businessDate` null when never stamped); the run is reported as not run, never as passed | MSG-P1-001 | AC2, AC4, AC9 |
| X6 | The SCR-45 answer and the reconciliation extract disagree | The run fails on AC3; the report names both answers and the variance | None | AC3 |
| X7 | A caller without the Platform administration right has a run started anyway | The run fails on AC5; the report names the caller role and the operation, and asserts that no break row was written | MSG-P4-002 | AC5 |

The report text belongs to the wave entry check and is not part of the message standard. The business messages the journey produces are in section 14, and the harness asserts them as data on the owner's answer and not as free text.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and their stubs from Day 1; the only wait is RWB-P1-DM007-APP and, one at a time, the S4, P6, S9 and P3 owners |
| Negotiable | The fixtures, the base hosts, the break-list contract and the report shape are configuration agreed at the wave entry check, not business values in code |
| Valuable | The legal key set is proven resolvable, and every orphan is listed, before litigation is cut over onto the new schemas |
| Estimable | One journey runner, one stub set, two fixtures, one key resolver, one break-list assertion and one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion runs against the stubs and again against the real owner as each lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate legal events and cases - wave 4 cutover reconciliation harness

  Background:
    Given legal action "LA-0607" on case "RW-2026-000607" with action_type "LAWSUIT"
    Given notice "N-0607" on the case carries person_key "PERS-SYN-0607"
    Given instruction "PI-0607" is open with firm "FIRM-SYN-0607" and due date "2026-12-15"
    Given the DP07 record read answers the court record with lawsuit_no "LIT-SYN-0607" and its hearing rows for the case
    Given ReconciliationWorkflow "recon-2026-12-31" (JOB-04) has completed for business date "2026-12-31" as the child of AceIngestCheck

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-007 AC1, changed by RD-P1-027)
    Given the legacy Workbench legal action, notice and partner instruction records for the open cases at cutover
    When the migration reads them
    Then each legal action keeps its id, case_id, law_firm_id, action_type and status, each notice its person_key, and each instruction its firm and its due date
    And each migrated record carries migration_source and migrated_at
    And its lawsuit_no is carried as the linking ACE business key
    And its court, claim and judgment are not carried and are answered by the DP07 record read from v_ace_lawsuit
    And no lawsuit and no hearing record is copied, because the court record is read from v_ace_lawsuit and v_ace_hearing

  Scenario: AC2 Reconcile the business keys (legacy RWB-DM-007 AC2)
    Given the migrated records
    When the harness resolves the keys of the migrated records for business date "2026-12-31"
    Then every business key on a migrated record resolves to its view row, account_key and person_key included, person_key "PERS-SYN-0607" through the DP02 record read
    And each orphan is listed for the data steward and the ACE team in the run report
    And no legal action or notice key is expected from the REC-05 step of JOB-04, whose scope does not hold them (RD-P1-022)
    And the court record link of a migrated legal action is its carried lawsuit_no

  Scenario: AC3 An orphan lawsuit key is listed and the instruction stays open (new, D-RCV-60)
    Given the reconciliation extract fixture relates legal action "LA-0607" to lawsuit_no "LIT-SYN-0777"
    And the DP07 record read answers no court record for lawsuit_no "LIT-SYN-0777"
    When the harness reads the reconciliation outcome for business date "2026-12-31"
    Then the break list of the reconciliation extract fixture holds one row for legal action "LA-0607" with key type "LAWSUIT" and key value "LIT-SYN-0777"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the legal action, its notice and its instruction stay readable through their owners' contracts
    And no hearing is recorded and no instruction is recalled
    And on the real services the listing of this key is pending the break-detail store (GAP-1508, NEW-GAP-S2B-03)

  Scenario: AC4 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-12-31" has run once
    When POST /business-days/2026-12-31/ready is called again with a new UUID Idempotency-Key and answers 202
    Then the repeated call starts nothing: no second ReconciliationWorkflow run for "2026-12-31", because every due source of the date is stamped and the run has ended
    And no second set of reconciliation result rows exists for 2026-12-31
    And the break list holds exactly one row for lawsuit_no "LIT-SYN-0777"
    And the counts of legal actions, notices and instructions equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC5 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When that user calls POST /business-days/2026-12-31/ready with a UUID Idempotency-Key
    Then the answer is 403 with a problem body whose messageCode is "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC6 Each business rule in section 8 is traced to a test (new, D-RCV-60)
    Given the business rules BR1 to BR8 in section 8
    When the story is checked against section 16
    Then each rule BR1 to BR8 is named by a test case row in section 16

  Scenario: AC7 A consumed call that fails or does not answer is reported and no break is rounded away (new, D-RCV-60)
    Given the gateway-bff composite route for SCR-45 composes the reconciliation extract of rwb-source-data with the owners' reads
    And one consumed rwb-source-data call answers 503 with messageCode "MSG-GEN-006" or does not answer within 2 s
    When the harness calls the composite route for business date "2026-12-31"
    Then the answer is an error and no partial break list is returned
    And the run report records the failed call and the state it read
    And no break is rounded away (BR3)

  Scenario: AC8 The migrated records are read through their owners and keep their origin (new, D-RCV-60)
    Given legal action "LA-0607", notice "N-0607" and instruction "PI-0607" are migrated, each owner in its own schema and its own Flyway sequence (BR8)
    And one business key of the case does not resolve
    When the harness reads the records and the case before and after the reconciliation for business date "2026-12-31"
    Then ACE data is read only through the rwb-source-data contract and the views it owns (BR4)
    And the prescription clock of the case does not pause (BR6)
    And each migrated record keeps its migration_source and migrated_at, which the harness asserts and never rewrites (BR7)
    And each record is read through its owner's contract after that owner's cutover and not from a staged load (BR8)

  Scenario: AC9 A late or never stamped batch is reported as not run (new, RD-P1-040, RD-P1-041)
    Given the readiness status fake answers status "LATE" for business date "2026-12-31"
    And the freshness fake answers DP07 with status "STALE" and businessDate null
    When the harness runs for business date "2026-12-31"
    Then the run report records "not run" with DP07, the business date and "MSG-P1-001"
    And no key is resolved, no break row is asserted and the run is not marked passed
```

Legacy AC3 belongs to RWB-P1-DM007-APP, and the nine criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated legal action, notice and instruction resolves to its ACE view row, account_key and person_key included | REQ-RDF-007; DL25 (ASM-0728, ASM-0735, ASM-0743, ASM-2602); legacy AC2 |
| BR2 | Every break is listed with its key type, its key value, its reason and its owner role, for the data steward and the ACE team | REQ-RDF-008; legacy AC2 |
| BR3 | Zero tolerance: a variance or an orphan is a break and is never rounded away or reported as a pass | DL25 (ASM-0728, ASM-0735, ASM-0743, ASM-2602); DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00; REQ-RDF-007 |
| BR4 | ACE data is read only through rwb-source-data's contract and the views it owns, never from another service's schema or from a view held locally | D-RCV-35; ADR-010; DP-05 |
| BR5 | The court case and the hearing record are read from v_ace_lawsuit and v_ace_hearing and are never copied into a Workbench table | legacy AC1; RD-P1-027 (court fields are ACE_READ, never carried) |
| BR6 | The prescription clock never pauses, and an unresolved key does not pause it either | R-DEV-01 |
| BR7 | A migrated record keeps its `migration_source` and `migrated_at`, and the harness asserts both and never rewrites them | Legacy RWB-DM-007 guardrails; RD-P1-027 |
| BR8 | Each owner migrates in its own schema and its own Flyway sequence, so the harness proves the owner's cutover and not a staged load | DP-15 |

### 9. State transitions

The harness changes no state. The legal action, the notice and the instruction keep the state and the dates they were migrated with, and the case keeps its status and its stage. An orphan stays readable through its owner's contract and is only listed; a listed orphan that later resolves on a later run is no longer listed, and nothing about the record itself moves. A state the harness set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

S4 rwb-litigation, P6 rwb-comms and S9 rwb-partner own every state change on these records, with P3 rwb-case owning the case state. The harness reads through their contracts and writes only its own evidence report.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the break list and the run report; owns the reconciliation question for the legal key set |
| RW-COE, centre of excellence | Reads the same evidence and the REC-05 result |
| RW-AUDIT, internal audit | Reads the run report and the break list as retained evidence |
| RW-COMPLY, compliance | Reads the same evidence for the litigation and prescription position |
| RW-PLATADM, platform administrator | Holds Platform administration R and reads the same evidence; the readiness call needs Platform administration U |
| Harness caller | Holds Platform administration U for the readiness call, Platform administration R for the status and result reads and Case record R for the record and freshness reads |
| RW-SECADM, security administrator | Holds Platform administration R and may read the same evidence |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real owner |
| S4, P6, S9 and P1 identities | rwb-litigation, rwb-comms and rwb-partner serve their records; rwb-source-data runs JOB-04 as a child of `AceIngestCheck` and writes the reconciliation result; no store holds key-level break rows yet (GAP-1508) |
| No delegation of authority level applies | The harness takes no business decision and approves nothing |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, status, stage_code; the other fields are not all confirmed against LDM v9 (DOR-RWB-ITG-DM007-ITG-7) | Read, through the rwb-case contract |
| DF-LEG-001 to DF-LEG-014 | legal_action | Carried: DF-LEG-001 to DF-LEG-004 and DF-LEG-014 (id, case_id, law_firm_id, action_type, status); KEY: DF-LEG-005 lawsuit_no, the linking ACE business key to `v_ace_lawsuit` (RD-P1-068 rule 4). ACE_READ, never carried: DF-LEG-006 to DF-LEG-013 (court, claim, judgment and the other court facts; RD-P1-027) | Read, through the rwb-litigation contract; court facts through the DP07 record read |
| DF-LEG-015 to DF-LEG-023 | notice | Carried: DF-LEG-015 to DF-LEG-018 (id, case_id and document fields). ACE_READ, never carried: DF-LEG-019 to DF-LEG-023 (sent_date, barcode, callback_date, delivery_status, sent_type; RD-P1-027) | Read, through the rwb-comms contract; delivery facts through the DP07 record read |
| DF-LEG-024 to DF-LEG-029 | hearing | Not specified in the source documents (CG-ALL-1013) | Read, through the owning contract |
| DF-LEG-030 to DF-LEG-034 | notice | KEY: DF-LEG-030 person_key. Carried: DF-LEG-031 to DF-LEG-034 (template_id, hold_reason, dispatch_file_id, dispatch_attempts; RD-P1-027) | Read, through the rwb-comms contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at; the legal slice is handed over by RWB-P1-DM007-APP and the panel slice by the RWB-DM-008 migration, both loaded idempotent on the instruction id | Read, through the rwb-partner contract |
| Standard column | legal_action, notice, partner_instruction | migration_source, migrated_at (RD-P1-027) | Read, through the owning contract |

The court and delivery facts are read through the DP07 Legal events and cases record read, which is view-backed (v_ace_lawsuit, v_ace_hearing, v_ace_pod), and the person_key resolves through DP02 Customer and party for the person_key; the harness reads DP07 only through the data product contract and never the v_ace_lawsuit or v_ace_hearing views. The harness owns no table and writes no row directly: it reads through the owner's contract and the data product contract (DP-05, ADR-010), and it seeds nothing. The seeding set is not specified in the source documents (GAP-0447; ASM-0639). The lists and parameters the harness reads come through the reference-data contract of DP-06 and DP-07; the parameter names are not specified in the source documents (DOR-RWB-ITG-DM007-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Start `AceIngestCheck`, whose child is JOB-04, with a UUID Idempotency-Key; 202 (AC2, AC4, AC5) |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data | `RUNNING`, `DONE` or `LATE` for the business date (X5, AC9) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | The REC rows of the business date (AC2, AC3); pending in the yaml file (RWB-P1-E1011-CON) |
| GET | `/api/recovery/source-data/v1/data-products/DP07/records?caseId={caseId}` | P1 rwb-source-data | The view-backed court record and hearing presence through DP07 (AC1, AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | Resolve the person_key on the notice through DP02 (AC2) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP07` | P1 rwb-source-data | `status`, `businessDate` and `loadedAt` of DP07, so a late batch is reported (X5, AC9) |
| GET | `/api/recovery/litigation/v1/legal-actions/{legalActionId}` | S4 rwb-litigation | The legal action, its case, its action_type, its lawsuit_no and its judgment (AC1, AC3) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice, its case and its person_key (AC1, AC3) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instruction, its firm, its due date and that it is still open (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status and stage before and after the run (AC2) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration R check, including the refusal path (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-05, DP-11). Every error of rwb-source-data is an `application/problem+json` body with `messageCode` (RD-P1-004). Where a screen would compose the answer, the harness calls the gateway-bff composite route (DP-19).

The break list and its two answers are read through the gateway-bff composite route for SCR-45 Data quality, which composes the reconciliation extract of rwb-source-data with the owners' reads. Its path and its merge order are Not specified in the source documents (GAP-0447; ASM-0639). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its evidence report to the wave record.

#### 12.4 Events consumed

None. JOB-04 runs inside rwb-source-data as a child of `AceIngestCheck` (RD-P1-040), and the harness starts it with the readiness call and observes it through the owner's operations rather than through a topic.

#### 12.5 Workflows and activities

None added. The harness exercises the existing JOB-04 Reconciliation workflow `ReconciliationWorkflow` of rwb-source-data, workflow ID `recon-{businessDate}`, started by `AceIngestCheck` as its child after the ALS stamp (RD-P1-040), and asserts its effect through the owner's contract (DP-05). No workflow, activity or task queue is created, changed or owned by this story, and LitigationWorkflow is not started by the harness.

#### 12.6 Schedules

None added. JOB-04 runs for the business date under test through the readiness call only, and no cron, overlap policy or catch-up window is set by this story.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01, DP-15); it reads through the owners' contracts and through the DP02 and DP07 data product contract.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-source-data | `fakes/rwb-source-data/5.1.0/`: the readiness call and status, the reconciliation result reads, the DP02 and DP07 record reads and the freshness read | Day-1 trigger, key resolution and freshness assertions before the owner is live |
| Stub for rwb-litigation | `GET /legal-actions/{legalActionId}` | Day-1 assertion on the legal action, its lawsuit_no and the absence of a copied hearing |
| Stub for rwb-comms | `GET /notices/{noticeId}` | Day-1 assertion on the notice and its person_key |
| Stub for rwb-partner | `GET /partner/instructions` | Day-1 assertion on the open instruction, its firm and its due date |
| Stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertion on the case status and stage |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path |
| Cutover extract fixture | The migrated legal action, notice, instruction and case records with their keys | The records the run asserts, on Day 1 and in SIT |
| Reconciliation extract fixture | The break list of the business date | The one break row, its reason and its owner role |
| SCR-45 composite route stub | The gateway-bff Data quality route | The same break list as a screen would receive it |

The harness builds against contract version 5.1.0 of rwb-source-data, rwb-litigation, rwb-comms, rwb-partner, rwb-case and rwb-access (API Specification v7, `info.version`). Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the cutover extract fixture and its field layout, the break-list fields, the reconciliation extract format and retention and the data seeding set are not specified in the source documents (GAP-0447; ASM-0639). Section 4 states the pass gate and when the environment, hosts, fixture layout, break-list fields, extract format and retention are fixed.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 11 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-05, DP-11) |
| Kafka | None published and none consumed; JOB-04 is started through the readiness call |
| Temporal | None added; `ReconciliationWorkflow` (JOB-04) is exercised as the child of `AceIngestCheck` (DP-05) |
| File | The cutover extract fixture and the reconciliation extract fixture, both as fixtures |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The blocking dependency is the single I story, RWB-P1-DM007-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the criteria of section 7 in order for a business date and holds the run lock |
| StubSet | Fake | The six service stubs generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The migrated legal action, notice, instruction and case records with their keys, keyed by business date |
| LawsuitKeyResolver | Service | Resolves lawsuit_no and person_key through DP07 and DP02 and reports a missing view row as an orphan |
| BreakListAssertion | Service | Asserts one break row, its reason and its owner role, and its stability across a repeated run |
| EvidenceReport | Service | Writes one report per business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real owners as they land, on case `RW-2026-000607`, legal action `LA-0607` with action_type `LAWSUIT` and lawsuit_no `LIT-SYN-0607`, notice `N-0607` with person_key `PERS-SYN-0607`, open instruction `PI-0607` with firm `FIRM-SYN-0607` and due date 2026-12-15, the orphan lawsuit_no `LIT-SYN-0777` and business date 2026-12-31. The data is synthetic and holds no personal data beyond the keys, and no court name and no claim amount is stated because the sources give none. The environment, the base hosts, the fixture layout, the seeding set and the evidence retention are not specified in the source documents (GAP-0447; ASM-0639). Seeding uses only the owners' cutover loads and never a schema write.

**Build steps**

1. Generate the six stubs from the published contracts and pin each contract version in the run report; fail the run on a version mismatch (X1).
2. Build the cutover extract fixture and the reconciliation extract fixture for business date 2026-12-31, and prove the read-back for one date (X2).
3. Build AC1 and AC2: send the readiness call with a UUID Idempotency-Key and wait for `recon-2026-12-31`, read the legal action, the notice, the instruction and the case, read the court record through DP07 and resolve the person_key through DP02, and assert no copied hearing (BR5).
4. Add the freshness read, the readiness status and the stale path, so a late batch is reported as not run and not as a pass (X5, AC9).
5. Add AC3: the orphan lawsuit_no `LIT-SYN-0777`, one break row with reason `NO_ACE_ROW` and owner role `RW-DATASTEW`, the instruction still open and no hearing recorded (X3, X6).
6. Add AC4 and AC5: the repeated readiness call for the same business date with one break row, equal counts and one report entry, then the `RW-OFF` refusal with no run started and no break row written (X4, X7).
7. Add the EvidenceReport and the gate, then swap one stub for its real owner as each lands and repeat the criteria of section 7.

**Feature switch.** None. The harness has no feature switch of its own, and it reads the owners' data as released.

**Done when.** The tests of section 16 pass for the criteria of section 7; those criteria pass against the six stubs on Day 1 and again against RWB-P1-DM007-APP and each real owner as they land; and the wave entry check holds one run report per business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. | The freshness read answers `STALE` for DP07, or the readiness status reads `LATE`, for the business date |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. | rwb-source-data raises it only for a REC-01 or REC-02 BREAK (RD-P1-042); the harness asserts it only against a BREAK fixture |
| MSG-GEN-001 | Error | Enter {field}. | A required key or business date is missing from the run request |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A caller without Platform administration R calls the reconciliation run |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a run failure points at a service and a message and not only at a date.

### 15. Screens and states

SCR-45 Data quality carries five states, the two legacy states Loading and Breaks and the Empty, Error and No access states added (CG-ALL-1021), and the harness asserts each one through the gateway-bff composite route:

| State | What the user sees and does | What the harness asserts through the composite route |
|---|---|---|
| Loading | The data steward opens Data quality for the business date and waits for the reconciliation answer | The route answers with the break list of business date 2026-12-31 and not with a partial list, and the run report records the state it read |
| Empty | Not specified in the source documents (CG-ALL-1021) | The route answers with an empty break list for that business date, and the run report records the state it read |
| Error | Not specified in the source documents (CG-ALL-1021) | The screen shows the error and no break list, the run report records the state it read, and no break is rounded away (BR3) |
| No access | Not specified in the source documents (CG-ALL-1021) | The route refuses the caller and returns no break list (TC-DM-007-04-ITG) |
| Breaks | The data steward reads each break with its key type, key value, reason and owner role, and routes it to the ACE team | One row for legal action `LA-0607`, key type `LAWSUIT`, key value `LIT-SYN-0777`, reason `NO_ACE_ROW`, owner role `RW-DATASTEW`, stable across a repeated run; from the extract fixture until the break-detail store exists (GAP-1508) |

The harness renders no screen. Screen behaviour stays with the owning APP stories, and the Data quality and reconciliation console itself is RWB-AD-019. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0447; ASM-0639).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-007-01-ITG | AC1 (legacy); ITG AC1; BR5 | Integration | Legal action LA-0607, notice N-0607 and instruction PI-0607, with the DP02 and DP07 rows served by the rwb-source-data contract fake (§12.8) |
| TC-DM-007-02-ITG | AC2 (legacy); ITG AC1, ITG AC2, ITG AC3; BR1, BR2, BR3 | Integration | One lawsuit_no LIT-SYN-0777 with no view row |
| TC-DM-007-03-ITG | AC3 (legacy, owned by RWB-P1-DM007-APP); ITG AC4 | Integration | Two readiness calls for business date 2026-12-31 |
| TC-DM-007-04-ITG | Access; ITG AC5 | Component | RW-OFF caller without Platform administration R |
| TC-DM-007-05-ITG | ITG AC6 | Not specified in the source documents (NEWAC-RWB-ITG-DM007-ITG-AC6) | Business rules BR1 to BR8 of section 8 |
| TC-DM-007-06-ITG | ITG AC7 | Not specified in the source documents (NEWAC-RWB-ITG-DM007-ITG-AC7) | One consumed call of the composite route that fails or does not answer for business date 2026-12-31 |
| TC-DM-007-07-ITG | ITG AC8; BR4, BR6, BR7, BR8 | Integration | Legal action LA-0607, notice N-0607 and instruction PI-0607 with one unresolved business key, for business date 2026-12-31 |
| TC-DM-007-01-ITG, TC-DM-007-02-ITG, TC-DM-007-08-ITG, TC-DM-007-09-ITG, TC-DM-007-03-ITG, TC-DM-007-04-ITG, TC-DM-007-10-ITG, TC-DM-007-06-ITG, TC-DM-007-07-ITG | New ITG AC9 and the changed assertions of ITG AC1 to AC5, AC7 and AC8 | Integration | Values of section 7 |

The four cases are the ITG copies of the legacy cases of the same number and carry the legacy data unchanged, with the two new criteria and the access refusal added at the levels shown. TC-DM-007-05-ITG and TC-DM-007-06-ITG cover the new AC6 and AC7 and have no legacy copy. TC-DM-007-07-ITG covers the new AC8 and has no legacy copy. For the four ITG copies, the full test, with its Given, When and Then, is in the Test Cases workbook, tab Story test cases, under the same test case ID. TC-DM-007-05-ITG, TC-DM-007-06-ITG and TC-DM-007-07-ITG have no row there yet.

### 17. Guardrails

- No business value in code: court dates, prescription dates, SLA dates, the break reasons and the owner roles are data, not constants in the runner.
- No personal data anywhere: the notice carries a person_key only, the fixtures hold synthetic keys, and the report never writes a name, an address or a contact detail.
- No cross-schema read: every read goes through the owner's contract or the DP02 and DP07 data product contract, and no service reads another service's tables (DP-01, DP-05, ADR-010).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a legal action, notice, instruction, case, break or report state by hand.
- A failing criterion is fixed in the service that owns it or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-007 "Migrate legal events and cases" | Data Migration Stories v4, RWB-DM-007 section 1 | Section 1 and section 2; AC1 and AC2 are the parts this story owns |
| Legacy AC1 verbatim: "Given the legacy Workbench legal action, notice and partner instruction records for the open cases at cutover / When the migration reads them / Then each legal action keeps its case, its court, its claim and its judgment, each notice its person_key, and each instruction its firm and its due date / And no lawsuit and no hearing record is copied, because the court record is read from v_ace_lawsuit and v_ace_hearing" | Data Migration Stories v4, RWB-DM-007 | Section 7, ITG AC1; BR5, BR7 |
| Legacy AC2 verbatim: "Given the migrated records / When the REC-05 step runs / Then every business key on a migrated record resolves to its view row, account_key and person_key included / And each orphan is listed for the data steward and the ACE team" | Data Migration Stories v4, RWB-DM-007 | Section 7, ITG AC2; BR1, BR2 |
| Legacy test cases TC-DM-007-01, TC-DM-007-02, TC-DM-007-03 and TC-DM-007-04 as the -ITG copies | Data Migration Stories v4, RWB-DM-007 | Section 16 |
| DF-CAS-001 to DF-CAS-055, DF-LEG-001 to DF-LEG-014, DF-LEG-015 to DF-LEG-034, DF-PRT-008 to DF-PRT-016 and the standard source and migrated_at columns | Logical Data Model and Data Dictionary; RWB-DM-007 data table | Section 11 |
| DL25 | Legacy RWB-DM-007 decision | BR3; AC1, AC2 |
| R-DEV-01 | Business Rules and Routing Logic v4 | BR6; section 2 |
| D-RCV-35 and ADR-010 | Program Requirements v4; Architecture v5 slides 11, 15 and 45 | BR4; section 12.2 |
| RWB-E1-011 Reconciliation and data quality report | Business Requirements Epic 1 v5 | Section 2, section 15 and JOB-04, which this harness exercises |
| DP-05, DP-15 and DP-19 | Template and Rules v1 section R5.5 | Section 13, and the patterns applied in the metadata |

### 19. Out of scope

- RWB-P1-DM007-APP and the cutover itself, including legacy AC3 and the data steward's sign-off.
- The cutover loads of S4 rwb-litigation, P6 rwb-comms, S9 rwb-partner and P3 rwb-case, and their CON, APP and DB stories.
- The SCR-45 Data quality and reconciliation console as a product screen, which is RWB-AD-019, and every other screen.
- The cutover plan, the business date calendar and the sign-off record.
- ACE ingestion, the v_ace_* views and the court-record interfaces, which are RWB-ACE-001.
- LitigationWorkflow, hearings, judgments, enforcement and the auction ladder, which are the S4 app stories.
- Platform configuration, base hosts, retention policy and the evidence repository.
- The other data migration keys of wave 4 and their harnesses.

### 20. Remaining delivery steps

- Size the story (RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish the rwb-source-data 5.1.0 fake and add the reconciliation result reads to the yaml file (rwb-source-data contract owner).
- Settle the break-detail store (rwb-source-data data architect; GAP-1508, NEW-GAP-S2B-03). The court record link is the carried lawsuit_no (RD-P1-068).
- Add the authorise path to the rwb-access yaml (rwb-access contract owner) and settle a staff read of one partner instruction (rwb-partner contract owner).
- Provide the stubs and synthetic fixtures in DEV (integration lead).
- Add the new and changed test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).
