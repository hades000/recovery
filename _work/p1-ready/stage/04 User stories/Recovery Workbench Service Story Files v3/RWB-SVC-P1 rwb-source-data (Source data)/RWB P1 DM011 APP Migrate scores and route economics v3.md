# RWB-P1-DM011-APP Migrate scores and route economics

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM011-APP |
| Work type | APP (App development) |
| Size | Set by the squad at refinement (DOR-RWB-P1-DM011-APP-16) |
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
| Contract dependencies | None for this story's code; the result reads of RWB-P1-E1011-CON and RWB-P1-AD018-CON, which it does not call |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), additive inside /v1 (RD-P1-005); this story provides no operation, event or workflow of its own |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-042, RD-P1-045 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-011 for the P1 cutover extract of the legacy case list rows, the route each open case carries and the baseline measure snapshots, the load of the service's own `case_list_row` for the cutover business date, the handover of the route facts to rwb-case and of the baseline to rwb-reporting, and the cutover evidence. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: targeted edits for version 3. Tool: Claude Sonnet 5.5.

**Version 3 changes** (D-RCV-60 P1 developer readiness):

- The load of `case_list_row` is removed: rwb-case holds the case list and P1 has no such table; the legacy case list rows are read but not migrated (RD-P1-024; finding #5).
- The route facts and the baseline are closed field lists by dictionary ID with `migration_source` and `migrated_at` (RD-P1-027; findings #1, #4).
- DL25 is applied with `recon.tolerance.pct` version 1 = 0.00 and one clean-day definition (RD-P1-042).
- AC1, AC3, AC4 and AC5 are rewritten or extended and AC6 to AC9 added (findings of the review's sections D and E).
- Reads, workflows, contract references and rollback follow the register (RD-P1-005, RD-P1-012, RD-P1-040, RD-P1-045; findings #2, #3, #6, #7, #8).
- Finishing pass: message references are Error and Message Standard v6; test case IDs of Test Cases v9 cited.

### 1. Story

As a **data steward (RW-DATASTEW)** I want **the route each open case carries and the route economics baseline the Workbench calculates migrated**, so that **the baseline and the route history survive cutover while the COLLINS score itself is read from ACE**.

- **Extract here:** one read of the legacy cutover dump for the open cases at cutover — their route facts and the baseline snapshots with their dimension, value and baseline flag (legacy AC1). The legacy case list rows in the dump are not carried: the case list is served by rwb-case from its own rows and P1 account reads (RD-P1-024).
- **Nothing is loaded here:** `rwb_source_data` has no `case_list_row` table and this story writes no business row in it (RD-P1-024).
- **Handover:** the route code and route state of each case go to P3 rwb-case and the baseline snapshots to P9 rwb-reporting, each as a file with a checksum, each loaded by its owner on its own sequence; this story writes no row of `rwb_case` and none of `rwb_reporting`.
- **No score carried:** no COLLINS score, estimate or model version is copied; the score is read through `v_ace_score` and its absence from every artefact is proved by a column-level check (ASM-3509).
- **Evidence:** ten consecutive business dates on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 with no new REC-05 orphan, read from the `reconciliation_result` rows JOB-04 writes, a break resetting the count (legacy AC3; DL25 option A applied by RD-P1-042; ASM-3510).
- **No REST operation, event, workflow or screen:** the cutover is a release-pipeline step, and SCR-45 Data quality is a gateway-bff composite route this story does not render, behind which the reconciliation of the clean days is read (DP-19; ASM-3511). This story therefore renders none of its empty, loading, error or no access states (section 15).

The legacy key is not withdrawn — route history and a frozen baseline are Workbench records no ACE table holds. What changes is who holds each: `recovery_case` is P3's and `measure_snapshot` is P9's (GAP-2175; ASM-3508); the legacy case list of a date is no longer stored by any service (RD-P1-024).

### 2. Business rationale

Route economics is the argument the recovery programme makes about itself. Each open case carries the route the rule set put it on, and the Workbench keeps the routing state that says where on that route it stands. Around those facts sits the baseline: measures of the portfolio at a chosen business date, frozen, so a later claim of improvement is measured against a number nobody can move. A route that arrives blank is a case nobody's rule is working; a baseline that is rebuilt rather than frozen measures itself.

**Why the two facts go to two owners.** A service writes only its own schema, so a cutover spanning two tables spans two owners: rwb-case holds the case and its state and rwb-reporting the measures and snapshots. The route code and route state are columns of the case, so they are the case service's; a baseline snapshot is one measure for one date, product and dimension value, so it is reporting's. The legacy case list rows have no target table: rwb-case composes the list at read time from its own rows and P1 account reads, so storing a copy in P1 would be the defect the target removes (RD-P1-024). So this story reads the dump once, hands the two facts over and inserts nothing (GAP-2175).

**Why the score is not carried.** Legacy AC1 is explicit, and the target keeps it in the schema and not only in a sentence: the legacy `score` table leaves the model, `v_ace_score` replaces it keyed by account rather than by case, and the case is reached through `case_account.account_key`. A copied score would be frozen at cutover and quoted for years, the opposite of what a daily COLLINS feed is for. The absence is therefore mechanical — every artefact is checked for a score column and a score value before it is handed over (ASM-3509).

**Why P1 holds the evidence.** `reconciliation_result` is a P1 table; REC-01 compares the ACE count with the open case accounts rwb-case returns and REC-05 uses the rwb-case key list (RD-P1-024). The ten clean days are counted from rows that already exist, and the baseline is read back from rwb-reporting through its contract (ASM-3510). What carries over unchanged: the case number, route code and route state of each case; the measure code, definition version, date, product group and dimension of each snapshot with its value and baseline flag; and the source and migration date of every record. No ACE field is carried, because those stay in ACE behind the views.

### 3. Preconditions

- The ownership reading is: route facts with P3 and baseline with P9, loaded by each owner (GAP-2175; ASM-3508); the case list, its API and screen with P3, and no `case_list_row` in P1 (RD-P1-024).
- The per-service Flyway contract `RWB-PLT-E1044-CON` is in place, with the sequence of `rwb_source_data` and its baseline, so this story takes the next free version and writes one history row (DP-15).
- rwb-case and rwb-reporting have added `migration_source varchar(20)` and `migrated_at timestamptz` to `recovery_case` and `measure_snapshot` in their own Flyway steps (RD-P1-027 item 3). The values of list LOV-MIGRATION-SOURCE are Pending: owner data owner (GAP-3275).
- The data product catalogue of `RWB-P1-E1001-APP` is live, so a product group and an account key have one named owner before a row is written.
- The 30 read-only `recovery.v_ace_*` views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`; this story reads `v_ace_score` and nothing else of ACE (DP-05).
- JOB-04, `ReconciliationWorkflow`, a child of `AceIngestCheck` after the ALS stamp (RD-P1-040), writes `reconciliation_result` for REC-01 and REC-02, with REC-05, graded PASS or BREAK under `recon.tolerance.pct` version 1 = 0.00; a run that cannot proceed writes no row (RD-P1-042). It is `RWB-P1-E1011-APP`'s build and this story only reads its rows.
- The gateway-bff composite route of `RWB-PLT-N001-CON` is in place, so the reconciliation behind the result is readable on SCR-45 without a screen of this story's own (DP-19).
- The cutover runs of rwb-case and rwb-reporting can receive a file on their own sequences and logins; neither must be deployed, because the handover is a file and the mocks answer until the loads are live (section 12.8).
- The synthetic dump fixture, the `v_ace_score` fixture and the two contract mocks exist before the first build, so no production data is needed.
- The dump's source and format, the handover locations, the retention period and the place of the sign-off are given by no source document (GAP-2175; ASM-3508; ASM-3510).
- The cutover reconciliation harness pack (environment and base hosts, synthetic cutover extract fixture, reconciliation extract and break-list fields, evidence format and retention, pass or fail gate, data seeding set) is agreed at the wave 4 entry check; its values are Not specified in the source documents (GAP-0451).

### 4. Flow

1. The release pipeline starts the cutover run for the cutover business date under the `rwb_source_data` service identity with one Idempotency-Key per run. The run is a pipeline step, not an API call (section 12.1).
2. CutoverExtractReader reads the legacy dump once and selects the route facts of each open case, the `account_key` values of each open case (for the score check only) and the baseline snapshots (DF-RPT-041 to DF-RPT-052). The legacy case list rows are not selected (RD-P1-024). Nothing is requested from the running legacy application.
3. CaseKeyMapper maps each row onto its Workbench business keys and adds none of its own: the case keeps its `case_id`, `case_no`, `route_code` and `route_state`, each snapshot the fields of section 11 (legacy AC1).
4. The mapper takes no ACE field — an account name, a balance, an identity number, a contact point or an address in the dump is dropped and never carried (legacy guardrails; DP-05).
5. ScoreAbsenceCheck runs over every artefact before it leaves the service: no score, estimate or model column exists and no value of those fields is present (legacy AC1; ASM-3509).
6. The handover files are assembled from the section 11 fields only, each with its row count, its checksum, the cutover business date and its `migration_source` value. No row is written to `rwb_source_data`.
7. RouteFactHandover writes the route facts to the location agreed with rwb-case, with a checksum and a case count, and BaselineSnapshotHandover writes the snapshots to the location agreed with rwb-reporting, with a checksum and a count by measure and product group. Each owner loads its own file; this story holds no grant on `rwb_case` or `rwb_reporting` (ASM-3508).
8. From the next business date JOB-04 reconciles the business keys to the views, and CutoverEvidenceCounter counts a clean day when every REC-01 and REC-02 row of the date is PASS under `recon.tolerance.pct` version 1 and no new REC-05 orphan appears on a migrated key (RD-P1-042 item 4; ASM-3510). A date with no result row is not a clean day.
9. A break resets the count to zero and lists the date with its result rows; at ten consecutive clean dates the cutover record moves to ready for sign-off, and the data steward signs off in the release pipeline's cutover record, not in a Workbench row.
10. After the sign-off the legacy tables stay read-only for their retention period and the records are served from the new schema — route facts from `rwb_case` and baseline from `rwb_reporting` (legacy AC3).
11. The version is applied on the sequence of `rwb_source_data`: it creates no table, no column and no score column, and records the extract, its field list and the read-only window in its description.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The dump is absent, unreadable or not the dump of the cutover business date | The run stops before any extract; no row written, nothing handed over, the pipeline step FAILED and the cutover record names the dump and the date | None | AC1 |
| X2 | A route fact lacks its `case_no`, `route_code` or `route_state` | The fact is refused and listed for the data steward; no partial route is handed over and no route is invented | MSG-GEN-001 | AC1, TC-DM-011-01 |
| X3 | A route fact lacks its `case_id` or `case_no`, or a snapshot lacks its `id` | The record is refused and listed, and the missing field is named | MSG-GEN-001 | AC1, AC6 |
| X4 | A snapshot lacks its `measure_code`, `definition_version`, its dimension, its value or its baseline flag | The snapshot is refused and listed, and the measure is handed over without that row | MSG-GEN-001 | AC1, TC-DM-011-01 |
| X5 | The dump carries a COLLINS score, an estimate or a model version | The field is dropped and step 5 proves its absence from every artefact; the run continues | None | AC1, TC-DM-011-01 |
| X6 | `v_ace_score` returns no row for an `account_key` of an open case | No legacy value replaces the missing score, and the account is listed for the data steward and the ACE team | None | AC1, AC3 |
| X7 | rwb-case or rwb-reporting rejects the handed-over file | No row is loaded by that service for that run, the mismatch is listed with entity and count, and the cutover record shows the handover FAILED | None | AC3, TC-DM-011-03 |
| X8 | A business date of the ten has a BREAK result or a new REC-05 orphan | The count resets to zero and the date and its rows are listed; the cutover record shows the break | None | AC3, TC-DM-011-03 |
| X9 | A REC-01 or REC-02 row of a date is BREAK | The date is no clean day, the variance is stated, and MSG-P1-012 and the reconciliation break alert are raised by the reconciliation (no publish status exists in P1) | MSG-P1-012 | AC3, AC8 |
| X10 | The ACE batch of a business date is not COMPLETED, so the reconciliation cannot run and writes no row | The date is no clean day and the product is named with its last completed business date | MSG-P1-001 | AC3 |
| X11 | A caller without the Platform administration right starts a handover or reads the result | The call is refused before any file is read | MSG-P4-002 | AC4, TC-DM-011-04 |
| X12 | The version is applied twice, or the run is repeated for the same business date | Flyway reports the version as already applied; a repeated run writes both handover files for the date again, replacing the earlier ones whole, and the cutover record keeps both checksums | None | AC1, AC9 |

X1 to X5 and X12 are exercised inside the story's own tests and carry no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One reader of the dump, one key mapper, one score-absence check, two handovers, one evidence counter and one Flyway version; the two loads, the reconciliation and the screen belong to other stories |
| Negotiable | The handover file format and location, the cutover record layout and the retention period are agreed at the wave 4 entry check; the story fixes the two artefacts, their fields and the no-score rule |
| Valuable | Every open case arrives on the route it had, the baseline is frozen before go-live, and no COLLINS score is quoted from a migrated row |
| Estimable | One reader, one mapper, one check, two handovers, one counter, one version and their test cases |
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
    And the route-fact file holds one row per open case with exactly the section 11 fields of "recovery_case" and the baseline file one row per snapshot with exactly the section 11 fields of "measure_snapshot"
    And each file records its row count, its checksum and the cutover business date, and each row its "migration_source" value
    And no "case_list_row" record is carried and no row of any "rwb_source_data" table is added or changed

  Scenario: AC3 Cut over (legacy RWB-DM-011 AC3)
    Given ten clean days on the migrated records
    Given nine consecutive business dates on which every REC-01 and REC-02 row is "PASS" under "recon.tolerance.pct" version 1 = 0.00 with no new REC-05 orphan, and a tenth such date
    Given the rwb-case contract mock returns the migrated case served from schema "rwb_case"
    Given the rwb-reporting contract mock returns the baseline measure snapshot served from schema "rwb_reporting"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And the cutover record holds the sign-off, the ten result sets, both file checksums and counts, both load acceptances and the retention window

  Scenario: AC4 A caller without the Platform administration right is refused before any file is read (new, D-RCV-60)
    Given a caller without the Platform administration right
    When the caller starts a handover or reads the result
    Then the call is refused before any file is read
    And the refusal shows MSG-P4-002 "You cannot run the score and route cutover here. Your role does not include it." or "You cannot read the cutover result here. Your role does not include it."
    And no handover file is written, and the same call with the right present is accepted

  Scenario: AC5 The migration writes no business row (new, D-RCV-60; rewritten by RD-P1-024)
    Given the route facts of recovery_case owned by P3 and the measure_snapshot rows owned by P9
    When the migration extracts them and hands them over
    Then it writes no row of rwb_case
    And it writes no row of rwb_reporting
    And it writes no row of rwb_source_data other than its flyway_schema_history row at deploy

  Scenario: AC6 A record without a required field stops its file (new, X2, X3, X4)
    Given a route fact without "route_state" and a snapshot without "value"
    When the mapper processes the extract
    Then each record is refused and listed with MSG-GEN-001 naming the field
    And the route fact is not handed over and the measure is handed over without that snapshot

  Scenario: AC7 No score or ACE value leaves (new, X5, BR5)
    Given a dump row carrying a "score_value" column and an account name
    When the score-absence check runs over both files
    Then neither file holds a score, estimate, model version, name or balance column or value

  Scenario: AC8 A break resets the clean-day count (new, RD-P1-042)
    Given nine consecutive clean business dates after the load
    When the next date holds a "BREAK" row or a new REC-05 orphan on a migrated key
    Then the clean-day count is 0 and the cutover record names the date, the REC code and its rows
    And the sign-off stays closed, and a date with no result row adds no clean day

  Scenario: AC9 A repeated run for one business date replaces whole (new, X12)
    Given both handover files for business date D are written
    When the step runs again for business date D
    Then both files are written again whole, the cutover record keeps both checksums and the later set is marked current
    And no row of any schema of the platform is written by this story
```

AC1 and AC3 are copied character for character from legacy RWB-DM-011. The added Givens are the two owners' contract answers — the route facts are P3's and the baseline is P9's, so the served case and the served snapshot are answered by those contracts and their mocks — and they change no legacy value. AC2 Reconcile the business keys (REC-05) is owned by `RWB-ITG-DM011-ITG` and is not copied here; this story only reads the reconciliation results that story asserts (ASM-3511). The case list rows named in the legacy AC1 Given are read from nowhere into a target: RD-P1-024 removes the stored case list, and no Then line of the legacy criterion asserts them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `recovery_case` and its route facts are P3's and `measure_snapshot` is P9's: P1 extracts and hands over, and writes no row of `rwb_case`, `rwb_reporting` or its own business tables | GAP-2175; ASM-3508; DP-05; RD-P1-024 |
| BR2 | The legacy case list rows (DF-RPT-001 to DF-RPT-019) are not migrated: the target is retired and rwb-case composes the list at read time | RD-P1-024; RD-P1-027 (exclusion: approving role solution architect, confirmation GAP-3280) |
| BR3 | The route code and route state are handed over unchanged and loaded by rwb-case; no route is recomputed here | Legacy AC1; DP-15 |
| BR4 | Each baseline snapshot keeps its dimension, its value and its baseline flag and is loaded frozen by rwb-reporting; this story neither recomputes nor unfreezes a measure | Legacy AC1; FSD P1 v3 A2.19 |
| BR5 | No COLLINS score is copied: no score, estimate or model column enters any artefact, and the score is read only through `v_ace_score` on the service login | Legacy AC1; TSD P1 v3 T3.3 view 26; ASM-3509 |
| BR6 | ACE data is read only through `recovery.v_ace_*` on the service's own login with SELECT, and no ACE field is copied into a migrated row | BR-P1-001-2; DP-05 |
| BR7 | A migrated row keeps its source and its migration date (`migration_source`, `migrated_at`, written by the owner's load) and never a copy of an ACE row | Legacy guardrails; RD-P1-027 |
| BR8 | A repeated run for one business date replaces that date's handover files whole; no file is partly written | X12; DP-15 |
| BR9 | The evidence is ten consecutive business dates on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 with no new REC-05 orphan; a break resets the count, and the sign-off sits in the cutover record of the release pipeline | Legacy AC3; FSD P1 v3 A2.11; DL25 option A (RD-P1-042); ASM-3510 |
| BR10 | The expected-return and sale-estimate records the Workbench calculates are not moved by this story: they are the rwb_valuation route-decision output (S1). This story moves only the route facts and the baseline snapshots. `case_no`, `route_code` and `route_state` are indirect identifiers or Customer data, Confidential: they leave only in the route-fact file, appear in no log, metric or prompt and are masked in UAT where the inventory says so | Architecture v5 Text Extract v1 slide 18; Data Classification v6; RD-P1-024 |

BR1, BR2 and BR8 are the boundary, the exclusion and the idempotence; BR3 and BR4 are the content of the two artefacts; BR5 and BR6 the view rule; BR9 the cutover gate.

### 9. State transitions

None for the case: this story changes no status, stage, route code or route state, because the routing state machine lives in rwb-case. The moves below are the states of the cutover itself.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The run reads the dump | The dump is of the cutover business date | Extract ready: both artefacts exist, the score-absence check has passed, and nothing is written to a schema |
| Extract ready | Both files are handed over | Both checksums and counts recorded and both owners accept | Loaded: both owners report their load and the clean-day count is zero |
| Loaded | JOB-04 writes a PASS result set for a date | Every REC-01 and REC-02 row PASS and no new REC-05 orphan | Ten clean days running: the count moves to the next date |
| Ten clean days running | JOB-04 writes a BREAK, raises an orphan, or the ACE batch is absent | The date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days running | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy tables stay read-only and the records are served from the new schema |

The record of each move is the cutover record of the release pipeline plus the `reconciliation_result` rows of the date. No event announces a move, because a cutover is not a business event of the case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the clean-day count and the baseline read-back, and signs off in the cutover record (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the check, the handovers and the counter; runs the tests; applies the version |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result, the reconciliation results and the baseline read-back; each holds Platform administration R |
| The ACE team lead | Answers for the `v_ace_score` row of an account and receives every account listed as having none |
| The rwb-case service identity | Loads the handed-over route facts through its own migration; this story never uses that login |
| The rwb-reporting service identity | Loads the handed-over baseline snapshots through its own migration; this story never uses that login |
| The `rwb_source_data` login | Reads the dump and `v_ace_score` and writes one history row at deploy; no business row and no write on `rwb_case` or `rwb_reporting` |
| No delegation of authority level applies | The cutover takes no credit decision, sets no route and changes no measure |

The role codes are rows of rwb-access and the read of the result authorises through the guard of the published read; this story adds no role and no grant. The legacy permission row — Platform administration R for the six roles above — is kept unchanged.

### 11. Data

The handover fields are one row per Logical Data Model v11 field (RD-P1-027): CARRY is a field of the target owner whose system of record is Workbench, EXCLUDE does not leave. The same rows are to be held in Source to Target Mapping v7, sheet Migration packages.

| BR Field ID | Entity | Field | Disposition | Note (classification, Data Classification v6) |
|---|---|---|---|---|
| DF-CAS-001 | `recovery_case` | `id` | CARRY | Not personal, Internal; case reference |
| DF-CAS-002 | `recovery_case` | `case_no` | CARRY | Indirect identifier, Confidential; masked in UAT |
| DF-CAS-007 | `recovery_case` | `route_state` | CARRY | Customer data, Confidential |
| DF-CAS-008 | `recovery_case` | `route_code` | CARRY | Customer data, Confidential |
| DF-CAS-003 to DF-CAS-006, DF-CAS-009 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | `recovery_case` | all other fields | EXCLUDE | Not a route fact; the case itself is DM-003's extract |
| DF-RPT-041 | `measure_snapshot` | `id` | CARRY | Not personal, Internal |
| DF-RPT-042 | `measure_snapshot` | `measure_code` | CARRY | Not personal, Internal |
| DF-RPT-043 | `measure_snapshot` | `definition_version` | CARRY | Not personal, Internal |
| DF-RPT-044 | `measure_snapshot` | `business_date` | CARRY | Not personal, Internal |
| DF-RPT-045 | `measure_snapshot` | `product_group` | CARRY | Not personal, Internal |
| DF-RPT-046 | `measure_snapshot` | `dimension_code` | CARRY | Not personal, Internal |
| DF-RPT-047 | `measure_snapshot` | `dimension_value` | CARRY | Not personal, Internal |
| DF-RPT-048 | `measure_snapshot` | `value` | CARRY | Not personal, Internal |
| DF-RPT-049 | `measure_snapshot` | `case_count` | CARRY | Not personal, Internal |
| DF-RPT-050 | `measure_snapshot` | `is_baseline` | CARRY | Not personal, Internal |
| DF-RPT-051 | `measure_snapshot` | `frozen` | CARRY | Not personal, Internal |
| DF-RPT-052 | `measure_snapshot` | `published_at` | CARRY | Not personal, Internal |
| DF-RPT-001 to DF-RPT-019 | `case_list_row` (retired) | all fields | EXCLUDE | RD-P1-024: no target table; approving role solution architect (confirmation GAP-3280) |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` | view fields | Not carried; read | Read only, to prove the score, its estimate and its route are the view's |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | reconciliation row fields | Not carried; read | The cutover evidence, written by JOB-04 |
| None (standard columns, LDM v11 sheet Standard columns) | `recovery_case`, `measure_snapshot` | `migration_source`, `migrated_at` | Provenance | The files state `migration_source` (values Pending, GAP-3275); each owner's load writes both |
| None: framework table | `flyway_schema_history` | Version, description, checksum | Write | One row, at deploy only |

`rwb_source_data` holds none of the three legacy tables: `case_list_row` is retired and this story writes no business row (BR1, BR2). The baseline flag and the frozen state are carried as the legacy rows held them (BR4). `v_ace_score` is the only path to a COLLINS score (BR5, BR6; ASM-3509). The handover file format, field order, location, access and retention are Pending: agreed at the wave 4 entry check, owner data steward with the solution architect (GAP-2175).

### 12. Contract

**12.1 REST operations provided**

None. The legacy story states "No endpoint in this story": the cutover is a release-pipeline command that reads a dump and writes two handover files, and no path of `/api/recovery/source-data/v1` is added here. The result is read through operations that other RWB-SVC-P1 stories publish and this story neither claims nor changes:

| Operation | Base | Owner story | What it shows of this story |
|---|---|---|---|
| `GET /admin/reconciliation/results` (API-P1-003; replaces the withdrawn `/admin/data-quality/exceptions`) | `/api/recovery/source-data/v1` | RWB-P1-E1011-APP (contract RWB-P1-E1011-CON) | The PASS and BREAK rows the clean-day count is read from |
| `GET /admin/jobs` | `/api/recovery/source-data/v1` | RWB-P1-AD018-APP (contract RWB-P1-AD018-CON) | The `ReconciliationWorkflow` runs behind the clean days; the cutover step is not a job of the P1 job set (RD-P1-012) |

**12.2 REST operations consumed**

None at run time. The run reads its own dump, its own view on its own login and writes its handover files; it calls no service and holds no C dependency. The rwb-case and rwb-reporting contracts are fixtures in the tests and the read-back of what each owner loaded (section 12.8).

**12.3 Events published**

None. No Kafka event, no outbox row of this story and no new schema on `rwb.source-data.events.v1`; AceDataReady and AceDataLate are the topic's events, published by `RWB-P1-E1015-APP` (RD-P1-003), and rwb-source-data does not consume them.

**12.4 Events consumed**

None. No event starts the cutover: the release pipeline starts it for the cutover business date, and the reconciliation behind the evidence is a child workflow of `AceIngestCheck` in `RWB-P1-E1011-APP` that consumes no event (RD-P1-040).

**12.5 Workflows and activities**

None added. JOB-04 `ReconciliationWorkflow` is the child workflow of `AceIngestCheck` built by `RWB-P1-E1011-APP` on task queue `rwb-source-data` (RD-P1-040); this story creates and changes no workflow, activity or child workflow and starts none.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job sits here: the cutover is a one-off pipeline run, and the reporting extract at 01:30 is rwb-reporting's own Schedule.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `case_list_row` | none | none | Retired: not created in P1 and not written (RD-P1-024) |
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the evidence, written by JOB-04 |
| `recovery_case` | `rwb_case` | P3 | Not owned and not written: the route facts are handed over as a file |
| `measure_snapshot` | `rwb_reporting` | P9 | Not owned and not written: the baseline is handed over as a file |

No statement of the story names a table in `public`, no statement writes another service's schema, and the only cross-schema read is the granted `recovery.v_ace_score` view (BR1, BR6).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | Synthetic route facts, account keys of open cases and snapshots: case "RW-2026-000611" on route "R3" with route state "FIRM_INSTRUCTED", account keys "ACC-SYN-000611" and "ACC-SYN-000888", business date "2026-12-31", and a "CASES_BY_ROUTE" snapshot over dimension "MORTGAGE" with its baseline flag true | AC1, AC3 and X2 to X6 |
| View fixture (`v_ace_score`) | The view as synthetic rows in a container, with a score row for "ACC-SYN-000611" and none for "ACC-SYN-000888" | AC1's score read and the no-row path, X6 |
| rwb-case contract mock | The migrated case with its route code and route state, served from schema `rwb_case` | AC1, AC3 and the route read-back |
| rwb-reporting contract mock | The baseline snapshot with its dimension, its value and its baseline flag, served from schema `rwb_reporting` | AC1, AC3 and the baseline read-back |
| Reconciliation fixture | PASS result sets for ten consecutive dates, one BREAK set, one over-tolerance variance and one new REC-05 orphan | AC3, X8, X9, X10 |

The reconciliation fixture follows the answer shape of rwb-source-data.yaml 5.1.0 (RD-P1-011). Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change shows as a failed test rather than a silent pass. The source and format of the real dump and the handover locations are Not specified in the source documents (GAP-2175; ASM-3508).

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
| CutoverExtractReader | Repository | Reads the dump once and selects the route facts, the account keys of open cases and the baseline snapshots; no write, no `public` table, no other schema |
| CaseKeyMapper | Service | Maps each record to the section 11 fields and drops every other field, the ACE fields and the legacy case list rows |
| ScoreAbsenceCheck | Service | Proves over every artefact that no score, estimate or model column or value exists, and that the read path is `v_ace_score` |
| HandoverManifest | Service | Records for each file its row count, checksum, business date and `migration_source` in the cutover record, and marks the current set of a date |
| RouteFactHandover | Service | Writes the route facts with a checksum and a case count, and inserts nothing into `rwb_case` |
| BaselineSnapshotHandover | Service | Writes the baseline snapshots with a checksum and a count by measure and product group, and inserts nothing into `rwb_reporting` |
| CutoverEvidenceCounter | Service | Counts ten consecutive clean dates under RD-P1-042; a break resets it and no table holds it |
| `V<next>__dm011_score_route_cutover.sql` | Migration | The next free version: creates no table, column or index; records the extract, its field list and the read-only window |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the 30 views, so the score read and the key resolution are its own SQL on its own login and add no contract hop — which is what makes the no-copy rule provable (BR5). DP-15 gives this story its version for the extract's record and gives each owner the sequence that loads its own handover, so no load needs a cross-schema write (GAP-2175; ASM-3508). DP-19 applies to the read of the result on SCR-45 and adds no screen. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of its own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no schedule (DP-10).

**Database and migrations**

- Reads the dump and `v_ace_score`; writes no business row; writes one history row at deploy. The schemas `rwb_case` (owner P3) and `rwb_reporting` (owner P9) are named only to bound this service's grants; their owners write them.
- No `case_list_row` table is created on the `rwb_source_data` sequence (RD-P1-024).
- The version creates no route or measure object, adds no score column and grants nothing on `rwb_case` or `rwb_reporting` (BR1). Its description records the extract, the field list and the read-only window.
- The version number is the next free one after the baseline and the two view versions of TSD P1 v3 T3.2; no version of the sequence names a COLLINS score, a route load or a measure object.
- The loads' sequences are rwb-case's and rwb-reporting's, described and applied by them (DP-15). The dump's format and the retention period are Not specified in the source documents (GAP-2175; ASM-3508).

**Configuration and reference data**

- No parameter and no reference list is read, so DP-06 and DP-07 are outside the pattern set. The cutover date, the handover locations and the retention period are release-pipeline configuration agreed at the wave 4 entry check; no value is written in code (FSD P1 v3 BR-P1-019; ASM-3508). Their parameter-catalog key and reference-data contract are Not specified in the source documents (DOR-RWB-P1-DM011-APP-20).
- The view's field IDs, the two schemas and the measure definitions are their owners'; the story consumes `route_code`, `route_state`, the dimension, the value and the baseline flag and re-implements no rule.
- Feature flag `rwb.source-data.score-route-cutover` from the platform flag library: off, the run does not start and the cutover record stays at Not started.
- Login `rwb_source_data`: SELECT on the 30 views, USAGE on `rwb_source_data`, no privilege in `public`, none in `rwb_case` and none in `rwb_reporting`.

**Rollback (RD-P1-045)**

- Switch `rwb.source-data.score-route-cutover` off first; redeploy the previous image tag and chart version only if the flag does not cover the fault, naming in the release note every P1 capability the redeploy reverts. A migration is never reversed and no `U*.sql` or down script exists; a faulty version is corrected by a new forward version. This version creates no object, so the previous tag runs unchanged. A file already loaded by rwb-case or rwb-reporting is not undone by P1.

**Build steps**

1. Reader and mapper over the dump fixture: the two artefacts, their fields, the dropping of every ACE field and of the case list rows; AC1, AC7, X5.
2. ScoreAbsenceCheck with a fixture carrying a `score_value` column, proving the run fails; AC1, BR5.
3. HandoverManifest: counts, checksums and business date, a repeated run replacing the files whole, and a refused record naming its field; AC6, AC9, X3, X12.
4. The `v_ace_score` read over the account keys of open cases: a scored account and an account with no row, the latter listed without a legacy value; AC1, X6.
5. Both handovers with checksums and counts, the assertion that this service writes zero rows of `rwb_case` and `rwb_reporting`, and the baseline flag and frozen state carried unchanged; AC1, BR4.
6. CutoverEvidenceCounter over the reconciliation fixture: ten PASS dates, a BREAK on the sixth, a missing ACE batch and a new orphan; AC3, AC8, X8, X9, X10.
7. The read-backs through the two contract mocks and the refusal path through the guard, with no file read after a deny; AC1, AC3, TC-DM-011-04.
8. The migration with no object and the extract, field list and read-only window in its description, plus the repeated-apply check; AC1.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no case list, route or measure table and no new row, both handovers carry their checksums, no artefact holds a score column or value, the counter reads ten clean days and resets on a break, and no class of the service writes `rwb_case`, `rwb_reporting` or a `public` table.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | The ACE batch of a date in the ten is not COMPLETED, so the reconciliation cannot run | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | A REC-01 or REC-02 row of a date in the ten is BREAK | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | A route fact or a snapshot lacks a field it must carry | Enter {field}. |
| MSG-P4-002 | Error | The caller's Platform administration right is absent | You cannot {action} here. Your role does not include it. |

MSG-P1-001 and MSG-P1-012 are copied character for character from the Error and Message Standard (current version v6); MSG-GEN-001 and MSG-P4-002 are copied character for character from the legacy story. {product} is the product code under test ("DP01" or "DP02") and {date} its last completed business date; in MSG-P1-012 {date} is the date of the case list and {product} the product group; {field} is the refused field name ("id", "case_no", "route_code", "route_state", "measure_code", "definition_version", "dimension_code", "value" or the baseline flag); {action} is "run the score and route cutover" or "read the cutover result" and never a route, a measure or a field value.

### 15. Screens and states

No screen in this story. The legacy screen table names one — SCR-45 Data quality, "Loading; breaks" — which is a gateway-bff composite route over the published reads (DP-19; H `RWB-PLT-N001-CON`), belongs to the edge stories, and is rendered by no part of this story (ASM-3511).

| State | What the cutover record and SCR-45 show |
|---|---|
| Extract ready | The dump read once, the counts of route facts and snapshots, the effect of the score-absence check, and the accounts with no score row |
| Loaded | Both handovers accepted with their checksums read back, and a clean-day count of zero |
| Ten clean days running | The dates counted so far, each with the PASS results of its reconciliation |
| Break | The date of the break, its BREAK rows, its variance or its orphan, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy tables read-only |

The empty, loading, error and no-access states of SCR-45 belong to the console stories; this story defines none.

A run that cannot start shows in its failed state in the cutover record, with the dump and the date named and no handover file written, so a cutover that did not happen is never read as one that did.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-011-01 | AC1; BR2, BR3, BR4, BR5, BR6, BR8 | End to end | The cutover fixture: case "RW-2026-000611" on route "R3" with route state "FIRM_INSTRUCTED", account keys "ACC-SYN-000611" and "ACC-SYN-000888" for business date "2026-12-31", a "CASES_BY_ROUTE" snapshot over "MORTGAGE" with its baseline flag true; a dump row carrying a `score_value` column and legacy case list rows; every `rwb_source_data` row count before and after; the version applied once and again |
| TC-DM-011-03 | AC3; BR7, BR9 | End to end | The reconciliation fixture with ten PASS dates, then a BREAK and a new orphan; a date whose ACE batch is absent; the rwb-case mock answering `route_code` and `route_state` from "rwb_case" and the rwb-reporting mock answering the baseline from "rwb_reporting" |
| TC-DM-011-04 | AC4; Access refusal; BR6 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present; the row counts and the handover files before and after the refusal |
| TC-DM-011-05 | AC5; BR1 | Component | The legacy cutover extract fixture, run through the extract and both handovers; the writes the run issues, showing none to `rwb_case`, `rwb_reporting` or a business table of `rwb_source_data` |
| TC-P1-DM011-APP-01 | AC6; X2 to X4 | Component | A route fact without `route_state`, a snapshot without `value` |
| TC-P1-DM011-APP-02 | AC7; BR5 | Component | A dump row with a score column and an account name |
| TC-P1-DM011-APP-03 | AC8; X8, X9 | Component | Nine clean dates, then a BREAK, a new orphan and a date with no row |
| TC-P1-DM011-APP-04 | AC9; BR8; X12 | Component | The step run twice for one business date |

TC-DM-011-01 and TC-DM-011-03 are End to end because the run leaves the service boundary: it reads a file, resolves the score through a view and reports two loads other services performed. TC-DM-011-04 is Component because it exercises the guard at the published read. The rows are held in Test Cases v9, tab Story test cases. The legacy text of TC-DM-011-02 Reconcile the business keys is not repeated: AC2 and its test belong to `RWB-ITG-DM011-ITG` as `TC-DM-011-02-ITG`.

### 17. Guardrails

- No business value in code: the cutover date, the handover locations and the retention period are release configuration; the story writes no threshold, percentage, amount or date.
- No personal data in logs, tests or prompts: the fixtures are synthetic, `primary_person_key` is a business key and not an identity, and no name, identity number, contact point or address enters any artefact.
- ACE data only through `v_ace_*` views, and here the service owns them: one login, SELECT only, no `public` table named in any statement (BR6).
- No COLLINS score anywhere but the view: no score column and no score value exists in either handover, and the check is mechanical (BR5; ASM-3509).
- No cross-schema write: the route facts are loaded by rwb-case and the baseline by rwb-reporting, each on its own sequence, and this story holds no grant on either schema (BR1).
- The baseline is never recomputed or unfrozen here (BR4).
- A break is never waived: a BREAK result or a new orphan resets the count, and a date with no result row is never a clean day (BR9).
- A rerun replaces the handover files of the date whole and never duplicates them (BR8).
- The sign-off is a release artefact, not a Workbench row, and no counter table is invented (BR9; ASM-3510).

### 18. Traceability

| Legacy RWB-DM-011 item | Value (verbatim) | Feature | L3 process | Where it lands |
|---|---|---|---|---|
| Module | P1 Recovery data engine | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | rwb-source-data, epic RWB-SVC-P1; `recovery_case` P3, `measure_snapshot` P9, `case_list_row` retired (RD-P1-024) |
| Epic | E2, release 31 December 2026 | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Wave 4 from EP08; release 31 December 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | RWB-P1-E1001-APP and RWB-P1-E1069-APP |
| Decision | DL25 | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | BR9; the ten clean days; DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00, for Data lead confirmation; ASM-0728, ASM-0735, ASM-0743 confirmed with the tolerance named, ASM-2602 closed |
| Data | recovery_case DF-CAS-001 to DF-CAS-055; case_list_row DF-RPT-001 to DF-RPT-019; measure_snapshot DF-RPT-041 to DF-RPT-052 | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Section 11, which excludes `case_list_row` (RD-P1-024); AC1; TC-DM-011-01 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Section 12.1; the reads belong to other stories |
| Screen and states | SCR-45 Data quality, Loading; breaks | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Section 15; a gateway-bff composite route |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Section 10 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | BR6, BR7; section 17 |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Section 7; TC-DM-011-01 and TC-DM-011-03 |
| AC2 and TC-DM-011-02 | Reconcile the business keys, REC-05 | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM011-APP-2) | Owned by RWB-ITG-DM011-ITG as TC-DM-011-02-ITG |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_score` is read on the service login and no score column or value is copied into any artefact |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence for the extract's record, and the two loads on their owners' sequences |
| DP-19 | Template and Rules §R5.5 | SCR-45 is a gateway-bff composite route and the story renders no screen |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-45 |
| RWB-P1-E1001-APP | App development | H: the tables of this service and the data product catalogue |
| RWB-P1-E1069-APP | App development | H: the 30 views including `v_ace_score`, the login and the grant |
| RWB-P1-E1002-APP | App development | Builds the account read rwb-case uses to compose its case list; this story writes no list row (RD-P1-024) |
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
- The case list: rwb-case composes it from its own rows and the P1 account read; P1 builds no `case_list_row` and has no publish status (RD-P1-024).
- The case list API and screen, which stay with P3 behind gateway-bff: the read of a case and its route is the rwb-case contract's.
- SCR-45 Data quality and its route: the edge stories and the gateway-bff composite route.
- The 30 views, the login, the grant and the boundary test: `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`.
- The catalogue, the dictionary, the data contracts and the access rows: `RWB-P1-E1001-APP`.
- The COLLINS score and its daily ingestion into ACE: the ACE team's interface; this story reads the view and copies none of it.
- The retention period, the archival of the legacy tables and the decommissioning of the legacy Workbench: the cutover plan and the data steward; no source gives the period (GAP-2175; ASM-3508).
- The document and money extracts, which share the pattern of this story: `RWB-P1-DM010-APP` and `RWB-P1-DM013-APP`.
- The data lake, INT-19 and INT-20: removed, and no story of this key needs lake data (DP-17).

### 20. Remaining delivery steps

- Size the story at refinement (owner: squad).
- Record the EP08 epic design sign-off (owner: solution architect).
- Bring the contract stories this story builds against to Done and publish the rwb-case and rwb-reporting fakes at pinned versions (owner: contract owners).
- Agree the dump source and format, both handover file formats, locations, access, retention and load acceptance at the wave 4 entry check (owner: data steward with the solution architect; GAP-2175).
- Agree the harness environment, fixtures, evidence and pass gate (owner: integration lead; GAP-0451).
- Confirm the RW-DATASTEW role and its permission row in rwb-access (owner: access owner).
- Confirm the removal of the stored case list (owner: solution architect, programme directive owner; GAP-3280).
- Give the values of LOV-MIGRATION-SOURCE (owner: data owner; GAP-3275).
- Load the synthetic fixtures in DEV (owner: squad).
