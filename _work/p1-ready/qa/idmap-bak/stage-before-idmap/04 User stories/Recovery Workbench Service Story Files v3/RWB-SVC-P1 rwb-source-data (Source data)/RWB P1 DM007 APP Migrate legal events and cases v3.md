# RWB-P1-DM007-APP Migrate legal events and cases

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (27 November 2026, D-RCV-60 P1 developer readiness, RD-P1 register)

- RD-P1-027: the legal action package carries DF-LEG-001 to DF-LEG-004 and DF-LEG-014 only; DF-LEG-006 to DF-LEG-013 and the WIN notice facts are read, never carried (DF-LEG-005 is a key from batch D); AC5 and sections 4 and 11 are aligned; `person_key` travels as a linking key with stated handling (findings #2, #3).
- RD-P1-021, RD-P1-012, RD-P1-040 and RD-P1-042: no job rerun, no workflow dependency by event, clean day under `recon.tolerance.pct` version 1 = 0.00; the `recovery` 92-table fixture is removed (findings #1, #10).
- One feature flag key (GAP-0534); AC8 to AC10 rewritten to testable behaviour and AC11 to AC13 added (findings #4, #5, #7, #8).
- Still pending: package layout (NEW-GAP-S12-4), confirmation of MSG-P1-023, the flag owner and the delivery steps in section 20 (findings #4, #6, #9).
- Batch D and the finishing pass: `lawsuit_no` (DF-LEG-005) is the KEY that links a migrated legal action to `v_ace_lawsuit`, DF-LEG-006 to DF-LEG-013 stay ACE_READ (RD-P1-068; closes NEW-GAP-S12-6); each owner loads under its own workload identity (RD-P1-068); a refused sign-off answers MSG-P1-023 (RD-P1-042); the flag removal condition and off/on test are stated (AC14); test case IDs of Test Cases v9 cited.

| Item | Value |
|---|---|
| Story key | RWB-P1-DM007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Size | Not specified in the source documents (DOR-RWB-P1-DM007-APP-16) |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP (RWB-P1-E1001-APP and RWB-P1-E1069-APP not Done at 26 November 2026) |
| Contract dependencies | RWB-PLT-E1044-CON, RWB-PLT-N001-CON (not Done at 26 November 2026; no contract story of this legacy key) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) for the reconciliation results and the DP07 record read; rwb-litigation.yaml, rwb-comms.yaml and rwb-partner.yaml of the same folder for the owner mocks |
| Readiness decisions | RD-P1-001; RD-P1-004; RD-P1-005; RD-P1-012; RD-P1-021; RD-P1-027; RD-P1-040; RD-P1-042; RD-P1-043; RD-P1-045; RD-P1-068 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-DM007-APP-14) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P1-DM007-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-DM-007 is split, and this is the P1 cut-over slice — the single read of the legal action, notice and law firm instruction records of the open cases at cut-over, the handover of one package per owner to S4 rwb-litigation, P6 rwb-comms and S9 rwb-partner, the ten clean days counted from the service's own reconciliation rows, the steward's sign-off, the legacy read-only window, and DP07 served from the new schemas with the court record read from ACE and never copied. The extract rule and the business-key reconciliation of the key sit with RWB-ITG-DM007-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 6 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story
As a **data steward and data product owner (RW-DATASTEW) who signs off the legal cut-over, a squad member (RW-TRIBE) who builds and runs it, and the `rwb-source-data` service that owns the cut-over evidence and the DP07 read path**, I want **the cut-over step of RWB-DM-007: one read of the legal action, notice and law firm instruction records of the open cases at cut-over, one handover package per owner for the cut-over business date, the ten clean days counted from the reconciliation rows this service already writes, the steward's sign-off recorded once, the legacy tables held read-only for their retention period and the migrated records served from the new schemas**, so that **litigation continues at cut-over while the court case and the hearing record are read from ACE and never copied, and no service reads or writes another service's tables to make that happen**.

RWB-DM-007 keeps its place in the legacy master with its epic E2, its release 31 December 2026, its priority Must and its decision DL25. What the realignment changes is where the rows live and who moves them: the Ownership Map gives `legal_action` to S4 in `rwb_litigation`, `notice` to P6 in `rwb_comms` and `partner_instruction` to S9 in `rwb_partner`, each with its own login and its own Flyway sequence (DP-15), and DP-01 forbids the cross-schema write the monolith could make. This story therefore carries three things and no fourth:

- **The one read and the three packages.** The legal action, notice and instruction records of the open cases are read once from the cut-over dump, keep the Workbench-held fields of section 11 whole, and leave as one package per owner per business date; the package fields are section 11; its file layout and location are fixed at the cut-over rehearsal (GAP-2170; ASM-3484; NEW-GAP-S12-4).
- **The evidence.** Ten clean days are counted from the `reconciliation_result` rows JOB-04 writes for the migrated records (ASM-0743), and the sign-off, the ten day rows and the read-only window sit in the cut-over record of the release pipeline (ASM-3485), run as one-off bulk work and never by a scheduler.
- **The read path.** `legal_action`, `notice`, `partner_instruction`, `lawsuit` and `hearing` are no objects of `rwb_source_data`: the records are served from the three owners' schemas through their contracts, and DP07 is answered by the product's own record read with its freshness stamp (DP-05).

AC1 Extract the Workbench records and AC2 Reconcile the business keys of the legacy key belong to RWB-ITG-DM007-ITG, which carries them and their test cases as the `-ITG` copies; this story claims AC3 and writes neither of the other two (ASM-3487). Bases and names: REST base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-13, DP-14).

### 2. Business rationale
DP07 Legal events and cases is the product of the court record and of the Workbench's own legal facts: the suite in LIT and the notices of WIN are read through `v_ace_lawsuit`, `v_ace_hearing` and `v_ace_pod`, and the Workbench keeps the legal action it raised, the notice it already sent and the instruction it gave a panel firm, refreshed daily and expected by 08:00 (FSD P1 v3 A2.2.2). At cut-over the open cases must keep the action, the notice and the instruction that carry a court date, a sent date and a due date, because a litigation that restarts from a blank record loses the very dates a court and a firm work to.
The court date, the court and claim facts and the sent date are LIT and WIN facts: they are not carried in a package and are read from ACE through the views; the packages carry the Workbench-held fields of section 11 only (RD-P1-027).

Legacy RWB-DM-007 moved all three in one cutover step in the single `recovery` schema. Under D-RCV-60 the rows sit in three schemas and belong to three services, so the cut-over becomes a handover and its evidence has to be provable instead of asserted. This story answers with what the service already owns: the reconciliation rows of JOB-04 for the migrated records, the steward's sign-off, the read-only window on the legacy tables and the new read path — the four things AC3 names, with no new table and no new business value. It changes no private fact of a legal action, no value of section 11 and no message text of section 14; it changes the boundary, so that this service extracts and hands over and holds no INSERT against another schema, copies no court record and counts its clean days from data rather than from a checklist (BR1, BR3, BR5). A break resetting the count is stricter than a sign-off on a promise, and it is what the steward signs (ASM-0743).

### 3. Preconditions
- RWB-P1-E1001-APP is in place: `reconciliation_result`, `data_product`, `data_product_load` and the dictionary exist in `rwb_source_data`, with the DP07 catalog row (DP-15 baseline; H). The three owners' target tables carry `migration_source varchar(20)` and `migrated_at timestamptz`, added by each owner in its own Flyway step (RD-P1-027); Pending: the values of LOV-MIGRATION-SOURCE, owner data owner (NEW-GAP-B4).
- RWB-P1-E1069-APP is in place: the 30 read-only `recovery.v_ace_*` views with their grants to `rwb_source_data` only, `v_ace_lawsuit` (view 22) and `v_ace_hearing` (view 23) among them, the Section B views behind RWB-ACE-001 and DL43 (DP-05; H).
- RWB-PLT-E1044-CON gives the per-service Flyway sequence, so this story's version migrates in `rwb_source_data` and nowhere else (DP-15; H).
- RWB-PLT-N001-CON gives the gateway-bff composite route for SCR-45 and the DP07 record read (DP-19; H).
- JOB-04 is live and writes one `reconciliation_result` row set per business date, `REC-01`, `REC-02` and `REC-05` among the checks, as ReconciliationWorkflow, a child of AceIngestCheck (RWB-P1-E1011-APP; FSD P1 v3 A2.11; ASM-0743).
- The three owners' cut-over migrations exist or are mocked: S4's `rwb_litigation`, P6's `rwb_comms` and S9's `rwb_partner`, each on its own sequence. They are no build dependency of this story, which writes none of their rows; AC1 is proved against their contract mocks (ASM-3483).
- The legacy cut-over dump of the open cases is available for the cut-over business date, with the record sets of section 11; its name, its layout and the identity that may read it are Not specified in the source documents (GAP-2170; ASM-3484).
- The retention period of the legacy tables is read from the retention rule in force (RWB-P1-E1017-APP) and is never a constant of this story; the grant change that makes the tables read-only is executed by the ACE team on the legacy schema, and this service proves the refusal (GAP-2170; ASM-3486).
- Status is Draft (realignment v1) because no approval of the realigned story is recorded, and 31 December 2026 is copied unchanged and marked tentative (ASM-0747).

### 4. Flow
1. The cut-over window opens and the release pipeline starts the cut-over step for one business date and one environment as one-off bulk work, a pipeline command under one Idempotency-Key (a UUID). No Temporal Schedule runs it and no operator touches a schema (Arch v5 slide 32; ASM-3485). The feature switch `rwb.source-data.dm007-cutover-extract` defaults off when the release pipeline first runs the step (GAP-0534).
2. `CutoverLegalReader` reads the dump once for the open cases at cut-over and only those: the `recovery_case` rows, the `legal_action` rows, the `notice` rows and the `partner_instruction` rows (`DF-PRT-008` to `DF-PRT-016`); a second read inside the same business date is refused. The package carries only the CARRY and KEY fields of section 11 (RD-P1-027; GAP-0532).
3. `LegalRecordMapper` keeps every CARRY and KEY field whole and derives none: the legal action keeps its `id`, case, law firm, action type, `status` and `lawsuit_no` (DF-LEG-005, the linking key to `v_ace_lawsuit`); the notice its `id`, case, document, type, template, hold reason, dispatch file, dispatch attempts and `person_key`; the instruction its id, firm, type, `instructed_at` and `due_at`. The court facts of LIT (DF-LEG-006 to DF-LEG-013) and the delivery facts of WIN (DF-LEG-019 to DF-LEG-023) are not carried (RD-P1-027).
4. `LegalHandoverPackages` assembles one package per owner — legal action for rwb-litigation, notice for rwb-comms, instruction for rwb-partner — each row carrying its case, its section 11 fields and `migration_source`, with row count and checksum per package, and writes them to the cut-over record of the release pipeline and not to a table (ASM-3484). The package layout is agreed at the cut-over rehearsal (GAP-0532).
5. The packages are handed over and S4, P6 and S9 each load their own rows on their own Flyway sequences; this service writes no row of those schemas and joins nothing across the boundary (BR1; DP-01, DP-15).
6. `CutoverEvidenceReader` reads the `reconciliation_result` rows of the business dates after the load (`DF-OPS-118` to `DF-OPS-129`): a business date on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears moves the count up one day, and a BREAK row or a new orphan resets it to zero and names the day (BR5; ASM-0743).
7. On the tenth consecutive clean day the data steward signs off, once and idempotent on its key, beside the ten day rows and the extract they came from; a sign-off before ten is refused (BR6; ASM-3485).
8. The legacy tables are held read-only for their retention period and the records are served from the new schemas — a legal action from `rwb_litigation`, a notice from `rwb_comms`, an instruction from `rwb_partner`, each through its owner's contract — and DP07's own record read answers with the product's freshness stamp (BR6, BR7).
9. At deploy this story's version applies on `rwb_source_data`'s own sequence, writes one `flyway_schema_history` row and creates no table, column or index for a legal record; its description carries the extract's definition, the field list and the read-only window (BR8; DP-15).
10. A new run of the pipeline step for the same business date after a failure produces the same packages and the same count and duplicates nothing (AC7); the cut-over record is the ledger of every move. The shape of the dump, the cut-over record and the DM007 instruction slice is agreed at the cut-over rehearsal and recorded in the runbook entry of the release pipeline (GAP-2171).

### 5. Exception paths
| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The dump is absent, unreadable, or read a second time for the same business date | The step stops before any mapping; nothing is handed over and the cut-over record names the business date and the reason | MSG-GEN-001 | AC7 |
| X2 | A legal action, notice or instruction row carries no case, or its case is not in the extract | The row is refused whole, the step stops and the cut-over record names the record and the missing case; no partial package leaves | MSG-GEN-001 | AC7 |
| X3 | A required key is empty, such as `action_type`, `notice_type`, `instructed_at` or `due_at` | The row is refused whole with the field named; no default and no derived value is substituted | MSG-GEN-001 | AC7 |
| X4 | The legal action's court record is not in `v_ace_lawsuit` | The action is handed over with its section 11 fields only, `lawsuit_no` among them; the step reads no court view; the DP07 read answers the action with no court fact and nothing is invented | None | AC5 |
| X5 | The DP07 batch is late | The Workbench facts are still handed over, the product shows its freshness warning and no court fact is carried as current | MSG-P1-001 | AC6 |
| X6 | JOB-04 writes a BREAK row or a new REC-05 orphan for a migrated record during the ten days | The count resets to zero, the day is named in the cut-over record and the break is listed for the data steward; a sign-off is refused | MSG-P1-012 | AC2 |
| X7 | An owner's load rejects or fails after another owner accepted, or the same instruction arrives in both the DM007 and the DM008 package | The day is not clean, the row is listed for the data steward and that owner's role, and the second package completes the row on the instruction id instead of duplicating it | None | AC10, AC12; ASM-0742 |
| X8 | A caller without the Platform administration right R starts the step | 403 (401 with no session) before any read of the dump and nothing is written | MSG-P4-002, MSG-P4-001 | AC3, AC8 |
| X9 | A sign-off is attempted while the count is below ten | The sign-off is refused, the count and the resetting day are returned, and no sign-off record is written | MSG-P1-023 | AC1 |

The message texts are the legacy ones and are unchanged (section 14). X1, X2, X3, X4 and X7 carry no new message ID. A sign-off refused below ten clean days answers MSG-P1-023 (RD-P1-042; it settles NEW-GAP-S13-2), whose text confirmation is Pending, owner Error and Message Standard owner; MSG-P1-012 stays the break message only.

### 6. INVEST check
| Test | Result |
|---|---|
| Independent | One reader, one mapper, one package assembler, one evidence reader, one sign-off operation and one Flyway version; the three owner loads are mocked |
| Negotiable | The package layout and the cut-over record are agreed at the rehearsal; this story fixes the three record sets, the no-copy rule, the count and the sign-off only |
| Valuable | Every legal action, notice and instruction of an open case keeps its case, its firm and its dates at cut-over, and the cut-over is evidenced rather than asserted |
| Estimable | One batch step, five components, one migration, six fixtures and the test cases of section 16 |
| Small | Fits one sprint, as the P1 slice of a split legacy key whose other two criteria sit with one integration story |
| Testable | AC1 runs end to end on a synthetic dump and synthetic reconciliation rows; no production data and no live ACE data are needed |

### 7. Acceptance criteria
No legacy criterion other than AC3 is owned here: AC1 and AC2 of RWB-DM-007 sit with RWB-ITG-DM007-ITG, which is where the extract rule and the REC-05 key resolution are proved, and neither is copied (ASM-3487). AC1 below is AC3 of the legacy key, character for character, with the three Givens its cross-service part needs, each of them a mock of an owner's contract. The thirteen criteria after it are new for this slice and test only the cut-over deliverable: the count, the sign-off, the boundary, the no-copy rule, the read path and the rerun. Every value reused — ten clean days, the sign-off, the retention period, the migrated records served from the new schema — is the legacy value, and no business value is added.

```gherkin
Feature: Migrate legal events and cases

  Background:
    Given the environment is SIT
    Given the service is rwb-source-data, its schema is rwb_source_data and its REST base is /api/recovery/source-data/v1
    Given schema "rwb_source_data" holds the baseline of RWB-P1-E1001-APP, the owner contract mocks are registered and the cut-over dump of the open cases is available

  Scenario: AC1 Cut over (legacy RWB-DM-007 AC3)
    Given ten clean days on the migrated records
    Given the rwb-litigation contract mock returns the migrated legal action served from schema "rwb_litigation"
    Given the rwb-comms contract mock returns the migrated notice served from schema "rwb_comms"
    Given the rwb-partner contract mock returns the migrated partner instruction served from schema "rwb_partner"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And each record answered by an owner mock carries "migration_source" and "migrated_at"

  Scenario: AC2 Ten clean days are counted from the reconciliation rows (new, D-RCV-60)
    Given ten clean days on the migrated records, with a PASS reconciliation_result row set written by JOB-04 for each business date from 2026-12-01 to 2026-12-10 of a fixture holiday calendar in which all ten are business days, every REC-01 and REC-02 row PASS under "recon.tolerance.pct" version 1 = 0.00, and no new REC-05 orphan on any of them
    When the cut-over evidence reader runs for business date 2026-12-10
    Then the count is 10 and the cut-over record names the ten dates and the rows each day came from
    And a BREAK row for 2026-12-08, or a new REC-05 orphan dated 2026-12-08, sets the count to 2 for the two dates after it and names 2026-12-08 as the day the count restarted
    And the reader writes no row of reconciliation_result, which stays JOB-04's

  Scenario: AC3 The sign-off is recorded once and only with the right (new, D-RCV-60)
    Given the count at 10 and the rwb-access authorise fake holding Platform administration right R for the caller
    When the data steward signs off for business date 2026-12-10 twice with the same Idempotency-Key
    Then one sign-off record exists carrying the business date, the ten day rows it read, the read-only window and the caller's role code, and the second call returns the same record
    And a caller whose right R is absent is refused with MSG-P4-002 before any read of the dump, and no package and no sign-off record is written
    When a sign-off is attempted at a count of 9
    Then it is refused with "MSG-P1-023" "The cutover cannot be signed off. It has 9 clean days and needs 10.", the day the count restarted is returned and no sign-off record is written

  Scenario: AC4 No row of another service's schema is written (new, D-RCV-60)
    Given the three owner contract mocks of AC1 and the rwb_source_data login
    When the cut-over step runs to completion for 2026-12-10
    Then rwb_source_data holds no legal_action, notice, partner_instruction, lawsuit or hearing table, and the step wrote no row of rwb_litigation, rwb_comms or rwb_partner
    Then a direct INSERT into rwb_litigation through the rwb_source_data login is refused with insufficient_privilege
    And the boundary test finds no statement, no constraint and no grant naming rwb_litigation, rwb_comms, rwb_partner or any other rwb_* schema

  Scenario: AC5 The court record is read and never copied (new, D-RCV-60)
    Given a legacy legal action whose "lawsuit_no" is "LIT-SYN-0777" with court name "SYN Court" and claim amount 1000000.00 in "v_ace_lawsuit"
    When the cut-over step hands the legal action over for 2026-12-10
    Then the package row carries the "id", "case_id", "law_firm_id", "action_type" and "status" of the action, "lawsuit_no" "LIT-SYN-0777" as its linking key and "migration_source"
    And it carries no case number, court name, claim amount, filed date, judgment fact or "lit_status"
    And the step issues no read of v_ace_lawsuit, v_ace_hearing or v_ace_pod, and writes no copy of any of them
    And GET /api/recovery/source-data/v1/data-products/DP07/records?caseId={caseId} answers court name "SYN Court" and claim amount 1000000.00 from v_ace_lawsuit, with the DP07 freshness stamp, through the view-backed read of RWB-P1-E1016-APP

  Scenario: AC6 The legacy read path is closed and the new one answers (new, D-RCV-60)
    Given the sign-off recorded for 2026-12-10 and the three owner rows loaded
    When a reader asks for the legal action, the notice and the instruction of case "RW-2026-000123" after the sign-off
    Then each is answered from rwb_litigation, rwb_comms and rwb_partner through their contracts and none of them from a legacy Workbench table
    And a write through the legacy identity is refused for the whole retention period, and the window and its end date are recorded in the cut-over record
    And the DP07 catalog entry and its freshness stamp still name one system of record and one read path

  Scenario: AC7 A refused or failed run writes nothing and is re-runnable (new, D-RCV-60)
    Given a dump that is unreadable on the first attempt
    When the cut-over step is started for 2026-12-10
    Then it stops before any mapping, writes no package and names the business date and the reason with MSG-GEN-001
    When the step is started again for the same business date with the dump readable
    Then exactly one package per owner exists for 2026-12-10, the count is unchanged, and no row and no file is duplicated

  Scenario: AC8 The step and the reads it uses refuse a caller without a session or right (new, D-RCV-60)
    Given a caller with no token, a caller whose Platform administration right is absent, and a case id that has no row
    When the first two start the cut-over step and the third asks the DP07 record read for that case id
    Then the answers are 401 "MSG-P4-001", 403 "MSG-P4-002" and 404 "MSG-P4-003", each a problem body with "messageCode"
    And no dump is read for the refused callers and no row is written

  Scenario: AC9 An interrupted run leaves no partial package and a new run adds no second one (new, D-RCV-60)
    Given the step is interrupted after the legal action package is written and before the notice package for 2026-12-10
    Then no package of the date is accepted and the cut-over record shows the step FAILED
    When the step is run again for 2026-12-10
    Then exactly one accepted package per owner exists for 2026-12-10 and the count is unchanged

  Scenario: AC10 An owner that fails after another accepted does not complete the handover (new, D-RCV-60)
    Given the rwb-litigation mock accepts its package and the rwb-comms mock fails or does not answer for 2026-12-10
    When the handover outcome is recorded
    Then the handover of the date is not complete, the record names rwb-comms and the error, and the clean-day count is not started
    When the date is run again with the rwb-comms mock answering
    Then each owner holds each record id once

  Scenario: AC11 An invalid extract row stops the step
    Given a dump with one legal action carrying no "case_id" and one instruction with an empty "due_at"
    When the mapper validates it
    Then the step stops, no package is accepted, the cut-over record names the record and the field and "MSG-GEN-001" names the field

  Scenario: AC12 An instruction handed over by two keys stays one row
    Given the instruction id "PI-SYN-0001" is in the DM007 package and in the DM008 package
    When the rwb-partner mock receives both
    Then it holds one row for "PI-SYN-0001" and P1 writes no row of rwb_partner

  Scenario: AC13 person_key travels only as a linking key
    Given a notice with "person_key" "PERS-SYN-000601"
    When the package, the fixtures, the logs and the cut-over record are produced
    Then the notice package row carries "person_key" for rwb-comms only
    And no log line, error message or cut-over record entry holds its clear value and UAT data shows it masked

  Scenario: AC14 The feature switch off stops the step and on lets it run
    Given the flag "rwb.source-data.dm007-cutover-extract" is off
    When the release pipeline starts the step for 2026-12-10
    Then the step refuses to start, no dump is read and no package leaves
    Given the flag is on
    When the step is started for 2026-12-10
    Then the step runs and hands over the packages
```

### 8. Business rules
| ID | Rule | Source |
|---|---|---|
| BR1 | `legal_action` is S4's in `rwb_litigation`, `notice` is P6's in `rwb_comms` and `partner_instruction` is S9's in `rwb_partner`; this service extracts and hands over and never loads another service's schema | Ownership Map on the three tables; DP-01; Arch v5 slide 41; ASM-3483 |
| BR2 | The dump is read once per cut-over business date, and `rwb_source_data` holds no legal action, notice, instruction, lawsuit or hearing table and no row of one | Legacy RWB-DM-007 Data and guardrails; TSD P1 v3 T3.10; GAP-2170 |
| BR3 | No lawsuit and no hearing record is copied: the court record is read from `v_ace_lawsuit` and `v_ace_hearing` by the DP07 record read on this service's own login, and the package carries no court or case number or court fact (DF-LEG-006 to DF-LEG-013 are ACE_READ); `lawsuit_no` (DF-LEG-005) is carried only as the linking key | Legacy RWB-DM-007 AC1 (that criterion sits with RWB-ITG-DM007-ITG); TSD P1 v3 T3.3 views 22 to 24; ADR-010; ASM-3488; RD-P1-027 as amended by RD-P1-068 |
| BR4 | A migrated record carries `migration_source` and `migrated_at`, written by the owner's load, and never a copy of an ACE row | Legacy RWB-DM-007 guardrails; TSD P1 v3 T1.1 |
| BR5 | Ten clean days are counted from the `reconciliation_result` rows of JOB-04 on the migrated records; a business date on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears extends the count and a break resets it and names the day | Legacy RWB-DM-007 AC3; FSD P1 v3 A2.11; DL25 option A applied by RD-P1-042; ASM-0743 |
| BR6 | The sign-off is recorded once in the cut-over record of the release pipeline, the legacy tables stay read-only for their retention period, and the migrated records are served from the new schemas | Legacy RWB-DM-007 AC3; ASM-3485, ASM-3486 |
| BR7 | A business key with no ACE row is an orphan and is listed for the data steward and, where the row is missing in ACE, for the ACE team; it never deletes or changes a record | BR-P1-011-3; FSD P1 v3 A2.11.3.1; legacy AC2 (owned by RWB-ITG-DM007-ITG) |
| BR8 | The service migrates on its own Flyway sequence only, forward only; this story's version creates no table for a legal record | DP-15; ADR-021; TSD P1 v3 T3.2 |
| BR9 | ACE data is read only through the `recovery.v_ace_*` views on the service's own login, SELECT only, and never from `public` | BR-P1-001-2, BR-P1-001-4; ADR-010; DP-05 |
| BR10 | No value a business person may change is written in code. The only personal data a package carries is `notice.person_key` as a linking key (Data Classification: Confidential indirect identifier); it goes only to rwb-comms, is masked in UAT and never appears in clear in a log, a fixture taken from real data or a prompt | Legacy RWB-DM-007 guardrails; BR-P1-011; Template and Rules §R7.2 s17; Data Classification v6; RD-P1-027 |

Where each rule lives in the target: BR1 and BR2 are the boundary and are proved by the absence of the five tables and of any write outside `rwb_source_data`; BR3 is the no-copy assertion of AC5; BR4 is carried on the package row; BR5, BR6 and BR7 are the cut-over evidence and the orphan rule it reads; BR8 is the migration; BR9 is the view grant of RWB-P1-E1069-APP; BR10 is the review rule for the cut-over code and its fixtures.

### 9. State transitions
This story changes no case status, no stage, no task and no legal state. The legal action, the notice and the instruction state machines live in S4, P6 and S9, and this story reads them and never writes them. The moves below are the cut-over's own.

| From | Event | Condition | To |
|---|---|---|---|
| Cut-over not started | The step is started for the business date | The dump is readable and every open case is in it | Extracted: the three record sets are read once and mapped to their cases |
| Extracted | The packages are assembled | Every row carries its section 11 fields and `migration_source`, and every instruction its firm and its due date | Handed over: one package per owner sits in the cut-over record |
| Handed over | S4, P6 and S9 each apply their own version | Each owner's sequence is at the version that creates its tables | Loaded: the records are served from `rwb_litigation`, `rwb_comms` and `rwb_partner` |
| Loaded | JOB-04 writes its PASS rows for the migrated records | Every REC-01 and REC-02 row PASS and no new REC-05 orphan on the day | Count at the number of consecutive clean days |
| Count running | A BREAK row or a new REC-05 orphan appears | The break is listed for the data steward | Count at zero, the day named in the cut-over record |
| Count at 10 | The tenth clean day is reached and the steward signs off | The sign-off is recorded once | Signed off: the legacy tables are read-only for their retention period and the records are served from the new schemas |

The cut-over record of the release pipeline is the ledger of each move, and the Flyway history row of this story's version is the schema's own record of the deploy. This story publishes no event that announces a move.

### 10. Authority
| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the cut-over step for a business date, owns the ten day evidence and records the sign-off (FSD P1 v3 A2.11.3.3, A2.2.3.3) |
| RW-TRIBE, squad member | Builds the reader, the mapper, the packages, the evidence reader and the sign-off, and applies the version on the per-service sequence |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right R of the legacy permission check and may read the cut-over record, the evidence and the reconciliation extract for their scope (legacy RWB-DM-007 permission check; TSD P1 v3 T6.1) |
| RW-AUDIT, RW-COMPLY | Read the cut-over record, the ten day rows and the sign-off as evidence; they take no cut-over decision |
| The `rwb_source_data` login | Reads the reconciliation rows and its own dictionary, writes the Flyway history row of its own version and nothing else |
| S4 rwb-litigation, P6 rwb-comms, S9 rwb-partner and their logins | Own their schemas, their sequences and the load of the rows handed over; this story takes no right over them |

No approval level of the delegation of authority applies: the cut-over files no lawsuit and approves no legal step, and the record carries no court fact. Every "who" is a role code held as data in `rwb-access`, and the step authorises through the rwb-access guard; this story adds no role and no grant.

### 11. Data
| BR Field IDs | Entity | What it carries, and what this story does with it |
|---|---|---|
| DF-CAS-001 to DF-CAS-055 | `recovery_case` | EXCLUDE: read from the dump to select the open cases; the case travels as `case_id` on each package row; never written here (P3 owns the table) |
| DF-LEG-001 to DF-LEG-004, DF-LEG-014 | `legal_action` | CARRY: `id`, `case_id`, `law_firm_id`, `action_type`, `status`; handed over, written by S4 |
| DF-LEG-005 | `legal_action` | KEY: `lawsuit_no`, the linking ACE business key to `v_ace_lawsuit` (`DF-ACE-233`); handed over with the action |
| DF-LEG-006 to DF-LEG-013 | `legal_action` | ACE_READ (LIT): `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status`; never carried |
| DF-LEG-015 to DF-LEG-018, DF-LEG-031 to DF-LEG-034 | `notice` | CARRY: `id`, `case_id`, `document_id`, `notice_type`, `template_id`, `hold_reason`, `dispatch_file_id`, `dispatch_attempts`; handed over, written by P6 |
| DF-LEG-030 | `notice` | KEY: `person_key`, linking key with the handling of BR10 |
| DF-LEG-019 to DF-LEG-023 | `notice` | ACE_READ (WIN): `sent_date`, `barcode`, `callback_date`, `delivery_status`, `sent_type`; never carried |
| DF-PRT-008 to DF-PRT-013 | `partner_instruction` | CARRY: `id`, `case_id`, `partner_id` as the firm, `instruction_type`, `instructed_at`, `due_at`; S9 loads both slices, idempotent on the instruction id (ASM-0742). DF-PRT-014 to DF-PRT-016 are RWB-P1-DM008-APP's and EXCLUDE here |
| None (standard columns, LDM v11) | the three owner tables | `migration_source`, `migrated_at`: written by each owner's load |
| DF-ACE-231 to DF-ACE-243 | `v_ace_lawsuit` | The court record, read only by the DP07 record read; never copied and never written (view 22, Section B) |
| DF-ACE-244 to DF-ACE-250 | `v_ace_hearing` | The hearing record, read only by the DP07 record read; no hearing record is copied (view 23) |
| DF-ACE-251 to DF-ACE-260 | `v_ace_pod` | The proof of delivery, read only by the DP07 record read (view 24) |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | `rec_code`, `business_date`, `product_group`, `variance_count`, `variance_pct`, `tolerance_pct` and `result`; read for the clean day count, written by JOB-04 and never here |
| DF-REF-070 to DF-REF-079 | `data_product` | The DP07 row: `product_code`, `system_of_record`, `owner_role`, `refresh_cycle` DAILY and `expected_by` 08:00; read only, written by RWB-P1-E1001-APP |
| DF-OPS-001 to DF-OPS-009 | `data_product_load` | The freshness stamp read with DP07 and cited on the cut-over record; written by RWB-P1-E1015-APP |
| None: framework table, Flyway's own history, outside LDM v11 and Data Classification v6 | `flyway_schema_history` | One row at deploy, at the version of this story, with no table for a legal record |

Field IDs are those of the Logical Data Model and Data Dictionary v11 and TSD P1 v3 T3.3 and T3.6; the same package rows are held in Source to Target Mapping v7, sheet Migration packages. `legal_action`, `notice`, `partner_instruction`, `lawsuit` and `hearing` are no objects of `rwb_source_data`: there is no such table, view or synonym in the schema, and this story's version creates none (BR2). The dump's own layout, its field order, its record format and its file name are Not specified in the source documents (GAP-2170; ASM-3484), and the package layout is fixed at the rehearsal. A migrated legal action links to its court record by `lawsuit_no` (DF-LEG-005, KEY) into `v_ace_lawsuit` (RD-P1-068; settles NEW-GAP-S12-6). S4, P6 and S9 each load their package under their own workload identity and migration owner, the retired SY-DATALOAD identity being used by none (RD-P1-068). The `notice.person_key` and the case's `account_key` are the keys AC2 resolves against the customer and account views, and that resolution is RWB-ITG-DM007-ITG's and REC-05's, not this story's. The only personal data carried is `person_key`, as a key only, handled as BR10 states.

### 12. Contract
#### 12.1 REST operations provided
| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| - | - | This story adds no operation. It reads two existing ones of the service: `GET /api/recovery/source-data/v1/admin/reconciliation/results` (API-P1-003) for the ten day rows, and `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId=` (API-P1-010) for the DP07 read path. The cut-over step itself is a pipeline command, not a job type of the job monitor, and the rerun operation does not apply to it (GAP-2170; ASM-3485; RD-P1-012) | None | None |

#### 12.2 REST operations consumed
| Method | Path | Owner | Use in this story |
|---|---|---|---|
| None | None | None | No cross-service operation is called at run time. The three packages leave as files and each owner's own cut-over step loads its rows; the owners' answers are used only by the contract mocks of AC1 and AC6, one hop and a 2 s timeout where a real call replaces the mock |

#### 12.3 Events published
| Event | Topic | Owner | Trigger |
|---|---|---|---|
| None | `rwb.source-data.events.v1` | P1 `rwb-source-data` | This story publishes no event. `AceDataReady` (EV-26) and `AceDataLate` (EV-27), published on this topic by the freshness story RWB-P1-E1015-APP, belong to AceIngestCheck, of which JOB-04 is a child; a cut-over hands over files and publishes no fact about a case |

#### 12.4 Events consumed
| Event | Topic | Owner | Handler |
|---|---|---|---|
| None | None | None | This story consumes no event and registers no consumer. JOB-04 is started as a child of AceIngestCheck in RWB-P1-E1011-APP, and the cut-over is started by the release pipeline and never by an event |

#### 12.5 Workflows and activities
| Workflow or activity | Queue | Purpose |
|---|---|---|
| None | `rwb-source-data` | This story registers no workflow and no activity. The cut-over is one-off bulk work of the release pipeline and not a Temporal process; JOB-04's reconciliation run on this queue belongs to RWB-P1-E1011-APP |

#### 12.6 Schedules
| Schedule | Queue | When | Purpose |
|---|---|---|---|
| None | `rwb-source-data` | None | This story creates and changes no Temporal Schedule: the cut-over runs once per cut-over window and not on a clock, and JOB-04 runs as a child of AceIngestCheck |

#### 12.7 Tables owned
| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| `reconciliation_result` | `rwb_source_data` | P1 | Read only, for the clean day count of AC2; written by JOB-04 |
| `data_product` | `rwb_source_data` | P1 | Read only, the DP07 row; written by RWB-P1-E1001-APP |
| `data_product_load` | `rwb_source_data` | P1 | Read only, the DP07 freshness stamp; written by RWB-P1-E1015-APP |
| `sys_objects`, `sys_fields`, `data_product_access`, `data_contract` | `rwb_source_data` | P1 | Read only where a read path needs them; no row is written by this story |
| `flyway_schema_history` | `rwb_source_data` | P1 | One row at deploy, at this story's version |
| `legal_action`; `notice`; `partner_instruction` | `rwb_litigation`; `rwb_comms`; `rwb_partner` | S4; P6; S9 | **Never written.** The rows leave as packages and each owner loads them on its own sequence (BR1) |
| `recovery_case`, `case_account`, `case_party` | `rwb_case` | P3 | **Never read and never written.** The case and its keys arrive on the dump row |
| `recovery.v_ace_lawsuit`, `recovery.v_ace_hearing`, `recovery.v_ace_pod` and the other 27 `v_ace_*` views | `recovery` | ACE; granted to P1 | Read only, by the DP07 record read of this service; never copied and never written (BR3, BR9) |

`rwb_source_data` writes nothing outside its own schema, and the only row this story writes there is the Flyway history row of its version. The login holds a grant on `rwb_source_data` and SELECT on the 30 `recovery.v_ace_*` views, and no grant on `rwb_litigation`, `rwb_comms`, `rwb_partner` or `rwb_case` (DP-01, DP-05; ASM-3483).

#### 12.8 Contract fakes
| Fake | Serves | Used for |
|---|---|---|
| rwb-litigation contract fake | S4's legal action answer (no H and no C dependency: the contract is S4's) | "the rwb-litigation contract mock returns the migrated legal action served from schema rwb_litigation" in AC1, and the post-sign-off read of AC6 and the handover outcome of AC10 |
| rwb-comms contract fake | P6's notice answer | The notice Given of AC1, the AC6 read and the failing case of AC10 |
| rwb-partner contract fake | S9's instruction answer | The instruction Given of AC1 and the AC6 read |
| rwb-access authorise fake | DP-08 style authorise answer for the Platform administration right R | The refusal and the contrast call of AC3 |
| JOB-04 reconciliation fixture | The `reconciliation_result` row sets of ten business dates, one PASS to BREAK and back | AC2's count and reset and AC3's refused sign-off |
| ACE view fixture for DP07 | `v_ace_lawsuit` with "LIT-SYN-0777", court name "SYN Court" and claim amount 1000000.00; `v_ace_hearing` and `v_ace_pod` rows | AC5, which also asserts that the cut-over step reads none of the three |

Each fake is replaced by the real owner as its contract story lands, without a change to the scenarios.

#### 12.9 Call-type summary
| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0, consumed 0 | Two existing reads of the service are used; no cross-service call is made at run time |
| Kafka | Published 0, consumed 0 | Topic `rwb.source-data.events.v1` is named for DP-14; this story produces and consumes nothing on it |
| Temporal | 0 workflows, 0 activities, 0 schedules | Queue `rwb-source-data` in namespace `rwb-recovery` is used by JOB-04's reconciliation, not by the cut-over |
| File | 1 read, 3 written | The cut-over dump is read once, and three owner packages are written to the cut-over record of the release pipeline |

### 13. Solution plan
**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `sourcedata/cutover`. Service base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`. The version sits on the service's own Flyway sequence (DP-15). `rwb_litigation` appears in Build step 5 only as the schema the boundary test refuses; it is S4's, and this story writes none of it.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy marker this slice replaces is one schema under one `V0001` baseline in which a cut-over step could read and write `legal_action`, `notice` and `partner_instruction` itself (DP-15): the split is the new work, and DP-05 and DP-19 are carried by the read path — the court record comes to the Workbench only through this service's `v_ace_*` views, and the screens that show it come through the gateway-bff route. The monolith names `recovery.legal_action`, `recovery.notice` and `recovery.partner_instruction` are as-built objects and legacy marker text only; they are not the target and not a read path.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `CutoverLegalReader` | Batch step | Reads the dump once per business date and refuses a second read |
| `LegalRecordMapper` | Domain | Maps each record to its case and its keys and keeps every CARRY and KEY field of section 11 whole; derives no value |
| `LegalHandoverPackages` | Build and run artefact | Assembles one package per owner per business date and writes it to the cut-over record |
| `CutoverEvidenceReader` | Domain and read | Counts the clean days from `reconciliation_result` and names the reset day |
| `CutoverSignOff` | Service operation | Records the sign-off once, idempotent on its key, guarded by the right R |
| `CutoverBoundaryTest` | Test (pipeline) | Fails on any statement, constraint or grant naming another `rwb_*` schema |

**Migrations in order** (the service's own sequence, forward only). 1. The service baseline: schema, login, the seven standard columns and the reconciliation tables (RWB-P1-E1001-APP; already applied). 2. This story: one version that creates nothing, writes no row, and whose description carries the extract's definition, the field list of section 11 and the read-only window. 3. After it, nothing of this key: the three owners' cut-over migrations run on their own sequences and are not this story's.

**Configuration and reference data.** The flag `rwb.source-data.dm007-cutover-extract` (GAP-0534) comes from the platform flag library and defaults off: off, the step refuses to start and no package leaves, and the version still applies because it creates nothing (GAP-2170; ASM-3489). The sign-off and the read-only window sit in the cut-over record of the release pipeline, and the pipeline reads API-P1-003 and API-P1-010 (GAP-2170). The tracker and data-quality-exception rows of the context pack are out of system scope. The retention period of the legacy tables is read from the retention rule in force (RWB-P1-E1017-APP), the DP07 refresh cycle and expected-by time from the catalog row, and the product group and result lists through the reference-data contract of `rwb-case` with the version in force — never as a constant of this story.

**Flag.** One key, `rwb.source-data.dm007-cutover-extract`; it is removed in the release after it is on in production (Environment and Deployment Design, flag table, removal; RD-P1-045); off and on are tested by AC14. Pending: the flag owner, owner solution architect, tracked as GAP-0534.

**Rollback (RD-P1-045).** Switch the flag off first; redeploy the previous tag only if the flag does not cover the fault; never reverse a migration. A repeated run for a recorded business date adds no package.

**Build steps**
1. Write `CutoverLegalReader` and `LegalRecordMapper` over a synthetic dump and prove the single read, the refusal of a second read and the refusal of a row with a missing case or key (AC7; X1 to X3).
2. Write `LegalHandoverPackages` and prove one package per owner per business date, with the section 11 fields and no court or delivery fact (AC1, AC5, AC13).
3. Write `CutoverEvidenceReader` and prove the count, the reset and the named day over the ten date fixture (AC2).
4. Write `CutoverSignOff` behind the guard and prove the single record, the idempotent second call, the refusal below ten and the refusal with MSG-P4-002 before any read of the dump (AC3).
5. Write `CutoverBoundaryTest` and prove the absence of the five tables, the refused INSERT into `rwb_litigation` and the post-sign-off read through the three contracts (AC4, AC6); then the failure and replay cases (AC8 to AC12).

**Done when.** The test cases of section 16 pass; the version applies clean in DEV and SIT on `rwb_source_data`'s own sequence and creates no table; one package per owner exists for the cut-over business date with the fields of section 11; the count, the reset and the sign-off behave as AC2 and AC3 state; the boundary test reports nothing outside `rwb_source_data`; and the post-sign-off read is answered by the three owner contracts with the DP07 freshness stamp.

**Cut-over harness.** The environment, base hosts and synthetic cutover extract fixture with its field layout are agreed at the wave 4 entry check. The SCR-45 composite route path and the break-list fields are taken from the gateway-bff contract once it and the P1 reconciliation operations publish. The reconciliation extract format and retention are fixed with the data steward. The gate is all criteria of section 7 passing on the stubs and again on the real owners.

### 14. Validation and messages
| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P1-001 | The DP07 batch is late when the cut-over hands the Workbench facts over | {product} is from {date}. Today's load has not arrived. | The cut-over record and the DP07 freshness read (X5) |
| MSG-P1-012 | A reconciliation break or a new REC-05 orphan falls on a day of the ten | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. | The evidence reader (X6; AC2) |
| MSG-P1-023 | A sign-off is asked below ten clean days | The cutover cannot be signed off. It has {count} clean days and needs {required}. | The sign-off (X9; AC1) |
| MSG-GEN-001 | The dump is unreadable, or a row has no case or an empty required key | Enter {field}. | The reader and the mapper (X1 to X3; AC7) |
| MSG-P4-002 | A caller without Platform administration right R starts the step or signs off | You cannot {action} here. Your role does not include it. | The authorise guard (X8; AC3) |
| MSG-P4-001 | No session when the step is started | As published in the Error and Message Standard | The authorise guard (X8; AC8) |
| MSG-P4-003 | The DP07 read is asked for a case id with no row | As published in the Error and Message Standard | The DP07 record read (AC8) |

The message texts are the legacy ones of RWB-DM-007, unchanged; MSG-P1-001 and MSG-P1-012 match the Recovery Workbench Error and Message Standard v6 text, and each error that reaches a caller is an RFC 9457 problem response with `messageCode` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. No message carries a personal value, a name or an e-mail address, and Thai text for each message follows DL10 in the story that raises it.

### 15. Screens and states
| Screen | States | Where it is |
|---|---|---|
| SCR-45 Data quality | Loading; breaks; empty, error and no access: Not specified in the source documents (CG-ALL-1937) | `rwb-source-data`, through the gateway-bff composite route of DP-19; the ten day rows, the reset day and the sign-off are read there beside the reconciliation breaks and the REC-05 orphans |
| DP07 record read inside the case screen | Loading; one case's legal actions, notices, hearing record and proof of delivery; stale | `rwb-source-data`, `GET /api/recovery/source-data/v1/data-products/DP07/records?caseId=` with the product's freshness stamp |

No screen is built in this story and no panel is specified: the two rows above name where the cut-over evidence and the migrated records surface. The field list, the panel ids and the layout of SCR-45 for the cut-over are Not specified in the source documents (GAP-2170; ASM-3484) and belong to RWB-P1-AD019-APP, which builds that console.

### 16. Test cases
| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-007-03 | AC1, AC2; BR1, BR5, BR6 | End to end | The synthetic dump with two open cases, two legal actions, two notices and two instructions; the three owner contract mocks; ten consecutive PASS `reconciliation_result` row sets, then one BREAK row and one REC-05 orphan, then ten clean sets again; the sign-off recorded once at ten; a row count of every table of `rwb_source_data` before and after |
| TC-DM-007-04 | Access; AC3; BR6 | Component | A caller whose Platform administration right R is absent in the authorise fake, starting the step and signing off, with no read of the dump and no row written; a second call with the right present for the contrast |
| TC-P1-DM007-APP-01 | AC2; BR5, BR7 | Component | `reconciliation_result` row sets for 2026-12-01 to 2026-12-10, a BREAK row and a new orphan dated 2026-12-08, and a sign-off attempted at a count of 2 |
| TC-P1-DM007-APP-02 | AC4; BR1, BR2 | Component | The three owner mocks, the `rwb_source_data` login, a direct INSERT into `rwb_litigation` and a fixture statement naming `rwb_case`, each refused or failed by the boundary test |
| TC-P1-DM007-APP-03 | AC5; BR3, BR9 | Component | One legacy `lawsuit_no` "LIT-SYN-0777" with a view row, court name "SYN Court" and claim amount 1000000.00; one legal action with no court record; the package row checked for `lawsuit_no` and no other LIT field; the statement log of the step |
| TC-P1-DM007-APP-04 | AC6, AC7; BR4, BR8, BR10 | Component | The sign-off recorded for 2026-12-10 and the post-sign-off read of case "RW-2026-000123"; an unreadable dump and a second run for the same business date |
| TC-P1-DM007-APP-05 | Section 12 operations, events and activities | Contract | Each operation, event and activity of section 12 against its contract, with the three owner contract mocks and the DP07 read |
| TC-P1-DM007-APP-06 | Section 12.7 (ASM-3438); BR1, BR2 | Component | Each table of section 12.7 in a fixture statement, the `rwb_source_data` login's grants, and a row count before and after; the boundary test reports any write outside `rwb_source_data` |
| TC-P1-DM007-APP-07 | AC8 | Contract | Each provided operation of section 12 called without a token, with a token lacking the right, and for a case id with no row; the answers checked as 401, 403 and 404 |
| TC-P1-DM007-APP-08 | AC9 | Component | The cut-over activity retried and run past its timeout for 2026-12-10, then run again; the package and count rows checked for duplicates |
| TC-P1-DM007-APP-09 | AC10 | Component | The rwb-litigation contract mock failing and not answering during the cut-over step for 2026-12-10; the package rows and the cut-over record checked |
| TC-P1-DM007-APP-10 | AC11 | Component | Dump with a row without case and an instruction without `due_at` |
| TC-P1-DM007-APP-11 | AC12 | Component | An instruction id in both packages; owner mocks with one failing after another accepted |
| TC-P1-DM007-APP-12 | AC13 | Component | `person_key` handling checked in captured logs |
| TC-P1-DM007-APP-13 | AC14 | Component | The flag fake off, then on |

The legacy test case IDs of the criteria this story owns are kept as they are: `TC-DM-007-03` for AC3 and `TC-DM-007-04` for the access check. `TC-DM-007-01` and `TC-DM-007-02` sit with AC1 and AC2 on RWB-ITG-DM007-ITG as `TC-DM-007-01-ITG` and `TC-DM-007-02-ITG` and are not repeated here, and `TC-DM-007-03-ITG` and `TC-DM-007-04-ITG` are that story's integration copies of the two cases above. The nine cases with the service prefix are in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same ID; the rows for AC5 and AC8 to AC10 are to be updated there and in the traceability matrix to the version 3 criteria.

### 17. Guardrails
- No business value in code: the ten clean days, the retention period, the refresh cycle, the expected-by time, the product group and the result lists are rows and parameters read at the version in force; nothing of them is a constant, an enum or a check constraint of this story (BR10).
- Personal data: the packages carry keys and codes and never a name, an address or an identity number; `person_key` is carried to rwb-comms only, masked in UAT, and no log line, fixture or prompt carries it in clear (BR10).
- No cross-schema read and no cross-schema write (DP-01): every statement names `rwb_source_data` or a `recovery.v_ace_*` view, the login holds no grant on `rwb_litigation`, `rwb_comms`, `rwb_partner` or `rwb_case`, and the boundary test fails the build on any other name (BR1; AC4).
- ACE data only through the owner's contract or a `v_ace_*` view: the court record is read through `v_ace_lawsuit` and `v_ace_hearing` on this service's own login, SELECT only, and no ACE row is copied (BR3, BR9; AC5).
- One read of the dump per business date, one sign-off per cut-over, and one write per record: the step is idempotent on its business date and its key, the migration is forward only and creates no table, and nothing is dropped in PROD (BR6, BR8; AC3, AC7).

### 18. Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | Recovery data in 14 data products, each with one system of record and one owner; ACE data read through the views and not copied | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | All recovery processes | DP-07 | TC-DM-007-03, TC-P1-DM007-APP-03 |
| REQ-RDF-008 | Reconciliation breaks, referential completeness and quality measures reported, each break with a reason visible to the data owner | Epic 1, 5.2; Program, 5.1 | FEAT-RDF-01 | All recovery processes | REC-01, REC-02, REC-05; DL25 | TC-DM-007-03, TC-P1-DM007-APP-01 |

REQ-RDF-001 and REQ-RDF-008 are carried here for the cut-over share only: the DP07 catalog row and its read path, and the ten day evidence read from the reconciliation rows of REC-01, REC-02 and REC-05. The reconciliation itself, its report and its freshness stamp are RWB-P1-E1011-APP's and RWB-P1-E1015-APP's, and this story writes no row of them.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-ITG-DM007-ITG | Integration | Owns legacy AC1 and AC2 and the `-ITG` copies of the four test cases; proves the extract rule and the REC-05 key resolution across the three owners |
| RWB-P1-E1001-APP, RWB-P1-E1069-APP | App development | H: the reconciliation, catalog and dictionary tables in `rwb_source_data`, and the 30 read-only ACE views with their grants |
| RWB-P1-E1011-APP, RWB-P1-E1015-APP | App development | JOB-04's reconciliation run and the freshness stamp whose rows this story reads |
| RWB-P1-E1017-APP | App development | The retention rule that fixes the read-only period of the legacy tables |
| RWB-P1-AD019-APP | App development | The data quality console that shows the ten day rows, the reset day and the sign-off |
| RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the per-service Flyway sequence and the gateway-bff composite route (DP-15, DP-19) |
| S4, P6 and S9 cut-over stories of their own keys | App development | Load the packages into `rwb_litigation`, `rwb_comms` and `rwb_partner` on their own sequences |

| Legacy reference | Where it is kept |
|---|---|
| The story, the case of a legal record and its keys | Sections 1, 4, 11, 12.7 |
| AC1 Extract the Workbench records and AC2 Reconcile the business keys | RWB-ITG-DM007-ITG; named here in sections 1, 7, 8, 16 and 19 |
| AC3 Cut over: ten clean days, the sign-off, the read-only legacy tables, the new schema | Sections 4, 5, 7 (AC1 to AC3), 8 (BR5, BR6), 9, 13, 16 |
| The law firm instruction as the legal slice of the row, and the panel slice of RWB-DM-008 | Sections 1, 4, 5 (X7), 11; ASM-0742 |
| No lawsuit and no hearing record copied; the court record from `v_ace_lawsuit` and `v_ace_hearing` | Sections 1, 4, 7 (AC5), 8 (BR3), 11, 12.7 |
| Messages MSG-P1-001, MSG-P1-012, MSG-GEN-001 and MSG-P4-002; the legacy permission check | Sections 10, 14, 16 |
| Test cases TC-DM-007-01 to TC-DM-007-04; key RWB-DM-007; story RWB-P1-DM007-APP; patterns DP05, DP15, DP19 | Sections 12, 13, 16, metadata |

The other criteria of the key answer the rest: the extract and the key resolution are RWB-ITG-DM007-ITG's, the panel facts of the same instruction are RWB-P1-DM008-APP's, the rows themselves are S4's, P6's and S9's cut-over stories', and the reconciliation, the freshness stamp and the retention rule are RWB-P1-E1011-APP, RWB-P1-E1015-APP and RWB-P1-E1017-APP.

Open decisions applied in this story: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863), still open and taken as its assumption; DL25 option A applied by RD-P1-042 (assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602); DL43 planning basis A applied by RD-P1-043 (assumptions ASM-0193, ASM-0737, ASM-0748, ASM-0816).

### 19. Out of scope
- Legacy AC1 and AC2, the extract rule, the REC-05 key resolution and the orphan list: RWB-ITG-DM007-ITG, which owns them and carries TC-DM-007-01 and TC-DM-007-02 as the `-ITG` copies.
- The loads into `rwb_litigation`, `rwb_comms` and `rwb_partner`, their tables, their sequences and their state machines: S4, P6 and S9's own cut-over stories. This story writes no row of theirs (BR1).
- The panel facts of the same law firm instruction — panel status, contract end and score: RWB-P1-DM008-APP and S9, which loads both packages idempotent on the instruction id.
- The reconciliation run, its report, the freshness stamp and the retention rule: RWB-P1-E1011-APP, RWB-P1-E1015-APP and RWB-P1-E1017-APP; and the data quality console SCR-45 itself: RWB-P1-AD019-APP.
- Any copy of a court, hearing or proof-of-delivery record, and any new table of a legal record in `rwb_source_data`: forbidden by BR2 and BR3 and not built here.
- The tracker inventory and retirement operations, the data quality exception list and any inbound load: out of system scope under D-RCV-35 U5 and RWB-ACE-001, and this story relies on none of them (GAP-2170; ASM-3483).

### 20. Remaining delivery steps

- Size the story (squad, role RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Confirm the platform contracts as Done and publish the contract fake library version (solution architect).
- Agree the package file layout and location at the cut-over rehearsal (data steward; NEW-GAP-S12-4).
- Confirm the MSG-P1-023 sign-off message (Error and Message Standard owner) and name the flag owner (solution architect; GAP-0534).
- Provide the synthetic dump, view, reconciliation and owner fixtures in DEV (squad).
- Update the DM007 rows in Test Cases v9 and the traceability matrix to the version 3 criteria (QA).
