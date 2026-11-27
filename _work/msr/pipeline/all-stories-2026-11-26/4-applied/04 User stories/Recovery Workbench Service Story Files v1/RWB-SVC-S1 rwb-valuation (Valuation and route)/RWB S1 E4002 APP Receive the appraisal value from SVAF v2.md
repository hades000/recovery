# RWB-S1-E4002-APP Receive the appraisal value from SVAF

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-002 for rwb-valuation (S1). The appraisal ACE ingests from SVAF is read SELECT-only from `recovery.v_ace_valuation` and never copied (DP-05); the Workbench's own decision about it is one `valuation_ext` row in `rwb_valuation` keyed on `valuation_key`, written with its local decision record in one transaction through the RWB-PLT-E1027-CON library (DP-03); the base becomes `/api/recovery/valuation/v1` (DP-13) and SCR-13 is reached through the gateway-bff composite route (DP-19). The legacy AC2 is copied verbatim; AC3 and AC4 are new and test only the target read and row write. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S1-E4002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S1-E4002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-B |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4002-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the Workbench to read the appraisal that ACE has ingested from SVAF for the asset of a case through the SELECT-only `recovery.v_ace_valuation` view and keep its own decision about it — acceptance, the stale flag and the age — in one `valuation_ext` row of `rwb_valuation` against the `valuation_key`, writing the local decision record with the rule ID and the rule version in the same transaction when the case owner assesses the route**, so that **the route is chosen on expected return with reasons instead of on an officer's judgement written up in an account plan**.

This is the application slice of legacy RWB-E4-002. It owns:

- the legacy acceptance criterion AC2 of the story, copied verbatim with its origin tag, and the messages it names;
- the read of the appraisal facts — number, type, value, date and the valuer — for an `asset_key`, from the ACE view ACE fills from the SVAF feed, with no file load, no copy table and no inbound interface (FSD S1 A2.2; D-RCV-35 U1 and U3; ADR-010);
- `valuation_ext` in schema `rwb_valuation`, written and read by this service only, with `stale_flag` and `age_days` computed against the limit in force (DP-01);
- the freshness gate VR-S1-002-1 on `v_ace_batch_status` before the value is used, with MSG-P1-001;
- the local decision record of the receipt, written through the RWB-PLT-E1027-CON library inside the caller's transaction, carrying the rule ID and the rule version (DP-03);
- `POST /cases/{caseId}/route` on base `/api/recovery/valuation/v1`, which is the operation through which the route assessment — and with it this read — is reached (DP-13).

It does not own: the published shape of the operation, the `RouteRequest` and `Approval` schemas, the `valuation_ext` DDL template and the fakes, which are RWB-S1-E4002-CON; ordering an appraisal when the last one is stale (FEAT-VAL-01); flagging outliers against market and the last value (FEAT-VAL-03); accepting the value (FEAT-VAL-04); the COLLINS return by route (FEAT-VAL-05); the route scoring and recommendation (FEAT-VAL-07); the ACE ingestion of the SVAF feed, which is ACE's, and the `v_ace_*` views, which rwb-source-data owns; the case, its status and the case view, which are rwb-case's (P3); the central decision ledger, which is rwb-decision's (P7); the rights and scope data, which are rwb-access's (P4); the composite route and the screen field list, which are the platform edge story's and the screen owners'.

### 2. Business rationale

A route chosen on expected return needs a value the bank trusts. Today the appraisal reaches the Workbench as a file the Workbench loaded and kept in a table of its own, next to the case, the collateral and the decision log in the one `recovery` schema; the officer's judgement about whether to use it was written into an account plan. The target removes both halves of that: ACE ingests the SVAF feed and exposes it through `recovery.v_ace_valuation`, and the Workbench keeps only its own decision — whether the value is accepted, whether it is stale and how old it is — in `recovery.valuation_ext` (FSD S1 A2.2; D-RCV-35; ADR-010). The business objective is unchanged: read the appraisal the bank has, link it to the collateral by the ACE asset key, and record what the Workbench decided about it, so the route decision runs on expected return with reasons.

What D-RCV-60 changes is where the rows live and who owns each of them. In the target the appraisal facts belong to ACE and are read, never copied: the view is SELECT-only, it is re-pointed by the ACE ingestion and not by this service, and this service holds no foreign key into it (DP-05). The Workbench's own part is one `valuation_ext` row in `rwb_valuation`, written by this service's own login in one transaction with the local decision record and the outbox rows (DP-01, DP-03). That split is why the story is small: one read, one row, one record.

The base and the screen move with it. The monolith served the route assessment on a shared base; the target serves it on `/api/recovery/valuation/v1`, so a route call does not share a path namespace with the case, the payment or the asset services (DP-13), and SCR-13 Route decision is composed by the gateway-bff composite route from the case read and this service's answer rather than by a screen that reads one database (DP-19).

Two boundaries are recorded rather than assumed. The Ownership Map for S1 lists REST operations and the `RouteDecisionWorkflow` but no table, while the legacy story and TSD S1 both give this service a valuation row; the split is read as an omission of the map, and the table is created in `rwb_valuation` by this service (GAP-2594; ASM-4291). And the FSD trigger phrase "a completed ACE batch, an event or a timer" names no schedule, job or event for S1 — the ownership rows show none — so the receipt runs inside the route assessment, with the batch leg asserted by the freshness rule (GAP-2594; ASM-4292).

Serves the route decision of EP04 in wave 3 on release 28 February 2027 (tentative). No business value is invented or moved: the states, the lists, the messages and the rights are the values the FSD, the TSD and the rule workbook already carry, read in force.

### 3. Preconditions

- RWB-S1-E4002-CON is published: base `/api/recovery/valuation/v1`, `POST /cases/{caseId}/route` with `RouteRequest` and `Approval`, the error set with the RFC 9457 problem body, the `Idempotency-Key` header, the `valuation_ext` DDL template and the fakes. This story builds against that contract and its fake and never against a sibling service.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` declared with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003, and the `decision_record` DDL template applied in this service's own schema (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-13 from the case read and the valuation read, one hop each, read only (DP-19).
- The `rwb_valuation` schema and its login exist from the platform database story; the view owner grants this login SELECT on `recovery.v_ace_valuation` and `recovery.v_ace_batch_status`, and on nothing else (ASM-4293).
- The lists LOV-APPRAISAL and LOV-ROUTE are values in force read as data with their version; no member is written in code (BR-S1-002; TSD S1 T3.2).
- The appraisal age limit, the freshness limit and the acceptance rule are reference values in force for the business date; they are read, never constant (BR-S1-002; ASM-4295).
- FSD S1 and TSD S1 carry status "In review" and no approval is needed to build against a Draft baseline; the split proceeds at status Draft (ASM-4296).
- A CON story is Day 1 by rule: this story has only CON build dependencies and starts on Day 1 (§R5.7).

### 4. Flow

1. The case owner opens SCR-13 Route decision for a case and asks for the route assessment; the browser calls `POST /cases/{caseId}/route` on the service base through gateway-bff (DP-13, DP-19).
2. The guard resolves the caller's right from the `security` declaration of the contract; right U in the capability area Treatment and offer is required and the scope is applied (BR-S1-002; TSD S1 T6.1).
3. The freshness gate runs: VR-S1-002-1 reads `recovery.v_ace_batch_status` for the valuation product and, when the product is from an earlier date, the step stops with MSG-P1-001 and writes nothing.
4. The service resolves the asset keys of the case from the request — the asset of the case and, through it, the collateral — and reads the appraisal facts for the `asset_key` from `recovery.v_ace_valuation`: `valuation_key`, `appraisal_no`, `appraisal_type`, `appraised_value`, `appraisal_date`, `forced_sale_value` and the valuer (DP-05).
5. `stale_flag` is set from the appraisal age against the limit in force, and `age_days` from `appraisal_date` and the business date; both are computed, neither is stored in a constant (VR-S1-002-1; BR-S1-002).
6. One transaction opens. The `valuation_ext` row is inserted or updated against the `valuation_key` with `stale_flag`, `age_days`, the valuer reference, the standard record columns and the outbox rows; the request's idempotency row is written in the same transaction (DP-01; DP-13).
7. `DecisionRecordWriter.record` writes the local `decision_record` in the same transaction, with the rule ID and the rule version in force and with the appraisal reference and the stale flag as the facts of the decision; a refusal or an unavailable store rolls the whole transaction back (DP-03; MSG-P7-003).
8. The transaction commits and the route assessment continues in the service with the accepted-or-pending value the row now holds; the recommendation, the COLLINS return and the approval are the sibling stories' (FEAT-VAL-05, FEAT-VAL-07, FEAT-VAL-08).
9. The answer to the caller carries the appraisal facts read from the view and the Workbench's own flags from `valuation_ext`, so SCR-13 shows the value, its type, its date, the stale flag and the age without reading a second database.
10. A repeated request with the same `Idempotency-Key` returns the first answer and writes no second row, no second record and no second outbox row.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without right U in Treatment and offer, or a case outside the scope | 403; the refusal is the guard library's answer and the log carries the role and the operation, never a personal field | MSG-P4-002 | Section 10; TC-E4-002-03 |
| X2 | The valuation product is stale for the business date | The step stops before the read is used: nothing is written and no record is created | MSG-P1-001 | AC4 |
| X3 | The decision record cannot be written | The transaction rolls back: no `valuation_ext` row, no outbox row, no idempotency row; the user sees MSG-P7-003 and the call is retried with the same key | MSG-P7-003 | AC2; TC-E4-002-04 |
| X4 | The asset of the case has no appraisal row in `v_ace_valuation` | No `valuation_ext` row is created, nothing is overwritten and the assessment continues without a value; the screen states that no appraisal is held | None | AC3 |
| X5 | A redelivered ACE row with the same `valuation_key` | The same row is updated, never duplicated, because the key is the unique key of `valuation_ext`; `updated_at` and `version` move | None | AC3 |
| X6 | The ACE view cannot be read, or returns an error | 503 with the platform problem body; nothing is written | MSG-GEN-006 | AC3 |
| X7 | A field of the request is missing or outside its list | 422 with MSG-GEN-001 naming the field; the transaction never opens | MSG-GEN-001 | Section 12.1 |

X1 to X3 are the legacy paths carried onto the split: X1 is the permission check of the legacy story, X2 the freshness rule the FSD gives the feature, X3 legacy AC2. X4 to X7 are the paths the read of a view adds. A refusal under X1, X2 or X7 writes nothing at all, because the guard, the freshness gate and the validator run before the transaction opens.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-S1-E4002-CON fake, the decision-record writer fake and the composite-route fake, with a view fixture standing where ACE's row would be; needs no live ACE, rwb-case or rwb-decision |
| Negotiable | The component names, the internal method boundary, the flag name and the outbox use are this story's choice; the operation, the schemas, the field identifiers, the rule, the messages and the rights are fixed |
| Valuable | The value the bank already holds is used with the Workbench's own decision on record, so the route can be chosen on expected return with reasons |
| Estimable | One operation, one read of a view, one table, one computed flag and age, one library adapter, one migration |
| Small | Fits two weeks with its tests |
| Testable | Each criterion of section 7 is one automated test; the view, the writer and the composite route are fixtures and fakes |

### 7. Acceptance criteria

```gherkin
Feature: Receive the appraisal value from SVAF

  Scenario: AC2 Not recorded (legacy RWB-E4-002 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The appraisal is read from the ACE view and the Workbench's decision is one valuation_ext row (new, D-RCV-60)
    Given the v_ace_valuation fixture holds appraised value 4250000 for appraisal AP-0001 on asset AST-0001 at appraisal date 2026-11-02
    Given the v_ace_batch_status fixture shows the valuation product at the business date
    When the route assessment runs POST /cases/{caseId}/route
    Then the service reads valuation_key, appraisal_no, appraisal_type, appraised_value, appraisal_date and the valuer from v_ace_valuation for the asset_key
    Then it writes one valuation_ext row against the valuation_key with stale_flag and age_days computed from the limit in force
    Then it copies no appraisal fact into rwb_valuation and joins no table of another schema
    Then the local decision record carries the rule ID and the rule version in the same transaction

  Scenario: AC4 A stale valuation product stops the step before the value is used (new, D-RCV-60)
    Given the v_ace_batch_status fixture shows the valuation product from an earlier date
    When the route assessment runs POST /cases/{caseId}/route
    Then the step stops with MSG-P1-001 naming the product and its date
    Then no valuation_ext row is written and no decision record is created
```

**Target reading.** AC2 is the legacy criterion, copied character for character; "the decision log" is the local `decision_record` written through RWB-PLT-E1027-CON in the same transaction as the row, and "nothing changes" is that one transaction rolling back (DP-03). AC3 and AC4 are new and test only the target read and row write; the values AP-0001, AST-0001, 4250000 and 2026-11-02 are the legacy story's own acceptance values, kept character for character, and no business value is added. AC3's read is the DP-05 second option — this service's own SELECT-only access to the ACE view — with `v_ace_batch_status` as the freshness source the FSD's VR-S1-002-1 names (ASM-4293). AC1 of the legacy story — the main success path — is the same read and row write; its acceptance text is not owned by this story and its test TC-E4-002-01 runs here (section 16). The row is one row per `valuation_key` and AC5's redelivered row is an update (section 9). The one operation sits on base `/api/recovery/valuation/v1` (DP-13) and SCR-13 reaches it through the gateway-bff composite route (DP-19).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The appraisal facts are read from `recovery.v_ace_valuation` for the `asset_key` and are never loaded by the Workbench and never copied into `rwb_valuation` | FSD S1 A2.2; D-RCV-35 U1 and U3; ADR-010; DP-05 |
| BR2 | The Workbench keeps its own decision about the appraisal — `accepted`, `accepted_at`, `accepted_by`, `stale_flag`, `age_days` and the valuer — in `valuation_ext` against the `valuation_key` | legacy RWB-E4-002 story and data; FSD S1 A2.4.3.2; DP-01 |
| BR3 | A stale data product stops the read: when `v_ace_batch_status` shows the valuation product from an earlier date, the step stops with MSG-P1-001 and nothing is written | VR-S1-002-1; FSD S1 A2.2.3.1 |
| BR4 | No value a business person may change is written in code: the age limit, the freshness limit, the lists and the rule version are values in force read with their version | BR-S1-002; FSD S1 A2.2.3.1 |
| BR5 | The result is recorded in the local decision record with the rule ID and the rule version in force, and a decision that cannot be recorded does not proceed | legacy RWB-E4-002 AC1 and AC2; DP-03; REQ-DRI-005 |
| BR6 | This service writes no case table, holds no case status and reads no table of another service: the case reaches it as a path identifier and the ACE data through the view | DP-01; ASM-4291 |
| BR7 | The route assessment needs right U in the capability area Treatment and offer; the check is the platform guard library's and no role list is written here | TSD S1 T6.1; legacy permission checks |
| BR8 | One `valuation_key` has one `valuation_ext` row; a redelivered ACE row updates it and a repeated request key returns the first answer | legacy RWB-E4-002 data; section 9 |
| BR9 | The acceptance of the value itself — the user act that fixes the band the route decision runs on — is FEAT-VAL-04's; this story writes the flags the receipt observes and the default the row carries at receipt | FSD S1 A2.4; GAP-2594; ASM-4295 |

**Where each rule lives in the target.** BR1 is the `AppraisalReadService` query on the view, with no repository for an appraisal table. BR2 and BR8 are `ValuationExtRepository` and the unique key on `valuation_key`. BR3 is the freshness gate in front of the read. BR4 is the reference-data reads and the Drools runtime of the service template. BR5 is the `DecisionRecordAdapter` and the one transaction. BR6 is the schema boundary and the absence of a cross-schema key. BR7 is the contract's `security` section and the guard library. BR9 draws the line to FEAT-VAL-04 in section 19 and is recorded with the assumption on the receipt default.

### 9. State transitions

No case status is owned here; the case is moved by `CaseWorkflow` on rwb-case. The only lifecycle this story writes is the `valuation_ext` row and its two flags.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| `valuation_ext` row | absent | the appraisal step runs | a row exists in `v_ace_valuation` for the asset_key and the product is fresh | row created with `stale_flag` false |
| `valuation_ext` row | absent, or present | the appraisal step runs | `appraisal_date` older than the age limit in force | row written with `stale_flag` true; the order path FEAT-VAL-01 takes it |
| `valuation_ext` row | present | the appraisal step runs again for the same `valuation_key` | a redelivered or re-read ACE row | same row updated; `version` and `updated_at` move, no second row |
| `valuation_ext` row | present | the case owner accepts the value | FEAT-VAL-04 runs | `accepted` true with `accepted_at` and `accepted_by`; not this story's write |
| `valuation_ext` row | absent | the appraisal step runs | no row in the view for the asset_key | stays absent; nothing is written |

The `state` column takes the standard record lifecycle of TSD S1 T3.0 and carries no business meaning in this story. The receipt itself has no workflow state: the step either commits its one transaction or writes nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-valuation squad, service identity of `rwb_valuation` | Runs the read and the row write on the case's behalf; holds SELECT on the two views only |
| RW-CASEOWN, case owner (right U) | Assesses the route of a case in scope and thereby triggers the receipt |
| RW-RESTRUCT, restructuring officer; RW-SPECIAL, hardship and vulnerability specialist; RW-GUARANT, guarantee officer (right U) | The same right in the same capability area, on the cases in scope |
| RW-TEAMMGR, RW-PRODHEAD, RW-CREDCOMM, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (right R) | Read the value, its flags and the age on SCR-13; they trigger nothing here |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities through the same checks |
| rwb-case (P3) | Owns the case, its status, `CaseWorkflow` and the case view SCR-13 composes |
| rwb-source-data (P1) | Owns the `recovery.v_ace_*` views and grants this service SELECT on the two it needs |
| ACE ingestion | Owns the SVAF feed and writes `v_ace_valuation`; the Workbench neither loads nor corrects it |
| rwb-decision (P7) | Owns the central ledger and the rule packages with their versions |
| rwb-access (P4) | Owns the roles, the rights and the scope data the guard answers with |
| No delegation of authority level applies | The story reads a value and records a decision about it; it approves nothing and moves no case |

No credential and no personal name appears in the request, the row, the workflow input, the record or the logs. The valuer is held as a partner reference (`valuer_partner_id`), never as a name.

### 11. Data

| BR Field ID | Entity | Fields | Read or write |
|---|---|---|---|
| DF-ACE-187 to DF-ACE-195 | `recovery.v_ace_valuation` (ACE data, view owned by rwb-source-data) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date and 3 more, as the legacy data row lists them | Read only, SELECT |
| DF-ACE-091 to DF-ACE-098 | `recovery.v_ace_collateral` (ACE data, view owned by rwb-source-data) | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and 2 more | Read only: the asset-to-collateral link of the case |
| `v_ace_batch_status` (no DF id in the legacy story) | `recovery.v_ace_batch_status` (view owned by rwb-source-data) | the product and its date | Read only: the freshness gate VR-S1-002-1 |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` in `rwb_valuation` | valuation_key, accepted, accepted_at, accepted_by, stale_flag, age_days and 8 more | Write on receipt: `stale_flag`, `age_days`, the valuer reference and the standard columns; `accepted_at` and `accepted_by` are FEAT-VAL-04's |
| DF-COL-026, DF-COL-027, DF-COL-043, DF-COL-044 | `valuation` in TSD S1 T3.1 | valuer_partner_id, accepted, stale_flag, age_days | The same Workbench columns under the TSD's table and field names; the story's `valuation_ext` is that row (GAP-2594; ASM-4295) |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (local, in `rwb_valuation`) and `decision_log_entry` (`rwb_decision`, owner P7) | all fields of the record | Write the local record through the library in the same transaction; the central ledger is sealed by P7 and never written here |
| DF-REF-001 to DF-REF-015 | `rule_row` (`rwb_decision`, owner P7) | the rule row of the receipt | Not read directly: the evaluated package returns the rule ID and version |

`valuation_ext` is the only table this story creates, and it is created with the field identifiers the legacy data row names — DF-EXT-036 to DF-EXT-049 — read as the TSD's valuation fields where the two name the same column. The view is not copied, no foreign key points into it, and no column of another service's table is joined (DP-01). The Ownership Map lists no table for S1, so the table is created here on the assumption that the map's S1 table row is incomplete (GAP-2594; ASM-4291).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the handler of the operation that reaches the read; its published shape, error set and fakes are declared by RWB-S1-E4002-CON.

| Method | Path | Request and response | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in, `Approval` out, with the elements of TSD S1 T-A.2; the answer carries the appraisal facts read from the view and the flags of `valuation_ext` | Treatment and offer U, scope applied, through the guard library | `Idempotency-Key` header required |

The errors are 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body; 403 carries MSG-P4-002, 404 carries the guard's not-in-scope answer, 422 carries MSG-GEN-001 with the field name, 503 carries MSG-GEN-006, and the cause of the 409 is Not specified in the source documents (GAP-2595; ASM-4295). The two asset valuation operations the S1 ownership rows carry are not declared here: they belong to the sibling valuation stories of this service and to their own contracts (ASM-4294).

#### 12.2 REST operations consumed

None. The ACE appraisal arrives through the view, not through a contract; the case arrives as the path identifier of the operation; the rule package arrives through the workflow's package read; the rights and the lists arrive through the template's client libraries. This story therefore adds no contract and no integration dependency of its own (ASM-4293).

#### 12.3 Events published

None. The service topic is `rwb.valuation.events.v1` with event names `rwb.valuation.<Event>.v1` (DP-14) and the ownership rows give S1 no event; this story writes no outbox row of its own beyond the `DecisionRecorded` row the library writes inside the transaction (DP-03).

#### 12.4 Events consumed

None. The FSD's trigger phrase "a completed ACE batch, an event or a timer" names no event and no job for S1, and the ownership rows show none; the batch leg is the freshness gate of section 4 step 3 (GAP-2594; ASM-4292).

#### 12.5 Workflows and activities

None. `RouteDecisionWorkflow` is the service's one workflow in the ownership rows and is neither created nor changed by this story; the read and the row write are service methods that the route assessment calls, and the workflow that runs the assessment is the route-decision story's. No activity is added on task queue `rwb-valuation`.

#### 12.6 Schedules

None. No Temporal Schedule and no legacy Quartz job is created: the receipt has no clock of its own, and the batch leg is asserted by the freshness gate rather than by a schedule (GAP-2594; ASM-4292).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `valuation_ext` | `rwb_valuation` | S1 | Created by this story's Flyway version; DF-EXT-036 to DF-EXT-049; one row per `valuation_key`; written on receipt |
| `decision_record` | `rwb_valuation` | PLT library object applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction (DP-03) |

The ACE views are read and never created, altered or copied, and no table of another service is named, read or keyed (DP-01, DP-05). The ownership rows list no table for S1 and the table is created here on the assumption of section 11 (GAP-2594; ASM-4291).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S1-E4002-CON route fake | `POST /cases/{caseId}/route` | An `Approval` answer carrying the appraisal facts and the flags; a 403, a 404, a 409, a 422 and a 503 answer; a repeated key answering the first result |
| RWB-PLT-E1027-CON writer fake | `DecisionRecordWriter.record` | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009; an unavailable store raising MSG-P7-003 |
| RWB-PLT-N001-CON composite-route fake | SCR-13 | The composed case read and valuation read in one hop each |
| `v_ace_valuation` and `v_ace_batch_status` fixtures | The read and the freshness gate | AP-0001 on AST-0001 with 4250000 at 2026-11-02; a product at the business date; a product from an earlier date; an asset with no appraisal row |

The view fixtures stand where ACE's own row would be and are test-only; they are recorded with GAP-2594 and ASM-4293.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation on `/api/recovery/valuation/v1` | 0 | OpenAPI 3.1; the browser reaches it through gateway-bff (DP-19) |
| Kafka | None | None | Own topic named, no event type of this key |
| Temporal | None | None | No workflow and no Schedule in this story |
| File | None | None | No SVAF file is read or written by the Workbench; ACE ingests the feed |
| SQL view | None | 3 views | SELECT-only on `v_ace_valuation`, `v_ace_collateral` and `v_ace_batch_status`, granted by rwb-source-data (DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, modules `appraisal` and `route`, with the published types in `...valuation.api`. Service base `/api/recovery/valuation/v1`, schema `rwb_valuation`, topic `rwb.valuation.events.v1`, task queue `rwb-valuation` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The service's own SELECT-only read of `v_ace_valuation`, `v_ace_collateral` and `v_ace_batch_status` | none |
| DP-13 | the monolith API base | `/api/recovery/valuation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is the pattern the story turns on: the appraisal is read where ACE keeps it, so the Workbench holds no copy and no load. DP-03 is the record of the decision about it, DP-13 the base of the one operation and DP-19 the only route SCR-13 uses. DP-01 stands behind sections 11 and 12.7 as the schema rule and adds no dependency; the Drools runtime, the guard, the inbox and the reference data are the service template's wave-0 capabilities.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteController` | Controller | The operation of 12.1, the validation, the problem body and the guard |
| `AppraisalReadService` | Service | Resolves the asset key of the case and reads the six appraisal facts from the view |
| `FreshnessGate` | Service | VR-S1-002-1 on `v_ace_batch_status` before any read is used |
| `AppraisalFlagService` | Service | Computes `stale_flag` and `age_days` from the appraisal date, the business date and the limit in force |
| `ValuationExtRepository` | Repository | One row per `valuation_key` in `rwb_valuation`; insert or update, never a second row |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with the rule ID and the rule version in the caller's transaction (DP-03) |
| `RouteAnswerAssembler` | Service | Builds the `Approval` answer with the facts read and the flags written |
| `Migrations` | Migration | `valuation_ext` on the per-service Flyway sequence, with no cross-schema key |

**Database.** `valuation_ext` is created with the standard columns of TSD S1 T3.0 — `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` — with the primary key on `id`, a unique key on `valuation_key`, an index on `asset_key`, `stale_flag` and `age_days` as TSD S1 T3.1 types them, and the valuer held as a cross reference. No foreign key points into the views and no column of another schema is named (DP-01).

**Configuration and reference data.** LOV-APPRAISAL and LOV-ROUTE are read as values in force with their version and no member is a constant (BR-S1-002). The age limit, the freshness limit and the receipt default of `accepted` are reference values; the last is the working read of ASM-4295. The capability area and the rights are rwb-access data and are declared, not implemented.

**Build steps**

1. The Flyway version with `valuation_ext`, its unique key and its standard columns (AC3).
2. `FreshnessGate` and its fixture, with MSG-P1-001 (AC4).
3. `AppraisalReadService` against the view fixtures, with no repository for an appraisal table (AC3).
4. `AppraisalFlagService` and the reference-data reads for the two limits (AC3).
5. `ValuationExtRepository` and `RouteAnswerAssembler` for the one operation (AC3).
6. `DecisionRecordAdapter` and the one transaction, with the rollback path (AC2).
7. Tests for AC2 to AC4 against the fakes of 12.8.

**Feature flag.** `rwb.valuation.receive-appraisal`.

**Done when.** The tests in section 16 pass, the RWB-S1-E4002-CON contract tests stay green, one synthetic assessment writes one `valuation_ext` row with its `decision_record` in the same transaction in SIT, a redelivered row updates the same row, a forced record failure leaves no row and no outbox row, a stale product writes nothing, and SCR-13 shows the value, the stale flag and the age through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. |
| MSG-P1-001 | The valuation product is stale for the business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The ACE view or the service is unavailable | {system} is not available. Your request is queued and will be retried. |

MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the three legacy texts carried unchanged. MSG-P1-001 is the freshness message the FSD gives VR-S1-002-1 and is carried with its placeholders. MSG-GEN-006 is the platform availability text. No message identifier is invented here, and no text is paraphrased. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | States | What this story puts on it |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The appraised value, its type, its date, the stale flag and the age of the appraisal for the asset of the case, read from the view and from `valuation_ext` |

The screen is served by the gateway-bff composite route, which composes the case read of rwb-case with the valuation read of this service, one hop each, read only (DP-19); the browser calls no owner service directly. The recommendation, the override and the submission states are the sibling stories'; the screen field list, the composite route specification and the layout belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-002-01 | AC1 | End to end | Receive the appraisal value from SVAF |
| TC-E4-002-02 | AC2 | End to end | Not recorded |
| TC-E4-002-03 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-002-04 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-S1-E4002-APP-01 | AC3 | Component | The view fixture of AP-0001 on AST-0001; one `valuation_ext` row, its flags, no copy and one record |
| TC-S1-E4002-APP-02 | AC4 | Component | The stale product fixture; MSG-P1-001; no row and no record |

The four legacy test case IDs, their Covers and their Data are kept in order and character for character. TC-E4-002-01 covers legacy AC1, whose own acceptance text is not owned by this story and whose read path is the one built here; TC-E4-002-02 is the criterion of section 7, TC-E4-002-03 the guard's published answer and TC-E4-002-04 the rollback of the one transaction. The `-ITG` copies of the four legacy cases belong to the wave 3 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the age limit, the freshness limit, the receipt default, the lists and the rule version are values in force read with their version (BR-S1-002).
- No personal data in logs, tests, workflow inputs or prompts: the request, the row, the record and the logs carry case IDs, asset keys, valuation keys, codes, dates and amounts only; the valuer is a partner reference, never a name.
- No read of another module's tables: the appraisal and the collateral come through the SELECT-only views, the rule through its package, and `rwb_valuation` holds no foreign key into another schema (DP-01, DP-05).
- ACE data only through the owner's contract or `v_ace_*`: this story uses the view and writes no ACE schema, and the ACE ingestion of the SVAF feed is not touched.
- No copy of the appraisal: no table, no column and no cache in `rwb_valuation` holds `appraised_value`, `appraisal_no` or `appraisal_date`.
- The decision record is written in the same transaction as the row, and a failed write rolls the whole call back with MSG-P7-003 (DP-03).
- The central ledger is never written or read here: `decision_log_entry` belongs to P7 and is reached only through the shared topic.
- An applied migration is never edited: a correction to `valuation_ext` is a new version on the service sequence.
- No right is re-implemented: the capability area and the right are declared, and the guard library answers.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None stated for FEAT-VAL-02 (GAP-2594; ASM-4295) | The FSD's requirement table carries no row for the receipt; REQ-S1-002 (a valuation that is an outlier against market and the last value is flagged before it is accepted) is the requirement that consumes this read | Business Requirements Program v5, section 5; FSD S1 Requirements served | FEAT-VAL-02 | D6 Route decision | VR-S1-002-1, BR-S1-002 | TC-E4-002-01 to TC-E4-002-04, TC-S1-E4002-APP-01, TC-S1-E4002-APP-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S1-E4002-CON | Contract | H: declares the operation, the `RouteRequest` and `Approval` shapes, the `valuation_ext` DDL template, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the row's record is written through in the same transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-13 |
| RWB-S1-E4001-APP, RWB-S1-E4003-APP, RWB-S1-E4004-APP | App development | Siblings: ordering a stale appraisal (FEAT-VAL-01), flagging outliers (FEAT-VAL-03) and accepting the value (FEAT-VAL-04) on the row this story writes |
| RWB-S1-E4005-APP, RWB-S1-E4007-APP, RWB-S1-E4008-APP | App development | Siblings: the COLLINS return by route, the route scoring and the approval inside the limit, which the assessment continues with |
| P1 rwb-source-data | App development | Owns the ACE views this story reads and grants the SELECT |
| P3 rwb-case | App development | Owns the case, its status and the case read SCR-13 composes |
| RWB-ITG-W3 | Integration | The cross-service proof of the read and the row against the live views and the live case, held by the wave 3 harness |

### 19. Out of scope

- The published shape of the operation, the `RouteRequest` and `Approval` schemas, the `valuation_ext` DDL template, the error set and the fakes: RWB-S1-E4002-CON.
- Ordering an appraisal when the last one is stale, and the SVAF order and its panel service level: FEAT-VAL-01.
- Flagging an outlier against market and the last value, and the flag a person reviews: FEAT-VAL-03.
- Accepting the value — `accepted`, `accepted_at` and `accepted_by` as a user act — and the band it fixes: FEAT-VAL-04.
- The COLLINS return by route, the payoff and the settlement range, the route recommendation, the approval inside the limit, the committee, the hold and the route flow: FEAT-VAL-05 to FEAT-VAL-12.
- The ACE ingestion of the SVAF feed, the SVAF order and the `v_ace_*` views themselves: ACE and rwb-source-data (P1).
- The case, its status, `CaseWorkflow` and the case view: rwb-case (P3).
- The central decision ledger and the rule packages: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-13: the platform edge story and the screen owners (DP-19).
- The valuation tables the TSD names without a field list for the receipt, and the receipt default of `accepted` (GAP-2594; ASM-4295).
- The two asset valuation operations of the S1 ownership rows, which belong to the sibling valuation keys (ASM-4294).
- The real cross-service proof of the read against the live views and the live case: the wave 3 integration harness.
- The deployment of this build: chart values, the schema and login, the view grants, the flag, dashboards and the runbook.
