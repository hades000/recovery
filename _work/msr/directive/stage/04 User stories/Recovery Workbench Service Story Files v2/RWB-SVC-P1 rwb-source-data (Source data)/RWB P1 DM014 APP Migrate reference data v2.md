# RWB-P1-DM014-APP Migrate reference data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-DM014-APP-16) |
| Patterns applied | DP05, DP07, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P1-DM014-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-014 for the P1 cutover extract of the Workbench reference versions, their rows and the lists of values the Workbench owns, and for the handover of that extract to the reference-data contract of rwb-case. No other change. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 15 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **the legacy Workbench reference versions, their rows and the lists of values that the Workbench owns read once at cutover, kept whole with their table code, version number, valid from date and approver, and handed over in one file per table code in the load shape of the rwb-case reference-data contract**, so that **the versions in force at go-live are the ones the business approved, every rule row names the test case that proves it, and no service keeps a second copy of a list that ACE holds**.

The legacy key is **split, not preserved**: its three entities are Workbench records that no ACE table holds, but the service that owns them after the split is not the service that can read the legacy cutover dump. The Ownership Map puts `reference_version`, `reference_row` and `lov_value` with **P3 rwb-case** under the reference-data ruling (DP-07) and puts `rule_row` and `rule_test_case` with **P7 rwb-decision**. This story therefore extracts and hands over, and loads neither (GAP-2179; ASM-3521).

- **Extract, here:** the cutover run reads the legacy cutover dump once, selects the table codes the Workbench owns, keeps every version fact with every row key and value, and writes one file per table code with its checksum and row count. It inserts nothing into `rwb_source_data` (ASM-3521).
- **Handover, here:** each file is posted to `POST /api/recovery/case/v1/admin/reference-loads` with `table`, `validFrom` and an `Idempotency-Key`, and the returned load id is kept in the cutover record.
- **Load and approval, in rwb-case:** rwb-case loads the file into `rwb_case`, verifies it, and an approver who is not the author approves it, so the version in force is served from the schema of the service that owns it (RWB-P3-E1043-CON; DP-07; DP-15).
- **Rule rows:** each rule row carries the test case that proves it in its own row data, and is checked before the handover. The executable rule package and its registry stay with rwb-decision, which this story neither calls nor governs (ASM-3523).
- **No list that ACE holds is loaded:** the action codes, the products, the branches and the holidays are read through `v_ace_efs_action_code`, `v_ace_product`, `v_ace_branch` and `v_ace_holiday` on the `rwb_source_data` login and never enter a file (ASM-3522; DP-05).
- **Cutover evidence, here:** ten consecutive business dates on which the reconciliation of the case list to `v_ace_account` is PASS with no unexplained variance and no new REC-05 orphan, and on which the read-back of each version in force matched the file. A break resets the count (ASM-3524).
- **Sign-off, in the release pipeline:** the data steward signs the cutover record, the legacy tables stay read-only for their retention period, and the migrated records are served from `rwb_case` (legacy AC3).
- **No endpoint, event, workflow or screen of its own:** the cutover is a release-pipeline command, publishes nothing on `rwb.source-data.events.v1`, and DP-19 applies to the existing monitor screen only.

### 2. Business rationale

Reference data is the part of the Workbench that decides without a person: which band an exposure falls in, which queue a case goes to, which service level applies, which approval limit a settlement needs, which template a notice uses and which legal period governs a step. Every one of those answers is a row of a versioned table, and the version that produced the answer is written into the decision record. At go-live the business approves the versions in force. If the cutover loads different rows, or a version nobody approved, every decision taken on the first morning is taken under a rule the business never signed. That is why the legacy outcome is a cutover gate rather than a deployment step.

The legacy story puts the position in its own words: "As a data steward, I want the rules, the approval limits, the lists of values and the letter templates that the Workbench owns migrated as versioned reference data, so that the versions in force at go-live are the ones the business approved." Its guardrails row fixes the boundary this story keeps: "No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row."

**Why P1 extracts and P3 loads.** In the monolith the reference tables sat in the same schema and process as the data engine, so migrating and serving were one act. After the split the case, allocation and timer engines read their reference data across the reference-data contract of rwb-case, which owns the three tables, while the data engine is the only component that can read the legacy cutover dump and the ACE views. `rwb-source-data` owns neither reference table and writes only its own schema (DP-01), so what only it can do is keep the version facts intact and hand them over in the shape the owner's contract accepts.

**Why the ACE lists stay where they are.** The action codes, the products, the branches and the holidays look like reference data and are not: ACE ingests them from EFS, the core bank and the bank calendar, and P1 reads them through four of its 30 views. Copying them would create a second system of record for a list the bank already maintains, wrong the first morning the bank changed a holiday. Legacy AC1 forbids the re-load in the same sentence that names the four views, and this story keeps both halves (ASM-3522; DP-05).

**What legacy AC2 means in the target.** Its "reference data service" exists in no source document. In the target rwb-case answers every version in force with its row count, its content hash and its approver, because those are columns of the version it holds, and its verify operation answers per row and per column. This story compares that answer with the file it handed over; the rule-row half is checked inside the same file, where every rule row carries its test case (ASM-3523).

**What the split adds.** The load needs no cross-schema grant, no shared table and no second login, because the extract is produced by the data engine and consumed by the owner. The ten days are counted from reconciliation results that already exist for every business date, so the sign-off rests on data rather than on a cutover meeting. And this story's Flyway version creates no reference object, so nobody later mistakes `rwb_source_data` for a second home of the reference tables (DP-15).

### 3. Preconditions

| Precondition | Why it is needed | Where it comes from |
|---|---|---|
| `RWB-P1-E1001-APP` is done | The data products, their loads and the reconciliation results exist, and the clean-day count is read from them | H dependency, same lane |
| `RWB-P1-E1069-APP` is done | The read-only ACE views and the boundary rule are in place, so the four list views are readable on the service login | H dependency, same lane |
| `RWB-PLT-E1043-CON` is done | The platform side of the reference-data contract and its fake are fixed, so the client library compiles on Day 1 | H dependency, DP-07 |
| `RWB-PLT-E1044-CON` is done | The per-service Flyway sequence and its history table exist, so this story's version has a home | H dependency, DP-15 |
| `RWB-PLT-N001-CON` is done | The gateway-bff route that serves the existing monitor screen is fixed, so the cutover result is readable | H dependency, DP-19 |
| The legacy cutover dump is released to the run | Nothing can be extracted without it | Release pipeline; source and format are not specified (GAP-2179; ASM-3525) |
| The data steward and an approver who is not the author are named for the cutover window | The approval must be a second person | Reference-data contract rule BR4; no name is recorded in this story |

### 4. Flow

1. The release pipeline starts the cutover command for the cutover business date under the recovery service identity. No API call and no event starts it.
2. The extract reads the legacy cutover dump once and selects the `reference_version` rows whose table code the Workbench owns, with their version number, version label, valid from and valid to dates and approver. The rule rows and their test cases are not read; they stay with the rule registry of rwb-decision.
3. For each selected version it reads the `reference_row` and `lov_value` rows, keeping each row key and each row value exactly as the dump holds them, and drops any column whose values come from an ACE list.
4. It reads `v_ace_efs_action_code`, `v_ace_product`, `v_ace_branch` and `v_ace_holiday` on the `rwb_source_data` login and refuses the extract if a file would carry a row of a list that ACE holds. No row of those views is written anywhere.
5. It writes one file per table code with the version facts, the rows, the row count and the content hash of the file, and records both in the cutover record.
6. It posts each file to `POST /api/recovery/case/v1/admin/reference-loads` with `table`, `validFrom` and an `Idempotency-Key`, and keeps the returned load id and its status.
7. It calls the verify operation on each load id and reads each version in force back through `GET /api/recovery/case/v1/admin/lists/{listCode}` with the cutover date, comparing row count, content hash, approver and valid from date with the file. Approval of each version is done by rwb-case, not by this story.
8. For each business date it reads `reconciliation_result` for the REC-01 to REC-05 checks of that date and the read-back of step 7, and counts a clean day only when every check is PASS and no new REC-05 orphan exists. A break resets the count.
9. When ten consecutive clean dates exist, the data steward signs the cutover record. The legacy tables become read-only for their retention period and the service answers from `rwb_case`. A break before the sign-off leaves the count at zero and the pipeline stops at the gate.

### 5. Exception paths

| ID | Condition | Result | Covered by |
|---|---|---|---|
| X1 | The legacy dump is absent, unreadable, or holds no version for a table code the Workbench owns | The run stops before any load call, the cutover record names the table code, and nothing is handed over | AC1 |
| X2 | A version row has no table code, no version number, no valid from date or no approver | The file for that table code is refused whole; the other table codes may proceed | AC1 |
| X3 | A file would carry a row of `v_ace_efs_action_code`, `v_ace_product`, `v_ace_branch` or `v_ace_holiday` | The ACE-list guard refuses the file and names the view; no ACE row is copied or written | AC1 |
| X4 | `POST reference-loads` answers 409 because an approved version already has this valid from | The load is not repeated; the existing version stays in force and the break is recorded | AC2 |
| X5 | The verify operation answers a failed check, or the read-back differs from the file in row count, content hash, approver or valid from date | The version is not approved; the difference is listed and never repaired in place | AC2 |
| X6 | The legacy dump holds rule rows or rule test cases | They are not read or handed over by this story; they stay with the rule registry of rwb-decision | AC2 |
| X7 | The count of clean dates is broken by a BREAK result or a new REC-05 orphan | The count resets to zero and the gate stays closed | AC3 |
| X8 | A caller without the platform-administration right tries to run or re-run the cutover | The action is refused with MSG-P4-002 | AC3 |

### 6. INVEST check

| Letter | Assessment | Result |
|---|---|---|
| Independent | The extract reads its own dump and the four views, and its only outward call is the published reference-data contract with a fake on Day 1; it can be built and tested alone | Pass |
| Negotiable | The packet layout, the counting of the clean days and the place of the sign-off are stated as assumptions and may change without changing the criteria | Pass |
| Valuable | It is the only step that guarantees the versions in force on the first morning are the versions the business approved | Pass |
| Estimable | One reader, one mapper, one guard, one writer, one read-back and one evidence reader, with four legacy criteria | Pass |
| Small | One service, one release-pipeline command, no new endpoint, no event, no workflow, no table; the load belongs to another service | Pass |
| Testable | Four legacy test cases, a fixture dump per table code, the contract fake and ten PASS dates prove every criterion | Pass |

### 7. Acceptance criteria

```gherkin
Feature: Migrate reference data

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-014 AC1)
    Given the legacy Workbench reference versions, their rows and the lists of values that the Workbench owns
    When the migration reads them
    Then each version keeps its table code, its version number, its valid from date and its approver, and each row its key and its data
    And no list that ACE holds is re-loaded, because the action codes, the products, the branches and the holidays are read from v_ace_efs_action_code, v_ace_product, v_ace_branch and v_ace_holiday

  Scenario: AC2 Reconcile the versions (legacy RWB-DM-014 AC2)
    Given the rwb-case reference-data contract mock returns, for each table code, the approved version in force with its row count, its content hash and its approver
    And the migrated reference versions
    When the reference data service validates them
    Then every version in force has its row count, its content hash and its approver
    And no rule row or rule test case is read or written by this story

  Scenario: AC3 Cut over (legacy RWB-DM-014 AC3)
    Given ten clean days on the migrated records
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema

  Scenario: AC4 A repeated load writes nothing and returns the first load (new, D-RCV-60)
    Given a reference load already accepted for a table code, valid from date and content hash
    When the same load is posted again
    Then no row is written and the first load is returned

  Scenario: AC5 A load status the contract does not allow is refused (new, D-RCV-60)
    Given the rwb-case contract returns for a load a status it does not allow
    When the extract reads that status
    Then the refusal is recorded in the cutover record and the pipeline stops at the gate
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | No value a business person may change is written in code; it is read from reference data with its version | BR-P1-001, BR-P1-002; legacy guardrails | AC1; TC-DM-014-01 |
| BR2 | A version takes effect only after an approver who is not the author approves it | Reference-data contract BR4; ADR-012 | AC2; TC-DM-014-02 |
| BR3 | No list that ACE holds is re-loaded; the four views are the only read path for them | Legacy AC1; DP-05 | AC1; TC-DM-014-01 |
| BR4 | Rule rows and their test cases are not loaded by this story; they stay with the rule registry of rwb-decision | Legacy AC2; GAP-2179 | AC2; TC-DM-014-02 |
| BR5 | The legacy tables stay read-only for their retention period, and the records are served from `rwb_case` | Legacy AC3 | AC3; TC-DM-014-03 |
| BR6 | A repeated load of the same table, valid from date and content hash writes nothing and returns the first load | Reference-data contract BR5 | AC4; TC-DM-014-05 |

### 9. State transitions

| From | Event | To | Evidence |
|---|---|---|---|
| none | The file is posted and every load check passes | VALIDATED | 201 with the load id and the row count |
| VALIDATED | A person other than the author approves | APPROVED | 200 with the approver and the approval time |
| APPROVED | The valid from date is reached | In force | `GET /admin/lists/{listCode}` with `asOf` returns it |
| In force | A later version reaches its valid from date | Superseded | The same read returns the later version |
| APPROVED | An administrator rolls the version back with a reason | ROLLED_BACK | P3 admin operation; not this story |
| Cutover record: counted | Ten consecutive clean business dates | Signed off | The data steward's signature in the release pipeline |
| Cutover record: counted | A BREAK result or a new REC-05 orphan | Count reset | The same evidence read, over the dates since the break |

### 10. Authority

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

The cutover command runs under the recovery service identity; a person starts it through the release pipeline and needs the platform-administration right above, otherwise MSG-P4-002 is returned. The approval is the act of the approver in rwb-case, whose right is resolved on the rwb-access authorise operation by that service, not by this story. The signature on the cutover record is the data steward's; the auditor and compliance roles read the record.

### 11. Data

The legacy Data table, copied character for character:

| Entity | Fields | BR Field IDs |
|---|---|---|
| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |
| reference_version | id, table_code, version_no, version_label, valid_from, valid_to and 16 more | DF-REF-159 to DF-REF-180 |
| reference_row | id, version_id, row_key, row_data | DF-REF-181 to DF-REF-184 |

**What a file carries.** Per table code: the table code, the version number, the version label, the valid from and valid to dates and the approver of the version; then one line per row with its row key and its row data; then the row count and the content hash of the file. A list of values travels as its version: the list code, the value code, the labels and the sort order of each value. Every record keeps its source and its migration date. The file format is not specified in the source documents (GAP-2179; ASM-3525).

**What is read here and written nowhere.** `reconciliation_result` (P1) for the clean-day count, and the four ACE views for the guard: `v_ace_efs_action_code` (DF-ACE-128 to 130), `v_ace_product` (DF-ACE-146 to 150), `v_ace_branch` (DF-ACE-151 to 154) and `v_ace_holiday` (DF-ACE-155 to 159). No reference table, no list table and no copy of an ACE row exists in `rwb_source_data` after this story. The three tables land in the schema of their owner, `rwb_case`, as BR5 states. The load into that schema is the owner's Flyway step under `RWB-PLT-E1044-CON`, run by the owner's migrator login created by `RWB-PLT-N011-DB`; this story never writes another schema.

### 12. Contract

**12.1 REST operations provided**

None. The cutover is a release-pipeline command under the service identity, and the legacy story says the same: "No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract." No path is added to `/api/recovery/source-data/v1`.

**12.2 REST operations consumed**

| Operation | Provider and dependency | Purpose |
|---|---|---|
| `POST /api/recovery/case/v1/admin/reference-loads` | P3 rwb-case, `RWB-P3-E1043-CON` | Load one file with `table`, `validFrom`, an `Idempotency-Key`; answers 201 with the load id, the table, the valid from date, status VALIDATED and the row count |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify` | P3 rwb-case, `RWB-P3-E1043-CON` | Verify the validated load; answers the check result per row and per column |
| `GET /api/recovery/case/v1/admin/lists/{listCode}?asOf=YYYY-MM-DD` | P3 rwb-case, `RWB-P3-E1043-CON` | Read back the version in force with its row count, content hash, approver and rows; 404 with MSG-P3-027 when no version is in force |

This contract is the C dependency and never blocks the build: the client is written against the published contract and its fake from Day 1, and a drift between the fake and the contract fails the build. Each call is one hop with a 2 s timeout and a breaker (DP-07; ADR-020). No operation of rwb-decision is consumed here.

**12.3 Events published**

None. No outbox row is written and no schema is added to `rwb.source-data.events.v1`; no reference-data event exists in the catalogue.

**12.4 Events consumed**

None. The cutover is started by the release pipeline for a business date. The reconciliation whose results are counted is started by its own trigger in `RWB-P1-E1011-APP`.

**12.5 Workflows and activities**

None added. The story starts no workflow, registers no activity and joins no child workflow on the `rwb-source-data` queue.

**12.6 Schedules**

None. The cutover is a one-off pipeline run and the clean days are read from rows that another story's trigger already writes; no Temporal Schedule and no legacy job sits here.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only; written by its own job |
| `reference_version`, `reference_row`, `lov_value` | `rwb_case` | P3 | Not owned, not written: handed over through the contract |

The Flyway version creates no table, no column, no index and no grant, and records the extract's definition, its field list and the read-only window in its description. The source, the format and the length of the retention period of the legacy tables are not specified in the source documents (GAP-2179; ASM-3525).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| rwb-case reference-data fake (`RWB-P3-E1043-CON`) | The three operations above, the version projection with row count, content hash and approver, and the 404 no-version refusal | AC1, AC2 and the read-back |
| Legacy extract fixture | Synthetic `reference_version`, `reference_row` and `lov_value` rows for two table codes, one version in force, one approved later, and one row set carrying an ACE product column | AC1 and X2 to X4 |
| View fixtures | One row per ACE view used by the guard, none of them in a file | AC1, X3 |
| Reconciliation fixture | PASS result sets for ten consecutive dates, one BREAK set, one date with no ACE batch | AC3, X7 |

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | Three operations of one contract | One hop, 2 s timeout, breaker, idempotency key on the load; the approval is the approver's act in rwb-case, not a call of this story |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule |
| File | None | One | The legacy cutover dump, read once per run; one handover file per table code is written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.reference`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and queue `rwb-source-data` (the last two are named for completeness and used by nothing here).

| Component | Type | Responsibility |
|---|---|---|
| ReferenceVersionReader | Repository | Reads the dump once and selects the versions of the Workbench table codes |
| ReferenceRowReader | Repository | Reads the rows and list values of each selected version, keeping every key and value |
| ReferenceVersionMapper | Service | Keeps the version facts and the row key and data; drops every ACE list column |
| AceListGuard | Service | Reads the four views on the service login and refuses a file that would carry a list ACE holds |
| ReferenceHandoverWriter | Service | Writes one file per table code with its checksum and row count, and posts it with its idempotency key |
| ReferenceReadBack | Service | Verifies each load and reads each version in force back through the contract, comparing four facts |
| CutoverEvidenceCounter | Service | Reads `reconciliation_result` per business date and counts ten consecutive clean dates; a break resets it |
| `V<nnnn>__dm014_reference_extract.sql` | Migration | `<nnnn>` is the next free four-digit number of the rwb-source-data Flyway sequence (V0001 to Vnnnn), taken at merge: creates no object and records the extract, its field list and the read-only window |

| DP | Legacy marker | Pattern applied | Dependency added |
|---|---|---|---|
| DP-05 | `v_ace_*`, AceSourceQuery | Read through the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H `RWB-PLT-E1044-CON` |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-05 applies in its own-service form, because this is the service that owns the 30 views: the guard is its own SQL on its own login and adds no hop. DP-07 shapes the whole output, since the file is written in the contract's load shape and the reconciliation is the contract's read. DP-15 gives the story its version and the history row, with no schema change. DP-19 is used only by the existing monitor screen that reads the result. No other pattern applies: no event, no parameter, no guard library, no adapter and no schedule. No rule package is evaluated here.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P3-027 | Not specified in the source documents (DOR-RWB-P1-DM014-APP-9) | Not specified in the source documents (DOR-RWB-P1-DM014-APP-9) |

The warning is raised when a clean day is counted on a date whose ACE batch has not arrived; that date is not a clean day. The error MSG-GEN-001 is raised when a version row lacks its table code, version number, valid from date or approver. MSG-P4-002 is raised for the caller of section 10. The contract's own refusals — the 409 on a duplicate valid from date, the 409 when the approver is the author, and the 404 with MSG-P3-027 when no version is in force — are returned by rwb-case and are recorded in the cutover record as they arrive.

### 15. Screens and states

No screen is added by this story, and the legacy story states the same: "No screen in this story." The result is read on two screens that already exist: SCR-44 Interface and job monitor, for the run with its status and business date, and SCR-45 Data quality, for the reconciliation results the clean days are counted from. Both are served through the gateway-bff composite route, which is why `RWB-PLT-N001-CON` is a build dependency (DP-19). No new state, label or message is introduced on either screen.

SCR-44 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-1991).

SCR-45 states: loading as Screen Specifications v1 gives it; empty, error and no access are Not specified in the source documents (CG-ALL-1992).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-014-01 | AC1 | Component | A synthetic dump with two table codes, two versions, one row per list value, and one row carrying an ACE product column that must be dropped; the four view fixtures |
| TC-DM-014-02 | AC2 | Contract | The reference-data fake: a validated load, a misplaced hash, and a missing approver |
| TC-DM-014-03 | AC3 | End to end | Ten PASS dates, then one BREAK date; a signed cutover record; the read-back of every version in force |
| TC-DM-014-04 | Access | Component | A caller without the platform-administration right, and the same caller with it |
| TC-DM-014-05 | AC4 | Contract | The reference-data fake: the same table, valid from date and content hash posted twice |
| TC-DM-014-06 | AC5 | Contract | Not specified in the source documents (NEWAC-RWB-P1-DM014-APP-AC5) |

The two contract refusals of section 14 are exercised inside TC-DM-014-02 with the fake, and the clean-day reset is exercised inside TC-DM-014-03, so no test case is invented for them.

### 17. Guardrails

- No value a business person may change is written in code; every one is read from a versioned reference row or from a view.
- No personal data in the files, the events, the logs, the tests or the prompts. A file carries reference rows only.
- ACE data only through the four `v_ace_*` views on the `rwb_source_data` login, with SELECT only; no ACE row is copied into a file or a table.
- No read or write of another service's tables: the reference tables are reached only through the contract, and a boundary test fails the build on a cross-schema reference (DP-01).
- Every file carries the content hash and the row count it was built with, and every load id is kept in the cutover record.
- The extract is idempotent: the same table, valid from date and content hash returns the first load and writes nothing.

### 18. Traceability

| Legacy item (RWB-DM-014) | Feature | L3 process | Where it is kept | Proved by |
|---|---|---|---|---|
| Story line | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 1 | AC1 to AC3 |
| AC1 Extract the Workbench records | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 7, verbatim | TC-DM-014-01, TC-DM-014-02 |
| AC2 Reconcile the versions | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 7, with the mocked Given; the rule-row line is replaced under GAP-2179 | TC-DM-014-02 |
| AC3 Cut over | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 7, verbatim | TC-DM-014-03 |
| Data table (three entities) | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 11, verbatim | TC-DM-014-01 |
| Permission table | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 10, verbatim | TC-DM-014-04 |
| Validation table | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 14, verbatim | TC-DM-014-03, TC-DM-014-04 |
| Guardrails | Migrate reference data | Not specified in the source documents (DOR-RWB-P1-DM014-APP-2) | Section 17 | TC-DM-014-01 |

Upward: `RWB-SVC-P1`, business epic EP08, wave 4, release 30 November 2026 (tentative). Across: H `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-P1-E1001-APP`, `RWB-P1-E1069-APP`; C `RWB-P3-E1043-CON`. Downward: the owner's load and approval are in rwb-case, and the rule registry stays with rwb-decision. The owner-side Flyway load is `RWB-PLT-E1044-CON`, run in the same cutover step as this story; no story ID is created for it. Every candidate gap and assumption behind this story is in the registers under `GAP-2179` and `ASM-3521` to `ASM-3525`.

### 19. Out of scope

- Loading, verifying, approving or rolling back a version: all four acts belong to rwb-case and its admin users.
- The reference tables themselves, their indexes, their keys and their grants: owned by rwb-case (DP-07).
- The authoring, testing, four-eyes approval and effective dating of rule packages: owned by rwb-decision.
- Maintaining the ACE lists that the four views expose, and any change to the views or their grants.
- The daily reconciliation job and its report, and the freshness stamp: their own stories in this lane.
- Any screen, endpoint, event, workflow or schedule of this service.
- The retention period of the legacy tables, which is not specified in the source documents (GAP-2179; ASM-3525).
