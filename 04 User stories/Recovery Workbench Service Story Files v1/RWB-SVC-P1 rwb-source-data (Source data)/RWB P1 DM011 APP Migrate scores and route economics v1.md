# RWB-P1-DM011-APP Migrate scores and route economics

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-011 |
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

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-011 for the P1 cutover extract of the legacy case list rows, the route each open case carries and the baseline measure snapshots, the load of the service's own `case_list_row` for the cutover business date, the handover of the route facts to rwb-case and of the baseline to rwb-reporting, and the cutover evidence. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward** I want **the route each open case carries, the case list rows of the cutover business date and the route economics baseline the Workbench calculates migrated**, so that **the baseline and the route history survive cutover while the COLLINS score itself is read from ACE**.

- **Extract here:** one read of the legacy cutover dump for the open cases at cutover — their route facts, the case list rows of the cutover business date, and the baseline snapshots with their dimension, value and baseline flag (legacy AC1).
- **Load here:** those case list rows go into this service's own `case_list_row` for that date, replacing any set already held, so the first reconciliation of the new world has a Workbench side to count (DP-05, DP-15).
- **Handover:** the route code and route state of each case go to P3 rwb-case and the baseline snapshots to P9 rwb-reporting, each as a file with a checksum, each loaded by its owner on its own sequence; this story writes no row of `rwb_case` and none of `rwb_reporting`.
- **No score carried:** no COLLINS score, estimate or model version is copied; the score is read through `v_ace_score` and its absence from every artefact is proved by a column-level check (ASM-3509).
- **Evidence:** ten consecutive PASS reconciliation dates with no unexplained variance and no new REC-05 orphan, read from the `reconciliation_result` rows JOB-04 writes, a break resetting the count (legacy AC3; ASM-3510).
- **No REST operation, event, workflow or screen:** the cutover is a release-pipeline step, and SCR-45 Data quality is a gateway-bff composite route this story does not render (DP-19; ASM-3511).

The legacy key is not withdrawn — route history, a case list of one date and a frozen baseline are Workbench records no ACE table holds. What changes is who holds each: `recovery_case` is P3's, `measure_snapshot` is P9's, `case_list_row` is P1's (GAP-2175; ASM-3508).

### 2. Business rationale

Route economics is the argument the recovery programme makes about itself. Each open case carries the route the rule set put it on, and the Workbench keeps the routing state that says where on that route it stands. Around those facts sits the baseline: measures of the portfolio at a chosen business date, frozen, so a later claim of improvement is measured against a number nobody can move. A route that arrives blank is a case nobody's rule is working; a baseline that is rebuilt rather than frozen measures itself.

**Why the three tables split three ways.** A service writes only its own schema, so a cutover spanning three tables spans three owners: rwb-case holds the case and its state, rwb-reporting the measures and snapshots, rwb-source-data the ACE view contract, extension tables, freshness and reconciliation. The route code and route state are columns of the case, so they are the case service's; a baseline snapshot is one measure for one date, product and dimension value, so it is reporting's; what is left to P1 is the row it already publishes, `case_list_row`, whose own `route_code` and `publish_status` carry the route of the projected case. So this story reads the dump once, loads its own row set, hands the other two facts over, and inserts nothing anywhere else (GAP-2175; ASM-3508).

**Why the score is not carried.** Legacy AC1 is explicit, and the target keeps it in the schema and not only in a sentence: the legacy `score` table leaves the model, `v_ace_score` replaces it keyed by account rather than by case, and the case is reached through `case_account.account_key`. A copied score would be frozen at cutover and quoted for years, the opposite of what a daily COLLINS feed is for. The absence is therefore mechanical — every artefact is checked for a score column and a score value before it is handed over (ASM-3509).

**Why P1 holds the evidence.** `reconciliation_result` is a P1 table and its counts are taken from `case_list_row`, which makes the row set this story writes the first Workbench side the new world has. The ten clean days are counted from rows that already exist, and the baseline is read back from rwb-reporting through its contract (ASM-3510). What carries over unchanged: the case number, account key, product group, status, owner, queue and route code of each case list row; the route code and route state of each case; the measure code, definition version, date, product group and dimension of each snapshot with its value and baseline flag; and the source and migration date of every record. No ACE field is carried, because those stay in ACE behind the views.

### 3. Preconditions

- The Ownership Map reading is accepted: route facts with P3, baseline with P9, `case_list_row` with P1, and the case list API and screen with P3 (GAP-2175; ASM-3508).
- The per-service Flyway contract `RWB-PLT-E1044-CON` is in place, with the sequence of `rwb_source_data` and its baseline, so this story takes the next free version and writes one history row (DP-15).
- `case_list_row` exists on that sequence with the field list of TSD P1 v3 T3.6, re-keyed to `account_key` and constrained on `(business_date, account_key)`, so a rebuild of a date replaces its set rather than adding to it.
- The data product catalogue of `RWB-P1-E1001-APP` is live, so a product group and an account key have one named owner before a row is written.
- The 30 read-only `recovery.v_ace_*` views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`; this story reads `v_ace_score` and nothing else of ACE (DP-05).
- JOB-04, the reconciliation with REC-01, REC-02 and REC-05, runs for every business date and writes `reconciliation_result`; it is `RWB-P1-E1011-APP`'s build and this story only reads its rows.
- The gateway-bff composite route of `RWB-PLT-N001-CON` is in place, so the result is readable on SCR-45 without a screen of this story's own (DP-19).
- The cutover runs of rwb-case and rwb-reporting can receive a file on their own sequences and logins; neither must be deployed, because the handover is a file and the mocks answer until the loads are live (section 12.8).
- The synthetic dump fixture, the `v_ace_score` fixture and the two contract mocks exist before the first build, so no production data is needed.
- The dump's source and format, the handover locations, the retention period and the place of the sign-off are given by no source document (GAP-2175; ASM-3508; ASM-3510).

### 4. Flow

1. The release pipeline starts the cutover run for the cutover business date under the `rwb_source_data` service identity with one Idempotency-Key per run. The run is a pipeline step, not an API call (section 12.1).
2. CutoverExtractReader reads the legacy dump once and selects the route facts of each open case, the case list rows of the cutover date (DF-RPT-001 to DF-RPT-019) and the baseline snapshots (DF-RPT-041 to DF-RPT-052). Nothing is requested from the running legacy application.
3. CaseKeyMapper maps each row onto its Workbench and ACE business keys and adds none of its own: the case keeps its `case_no` and `case_id`, each row its `account_key`, `product_group` and `route_code`, each snapshot its `measure_code`, `definition_version`, `business_date` and dimension (legacy AC1).
4. The mapper takes no ACE field — an account name, a balance, an identity number, a contact point or an address in the dump is dropped and never carried (legacy guardrails; DP-05).
5. ScoreAbsenceCheck runs over every artefact before it leaves the service: no score, estimate or model column exists and no value of those fields is present (legacy AC1; ASM-3509).
6. CaseListRowWriter writes the rows of the cutover date into `case_list_row` of `rwb_source_data`, one row per case account and date, with the `route_code`, `total_balance`, `days_past_due`, `refreshed_at` and `publish_status` the legacy row held; a set already present for the date is replaced whole (DP-15).
7. RouteFactHandover writes the route facts to the location agreed with rwb-case, with a checksum and a case count, and BaselineSnapshotHandover writes the snapshots to the location agreed with rwb-reporting, with a checksum and a count by measure and product group. Each owner loads its own file; this story holds no grant on `rwb_case` or `rwb_reporting` (ASM-3508).
8. From the next business date JOB-04 reconciles the case list to `v_ace_account`, and CutoverEvidenceCounter counts a clean day when every result of a date is PASS with no unexplained variance and no new REC-05 orphan on a migrated row (ASM-3510).
9. A break resets the count to zero and lists the date with its result rows; at ten consecutive clean dates the cutover record moves to ready for sign-off, and the data steward signs off in the release pipeline's cutover record, not in a Workbench row.
10. After the sign-off the legacy tables stay read-only for their retention period and the records are served from the new schema — case list rows from `rwb_source_data`, route facts from `rwb_case`, baseline from `rwb_reporting` (legacy AC3).
11. The version is applied on the sequence of `rwb_source_data`: it creates no route and no measure object, adds no score column, and records the row set, its field list and the replacement rule in its description.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The dump is absent, unreadable or not the dump of the cutover business date | The run stops before any extract; no row written, nothing handed over, the pipeline step FAILED and the cutover record names the dump and the date | None | AC1 |
| X2 | A route fact lacks its `case_no`, `route_code` or `route_state` | The fact is refused and listed for the data steward; no partial route is handed over and no route is invented | MSG-GEN-001 | AC1, TC-DM-011-01 |
| X3 | A case list row lacks its `case_no`, `account_key` or `product_group` | The row is refused and listed, no row set is written for the date, and the missing field is named | MSG-GEN-001 | AC1, TC-DM-011-01 |
| X4 | A snapshot lacks its `measure_code`, `definition_version`, its dimension, its value or its baseline flag | The snapshot is refused and listed, and the measure is handed over without that row | MSG-GEN-001 | AC1, TC-DM-011-01 |
| X5 | The dump carries a COLLINS score, an estimate or a model version | The field is dropped and step 5 proves its absence from every artefact; the run continues and the row keeps no score | None | AC1, TC-DM-011-01 |
| X6 | `v_ace_score` returns no row for an account of a case list row | The row is written with its own fields, no legacy value replaces the missing score, and the account is listed for the data steward and the ACE team | None | AC1, AC3 |
| X7 | rwb-case or rwb-reporting rejects the handed-over file | No row is loaded by that service for that run, the mismatch is listed with entity and count, and the cutover record shows the handover FAILED | None | AC3, TC-DM-011-03 |
| X8 | A business date of the ten has a BREAK result or a new REC-05 orphan | The count resets to zero and the date and its rows are listed; the cutover record shows the break | None | AC3, TC-DM-011-03 |
| X9 | The case list of a business date misses the tolerance of its data product | The date is no clean day, the variance is stated in accounts and in percent, and the publish of that date is held by the story that owns it | MSG-P1-012 | AC3 |
| X10 | The ACE batch of a business date is not COMPLETE, so the reconciliation cannot run | The date is no clean day and the product is named with its last completed business date | MSG-P1-001 | AC3 |
| X11 | A caller without the Platform administration right starts a handover or reads the result | The call is refused before any file is read | MSG-P4-002 | TC-DM-011-04 |
| X12 | The version is applied twice, or the run is repeated for the same business date | Flyway reports the version as already applied; the row set of the date is replaced whole and no row is written twice | None | AC1 |

X1 to X5 and X12 are exercised inside the story's own tests and carry no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One reader of the dump, one key mapper, one score-absence check, one writer of the service's own table, two handovers, one evidence counter and one Flyway version; the two loads, the reconciliation and the screen belong to other stories |
| Negotiable | The handover format and location, the cutover record layout and the retention period are agreed at the wave 4 entry check; the story fixes the three artefacts, their keys and the no-score rule only |
| Valuable | Every open case arrives on the route it had, the baseline is frozen before go-live, and no COLLINS score is quoted from a migrated row |
| Estimable | One reader, one mapper, one check, one writer, two handovers, one counter, one version and three test cases |
| Small | Fits one sprint; the two loads, the measure projection, the reconciliation and the screen are other stories' |
| Testable | Every criterion of section 7 runs against synthetic fixtures with no legacy and no ACE data |

### 7. Acceptance criteria

```gherkin
Feature: Migrate scores and route economics

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-011 AC1)
    Given the legacy Workbench route decisions, case list rows and baseline measure snapshots at cutover
    Given the rwb-case contract mock returns the migrated case with its route code and its route state
    Given the rwb-reporting contract mock returns the baseline measure snapshot with its dimension, its value and its baseline flag
    When the migration reads them
    Then each case keeps its route code and route state, and each measure snapshot keeps its dimension, its value and its baseline flag
    And no COLLINS score is copied, because the score, its estimate and its route are read from v_ace_score

  Scenario: AC3 Cut over (legacy RWB-DM-011 AC3)
    Given ten clean days on the migrated records
    Given the rwb-case contract mock returns the migrated case served from schema "rwb_case"
    Given the rwb-reporting contract mock returns the baseline measure snapshot served from schema "rwb_reporting"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
```

AC1 and AC3 are copied character for character from legacy RWB-DM-011. The added Givens are the two owners' contract answers — the route facts are P3's and the baseline is P9's, so the served case and the served snapshot are answered by those contracts and their mocks — and they change no legacy value. AC2 Reconcile the business keys (REC-05) is owned by `RWB-ITG-DM011-ITG` and is not copied here; this story only reads the reconciliation results that story asserts (ASM-3511).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `recovery_case` and its route facts are P3's and `measure_snapshot` is P9's: P1 extracts, loads its own `case_list_row` and hands over, and writes no row of `rwb_case` and none of `rwb_reporting` | GAP-2175; ASM-3508; DP-05 |
| BR2 | The row set of the cutover business date carries DF-RPT-001 to DF-RPT-019, `account_key` included, and keeps the `route_code` the case held | Legacy AC1; TSD P1 v3 T3.6 |
| BR3 | The route code and route state are handed over unchanged and loaded by rwb-case; no route is recomputed here | Legacy AC1; DP-15 |
| BR4 | Each baseline snapshot keeps its dimension, its value and its baseline flag and is loaded frozen by rwb-reporting; this story neither recomputes nor unfreezes a measure | Legacy AC1; FSD P1 v3 A2.19 |
| BR5 | No COLLINS score is copied: no score, estimate or model column enters any artefact, and the score is read only through `v_ace_score` on the service login | Legacy AC1; TSD P1 v3 T3.3 view 26; ASM-3509 |
| BR6 | ACE data is read only through `recovery.v_ace_*` on the service's own login with SELECT, and no ACE field is copied into a migrated row | BR-P1-001-2; DP-05 |
| BR7 | A migrated row keeps its source and its migration date and never a copy of an ACE row | Legacy guardrails |
| BR8 | A row set for the cutover business date is replaced whole on a rerun, so a date holds one row per case account and never two | TSD P1 v3 T3.6; DP-15 |
| BR9 | The evidence is ten consecutive business dates of PASS results with no unexplained variance and no new REC-05 orphan; a break resets the count, and the sign-off sits in the cutover record of the release pipeline | Legacy AC3; FSD P1 v3 A2.11; ASM-3510 |

BR1 and BR8 are the boundary and the idempotence; BR2 to BR4 are the content of the three artefacts; BR5 and BR6 the view rule; BR9 the cutover gate.

### 9. State transitions

None for the case: this story changes no status, stage, route code or route state, because the routing state machine lives in rwb-case. The moves below are the states of the cutover itself.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The run reads the dump | The dump is of the cutover business date | Extract ready: the three artefacts exist, the score-absence check has passed, and nothing is written outside `rwb_source_data` |
| Extract ready | The row set is written and both files handed over | The row set is written once and both checksums recorded | Loaded: `case_list_row` holds the date, both owners report their load, and the clean-day count is zero |
| Loaded | JOB-04 writes a PASS result set for a date | No unexplained variance and no new REC-05 orphan | Ten clean days running: the count moves to the next date |
| Ten clean days running | JOB-04 writes a BREAK, raises an orphan, or the ACE batch is absent | The date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days running | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy tables stay read-only and the records are served from the new schema |

The record of each move is the cutover record of the release pipeline plus the `reconciliation_result` rows of the date. No event announces a move, because a cutover is not a business event of the case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the clean-day count and the baseline read-back, and signs off in the cutover record (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the check, the writer, the handovers and the counter; runs the tests; applies the version |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result, the reconciliation results and the baseline read-back; each holds Platform administration R |
| The ACE team lead | Answers for the `v_ace_score` row of an account and receives every account listed as having none |
| The rwb-case service identity | Loads the handed-over route facts through its own migration; this story never uses that login |
| The rwb-reporting service identity | Loads the handed-over baseline snapshots through its own migration; this story never uses that login |
| The `rwb_source_data` login | Reads the dump and `v_ace_score`, writes the case list rows of one date and one history row; no write on `rwb_case` or `rwb_reporting` |
| No delegation of authority level applies | The cutover takes no credit decision, sets no route and changes no measure |

The role codes are rows of rwb-access and the read of the result authorises through the guard of the published read; this story adds no role and no grant. The legacy permission row — Platform administration R for the six roles above — is kept unchanged.

### 11. Data

| BR Field ID | Entity | Field | Read, extract or write |
|---|---|---|---|
| DF-RPT-001 to DF-RPT-019 | `case_list_row` | `id`, `business_date`, `case_id`, `case_no`, `account_key`, `account_no`, `product_group`, `stage_code`, `status`, `owner_user_id`, `queue_code`, `team_code`, `route_code`, `total_balance`, `days_past_due`, `refreshed_at`, `last_contact_at`, `last_action_code`, `publish_status` | **Write**, one row set for the cutover business date in `rwb_source_data`, replaced whole on a rerun |
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | The 55 case fields, the route code and the route state among them | Read for the route facts and extracted to the handover; P3's table, never written here |
| DF-RPT-041 to DF-RPT-052 | `measure_snapshot` | `id`, `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code` and 6 more | Extracted and handed over; P9's table, never written here |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` | `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value`, `route_code`, `scored_at`, `source_system`, `data_as_of` | Read only, on the `rwb_source_data` login, to prove the score, its estimate and its route are the view's; never extracted |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | `rec_code`, `business_date`, `product_group`, `source_count`, `workbench_count`, `variance_count`, `variance_pct`, `tolerance_pct`, `result` and the rest of the 12 fields | Read as the cutover evidence, written by JOB-04; never written here |
| None: framework table | `flyway_schema_history` | The version, the description and the checksum of this story's version | Write, one row, at deploy only |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD P1 v3 T3.3 and T3.6, and of the legacy Data table. `rwb_source_data` holds **one** of the three legacy tables, `case_list_row`, and this story writes it for the cutover business date only: the row set is a published projection of one date, not a copy of the account and not a second case table (BR2, BR8). The route **state** has no column there and survives only on the case, which is why the route facts are handed to rwb-case as well (BR3). The baseline flag and the frozen state are carried as the legacy rows held them (BR4). `v_ace_score` is the only path to a COLLINS score (BR5, BR6; ASM-3509).

### 12. Contract

**12.1 REST operations provided**

None. The legacy story states "No endpoint in this story": the cutover is a release-pipeline command that reads a dump and writes a row set, and no path of `/api/recovery/source-data/v1` is added here. The result is read through operations that other RWB-SVC-P1 stories publish and this story neither claims nor changes:

| Operation | Base | Owner story | What it shows of this story |
|---|---|---|---|
| `GET /admin/data-quality/exceptions` | `/api/recovery/source-data/v1` | RWB-P1-E1011-APP | The PASS and BREAK rows the clean-day count is read from |
| `GET /admin/jobs` | `/api/recovery/source-data/v1` | RWB-P1-AD018-APP | The run of the cutover step, with its status and its business date |

**12.2 REST operations consumed**

None at run time. The run reads its own dump, its own view on its own login and writes its own table; it calls no service and holds no C dependency. The rwb-case and rwb-reporting contracts are fixtures in the tests and the read-back of what each owner loaded (section 12.8).

**12.3 Events published**

None. No Kafka event, no outbox row of this story and no new schema on `rwb.source-data.events.v1`; AceDataReady and AceDataLate remain the topic's events and belong to `RWB-P1-E1013-APP` and `RWB-P1-E1011-APP`.

**12.4 Events consumed**

None. No event starts the cutover: the release pipeline starts it for the cutover business date, and the reconciliation behind the evidence is started by AceDataReady in `RWB-P1-E1011-APP`.

**12.5 Workflows and activities**

None added. JOB-04 is the event-triggered workflow of `RWB-P1-E1011-APP` on task queue `rwb-source-data`; this story creates and changes no workflow, activity or child workflow and starts none.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job sits here: the cutover is a one-off pipeline run, and the reporting extract at 01:30 is rwb-reporting's own Schedule.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `case_list_row` | `rwb_source_data` | P1 | **Write**, the row set of the cutover business date only, replaced whole on a rerun; the daily build and the publish status are `RWB-P1-E1002-APP`'s |
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the evidence, written by JOB-04 |
| `recovery_case` | `rwb_case` | P3 | Not owned and not written: the route facts are handed over as a file |
| `measure_snapshot` | `rwb_reporting` | P9 | Not owned and not written: the baseline is handed over as a file |

No statement of the story names a table in `public`, no statement writes another service's schema, and the only cross-schema read is the granted `recovery.v_ace_score` view (BR1, BR6).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | Synthetic route facts, case list rows and snapshots: case "RW-2026-000611" on route "R3" with route state "FIRM_INSTRUCTED", rows for business date "2026-12-31" with account keys "ACC-SYN-000611" and "ACC-SYN-000888", and a "CASES_BY_ROUTE" snapshot over dimension "MORTGAGE" with its baseline flag true | AC1, AC3 and X2 to X5 |
| View fixture (`v_ace_score`) | The view as synthetic rows in a container, with a score row for "ACC-SYN-000611" and none for "ACC-SYN-000888" | AC1's score read and the no-row path, X6 |
| rwb-case contract mock | The migrated case with its route code and route state, served from schema `rwb_case` | AC1, AC3 and the route read-back |
| rwb-reporting contract mock | The baseline snapshot with its dimension, its value and its baseline flag, served from schema `rwb_reporting` | AC1, AC3 and the baseline read-back |
| Reconciliation fixture | PASS result sets for ten consecutive dates, one BREAK set, one over-tolerance variance and one new REC-05 orphan | AC3, X8, X9, X10 |

Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change shows as a failed test rather than a silent pass. The source and format of the real dump and the handover locations are Not specified in the source documents (GAP-2175; ASM-3508).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | The cutover is a pipeline command; the result is read through two operations of other stories |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule; JOB-04 is `RWB-P1-E1011-APP`'s |
| File | Two: the route-fact file and the baseline file, each with a checksum | One: the legacy dump, read once per run | Neither handover is a REST call; each owner loads its own file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data` (the last two named for completeness and used by no part of this story).

| Component | Type | Responsibility |
|---|---|---|
| CutoverExtractReader | Repository | Reads the dump once and selects the route facts, the case list rows of the cutover date and the baseline snapshots; no write, no `public` table, no other schema |
| CaseKeyMapper | Service | Maps each row onto its Workbench and ACE business keys and drops every ACE field |
| ScoreAbsenceCheck | Service | Proves over every artefact that no score, estimate or model column or value exists, and that the read path is `v_ace_score` |
| CaseListRowWriter | Service | Writes the row set of the cutover date into `case_list_row`, one row per case account and date, replacing the set whole |
| RouteFactHandover | Service | Writes the route facts with a checksum and a case count, and inserts nothing into `rwb_case` |
| BaselineSnapshotHandover | Service | Writes the baseline snapshots with a checksum and a count by measure and product group, and inserts nothing into `rwb_reporting` |
| CutoverEvidenceCounter | Service | Counts ten consecutive PASS dates with no unexplained variance and no new orphan; a break resets it and no table holds it |
| `V000x__dm011_case_list_cutover.sql` | Migration | The next free version: no route object, no measure object, no score column; records the row set, its field list and the replacement rule |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the 30 views, so the score read and the key resolution are its own SQL on its own login and add no contract hop — which is what makes the no-copy rule provable (BR5). DP-15 gives this story its version for the row set and gives each owner the sequence that loads its own handover, so no load needs a cross-schema write (GAP-2175; ASM-3508). DP-19 applies to the read of the result on SCR-45 and adds no screen. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of its own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no schedule (DP-10).

**Database and migrations**

- Reads the dump and `v_ace_score`; writes the case list rows of one date and one history row; writes no route row and no measure row anywhere.
- `case_list_row` is on this service's sequence with the field list of TSD P1 v3 T3.6 and `(business_date, account_key)` unique with `account_key NOT NULL`, so a replaced set leaves no duplicate.
- The version creates no route or measure object, adds no score column and grants nothing on `rwb_case` or `rwb_reporting` (BR1, BR8). Its description records the row set, the field list and the replacement rule.
- The version number is the next free one after the baseline and the two view versions of TSD P1 v3 T3.2; no version of the sequence names a COLLINS score, a route load or a measure object.
- The loads' sequences are rwb-case's and rwb-reporting's, described and applied by them (DP-15). The dump's format and the retention period are Not specified in the source documents (GAP-2175; ASM-3508).

**Configuration and reference data**

- No parameter and no reference list is read, so DP-06 and DP-07 are outside the pattern set. The cutover date, the handover locations and the retention period are release-pipeline configuration agreed at the wave 4 entry check; no value is written in code (FSD P1 v3 BR-P1-019; ASM-3508).
- The view's field IDs, the two schemas and the measure definitions are their owners'; the story consumes `route_code`, `route_state`, the dimension, the value and the baseline flag and re-implements no rule.
- Feature flag `rwb.source-data.score-route-cutover` from the platform flag library: off, the run does not start and the cutover record stays at Not started.
- Login `rwb_source_data`: SELECT on the 30 views, USAGE on `rwb_source_data`, no privilege in `public`, none in `rwb_case` and none in `rwb_reporting`.

**Build steps**

1. Reader and mapper over the dump fixture: the three artefacts, their keys, the dropping of every ACE field; AC1, X5.
2. ScoreAbsenceCheck with a fixture carrying a `score_value` column, proving the run fails; AC1, BR5.
3. CaseListRowWriter: first write, rerun replacing the set whole, and a refused row naming its field; AC1, X3, X12.
4. The `v_ace_score` read: a scored account and an account with no row, the latter carried without a legacy value and listed; AC1, X6.
5. Both handovers with checksums and counts, the assertion that this service writes zero rows of `rwb_case` and `rwb_reporting`, and the baseline flag and frozen state carried unchanged; AC1, BR4.
6. CutoverEvidenceCounter over the reconciliation fixture: ten PASS dates, a BREAK on the sixth, a variance, a missing ACE batch and a new orphan; AC3, X8, X9, X10.
7. The read-backs through the two contract mocks and the refusal path through the guard, with no file read after a deny; AC1, AC3, TC-DM-011-04.
8. The migration with no route or measure object and the row set, field list and replacement rule in its description, plus the repeated-apply check; AC1.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds the rows of one cutover date and no route or measure table, both handovers carry their checksums, no artefact holds a score column or value, the counter reads ten clean days and resets on a break, and no class of the service writes `rwb_case`, `rwb_reporting` or a `public` table.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | The ACE batch of a date in the ten is not COMPLETE, so the reconciliation cannot run | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-012 | Warning | The case list of a date misses the tolerance of its data product | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | A route fact, a case list row or a snapshot lacks a field it must carry | Enter {field}. |
| MSG-P4-002 | Error | The caller's Platform administration right is absent | You cannot {action} here. Your role does not include it. |

The four texts are copied character for character from the legacy story. {product} is the product code under test ("DP01" or "DP02") and {date} its last completed business date; in MSG-P1-012 {date} is the date of the case list and {product} the product group; {field} is the refused field name ("case_no", "account_key", "product_group", "route_code", "route_state", "measure_code", "definition_version", "dimension_code", "value" or the baseline flag); {action} is "run the score and route cutover" or "read the cutover result" and never a route, a measure or a field value.

### 15. Screens and states

No screen in this story. The legacy screen table names one — SCR-45 Data quality, "Loading; breaks" — which is a gateway-bff composite route over the published reads (DP-19; H `RWB-PLT-N001-CON`), belongs to the edge stories, and is rendered by no part of this story (ASM-3511).

| State | What the cutover record and SCR-45 show |
|---|---|
| Extract ready | The dump read once, the counts of route facts, case list rows and snapshots, the effect of the score-absence check, and the accounts with no score row |
| Loaded | The row set written, both handovers accepted with their checksums read back, and a clean-day count of zero |
| Ten clean days running | The dates counted so far, each with the PASS results of its reconciliation |
| Break | The date of the break, its BREAK rows, its variance or its orphan, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy tables read-only |

A run that cannot start shows in its failed state with the dump and the date named and no row set written, so a cutover that did not happen is never read as one that did.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-011-01 | AC1; BR2, BR3, BR4, BR5, BR6, BR8 | End to end | The cutover fixture: case "RW-2026-000611" on route "R3" with route state "FIRM_INSTRUCTED", rows for "2026-12-31" with account keys "ACC-SYN-000611" and "ACC-SYN-000888", a "CASES_BY_ROUTE" snapshot over "MORTGAGE" with its baseline flag true; a dump row carrying a `score_value` column; the `case_list_row` count before, after and after a rerun; the version applied once and again |
| TC-DM-011-03 | AC3; BR7, BR9 | End to end | The reconciliation fixture with ten PASS dates, then a BREAK, an over-tolerance variance and a new orphan; a date whose ACE batch is absent; the rwb-case mock answering `route_code` and `route_state` from "rwb_case" and the rwb-reporting mock answering the baseline from "rwb_reporting" |
| TC-DM-011-04 | Access refusal; BR6 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present; the row counts and the handover files before and after the refusal |

TC-DM-011-01 and TC-DM-011-03 are End to end because the run leaves the service boundary: it reads a file, resolves the score through a view and reports two loads other services performed. TC-DM-011-04 is Component because it exercises the guard at the published read. The legacy text of TC-DM-011-02 Reconcile the business keys is not repeated: AC2 and its test belong to `RWB-ITG-DM011-ITG` as `TC-DM-011-02-ITG`.

### 17. Guardrails

- No business value in code: the cutover date, the handover locations and the retention period are release configuration; the story writes no threshold, percentage, amount or date.
- No personal data in logs, tests or prompts: the fixtures are synthetic, `primary_person_key` is a business key and not an identity, and no name, identity number, contact point or address enters any artefact.
- ACE data only through `v_ace_*` views, and here the service owns them: one login, SELECT only, no `public` table named in any statement (BR6).
- No COLLINS score anywhere but the view: no score column and no score value exists in the row set or in either handover, and the check is mechanical (BR5; ASM-3509).
- No cross-schema write: the route facts are loaded by rwb-case and the baseline by rwb-reporting, each on its own sequence, and this story holds no grant on either schema (BR1).
- The baseline is never recomputed or unfrozen here (BR4).
- A break is never waived: a BREAK result, an over-tolerance variance or a new orphan resets the count, and a stale product is never a clean day (BR9).
- A rerun replaces and never duplicates: one row per case account and date (BR8).
- The sign-off is a release artefact, not a Workbench row, and no counter table is invented (BR9; ASM-3510).

### 18. Traceability

| Legacy RWB-DM-011 item | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | rwb-source-data, epic RWB-SVC-P1; `case_list_row` P1, `recovery_case` P3, `measure_snapshot` P9 |
| Epic | E2, release 31 December 2026 | Wave 4 from EP08; release 31 December 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | RWB-P1-E1001-APP and RWB-P1-E1069-APP |
| Decision | DL25 | BR9; the ten clean days and the zero-tolerance gate |
| Data | recovery_case DF-CAS-001 to DF-CAS-055; case_list_row DF-RPT-001 to DF-RPT-019; measure_snapshot DF-RPT-041 to DF-RPT-052 | Section 11; AC1; TC-DM-011-01 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Section 12.1; the reads belong to other stories |
| Screen and states | SCR-45 Data quality, Loading; breaks | Section 15; a gateway-bff composite route |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR6, BR7; section 17 |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Section 7; TC-DM-011-01 and TC-DM-011-03 |
| AC2 and TC-DM-011-02 | Reconcile the business keys, REC-05 | Owned by RWB-ITG-DM011-ITG as TC-DM-011-02-ITG |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_score` is read on the service login and no score column or value is copied into any artefact |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence for the row set, and the two loads on their owners' sequences |
| DP-19 | Template and Rules §R5.5 | SCR-45 is a gateway-bff composite route and the story renders no screen |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-45 |
| RWB-P1-E1001-APP | App development | H: the tables of this service and the data product catalogue |
| RWB-P1-E1069-APP | App development | H: the 30 views including `v_ace_score`, the login and the grant |
| RWB-P1-E1002-APP | App development | Owns the daily build of `case_list_row` and its publish status |
| RWB-P1-E1011-APP | App development | Builds JOB-04 and writes `reconciliation_result`, the evidence |
| RWB-ITG-DM011-ITG | Integration | Owns AC2 and asserts the keys and the break list across services |
| rwb-case cutover migration (P3) | App development | Loads the handed-over route facts into `rwb_case` |
| rwb-reporting (P9) | App development | Loads the handed-over baseline and owns the measure projection |

External dependencies: None.

### 19. Out of scope

- The load of the route facts into `rwb_case`, its migration and its rollback: P3's own cutover work (GAP-2175; ASM-3508).
- The load of the baseline into `rwb_reporting`, the freeze, the measure projection built from events and the dashboard it feeds: P9's own work (ASM-3511).
- AC2 Reconcile the business keys, REC-05, the break list and its report: `RWB-ITG-DM011-ITG`, with the reconciliation from `RWB-P1-E1011-APP`.
- JOB-04, its workflow, its activity, its rerun and its `reconciliation_result` rows: `RWB-P1-E1011-APP`.
- The daily build of `case_list_row`, its `publish_status` and the publish hold of a date: `RWB-P1-E1002-APP` and `RWB-P1-E1011-APP`.
- The case list API and screen, which stay with P3 behind gateway-bff: the read of a case and its route is the rwb-case contract's.
- SCR-45 Data quality and its route: the edge stories and the gateway-bff composite route.
- The 30 views, the login, the grant and the boundary test: `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`.
- The catalogue, the dictionary, the data contracts and the access rows: `RWB-P1-E1001-APP`.
- The COLLINS score and its daily ingestion into ACE: the ACE team's interface; this story reads the view and copies none of it.
- The retention period, the archival of the legacy tables and the decommissioning of the legacy Workbench: the cutover plan and the data steward; no source gives the period (GAP-2175; ASM-3508).
- The document and money extracts, which share the pattern of this story: `RWB-P1-DM010-APP` and `RWB-P1-DM013-APP`.
- The data lake, INT-19 and INT-20: removed, and no story of this key needs lake data (DP-17).
