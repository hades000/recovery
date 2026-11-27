# RWB-S9-AD022-APP Partner firms and partner users

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-AD022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-AD-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-S9-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-AD022-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P4-E1022-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the firm-and-user slice of RWB-AD-022 in rwb-partner. AC2 is kept word for word with its origin tag; the firm is the `partner` row of DF-PRT-001 to DF-PRT-007 and its users are the `partner_user` rows of DF-REF-212 to DF-REF-217, and the day the contract ends a dated pass ends the validity of every live user, so the partner portal refuses them, and sends the `contractEnd` command that closes the panel and recalls the open instructions at `RECALLED` through the branch RWB-S9-E7015-APP owns. No source gives `partner_user` a catalogue entry in TSD S9 T3.1, names the date trigger or a Schedule, or names an event that announces a recall (GAP-3103; ASM-5329, ASM-5330, ASM-5331). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-AD022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **every firm held as a panel record with its users and the period each user may sign in, so that the day its contract ends its accounts stop working and the work placed with it is recalled**, so that **partners see only the work placed with their firm and a firm with no contract holds no live work and no live user**.

This story owns:

- the one legacy criterion of RWB-AD-022 that the plan gives it, AC2, copied verbatim with its origin tag;
- the firm as master data: `partner` over DF-PRT-001 to DF-PRT-007, kept by SCR-34 Partner list;
- the firm's users: `partner_user` over DF-REF-212 to DF-REF-217 (`identity_ref`, `partner_id`, `role_code`, `valid_from`, `valid_to`), and the mapping of a partner's sign-in to that row and its firm;
- the dated pass that finds a firm whose `contract_end` has arrived, ends the validity of its live users in one transaction and sends the recall command for the firm;
- the two reads its screens use, SCR-34 Partner list and PRT-01 Partner home, behind the gateway-bff composite route (DP-19) on base `/api/recovery/partner/v1` (DP-13).

It does not own: the exit itself, that is the close of the panel at `EXITED`, the recall of the open instructions, the exit's decision record, the request to rwb-case to re-select and the service-level clock, which are the `contractEnd` branch of RWB-S9-E7015-APP on the same workflow (ASM-5331); the published shapes, the six operations, the rights, the error set and the fakes, which are RWB-S9-AD022-CON; the criterion that a partner sees only its own firm (AC1), which belongs to the partner-portal read story although the scope filter is built here (ASM-5333); issuing, accepting, declining, recording a result and invoicing an instruction; the notice on a missed target; the scorecard and the allocation; the case of record, which is rwb-case; the roles and rights, which are rwb-access; and the deployment, which is the operations story of this key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: partners were instructed and paid by email and spreadsheet, and a firm whose contract ended left its users able to sign in and its work stranded (FSD S9 A1.3, A2.12.1). The target holds the firm and its users as rows of one service and lets the end of the contract act on both, measured on the decision log and the Workbench records at the monthly target of A2.12.1. What D-RCV-60 changes is who owns the firm, the user, the trigger and the record.

- **The firm is this service's.** `partner`, `partner_instruction` and `partner_user` are S9's three tables in `rwb_partner` (context pack ownership rows), and the panel status, the contract end and the users live in them and nowhere else.
- **A partner user is a period, not a flag.** The module's rows give `partner_user` a `valid_from`, a `valid_to` and a `role_code` (DF-REF-212 to DF-REF-217), so an account is disabled by ending its validity at the contract end and no new status column is invented (ASM-5329).
- **The exit is already one branch.** The close of the panel, the recall to `RECALLED`, the exit record and the case request are the `contractEnd` branch of RWB-S9-E7015-APP under R-UNI-26 and R-UNI-45; this story adds the date trigger and the account effect and duplicates neither (ASM-5331).
- **The end of the contract is a dated rule.** AC2 reads "when the day ends", so the trigger is a date check on `contract_end` and no officer has to remember it; the pass is a Schedule of the service (ASM-5330).
- **Two facts have no source.** `partner_user` has no entry in the TSD S9 T3.1 catalogue (GAP-3103; ASM-5329), and the service's event pair EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted` carries neither a recall nor an account change, so nothing is announced (GAP-3103; ASM-5337).

No business value moves: the panel states, the instruction states, the contract date, the right and the target are reference data and rule values, read with their version and never written in code.

### 3. Preconditions

- RWB-S9-AD022-CON is published: the `partner` and `partner_instruction` elements, the four lists, the six operations on `/api/recovery/partner/v1`, the rights and the error set.
- `partner` and `partner_user` exist in `rwb_partner` from the DB story of this service, with DF-PRT-001 to DF-PRT-007, the user fields of DF-REF-212 to DF-REF-217 and the standard columns of TSD S9 T3.0. The user fields are not catalogued in TSD S9 T3.1 and are taken from the Logical Data Model (GAP-3103; ASM-5329).
- RWB-P4-E1022-CON is published with its fake: the partner-portal right of the caller and the status of a partner's sign-in, one hop, 2 s (ASM-5332).
- RWB-PLT-N001-CON is published: SCR-34 and PRT-01 reach this service through the gateway-bff composite route (DP-19).
- The `contractEnd` branch of RWB-S9-E7015-APP is available on `InstructionWorkflow` and accepts the firm reference and the end date as a command; the branch owns the panel, the recall, the record, the case request and the clock.
- A firm is on the panel at `ACTIVE` or `ON_NOTICE` with a `contract_end` of today and live users whose `valid_to` is open.
- The service runs as its own login on `rwb_partner`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or an ACE view is refused and fails the boundary test.
- No approval is needed to build against a Draft contract baseline.

### 4. Flow

1. The firm is kept as master data on SCR-34: code, registered name, type, panel status, contract end and latest score (DF-PRT-001 to DF-PRT-007); the panel, the fees and the service levels are reference data with their version (FEAT-PRM-02, BR-S9-012).
2. Each user of a firm is a `partner_user` row with its `identity_ref`, its `partner_id`, its `role_code` and the `valid_from` and `valid_to` of the period it may sign in (DF-REF-212 to DF-REF-217); the manager sets the period and a partner never extends its own.
3. A partner signs in through the partner gateway, the service maps the token subject to its `partner_user` row, and the request is refused at 403 with MSG-P4-002 when the row is unknown or its validity has ended (X3).
4. The dated pass runs daily at 00:05 on the Temporal Schedule `rwb-partner-contract-end` on task queue `rwb-partner` in namespace `rwb-recovery` (target design; ASM-5330).
5. The pass selects every firm whose `contract_end` is today or earlier and that still holds a user whose `valid_to` is open or null; a firm already wholly closed is skipped, so a second run of the same day changes nothing.
6. `AccountEndDecisionRecordWriter` writes one record per firm before any change: the firm, the contract end, the users whose validity ends, the rule version in force and the trigger (ASM-5331; R-UNI-39).
7. `endAccountValidity` writes in one transaction, per firm: `valid_to` of every live user set to the contract end, and the audit columns; no other column of `partner_user` moves and no row is deleted.
8. The pass then sends the `contractEnd` command for the firm on `InstructionWorkflow`: the same command the manager's act sends, which closes `panel_status` at `EXITED`, recalls the open instructions at `RECALLED`, records the exit, asks rwb-case to re-select each case and starts the service-level clock, all of it RWB-S9-E7015-APP's.
9. After the commit SCR-34 shows the firm at `EXITED` with its users closed, PRT-01 shows the recalled instructions and a partner call with an ended validity is refused (X3).
10. No event is published and no second topic is used: the account change and the recall are rows and records, and the owning services read them on the read surfaces (GAP-3103; ASM-5337).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The account record cannot be written for a firm | That firm's users keep their validity and the command is not sent; nothing else changes | MSG-P7-003 | AC2, TC-AD-022-02 |
| X2 | The caller does not hold the partner-portal right of the operation | 403 before any read or write | MSG-P4-002 | TC-AD-022-03 |
| X3 | The partner account is unknown, or its `valid_to` has passed | 403; no firm, instruction or fee is returned | MSG-P4-002 | TC-S9-AD022-APP-03 |
| X4 | An instruction is asked for by a caller of another firm | 404; the scope comes from the user's row, never from a parameter | None | §17, BR7 |
| X5 | The Schedule fires twice, overlaps or re-runs after a failure | One pass per firm per day: a closed firm is skipped and a half-written firm is retried whole | None | AC2, TC-S9-AD022-APP-01 |
| X6 | The rwb-access read or the command to the exit branch does not answer inside 2 s | The account rows stand as committed, the command is retried on the workflow's own schedule, and the caller sees 503 | None | §13 |
| X7 | The firm has live users and no open instruction, or the reverse | Each side acts on what exists and no error is raised | None | AC2 |
| X8 | A statement reaches a `v_ace_*` view, a `recovery_case` row or another schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | §17, BR9 |

X1 is the legacy exception flow of FSD S9 A2.12.4.3 and X2 the legacy right check; X3 to X8 are the paths the portal, the Schedule, the shared branch and the schema boundary add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-AD022-CON, the rwb-access fake, the decision-record stub and the exit branch's command surface, on its own schema, with no live P3 or P4 |
| Negotiable | The clock time, the activity names and the pass's internal shape are this story's design; the criterion, the base, the lists, the rights and the screens are fixed |
| Valuable | A firm whose contract ends has no user able to sign in the next morning and its work is recalled, with the change on the record |
| Estimable | One scheduled pass, one transaction over the users, one record write, one command and two read surfaces |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on a synthetic firm with a contract end of today, on the fakes, with the clock controlled |

### 7. Acceptance criteria

```gherkin
Feature: Partner firms and partner users

  Scenario: AC2 Contract ends (legacy RWB-AD-022 AC2)
    Given the rwb-access contract mock returns the partner portal right R
    Given a firm whose contract ends today
    When the day ends
    Then the system disables its user accounts and open instructions are recalled
```

AC2 is the legacy criterion word for word, with its origin tag added and nothing else changed: "a firm whose contract ends today", "the day ends" and "the system disables its user accounts and open instructions are recalled" all stand. Its cross-service part is the caller's right, so AC2 carries the one `Given the rwb-access contract mock returns the partner portal right R` line and that is the only addition. The outcome is the same as FSD S9 AC-S9-012-01, written one epic ahead: the accounts are disabled by ending their validity, and the recall is the `RECALLED` status the exit branch writes on the instructions of that firm (ASM-5331).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The firm and its users are `rwb_partner`'s rows and no statement leaves the schema; `partner_id` and `case_id` are identifiers of another row or another service's fact, not foreign keys across schemas | DP-01; TSD S9 T3.3 |
| BR2 | No value a business person may change is written in code: the panel states, the instruction states, the types, the contract end and the right are read with their version | BR-S9-012; FSD S9 A2.12.3.1; legacy Guardrails |
| BR3 | An account is disabled by ending its validity: `valid_to` is set to the firm's `contract_end`, and no row is deleted and no status column is invented | AC2; DF-REF-217; ASM-5329 |
| BR4 | The pass acts on the firm whose `contract_end` is today or earlier and skips a firm already closed; a second run of the same day changes nothing | AC2; X5 |
| BR5 | The record is written before the change, one per firm per pass, with the rule version in force; a failed write leaves the users as they were and sends no command | DP-03; R-UNI-39; FSD S9 A2.12.4.3 |
| BR6 | The exit is the branch of RWB-S9-E7015-APP: this pass sends the `contractEnd` command and writes no `panel_status`, no instruction status and no case request of its own | ASM-5331; R-UNI-26, R-UNI-45 |
| BR7 | The scope of every portal read is the firm of the caller's `partner_user` row; a request parameter never widens it | AC1 read surface; ASM-5333 |
| BR8 | No personal data in a row, a log or a workflow input: the user is an `identity_ref`, a firm and a role, and no name, e-mail, phone number or identity number is copied from the partner | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR9 | One base, one topic, one queue, one schema and one login per service; no `v_ace_*` grant and no grant on another `rwb_*` schema | DP-13, DP-14; Template and Rules §R4; ASM-5332 |
| BR10 | No event is published by this pass: neither a recall nor an account change is in the service's event pair | TSD S9 T5.3; GAP-3103; ASM-5337 |

The lists this story reads, copied from TSD S9 T3.2 and published unchanged:

| List | Values | Use here |
|---|---|---|
| LOV-PANEL | `ACTIVE`, `ON_NOTICE`, `SUSPENDED`, `EXITED` | The panel status shown on SCR-34 and read by the pass |
| LOV-INSTR-STATUS | `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE`, `RECALLED` | Read only, to show on PRT-01 which instruction is recalled |
| LOV-INSTRUCTION | `COLLECT`, `FILE_SUIT`, `ENFORCE`, `APPRAISE`, `REPOSSESS`, `LIST`, `SELL` | Read only, to show the instruction as placed |
| LOV-PARTNER-TYPE | `AGENCY`, `LAW_FIRM`, `VALUER`, `AUCTION_VENDOR`, `BROKER`, `DEBT_BUYER`, `AMC`, `RAMC` | Read only, to show the firm and its users |

### 9. State transitions

The account, as this story writes it:

| From | Event | Condition | To | Written by |
|---|---|---|---|---|
| `valid_to` open or null | The contract-end pass | The firm's `contract_end` is today or earlier | `valid_to` = the contract end | rwb-partner, this story |
| `valid_to` = the contract end | The pass again on the same or a later day | Any | Unchanged | none; the firm is skipped (X5) |
| `valid_to` in the future | A new contract or an extension | The manager sets a new period | A new `valid_to` | the manager's edit on SCR-34, not this pass |
| `valid_to` passed | A sign-in | Any | Refused at 403 with MSG-P4-002 | the portal check (X3) |

The firm and the instruction, as the pass reads them and the exit branch writes them:

| From (`panel_status`) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `ACTIVE`, `ON_NOTICE`, `SUSPENDED` | The `contractEnd` command | The end date has arrived | `EXITED` | RWB-S9-E7015-APP's branch, on R-UNI-26 |
| `SENT`, `ACCEPTED`, `IN_PROGRESS` | The `contractEnd` command | The firm exits | `RECALLED` | RWB-S9-E7015-APP's branch |
| `DECLINED`, `DONE`, `RECALLED` | The `contractEnd` command | The firm exits | Unchanged | none |

The panel and instruction states are the lists of TSD S9 T3.2 and this story moves none of them: it moves the validity of the accounts and sends the one command that moves the other two.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | CRUDA: the primary role of FSD S9 A2.12.3.3, keeping the firm, setting the users' periods and reading the recall |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL | RA: the also-uses roles of FSD S9 A2.12.3.3 |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | CRU: read the firm and its instructions and hold the work they placed |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | R: read only, in scope, refused the user edit |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | RU: partner users, scoped to their own firm, refused the user edit and the pass |
| rwb-partner service identity | Runs the pass, reads the right, writes the record and the validity, sends the command and serves the two reads; no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and nothing wider: the legacy table names eight roles and "21 more", and T6.1 resolves them to the 23 `RW-*` and 6 `PT-*` identities above, which are 29 and agree with the legacy count. DP-08 is not in the pattern set: the right is declared per operation and arrives on RWB-P4-E1022-CON, and the guard is a template capability (ASM-5332).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id | Read and write, the firm the users cite |
| DF-PRT-002 | partner (S9, `rwb_partner`) | partner_code | Read and write, the business key |
| DF-PRT-003 | partner (S9, `rwb_partner`) | partner_name | Read and write, the registered name |
| DF-PRT-004 | partner (S9, `rwb_partner`) | partner_type | Read and write over LOV-PARTNER-TYPE |
| DF-PRT-005 | partner (S9, `rwb_partner`) | panel_status | Read only here; written by the exit branch (BR6) |
| DF-PRT-006 | partner (S9, `rwb_partner`) | contract_end | Read, the date the pass tests |
| DF-PRT-007 | partner (S9, `rwb_partner`) | score | Read only, shown on SCR-34 |
| DF-REF-212 | partner_user (S9, `rwb_partner`) | identity_ref | Read, the sign-in mapped to this row; no name or contact value |
| DF-REF-213 | partner_user (S9, `rwb_partner`) | partner_id | Read, the firm that scopes the account |
| DF-REF-214 | partner_user (S9, `rwb_partner`) | role_code | Read, the partner role the account holds |
| DF-REF-215 | partner_user (S9, `rwb_partner`) | valid_from | Read, the start of the period |
| DF-REF-216 to DF-REF-217 | partner_user (S9, `rwb_partner`) | valid_to | Write, the end of the period this pass sets to the contract end |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read only here, to show the recalled instruction on PRT-01 |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, in `rwb_partner`) | rule id, rule version, decision code, inputs, from and to state, decided at | Write through the library, before the validity changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 20 more | Not read as a table and not written: the exit branch commands the case |
| every `v_ace_*` view | ACE (P1) | Any | Not read: no `v_ace_*` grant, and DP-05 is a prohibition (ASM-5332) |

The firm's fields are those of TSD S9 T3.1 and the Logical Data Model; the user's fields are DF-REF-212 to DF-REF-217 of the Logical Data Model, because TSD S9 T3.1 catalogues the firm and the instruction and not the user (GAP-3103; ASM-5329). **No new table, no new column and no migration** is declared: the three tables arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's migration (DP-03).

**No personal data.** The rows carry a firm, codes, dates, a list value and an identity reference. The partner user is a key, a firm, a role and a period, never a name: no e-mail, phone number, address or identity number is read into a row, an answer, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the two reads its screens use; the four mutations of the same baseline are built by the instruction stories.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partners` (API-S9-001) | Query `type`, `status`; `Partner[]` out with the panel status and the score | Partner portal, right R, scope applied | Not applicable |
| GET | `/partner/instructions` (API-S9-003) | Query `status`, `page`, `size`; `InstructionPage` out for the caller's firm | Partner portal, right R, scope applied | Not applicable |

The answers 401, 403 with MSG-P4-002 and 503 are the published error sets of TSD S9 T-A.2 for the two operations. The user edit and the contract-end pass have no published operation: the ownership rows give the service six operations and none of them maintains a user or ends a contract, so the account effect is read through `GET /partners` and the recall through `GET /partner/instructions` (GAP-3103; ASM-5329).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The partner-portal right and identity read (operation Not specified in the source documents (GAP-3103; ASM-5332)) | `/api/recovery/access/v1` | P4 rwb-access | The right of the caller per operation and the status of the partner's sign-in, once per request and once per pass; faked |

The row is one hop with a 2 s timeout and a breaker (ADR-020), and it is the contract dependency RWB-P4-E1022-CON of the metadata table. No read of rwb-case is declared: the case reference arrives on the instruction row as an identifier, and the re-selection is the exit branch's command (ASM-5331).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` (DP-14) and its set carries EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted`, both belonging to the instruction stories (TSD S9 T5.3; context pack events). Neither announces an account ending or a recall, so this story declares no event, no producer group and no outbox row, and the absence test fails a build that adds one (GAP-3103; ASM-5337).

#### 12.4 Events consumed

None. Work arrives as a row placed through API-S9-002 and the pass is date-driven, so this story holds no consumer group, no subscription and no inbox row. FSD S9 A2.12.4.4 declares no background event for the feature, which is the conflict recorded for the date trigger (GAP-3103; ASM-5330).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `rwb-partner-contract-end` pass | Schedule-started workflow execution, one per run, one child per firm | `rwb-partner` in namespace `rwb-recovery` | Input: the business date; outcome: the firms with users closed and the commands sent |
| `sweepContractEnd` | Activity, the selection of firms and their live users | `rwb-partner` | The business date in; the firms with their users and their contract end out |
| `endAccountValidity` | Activity, the record and the one transaction of a firm | `rwb-partner` | The firm, the users and the end date in; the record reference and the count out, record first |
| `InstructionWorkflow` | Workflow, one per firm, owned by RWB-S9-E7015-APP | `rwb-partner` | The `contractEnd` command with the firm reference and the end date; the panel, the recall, the case request and the clock are its branch's |

`InstructionWorkflow` is the one workflow in the context pack's ownership rows for this service, and the pass with its two activities is the service's dated step, a target design name. This story sends the command and changes no signal of the workflow; `CaseWorkflow` stays with rwb-case.

#### 12.6 Schedules

| Name | Schedule | Task queue | What it starts |
|---|---|---|---|
| `rwb-partner-contract-end` | Daily at 00:05, business calendar, overlap skipped, catch-up once | `rwb-partner` in namespace `rwb-recovery` | The contract-end pass, one run per business date |

The service owns no Quartz job and no shared job table (context pack, Jobs: None), and Temporal Schedules replace Quartz (ADR-016). No source names a Schedule, a clock time or an overlap rule for this pass and FSD S9 A2.12.4.4 declares no background event, so the name, the time and the catch-up rule are a target design and the absence of DP-10 and of RWB-PLT-E1071-CON from the pattern and build rows is recorded (GAP-3103; ASM-5330).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm, its panel status and its contract end; this story reads it and writes no status |
| partner_user | S9 (`rwb_partner`) | The firm's users and their periods; this story writes `valid_to` and the audit columns |
| partner_instruction | S9 (`rwb_partner`) | The work placed with a firm; this story reads the recalled status and writes none |
| decision_record | PLT library, in `rwb_partner` | The local hash-linked record of the pass (DP-03) |
| idempotency_key | PLT library, in `rwb_partner` | The keys of the instruction operations; the pass uses none |
| outbox_event | PLT library, in `rwb_partner` | Present as a library object; this pass writes no row (§12.3) |

Not owned and never read as a table: `recovery_case` (P3), every `v_ace_*` view (P1), `decision_log_entry` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access right and identity fake (`RWB-P4-E1022-CON`) | The partner-portal right per operation and a partner sign-in whose validity is live, open or ended | AC2, X1, X2, X3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-34 and PRT-01 answers for a firm before and after its exit | AC2, X5 |
| `contractEnd` command fake of the exit branch | The command accepted, the panel returned at `EXITED` and the instruction set at `RECALLED` | AC2, X7 |
| Clock fake for the Schedule | A business date before, on and after `contract_end` | AC2, X5 |

The fakes are test-only and are replaced by the real services in SIT; the operation name of the rwb-access read carries the placeholder until its owner confirms it (GAP-3103; ASM-5332).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | API-S9-001 and API-S9-003 on `/api/recovery/partner/v1`; the rwb-access read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the instruction stories; the pass announces nothing |
| Temporal | 1 Schedule, 2 activities, 1 command | `rwb-partner-contract-end`, `sweepContractEnd`, `endAccountValidity`, and the `contractEnd` command to `InstructionWorkflow` |
| File | None | No file is read, built or delivered; the partner portal of INT-24 is screen traffic |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `firm`; front end `src/modules/recovery/partner/PartnerList.tsx` and `PartnerHome.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as a prohibition: this service holds no `AceSourceQuery` and no `v_ace_*` grant, and a case or account reference arrives on the instruction request, so no view is read and no dependency is added. DP-13 moves the two legacy paths to the partner base. DP-19 is how SCR-34 and PRT-01 reach this service, one hop through the gateway. These three are the whole pattern set: DP-10 for the dated pass, DP-08 for the guard and DP-09 for an event are not in it, and their absence is recorded rather than added to the metadata table (GAP-3103; ASM-5330, ASM-5332, ASM-5337).

**Dependencies the tables add and the plan does not hold.** The pattern table adds `RWB-PLT-N001-CON` for DP-19, which the plan's H row carries. It does not carry `RWB-PLT-E1071-CON` for the Schedule of DP-10 or `RWB-PLT-TE006-CON` for the outbox of DP-09, and it does not carry the in-lane story RWB-S9-E7015-APP whose branch this pass commands; all three are recorded as absent from the metadata rows (ASM-5330, ASM-5331).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ContractEndPass` | Workflow | Runs once per business date, one child per firm, and reports the counts |
| `sweepContractEnd` | Activity | Selects the firms due to exit with their live users |
| `endAccountValidity` | Activity | Writes the record and the user periods in one transaction, then sends the command |
| `PartnerAccountGuard` | Service | Maps the caller to its `partner_user` row and firm, refuses an unknown or expired account and reads the right |
| `AccessRightClient` | Client | The rwb-access right and identity read, one hop, 2 s, breaker |
| `PartnerController`, `PartnerList`, `PartnerHome` | Controller and React components | `GET /partners` and `GET /partner/instructions` with the scope and the problem mapping, and the two screen fragments |

**Database and migrations.** No Flyway file: `partner`, `partner_user` and `partner_instruction` arrive with the DB story of this service, and the record is a library object created in `rwb_partner` by the library's migration (DP-03).

**Configuration and reference data.** The panel and instruction states and the partners' types are reference data with their version (BR2); the capability area "Partner portal" and its rights are access rows of rwb-access; the 00:05 clock, the overlap rule and the catch-up rule are service configuration, not constants (ASM-5330).

**Build steps**

1. `sweepContractEnd` against the clock fake, with the firm selection and the already-closed skip (AC2, X5, X7).
2. The record writer against the stub and `endAccountValidity` as one transaction over the users' `valid_to` (AC2, X1).
3. The `contractEnd` command with its retry and its 2 s budget, and the idempotent repeat (AC2, X5, X6).
4. `PartnerAccountGuard` and `AccessRightClient` against the fakes, with the unknown, expired and wrong-right paths (X2, X3).
5. `PartnerController` and the two screen fragments through the composite route fake, with the scope and the paging (§15).
6. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no case write, no panel or instruction write and no outbox row (X8, BR6, BR9, BR10).

**Feature flag.** `rwb.partner.contract-end-v1`, a flag of the platform library; off means the pass does not run and the users keep their periods, and the two reads are unaffected.

**Done when.** The tests of section 16 pass, a synthetic firm with a contract end of today has every live user closed and its work recalled in SIT, a second run of the same day changes nothing and writes no second record, a forced record failure leaves the users open and sends no command, an expired account is refused at 403, no `v_ace_*` read, no case write and no panel write exists in the build, and SCR-34 and PRT-01 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid: a code, a name, a type or a panel status (VR-S9-012-1) | Enter {field}. |
| MSG-P4-002 | The role lacks the partner-portal right, or the partner account is unknown or its validity has ended (X2, X3) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the pass changes anything (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those of the legacy and FSD sets; the text is copied unchanged, no message is reworded and no new one is added. MSG-P4-002 is the legacy partner-portal message, MSG-GEN-001 is VR-S9-012-1, and MSG-P7-003 is AC-EXC-S9-012-02 of FSD S9 A2.12.4.3.

### 15. Screens and states

SCR-34 Partner list holds the firms, their contracts, their panel status, their users and their scores, and PRT-01 Partner home holds the partner's own open instructions, due dates and messages (FSD S9 Screens; legacy table: SCR-34 "Loading; list", PRT-01 "Loading; list"). This story produces the pass's two visible results: SCR-34 shows the firm at `EXITED` with its users closed, and PRT-01 shows the recalled instructions with their due dates kept. Both are reached through the gateway-bff composite route (DP-19), and a partner outside the bank arrives on the partner gateway of FAPI 2.0 (Arch v5 slide 8; INT-24).

No screen is described for the pass and FSD S9 A2.12.4.4 declares no background event, so the place and the time of the trigger are Not specified in the source documents (GAP-3103; ASM-5330). The refusal, expired-account, already-closed and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-022-01 | Firm scope | Component | A partner user of one firm and the instruction read; only that firm's instructions return and the scope comes from the user's row |
| TC-AD-022-02 | AC2 | Component | A firm with a contract end of today and two live users with open validity; every `valid_to` set, the command sent, the panel and the recall read back |
| TC-AD-022-03 | Access | Component | A role without the partner-portal right and an account whose validity has ended; 403 with MSG-P4-002 and no read |
| TC-S9-AD022-APP-01 | AC2, X5 | Component | The same pass twice on one business date; one record, one command and no second change |
| TC-S9-AD022-APP-02 | AC2, X1 | Component | The decision-record stub stopped; the users open, no command sent and MSG-P7-003 raised |
| TC-S9-AD022-APP-03 | X3 | Component | An unknown account and an account whose `valid_to` has passed; 403 with MSG-P4-002 and no data |

The three legacy cases are those of RWB-AD-022 in their legacy order, with the Level column added: every case runs on the fakes and against this service's own rows, so every case is `Component`. TC-AD-022-01 exercises the firm-scope filter this story builds; the criterion it was written for, AC1, belongs to the partner-portal read story (ASM-5333). The three cases `TC-S9-AD022-APP-01` to `-03` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the panel and instruction states, the types, the contract end, the right and the target stay reference data and rule rows, never a constant, a default or a branch.
- No personal data in a row, a workflow input or a log: a firm, codes, dates, a list value and an `identity_ref` only, and every fixture is synthetic.
- ACE data only through the owner's contract or `v_ace_*` views, and this service holds no `v_ace_*` grant at all (DP-05).
- The case stays with rwb-case: no `recovery_case` row and no case state is written here (ASM-5331).
- The firm and the instruction stay with their owner: this pass writes no `panel_status` and no instruction `status`; those are the exit branch's writes (BR6).
- One base, one topic, one queue, one schema and one login per service (DP-13, DP-14).
- No event, topic, consumer or outbox row is added by this pass; a build that publishes an account change or a recall fails the absence test (BR10).
- The record is written before the rows; a build that answers outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-006 | A panel exit, a conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner | The dated pass, the account effect and the command to the exit branch | TC-AD-022-02, TC-S9-AD022-APP-01 |
| REQ-S9-001 | Every partner type is managed on the same six points, notice and exit among them | The firm, its users and the exit | TC-AD-022-01 |
| REQ-S9-002 | Each partner type has one named owner | The firm record and its users on SCR-34 | TC-AD-022-01 |
| REQ-S9-008 | Partners exchange data through the portal and the external gateway, not by email | The two reads through the composite route and the partner gateway | TC-AD-022-03 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the firm, its users and its instructions | TC-AD-022-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-AD-022-02 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The dated pass as a Temporal Schedule | TC-S9-AD022-APP-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The rwb-access read with its budget and breaker | TC-AD-022-03 |
| ADR-022 | Local decision record plus central ledger | The record written before the validity changes | TC-S9-AD022-APP-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-AD-022, disposition Split (rework); legacy feature None, and the closest published features are FEAT-PRM-02 and FEAT-PRM-12 (FSD S9 A2.2, A2.12) |
| Legacy criteria | AC2, owned word for word by this story; AC1 belongs to the partner-portal read story |
| Wave and release | Wave 4 and release 28 February 2027 (tentative), copied unchanged; EP08 is wave 4 and the service's Arch v5 wave is 4, so no W-MAP conflict is raised (ASM-5335) |
| Legacy dependency | "Depends on RWB-E1-022" is a monolith predecessor and is not a build row; the plan's H row carries the CON and the edge contract instead (ASM-5336) |
| Source text | Legacy RWB-AD-022; FSD S9 Partner management v3 A1.1, A1.3, A2.1, A2.2, A2.12, A2.12.1 to A2.12.4; TSD S9 Partner management v2 T0.2, T2, T3.0, T3.1, T3.2, T3.3, T5.1, T6.1, T6.2, T-A; Logical Data Model rows DF-REF-212 to DF-REF-217 |
| Test cases | The three legacy cases and the three new component cases TC-S9-AD022-APP-01 to -03 |
| Feature and screens | FEAT-PRM-02 and FEAT-PRM-12; SCR-34 Partner list and PRT-01 Partner home |
| Rules | BR-S9-012, VR-S9-012-1, and R-UNI-26 and R-UNI-39 in the UNIVERSAL package as the exit branch applies them |
| Decoupling patterns | DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The exit itself and its record, the recall of the instructions, the case request and the service-level clock: RWB-S9-E7015-APP and its `contractEnd` branch (ASM-5331).
- The published shapes, the six operations, the rights, the error set and the fakes: RWB-S9-AD022-CON.
- The criterion that a partner sees only its own firm's work: AC1 and the partner-portal read story; this story builds the scope filter only (ASM-5333).
- Issuing, accepting, declining, recording a result and invoicing an instruction: API-S9-002, API-S9-004, API-S9-005, API-S9-006 and the instruction stories.
- The panel, the fee schedule, the service levels and the onboarding of a firm: FEAT-PRM-01 and FEAT-PRM-02.
- Allocation, the override, the scorecard, the review and the notice: FEAT-PRM-03, FEAT-PRM-04, FEAT-PRM-08, FEAT-PRM-10 and FEAT-PRM-11.
- The case, its route state and its re-selection: rwb-case (P3), commanded by the exit branch and never written here.
- The rights, the partner's sign-in and the partner gateway: rwb-access (P4) and the edge, reached on RWB-P4-E1022-CON, RWB-PLT-N001-CON and the FAPI 2.0 gateway.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
