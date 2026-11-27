# RWB-S9-E6030-APP Hold the partner panel and fee schedule as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6030-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP13, DP19 |
| Parallel lane | L-S9-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E6030-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-030 is realigned onto rwb-partner (S9, service wave 4, business wave 4). The legacy criterion this slice owns is kept word for word with its origin tag and only the `Given the <service> contract mock returns <x>` lines are added. The panel is held as versioned rows of `partner` in `rwb_partner` and served with the reference-data version in force; the fee schedule, the service levels and the two lists are reference data of rwb-case read on its reference-data contract and never copied here (DP-07); the decision record is written through the local library before any panel version changes (DP-03); the two reads move onto `/api/recovery/partner/v1` (DP-13) and the two screens are reached through the gateway-bff composite route (DP-19). The maintenance surface of the panel has no published write operation, the version has no column, and FEAT-PRM-02 has no requirement row (GAP-3108; ASM-5348 to ASM-5358; ASM-5360, ASM-5361). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E6030-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator**, I want **to keep every panel, fee schedule and service level as versioned reference data**, so that **partners are placed, paid and measured by rule**.

This story owns:

- the one legacy criterion of RWB-E6-030 that the plan assigns to this slice (AC2, verbatim with its origin tag), and the rules, messages and screens it depends on;
- the panel as versioned data: the `partner` rows in `rwb_partner` with `panel_status`, `contract_end`, `score` and the standard record columns over DF-PRT-001 to DF-PRT-007, and the panel version load that puts a set of values in force;
- the reference-data version in force: `LOV-PANEL` and `LOV-PARTNER-TYPE` and the fee schedule and service levels behind them, read on rwb-case's reference-data contract and stamped on every answer, never copied into this schema (DP-07);
- the decision record of a version load or a panel change, written through the local decision-record library **before** the row changes (DP-03);
- the two reads on base `/api/recovery/partner/v1`: `GET /partners` and `GET /partner/instructions`, each with the caller's scope applied (DP-13);
- the read-only slices of SCR-34 Partner list and SCR-35 Placement and allocation behind the gateway-bff composite route (DP-19).

It does not own: the published shapes, the `Partner` element, the two lists, the version stamp, the error set and the fakes (RWB-S9-E6030-CON); AC1 and the end-to-end panel read, which RWB-ITG-E6030-ITG owns (ASM-5357); the firm record and its portal users, the contract-end pass and the recall, which are RWB-S9-AD022-APP (ASM-5356); the reference data and its lists (rwb-case, P3); the ledger and the rule rows (rwb-decision, P7); the roles and rights (rwb-access, P4); the instruction lifecycle and the two events EV-20 and EV-21, which belong to the instruction stories (ASM-5351); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective and the metric do not move: every partner type is managed on the same six points, selection and contract and fees among them, and fees are calculated from the contracted schedule and paid against recorded results (FSD S9 Requirements served, REQ-S9-001 and REQ-S9-004); the metric is "Placements by scorecard, 100 percent, measured on the decision log and the Workbench records, reviewed monthly" (FSD S9 A2.2.1).

The problem is the one the module is built for: partners are instructed and paid by email and spreadsheet, and allocation is not based on performance (FSD S9 A1.3). A panel that sits in a spreadsheet cannot be placed by rule, cannot be scored and cannot be the basis of a fee.

D-RCV-60 changes who owns each fact, not what the administrator gets:

- **The panel is this service's, and so is its version.** `partner` is one of the three tables the Ownership Map gives S9; `panel_status`, `contract_end` and `score` are its columns and its `version` is the optimistic lock (context pack ownership rows; TSD S9 T3.1, T3.0).
- **The fee schedule and the service levels are reference data, not tables of this service.** The Ownership Map gives S9 no fee-schedule and no service-level table, and the default ruling of Template and Rules v1 R3 puts parameters and reference data with P3 rwb-case; DP-07 is the pattern of the key, so the schedule, the levels and the two lists are read at the version in force (GAP-3108; ASM-5348).
- **No value is a constant.** BR-S9-002 and legacy AC1 both say it: every value a business person may change is read from reference data with its version (FSD S9 A2.2.3.1).
- **The decision is recorded first**, in the transaction of the change, which is what legacy AC2 tests (DP-03; TSD S9 T2 writes the decision log entry before any change).
- **One base and one route.** The monolith path `monolith-base/partners` becomes `/api/recovery/partner/v1/partners` (DP-13) and the screens are served on the gateway-bff composite route, one hop, 2 s (DP-19).

No business value moves: the panel statuses, the partner types, the schedule and the levels stay data rows read with their version, never a constant of the code.

### 3. Preconditions

- RWB-S9-E6030-CON is published and tagged: the two reads on `/api/recovery/partner/v1`, the `Partner` element, `LOV-PANEL` and `LOV-PARTNER-TYPE`, the version stamp, the consumed reference-data row, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1043-CON is published with the reference-data client library: one read per list set, the version in force returned with the values, one hop and a 2 s budget (DP-07).
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `partner` and `partner_instruction` exist in `rwb_partner` from the DB story of this service with the columns of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; this story adds no table, no column and no migration.
- The reference data of rwb-case is in force at its version with `LOV-PANEL` (ACTIVE, ON_NOTICE, SUSPENDED, EXITED) and `LOV-PARTNER-TYPE` (AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC, RAMC), authored in rwb-case and loaded here through the library (FSD S9 A2.2.3.2; TSD S9 T3.2; ASM-5349).
- The Partner portal right R is declared on both reads and checked through the rwb-access guard; the FSD primary role Reference data administrator is not a role of TSD S9 T6.1, so the rights checked are the ones the two operations declare (GAP-3108; ASM-5352).
- The service runs as its own login on `rwb_partner` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E6030-CON when its tests pass.

### 4. Flow

1. The reference data administrator opens SCR-34 Partner list. The screen calls `GET /partners` on `/api/recovery/partner/v1` with the optional `type` and `status` filters (API-S9-001).
2. The handler asks the reference-data library of rwb-case for `LOV-PANEL` and `LOV-PARTNER-TYPE` at the version in force, one hop and 2 s, and keeps neither value (DP-07; ASM-5349).
3. The handler reads `partner` in `rwb_partner` with the caller's scope applied and answers `PartnerList`: `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end` and `score`, each row carrying the reference-data version in force (DF-PRT-001 to DF-PRT-007).
4. On SCR-35 Placement and allocation the same panel is read for the placement view, and `GET /partner/instructions` answers the instructions placed with the caller's firm from `partner_instruction` with `status`, `page` and `size` and no value beyond the caller's scope (API-S9-003).
5. A panel version load begins with the values to be put in force and the reason; the guard checks the Partner portal right of the caller before anything is read or written.
6. `loadPanelVersion` evaluates the change against the reference data in force and writes **one decision record before any row changes**: the version reference, the rule ID with its version, the inputs reference (the version in force and the version loaded), the outcome and the decided-at time (DP-03; TSD S9 T2).
7. In the same `rwb_partner` transaction the activity writes the panel rows: `panel_status`, `contract_end`, `score` and the standard record columns, with `version` incremented per row by the optimistic lock.
8. The version in force moves; every later answer of section 12.1 carries the new version, and no instruction already issued is re-priced or re-stated (GAP-3108; ASM-5350).
9. A required value that is absent or invalid is refused with the field named and nothing is written (VR-S9-002-1; MSG-GEN-001); a repeated load of the same version answers the record it already wrote and writes nothing.
10. No event leaves this story: the two events of this service are EV-20 and EV-21 and both belong to the instruction stories (ASM-5351).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no `partner` row, no new version, no answer | MSG-P7-003 | AC2, TC-E6-030-02, TC-E6-030-04 |
| X2 | The caller lacks the Partner portal right R of the read or of the load | 403 before any read and before any decision record | MSG-P4-002 | AC2, TC-E6-030-03 |
| X3 | A required value is absent or invalid: code, name, type, panel status | Refused with the field named; nothing written | MSG-GEN-001 | AC2 |
| X4 | The reference-data read of rwb-case does not answer inside 2 s or its breaker is open | The panel shows as unavailable, no value is substituted and no local copy is used | None (platform 503 envelope) | AC2 |
| X5 | A list value is not in `LOV-PANEL` or `LOV-PARTNER-TYPE` at the version in force | The value is refused and the version is named in the error detail | MSG-GEN-001 | AC2 |
| X6 | The version loaded is older than the version in force | The load is refused as stale and nothing changes | None (domain refusal) | AC2 |
| X7 | The same version is loaded twice | One decision record and one move: the repeat is counted and nothing is written | None | AC2 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17, BR5, BR6 |

X1 to X3 are the paths RWB-E6-030 carries; X4 to X7 are the paths DP-07 and the version rule add; X8 is the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E6030-CON, the reference-data library stub, the decision-record stub, the gateway-bff fake and the access fake, on its own schema, and needs no live P3, P4 or P7 |
| Negotiable | The element names, the load command and the shape of the version stamp are this story's choice; the operations, the fields, the two lists, the rights and the messages are fixed |
| Valuable | The panel, its status, its contract end and its score are read as the version in force, and every change is recorded before it is made |
| Estimable | Two read handlers, one load command with its decision record, two screen fragments and the access and failure tests |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic partners through the contract fakes, plus the access refusal and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Hold the partner panel and fee schedule as data

  Background:
    Given the reference data of rwb-case is in force at its version and carries LOV-PANEL and LOV-PARTNER-TYPE
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E6-030 AC2)
    Given the rwb-partner contract mock returns partner "PTN-2026-000030" of type "AGENCY" on panel status "ACTIVE" with contract end 2027-03-31 and score 72.50
    Given the rwb-case contract mock returns reference data version "RD-2026-11-01" with LOV-PANEL ACTIVE, ON_NOTICE, SUSPENDED, EXITED
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC2 is the criterion of RWB-E6-030 word for word: `the decision log cannot be written`, `the action is taken`, `nothing changes` and `the user sees MSG-P7-003` all stand, and the only additions are the two mock lines that stand in for the contract this service publishes and for the reference data it does not own. On this story "the action" is a panel version load or a panel change: both write the decision record first, so both change nothing when the record cannot be written, and neither leaves a partner row, a new version or an answer behind (DP-03).

AC1 of RWB-E6-030 is not copied here: the split plan gives this slice AC2 only and gives the end-to-end panel read to RWB-ITG-E6030-ITG, which carries AC1 word for word with its `-ITG` test copies (ASM-5357). The partner code, the version reference and the dates in the mock lines are synthetic test data and no source value (section 16).

### 8. Business rules

| ID | Rule | Message | Source |
|---|---|---|---|
| VR-S9-002-1 | Required field empty | MSG-GEN-001 Enter {field}. | FSD S9 A2.2.3.1 |
| BR-S9-002 | No value a business person may change is written in code; it is read from reference data with its version | None | FSD S9 A2.2.3.1 |
| BR1 | `partner` is this service's: the code, the name, the type, the panel status, the contract end and the score are its columns in `rwb_partner`, and only the panel fields and the version are written here | None | Context pack ownership rows; TSD S9 T3.1; ASM-5356 |
| BR2 | The fee schedule, the service levels and the two lists are reference data of rwb-case, read at the version in force on its reference-data contract; none of them is copied into `rwb_partner` | None | DP-07; Template and Rules v1 R3 default ruling; ASM-5348 |
| BR3 | The decision is recorded before a panel row changes, with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | MSG-P7-003 | DP-03; TSD S9 T2; legacy AC2 |
| BR4 | Both reads declare Partner portal R with scope applied, and no read answers a firm the caller does not own | MSG-P4-002 | TSD S9 T6.1 and T-A.2 |
| BR5 | No ACE table, no `v_ace_*` view, no document blob and no other service's schema is read here | None | DP-01, DP-05; context pack naming rules |
| BR6 | No event is published and none consumed: the two events of this service are the instruction events of other keys | None | Context pack Events; TSD S9 T5.3; ASM-5351 |
| BR7 | The same version loaded twice writes once and answers one record; a load older than the version in force is refused | None | TSD S9 T-A.2; ASM-5350 |
| BR8 | No personal data enters `rwb_partner`, the decision record, a log or an answer beyond the firm's own registration data | None | Template and Rules v1 §R7.2 s17; TSD S9 T6.2 |

The two FSD rows are copied character for character; BR1 to BR8 are the target rules of this slice and each names the source it rests on.

### 9. State transitions

This story owns the panel status of the record it writes, over the four values of `LOV-PANEL` (TSD S9 T3.2), and the lifecycle of a panel version.

| From (`panel_status`) | Event | Condition | To |
|---|---|---|---|
| No row | A partner is put on the panel | Type, name and status valid at the version in force | ACTIVE, or ON_NOTICE where the contract says so |
| ACTIVE | A missed target or an upheld conduct breach | The rule of the owning story fires | ON_NOTICE |
| ON_NOTICE | The cure period lapses | The rule of the owning story fires | SUSPENDED |
| SUSPENDED or ON_NOTICE | The contract ends or the exit is approved | `contract_end` passes or the exit is approved | EXITED |
| EXITED | A re-entry is approved | A new contract is in force | ACTIVE |

| Version state | Event | Condition | To |
|---|---|---|---|
| None in force | A version is loaded | Newer than the version in force and the record is written | In force |
| In force | A newer version is loaded | The record is written and the rows commit | New version in force, the previous one superseded |
| In force | A load older than the version in force | X6 | Unchanged, refused |

The moves to ON_NOTICE, SUSPENDED and EXITED are driven by the notice, review and exit stories of this service; this story fixes the values and the record, not their triggers.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Reference data administrator | The primary role of FSD S9 A2.2.3.3: opens SCR-34 and SCR-35, reads the panel and loads a panel version. Not a role of TSD S9 T6.1 (GAP-3108; ASM-5352) |
| Partner and agency manager (RW-AGENCYMG) | Holds CRUDA on the Partner portal and is the secondary user of FSD S9 A2.2.3.3 |
| Platform administrator (RW-PLATADM) | Holds R on the Partner portal and reads the panel |
| Read-only bank roles of TSD S9 T6.1 | Hold R on the Partner portal; the scope decides which rows they see |
| Partner portal users (PT-AGENCY and the other PT roles) | Hold RU and read only their own firm's instructions on `GET /partner/instructions` |
| rwb-case (P3) | Owns the reference data, its lists and their versions; this story reads them and copies none |
| rwb-decision (P7) | Owns the ledger and the rule rows; this story writes its local record and ships it |
| rwb-access (P4) | Owns the roles and the capability rights this story checks through the guard |
| Solution architect | Confirms the maintenance surface of the panel and the version storage (GAP-3108) |

No delegated authority limit applies: the story takes no credit decision and approves no money.

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | `partner` | S9, `rwb_partner` | **Write and read**: `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score`, plus `version` and the standard columns of TSD S9 T3.0 |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | S9, `rwb_partner` | **Read**: the instruction rows of `GET /partner/instructions`; written by the instruction stories |
| None: library table | `decision_record` | Platform library in `rwb_partner` | The hash-linked record written before the row (DP-03) |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | The rule rows and their versions; read through the package, never written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; the record of DP-03 is copied to it by rwb-decision |
| DF-REF-027 to DF-REF-033 | `lov_value` | P3 rwb-case | The values behind `LOV-PANEL` and `LOV-PARTNER-TYPE`, read at the version in force (DP-07) |
| DF-WRK-027 to DF-WRK-036 | `timer` | P3 rwb-case | Named only; this story sets no timer |

The owned row writes six business fields and no personal data: `partner_code` is the firm's bank code and no customer name, contact value or address is copied into `rwb_partner` (BR8). The fee schedule and the service levels appear in the legacy data table of RWB-E6-030 as `rule_row`, `lov_value` and `timer`, which belong to rwb-decision and rwb-case, and no own table carries them (GAP-3108; ASM-5348). `partner_user` is RWB-S9-AD022-APP's and is not read or written here (ASM-5356). The two lists are read as published enumerations at their version and never as constants (BR-S9-002).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). Both rows are read operations of the Ownership Map; the four partner-portal operations of the map belong to the instruction stories of this service (ASM-5351).

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partners` | Query `type`, `status`; `PartnerList` out (API-S9-001) | Partner portal, right R, scope applied | Not applicable |
| GET | `/partner/instructions` | Query `status`, `page`, `size`; `InstructionPage` out (API-S9-003) | Partner portal, right R, scope applied | Not applicable |

Both answer 401, 403 with MSG-P4-002 and 503, each in the platform error envelope; the exact status list and the shapes are RWB-S9-E6030-CON's. No write operation is published for the panel, the fee schedule or the service level (GAP-3108; ASM-5350).

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The reference-data list read; `GET /api/recovery/case/v1/admin/lists/{listCode}` on `/api/recovery/case/v1`, taken from the reference-data contract and published by no S9 source (GAP-3108; ASM-5349) | P3 rwb-case (RWB-P3-E1043-CON) | `LOV-PANEL` and `LOV-PARTNER-TYPE` at the version in force, returned with the values; faked on Day 1 |

One hop with a 2 s budget and a breaker, and no retry inside the step (DP-07, DP-11, ADR-020). The plan's C row for this story is RWB-P3-E1043-CON and it is the only one; rwb-access, rwb-decision and rwb-source-data are reached through the guard and the package, with no direct read.

#### 12.3 Events published

None. The Ownership Map gives S9 EV-20 and EV-21 and both are the instruction events `InstructionIssued` and `PartnerResultSubmitted` of TSD S9 T5.3; a panel version load is not an event any source publishes (GAP-3108; ASM-5351).

#### 12.4 Events consumed

None. The panel and its version are read on the reference-data contract, not from an event, and this story listens to no topic.

#### 12.5 Workflows and activities

None added. `InstructionWorkflow` is the one workflow the Ownership Map gives S9 and it belongs to the instruction stories; the panel version load runs as a service command in the api deployment, inside one transaction, and starts no workflow and no child (context pack Workflows; ASM-5350).

#### 12.6 Schedules

None. The Ownership Map gives S9 no job, and this story declares no Temporal Schedule, no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `partner` | S9, `rwb_partner` | The panel row: code, name, type, status, contract end and score |
| `partner_instruction` | S9, `rwb_partner` | The instructions of the firm, read by `GET /partner/instructions` |
| `decision_record` | Platform library in `rwb_partner` | The local record written before the row (DP-03) |

`rule_row`, `decision_log_entry`, `lov_value`, `timer`, `partner_user`, `recovery_case` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_partner` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case reference-data fake | `LOV-PANEL` and `LOV-PARTNER-TYPE` at version `RD-2026-11-01`; a superseded version; no answer inside 2 s | AC2, X4 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| rwb-partner contract mock (this service's own baseline) | The `Partner` element and `PartnerList` for a synthetic firm; a refused scope | AC2, X2 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for a synthetic panel | AC2 |
| rwb-access rights fake | Partner portal R held and not held | AC2, X2 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | `GET /partners` and `GET /partner/instructions` on `/api/recovery/partner/v1`; the rwb-case reference-data read; one hop, 2 s |
| Kafka | None | No event published or consumed; the decision record rides the library's `rwb.decision-record.v1` and is not an event of this service |
| Temporal | None | No workflow, no activity and no Schedule added |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/partner/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-13 moves the base of the two reads and nothing else. DP-19 puts SCR-34 and SCR-35 behind the composite route. DP-07 is the heart of the story: it is what makes the fee schedule and the service levels data of their owner rather than a copy here. DP-08 and DP-09 are not in the pattern set of this key although the guard is used in fact and no outbox is needed (ASM-5353, ASM-5354).

**Deliverables.** The two read handlers with their scope filter and their version stamp, the reference-data client wiring with its breaker, the panel version load with its record and its optimistic lock, the two screen fragments and the five fakes.

**Build steps.** (1) Wire the reference-data client behind the library and its breaker. (2) Implement `GET /partners` with its filters and its scope. (3) Implement `GET /partner/instructions` with its paging and its firm scope. (4) Write `loadPanelVersion` with the record first, the row update and the version check. (5) Add the two screen fragments on the composite route. (6) Prove AC2 and the eight exception paths on the fakes.

**Done when.** AC2 passes at component level on the fakes, a load with a stopped record stub changes nothing, the boundary test shows no `v_ace_*` read and no `rwb_case` statement, and the two screens answer through the gateway-bff route with the version in force.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the load or of the read is absent or invalid (X3, X5) | Enter {field}. |
| MSG-P4-002 | The role lacks the Partner portal right the operation or the load needs (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The text is the legacy and FSD S9 wording, copied unchanged; no message is reworded and none is added. No message is published for X4, X6 and X7: the 503 is the platform envelope and the stale-version and repeat paths carry no message in any source (GAP-3108; ASM-5361).

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-34 Partner list | Loading; list | Partners, their contracts, panel status and scorecards from `GET /partners`, each row stamped with the version in force (FSD S9 Screens) |
| SCR-35 Placement and allocation | Loading; list | Work placed with partners by rule from the same panel; the slice this story owns is the panel the placement reads |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case and its owner; this story fixes only its own answers. The loading, refused, not-recorded and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-030-01 | AC1 (as the legacy id of this key: the panel held as versioned data) | Component | Synthetic firm `PTN-2026-000030`; one `partner` row and one version stamp on the answer; the end-to-end half is RWB-ITG-E6030-ITG |
| TC-E6-030-02 | AC2 | Component | The decision-record stub stopped on the load; no row, no new version, no answer, MSG-P7-003 |
| TC-E6-030-03 | AC2, X2 | Component | A role without Partner portal R; 403 with MSG-P4-002 and no decision record |
| TC-E6-030-04 | AC2, X1 | Component | A forced decision-record write failure stops the action with MSG-P7-003 |

The four ids are the legacy cases of RWB-E6-030 in their legacy order, carried as the application proof of this slice; TC-E6-030-01 exercises the panel this story writes and its cross-service half is proved by RWB-ITG-E6030-ITG under the same id with the `-ITG` suffix (ASM-5357). The legacy cases carry no level, so each is mapped to Component here and to Contract in RWB-S9-E6030-CON (GAP-3108; ASM-5357). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id.

### 17. Guardrails

- No business value in code: the panel statuses, the partner types, the fee schedule and the service levels stay reference data read with their version, never a constant.
- No personal data in `rwb_partner`, the decision record, a log or an answer: the firm's own registration data, codes and a version only.
- ACE data and documents only through the owner's contract: no `v_ace_*` view, no ACE table, no document blob and no other service's schema (DP-01, DP-05).
- One base, one topic, one queue and one login per service; this story adds no topic, no workflow and no Schedule (DP-13, DP-14).
- The decision record is written before the change and in its transaction; a failure rolls the row and the version back (DP-03).
- The reference data is read at the version in force and never cached beyond the request that read it (BR2, BR7).

### 18. Traceability

| Legacy | Story | Test |
|---|---|---|
| RWB-E6-030 AC1 | Not copied here; owned by RWB-ITG-E6030-ITG (ASM-5357) | TC-E6-030-01 (the application half), TC-E6-030-01-ITG |
| RWB-E6-030 AC2 | AC2 (verbatim, with the mock lines) | TC-E6-030-02, TC-E6-030-04 |
| RWB-E6-030 TC-03 Access | AC2, X2 (the right on the two reads and on the load) | TC-E6-030-03 |
| RWB-E6-030 TC-04 Principle 5 | AC2, X1 (the forced failure of the decision record) | TC-E6-030-04 |

| Source | What it supplies |
|---|---|
| REQ-S9-001, REQ-S9-004 (FSD S9 Requirements served) | The six points of partner management and the fees from the contracted schedule; no requirement row maps to FEAT-PRM-02 (GAP-3108; ASM-5355) |
| FSD S9 A2.2, A1.3, A1.4 and Screens | The feature, the problem, the freshness precondition, VR-S9-002-1, BR-S9-002, the roles and SCR-34 and SCR-35 |
| TSD S9 T2, T3.1, T3.2, T5.2, T6.1, T6.2 and T-A.1 | The decision-first rule, the `partner` and `partner_instruction` columns, the two lists, the cross-module interfaces, the rights and the two operations |
| Context pack S9 and the ownership rows | The schema, base, topic, queue, the three owned tables, the two reads and the two instruction events |
| Template and Rules v1 R3, R5.5 and R7.3 | The default ruling on reference data, DP-03, DP-07, DP-13 and DP-19, and the fill order of the thin story, whose step 4 is unavailable because the Epics 3 to 8 extract is absent (ASM-5360) |
| Split plan, slice RWB-S9-E6030-APP | H, C, I, X, the lane, the wave and the release (GAP-3108) |

### 19. Out of scope

- The contract surface: the OpenAPI document, the `Partner` element, the two lists, the version stamp, the error set and the fakes (RWB-S9-E6030-CON).
- The end-to-end panel read across the services and the wave 4 harness (RWB-ITG-E6030-ITG, which owns AC1); the AC1 happy path is not restated here.
- The firm record, its portal users, the contract-end pass and the instructions recalled by it (RWB-S9-AD022-APP).
- The instruction lifecycle: issuing, accepting, declining, results and invoices, and the two events EV-20 and EV-21 - each is its own story of this service.
- The notice on a missed target, the partner review, the conduct check, the fee approval, the monthly score and the contract exit - each is its own story of this service.
- The reference data of rwb-case and its lists (rwb-case, P3); the ledger and the rule rows (rwb-decision, P7); the roles and rights (rwb-access, P4); the case of record (rwb-case).
- The schema, the migration, the login, the deployment, the observability and the pipeline of `rwb_partner` (the DB, INF and OPS stories of this legacy key); the composite route, which is RWB-PLT-N001-CON's.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
