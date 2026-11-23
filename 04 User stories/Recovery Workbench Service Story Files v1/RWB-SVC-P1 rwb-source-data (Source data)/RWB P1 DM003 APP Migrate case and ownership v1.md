# RWB-P1-DM003-APP Migrate case and ownership

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-003 for the P1 cutover extract of the case and ownership records, its handover to rwb-case and its cutover evidence. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)** and **a squad member (RW-TRIBE)**, I want **the P1 cutover extract of the legacy Workbench case, case account, case party and assignment records for the open cases at cutover, mapped to the ACE business keys and handed to rwb-case for its own cutover migration, together with the cutover evidence counted from the reconciliation results**, so that **every open case keeps its owner, its queue and its history from the first day, and no account and no customer record is copied from ACE**.

The legacy key is **not withdrawn**. RWB-DM-001 and RWB-DM-002 leave under D-RCV-35 (U1) because ACE already holds their data and the Workbench loads none of it; RWB-DM-003 stays, because a case, its owner, its queue, its stage and its assignment history are Workbench records that no ACE table holds. What D-RCV-60 changes is who holds them: the Ownership Map puts `recovery_case`, `case_account`, `case_party` and `assignment` with **P3 rwb-case**, so this P1 slice extracts and hands over, and P3 loads (GAP-0521; ASM-0716).

- **Extract, in `rwb-source-data` (this story):** the cutover run reads the legacy Workbench cutover dump once for the open cases at cutover, maps every record to its ACE business key, and hands the extract over. The extract is a boundary of this story, not a table of it: it lands nothing in `rwb_source_data` and holds no case, account-link, party-link or assignment table (ASM-0717).
- **Load, in P3 rwb-case:** rwb-case loads the handed-over rows into `rwb_case` through its own cutover migration on its own Flyway sequence, so the case, its owner, its queue, its stage and its links are served from the schema of the service that owns them (DP-15; RWB-ITG-DM003-ITG §1).
- **Cutover evidence, in `rwb-source-data` (this story):** ten consecutive business dates on which the reconciliation of the case list to `v_ace_account` is PASS, with no unexplained variance and no new REC-05 orphan on a migrated record; a break resets the count (ASM-0718). The evidence is read from the `reconciliation_result` rows that JOB-04 writes; this story builds neither JOB-04 nor a table for the count.
- **Sign-off, in the release pipeline:** the data steward signs off in the cutover record of the release pipeline, and the legacy tables stay read-only for their retention period while the migrated records are served from `rwb_case` (ASM-0717; legacy AC3).
- **Per-service migration (DP-15):** one version on the sequence of `rwb_source_data` that creates no table, no column and no index for a case or an ownership row, and whose history description records the extract's definition, its field list and the read-only window. A later reader of the schema finds no copy; a later reader of the history finds why.
- **No screen of its own:** the cutover result is read on SCR-44 Interface and job monitor through the gateway-bff composite route (DP-19; H `RWB-PLT-N001-CON`), and on the reconciliation result list of this service.
- **No REST operation, no event, no workflow:** the cutover runs as a release-pipeline command, not as an API. This story adds no path to `/api/recovery/source-data/v1`, publishes nothing on `rwb.source-data.events.v1`, starts no workflow on `rwb-source-data` and writes no `rwb_case` row.

### 2. Business rationale

An open case is the unit of recovery work. It carries the case number the customer and the officer both quote, the owner who is answerable for it, the queue it waits in and the stage it has reached, and behind it the accounts under recovery and the people liable for them. On the day after cutover an officer must open a case and find all four facts, and the queue reports of the first morning must count the same work that the legacy Workbench counted on the last. A case that arrives without its owner is work nobody picks up; a case that arrives without its account link is a case whose balance nobody can see.

The legacy story states the position in its own words. Its story line is: "As a data steward, I want the Workbench case and ownership records migrated from the legacy Workbench with their ACE business keys, so that every open case keeps its owner, its queue and its history from the first day." Its Data table names the four tables it migrates, quoted here character for character:

> | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
> | case_account | id, case_id, account_key, is_primary, linked_from, linked_to | DF-CAS-024 to DF-CAS-029 |
> | case_party | id, case_id, person_key, party_role, role_from, role_to | DF-CAS-030 to DF-CAS-035 |
> | assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 4 more | DF-WRK-009 to DF-WRK-040 |

Its guardrails row then fixes the boundary that this story keeps: "No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row."

**Why P1 extracts and P3 loads.** The four tables are the case aggregate, and the Ownership Map puts them with rwb-case: Architecture v5 slide 41 gives rwb-case "case, CMMN state, queues, tasks, allocation, timers", and gives rwb-source-data "ACE view contract, extension tables, freshness, reconciliation" (Ownership Map basis; TSD P3 v3 T3.1). A service writes only its own schema, and the architecture makes that a build-breaking rule rather than a preference: "write only your own schema, no cross-schema joins or foreign keys, IDs across services, contracts for everything else", with a boundary test that fails the build on any violation (Architecture v5 slide 45; DP-01). This story therefore does what only it can do — read the legacy Workbench once, resolve the ACE business keys against the views it is the sole reader of, and hand the extract over — and leaves the insert into `rwb_case` with the service that owns the schema and its Flyway sequence. Architecture v5 slide 32 says the same for one-off bulk work: cutover loads and backfills go through service APIs "never their schemas" (GAP-0521; ASM-0716).

**Why P1 holds the evidence.** The reconciliation is P1's: slide 41 gives rwb-source-data the reconciliation, slide 44 gives it JOB-04 as an event-triggered workflow on `rwb-source-data`, and the FSD details the check that compares the case list with `v_ace_account` and resolves every business key (FSD P1 v3 A2.11). `reconciliation_result` is a P1 table in `rwb_source_data` (TSD P1 v3 T3.6, DF-OPS-118 to DF-OPS-129). So the ten clean days of AC3 cannot be counted by the load, which has no view of the reconciliation, and cannot be asserted by hand; they are counted from the results P1 already writes for every business date, and this story reads them and records the count in the cutover record (ASM-0718). A break resets the count, because ten clean days that ignore a break are ten days of a case list that does not reconcile to ACE: the failure is quiet, and the cutover is the one moment when it can still be stopped cheaply.

**What the realignment adds that the legacy story could not say.** First, the boundary: the extract is produced by the data engine and consumed by the case service, so the load needs no cross-schema grant, no shared table and no second login, and the case service can move to its own server by changing a connection string (Architecture v5 slide 45). Second, the evidence is machine-readable: the count is a read over rows that exist for every business date, not a minute of a cutover meeting, so the sign-off rests on data rather than on assurance. Third, the schema is honest about what it does not hold: the version of this story records the extract, its field list and the read-only window in the history, and creates no case or ownership object, so nobody later mistakes `rwb_source_data` for a second home of the case aggregate (DP-15).

**What carries over unchanged.** The case number, the owner, the queue, the stage, the `account_key` on each account link, the `person_key` on each party link, and the source and the migration date of every migrated record. Nothing about an ACE account or an ACE customer is carried: no name, no identity number, no balance and no contact point enters the extract, because those fields stay where ACE holds them and are read through the views (legacy guardrail; DP-05; D-RCV-35 U1). The ten-clean-day rule, the read-only retention of the legacy tables and the sign-off by the data steward are the legacy criteria and are copied into section 7 with their origin tag.

### 3. Preconditions

- The Ownership Map entry for the four tables is accepted: `recovery_case`, `case_account`, `case_party` and `assignment` are P3's, and rwb-case owns their cutover migration and its Flyway sequence (Ownership Map v1; DP-01; GAP-0521; ASM-0716).
- The cutover run of rwb-case is ready to receive the extract: its own migration on its own sequence, its own login and its own schema `rwb_case`. This story neither writes it nor waits for it to be deployed, because the handover is a file and the contract mock answers until the load is live (DP-15; RWB-ITG-DM003-ITG §12.8).
- The per-service Flyway contract `RWB-PLT-E1044-CON` is in place, with the sequence of `rwb_source_data` and its baseline, so this story takes the next free version and writes one history row (DP-15; TSD P1 v3 T3.2).
- The data product catalogue of `RWB-P1-E1001-APP` is live: DP01 Account and arrears and DP02 Customer and party each name one system of record, so an `account_key` and a `person_key` have one named owner before a key is resolved (FSD P1 v3 A2.2; TSD P1 v3 T3.6).
- The 30 read-only `recovery.v_ace_*` views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`. This story reads `v_ace_account` (DF-ACE-001 to DF-ACE-042) and `v_ace_customer` (DF-ACE-055 to DF-ACE-074) and nothing else of ACE (FSD P1 v3 A2.1.2; TSD P1 v3 T3.3 and T3.4; T6.3).
- JOB-04, the reconciliation of the case list to `v_ace_account` with REC-01, REC-02 and REC-05, runs for every business date and writes `reconciliation_result`. The workflow is the build of `RWB-P1-E1011-APP` in this service; this story consumes its rows and changes none of them (FSD P1 v3 A2.11; TSD P1 v3 T3.6 and T3.7; Architecture v5 slide 44).
- The gateway-bff composite route of `RWB-PLT-N001-CON` is in place, so the cutover result can be read on SCR-44 Interface and job monitor without a screen of this story's own (DP-19).
- The synthetic fixture of the cutover extract, the view fixture and the rwb-case contract mock exist before the first build, so the story starts after its two in-lane predecessors and needs no production data (section 12.8).
- The source of the legacy extract, its format and the place that holds the sign-off are given by no source document: the extract is read once from the legacy Workbench cutover dump, lands nothing, and the sign-off is held in the cutover record of the release pipeline (GAP-0522; ASM-0717).

### 4. Flow

1. The release pipeline starts the cutover run for the cutover business date, under the `rwb_source_data` service identity and one Idempotency-Key per run. The run is a pipeline step, not an API call: this service publishes no operation for it (section 12.1).
2. CutoverExtractReader reads the legacy Workbench cutover dump once, for the open cases at cutover, and selects `recovery_case`, `case_account`, `case_party` and `assignment` rows with the fields of the legacy Data table. The dump is read as a file; nothing is requested from the running legacy application.
3. BusinessKeyMapper maps each record to its ACE business key without adding one of its own: the case keeps its `case_no`, its `owner_user_id`, its `queue_code` and its `stage_code`; each `case_account` row carries the `account_key` it held; each `case_party` row carries the `person_key` it held; each `assignment` row keeps its task, its assignee and its assignment and end dates (legacy AC1).
4. The mapper takes no ACE field. An account name, an identity number, a balance, a contact point or a customer address in the dump is dropped and never carried, so the extract holds no copy of an ACE row (legacy AC1 and guardrails; DP-05).
5. CutoverKeyResolver checks every extracted key against the views on the same login: `v_ace_account` for an `account_key` and `v_ace_customer` for a `person_key`. A key with no view row does not stop the extract: the record is handed over with the key as it stands and the orphan is listed for the data steward and the ACE team, because a suppressed break is a silent loss (FSD P1 v3 A2.11.3.1 BR-P1-011-3).
6. CutoverExtractHandover writes the extract to the handover location agreed with rwb-case and records its checksum, its row counts per entity and its business date in the cutover record. Nothing is inserted into `rwb_source_data`; the extract is a file with a checksum, not a staging table (ASM-0717).
7. rwb-case reads the handed-over extract and loads it into `rwb_case` through its own cutover migration on its own Flyway sequence, which sets the `source` and `migrated_at` of every migrated record. This story does not run that migration and holds no grant on `rwb_case` (DP-01; DP-15).
8. From the business date after the load, JOB-04 reconciles the case list to `v_ace_account` and writes its results. CutoverEvidenceCounter reads the `reconciliation_result` rows of each business date and counts a clean day when every result is PASS with no unexplained variance and no REC-05 orphan on a migrated record (ASM-0718).
9. A break of either kind resets the count to zero and the date is listed with its result rows, so the next clean day starts a new run of ten. The counter holds no table: the count is derived each time from the rows already written.
10. When the count reaches ten consecutive business dates, the cutover record moves to ready for sign-off. The data steward signs off in the cutover record of the release pipeline; the sign-off is a release artefact, not a Workbench row (ASM-0717; legacy AC3).
11. After the sign-off the legacy Workbench tables stay read-only for their retention period and the migrated records are served from `rwb_case` through the rwb-case contract (legacy AC3).
12. The version of this story is applied on the sequence of `rwb_source_data`. It creates no table, no column and no index for a case, an account link, a party link or an assignment, and its description records the extract's definition, its field list and the read-only window.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The legacy cutover dump is absent, unreadable or not the dump of the cutover business date | The run stops before any extract is produced; no record is handed over, the pipeline step is FAILED and the cutover record names the dump and the date | None | AC1, component test |
| X2 | A case row lacks its `case_no`, its owner, its queue or its stage | The row is refused and listed for the data steward; no partial case is handed over and no value is invented | MSG-GEN-001 | AC1 |
| X3 | A `case_account` row carries no `account_key`, or a `case_party` row carries no `person_key` | The row is refused and listed; the case is handed over without that link and the missing key is named | MSG-GEN-001 | AC1, TC-DM-003-01 |
| X4 | A key resolves to no `v_ace_account` or `v_ace_customer` row | The record is handed over with its key unchanged and the orphan is listed for the data steward and the ACE team; nothing is deleted and nothing is rewritten | None | AC1, AC3 (a break day is not counted) |
| X5 | The dump carries an ACE account or an ACE customer column | The column is dropped; the extract holds no ACE field and `rwb_source_data` stores no copy of it | None | AC1, TC-DM-003-01 |
| X6 | rwb-case rejects the handed-over extract | No row is loaded by that run; the mismatch is listed with the entity and the count, and the cutover record shows the handover FAILED | None | AC3, TC-DM-003-03 |
| X7 | A business date of the ten clean days has a BREAK result or a new REC-05 orphan | The count resets to zero and the date and its result rows are listed; the cutover record shows the break | None | AC3, TC-DM-003-03 |
| X8 | The ACE batch of a business date is not COMPLETE, so the reconciliation cannot run | The date counts as no clean day and the product is named with its last completed business date; a stale product is never treated as a clean day | MSG-P1-001 | AC3 |
| X9 | A caller without the Platform administration right asks for the cutover result or starts the run | The call is refused before any file is read or any record handed over | MSG-P4-002 | TC-DM-003-04 |
| X10 | The version of this story is applied a second time | Flyway reports it as already applied; no row is written twice and no version is edited in place | None | AC1 |

The message texts are the legacy ones, unchanged (section 14). X1, X2, X3, X5 and X10 are exercised inside the story's own tests and carry no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One reader over the legacy dump, one key mapper, one key resolver over two views, one handover writer, one evidence counter and one Flyway version; the load and the reconciliation are other stories' |
| Negotiable | The handover format, the cutover record's layout and the retention period of the legacy tables are agreed at the wave 4 entry check; this story fixes the four entities, the keys and the no-copy rule only |
| Valuable | Every open case keeps its owner, its queue, its stage and its links from the first day, and the cutover is signed off on ten counted clean days rather than on assurance |
| Estimable | One reader, one mapper, one resolver, one handover, one counter, one no-op migration and three test cases |
| Small | Fits one sprint; the load, the reconciliation and the screen belong to other stories |
| Testable | Every criterion in section 7 runs against synthetic fixtures with no legacy data and no ACE data |

### 7. Acceptance criteria

```gherkin
Feature: Migrate case and ownership

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-003 AC1)
    Given the legacy Workbench case, case account, case party and assignment records for the open cases at cutover
    Given the rwb-case contract mock returns the migrated case with its owner, its queue and its stage
    When the migration reads them
    Then each case keeps its case number, its owner, its queue and its stage, each account link carries an account_key and each party link a person_key
    And no account and no customer record is copied from ACE

  Scenario: AC3 Cut over (legacy RWB-DM-003 AC3)
    Given ten clean days on the migrated records
    Given the rwb-case contract mock returns the migrated records served from schema "rwb_case"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
```

AC1 and AC3 are copied character for character from legacy RWB-DM-003. The two added Givens are the rwb-case contract answers — the load is P3's, so the case and its served schema are answered by that contract and its mock — and they change no legacy value. AC2 Reconcile the business keys (REC-05) is owned by `RWB-ITG-DM003-ITG` and is not copied here; this story only reads the reconciliation results the ITG story asserts.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `recovery_case`, `case_account`, `case_party` and `assignment` are P3's: P1 extracts and hands over, and writes no row of `rwb_case` and no other service's schema | Ownership Map v1; Architecture v5 slides 41 and 45; DP-01; ASM-0716 |
| BR2 | The extract carries the case number, the owner, the queue, the stage, an `account_key` on each account link and a `person_key` on each party link, and keeps every field the legacy Data table names | Legacy RWB-DM-003 AC1 |
| BR3 | No account and no customer record is copied from ACE: no ACE account or customer field enters the extract and no copy is landed in `rwb_source_data` | Legacy RWB-DM-003 AC1 and guardrails; D-RCV-35 (U1); DP-05 |
| BR4 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, with SELECT and nothing else | BR-P1-001-2; Architecture v5 slides 29 and 41; ADR-010; DP-05 |
| BR5 | A business-key link is a business key with no foreign key into ACE; `account_key` and `person_key` are that link and are checked by REC-05 | BR-P1-001-3; TSD P1 v3 T3.9 |
| BR6 | A migrated record keeps its source and its migration date, and never a copy of an ACE row; the load sets both, and this story reads them through the rwb-case contract | Legacy RWB-DM-003 guardrails; D-RCV-35 (U1) |
| BR7 | A REC-05 orphan never deletes or changes a Workbench record: it is listed for the data steward and, where the row is missing in ACE, for the ACE team | FSD P1 v3 A2.11.3.1 BR-P1-011-3 |
| BR8 | The cutover evidence is ten consecutive business dates of PASS reconciliation results, with no unexplained variance and no new REC-05 orphan on a migrated record; a break resets the count and no counter table is created | Legacy RWB-DM-003 AC3; FSD P1 v3 A2.11; ASM-0718 |
| BR9 | The sign-off is held in the cutover record of the release pipeline, and no Workbench table holds it | ASM-0717 |
| BR10 | The service runs its own Flyway sequence in its own schema; the version of this story creates no case or ownership object and records the extract, its field list and the read-only window in its description | DP-15; ADR-021; TSD P1 v3 T3.2 |

Where each rule lives in the target: BR1, BR5 and BR10 are the boundary, and the story proves them in the schema, in the history and in the refusal to write `rwb_case`. BR2, BR3 and BR6 are the extract's content, proved by the field list and by the absence of any ACE field. BR4 is the grant, proved by the boundary test of the service. BR7 is the handling of an orphan, which is listed and never repaired in place. BR8 and BR9 are the cutover gate: the count is derived from the results, and the sign-off is a release artefact.

### 9. State transitions

None for the case. This story changes no case status, no stage and no task: the case state machine lives in rwb-case and is moved by rwb-case after the load. The moves below are the states of the cutover itself, as the cutover record and SCR-44 show them.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The cutover run reads the legacy dump | The dump is the dump of the cutover business date | Extract ready: every open case holds its case number, owner, queue and stage, every link its key, and nothing is written to `rwb_source_data` |
| Extract ready | rwb-case loads the handed-over extract through its own migration | The extract is accepted with its checksum | Loaded: the records are served from `rwb_case` with their `source` and `migrated_at`, and the clean-day count is zero |
| Loaded | JOB-04 writes a PASS result set for a business date | No unexplained variance and no new REC-05 orphan | Ten clean days running: the count moves to the next business date |
| Ten clean days running | JOB-04 writes a BREAK result or raises a REC-05 orphan | The business date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days running | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy tables stay read-only for their retention period and the migrated records are served from `rwb_case` |

The record of each move is the cutover record of the release pipeline and the `reconciliation_result` rows for the business date. This story publishes no event that announces a move, because a cutover is not a business event of the case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the clean-day count, and signs off in the cutover record (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the resolver, the handover and the counter; runs the tests; applies the version on the per-service sequence |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result and the reconciliation results; each holds Platform administration R |
| The ACE team lead | Receives every listed orphan whose row is missing in ACE, and answers for the view row |
| The rwb-case service identity (the `rwb_case` login) | Loads the handed-over rows through its own cutover migration; this story never uses that login |
| The rwb-source-data service identity (the `rwb_source_data` login) | Reads the dump and the two views and writes one Flyway history row; it holds no write on `rwb_case` and no write on any `public` table |
| No delegation of authority level applies | The cutover takes no credit decision and changes no case fact |

The role codes are rows of rwb-access, and the read of the cutover result authorises through the guard of the published operation; this story adds no role and no grant of its own. The legacy permission row for the key is Platform administration R for the six roles above, and it is kept unchanged.

### 11. Data

| BR Field ID | Entity | Field | Read, extract or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code`, `owner_user_id`, `queue_code`, `source`, `migrated_at` and the rest of the 55 fields | Extracted from the legacy dump and handed over; P3's table, never written here |
| DF-CAS-024 to DF-CAS-029 | `case_account` | `id`, `case_id`, `account_key`, `is_primary`, `linked_from`, `linked_to` | Extracted and handed over; P3's table, never written here |
| DF-CAS-030 to DF-CAS-035 | `case_party` | `id`, `case_id`, `person_key`, `party_role`, `role_from`, `role_to` | Extracted and handed over; P3's table, never written here |
| DF-WRK-009 to DF-WRK-040 | `assignment` | `id`, `case_id`, `task_id`, `assignee_user_id`, `assigned_at`, `ended_at` and the rest of the 32 fields | Extracted and handed over; P3's table, never written here |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | `rec_code`, `business_date`, `product_group`, `result`, `variance_count`, `variance_pct` and the rest of the 12 fields | Read as the cutover evidence, written by JOB-04; never written here |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` | `account_key` and the 41 other fields of the account view | Read only, to resolve an `account_key`; never extracted into the handover |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` | `person_key` and the 19 other fields of the customer view | Read only, to resolve a `person_key`; never extracted into the handover |
| None: framework table | `flyway_schema_history` | The version, the description and the checksum of this story's version | Write, one row, at deploy only |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD P1 v3 T3.6 and of TSD P1 v3 T3.4. `rwb_source_data` holds **no** case, account-link, party-link or assignment table, and this story's version creates none: the four tables are P3's, the extract is a file with a checksum, and the only row the story writes is the history row of its own version. The two views are read for their keys and are never copied, so no account name, identity number, balance, contact point or address enters the extract (BR3, BR4).

The migrated record keeps its `source` and its `migrated_at`, and both are set by the load in rwb-case, not here; this story reads them back through the rwb-case contract when it reports the load (BR6). `case_list_row` is a P1 table but not this story's: the daily case list projection and its publish status belong to `RWB-P1-E1002-APP` and `RWB-P1-E1011-APP`.

### 12. Contract

**12.1 REST operations provided**

None. The cutover is a release-pipeline command and not an operation of the service: it reads a dump and hands over a file, so no caller could sensibly address it, and no path of `/api/recovery/source-data/v1` is added here. The result of the cutover is read through operations that other RWB-SVC-P1 stories already publish and that this story neither claims nor changes:

| Operation | Base | Owner story | What it shows of this story |
|---|---|---|---|
| `GET /admin/reconciliation/results` (API-P1-003) | `/api/recovery/source-data/v1` | RWB-P1-E1011-APP | The PASS and BREAK rows the clean-day count is read from |
| `GET /admin/jobs` (API-P1-001) | `/api/recovery/source-data/v1` | RWB-P1-AD018-APP (legacy RWB-AD-018) | The run of the cutover step, with its status and its business date |

API-P1-003 keeps its ID from the legacy inventory and lists the daily reconciliation results and the REC-05 orphans (TSD P1 v3 Appendix T-A.2), which is exactly the evidence of AC3; the extract itself has no endpoint, because the legacy story states "No endpoint in this story" and no source gives one.

**12.2 REST operations consumed**

None at run time. The run reads its own dump file, resolves its own keys against its own views on its own login, and writes its own history row; it calls no service and holds no C dependency. The rwb-case contract is used as a fixture in the tests and as the read-back of what was loaded, and it adds no run-time C dependency to the story (section 12.8).

**12.3 Events published**

None. The cutover publishes no Kafka event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`. AceDataReady and AceDataLate belong to `RWB-P1-E1013-APP`.

**12.4 Events consumed**

None. No event starts the cutover: it is started by the release pipeline for the cutover business date, and the reconciliation that produces the evidence is started by AceDataReady in `RWB-P1-E1011-APP`.

**12.5 Workflows and activities**

None added. JOB-04, the reconciliation whose results are counted, is the event-triggered workflow of `RWB-P1-E1011-APP` on task queue `rwb-source-data` (Architecture v5 slide 44); this story neither creates nor changes a workflow, an activity or a child workflow, and it starts no workflow of its own.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job sits in this story: the cutover is a one-off pipeline run, and the daily counting is a read over rows that another story's trigger already writes.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the cutover evidence, written by JOB-04 (`RWB-P1-E1011-APP`) |
| `recovery_case`, `case_account`, `case_party`, `assignment` | `rwb_case` | P3 | **Not owned and not written here**: extracted to a file, loaded by rwb-case's own migration |

There is no case, account-link, party-link or assignment table in `rwb_source_data`, and this story adds none. No statement of the story names a table in `public`, no statement names another service's schema, and the only cross-schema read is the granted `recovery.v_ace_*` view (DP-01, DP-05; Architecture v5 slide 45).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | The `recovery_case`, `case_account`, `case_party` and `assignment` rows of the open cases at cutover, synthetic: case "RW-2026-000601" with owner "RW-OFF", queue "MTG-BKK-CO" and stage "WITH_FCR_OFFICER", account links "ACC-SYN-000601" and "ACC-SYN-000777", party link "PERS-SYN-000601" | AC1 and AC3, and the exception paths X2 to X5, from Day 1 |
| View fixture (`v_ace_account`, `v_ace_customer`) | The two views as synthetic rows in a container, with one row for "ACC-SYN-000601" and one for "PERS-SYN-000601" and none for "ACC-SYN-000777" | AC1 key resolution and the orphan path, X4 |
| rwb-case contract mock (`GET /cases/{caseId}`, `/accounts`, `/parties`) | The migrated case with its owner, its queue, its stage and its links, served from schema `rwb_case` | AC1 and AC3, and the load report |
| Reconciliation extract fixture (`reconciliation_result` rows) | PASS result sets for ten consecutive business dates, and one BREAK set for the counter-reset case | AC3, X7 and X8 |

Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change shows up as a failed test rather than as a silent pass. The source of the real legacy dump, its format and the place that holds the sign-off are Not specified in the source documents (GAP-0522; ASM-0717).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | The cutover is a pipeline command; the result is read through API-P1-003 and API-P1-001, which other stories own |
| Kafka | None | None | No event published or consumed by this story |
| Temporal | None | None | No workflow, activity or schedule; JOB-04 is `RWB-P1-E1011-APP`'s |
| File | None | One | The legacy cutover dump, read once per cutover run, and the handed-over extract with its checksum |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data` (the last two are named for completeness and used by no part of this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CutoverExtractReader | Repository | Reads the legacy cutover dump once and selects the four entities with the fields of the legacy Data table; no write, no `public` table, no other schema |
| BusinessKeyMapper | Service | Maps each record to its ACE business key — it keeps the case number, the owner, the queue, the stage, `account_key`, `person_key`, `source` and `migrated_at` — and drops every ACE field the dump may carry |
| CutoverKeyResolver | Service | Resolves each `account_key` against `v_ace_account` and each `person_key` against `v_ace_customer` on the service login, and names every key that resolves to no row |
| CutoverExtractHandover | Service | Writes the extract to the handover location with its checksum and its per-entity counts, and records both in the cutover record; inserts nothing into `rwb_source_data` |
| CutoverEvidenceCounter | Service | Reads `reconciliation_result` for each business date and counts ten consecutive PASS dates with no unexplained variance and no new REC-05 orphan; a break resets the count and no table holds it |
| `V000x__dm003_cutover_extract.sql` | Migration | The next free version of the per-service sequence: creates no table, no column, no index and no grant, and records the extract's definition, its field list and the read-only window of the legacy tables |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the 30 views, so the key resolution is its own SQL on its own login and adds no contract hop. DP-15 gives this story its version and its history row, and gives rwb-case the sequence that loads the rows, so the load needs no cross-schema write (GAP-0521; ASM-0716). DP-19 applies to the read of the result on SCR-44 and adds no screen. No other pattern of the table applies: there is no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of this story's own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no schedule (DP-10).

**Database and migrations**

- Reads the dump and the two views and writes no row at run time. The only write of the story is the Flyway history row of its own version.
- The version creates no table, no column, no index and no constraint: `rwb_source_data` holds no case, account-link, party-link or assignment table before or after it, and it grants nothing on `rwb_case` (BR1, BR10).
- Its description records the extract's definition, the field list of the four entities and the read-only window of the legacy tables, so a later reader of the schema and of the history finds both facts. The source, the format and the retention period of the legacy tables are Not specified in the source documents (GAP-0522; ASM-0717).
- The version number is the next free one on the sequence (a `V000x` after the baseline and the Section A and Section B versions of TSD P1 v3 T3.2). No source names the legacy migration file, so the story asserts that no version of the sequence names a case or an ownership extract, load or reconciliation.
- The load's migration and its sequence are rwb-case's, and this story neither describes nor applies them (DP-15).

**Configuration and reference data**

- No parameter and no reference list is read: DP-06 and DP-07 are not in the pattern set. The cutover business date, the handover location and the retention period are configuration of the release pipeline, agreed at the wave 4 entry check, and no value is written in code (the no-value-in-code rule of FSD P1 v3 BR-P1-011); where a source gives none, the story names the assumption rather than a number (ASM-0717).
- The two views, their field IDs and their types are the view contract's, not this story's; the story consumes `account_key` and `person_key` and re-implements no view rule.
- The feature switch is `rwb.source-data.cutover-extract`, from the platform flag library: off, the cutover run does not start, the extract is not produced and the cutover record stays at Not started.
- The login is `rwb_source_data` (Architecture v5 slide 29): SELECT on the 30 views, USAGE on `rwb_source_data`, and no privilege in `public` and none in `rwb_case` (T6.3).

**Build steps**

1. CutoverExtractReader over the dump fixture, with the four entities and the field list; prove one read per run and no write.
2. BusinessKeyMapper: the case number, the owner, the queue, the stage, `account_key`, `person_key`, `source` and `migrated_at`, and the dropping of every ACE field; tests for AC1 and X5.
3. CutoverKeyResolver over the two views with a resolvable and an unresolvable key; the orphan list for the data steward and the ACE team; tests for AC1 and X4.
4. CutoverExtractHandover with the checksum and the per-entity counts, and the assertion that `rwb_source_data` holds zero rows of the four entities before and after; tests for AC1.
5. CutoverEvidenceCounter over the reconciliation fixture: ten consecutive PASS dates, a BREAK on the sixth, a missing ACE batch and a new REC-05 orphan; tests for AC3 and X7, X8.
6. The read-back of the load through the rwb-case contract mock, so the story proves the served schema and the `source` and `migrated_at` of a migrated record; tests for AC3.
7. The refusal path through the guard of the published operations, with no file read after a deny; test for TC-DM-003-04.
8. The migration as a no-op on the schema with the extract, the field list and the read-only window in its description, and the repeated-apply check; test for AC1.

**Feature flag.** `rwb.source-data.cutover-extract`, from the platform flag library. Off: the run does not start, the extract is not produced, and the migration still applies because it creates nothing.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no case or ownership table, the extract is handed over with a checksum and lands nothing, the counter reads ten clean days from the reconciliation results and resets on a break, and no class of the service writes `rwb_case` or names a `public` table.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | The ACE batch for a business date of the ten clean days is not COMPLETE, so the reconciliation for that date cannot run | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | A case row lacks its case number, its owner, its queue or its stage, or a link lacks its key | Enter {field}. |
| MSG-P4-002 | Error | The caller's Platform administration right R or U is absent | You cannot {action} here. Your role does not include it. |

The three messages are copied character for character from the legacy story and the FSD of this module. For MSG-P1-001, {product} is the product code of the source-fed product under test ("DP01" or "DP02") and {date} is its last completed business date. For MSG-GEN-001, {field} is the field name of the refused row ("case_no", "owner_user_id", "queue_code", "stage_code", "account_key" or "person_key"). For MSG-P4-002, {action} is "run the case and ownership cutover" or "read the cutover result" and never a case fact or a field value. No other message is raised by this story.

### 15. Screens and states

No screen in this story, and the legacy story states the same: "No screen in this story." The cutover result is read on SCR-44 Interface and job monitor, the administration screen that shows a run with its status and its reruns, composed through the gateway-bff composite route (DP-19; H `RWB-PLT-N001-CON`; SCR-44 "Module P1, Access: Platform administration"). The clean-day count and the reconciliation result it is read from are shown on that screen and on the reconciliation result list of API-P1-003, which `RWB-P1-E1011-APP` publishes.

| State | What the cutover record and SCR-44 show |
|---|---|
| Extract ready | The dump read once, the per-entity counts, the checksum, and the orphan list of any key that resolved to no view row |
| Loaded | The handover accepted by rwb-case, the load reported through the rwb-case contract, and a clean-day count of zero |
| Ten clean days running | The business dates counted so far, each with the PASS results of its reconciliation and its business date |
| Break | The date of the break, its BREAK result rows or its REC-05 orphan, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy tables read-only for their retention period |

A run that cannot start shows on SCR-44 in its failed state, with the dump and the business date named and no extract produced, so a cutover that did not happen is never read as a cutover that happened.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-003-01 | AC1; BR1, BR2, BR3, BR4, BR6, BR10 | End to end | The legacy cutover extract fixture with one case "RW-2026-000601", owner "RW-OFF", queue "MTG-BKK-CO", stage "WITH_FCR_OFFICER", two account links "ACC-SYN-000601" and "ACC-SYN-000777" and one party link "PERS-SYN-000601"; the view fixture with one row for the account and one for the person; a dump row carrying an ACE account name to prove it is dropped; the count of rows of the four entities in `rwb_source_data` before and after; the story's version applied once and again |
| TC-DM-003-03 | AC3; BR5, BR7, BR8, BR9 | End to end | The reconciliation fixture with PASS result sets for ten consecutive business dates, then one BREAK set and one new REC-05 orphan on a later date; a business date whose ACE batch is absent; the rwb-case contract mock answering the migrated records with `source` and `migrated_at` from schema "rwb_case" |
| TC-DM-003-04 | Access refusal; BR4 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present for the contrast; a row count of `rwb_source_data` before and after the refusal |

TC-DM-003-01 and TC-DM-003-03 are End to end because the run leaves the service's own boundary: it reads a file, resolves keys against views and reports a load that another service performed. TC-DM-003-04 is Component because it exercises the guard at the boundary of the published operation. The legacy test text of TC-DM-003-02 Reconcile the business keys is not repeated here: the ITG copy is `TC-DM-003-02-ITG` on `RWB-ITG-DM003-ITG`, where AC2 is owned. The full new tests, with their Given, When and Then, are recorded in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case IDs.

### 17. Guardrails

- No business value in code: the cutover business date, the handover location and the retention period are configuration of the release pipeline; the story writes no threshold, no percentage, no currency amount and no date.
- No personal data in logs, tests or prompts: the fixtures are synthetic, the `person_key` is a business key and not an identity, and no name, identity number, contact point or address enters the extract at all.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table named in any statement (BR4).
- No copy of an ACE row: no account or customer field enters the extract, and `rwb_source_data` holds no case, account-link, party-link or assignment table before or after this story (BR1, BR3).
- No cross-schema write: the rows are loaded by rwb-case through its own migration, and this story holds no grant on `rwb_case` (DP-01; Architecture v5 slide 45).
- An orphan is listed and never repaired: no migrated record is deleted or changed to make a key resolve (BR7).
- A break is never waived: a BREAK result or a new REC-05 orphan resets the count, and a stale product is never counted as a clean day (BR8; MSG-P1-001).
- The sign-off is an artefact of the release, not a Workbench row: no table is invented for it, and no counter table is invented for the ten days (BR9; ASM-0717; ASM-0718).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).

### 18. Traceability

| Legacy RWB-DM-003 item | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1; the four tables are P3's and are loaded by rwb-case |
| Epic | E1, release 30 November 2026 | Wave 4 tag from EP08; release 30 November 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | RWB-P1-E1001-APP (the tables and the catalog of this service) and RWB-P1-E1069-APP (the views and the grant) |
| Decision | DL25 | BR8, BR9; the ten clean days and the zero-tolerance cutover gate |
| Data | recovery_case DF-CAS-001 to DF-CAS-055; case_account DF-CAS-024 to DF-CAS-029; case_party DF-CAS-030 to DF-CAS-035; assignment DF-WRK-009 to DF-WRK-040 | Section 2 quotation; section 11; AC1; TC-DM-003-01 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Section 12.1; API-P1-003 is the read of the breaks and belongs to RWB-P1-E1011-APP |
| Screen and states | No screen in this story. | Section 15; the result is read on SCR-44 |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR3, BR6; AC1; section 17 |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Section 7; TC-DM-003-01 and TC-DM-003-03 |
| AC2 and TC-DM-003-02 | Reconcile the business keys, REC-05 | Owned by RWB-ITG-DM003-ITG as AC1 and TC-DM-003-02-ITG; not copied here |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_account` and `v_ace_customer` are read by this service on its own login, to resolve the two keys and to copy nothing (section 13) |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence for the extract's record, and the load on rwb-case's own sequence (section 13, AC1, AC3) |
| DP-19 | Template and Rules §R5.5 | The cutover result is read on SCR-44 through the gateway-bff composite route (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H build dependency: the gateway-bff composite route that serves SCR-44 |
| RWB-P1-E1001-APP | App development | H build dependency: the tables of this service and the data product catalog the keys resolve against |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 read-only views, the login and the grant |
| RWB-P1-E1011-APP | App development | Builds JOB-04 and writes `reconciliation_result`, which is the cutover evidence |
| RWB-P1-E1002-APP | App development | Owns `case_list_row` and the case list projection the reconciliation reads |
| RWB-ITG-DM003-ITG | Integration | Owns AC2 and asserts the keys and the break list across the services; its I dependency is this story |
| The rwb-case cutover migration (P3) | App development | Loads the handed-over extract into `rwb_case`; the boundary and the contract for the load are P3's |

External dependencies: None. The story adds no X row of its own.

### 19. Out of scope

- The load of the four tables into `rwb_case`, its migration, its sequence, its rollback and its reconciliation to the extract: P3 rwb-case's own cutover work (GAP-0521; ASM-0716).
- AC2 Reconcile the business keys, REC-05, the break list and its report: `RWB-ITG-DM003-ITG` owns AC2 and `RWB-P1-E1011-APP` builds the reconciliation that produces the results.
- JOB-04, its workflow, its activity, its rerun operation and the `reconciliation_result` rows: `RWB-P1-E1011-APP`.
- `case_list_row`, the daily case list and its publish status: `RWB-P1-E1002-APP` and `RWB-P1-E1011-APP`.
- The 30 read-only views, the `rwb_source_data` login and its grant, and the boundary test: `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`.
- The data product catalogue, the dictionary, the data contracts and the access rows: `RWB-P1-E1001-APP`.
- SCR-44 Interface and job monitor and its route: `RWB-P1-AD018-APP`, its CON story and the gateway-bff composite route.
- The retention period itself, the archival of the legacy tables and the decommissioning of the legacy Workbench: the cutover plan and the data steward, and no source gives the period (GAP-0522; ASM-0717).
- The extract of the treatment and offer records, which shares the pattern of this story: `RWB-P1-DM004-APP`.
- The data lake, INT-19 and INT-20: removed, and no story of this key needs lake data (DP-17).
