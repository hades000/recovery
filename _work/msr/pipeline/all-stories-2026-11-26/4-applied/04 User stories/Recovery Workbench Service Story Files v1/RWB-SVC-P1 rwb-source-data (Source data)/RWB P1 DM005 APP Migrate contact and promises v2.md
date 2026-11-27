# RWB-P1-DM005-APP Migrate contact and promises

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-005 |
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

**Change log.** D-RCV-60, 22 November 2026: P1 slice of RWB-DM-005 for rwb-source-data — the one-off cutover load of the Workbench contact notes and open promises held outside EFS into this service's own `interaction` and `contact_point_ext`, the no-copy boundary of the EFS history, the ten clean days and the sign-off; legacy AC1 and AC2 move to RWB-ITG-DM005-ITG and this story owns legacy AC3. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-DM005-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)** and a **squad member (RW-TRIBE)**, I want **the open promises and contact notes the legacy Workbench holds outside EFS extracted once at cutover and loaded into this service's own `interaction` and `contact_point_ext` tables in `rwb_source_data`, each interaction keeping its case, its person key, its contact key, its promise date and its promise amount, with the EFS history read from `v_ace_efs_action` and never copied, and the ten clean days and the sign-off recorded as the cutover evidence**, so that **no promise a customer made is lost at cutover while the EFS history itself is read from ACE**.

**This is the P1 slice of legacy RWB-DM-005, not a withdrawal of it.** The legacy key keeps its epic E1, its release 30 November 2026 and its decision DL25; the realignment changes who owns the rows. The interaction ledger is rwb-source-data's (DP-18; ASM-0067), `contact_point_ext` is one of the four extension tables P1 owns (Architecture v5 slide 41; TSD P1 v3 T3.5), and DP05 Contact and promises names `interaction` with the three EFS views as its reads (FSD P1 v3 A2.2). `recovery_case` is P3 rwb-case's and is read through its contract, never written (DP-01). The slice is exactly four things: the one-off cutover load of the two tables on this service's login and per-service Flyway sequence (DP-15), the no-copy boundary of the EFS history, the ten clean days counted from the `reconciliation_result` rows of JOB-04, and the sign-off that closes the cutover.

**What this story does not build.** No REST operation of its own, no Kafka event, no workflow, no Schedule and no screen: the cutover is one-off bulk work from the release pipeline, and its result and breaks are read on SCR-44 Interface and job monitor and SCR-45 Data quality through the gateway-bff composite route (DP-19; Architecture v5 slide 32). Section 12 says so table by table.

### 2. Business rationale

A promise date or amount lost at cutover cannot be recovered afterwards: the customer keeps a commitment the bank no longer sees, the arrears strategy runs on a wrong date, and the next call opens with no record of what was agreed. The opposite risk is as costly: a copy of the EFS history into the Workbench makes the two stores drift, holds personal data under a retention rule the Workbench does not own, and answers the same case twice. The legacy story says what it protects:

> **Epic** E1, release 30 November 2026 · **Module** P1 Recovery data engine · **Depends on** RWB-E1-001, RWB-E1-069 · **Decision** DL25
>
> **Story** As a data steward, I want the open promises and contact notes held outside EFS migrated to the case, so that no promise a customer made is lost at cutover while the EFS history itself is read from ACE.

**Why this service loads its own tables.** Three ownership facts agree here: Architecture v5 slide 41 and the default ruling put the interaction ledger with rwb-source-data (DP-18; ASM-0067); the FSD gives DP05 `interaction` with the three EFS views (refresh DAILY, expected by 08:00); and the TSD defines `contact_point_ext` as a P1 extension table keyed by `contact_key`, holding a Workbench decision about an ACE record and never a copy of it (TSD P1 v3 T3.5). The service that owns the rows reads the dump and writes on its own login, with no handover and no C dependency of its own.

**Why the EFS history is read and never copied.** EFS is ingested into ACE (INT-07, owner the ACE team: TSD P1 v3 T5.1) and read through views 9, 10 and 11; the monolith copy `collections_history` is removed as a copy of EFS data (TSD P1 v3 T3.10; D-RCV-35 U1), and DL29 keeps twelve months readable. The Workbench holds the promise the customer made to us; ACE holds the contact history that was always ACE's. The extract therefore refuses a legacy row whose EFS record key resolves to a view row (legacy AC1, owned by RWB-ITG-DM005-ITG).

**Why ten clean days, and why the load is idempotent.** The cutover ends when the moved rows are seen to reconcile day after day: JOB-04 writes one `reconciliation_result` row per check and product group, REC-05 included (FSD P1 v3 A2.11; TSD P1 v3 T3.6). Ten consecutive clean days, with a break resetting the count, is that evidence; the count, the record that holds it and the sign-off shape are not fixed beyond AC3, so they are one assumption rather than an invention (GAP-2166; ASM-3477). And because the ledger is append only with no update path (RWB-P1-E1066-APP), each legacy row carries its own record key and the load is idempotent on it.

### 3. Preconditions

- **The views exist and are granted.** RWB-P1-E1069-APP creates the Section A views on the per-service sequence, views 9 to 11 with fields `DF-ACE-108` to `DF-ACE-139` among them (TSD P1 v3 T3.2, T3.3), and the `rwb_source_data` login holds SELECT on them and nothing in `public` (TSD P1 v3 T6.3).
- **The two target tables exist.** `interaction` arrives with RWB-P1-E1001-APP and its ledger shape, unique keys, sequence allocator and append-only trigger with RWB-P1-E1066-APP; `contact_point_ext` arrives with RWB-P1-E1069-DB (TSD P1 v3 T3.5). This story creates and alters neither.
- **The reconciliation writes its rows.** JOB-04, its REC-01, REC-02 and REC-05 checks and `reconciliation_result` belong to RWB-P1-E1011-APP; until it lands a fixture stands in for the rows the count reads (12.8).
- **The per-service Flyway contract is in place.** RWB-PLT-E1044-CON gives the sequence with its `V0001` baseline and the view versions (DP-15); this story takes the next free version and creates nothing in it.
- **The gateway-bff composite route exists**, because RWB-PLT-N001-CON is the H dependency of DP-19: the result and its breaks are read through a route, not stitched by a screen.
- **The cutover has a place to run.** The release pipeline runs it for one business date against the service's own API and never touches a `rwb_*` schema (Architecture v5 slide 32). **The pipeline step name, the cutover record format and the dump layout:** Not specified in the source documents (GAP-2166; ASM-3474).
- **No dependency blocks the start.** The two platform stories are contract stories and the two P1 stories are in-lane APP work, so the story starts after RWB-P1-E1001-APP and RWB-P1-E1069-APP (§R5.7 rules 2, 3 and 8); the wave 4 tag is the W-MAP tag of EP08 and does not delay the build.

### 4. Flow

1. The cutover window opens; the release pipeline starts the step for one business date and one environment as one-off bulk work through this service's own admin operation. No scheduler runs it.
2. CutoverContactPromiseExtract reads the legacy cutover dump once, only for the promises and notes held outside EFS: the case rows of their cases (`DF-CAS-001` to `DF-CAS-055`), their `interaction` rows (`DF-INT-001` to `DF-INT-029`) and the `contact_point_ext` rows of their contact keys (`DF-EXT-013` to `DF-EXT-026`).
3. EfsDuplicateGuard reads `v_ace_efs_action` (view 9) once for the account keys of the extract and refuses every legacy row whose EFS record key resolves to a view row; action codes are carried as held and checked against `v_ace_efs_action_code` (view 10), with none minted and none translated.
4. InteractionCutoverMapper maps each remaining interaction to its case and keeps the five facts whole — case, `person_key`, `contact_key`, `promise_date`, `promise_amount` — copying and deriving nothing and inventing no `party_id` or `contact_point_id` (ASM-3475).
5. CaseContractCheck calls the P3 case read for each case and refuses the batch when a case does not answer, so no migrated row points at a case the case service does not serve; the answer is a mock in the tests and adds no C dependency (12.2).
6. ContactPromiseCutoverLoader inserts both tables in one transaction per cutover business date: one `interaction` row per note or promise through the ledger's sequence allocator, with `source_system` and `source_ref` carrying what the legacy row holds; one `contact_point_ext` row per contact key, with consent carried as `consent_given` plus `consent_at` — WITHDRAWN as false with its date, UNKNOWN as no row at all (TSD P1 v3 T3.5).
7. CutoverEvidenceReader reads the `reconciliation_result` rows JOB-04 writes after the load (`DF-OPS-118` to `DF-OPS-129`) and counts the clean days: a PASS row with no unexplained variance and no new REC-05 orphan adds a day; a BREAK row or new orphan resets the count to zero and names the day.
8. On the tenth consecutive clean day the data steward signs off, held in the cutover record beside the ten day rows; the legacy tables are then set read-only for their retention period and the records are served from the new schema through this service's interaction read.
9. At deploy the version applies on the per-service sequence, writes one `flyway_schema_history` row and creates no table, column or index; its description carries the extract definition, the field list, the legacy record key and the read-only window (DP-15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The dump is absent, unreadable or read twice for the same business date | The step stops before any mapping; no row is written and the record names the date and the reason | MSG-GEN-001 | AC3 |
| X2 | An interaction carries no case, or its case does not answer | The row is refused whole, the step stops and the record names the row and the case; no partial load | MSG-GEN-001 | AC3 |
| X3 | A required key is empty: case, `person_key`, `contact_key`, `promise_date`, `promise_amount`, `contact_type` or `source_system` | The row is refused whole with the field named; no default and no derived value | MSG-GEN-001 | AC3 |
| X4 | `v_ace_efs_action` holds the EFS record key a legacy row carries | The legacy row is not migrated — that history is read from the view — and is counted as skipped | None | AC3 |
| X5 | A view read fails: relation absent or statement error | The step stops with no partial load and no stale history carried as current | None | AC3 |
| X6 | The transaction of a business date fails during the load | Nothing of that date is committed; the rerun is idempotent on the legacy record key | None | AC3 |
| X7 | JOB-04 writes a BREAK row or a new orphan for a migrated record during the ten days | The count resets to zero, the day is named and the break is listed; the sign-off cannot be recorded | None | AC3 |

The message texts are the legacy ones (section 14). MSG-P1-001 is raised by the freshness read of this service when the EFS batch is late; this story asserts it and does not produce it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One extract reader, one duplicate guard, one mapper, one case check, one loader, one evidence reader and one migration; the case is mocked |
| Negotiable | The dump layout and the cutover record are agreed at the rehearsal; this story fixes only the five facts, the no-copy rule and the idempotency key |
| Valuable | Every promise and consent held outside EFS survives cutover in the schema that now owns it, evidenced by ten clean days |
| Estimable | One batch step, five components, one migration, five fixtures and two test cases |
| Small | Fits one sprint, as the P1 slice of a split legacy key |
| Testable | AC3 runs end to end on a synthetic extract and synthetic reconciliation rows; no production and no ACE data needed |

### 7. Acceptance criteria

```gherkin
Feature: Migrate contact and promises

  Scenario: AC3 Cut over (legacy RWB-DM-005 AC3)
    Given ten clean days on the migrated records
    Given the rwb-case contract mock returns the case of each migrated interaction
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
```

AC3 is copied character for character from legacy RWB-DM-005. The added Given is the rwb-case contract answer — the case of each interaction is read through the contract and never from a table — and it changes no legacy value in the When or Then lines. AC1 Extract the Workbench records and AC2 Reconcile the business keys are owned by RWB-ITG-DM005-ITG and are claimed by neither this file nor this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The interaction ledger is P1's in `rwb_source_data` and is written only by this service; `recovery_case` is P3's, read through its contract and never written | ASM-0067; DP-01, DP-18; Architecture v5 slide 41 |
| BR2 | `contact_point_ext` is P1's extension table keyed by `contact_key`, holding a Workbench decision about an ACE record; this story writes its rows and copies no ACE column into it | TSD P1 v3 T3.5; FSD P1 v3 A2.2; DP-01 |
| BR3 | The EFS history is read from `v_ace_efs_action`, `v_ace_efs_action_code` and `v_ace_efs_assignment` and never copied; a legacy row whose EFS record key resolves to a view row is not migrated | Legacy RWB-DM-005 AC1; DL29; TSD P1 v3 T3.3, T3.10; REQ-RDF-003 |
| BR4 | A migrated interaction keeps its case, `person_key`, `contact_key`, promise date and promise amount; no value is derived or defaulted | Legacy RWB-DM-005 AC1 (owned by RWB-ITG-DM005-ITG); TSD P3 v3 T3.1 |
| BR5 | The load is idempotent on the legacy record key: a second run of the same business date inserts no row and reports it as already loaded | AC3; RWB-P1-E1066-APP (append-only ledger) |
| BR6 | Ten clean days are counted from the `reconciliation_result` rows of JOB-04 on the migrated records; a PASS row with no unexplained variance and no new orphan adds a day and a break resets the count | Legacy RWB-DM-005 AC3; FSD P1 v3 A2.11; DL25; ASM-3477 |
| BR7 | The sign-off is held in the cutover record, the legacy tables stay read-only for their retention period, and the records are served from the new schema | Legacy RWB-DM-005 AC3; REQ-RDF-013; ASM-3474 |
| BR8 | The service runs its own Flyway sequence in its own schema; this story's version creates no table, no column and no index | DP-15; ADR-021; TSD P1 v3 T3.2 |
| BR9 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, SELECT only, with no `public` table in any statement | BR-P1-001-2, BR-P1-001-4; ADR-010; DP-05; TSD P1 v3 T6.3 |
| BR10 | A business key with no view row is an orphan: listed for the data steward and, where the row is missing in ACE, for the ACE team, and it never deletes or changes the record | BR-P1-011-3; FSD P1 v3 A2.11.3.1; REQ-RDF-008 |
| BR11 | No value a business person may change is written in code, and no personal data appears in the extract, a log, a fixture or a prompt | Legacy RWB-DM-005 guardrails; FSD P1 v3 BR-P1-011; §R7.2 s17 |

BR1 and BR2 are the schema of `rwb_source_data`, proved by the load's own inserts and by the absence of any write to `rwb_case`; BR3 by the guard and by no ledger row mirroring an EFS action; BR4 on the load row; BR5 by the unique key on the source reference; BR6 and BR7 by the cutover evidence; BR8 by the migration; BR9 by the grant and boundary test of RWB-P1-E1069-DB; BR10 by the reconciliation the count relies on; BR11 by the review rule for the cutover code and its fixtures.

### 9. State transitions

None for the case: this story changes no case status, stage, task or promise state. The moves are the cutover's own, and they are six.

| From | Event | Condition | To |
|---|---|---|---|
| Cutover not started | The step is started for the business date | The dump is readable and every case of the extract is in it | Extract ready |
| Extract ready | The loader commits the business date | Every row carries its five facts and its legacy record key | Loaded: rows in both tables |
| Loaded | The loader is started again for the same business date | The legacy record key is already present | Loaded, unchanged: nothing inserted, the repeat reported |
| Loaded | JOB-04 writes PASS rows for the migrated records | No unexplained variance and no new orphan on the day | Ten clean days running, at the consecutive count |
| Ten clean days running | A BREAK row or a new orphan appears | The break is listed for the data steward | Ten clean days running, at zero |
| Ten clean days running | The tenth clean day is reached and the steward signs off | The sign-off is recorded in the cutover record | Signed off: tables read-only, records served from the new schema |

The cutover record is the ledger of each move and the Flyway history row is the schema's record of the deploy; this story publishes no event for any move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the cutover for a business date, owns the ten day evidence and records the sign-off (FSD P1 v3 A2.11.3.3) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right R of the legacy permission check and may read the record, the evidence and the extract for their scope (TSD P1 v3 T6.1) |
| RW-TRIBE, squad member | Builds the components and applies the version on the per-service sequence |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads views 9 to 11 and the reconciliation rows, writes the migrated rows and its own history row |
| P3 rwb-case and its identity | Owns `recovery_case` and answers the case read; this story takes no right over the table |

The role codes are rows of rwb-access and the step authorises through the guard of the published admin operation; this story adds no role and no grant.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | The case of each interaction and its business keys | Read from the legacy dump and the P3 case contract; P3 owns the table and this story writes no row of it |
| DF-INT-001 to DF-INT-029 | `interaction` | All 29 fields, `case_id`, `occurred_at`, `action_code`, `promise_date`, `promise_amount`, `source_system`, `source_ref` first | Write, one row per note or promise, at the cutover only; no update, no delete |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` | `contact_key`, `contact_type`, `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` and the standard columns | Write, one row per contact key of a migrated interaction, at the cutover only |
| DF-ACE-108 to DF-ACE-127 | `v_ace_efs_action` | 20 fields of view 9, `efs_record_key` and `account_key` first | Read only, for the duplicate guard; never written, never copied |
| DF-ACE-128 to DF-ACE-130 | `v_ace_efs_action_code` | The 3 fields of view 10 | Read only, to check a carried action code against LOV-ACTION-CODE |
| DF-ACE-131 to DF-ACE-139 | `v_ace_efs_assignment` | The 9 fields of view 11, keyed by `account_key` | Read only, for the hand-over history of a promise account |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | The 12 fields of a reconciliation row | Read for the count; written by JOB-04, never here |
| None: framework table | `flyway_schema_history` | Version, description and checksum of this story's version | Write, one row, at deploy only |

Field IDs are those of TSD P1 v3 T3.3, T3.5 and T3.6 and of the Logical Data Model and Data Dictionary v9. The migrated row is a legacy Workbench fact and never a copy of an ACE row: the ACE side of a promise stays in `v_ace_efs_action` (BR3). One point is not settled — the legacy data row names `person_key` and `contact_key` while the ledger defines `party_id` and `contact_point_id` as cross-references and carries no column of either name, so **where the two business keys are held is** Not specified in the source documents (GAP-2166; ASM-3475). The seven standard record columns of TSD P1 v3 T3.0 are carried by both target tables and never by a view.

### 12. Contract

**12.1 REST operations provided**

None. The cutover is one-off bulk work from the release pipeline and is not a public operation: this story adds no path, no query parameter and no response field. The admin and reconciliation operations it is started and read by, and the interaction read its tests use, belong to other RWB-SVC-P1 stories and are named in 12.2, not claimed here (Architecture v5 slide 32).

**12.2 REST operations consumed**

None at run time by this story's own code. The step is started and its result read by the pipeline through this service's own operations, and the case is a mock in the tests:

| Caller | Operation | Owner | Why it is not a dependency of this story |
|---|---|---|---|
| The release pipeline | `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` for the cutover job of a business date | P1 rwb-source-data | Same service: an in-lane operation, held by the story that publishes it |
| The release pipeline | `GET /api/recovery/source-data/v1/admin/data-quality/exceptions` for the reconciliation extract | P1 rwb-source-data | Same service; the cutover record reads its evidence from it |
| The tests | `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Contract mock only; the extract carries the case as the dump holds it |
| The tests | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (RWB-P1-E1068-APP) | Same service: proves the records are served from the new schema |

The story therefore holds no C dependency and no I dependency. DP-11 is not one of its patterns: there is no outbound call to build against, so no timeout of its own is added beyond the platform's one hop and 2 s.

**12.3 Events published**

None. The cutover writes no outbox row and adds no schema to `rwb.source-data.events.v1`; `AceDataReady` and `AceDataLate` belong to this service's freshness stories (TSD P1 v3 T5.3).

**12.4 Events consumed**

None. The step is started for a business date by the release pipeline; it reads no topic and no inbox row, and the `reconciliation_result` rows it counts are read from the table.

**12.5 Workflows and activities**

None added. JOB-04 Reconciliation is an event-triggered workflow of this service, exercised through its rows and unchanged. The cutover is a batch job of the release pipeline, not a Temporal workflow, because it runs once per cutover business date and not on a schedule or an event.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits here; JOB-04 is started by `AceDataReady` and belongs to RWB-P1-E1011-APP.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 (ASM-0067; DP-18) | Write at the cutover: one INSERT per note or promise, idempotent on the legacy record key, through the ledger's sequence allocator; no UPDATE, no DELETE |
| `contact_point_ext` | `rwb_source_data` | P1 | Write at the cutover: one row per contact key of a migrated interaction, with the standard columns |
| `flyway_schema_history` | `rwb_source_data` | P1 | One row for its own version at deploy |
| `recovery_case` | `rwb_case` | P3 | Not written: read through the P3 contract only (DP-01) |
| `reconciliation_result` | `rwb_source_data` | P1 | Not written here: read for the count, written by JOB-04 |

Two tables are written and three are not, and that split is the boundary. That `contact_point_ext` is written here at all is the one point the sources do not settle: the FSD files it under DP02 and gives DP05 only `interaction`, while the legacy data row of this key carries the consent and quality rows, so the load stays with the slice that holds them (GAP-2166; ASM-3476). No statement names a `public` table, another service's schema or a cross-schema foreign key (DP-01, DP-05), and the append-only rule is respected, so a wrong row is corrected by its own record and not by an edit.

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | The notes and promises held outside EFS, as synthetic rows with their cases, person keys, contact keys and promises | AC3, from Day 1, with no legacy data |
| View fixture (`v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment`) | Synthetic EFS rows: one series matching a legacy EFS record key and one matching none, with the action code list | AC3 and the skip path of X4 |
| rwb-case contract mock | The case of each migrated interaction, and one case that does not answer | AC3 and the refusal path of X2 |
| Reconciliation extract fixture | The `reconciliation_result` rows: PASS, BREAK and the REC-05 orphan | AC3 and the reset path of X7 |
| P1 interaction read mock | The migrated records served from `rwb_source_data` | AC3, in the last Then line |

Each fake is generated from the published contract it fronts or from the fixture set agreed at the rehearsal, so a contract change shows up as a test failure. The fixture layouts and the dump file name are Not specified in the source documents (GAP-2166; ASM-3474).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 0 from this story's code | The step is started and read through this service's own admin and reconciliation operations, and the case through the P3 contract in the tests; one hop, 2 s |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule added; JOB-04 is exercised, not changed |
| File | None | One | The extract is read once from the legacy cutover dump, and the cutover record carries the evidence |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`; the topic and the queue are named for completeness and this story uses neither.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CutoverContactPromiseExtract | Batch job | The one-off read of the dump for the promises and notes held outside EFS; one pass per business date |
| EfsDuplicateGuard | Service | One SELECT on `v_ace_efs_action` and the refusal of every row whose EFS record key resolves to a view row; no copy, no write |
| InteractionCutoverMapper | Service | Maps each interaction to its case and keeps the five facts whole, carrying the two business keys |
| CaseContractCheck | Client | One call of the P3 case read per case, 2 s and a breaker, so no row points at a case the service does not serve |
| ContactPromiseCutoverLoader | Repository | The only write path: inserts both tables for one business date in one transaction, idempotent on the legacy record key |
| CutoverEvidenceReader | Service | Counts the clean days, resets on a break, and holds the ten day rows beside the sign-off |
| The next free version of the per-service sequence | Migration | Creates no object; records the extract definition, field list, legacy record key and read-only window in its description |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the views, so the EFS reads are its own SQL on its own login and add no contract hop (Architecture v5 slide 45; ADR-010). DP-15 gives the sequence the version runs on and the history row that records the cutover definition, and is also why the load is this service's and not a handover. DP-19 puts the result and its breaks behind the composite routes of SCR-44 and SCR-45. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of its own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no rule evaluation (DP-04).

**Database and migrations.** The story reads views 9 to 11 and the `reconciliation_result` rows and writes `interaction`, `contact_point_ext` and its own history row; no other table of any schema is named. The version creates no table, column, index or constraint — `interaction` comes from RWB-P1-E1001-APP and RWB-P1-E1066-APP and `contact_point_ext` from RWB-P1-E1069-DB (BR8). No grant is made or changed: the login and its SELECT on the 30 views are RWB-P1-E1069-DB's. The version number is the next free one on the sequence and is not fixed here (TSD P1 v3 T3.2; ADR-021).

**Configuration and reference data.** No parameter and no reference list is read: DP-06 and DP-07 are not patterns of this story, and the ten day target, the business date and the retention period are data of the cutover record, not constants. The feature switch is `rwb.source-data.dm005-cutover-extract` from the platform flag library: off, the step refuses to start and no row is written, while the migration still applies because it creates nothing (ASM-3478).

**Build steps**

1. Extract over the cutover fixture, one pass per business date, with the absent-dump and double-read cases; AC3 and X1.
2. Guard over the three view fixtures, one row whose EFS record key matches and one that matches nothing, proving the match is skipped and no view field is written; AC3 and X4.
3. Mapper and case check: five facts whole, two business keys kept, no derived value or default, and one case that does not answer; AC3, X2 and X3.
4. Loader: one transaction per business date, the sequence allocator, the consent mapping of GIVEN, WITHDRAWN and UNKNOWN, the repeat run that inserts nothing, and the rollback of X6; AC3 and X6.
5. Evidence reader: ten PASS rows count up, a BREAK row or a new orphan resets the count, and the sign-off is refused below ten; AC3 and X7.
6. The version on the next free sequence as a no-op on the schema, plus the repeated-apply check, and the refusal path through the guard of the admin operation; AC3 and TC-DM-005-04.

**Done when.** The tests of section 16 pass, the migrated promises and consents answer from `rwb_source_data` through this service's own read and no EFS row has been copied, AC3 counts ten clean days and records the sign-off, a repeat of the same business date inserts nothing, and no class of the service names a `public` table or another service's schema.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-GEN-001 | Error | The extract lacks a required field or record: a case, a person key, a contact key, a promise date, a promise amount or a contact type | Enter {field}. |
| MSG-P4-002 | Error | A caller without the Platform administration right starts the cutover step | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | Warning | The EFS feed behind DP05 is late for the business date, so the history cannot be carried as current | {product} is from {date}. Today's ACE batch has not arrived. |

The three messages are copied character for character from the legacy master (legacy RWB-DM-005 validation table; FSD P1 v3 VR-P1-011-1; TSD P1 v3 T3.7). This story raises MSG-GEN-001 and MSG-P4-002 itself: {field} is the field or record the extract lacks, and {action} is "run the contact and promise cutover extract", never a case fact or a value. MSG-P1-001 is raised by the freshness read of this service and asserted here as evidence.

### 15. Screens and states

No screen in this story. The cutover is started and its result read on SCR-44 Interface and job monitor, and the breaks that reset the count are shown on SCR-45 Data quality, which RWB-P1-AD019-APP owns. Both are read through the gateway-bff composite route (DP-19; H RWB-PLT-N001-CON); this story adds no route, field or rendering, and the route path and merge order are Not specified in the source documents (GAP-2166; ASM-3474).

| State | What the cutover record holds | What the monitor shows |
|---|---|---|
| Extract ready | Business date, rows read, rows refused as EFS duplicates, cases resolved | The step is running and the extract is ready |
| Loaded | Rows written per table, with their legacy record keys | The rows are in `rwb_source_data` and answer through this service's read |
| Repeated run | Rows already present, rows written as zero, business date | The rerun completed and nothing was duplicated |
| Ten clean days running | Consecutive clean days and the last clean day | The count, its date and the remaining days |
| Break | The BREAK row or orphan, its date, code and owner role, count at zero | The break is listed and the count is reset |
| Signed off | The ten day rows, the extract, the sign-off and the read-only window | The cutover is complete and the legacy tables are read-only |

A cutover that has not reached ten clean days shows as a count and not as a pass, so one break in the window is visible as a reset and the sign-off cannot be recorded below ten (AC3).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-005-03 | AC3; BR1, BR3, BR5, BR6, BR7 | End to end | The cutover fixture with two open promises and two contact notes, one an EFS duplicate; the three view fixtures; the rwb-case mock with two cases and one that does not answer; ten PASS `reconciliation_result` rows, then one BREAK row and one orphan, then ten clean rows again; a repeated run of the same business date; the sign-off recorded once at ten |
| TC-DM-005-04 | Access; BR9 | Component | A caller whose Platform administration right R is absent in the authorise fake, starting the cutover for a business date; a second call with the right present for contrast |

The legacy test case numbers are kept. `TC-DM-005-01`, the extract test, and `TC-DM-005-02`, the reconcile test, sit with AC1 and AC2 on RWB-ITG-DM005-ITG as `TC-DM-005-01-ITG` and `TC-DM-005-02-ITG` and are not repeated here; `TC-DM-005-03-ITG` and `TC-DM-005-04-ITG` are the integration copies of the two cases above, so this story owns the End to end and the Component ones. The full test, with its Given, When and Then, is recorded in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the five facts are data on the load row, and the ten day target, the business date and the retention period are data of the cutover record, never a constant, an amount or a date in a class.
- No personal data in the extract, the logs, the fixtures or the prompts: it carries case and promise facts and ACE business keys, and no customer name, phone number, e-mail address or identity field; the fixtures are synthetic (BR11).
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table in any statement (BR9).
- No copy of an ACE row: the EFS history is read through views 9 to 11 and never copied, and a legacy row that resolves to an EFS record is not migrated at all (BR3).
- No cross-schema write and no cross-schema join: `recovery_case` is read through the P3 contract and no statement names `rwb_case` (BR1; DP-01).
- The ledger is append only and one version on the per-service sequence is never edited in place: the load inserts, never updates and never deletes, and a later change is a new version (BR5, BR8).
- A cutover is never declared on a count that has been reset: a break sets the count to zero and the sign-off stays closed (BR6, BR7).

### 18. Traceability

| Legacy RWB-DM-005 row | Value (verbatim) | Where it lands |
|---|---|---|
| Epic | E1, release 30 November 2026 | Metadata wave and release; section 2 |
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 |
| Feature | None | No feature grouping is used |
| Process | All recovery processes | The cutover covers the notes and promises of every process the key names |
| Priority | Must | Sections 1, 2 and 19 |
| Depends on | RWB-E1-001, RWB-E1-069 | Rebased by D-RCV-60 onto RWB-P1-E1001-APP and RWB-P1-E1069-APP, plus the two platform contracts |
| Decision | DL25 | BR6; the ten clean days as cutover evidence |
| Story | As a data steward, I want the open promises and contact notes held outside EFS migrated to the case, so that no promise a customer made is lost at cutover while the EFS history itself is read from ACE. | Section 1; section 2 quotation; BR1 to BR5 |
| Data | recovery_case, interaction, contact_point_ext with their field ranges | Section 11; AC3 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Sections 12.1, 12.2 and 15 |
| Screen and states | No screen in this story. | Section 15 |
| Permission checks | Platform administration R: RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10; TC-DM-005-04 |
| Validation and messages | MSG-P1-001, MSG-GEN-001, MSG-P4-002 | Section 14 |
| Test cases | TC-DM-005-01 to TC-DM-005-04 | Section 16; 01 and 02 sit on RWB-ITG-DM005-ITG |
| Guardrails | No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR3, BR9, BR11; section 17 |

Patterns: DP-05 — views 9 to 11 are read by this service on its own login and by no other service (section 13). DP-15 — the version on the per-service sequence, with the history row that records the cutover definition and the load written by the schema's owner (section 13; AC3). DP-19 — the result and its breaks are read through the composite routes behind SCR-44 and SCR-45 (section 15).

Related stories: RWB-PLT-E1044-CON and RWB-PLT-N001-CON are the H contract dependencies (the sequence and the composite route); RWB-P1-E1001-APP and RWB-P1-E1069-APP are the H in-lane dependencies (the `interaction` base table and the Section A views); RWB-P1-E1066-APP and RWB-P1-E1068-APP supply the append-only ledger and the interaction read and are changed by neither; RWB-P1-E1069-DB creates the extension tables and grants and RWB-P1-E1011-APP writes the rows the count reads; RWB-P1-DM002-APP reads `contact_point_ext` and writes none of it; RWB-ITG-DM005-ITG owns AC1 and AC2. External dependencies: None.

### 19. Out of scope

- The extract, the REC-05 reconciliation of the business keys and the ITG test copies: RWB-ITG-DM005-ITG, which owns legacy AC1 and AC2 and proves them against this service's contract.
- JOB-04, its REC-01, REC-02 and REC-05 checks, the `reconciliation_result` rows and the publish hold: RWB-P1-E1011-APP.
- The `interaction` table's shape, its unique keys, its sequence allocator and its append-only trigger: RWB-P1-E1001-APP and RWB-P1-E1066-APP; this story inserts rows and changes none of them.
- The interaction read `GET /cases/{caseId}/interactions` with its filters, paging and masking: RWB-P1-E1068-APP.
- The four extension tables and every grant: RWB-P1-E1069-DB; and the consent read path on the case screen: RWB-P1-DM002-APP.
- The views themselves and the DP05 catalog row with its freshness: RWB-P1-E1069-APP, RWB-P1-E1001-APP and RWB-P1-E1015-APP.
- The SCR-44 and SCR-45 screens and their break list, and the retention rule behind the read-only window: RWB-P1-AD018-APP, RWB-P1-AD019-APP and RWB-P1-E1017-APP.
- The legacy EFS history beyond the twelve months DL29 keeps, and every EFS copy: none exists in the target (TSD P1 v3 T3.10).
- The case record, its status, its stage and its timeline — P3 rwb-case, read through its contract and never written here — and the platform configuration of Kafka, Temporal and the gateway routes, which belongs to the platform epics.
- Any REST operation, Kafka event, Temporal workflow, Schedule or screen: this story builds none, and section 12 says so table by table.
