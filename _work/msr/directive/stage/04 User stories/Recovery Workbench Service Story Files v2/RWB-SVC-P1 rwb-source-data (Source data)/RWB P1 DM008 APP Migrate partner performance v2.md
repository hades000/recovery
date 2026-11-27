# RWB-P1-DM008-APP Migrate partner performance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P1-DM008-APP-16) |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Contract version | /v1 (path version; patch version not specified in the source documents, DOR-RWB-P1-DM008-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the cutover slice of RWB-DM-008 for rwb-source-data — the extract of the panel firms, their users and the performance facts of the partner instructions, the handover to rwb-partner, the ten-day cutover evidence and the per-service Flyway version. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Status.** Draft (realignment v1). No approval of the split is recorded and this run takes no approval step, so the status is an assumption, not a portfolio decision (ASM-3497).

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **the legacy Workbench partner, partner user and partner instruction records of the open cases extracted once at cutover, handed to rwb-partner with each firm keeping its panel status, its contract end and its score, each user its role and its dates, and each instruction its case and its result, and the cutover evidenced by ten clean days and a sign-off**, so that **panel status and performance continue across cutover without a break for the firm, the user or the case the instruction belongs to**.

RWB-DM-008 keeps its place in the legacy master with epic E2, release 31 December 2026 and decision DL25. The disposition is **Split (rework)**: the rows do not stay with P1, because the Ownership Map gives `partner`, `partner_user` and `partner_instruction` to S9 rwb-partner in schema `rwb_partner` on S9's own Flyway sequence (DP-15), and `partner_user` stays with S9 rather than with P4 (ASM-0072). `recovery_case` is P3's and is read here only as the case an instruction names. This story therefore carries three things and nothing else:

- **The cutover extract.** The partner, partner user and partner instruction records of the open cases are read once from the legacy Workbench cutover dump and kept whole: the firm's `panel_status`, `contract_end` and score; the user's `identity_ref`, `role_code`, `valid_from` and `valid_to`; the instruction's `case_id`, `instruction_type`, `instructed_at`, `due_at` and result. The extract carries no settlement field and holds each case once, as the case an instruction names (AC3; BR3).
- **The handover.** The extract leaves as one package per cutover business date. The load into `rwb_partner` is S9's own cutover step on S9's own sequence: P1 holds no INSERT against another service's schema and joins nothing across the boundary (DP-01; ASM-3490).
- **The cutover evidence.** Ten clean days are counted from the `reconciliation_result` rows JOB-04 writes after the load, a break resets the count to zero, the data steward signs off in the cutover record, the legacy tables stay read-only for their retention period, and the migrated records are served from the new schema (AC3; ASM-3492).

The **per-service Flyway version (DP-15)** is the fourth artifact and is empty of schema: it creates no table, no column and no index for a partner, user or instruction row, and records the extract's definition, its field list and the read-only window in its history description. No REST operation, Kafka event, workflow, Schedule or screen is built; the cutover runs as one-off bulk work from the release pipeline and its result is read on SCR-44 through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON).

### 2. Business rationale

A panel firm is a promise of work and a promise of performance. At cutover the firm keeps the panel status the allocation rule routes on, the contract end that decides whether it may still be instructed, and the score the ranking reads; the user keeps the role and validity window that decide what the firm's people may see and until when; the instruction keeps the case it was raised on, the type, the two dates its service level is measured on and the result it came back with. A firm that loses its panel status cannot be selected, a user whose dates are lost is admitted after the contract ended or refused inside it, and an instruction whose result is dropped is a performance record the scorecard counts as never answered. The legacy story states the outcome:

> **Epic** E2, release 31 December 2026. **Module** P1 Recovery data engine. **Depends on** RWB-E1-001, RWB-E1-069. **Decision** DL25.
> **Story** As a data steward, I want the panel firms, their users and their open instructions migrated from the legacy Workbench, so that panel status and performance continue across cutover.

**Why P1 extracts and S9 loads.** Two ownership rulings meet at this boundary. The live records are S9's: Arch v5 slide 41 gives rwb-partner "panel, partner users, instructions, results, fees, scorecards", schema `rwb_partner` and wave 4, and DP-15 gives every service its own sequence in its own schema. The cutover evidence is P1's: slide 41 gives rwb-source-data "ACE view contract, extension tables, freshness, reconciliation", slide 44 puts JOB-04 Reconciliation with rwb-source-data, and `reconciliation_result` is a P1 table. DP-01 forbids the one thing that would make the load simple — a service never writes another service's tables — and the grants of slide 29 enforce that boundary. So P1 reads the dump, keeps the evidence in its own schema and hands the rows to the service that owns them; a P1 INSERT into `rwb_partner` would break the architecture test, and an S9 read of the cutover dump would break the single-reader rule of the migration keys (GAP-2172; ASM-3490).

**Why the product has no view read and therefore no freshness stamp.** DP08 "Partner performance" names the Workbench as system of record, no ACE system and no `v_ace_*` view, with the Workbench tables `partner` and `partner_instruction` and refresh ON_CHANGE (FSD P1 v3 A2.2.2; TSD P1 v3 T3.7, where DP08 is one of the seven Workbench products refreshed on change). Freshness is written from `v_ace_batch_status` for source-fed products only, so a cutover that waited for an ACE batch for DP08 would wait forever, and one that stamped a LOADED row would invent a provenance the product does not have. The recursion evidence is therefore the daily reconciliation, the only measured statement the platform makes about these rows (ASM-3493).

**Why the extract refuses two things.** AC1 carries two prohibitions that a split easily loses: no case record is duplicated, and no settlement figure is read. The first exists because the case belongs to P3 and a copied case under a partner package would be a second case row; the second because a settlement figure is a treatment fact held in the ACE plan and settlement record, and a performance extract is not the place it becomes a second source. Both are rules of section 8 and both are tested in the cutover's component tests.

### 3. Preconditions

- **The per-service Flyway contract is in place.** RWB-PLT-E1044-CON gives the sequence of `rwb_source_data` with its `V0001` baseline and the two view versions (TSD P1 v3 T3.2; DP-15). This story takes the next free version and creates nothing in it.
- **The recovery tables and the data product catalog exist.** RWB-P1-E1001-APP owns the P1 tables and the catalog rows of the 14 data products, DP08 among them with system of record "Workbench" and refresh ON_CHANGE (FSD P1 v3 A2.2.2; TSD P1 v3 T3.6). This story reads none of those rows.
- **The view contract and the login exist, although this key reads no view.** RWB-P1-E1069-APP creates the Section A views on the per-service sequence and RWB-P1-E1069-DB grants the `rwb_source_data` login SELECT on them and no privilege in `public` (TSD P1 v3 T3.3 and T6.3; Arch v5 slide 29). The reconciliation this story counts on runs through that login.
- **The reconciliation runs and writes its rows.** RWB-P1-E1011-APP owns JOB-04, its REC-01, REC-02 and REC-05 checks and the `reconciliation_result` rows. Until it lands, a reconciliation fixture stands in for those rows (section 12.8).
- **The owning services' contracts are in the registry.** The P1 admin operations the pipeline calls, the P3 case read and the S9 partner and instruction reads that answer with the migrated records. The S9 reads are mocks in the tests and add no C dependency, because the load they front is S9's own cutover step (ASM-3490; 12.2).
- **The gateway-bff composite route behind SCR-44 exists.** RWB-PLT-N001-CON is the H dependency of DP-19; the cutover result is read through that route, not stitched by a screen.
- **The cutover step has a place to run.** The release pipeline runs it as one-off bulk work against the service's own API for a business date and never reads or writes a `rwb_*` schema (Arch v5 slide 32). The pipeline step, its job name, the dump's layout and the cutover record's format: Not specified in the source documents (GAP-2171; ASM-3494).
- **The instruction slice with RWB-DM-007 is agreed.** Both keys name the same `partner_instruction` entity (DF-PRT-008 to DF-PRT-016), so the rehearsal fixes which key hands over which facts; both packages carry the instruction id (BR9; ASM-3491).
- **No build dependency blocks the start.** RWB-PLT-E1044-CON and RWB-PLT-N001-CON are platform contract stories, and RWB-P1-E1001-APP and RWB-P1-E1069-APP are in-lane APP work; the story starts after the two (Template and Rules §R5.7 rules 2, 3 and 8). The wave 4 tag is the W-MAP tag of EP08 and does not delay the build.

### 4. Flow

1. The cutover window opens and the release pipeline starts the step for one business date and one environment, as one-off bulk work against the service's own admin operations; no scheduler runs it and no operator touches a schema (Arch v5 slide 32).
2. `CutoverPartnerExtract` reads the legacy cutover dump once for the open cases only: `recovery_case` rows (DF-CAS-001 to DF-CAS-055), `partner` (DF-PRT-001 to DF-PRT-007), `partner_user` (DF-REF-212 to DF-REF-217) and `partner_instruction` (DF-PRT-008 to DF-PRT-016). One pass per business date.
3. The extract applies AC1's two prohibitions before mapping: it reads no settlement field, and it holds each case once keyed by case id, so a case named by several instructions is one case row and not a copy per instruction (BR3).
4. `PartnerCutoverMapper` maps each firm, user and instruction to its case and its business keys and keeps the facts the promise rests on. It copies values and derives none: a code stays the code the legacy record held.
5. `InstructionSliceSelector` applies the ruled split with RWB-DM-007: this package carries the panel, the partner users and the performance facts of the instructions; DM007 carries the instructions raised for legal actions. Both carry the instruction id, so S9 writes one row and updates it (BR9).
6. `PartnerHandoverPackage` assembles one row per firm, per user and per instruction, each with its case, its facts, its source tag and the cutover business date, and writes the package to the cutover record of the release pipeline — not to a table.
7. The package is handed to rwb-partner, whose own cutover step loads it into `rwb_partner` on S9's sequence (DP-15). P1 writes no row of that schema (DP-01).
8. `CutoverEvidenceReader` reads the `reconciliation_result` rows for the business dates after the load (DF-OPS-118 to DF-OPS-129) and counts clean days: a PASS row with no unexplained variance and no new REC-05 orphan on a handed-over key adds a day; a BREAK row or a new orphan resets the count to zero and names the day (AC3; ASM-3492).
9. On the tenth consecutive clean day the data steward signs off; the sign-off sits in the cutover record beside the ten day rows and the reconciliation extract they came from, and nothing is written to a schema for it (AC3).
10. The legacy tables become read-only for their retention period and the migrated records are served from `rwb_partner` through the rwb-partner contract (AC3).
11. At deploy the story's version applies on the per-service sequence, writes one `flyway_schema_history` row and creates no table, no column and no index; its description carries the extract's definition, the field list and the read-only window (DP-15). The cutover record layout, the dump interface, the clean-day rule and the DM007 slice are kept in the values file and agreed at the cutover rehearsal, not in code (GAP-2171).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The cutover dump is absent, unreadable, or read twice for the same business date | The step stops before any mapping, nothing is handed over, and the cutover record names the date and the reason | MSG-GEN-001 | AC3 |
| X2 | A firm, user or instruction row names no case or no firm that is in the same extract | The row is refused whole, the step stops and the record names the record and the missing key; no partial package leaves | MSG-GEN-001 | AC3 |
| X3 | A required value is empty on a row, such as `partner_code`, `identity_ref`, `instruction_type` or `due_at` | The row is refused whole with the field named; no default and no derived value is substituted | MSG-GEN-001 | AC3 |
| X4 | The extract holds a case twice, or carries a settlement field | The step stops before handover; the record names the case or the field and the package is rebuilt from the dump | None | AC3; BR3 |
| X5 | S9's load does not apply after the handover, or refuses an instruction id it already holds | The record stays handed-over with the clean-day count not started; P1 neither loads nor repairs the row and reports the id to S9 with the date | None | AC3; BR9 |
| X6 | JOB-04 writes a BREAK row or a new REC-05 orphan on a handed-over key inside the ten days | The count resets to zero, the day is named, the break is listed for the data steward and the sign-off stays closed | MSG-P1-012 | AC3 |
| X7 | The story's Flyway version is applied a second time | Flyway reports it already applied; no row is written twice and no version is edited in place | None | AC3 |

The message texts are the legacy ones, unchanged (section 14). X1 to X4 and X7 are component tests inside the fixture of TC-DM-008-03 and add no message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One extract reader, one mapper, one slice selector, one handover package, one evidence reader and one Flyway version; the load is S9's and is mocked |
| Negotiable | The package layout, the cutover record and the DM007 split are agreed at the cutover rehearsal; the story fixes the facts, the no-copy rules and the boundary only |
| Valuable | Every firm keeps its status, contract end and score, every user its role and dates, every instruction its case and result, and the cutover is evidenced rather than asserted |
| Estimable | One batch step, five components, one migration, four fixtures and two test cases |
| Small | Fits one sprint as the P1 slice of a split legacy key |
| Testable | AC3 runs end to end on a synthetic extract and synthetic reconciliation rows; no production and no ACE data is needed |

### 7. Acceptance criteria

```gherkin
Feature: Migrate partner performance

  Scenario: AC3 Cut over (legacy RWB-DM-008 AC3)
    Given ten clean days on the migrated records
    Given the rwb-partner contract mock returns the migrated partner, partner user and instruction served from schema "rwb_partner"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema

  Scenario: AC4 The cutover keeps its data, schema and evidence rules (new, D-RCV-60)
    Given a synthetic cutover extract and synthetic reconciliation rows
    When the extract is handed over and the clean days are counted
    Then the extract is read once from the cutover dump and lands nothing in "rwb_source_data"
    And the package carries one case row per case and no settlement field
    And each migrated record keeps its source and its migration date and never a copy of an ACE row
    And no "v_ace_*" view is read and no DP08 record carries an ACE freshness stamp
    And a PASS row with no unexplained variance and no new REC-05 orphan extends the count, and a break resets it
    And this story's version creates no table, column or index for a partner, user or instruction row
    And the package holds the panel, the users and the performance facts of the instructions, and a repeated load on the instruction id is idempotent
    And no value a business person may change is written in code, and no personal data appears in the extract, a log, a fixture or a prompt

  Scenario: AC5 A status change the model does not allow is refused (new, D-RCV-60)
    Given Not specified in the source documents (NEWAC-RWB-P1-DM008-APP-AC5)
    When a status change the model does not allow is attempted
    Then the status change is refused
```

AC3 is copied character for character. The added Given is the rwb-partner contract answer this story builds against, because the load into `rwb_partner` is S9's own cutover step (ASM-3490); it changes no legacy value in the When or Then lines. AC1 Extract the Workbench records and AC2 Reconcile the business keys are owned by RWB-ITG-DM008-ITG, which carries the REC-05 proof across the services; the extract, the mapper and the handover of this story are proved by the end-to-end fixture of TC-DM-008-03 and by the rules of section 8 (ASM-3496).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `partner`, `partner_user` and `partner_instruction` are S9's in `rwb_partner`; P1 extracts and hands over and never loads another service's schema | Ownership Map; ASM-0072; DP-01; Arch v5 slide 41 |
| BR2 | The extract is read once from the cutover dump and lands nothing in `rwb_source_data`, which holds no partner, user or instruction table | Legacy RWB-DM-008 AC1; TSD P1 v3 T3.6; GAP-2172 |
| BR3 | No case record is duplicated and no settlement figure is read; the package carries one case row per case and no settlement field | Legacy RWB-DM-008 AC1 |
| BR4 | A migrated record keeps its source and its migration date and never a copy of an ACE row | Legacy RWB-DM-008 guardrails; D-RCV-35 (U1) |
| BR5 | DP08 is a Workbench product with no ACE view and refresh ON_CHANGE, so its records carry no ACE freshness stamp and this key reads no `v_ace_*` view | FSD P1 v3 A2.2.2; TSD P1 v3 T3.7; DP-05; ASM-3493 |
| BR6 | Ten clean days are counted from the `reconciliation_result` rows of JOB-04: a PASS row with no unexplained variance and no new REC-05 orphan extends the count, a break resets it | Legacy RWB-DM-008 AC3; FSD P1 v3 A2.11 and A2.13; DL25; ASM-3492 |
| BR7 | The sign-off is held in the release pipeline's cutover record, the legacy tables stay read-only for their retention period, and the migrated records are served from the new schema | Legacy RWB-DM-008 AC3; ASM-3494 |
| BR8 | The service runs its own Flyway sequence in its own schema; this story's version creates no table, no column and no index for a partner, user or instruction row | DP-15; ADR-021; TSD P1 v3 T3.2 |
| BR9 | This story hands over the panel, the users and the performance facts of the instructions; RWB-DM-007 hands over the instructions raised for legal actions; S9 loads both idempotently on the instruction id | GAP-2171; ASM-3491 |
| BR10 | No value a business person may change is written in code, and no personal data appears in an extract, a log, a fixture or a prompt | Legacy RWB-DM-008 guardrails; FSD P1 v3 BR-P1-011; Template and Rules §R7.2 s17 |

In the target BR1 and BR2 are proved by the schema of `rwb_source_data` and the absence of a write to `rwb_partner`; BR3 by the extract's field list and the case key; BR4 on the handover row; BR5 by the absence of a view read in the code; BR6 and BR7 by the cutover evidence; BR8 by the migration; BR9 by the package content and the idempotent load; BR10 by the review rule for the cutover code and its fixtures.

### 9. State transitions

None for the case: this story changes no case status, stage, task or partner record. The moves are the cutover's own, and they are six.

| From | Event | Condition | To |
|---|---|---|---|
| Cutover not started | The step is started for the business date | The dump is readable and every open case is in it | Extract ready: rows mapped, each instruction's case resolved |
| Extract ready | The handover package is assembled | Every firm, user and instruction carries its case, its facts and its firm key | Handed over: the package is in the cutover record and with rwb-partner |
| Handed over | S9's cutover step applies its Flyway version | S9's sequence is at the version that creates `rwb_partner` | Loaded: the records answer from `rwb_partner` through the S9 contract |
| Loaded | JOB-04 writes its PASS rows for the business date | No unexplained variance and no new REC-05 orphan on the day | Ten clean days running, count at the number of consecutive clean days |
| Ten clean days running | A BREAK row or a new REC-05 orphan appears | The break is listed for the data steward | Ten clean days running, count at zero |
| Ten clean days running | The tenth clean day is reached and the data steward signs off | The sign-off is recorded in the cutover record | Signed off: legacy tables read-only for their retention period, records served from the new schema |

The cutover record is the ledger of each move and the Flyway history row is the schema's own record of the deploy. No event announces a move: `InstructionIssued` and `PartnerResultSubmitted` on `rwb.partner.events.v1` are S9's, and a migration raises neither.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the cutover for a business date, owns the ten-day evidence and records the sign-off (FSD P1 v3 A2.11) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right R of the legacy permission check and may read the cutover record and the evidence for their scope |
| RW-TRIBE, squad member | Builds the extract, the mapper, the slice selector, the package and the evidence reader, and applies the version |
| RW-AUDIT, RW-COMPLY | Read the cutover record, the ten day rows and the sign-off as evidence; they take no cutover decision |
| The `rwb_source_data` service identity | Reads the reconciliation rows and writes no row except the Flyway history row of its own version |
| S9 rwb-partner and its identity | Owns `rwb_partner`, its sequence and the load of the rows handed over; this story takes no right over them |

The role codes are rows of rwb-access and the step authorises through the guard of the published admin operation; this story adds no role and no grant. No delegation-of-authority level applies: the migration approves no instruction and settles no case, because the panel status and the result are copied facts and not decisions.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | The case each instruction names | Read from the dump and handed over once per case; P3 owns the table and this story writes no row of it |
| DF-PRT-001 to DF-PRT-007 | `partner` | `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, the score and one field the legacy row does not name | Extracted and handed over; not written here, because `rwb_partner` is S9's |
| DF-REF-212 to DF-REF-217 | `partner_user` | `identity_ref`, `partner_id`, `role_code`, `valid_from`, `valid_to` | Extracted and handed over; not written here; the users stay with S9 (ASM-0072) |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, the result and two unnamed fields | Extracted and handed over, performance facts only; the legal-action instructions are DM007's (BR9) |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | `rec_code`, `business_date`, `product_group` and the other fields of a reconciliation row | Read for the clean-day count; written by JOB-04 and never by this story |
| None (framework table, outside Logical Data Model v9 and Data Classification v5) | `flyway_schema_history` | Version, description and checksum of this story's version | Write, one row, at deploy only |

Field IDs are those of Logical Data Model and Data Dictionary v9 and of the legacy data row. `rwb_source_data` holds no `partner`, `partner_user` or `partner_instruction` object and this version creates none. The extract is a file read once and a package handed over, not a table; its layout, field order and record format are Not specified in the source documents (GAP-2171; ASM-3494).

The legacy data row names six of the seven partner fields, five of the six user fields and six of the nine instruction fields, and AC1 supplies the score and the result; the DP08 catalog row names `partner` and `partner_instruction` only and does not carry `partner_user` at all (FSD P1 v3 A2.2.2; GAP-2172). The story therefore carries the three ranges whole and fixes no name of its own. The `source` and `migrated_at` columns of the partner tables are S9's to write on the load (BR4).

### 12. Contract

**12.1 REST operations provided**

None. The cutover is one-off bulk work started by the release pipeline, not a public operation: this story adds no path, no parameter and no response field. The admin and reconciliation operations it calls belong to other RWB-SVC-P1 stories and are named in 12.2.

**12.2 REST operations consumed**

None by this story's own code. The pipeline drives the step and the tests read the other services as mocks:

| Caller | Operation | Owner | Why it is not a dependency |
|---|---|---|---|
| The release pipeline | `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` (API-P1-002) | P1 rwb-source-data | Same service: an in-lane operation of the job story |
| The release pipeline | `GET /api/recovery/source-data/v1/admin/data-quality/exceptions` | P1 rwb-source-data | Same service: the breaks that reset the count are read from it |
| The tests | `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Mock only; the case travels as the dump holds it |
| The tests | `GET /api/recovery/partner/v1/partners/{partnerId}` | S9 rwb-partner | Mock only; the load into `rwb_partner` is S9's (ASM-3490) |

The story therefore holds no C and no I dependency. DP-11 is not a pattern of this story: there is no outbound call to build against and no timeout of its own.

**12.3 Events published**

None. The cutover publishes no Kafka event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`. `AceDataReady` (EV-26, consumed) and `AceDataLate` (EV-27, published) belong to the freshness stories; `InstructionIssued` and `PartnerResultSubmitted` are S9's.

**12.4 Events consumed**

None. The pipeline starts the step for a business date; the story reads no topic and no inbox row, and it reads the `reconciliation_result` rows from the table rather than from an event.

**12.5 Workflows and activities**

None added. JOB-04 Reconciliation is a workflow of this service, exercised here through its rows and not changed. The cutover itself is a batch job of the release pipeline and not a Temporal workflow, because it runs once per cutover date and neither on a schedule nor on an event.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits in this story: the cutover is one-off bulk work, and the count reads rows JOB-04 already writes on the `AceDataReady` trigger (Arch v5 slides 32 and 44).

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read for the clean-day count; written by JOB-04, not by this code |
| `partner` | `rwb_partner` | S9 | Not written here: the load is S9's own cutover step (DP-01) |
| `partner_user` | `rwb_partner` | S9 | Not written here: the users stay with S9 (ASM-0072) |
| `partner_instruction` | `rwb_partner` | S9 | Not written here: S9 loads the rows of this key and of DM007 on the instruction id |

No statement of this story names another service's schema or a table in `public` (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | Synthetic partner, partner user and partner instruction rows of two open cases, with case keys and source tags | AC3, from Day 1, with no legacy data |
| rwb-partner contract mock | The migrated partner, partner user and instruction served from `rwb_partner` | AC3 and its added Given |
| rwb-case contract mock | The case an instruction names, with its `case_no` | AC3, for the case key of the package |
| Reconciliation extract fixture | `reconciliation_result` rows of JOB-04: PASS, BREAK and one REC-05 orphan on a migrated key | AC3 and the reset path of X6 |

No view fixture is listed, deliberately: this key reads no `v_ace_*` view, so a view fixture would fake a call the story does not make. The fixture layouts, the dump's file name and the record format are Not specified in the source documents (GAP-2171; ASM-3494).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 0 from this code | The step is started and read through this service's own admin operations, one hop, 2 s |
| Kafka | None | None | No event published or consumed; the partner events are S9's |
| Temporal | None | None | No workflow, activity or schedule added; JOB-04 is exercised, not changed |
| File | None | One | The extract is read once from the cutover dump; the package leaves through the cutover record |

### 13. Solution plan

Package `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, under the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1`, queue `rwb-source-data`; the topic and the queue are named for completeness and this story uses neither.

| Component | Type | Responsibility |
|---|---|---|
| CutoverPartnerExtract | Batch job | The one-off read of the cutover dump for the open cases; one pass per business date, no table, no re-read, no settlement field, one row per case |
| PartnerCutoverMapper | Service | Maps each firm, user and instruction to its case and firm keys and keeps the facts whole: status, contract end and score; role and dates; case, type, dates and result; derives and defaults nothing |
| InstructionSliceSelector | Service | Applies the split with RWB-DM-007: this package carries the panel, the users and the performance facts; the legal-action instructions are DM007's; both carry the instruction id |
| PartnerHandoverPackage | Service | Assembles one row per firm, user and instruction with its case, facts, source tag and business date, and writes the package to the cutover record |
| CutoverEvidenceReader | Service | Counts clean days from the `reconciliation_result` rows, resets on a break or a new REC-05 orphan, and holds the ten day rows beside the sign-off |
| Flyway version, next free on the sequence | Migration | Creates no table, column or index for a partner row; records the extract's definition, field list and read-only window in its description |
| Cutover fixtures | Test fixture | Legacy extract, rwb-partner and rwb-case mocks, reconciliation rows; all synthetic |

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data through rwb-source-data's contract or the service's own views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in boundary form only, and this is where the story says so plainly. The pattern gives a service two lawful ways to reach ACE data — this service's contract or its own `v_ace_*` views — and this key takes neither, because DP08 has no ACE source view (FSD P1 v3 A2.2.2; TSD P1 v3 T3.7). The extract reads the legacy dump, the package carries the keys as the dump holds them, and the ACE-side resolution of `identity_ref` and `account_key` is the REC-05 leg that RWB-P1-E1011-APP owns. What the pattern fixes here is the boundary it forbids: S9 reads no view and this story writes no row in S9's schema (BR1). DP-15 gives the sequence and the history row; DP-19 puts the cutover result behind the composite route of SCR-44. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard of its own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no rule evaluation (DP-04).

- **Migrations.** The story reads the reconciliation rows and writes no row at run time; the only write is the Flyway history row of its own version. The version creates no table, column, index or constraint, because the partner rows are S9's and `rwb_source_data` stores none of them (BR1, BR2, BR8). The 13 P1 Workbench tables of TSD P1 v3 T3.6 are the service's own and none of them is a partner table; no fourteenth is added. No grant is made or changed: the login and its SELECT belong to RWB-P1-E1069-DB. The version number is the next free one after `V0001` and the two view versions of TSD P1 v3 T3.2; the story fixes no number.
- **Configuration.** No parameter and no reference list is read: DP-06 and DP-07 are not in the pattern set. The ten-day target, the business date and the retention period are data of the cutover record, never constants in code. The feature switch is `rwb.source-data.dm008-cutover-extract` from the platform flag library: off, the step refuses to start and no package leaves, while the migration still applies because it creates nothing (ASM-3495). The handover point and the cutover record format: Not specified in the source documents (GAP-2171; ASM-3494). Reference-data contract: Not specified in the source documents (DOR-RWB-P1-DM008-APP-20).
- **Build steps.** (1) The extract over the fixture, with the absent-dump and double-read cases, X1. (2) The two AC1 prohibitions over a fixture with a case named by two instructions and a planted settlement field, X4. (3) The mapper, with the firm's three facts, the user's role and dates and the instruction's case, type, dates and result, X2 and X3. (4) The slice selector over a fixture where one instruction id appears in both slices, proving one row per id. (5) The evidence reader: ten PASS rows count up, one BREAK or one new orphan resets, the sign-off is refused below ten, AC3 and X6. (6) The migration as a no-op on the schema with the definition, field list and read-only window in its description, plus the repeated-apply check X7; then the refusal path through the guard of the admin operation, TC-DM-008-04, and a mock run of the whole cutover so the story builds before S9's load and before JOB-04's real rows are live.
- **Done when.** The tests of section 16 pass, `rwb_source_data` holds no partner, user or instruction table, the package carries every firm, user and instruction with its case and its facts, no settlement field and no second case row, AC3 counts ten clean days from `reconciliation_result` rows and records the sign-off, and no class names a `public` table or another service's schema.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-GEN-001 | Error | The extract lacks a required field or record, such as a case, a firm key, a user identity or an instruction type | Enter {field}. |
| MSG-P4-002 | Error | A caller without the Platform administration right starts the cutover | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | Warning | A source product behind the reconciliation is late for the date, so the day cannot count as clean | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | A reconciliation row for the date is BREAK inside the ten days, so the count resets | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |

The four messages are copied character for character from the legacy master (legacy RWB-DM-008 validation table; FSD P1 v3 VR-P1-011-1 and VR-P1-013-1). This story raises MSG-GEN-001 and MSG-P4-002 itself: `{field}` is the field or record the extract lacks, and `{action}` is "run the partner cutover extract", never a case fact. MSG-P1-001 and MSG-P1-012 are raised by the reconciliation and the freshness read and are asserted here as evidence; DP08 has no ACE batch, so MSG-P1-001 is asserted on the source product the day depends on and never as a DP08 stamp (BR5).

### 15. Screens and states

No screen in this story. The cutover starts and its result is read on SCR-44 Interface and job monitor, which shows Workbench jobs and outbound actions with status and reruns, and the breaks that reset the count appear on SCR-45 Data quality (FSD P1 v3 Screens). Both are read through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON); this story adds no route, no field and no rendering, and the route's path and merge order are Not specified in the source documents (GAP-2171; ASM-3494).

| State | What the cutover record holds | What the monitor shows |
|---|---|---|
| Extract ready, handed over, loaded | The business date, the counts, the package identifier and the case of each instruction | The step running, then complete for the handover, then the rows answering from the new schema |
| Ten clean days running | The count of consecutive clean days and its last clean day | The count, its date and the days remaining |
| Break | The BREAK row or orphan, its date, code and owner role, with the count at zero | The break listed and the count reset; the sign-off closed |
| Signed off | The ten day rows, the reconciliation extract and the sign-off, with the read-only window | The cutover complete and the legacy tables read-only |
| SCR-44 Empty | Not specified in the source documents (CG-ALL-1945) | Not specified in the source documents (CG-ALL-1945) |
| SCR-44 Loading | Not specified in the source documents (CG-ALL-1945) | Not specified in the source documents (CG-ALL-1945) |
| SCR-44 Error | Not specified in the source documents (CG-ALL-1945) | Not specified in the source documents (CG-ALL-1945) |
| SCR-44 No access | Access is Platform administration, checked on every request (Screen Specifications v1 SCR-44) | MSG-P4-002: You cannot {action} here. Your role does not include it. |
| SCR-45 Empty | Not specified in the source documents (CG-ALL-1946) | Not specified in the source documents (CG-ALL-1946) |
| SCR-45 Loading | Screen Specifications v1 SCR-45 loading state | Screen Specifications v1 SCR-45 loading state |
| SCR-45 Error | Not specified in the source documents (CG-ALL-1946) | Not specified in the source documents (CG-ALL-1946) |
| SCR-45 No access | Access is Platform administration, checked on every request (Screen Specifications v1 SCR-45) | MSG-P4-002: You cannot {action} here. Your role does not include it. |

A cutover below ten clean days shows as a count and not as a pass, so a run with one break is visible as a reset rather than as a zero (AC3).

The break list carries, for each break, the firm, the key type, the key value, the reason and the two owners. The extract is retained with the wave record, and the wave gate is one binary pass or fail. The SIT environment and its base hosts are Not specified in the source documents (GAP-0448).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-008-03 | AC3; BR1 to BR10; the component paths of X1 to X5 and X7 | End to end | A synthetic cutover extract with two open cases, two firms, three users and four instructions, one instruction shared with the DM007 slice and one settlement field planted in a source row; the rwb-partner and rwb-case mocks; ten PASS reconciliation rows after the load, then one BREAK and one REC-05 orphan, then ten clean rows again; the sign-off recorded once at ten; a row count of every `rwb_source_data` table before and after |
| TC-DM-008-04 | Access: the MSG-P4-002 refusal path of section 5 | Component | A caller whose Platform administration right R is absent in the authorise fake, then a second call with the right present |
| TC-DM-008-05 | AC5 | Not specified in the source documents (NEWAC-RWB-P1-DM008-APP-AC5) | Not specified in the source documents (NEWAC-RWB-P1-DM008-APP-AC5) |
| TC-DM-008-06 | AC4; BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10 | Component | A synthetic cutover extract with one settlement field planted in a source row; synthetic PASS, BREAK and REC-05 orphan reconciliation rows; a repeated load on the same instruction id against the rwb-partner mock; a row count of every `rwb_source_data` table before and after |

The legacy numbers are kept. TC-DM-008-01 and TC-DM-008-02, the extract and reconcile tests of the legacy key, sit with the AC1 and AC2 copies on RWB-ITG-DM008-ITG as TC-DM-008-01-ITG and TC-DM-008-02-ITG and are not repeated here; TC-DM-008-03-ITG and TC-DM-008-04-ITG are their integration copies. The full Given, When and Then is recorded in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the firm's status and dates, the users' roles and dates and the instruction types and results are data on the cutover row, and the ten-day target and retention period are data of the cutover record.
- No personal data in the extract, logs, fixtures or prompts: `identity_ref` is a reference and not a person record, and every fixture is synthetic.
- ACE data only through the owner's contract or `v_ace_*` views, and this key reads neither: no statement names a view, a `public` table or another service's schema (BR5).
- No copy of an ACE row: the package carries the keys as the dump holds them (BR4).
- No cross-schema write: the load into `rwb_partner` is S9's own step on S9's own sequence (BR1, DP-01).
- No duplicated case and no settlement figure: one case row per case and no settlement field from any source (BR3).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).
- A cutover is never declared on a reset count: a break sets the count to zero and the sign-off stays closed (BR6, BR7).

### 18. Traceability

| Legacy key | Feature | L3 process |
|---|---|---|
| RWB-DM-008 | None; no feature grouping is used | All recovery processes |

| Legacy RWB-DM-008 row | Value (verbatim) | Where it lands |
|---|---|---|
| Epic | E2, release 31 December 2026 | Metadata release and wave; section 2 quotation |
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 |
| Feature | None | No feature grouping is used |
| Process | All recovery processes | The cutover covers the partner records of every process the key names |
| Priority | Must | Sections 1, 2 and 19 |
| Depends on | RWB-E1-001, RWB-E1-069 | Rebased by D-RCV-60 onto RWB-P1-E1001-APP and RWB-P1-E1069-APP, with RWB-PLT-E1044-CON and RWB-PLT-N001-CON |
| Decision | DL25 | BR6; the ten clean days as cutover evidence; still open, assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602 |
| Story | As a data steward, I want the panel firms, their users and their open instructions migrated from the legacy Workbench, so that panel status and performance continue across cutover. | Section 1 statement; section 2 quotation; BR1, BR3 and BR9 |
| Data | recovery_case DF-CAS-001 to DF-CAS-055; partner DF-PRT-001 to DF-PRT-007; partner_user DF-REF-212 to DF-REF-217; partner_instruction DF-PRT-008 to DF-PRT-016 | Section 11; the handover of section 4 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | 12.1 and 12.2: no operation provided, none consumed by this code |
| Screen and states | SCR-45 Data quality: Loading; breaks | Section 15, with the result read on SCR-44 |
| Permission checks | Platform administration, R, RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10; TC-DM-008-04 |
| Validation and messages | MSG-P1-001, MSG-P1-012, MSG-GEN-001, MSG-P4-002 | Section 14 |
| Test cases | TC-DM-008-01 to TC-DM-008-04 | Section 16; 01 and 02 sit on RWB-ITG-DM008-ITG |
| Guardrails | No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR4, BR5, BR10; section 17 |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | Boundary form only: this key reads no view, S9 reads none, and the key resolution is the reconciliation's (section 13) |
| DP-15 | Template and Rules §R5.5 | The version on the per-service sequence with the history row that records the cutover definition |
| DP-19 | Template and Rules §R5.5 | The cutover result is read through the composite route behind SCR-44, not stitched by a screen |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route behind SCR-44 |
| RWB-P1-E1001-APP, RWB-P1-E1069-APP | App development | H: the recovery tables and the views with the login, which this code does not read |
| RWB-P1-E1011-APP | App development | Writes the `reconciliation_result` rows the clean-day count reads |
| RWB-P1-DM007-APP | App development | The legal-events slice of the same cutover, on the same instruction id |
| RWB-ITG-DM008-ITG | Integration | Owns the AC1 and AC2 proof across the services and the ITG copies of the test cases |

External dependencies: None. The story adds no X row of its own.

### 19. Out of scope

- The load into `rwb_partner`, S9's Flyway sequence and every table of S9: S9 rwb-partner's; this story hands the rows over and stops (DP-01, DP-15).
- The AC1 extract proof and the AC2 reconciliation with the REC-05 orphan list across the services: RWB-ITG-DM008-ITG, with the ITG copies of the test cases (ASM-3496).
- The instructions raised for legal actions and the legal events package they travel in: RWB-P1-DM007-APP, on the same instruction id (BR9).
- The partner portal, its FAPI 2.0 path through the partner gateway, the instruction workflow with its service level timers, the fees and the scorecards: S9 rwb-partner.
- JOB-04, its REC-01, REC-02 and REC-05 checks and the `reconciliation_result` rows: RWB-P1-E1011-APP.
- The SCR-45 console and its break list: RWB-P3-AD019-APP; the reconciliation console read of this service: RWB-P1-AD019-APP.
- The views, the per-service login and its grants: RWB-P1-E1069-APP and RWB-P1-E1069-DB; the catalog rows and DP08's definition: RWB-P1-E1001-APP; the retention rule: RWB-P1-E1017-APP.
- The platform configuration of Kafka, Temporal and the gateway: the platform epics. Any REST operation, Kafka event, Temporal workflow, Schedule or screen of its own: this story builds none and section 12 says so table by table.
