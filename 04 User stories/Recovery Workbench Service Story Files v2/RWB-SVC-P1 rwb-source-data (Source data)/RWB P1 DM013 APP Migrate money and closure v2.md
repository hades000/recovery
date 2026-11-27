# RWB-P1-DM013-APP Migrate money and closure

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-DM013-APP-14) |
| Size | Not specified in the source documents (DOR-RWB-P1-DM013-APP-16); squad sizes at refinement |
| Contract version | Not specified in the source documents (DOR-RWB-P1-DM013-APP-23); path is /v1 only |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP; not started until both are done |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-013 for the P1 cutover extract of the open proceeds matches, the closures and the write-off decisions of the open cases, its handover to the three owning services, and the cutover evidence counted from the reconciliation results. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 8 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)** I want **the P1 cutover extract of the legacy Workbench proceeds, closure and write-off decision records of the open cases, resolved to the ACE business keys and handed over to rwb-payment, rwb-writeoff and rwb-case, with the cutover evidence counted from the reconciliation results**, so that **money already received stays matched to its case, a closed case keeps its closure reason, the write-off decisions arrive with their committee dates, and no payment and no GL posting is copied**.

The legacy key is kept; what changes is who holds each table. The context pack puts no proceeds table and no write-off table in `rwb_source_data` and lists `proceeds`, `write_off` and `recovery_case` under other owners (GAP-2178; ASM-3516). The story therefore reads once, resolves twice and hands over three parts:

- **Extract, in rwb-source-data (this story).** The cutover run reads the legacy Workbench cutover dump once for the open cases at cutover, selects the `proceeds` rows, the closure facts of the case row and the `write_off` decisions, resolves `payment_code` against `v_ace_payment` and `write_off_key` against `v_ace_write_off` on the `rwb_source_data` login, and writes one file per owner with a checksum. It lands no row in `rwb_source_data` (ASM-3517).
- **Load, in the owner's own migration.** rwb-payment loads the proceeds rows into `rwb_payment` keeping each open row's matching state; rwb-writeoff loads the write-off decisions into `rwb_writeoff` keeping each `committee_date` and `tax_criteria_met`; rwb-case loads the closure facts with the case row it already migrates into `rwb_case`. Each owner uses its own schema, its own login and its own sequence (DP-15).
- **Evidence, in rwb-source-data.** Ten consecutive business dates on which the case-list reconciliation is PASS with no unexplained variance and no new REC-05 orphan on a migrated record, and on which every `payment_code` of a migrated proceeds row resolves; a break resets the count. The evidence is a read over the `reconciliation_result` rows that JOB-04 writes; this story builds neither JOB-04 nor a table for the count (ASM-3518).
- **Sign-off, in the release pipeline.** The data steward signs off in the cutover record; the legacy tables stay read-only for their retention period and the migrated records are served from the three new schemas (ASM-3519).
- **Per-service migration (DP-15).** One version on the `rwb_source_data` sequence that creates no proceeds, closure or write-off object, whose description records the extract's definition, its field list and the read-only window.
- **No screen, no REST operation, no event, no workflow.** SCR-45 Data quality is a gateway-bff composite route (DP-19; ASM-3520). The cutover is a release-pipeline command: it adds no path to `/api/recovery/source-data/v1`, publishes nothing on `rwb.source-data.events.v1` and starts no workflow on the queue rwb-source-data.

### 2. Business rationale

Money and closure are the two ends of a case. A receipt that is not matched to its case is a receipt the bank cannot account for and an officer will chase twice. A closure that arrives without its date and its reason is a case nobody can explain to audit, to the regulator or to the customer. Between the two sits the write-off decision, which carries the date the committee answered.

The legacy story states the aim in its own words: "As a data steward, I want the open proceeds matches and the closures recorded in the legacy Workbench migrated, so that money already received stays matched to its case and a closed case keeps its closure reason." Its Data table names the three entities, quoted here character for character:

> | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
> | proceeds | id, case_id, treatment_id, payment_code, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
> | write_off | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date and 5 more | DF-FIN-010 to DF-FIN-020 |

Its guardrail fixes the boundary this story keeps: "A migrated record keeps its source and its migration date, and never a copy of an ACE row." ACE holds the payment and the GL posting, and P1 reads them through `v_ace_payment` and `v_ace_write_off` on its own login; a copied payment is a payment that drifts, and nothing in the target would reconcile the copy back.

**Why one extract and three loads.** Each entity belongs to a different service, and a service writes only its own schema, with no cross-schema join and no foreign key across services (DP-01, DP-05). Only P1 can read the legacy dump once, and only P1 is the sole reader of the ACE views that hold the keys, so the extract is P1's work; each load follows the schema its owner holds (GAP-2178; ASM-3516).

**Why the evidence is P1's.** REC-05 resolves every business key on a Workbench row, `payment_code` included, against its view, and JOB-04 writes one `reconciliation_result` per check and product group for every business date (FSD P1 v3 A2.11; TSD P1 v3 T3.6). The three loads see no reconciliation, so the ten clean days are counted from rows that already exist; a break resets the count, because ten clean days that ignore a break are ten days of money that does not reconcile to ACE (ASM-3518).

### 3. Preconditions

- The Ownership Map entry is accepted: `proceeds` is P8's, `write_off` is S7's and `recovery_case` is P3's, each with the cutover migration of its own rows on its own sequence (DP-01; GAP-2178; ASM-3516).
- `RWB-PLT-E1044-CON` gives the `rwb_source_data` sequence and its baseline, so this story takes the next free version and writes one history row (DP-15; TSD P1 v3 T3.2).
- The tables and the data product catalog of `RWB-P1-E1001-APP` are live, `data_product` carrying DP13 Money and closure with one system of record (FSD P1 v3 A2.2).
- The read-only ACE views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP`: this story reads `v_ace_payment` (DF-ACE-043 to DF-ACE-054) and `v_ace_write_off` (DF-ACE-261 to DF-ACE-269) and nothing else of ACE (TSD P1 v3 T3.3, T6.3).
- JOB-04 runs for every business date and writes `reconciliation_result` with REC-01, REC-02 and REC-05; it is the build of `RWB-P1-E1011-APP`, and this story reads its rows and changes none (FSD P1 v3 A2.11).
- The gateway-bff composite route of `RWB-PLT-N001-CON` is in place, so the cutover result and its breaks are read on SCR-45 without a screen of this story's own (DP-19; ASM-3520).
- The dump fixture, the view fixture and the three contract mocks exist before the first build, so the story needs no production data (section 12.8).
- The source of the legacy dump, its format and the place that holds the sign-off are Not specified in the source documents (GAP-2178; ASM-3517).

### 4. Flow

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Release pipeline | Starts the cutover run for the cutover business date | Checks the version of the extract definition in force and the caller's Platform administration right |
| 2 | The run | Reads the legacy cutover dump once and selects the open cases' `proceeds`, closure facts and `write_off` | Counts rows per entity and records the dump's checksum |
| 3 | The run | Maps each record to its fields and to its ACE business key | Keeps `payment_code`, the case, the closed date and reason, `committee_date` and `tax_criteria_met`; drops any amount, posting date and GL field |
| 4 | The run | Resolves each key against `v_ace_payment` and `v_ace_write_off` on the service login | Marks each row resolved or orphan; lists every orphan for the data steward and, where the ACE row is missing, for the ACE team |
| 5 | The run | Writes the three parts as handover files with their checksums and row counts, each to its owning service (rwb-payment, rwb-writeoff, rwb-case) | Records the run, its counts and its orphans in the cutover record, with the load command's run record; writes nothing to `rwb_source_data` |
| 6 | Data steward | Reads the count of clean days, each a PASS result, and at ten signs off in the cutover record of the release pipeline | The legacy tables stay read-only for their retention period and the migrated records are served from the three new schemas |

### 5. Exception paths

| # | Situation | What happens | Covered by |
|---|---|---|---|
| X1 | The dump for the cutover date is absent or unreadable | The run fails before any part is written; the cutover record names the dump and the date; no count moves | AC1 |
| X2 | A record carries no `payment_code`, no case, no closed date or reason, or no `committee_date` | That record is refused and listed with its entity and its missing field; the other records of the part are not held back | AC1 |
| X3 | A `payment_code` or `write_off_key` resolves to no view row | The row is listed as an orphan for the data steward and the ACE team; the record is never deleted or changed to make the key resolve (BR-P1-011-3) | AC2 (proved by `RWB-ITG-DM013-ITG`) |
| X4 | The dump carries an ACE amount, a posting date or a GL field | The field is dropped by the mapper and the drop is counted; no copy of a payment or of a GL posting is created | AC1 |
| X5 | An owner's migration refuses its part | The part is retried once; if it still fails, the run reports the owner, the part and the checksum, and the count does not start | AC1 |
| X6 | A reconciliation result for a business date is BREAK, holds a new REC-05 orphan on a migrated record, or leaves a `payment_code` unresolved | The count resets to zero and the date, its result rows and its rows are listed (ASM-3518) | AC3 |
| X7 | The ACE batch for DP13 is not complete for the business date | The date is not counted as clean; the report shows the product stale with MSG-P1-001 and the senders of the data product see it | AC3 |
| X8 | The caller holds no Platform administration right | Refused with MSG-P4-002 and the cutover record shows the refusal; nothing is read and nothing is written | Not specified in the source documents (DOR-RWB-P1-DM013-APP-3) |
| X9 | A `v_ace_*` view fails during the run | The run fails with MSG-GEN-006 naming "ACE database"; no part and no count is written, and the rerun writes all three parts | AC1 |

### 6. INVEST check

| Letter | Check | How this story meets it | Result |
|---|---|---|---|
| I | Independent | Builds against the four H dependencies and their fakes; the three owner contracts are fixtures only, so no C or I dependency exists | Met |
| N | Negotiable | The extract definition, the handover format and the ten-day rule are stated; the file format and the dump location stay open (ASM-3517) | Met |
| V | Valuable | Money already received stays matched and a closed case keeps its reason at go-live, which is the legacy aim | Met |
| E | Estimable | The entity list, the field list, the two views and the evidence rows are all named; nothing rests on an unknown volume | Met |
| S | Small | One reader, one mapper, one resolver, one writer and one count over rows another story writes | Met |
| T | Testable | Two legacy criteria plus the exception paths, each with a fixture and a Level in section 16 | Met |

### 7. Acceptance criteria

```gherkin
Feature: Migrate money and closure

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-013 AC1)
    Given the legacy Workbench proceeds, closure and write-off decision records at cutover
    Given the rwb-payment contract mock returns the migrated proceeds row with its payment_code and its case
    Given the rwb-writeoff contract mock returns the migrated write-off decision with its committee date
    Given the rwb-case contract mock returns the migrated closure with its closed date and its closure reason
    When the migration reads them
    Then each proceeds row carries its payment_code and its case, each closure keeps its closed date and reason, and each write-off decision its committee date
    And no payment and no GL posting is copied, because both are read from v_ace_payment and v_ace_write_off

  Scenario: AC3 Cut over (legacy RWB-DM-013 AC3)
    Given ten clean days on the migrated records
    Given the rwb-case contract mock returns the migrated records served from schema "rwb_case"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema

  Scenario: AC4 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change the model does not allow
    When the migration applies that status change
    Then the change is refused and the row counts of `rwb_source_data` are unchanged
```

AC1 and AC3 are copied character for character from legacy RWB-DM-013. The four added Givens are the contract answers of the three owners — the loads are theirs, so the migrated proceeds row, the migrated write-off decision, the migrated closure and the served schema are answered by their contracts and their mocks — and they change no legacy value. AC2 Reconcile the business keys is proved across the services by `RWB-ITG-DM013-ITG` as its AC1 with `TC-DM-013-02-ITG`, over the REC-05 rows this service writes. The cutover reconciliation harness pack for money and closure is Not specified in the source documents (GAP-0453); the fixture layout of the cutover extract, the break-list fields, the report shape, the evidence format and retention, the pass or fail gate and the synthetic data set are not set here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `proceeds` is P8's, `write_off` is S7's and `recovery_case` is P3's: this story extracts and hands over, and writes no row of `rwb_payment`, `rwb_writeoff` or `rwb_case` and no other service's schema | DP-01; GAP-2178; ASM-3516 |
| BR2 | The extract carries the `payment_code` and the case of a proceeds row, the closed date and the closure reason of a closure, and the `committee_date` and `tax_criteria_met` of a write-off decision, and keeps every field the legacy Data table names | Legacy RWB-DM-013 AC1 |
| BR3 | No payment and no GL posting is copied: no ACE amount, payment date, posting date or GL field enters the extract or lands in `rwb_source_data` | Legacy RWB-DM-013 AC1 and guardrails; DP-05 |
| BR4 | `payment_code` and `write_off_key` are resolved against `v_ace_payment` and `v_ace_write_off` on the service's own login, with SELECT and nothing else | TSD P1 v3 T3.3 and T6.3; DP-05 |
| BR5 | A link to ACE is a business key with no foreign key into ACE; `payment_code` and `write_off_key` are that link and REC-05 checks it | BR-P1-001-3; FSD P1 v3 A2.11 |
| BR6 | A migrated record keeps its source and its migration date, never a copy of an ACE row; each owner sets both and this story reads them through the owner's contract | Legacy RWB-DM-013 guardrails |
| BR7 | A REC-05 orphan never deletes or changes a Workbench record: it is listed for the data steward and, where the row is missing in ACE, for the ACE team | FSD P1 v3 A2.11.3.1 BR-P1-011-3 |
| BR8 | The cutover evidence is ten consecutive business dates of PASS reconciliation results with no unexplained variance and no new REC-05 orphan on a migrated record; a break resets the count and no counter table is created | Legacy RWB-DM-013 AC3; ASM-3518 |
| BR9 | The service runs its own Flyway sequence in its own schema; this version creates no money or closure object and records the extract, its field list and the read-only window in its description | DP-15; TSD P1 v3 T3.2 |

BR1, BR5 and BR9 are the boundary, proved in the history and in the refusal to write another schema. BR2, BR3 and BR6 are the extract's content, proved by the field list and by the absence of any ACE amount, posting date or GL field. BR4 is the grant. BR7 is an orphan, listed and never repaired in place. BR8 is the cutover gate.

### 9. State transitions

No case, no proceeds row and no write-off decision changes state here: the case state machine is rwb-case's, the matching state is rwb-payment's and the committee state is rwb-writeoff's. The moves below are the states of the cutover itself, as the cutover record and SCR-45 show them.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The run reads the dump for the cutover date | The dump is the dump of that business date | Extract ready: every open proceeds row holds its `payment_code` and its case, every closure its closed date and reason, every write-off decision its `committee_date`; nothing is written to `rwb_source_data` |
| Extract ready | The three owners load their part through their own migrations | Each part is accepted with its checksum | Loaded: the rows are served from `rwb_payment`, `rwb_writeoff` and `rwb_case` with their source and migration date; the count is zero |
| Loaded | JOB-04 writes a PASS result set for a business date | No unexplained variance, no new REC-05 orphan, every `payment_code` resolved | One clean day: the count moves to the next business date |
| One clean day | JOB-04 writes a BREAK result, raises a REC-05 orphan or leaves a `payment_code` unresolved | The business date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy tables stay read-only for their retention period and the migrated records are served from the three new schemas |

This story announces no move by event, because a cutover is not a business event of a payment, a case or a write-off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the clean-day count, signs off in the cutover record (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the resolver, the handover and the count; runs the tests; applies the version |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result and the reconciliation results; each holds Platform administration R |
| The ACE team lead | Receives every listed orphan whose row is missing in ACE and answers for the view row |
| The rwb-payment, rwb-writeoff and rwb-case service identities | Load the handed-over parts into their own schemas; this story never uses their logins |
| The rwb-source-data service identity | Reads the dump and the two views and writes one history row; holds no write on any other schema and none on `public` |

The legacy permission row for the key is kept unchanged: Platform administration R for the six roles above. The role codes are rows of rwb-access; this story adds no role and no grant.

### 11. Data

| BR Field ID | Entity | Field | Read, extract or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code`, the closed date and the closure reason of the row | Extracted from the dump and handed over; P3's table, never written here |
| DF-FIN-001 to DF-FIN-009 | `proceeds` | `id`, `case_id`, `treatment_id`, `payment_code`, `source`, `amount` and the rest of the 9 fields | Extracted and handed over to rwb-payment; P8's table, never written here |
| DF-FIN-010 to DF-FIN-020 | `write_off` | `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date` and the rest of the 11 fields | Extracted and handed over to rwb-writeoff; S7's table, never written here |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` | `payment_code`, `account_key` and the other 10 view fields | Read only, to resolve the key; never copied |
| DF-ACE-261 to DF-ACE-269 | `v_ace_write_off` | `write_off_key`, `account_key`, `amount`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product`, `source_system`, `data_as_of` | Read only, to resolve the key; no field of it enters the extract |
| DF-OPS-010 to DF-OPS-020 | `data_contract` | `contract_code`, `source_system`, `status`, `published_at` | Read only, to name the DP13 contract in force in the cutover record |

The `amount` of `proceeds` and the `amount` of `write_off` are Workbench facts and travel with their record; the `amount` of `v_ace_write_off` is an ACE fact and is never copied. P1 extracts the proceeds rows, the closures and the write-off decisions, hands proceeds to rwb-payment, write-off decisions to rwb-writeoff and closures to rwb-case, and copies no payment and no GL posting. How the matching state is kept through the handover is Not specified in the source documents (GAP-0543). The extract carries personal data as Data Classification v5 classes it, all Confidential: the indirect identifiers `case_no`, `primary_person_key` and `payment_code`, and the customer data `amount` of `proceeds` and of `write_off`, `tax_criteria_met` and `committee_date`; `write_off_key`, an indirect identifier, is read only to resolve the key. The Confidential handling rules apply: encrypted at rest and in transit, shown within the role's scope with indirect identifiers masked in UAT, export within the role's scope and logged, and no clear key or customer value in logs. No name, identity number, contact point or address is read. Reference data read: the `data_contract` view only (DF-OPS-010 to DF-OPS-020); the parameters read are Not specified in the source documents (DOR-RWB-P1-DM013-APP-20), and DP-06 and DP-07 are not applied by this story.

### 12. Contract

**12.1 REST operations provided**

None. The legacy story states "No endpoint in this story": the cutover is a release-pipeline command that reads a dump and hands over a file, so no caller could address it, and no path of `/api/recovery/source-data/v1` is added. The breaks and the result are read through the reconciliation result list that `RWB-P1-E1011-APP` already publishes (API-P1-003), which this story neither claims nor changes.

**12.2 REST operations consumed**

None at run time. The run reads its own dump, resolves its keys against its own views on its own login and writes its own history row. The three owner contracts are used as fixtures and as the read-back of what was loaded, which adds no run-time dependency (section 12.8).

**12.3 Events published**

None. No Kafka event, no outbox row and no schema on `rwb.source-data.events.v1`. AceDataReady and AceDataLate belong to `RWB-P1-E1013-APP`; ProceedsMatched and WriteOffApproved belong to the two owner services.

**12.4 Events consumed**

None. The release pipeline starts the cutover; the reconciliation that produces the evidence is started by AceDataReady in `RWB-P1-E1011-APP`.

**12.5 Workflows and activities**

None added. JOB-04, whose results are counted, is the event-triggered workflow of `RWB-P1-E1011-APP` on the queue rwb-source-data; the payment matching of JOB-07 is rwb-payment's and the write-off scan of JOB-16 is rwb-writeoff's. This story creates and changes no workflow, activity or child workflow.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job: the cutover is a one-off pipeline run and the daily count is a read over rows another story's trigger already writes.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the cutover evidence, written by JOB-04 (`RWB-P1-E1011-APP`) |
| `data_contract` | `rwb_source_data` | P1 | Read only: names the DP13 contract in force |
| `proceeds` | `rwb_payment` | P8 | Not owned and not written here: extracted to a file and loaded by its owner's migration |
| `write_off` | `rwb_writeoff` | S7 | Not owned and not written here: extracted to a file and loaded by its owner's migration |
| `recovery_case` | `rwb_case` | P3 | Not owned and not written here: the closure facts travel with the case row |

`rwb_source_data` holds no proceeds table and no write-off table, and this story adds none. No statement names a table in `public` and none names another service's schema; the only cross-schema read is the granted `recovery.v_ace_*` view (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | The `proceeds`, closure and `write_off` rows of the open cases at cutover, synthetic: proceeds row "PRC-SYN-000601" with `payment_code` "PAY-SYN-000601" on case "RW-2026-000601"; the closure of that case with closed date "2026-11-20" and reason "PAID_IN_FULL"; write-off decision "WO-SYN-000601" with `committee_date` "2026-11-18" | AC1 and AC3, and X1 to X4, from Day 1 |
| View fixture (`v_ace_payment`, `v_ace_write_off`) | The two views as synthetic rows, with one row for "PAY-SYN-000601" and one for "WO-SYN-000601", and none for "PAY-SYN-000777" | AC1 key resolution and the orphan path, X3 |
| rwb-payment contract mock (`GET /cases/{caseId}/payments`) | The migrated proceeds row with its `payment_code`, its case and its matching state, served from `rwb_payment` | AC1 and the load report |
| rwb-writeoff contract mock (`GET /write-offs`) | The migrated write-off decision with its `committee_date`, served from `rwb_writeoff` | AC1, X5 and the load report |
| rwb-case contract mock (`GET /cases/{caseId}`) | The migrated closure with its closed date and its reason, served from `rwb_case` | AC1 and AC3 |
| Reconciliation fixture (`reconciliation_result` rows) | PASS result sets for ten consecutive business dates and one BREAK set for the reset case | AC3, X6 and X7 |

Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change fails a test rather than passing silently.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | A pipeline command; the result is read through API-P1-003, which another story owns |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule; JOB-04, JOB-07 and JOB-16 are other stories' |
| File | None | One | The legacy cutover dump, read once per run, and the three handed-over parts with their checksums |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and queue rwb-source-data are named for completeness and used by no part of this story.

| Component | Type | Responsibility |
|---|---|---|
| MoneyClosureExtractReader | Repository | Reads the dump once and selects `proceeds`, the closure facts of `recovery_case` and `write_off` with the fields of the legacy Data table; no write, no `public` table |
| MoneyClosureKeyMapper | Service | Maps each record to its fields and drops every ACE amount, payment date, posting date and GL field |
| AceKeyResolver | Service | Resolves `payment_code` against `v_ace_payment` and `write_off_key` against `v_ace_write_off` on the service login; marks each row resolved or orphan (DP-05) |
| CutoverHandoverWriter | Service | Writes one part per owner with its checksum and its counts, and records the run, its counts and its orphans in the cutover record |
| CleanDayCounter | Service | Counts consecutive business dates whose `reconciliation_result` rows are PASS with no new REC-05 orphan and no unresolved `payment_code`; resets on a break (ASM-3518) |
| V1__money_closure_cutover.sql | Flyway version | Records the extract's definition, its field list and the read-only window in its description; creates no table, column or index (DP-15) |

**Build order.** The reader and the mapper first, against the dump fixture; then the resolver and the handover writer, against the view fixture; then the counter, against the reconciliation fixture; the version is applied and re-applied last, to prove the second run is a no-op. DP-19 is satisfied by reading, not building: SCR-45 is the composite route of `RWB-PLT-N001-CON` over API-P1-003.

**Estimate.** Five components, one SQL version and four fixtures: a small APP story, whose largest cost is the field-by-field mapping of the 20 fields of the three legacy entities.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-GEN-006 | Error | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

MSG-P1-001 and MSG-P1-012 are the two messages the legacy key carries and are copied unchanged; they are raised by the reconciliation of `RWB-P1-E1011-APP` and read here as the reason a date is not counted clean. MSG-GEN-001 carries the missing field of X2, MSG-GEN-006 the failing view of X9, and MSG-P4-002 the refusal of X8. No message text is held in code: the texts are rows of the message catalog in force.

### 15. Screens and states

This story renders no screen. The legacy screen SCR-45 Data quality stays the read of the result in its Loading and breaks states, and it is a gateway-bff composite route over the published reads (DP-19; H `RWB-PLT-N001-CON`; FSD P1 v3 SCR-45 "Reconciliation breaks, referential completeness (REC-05), quality measures and stale data products"). The reconciliation result list of API-P1-003, published by `RWB-P1-E1011-APP`, is the read behind it.

| State | What the cutover record and SCR-45 show |
|---|---|
| Loading | The dump read once, the counts of the three parts, the checksum, and the orphan list |
| Loaded | Each part accepted by its owner, the load reported through the three contracts, and a count of zero |
| Ten clean days running | The business dates counted, each with its PASS results |
| Break | The date of the break, its BREAK rows, its orphan or its unresolved key, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy tables read-only for their retention period |
| Empty | Not specified in the source documents (CG-ALL-1986) |
| Error | A run that cannot start: the failed state with the dump and the business date named and no part written |
| No access | A caller without the Platform administration right is refused with MSG-P4-002 |

A run that cannot start shows on SCR-45 in its failed state with the dump and the business date named and no part written, so a cutover that did not happen is never read as one that did.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-013-01 | AC1; BR1, BR2, BR3, BR4, BR6, BR9 | End to end | The dump fixture with proceeds row "PRC-SYN-000601" carrying `payment_code` "PAY-SYN-000601" on case "RW-2026-000601", the closure with closed date "2026-11-20" and reason "PAID_IN_FULL", and write-off decision "WO-SYN-000601" with `committee_date` "2026-11-18"; the view fixture with one row per key; a dump row carrying an ACE amount and a GL product, to prove both are dropped; the row counts of the three entities in `rwb_source_data` before and after; the version applied once and again |
| TC-DM-013-03 | AC3; BR5, BR7, BR8 | End to end | The reconciliation fixture with PASS sets for ten consecutive business dates, then one BREAK set, one new REC-05 orphan and one unresolved `payment_code`; a business date whose ACE batch is absent; the three contract mocks answering the migrated rows with their source and migration date from `rwb_payment`, `rwb_writeoff` and `rwb_case` |
| TC-DM-013-04 | Access refusal; BR4 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present for the contrast; the row counts of `rwb_source_data` before and after the refusal |
| TC-DM-013-05 | AC4 | Component | Not specified in the source documents (NEWAC-RWB-P1-DM013-APP-AC4) |

TC-DM-013-01 and TC-DM-013-03 are End to end because the run leaves the service's own boundary: it reads a file, resolves keys against views and reports three loads that other services performed. TC-DM-013-04 is Component because it exercises the guard at the boundary of the published operation. AC2 and its test case are proved across the services by `RWB-ITG-DM013-ITG` as `TC-DM-013-02-ITG`, where the REC-05 reconciliation of the migrated business keys is asserted; the live matching of a payment that arrives after cutover belongs to the rwb-payment story of the same legacy key and is not tested here.

### 17. Guardrails

- No business value in code: the cutover date, the handover location and the retention period are configuration of the release pipeline; the story writes no threshold, no percentage, no currency amount and no date.
- No clear personal data in logs, tests or prompts: the extract and its handover parts carry Confidential personal data (section 11) and are handled by the Confidential rules of Data Classification v5; the fixtures are synthetic, logs hold the id of the read, a code or an id and never a clear key or customer value, and no name, identity number, contact point or address enters the extract.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table named in any statement.
- No copy of an ACE row: no ACE amount, payment date, posting date or GL field enters the extract (BR3).
- `rwb_source_data` holds no proceeds and no write-off table before or after this story; a closure is a case fact in `rwb_case`, not a record of its own (BR1).
- No cross-schema write: each owner loads its part through its own migration, and this story holds no grant on any of the three schemas (DP-01).
- An orphan is listed and never repaired: no migrated record is deleted or changed to make a key resolve (BR7).
- A break is never waived: a BREAK result, a new orphan or an unresolved key resets the count, and a stale product is never counted as a clean day (BR8; MSG-P1-001).
- The sign-off and the count are artefacts of the release, not Workbench rows: no table is invented for either (ASM-3518; ASM-3519).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).

### 18. Traceability

| Legacy RWB-DM-013 item | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, epic RWB-SVC-P1; `proceeds` is P8's, `write_off` is S7's and the closure is P3's |
| Epic | E2, release 31 December 2026 | Wave 4 tag from EP08; release 31 December 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | RWB-P1-E1001-APP (tables and catalog) and RWB-P1-E1069-APP (views and grant) |
| Decision | DL25 (open; assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602) | BR8, BR9: the ten clean days and the zero-tolerance cutover gate |
| Data | `recovery_case` DF-CAS-001 to DF-CAS-055; `proceeds` DF-FIN-001 to DF-FIN-009; `write_off` DF-FIN-010 to DF-FIN-020 | Section 2 quotation; section 11; AC1; TC-DM-013-01 |
| Endpoints | "No endpoint in this story." | Section 12.1; API-P1-003 is the read of the breaks and belongs to RWB-P1-E1011-APP |
| Screen and states | SCR-45 Data quality: Loading; breaks | Section 15; the screen is a gateway-bff composite route |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR3, BR6; AC1; section 17 |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Section 7; TC-DM-013-01 and TC-DM-013-03 |
| AC2 and TC-DM-013-02 | Reconcile the business keys, REC-05 | Proved by RWB-ITG-DM013-ITG as its AC1 and TC-DM-013-02-ITG; not copied here |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_payment` and `v_ace_write_off` are read by this service on its own login, to resolve the two keys and to copy nothing (section 13) |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence for the extract's record, and one load sequence for each owner (BR9, AC1, AC3) |
| DP-19 | Template and Rules §R5.5 | The cutover result and its breaks are read on SCR-45 through the gateway-bff composite route (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-45 |
| RWB-P1-E1001-APP | App development | H: the tables of this service and the data product catalog DP13 resolves in |
| RWB-P1-E1069-APP | App development | H: the read-only views, the login and the grant |
| RWB-P1-E1011-APP | App development | Writes `reconciliation_result` through JOB-04, which is the cutover evidence |
| RWB-ITG-DM013-ITG | Integration | Proves AC2 across the services and asserts the keys, the break list and the cutover |
| The rwb-payment, rwb-writeoff and rwb-case stories of RWB-DM-013 | App development | Load the three handed-over parts into their own schemas and own the live behaviour afterwards |

### 19. Out of scope

- The load of a proceeds row, a closure or a write-off decision: each belongs to the service that owns the schema, and none is written here.
- The live proceeds matching, the payment event and the posting file of rwb-payment, and the committee, eligibility and posting of rwb-writeoff.
- The case state machine, the case record migration and the closure action of rwb-case.
- JOB-04, REC-01, REC-02, REC-05 and the reconciliation report: they are the build of `RWB-P1-E1011-APP`, and this story only reads their result rows.
- The data-quality console, its deployment and the SCR-45 screen itself: they belong to the P1 console stories and to the gateway-bff route.
- The ACE ingestion of ALS and GL, the continuance of `v_ace_payment` and `v_ace_write_off`, and the Interface Specifications of INT-02 and INT-16: the ACE team owns them.
- The retirement of the legacy Workbench tables: the retention period runs outside the Workbench and no statement of this story drops or truncates a table.
