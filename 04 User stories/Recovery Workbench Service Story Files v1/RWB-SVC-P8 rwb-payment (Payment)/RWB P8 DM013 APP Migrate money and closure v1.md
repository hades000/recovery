# RWB-P8-DM013-APP Migrate money and closure

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-DM013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P8-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-payment arm of RWB-DM-013 — the cutover load of the open proceeds matches into `rwb_payment`, the money side of a closure kept with the receipt that closed it, and the refusal to copy a payment or a GL posting — is issued for the first time. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)** I want **the open proceeds matches of the cutover handover loaded into `rwb_payment` with each receipt's payment reference, case, treatment, source, amount, received date and match value exactly as the legacy Workbench recorded them, and the money side of each closure kept with the receipt that closed it**, so that **money already received stays matched to its case at go-live, a closed case keeps its closure money fact, and no payment and no GL posting is copied**.

The legacy key is split across three slices and this is the payment arm of it:

- **Extract and cut over, in rwb-source-data.** `RWB-P1-DM013-APP` reads the legacy dump once, resolves `payment_code` against `v_ace_payment` on its own login and hands over one file per owner with a row count and a checksum. It owns AC1 and AC3 of the legacy key.
- **Load the payment part, in rwb-payment (this story).** One row per open receipt lands in `proceeds` in `rwb_payment`, with its match value copied from `LOV-MATCH` and never re-decided, and its payment reference kept as the business key of the row.
- **Load the other two parts elsewhere.** `rwb-writeoff` loads the write-off decisions with their committee dates, and `rwb-case` carries the closure facts with the case row it already migrates. This story writes neither, and no closure date and no closure reason enters `rwb_payment`.
- **Reconcile the business keys across the services.** That is legacy AC2, owned by `RWB-ITG-DM013-ITG`; this story lists the rows it refuses and proves that its own load leaves no row behind that the handover did not hold (AC5, AC6 of section 7).
- **One table, one sequence.** `proceeds` is the only table the context pack gives this service. The load is one version on the per-service Flyway sequence in `rwb_payment` (DP-15); the monolith's `V`-numbered migration is not reused (GAP-2533; ASM-4186).
- **No screen, no operation, no event, no workflow.** SCR-45 Data quality is the gateway-bff composite route of `RWB-PLT-N001-CON` (DP-19). The load is a release-pipeline command: it adds no path to `/api/recovery/payment/v1`, publishes nothing on `rwb.payment.events.v1`, and `ProceedsMatched` stays with the live matching of `RWB-P8-E2008-APP`. The load's command, its rights and its run record are Not specified in the source documents (GAP-2533; ASM-4186).

### 2. Business rationale

Money and closure are the two ends of a case. A receipt that is not matched to its case at go-live is a receipt the bank cannot account for, and an officer chases it a second time. A closed case whose money side was never migrated reads as an open balance to every report built on `rwb_payment`.

The legacy story states its aim in its own words: "As a data steward, I want the open proceeds matches and the closures recorded in the legacy Workbench migrated, so that money already received stays matched to its case and a closed case keeps its closure reason." Its Data table names the three entities, quoted here character for character:

> | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
> | proceeds | id, case_id, treatment_id, payment_code, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
> | write_off | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date and 5 more | DF-FIN-010 to DF-FIN-020 |

Its guardrail fixes the boundary this story keeps: "A migrated record keeps its source and its migration date, and never a copy of an ACE row." ACE holds the payment and the GL posting, and no service but rwb-source-data reads the `recovery.v_ace_*` views, so the receipt facts arrive on a handover file and the reference to the ACE payment stays a business key with no foreign key into ACE (DP-05).

**Why the load is this service's.** `proceeds` is in `rwb_payment` and a service writes only its own schema (DP-01); only the payment service can write a match value that its own matching of the next day will read. **Why it is a load and not a match.** The match value is a legacy fact of the business date it was decided on; re-deciding it at cutover would rewrite history that the reconciliation and the audit trail already carry.

### 3. Preconditions

- `RWB-P1-DM013-APP` runs for the cutover business date and hands over the payment part with its row count, its checksum and a resolution stamp per row (DP-05).
- The `proceeds` baseline of `RWB-P8-E2008-CON` is in place in the environment where the version is applied. That is a deploy order and not a build dependency: the plan gives this slice no H row, and the load is built against the baseline fixture from Day 1 (GAP-2533; ASM-4191).
- `RWB-PLT-E1044-CON` gives the `rwb_payment` sequence, so this story takes the next free version and writes one history row (DP-15).
- The handover file, its format, its location and its checksum are Not specified in the source documents (GAP-2533; ASM-4187), and so are the load's command, its rights and its run record (GAP-2533; ASM-4186).
- The handover fixture, the baseline fixture and the authorise fake exist before the first build, so the story needs no production data and no ACE row (section 12.8).
- The caller holds the Platform administration right R of the legacy permission row; the guard is drawn from the platform library and its fake.

### 4. Flow

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Release pipeline | Starts the load for the cutover business date under the `rwb_payment` service identity | Checks the caller's Platform administration right and the version of the load definition in force |
| 2 | The load | Reads the handover once and counts its rows against the row count and the checksum | A file that does not match is refused whole and nothing is written |
| 3 | The load | Maps each handover row to the nine fields of `proceeds` and keeps every value as recorded | `matched_to` is copied from `LOV-MATCH`, `source` from `LOV-PROCEEDS-SRC`; no rule is evaluated and no match is re-decided |
| 4 | The load | Refuses a row whose payment reference carries no resolution stamp | The row is listed once for the data steward; the other rows of the file are loaded |
| 5 | The load | Writes one proceeds row per accepted handover row with its provenance and its migration date | One transaction per batch of rows; a second run for the same cutover date writes no second row |
| 6 | Data steward | Reads the load report and the row counts | The legacy tables stay read-only for their retention period and the migrated receipts are served from `rwb_payment` |

### 5. Exception paths

| # | Situation | What happens |
|---|---|---|
| X1 | The handover for the cutover business date is absent, unreadable, or its row count or checksum does not match | The load is refused whole before any row is written; the load report names the file and the date |
| X2 | A handover row carries no id, no case, no `source` or no `matched_to`, or a value outside `LOV-MATCH` or `LOV-PROCEEDS-SRC` | The row is refused and listed with its entity and its field; the other rows of the batch are not held back (MSG-GEN-001) |
| X3 | A row's payment reference carries no resolution stamp | The row is not loaded and is listed once for the data steward with its payment reference; it is never repaired in place (AC5) |
| X4 | The same row is written twice, or a second run starts for a cutover date already loaded | The business key refuses the duplicate and the run is a no-op; no second row and no error (AC4) |
| X5 | The handover carries an ACE amount, a GL amount or a posting body | No ACE row and no GL posting is created; the posting reference is kept as the reference string only (AC3) |
| X6 | The version is applied in an environment where the `proceeds` baseline is absent | The version fails before the load runs; nothing is loaded and the report names the baseline |
| X7 | The caller holds no Platform administration right | Refused with MSG-P4-002 before the file is read; nothing is read and nothing is written (AC6) |

### 6. INVEST check

| Letter | Check | How this story meets it |
|---|---|---|
| I | Independent | No H, C, I or X row; built against the handover fixture, the baseline fixture and the authorise fake |
| N | Negotiable | Field mapping, refusal list and idempotency are stated; the file format and the command stay open (ASM-4186; ASM-4187) |
| V | Valuable | Money already received stays matched to its case at go-live, with no copied payment and no copied GL posting |
| E | Estimable | Nine fields, one table, one version and four fixtures; no volume rests on an unknown |
| S | Small | One reader, one mapper, one writer, one gate, one report |
| T | Testable | Six criteria and four test cases, each with a fixture and a Level in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Migrate money and closure

  Scenario: AC1 Load the open proceeds matches (new, D-RCV-60)
    Given the rwb-source-data cutover handover for the cutover business date holds the resolved proceeds rows of the open cases
    Given handover row "PRC-SYN-000601" with payment reference "PAY-SYN-000601", case "RW-2026-000601", treatment "TRT-SYN-0701", source "CUSTOMER", amount 12,500.00, received date "2026-11-19" and match "INSTALLMENT"
    When the load runs for the cutover business date
    Then one proceeds row exists in rwb_payment for "PRC-SYN-000601" with those nine values unchanged
    And the row keeps its migration provenance and its migration date
    And no rule is evaluated and no match value is changed

  Scenario: AC2 The closure money side is kept and no case fact is written (new, D-RCV-60)
    Given the handover holds a proceeds row of a case closed in the legacy Workbench with match "SETTLEMENT"
    When the load runs
    Then the row is loaded with match "SETTLEMENT" as recorded
    And no closed date, no closure reason and no case status is written to rwb_payment
    And the load creates no proceeds row that the legacy Workbench did not hold

  Scenario: AC3 No payment and no GL posting is copied (new, D-RCV-60)
    Given a handover row that carries a posting reference to the ACE payment it settles
    When the load runs
    Then rwb_payment holds no copy of the ACE payment row and no GL posting row
    And the posting reference is kept only as the reference string of the proceeds row
    And the amount and the received date stay the Workbench's recorded facts, stamped with their source

  Scenario: AC4 A repeated load is idempotent (new, D-RCV-60)
    Given the load completed for the cutover business date with the rows of AC1
    When the load is run again for the same cutover business date
    Then rwb_payment still holds one proceeds row per handover row
    And no duplicate row, no second event and no error is produced

  Scenario: AC5 A row whose key is not resolved is listed and not loaded (new, D-RCV-60)
    Given handover row "PRC-SYN-000777" whose payment reference "PAY-SYN-000777" carries no resolution stamp
    When the load runs
    Then no proceeds row is written for "PRC-SYN-000777"
    And the row is listed once for the data steward with its payment reference and its reason
    And the other rows of the handover are loaded

  Scenario: AC6 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a caller whose Platform administration right R is absent
    When the caller starts the load
    Then the load is refused with MSG-P4-002
    And nothing is read and nothing is written
```

The legacy key's three criteria are owned by the other two slices: AC1 (extract) and AC3 (cut over) by `RWB-P1-DM013-APP`, and AC2 (reconcile the business keys) by `RWB-ITG-DM013-ITG`. This story therefore copies no legacy criterion and carries six criteria of its own, each tagged `(new, D-RCV-60)`, and each tests only the load this story delivers: the rows land as recorded, the closure money side is kept without a case fact, no payment and no GL posting is copied, a second run is a no-op, an unresolved key is listed, and a caller without the right is refused. Every fixture value is synthetic.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `proceeds` in `rwb_payment` is the only table this story writes, and it reads no other service's table and no ACE view | DP-01, DP-05; context pack P8 ownership rows |
| BR2 | Each loaded row carries the nine fields of the legacy Data row with the values the legacy Workbench recorded | Legacy RWB-DM-013 AC1; TSD P8 v2 T3.1 |
| BR3 | `matched_to` and `source` are copied from `LOV-MATCH` and `LOV-PROCEEDS-SRC`; the load evaluates no rule and re-decides no match | TSD P8 v2 T3.2; section 1 |
| BR4 | No payment and no GL posting is copied: no ACE amount, no GL body and no posting row enters `rwb_payment`; the posting reference is a reference string | Legacy RWB-DM-013 AC1 and guardrails; DP-05 |
| BR5 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | Legacy RWB-DM-013 guardrails (ASM-4188) |
| BR6 | The payment reference is the business key of the row and stays a link into ACE with no foreign key; `account_payment_id` is written only where the handover gives the ACE payment identifier | Legacy RWB-DM-013; TSD P8 v2 T3.1 (ASM-4189) |
| BR7 | A second run for the same cutover date writes no second row: the row is keyed on the handover id and its payment reference | Legacy RWB-DM-013 AC3; ASM-4190 |
| BR8 | A row whose key does not resolve is listed and never repaired, deleted or changed to make it resolve | Legacy RWB-DM-013 AC2 (owned by `RWB-ITG-DM013-ITG`); FSD P8 v3 A1.4 |
| BR9 | One version on the per-service sequence in `rwb_payment`; a later change is a new version with its own history row | DP-15; TSD P8 v2 T3.1 (ASM-4191) |

BR1 and BR4 are the boundary, proved by the schema and by the absence of any ACE copy. BR2, BR3 and BR6 are the mapping, proved field by field. BR5 and BR7 are the provenance and the repeat. BR8 is the orphan, listed and never repaired. BR9 is the sequence.

### 9. State transitions

No case state, no plan state and no match state moves here: the case state machine is rwb-case's and the matching state is rwb-payment's live matching. The moves below are the states of the load itself, as the load report shows them.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The load reads the handover for the cutover date | Row count and checksum match | Handover accepted: every row mapped, every unresolved row listed, nothing written yet |
| Handover accepted | The first batch is committed | Every accepted row carries the nine fields and its provenance | Loading: the rows land in `proceeds` with their match values unchanged |
| Loading | The last batch is committed | No batch failed | Loaded: one row per accepted handover row; the report carries the counts and the refusal list |
| Loading | A batch fails | A write error or a refused value | Refused: the batch is rolled back, the row is listed with its field and the earlier batches stand |
| Loaded | The load is started again for the same cutover date | The business key is already present | No change: no second row, no second event and no error |
| Refused, or Loaded with refusals | The data steward reads the report | The count of clean days is ten, counted by P1 | Signed off: the legacy tables stay read-only for their retention period and the receipts are served from `rwb_payment` |

The load announces no move by event, because a cutover is not a business event of a payment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Starts the load for the cutover date, reads the load report and its refusal list, signs off (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the writer, the gate and the report; runs the tests; applies the version |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the load report and the row counts; each holds Platform administration R |
| The rwb-source-data service identity | Produces the handover; this story never uses its login |
| The rwb_payment service identity | Reads the handover file and writes `proceeds` and one history row; holds no write on any other schema and none on `public` |
| The ACE team lead | Answers for the ACE payment row behind a payment reference that does not resolve |

The legacy permission row is kept unchanged: Platform administration R for the six roles above. The role codes are rows of rwb-access; this story adds no role and no grant.

### 11. Data

| BR Field ID | Entity | Field | Read, extract or write |
|---|---|---|---|
| DF-FIN-001 to DF-FIN-009 | `proceeds` | `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to`, `posting_ref` | Written by the load into `rwb_payment`, one row per accepted handover row, values as recorded |
| TSD P8 v2 T3.0 | `proceeds` | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Written by the load with the values the baseline fixes; `created_by` is the service identity and `created_at` the load time |
| Legacy `payment_code` | handover and `proceeds` | the receipt's business key | Read from the handover and kept as the payment reference of the row; resolved into `account_payment_id` where the ACE payment identifier is given (ASM-4189) |
| `flyway_schema_history` | `rwb_payment` | `version`, `description`, `checksum` | Written once at deploy, by the load's own version (DP-15) |
| Legacy `recovery_case`, `write_off` | legacy Workbench | the case row and the write-off decision | Read only through the handover; never written here |

The load carries a business reference and no personal identifier, so no name, identity number, contact point or address is read. The closure date, the closure reason and the write-off decision stay with their owners: rwb-case and rwb-writeoff.

### 12. Contract

**12.1 REST operations provided**

None added. The two operations of the service — `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on base `/api/recovery/payment/v1` — are published by `RWB-P8-E2008-CON` and are neither claimed nor changed here. The load is a release-pipeline command addressed by the cutover record and not by a path; its command, its rights and its run record are Not specified in the source documents (GAP-2533; ASM-4186).

**12.2 REST operations consumed**

None at run time. The receipt facts arrive on the handover file that `RWB-P1-DM013-APP` writes, and the authorise check is drawn from the platform guard library and its fake (section 12.8). No other service is called by the load, so no C row is added and no timeout, retry or circuit breaker applies.

**12.3 Events published**

None. The load writes no outbox row and no schema on `rwb.payment.events.v1`. `ProceedsMatched` (EV-25) is published by the live matching of `RWB-P8-E2008-APP`; the other two events of the service are `TreatmentBooked` (EV-11) and `PaymentMissed` (EV-12).

**12.4 Events consumed**

None. A cutover is started by the release pipeline and by no event.

**12.5 Workflows and activities**

None added. The load is not a workflow and holds no activity; JOB-07 payment matching and JOB-08 booking confirmation are the builds of `RWB-P8-E2008-APP` and of the posting stories, and this story changes neither. It starts nothing on the queue rwb-payment.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job: the load runs once per cutover business date and the daily work that follows is JOB-07's.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `proceeds` | `rwb_payment` | P8 | Written by the load: one row per accepted handover row, keys as the baseline fixes them |
| `flyway_schema_history` | `rwb_payment` | P1 (library), created in `rwb_payment` | Writes one row for its own version at deploy |
| `write_off` | `rwb_writeoff` | S7 | Not owned and not written: loaded by that owner's migration |
| `recovery_case` | `rwb_case` | P3 | Not owned and not written: the closure facts travel with the case row |

No statement names a table in `public`, another service's schema or a `recovery.v_ace_*` view; the load reads a file and writes its own schema (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Cutover handover fixture | The payment part of the P1 extract for a synthetic cutover date: row "PRC-SYN-000601" with payment reference "PAY-SYN-000601" on case "RW-2026-000601" and match "INSTALLMENT", a row of a closed case with match "SETTLEMENT", and row "PRC-SYN-000777" with no resolution stamp | AC1, AC2, AC3, AC5 and X1 to X5, from Day 1 |
| Row count and checksum fixture | One handover whose count and checksum match and one whose checksum does not | AC1 and X1 |
| `proceeds` baseline fixture | The schema at the version of `RWB-P8-E2008-CON`, with the nine fields, the standard columns and the keys | AC1, AC3, AC4 and X6 |
| Authorise fake | The Platform administration right R present and absent, per role code | AC6 and X7 |
| Clock fixture | The cutover business date as an input and never as a literal | AC1 and AC4 |

Each fake is generated from a fixture or from the published contract and its version is pinned in the load report, so a change to the handover or to the baseline fails a test rather than passing silently.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | The two operations of the service belong to the baseline story |
| Kafka | None | None | No event published and none consumed |
| Temporal | None | None | No workflow, activity or schedule |
| File | None | One | The cutover handover, read once per run, and the load report written next to it |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment.cutover`. Service base `/api/recovery/payment/v1`, schema `rwb_payment`, login `rwb_payment`, topic `rwb.payment.events.v1` and queue rwb-payment are named for completeness and used by no part of this story.

| Component | Type | Responsibility |
|---|---|---|
| ProceedsHandoverReader | Repository | Reads the handover once, checks the row count and the checksum, and refuses the file whole when either differs |
| ProceedsLoadMapper | Service | Maps each handover row to the nine fields, copies `matched_to` and `source` from their lists, and drops every ACE amount, GL body and posting body |
| ProceedsLoadWriter | Repository | Writes `proceeds` in batches in one transaction each, with the keys the baseline fixes and the provenance the standard columns carry |
| ResolutionGate | Service | Refuses a row whose payment reference carries no stamp and lists it once for the data steward |
| LoadReportWriter | Service | Writes the load report: the counts, the checksum, the accepted rows, the refusals and the orphans |
| `V__proceeds_cutover_load.sql` | Flyway version | One row on the `rwb_payment` sequence; creates no table, column or index of its own (DP-15). Its name and its number are Not specified in the source documents (GAP-2533; ASM-4186) |

**Build order.** The reader and the mapper first, against the handover fixture; then the writer and the gate, against the baseline fixture and the unresolved row; then the report; the version is applied and re-applied last, to prove that a second run is a no-op. DP-19 is satisfied by reading, not building: SCR-45 is the composite route of `RWB-PLT-N001-CON` over the reconciliation reads of `RWB-P1-DM013-APP`, and this story adds no screen.

**Estimate.** Five components, one SQL version and four fixtures: a small APP story whose largest cost is the field-by-field mapping of nine fields and the two lists.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

These are the four messages of the legacy key and they are copied unchanged. MSG-GEN-001 carries the missing or invalid field of X2, MSG-P4-002 the refusal of X7, and MSG-P1-001 and MSG-P1-012 are the two the reconciliation of `RWB-P1-DM013-APP` raises and this story reads only as the reason a date is not counted clean. No message text is held in code: the texts are rows of the message catalog in force.

### 15. Screens and states

This story renders no screen. SCR-45 Data quality stays the read of the cutover result in its Loading and breaks states, and it is a gateway-bff composite route over the published reads (DP-19; FSD P8 v3 SCR-45, and the reconciliation reads of `RWB-P1-DM013-APP`). Nothing on that screen is built here.

| State | What the load report and SCR-45 show |
|---|---|
| Loading | The handover read once, its row count and checksum, and the rows mapped so far |
| Loaded | One row per accepted handover row, the counts per match value, and the batch committed |
| Refused | The file, the batch or the row, with its field, its payment reference and its reason |
| Loaded with refusals | The orphan list of the unresolved keys, each once, for the data steward and the ACE team |
| Signed off | The load report of the cutover date and the receipts served from `rwb_payment` |

A load that cannot start shows in its failed state with the file and the date named and nothing written, so a cutover that did not happen is never read as one that did.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-013-01 | AC1, AC2, AC3; BR1, BR2, BR3, BR4, BR5, BR6 | End to end | The handover fixture with row "PRC-SYN-000601" carrying payment reference "PAY-SYN-000601" on case "RW-2026-000601" with amount 12,500.00 and match "INSTALLMENT", and a row of a closed case with match "SETTLEMENT"; a handover row carrying a posting body, to prove it is dropped; the row counts of `proceeds` before and after; the version applied and re-applied |
| TC-DM-013-02 | AC5; BR8 | Component | The handover with row "PRC-SYN-000777" whose payment reference "PAY-SYN-000777" carries no stamp; the orphan list of the load report; the row count of `proceeds` for that row before and after (the business-key reconciliation is proved again by `RWB-ITG-DM013-ITG` as TC-DM-013-02-ITG) |
| TC-DM-013-03 | AC4; BR7, BR9 | End to end | The load run twice for the same cutover business date; the row count and the row keys of `proceeds` after each run; the outbox table, to prove that no event is written |
| TC-DM-013-04 | AC6; BR1 | Component | A caller whose Platform administration right R is absent in the authorise fake, starting the load; a second call with the right present for the contrast; the row count of `proceeds` before and after the refusal |

TC-DM-013-01 and TC-DM-013-03 are End to end because the run leaves the service's own boundary: it reads a file produced by another service and reports row counts that service produced. TC-DM-013-02 and TC-DM-013-04 are Component because each exercises one gate at the boundary of the load. No test case of this story claims legacy AC2: its full reconciliation across the three owners is the ITG slice.

### 17. Guardrails

- No business value in code: the cutover date, the file location, the retention period and the batch size are configuration of the release pipeline; the load writes no threshold, no percentage, no currency amount and no date.
- No personal data in logs, tests or prompts: every fixture is synthetic, a `case_id` is a business identifier and not an identity, and no name, identity number, contact point or address enters the handover, the load or the report.
- ACE data only through the owner's contract or `v_ace_*` views, and this service holds no view grant: the payment and the batch status are read by rwb-source-data and arrive on the handover (DP-05).
- No copy of an ACE row and no GL posting: no ACE amount, no posting body and no GL row enters `rwb_payment` (BR4, AC3).
- No cross-schema write: `proceeds` and the history table in `rwb_payment` are the only tables named, and the closure facts stay in `rwb_case` (BR1).
- The match value is never re-decided: the load evaluates no rule, calls no contract and publishes no event (BR3).
- An orphan is listed and never repaired: no migrated receipt is deleted or changed to make a key resolve (BR8).
- Provenance is kept: every row carries its source and its migration date, in the columns the standard record defines (BR5; ASM-4188).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15, BR9).

### 18. Traceability

| Legacy RWB-DM-013 item | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | The payment part lands in rwb-payment, epic RWB-SVC-P8; the extract stays in P1 and the write-off part in S7 |
| Epic | E2, release 31 December 2026 | Wave 4 tag from EP08 (the Arch v5 service row is wave 2); release 31 December 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | The `proceeds` baseline of `RWB-P8-E2008-CON` as a deploy order, and the handover of `RWB-P1-DM013-APP` |
| Decision | DL25 | BR7, BR9: the cutover gate and the per-service sequence |
| Data | `recovery_case` DF-CAS-001 to DF-CAS-055; `proceeds` DF-FIN-001 to DF-FIN-009; `write_off` DF-FIN-010 to DF-FIN-020 | Section 2 quotation; section 11; AC1 |
| Endpoints | "No endpoint in this story." | Section 12.1; the two operations of the service belong to `RWB-P8-E2008-CON` |
| Screen and states | SCR-45 Data quality: Loading; breaks | Section 15; the screen is a gateway-bff composite route |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10; AC6 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR4, BR5; AC3; section 17 |
| AC1 and AC3 | Copied and owned by `RWB-P1-DM013-APP` | Not copied here; the cutover gate it counts is read in section 9 |
| AC2 | Copied and owned by `RWB-ITG-DM013-ITG` | Not copied here; its orphan rule is kept in BR8 and AC5 |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | The payment facts arrive on the rwb-source-data handover and this service reads no `v_ace_*` view and no ACE table (BR1, BR4; section 12.2) |
| DP-15 | Template and Rules §R5.5 | One version on the `rwb_payment` sequence creates no object of its own and records the load in its history row (BR9; section 13) |
| DP-19 | Template and Rules §R5.5 | The cutover result and its breaks are read on SCR-45 through the gateway-bff composite route; this story builds no screen and takes no H row for the route (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P8-E2008-CON | Contract | The `proceeds` baseline and the two operations; a deploy order, not a build dependency (GAP-2533) |
| RWB-P1-DM013-APP | App development | Produces the handover and counts the clean days |
| RWB-ITG-DM013-ITG | Integration | Owns legacy AC2 and asserts the keys across the three owners |
| RWB-P8-E2008-APP | App development | Owns the live matching, JOB-07, `ProceedsMatched` and the match values this load leaves untouched |
| RWB-PLT-E1044-CON | Contract | The per-service sequence and its lint and drift gate |
| RWB-PLT-N001-CON | Contract | The gateway-bff composite route that serves SCR-45 |

The split plan carries no requirement id for this slice, so section 18 traces the criteria to the legacy key and to FEAT-PAY-04 and FEAT-PAY-10 of FSD P8 v3 rather than to a requirement row (GAP-2533).

### 19. Out of scope

- The extract of the legacy dump, the resolution of `payment_code` against the ACE view and the ten clean days: they are `RWB-P1-DM013-APP`.
- The load of a write-off decision into `rwb_writeoff` and of the closure facts into `rwb_case`: each belongs to the service that owns the schema.
- The live matching of a receipt after cutover, JOB-07, `ProceedsMatched`, `PaymentMissed` and the posting file: `RWB-P8-E2008-APP` and the posting stories of this service.
- The `proceeds` schema baseline, its keys and the two REST operations: `RWB-P8-E2008-CON`.
- The reconciliation console, its deployment and the SCR-45 screen itself: the P1 console stories and the gateway-bff route.
- The ACE ingestion of ALS and GL, the continuance of `v_ace_payment` and the Interface Specifications of INT-02 and INT-16: the ACE team owns them.
- The retirement of the legacy Workbench tables: the retention period runs outside the Workbench and no statement of this story drops or truncates a table.
