# RWB-S9-E7011-APP Score partners monthly

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S9-M |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7011-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the scorecard slice of RWB-E7-011 is realigned onto rwb-partner (S9, service wave 4, business wave 4). The two legacy criteria of this key are kept word for word with their origin tag and only the two `Given the <service> contract mock returns <x>` lines are added. The monthly run becomes a scheduled activity set on task queue `rwb-partner`: it reads the ACE score rows of the accounts placed with each partner on the rwb-source-data contract (DP-05, the `v_ace_score` read of the legacy Data table), scores each partner against the rule set in force, writes one entry through the local decision-record library before any change (DP-03), and publishes the result on `partner.score` for the panel and SCR-36 through the gateway-bff composite route (DP-19) on base `/api/recovery/partner/v1` (DP-13). It declares no operation of its own, because the Ownership Map gives S9 six operations and all six belong to the instruction, result, invoice and panel stories; no event, because EV-20 and EV-21 carry an instruction and a result and no scorecard fact; and no Schedule, because the map gives S9 no job and one workflow. No rule row of the ten route sets names partner scoring, the monthly trigger has no source, the measures of SCR-36 have no published element, the Power BI integration point is gone with the data lake (DP-17), and the plan's C and H rows omit the two consumed reads and the workflow kit (GAP-3121; ASM-5414 to ASM-5421). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E7011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)** — and as the unattended run that takes the act where no person is waiting — I want **the Workbench to build every partner's monthly scorecard from its measured results and publish it to the panel**, so that **partners are placed, paid and measured by rule and every partner decision cites the rule version it was judged under**.

This story owns:

- the two legacy criteria of RWB-E7-011 (AC1 and AC2), copied verbatim with their origin tag, and the rule, message and screen behaviour they depend on;
- the monthly scorecard run as a scheduled activity set on task queue `rwb-partner` in namespace `rwb-recovery`: `collectMeasuredResults`, `evaluateScorecardRules`, `publishScorecard` (ASM-5415);
- the measured-result read: the instruction and result facts of this service (`partner_instruction`) paired with the ACE score rows of the same accounts on the rwb-source-data contract, one hop and 2 s, never a view and never an ACE table (DP-05; ASM-5414);
- the scorecard evaluation against the rule set in force, with its package version taken from the row and never written in code (ASM-5416);
- the record-first rule: one entry per partner per run, written through the local decision-record library **before** the score is published, with the partner, the period, the rule set and its version, and a failed write leaving everything unchanged with MSG-P7-003 (DP-03; legacy AC1 and AC2);
- the publication: `partner.score` carries the latest scorecard result and the panel sees it on SCR-34 and SCR-36 through the composite route (DP-19; ASM-5417);
- the stale-input guard: a data product whose ACE batch has not arrived refuses the run and names the product and its date (VR-S9-008-1, MSG-P1-001).

It does not own: the published shapes, the scorecard element, the consumed rows, the rights, the error set and the fakes (RWB-S9-E7011-CON); the panel, the fee schedule and their reference data (FEAT-PRM-02); the allocation and its override (FEAT-PRM-03 and FEAT-PRM-04); the receive of a partner result (FEAT-PRM-05); the agency fee matching and its approval (FEAT-PRM-07 and FEAT-PRM-09); the partner review, the notice and the contract end (FEAT-PRM-10 to FEAT-PRM-12); the ACE score data and its batch record (rwb-source-data P1); the rules and their versions (rwb-decision P7); the rights and the lists of values (rwb-access P4); and the schema, migration, schedule registration and deployment of this capability (the DB, OPS and INF stories of this key).

### 2. Business rationale

The objective, the problem and the metric are the module's and do not move: partners are instructed and paid by email and spreadsheet and allocation is not based on performance, and the metric is placements by scorecard, targeted at 100 percent, measured on the decision log and the Workbench records and reviewed monthly (FSD S9 A2.8.1). The requirement is REQ-S9-003, "Work is allocated to partners by measured return against a scorecard, not by a fixed share", with REQ-S9-007 for the performance data that reach the review forum and REQ-S9-001 for the six points every partner type is managed on (FSD S9 Requirements served; Program BRD v4).

A scorecard is only worth the paper it is written on if it is built from measured facts, recorded with its rule version and read from one place. What D-RCV-60 changes is who owns each fact of that scorecard:

- **The score is a partner fact of this service.** `partner.score` is DF-PRT-007, numeric(5,2), described in the published API as "Latest scorecard result", so the publication is one column of a table this service already owns (TSD S9 T3.1; ASM-5417).
- **The measured result is not.** The ACE score rows are `v_ace_score`, DF-ACE-270 to DF-ACE-279, read from ACE and owned by no Workbench service; the context pack and the architecture slides give the views to rwb-source-data, so this service reads them on that owner's contract and never as a table (DP-05; ASM-5414).
- **The decision is recorded.** Legacy AC1 asks for the result in the decision log with the rule version, legacy AC2 stops the action when the log cannot be written, and R-UNI-39 says the same in the rules ("Block the action and raise an incident. No action proceeds unlogged"). The entry is written through the local library in one transaction, before the score is published (DP-03).
- **The rule set is versioned, not constant.** BR-S9-008 forbids a value a business person may change from being written in code, and R-UNI-38 applies a new rule version from its effective date, so the run evaluates the version in force and stamps it on the entry (ASM-5416).
- **The report to the forum is not a data-lake feed.** The legacy integration point is Power BI; there is no data lake in Arch v5 and rwb-reporting builds its read model from events, while S9 publishes no scorecard event. The score therefore reaches the panel and the screens and nothing else, and the reporting path is a gap (DP-17; ASM-5418).

No business value moves: the partner types, the panel statuses, the instruction statuses and the scorecard rule rows stay reference data or rule rows read with their version.

### 3. Preconditions

- RWB-S9-E7011-CON is published and tagged: the scorecard element, the consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-36 and SCR-34 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The ACE score read of rwb-source-data is published with its fake: the score rows of the accounts placed with a partner, their `model_code`, `model_version`, `score_value`, `estimate_value`, `route_code`, `scored_at` and `data_as_of`. Its operation name is Not specified in the source documents (GAP-3121; ASM-5414).
- `partner` and `partner_instruction` exist in `rwb_partner` from the DB story of this service with the columns of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; at least one partner is `ACTIVE` on the panel with instructions in `DONE` (TSD S9 T3.1, T3.2).
- The scorecard rule set is in force at its version and arrives loaded; it is authored, tested and approved in rwb-decision (P7) and names the measures of the scorecard (ASM-5416).
- The monthly trigger is available as a Temporal Schedule of the workflow platform, or the run can be started by hand through the same entry point; the Ownership Map gives S9 no job, so no Quartz row and no shared job table is created (ASM-5415).
- The lists of values this run reads — `LOV-PARTNER-TYPE` with AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED, and `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED — are reference data with their version and never written in code (TSD S9 T3.2).
- The run sees the ACE batch status of the score product through rwb-source-data, so a stale product is refused before any read of scores (VR-S9-008-1; ASM-5420).
- The service runs as its own login on `rwb_partner` and holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, on `rwb_source_data` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7011-CON when its tests pass.

### 4. Flow

1. The monthly schedule fires at the cut-off, or a member of the partner and agency manager role starts the run by hand with the same period; the run takes the business date of the ACE score product as its period (ASM-5415).
2. `collectMeasuredResults` reads the ACE batch status of the score product first. A stale or missing batch refuses the run with MSG-P1-001 and nothing is read or written (VR-S9-008-1).
3. The activity reads the partners on the panel from `rwb_partner` — code, type, panel status, contract end — and the instruction facts of each: `status`, `result_code`, `instructed_at` and `due_at` (DF-PRT-002 to DF-PRT-016).
4. It reads the ACE score rows of the same accounts from rwb-source-data, one hop and 2 s, as `model_code`, `model_version`, `score_value`, `estimate_value`, `route_code`, `scored_at` and `data_as_of` (DP-05; ASM-5414).
5. `evaluateScorecardRules` loads the scorecard rule set in force for the period and evaluates the measures over the paired facts: the worked instructions and their outcomes beside the ACE score of the same accounts. Where a partner has no measured result in the period, the run records that fact and evaluates it as the rule set says, and never substitutes a default (ASM-5416).
6. The run writes one entry through the local library **before any other effect**: the partner, the period, the measures with their values, the rule set and its package version, and the score. A failed write stops the run with nothing changed and MSG-P7-003 (DP-03; legacy AC1 and AC2).
7. `publishScorecard` writes the score to `partner.score` in the same transaction as the entry's outcome, sets `updated_at` and `updated_by` to the service identity, and leaves every other column of the row as it was (DF-PRT-007; ASM-5417).
8. The panel sees the result: SCR-36 shows the monthly score per partner against its measures and SCR-34 shows the score beside the panel status and the contract end, both read only, both through the composite route (DP-19; ASM-5419).
9. A partner whose panel status is `EXITED` or whose contract has ended keeps its last score and is not re-scored; the recall of its work is R-UNI-26's and not this story's (ASM-5417).
10. A repeat run for the same period is idempotent: one entry per partner and period, and the repeat answers the entry it already wrote without writing a second score or a second entry (ASM-5421).
11. The run ends and reports its counts: partners scored, partners with no measured result, and the rule set version applied.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no score, no entry, no report; the partner row keeps its previous score | MSG-P7-003 | AC2, TC-E7-011-02, TC-E7-011-04 |
| X2 | A caller without the Partner portal right starts the run by hand | 403 before any read of scores and before any record; the scheduled run runs under the service identity with the same check | MSG-P4-002 | TC-E7-011-03 |
| X3 | A required value is absent or invalid: no period, no partner code, no partner type or no panel status | The run refuses that partner, writes nothing for it and names the field | MSG-GEN-001 | AC1 |
| X4 | The data product is stale: the ACE batch for the score product has not arrived | The run refuses with nothing read and nothing written, and names the product and its date | MSG-P1-001 (VR-S9-008-1) | AC1 |
| X5 | The ACE score read does not answer inside 2 s, or its breaker is open | The run stops for that partner, retries on the workflow's own schedule and writes nothing; the caller sees the platform 503 envelope | None (platform envelope) | AC1 |
| X6 | A partner has no measured result in the period | The partner is scored on the facts that exist and the absence is recorded on the entry; no default, no zero and no carried-forward value is invented | None | AC1 |
| X7 | The same period is run twice | One entry and one score per partner and period; the repeat answers the entry that exists | None | AC1 |
| X8 | The rule set has no version in force for the period | The run waits, no score is published and the partner rows are unchanged; no score is taken on an unversioned rule set | None | AC1 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_source_data` row, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6 |

X1 and X2 are the legacy not-recorded and access paths of this key carried onto the slice; X3 to X8 are the paths the score read, the stale product and the unattended run add; X9 is the schema and ACE boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7011-CON, the decision-record stub, the score-read fake and the gateway-bff fake, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity names, the pairing rule between instruction and score and the shape of the entry are this story's choice; the rules, the messages, the screens, the score column and the period are fixed |
| Valuable | Every partner's month is scored from measured facts, recorded with its rule version and published once to the panel and to SCR-36 |
| Estimable | One scheduled activity set, three activities, one record write, one column write, two clients and one read-only screen pair |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic partners through the contract fakes, plus the stale product, the missing result, the refused-right, the repeat and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Score partners monthly

  Background:
    Given the scorecard rule set is in force at its version and is answered by its fake
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Score partners monthly (legacy RWB-E7-011 AC1)
    Given the rwb-source-data contract mock returns the ACE score rows of partner "AG-2026-0034" scored on "2026-11-30" at model_version "2026-11"
    Given the rwb-decision contract mock returns the partner scorecard rule set at version "SC-2026-11"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the scorecard from the measured results and publishes it to the panel
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E7-011 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E7-011 word for word, with their origin tag added and nothing else changed: the `Then builds the scorecard…` line keeps its missing subject, `its trigger arrives`, `publishes it to the panel` and `the decision log cannot be written` all stand. AC1's cross-service parts are mocked, so it carries the two `Given the <service> contract mock returns <x>` lines, and those are the only additions; AC2 has no cross-service part and is copied with nothing added. On this story "its trigger" is the monthly cut-off of the scorecard run, "the panel" is the partner panel behind SCR-36 and SCR-34, and "the action" is the publication of the score when the record cannot be written. What the legacy lines describe now happens in three places: rwb-source-data holds the ACE score rows, rwb-partner evaluates and records, and rwb-decision holds the rule set and the central ledger. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the `decision_log_entry` ledger of rwb-decision behind it. The partner code, the model version and the rule set version in the mock lines are synthetic test data and no source value (section 16).

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-25 | Universal rules | All | ANY_ACTIVE | PARTNER_NO_RESPONSE | the partner misses the service level on the portal | Chase once, then recall the work and re-select on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | per partner type |
| R-UNI-27 | Universal rules | All | ANY_ACTIVE | PARTNER_CONFLICT_DECLARED | the partner declares a conflict of interest | Withdraw the instruction, re-select the next partner on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | 2 working days |
| R-UNI-38 | Universal rules | All | ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date | Apply it to decisions taken from that date. Open cases keep the version they were decided under | RESUME_STATE | Center of excellence | Workbench | on the effective date |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-UNI-40 | Universal rules | All | ANY_ACTIVE | DUPLICATE_EVENT | the same event arrives twice with the same key | Ignore the second event, record the idempotency hit | RESUME_STATE | Workbench | Workbench | None |
| R-UNI-45 | Universal rules | All | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Partner and agency manager | Partner Portal | 2 working days |

The six rows are the rows of the Business Rules and Routing Logic v4, copied character for character. This story evaluates R-UNI-38 for the version it stamps and R-UNI-39 for the record-first rule, reads R-UNI-40 for the repeat of a run, and reads R-UNI-25, R-UNI-27 and R-UNI-45 as the rules that consume its score and never fires them. Their owner column names a business role and a system, not a service: "Partner Portal" is this service and its screens, and "Workbench" in R-UNI-38 to R-UNI-40 is the Workbench platform. No rule row of the ten route sets names partner scoring itself (GAP-3121; ASM-5416).

| ID | Rule | Source |
|---|---|---|
| BR1 | The scorecard is a decision first: one entry per partner and period is written through the local library, with the partner, the period, the measures, the rule set and its package version, and a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy AC1 and AC2 |
| BR2 | The measured result is read, the score is written: the ACE score rows are rwb-source-data's and are consumed one hop on its contract, and the result is published on `partner.score` (DF-PRT-007), a column this service already owns | Context pack ownership rows; LDM v8 DF-ACE-270 to DF-ACE-279 and DF-PRT-007; DP-01, DP-05 |
| BR3 | The run scores the partners on the panel and skips nothing silently: a partner with no measured result in the period is scored on the facts that exist and the absence is recorded; `EXITED` partners and ended contracts are not re-scored | FSD S9 A2.8.2 and A2.8.3.1; TSD S9 T3.2 LOV-PANEL |
| BR4 | A stale data product refuses the run before any read: the ACE batch status of the score product is checked first and the message names the product and its date | VR-S9-008-1, MSG-P1-001; FSD S9 A2.8.3.1 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers of other services' facts and the ACE score rows never land in this schema | DP-01; TSD S9 T3.3 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the score product arrives as published rows with their own `data_as_of` | DP-05, DP-11; TSD S9 T5.2.3 (SQL provided 0, consumed 0); ASM-5414 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: the scorecard rule set, the measures, the partner types, the panel statuses and the instruction statuses | FSD S9 A2.8.3.1 (BR-S9-008); legacy Guardrails |
| BR8 | The run is idempotent per partner and period: one entry, one score and one publication, and a repeat answers the entry that exists | R-UNI-40 read; TSD S9 T2; ASM-5421 |
| BR9 | No person name, contact value, address or identity number enters `rwb_partner`, the entry, a log or a workflow input; the partner code, the period and the score are the only facts published | Template and Rules §R7.2 (s17); LDM v8 |

### 9. State transitions

The case route state, the instruction state machine of `LOV-INSTR-STATUS` and the panel status of `LOV-PANEL` are not moved by this story: the run reads them and writes none of them (BR3).

| From (`partner.panel_status`, read) | The run | Condition | What this story writes |
|---|---|---|---|
| `ACTIVE` | Re-scored for the period | Measured results exist | One entry and one `score` |
| `ACTIVE` | Re-scored for the period | No measured result in the period | One entry that records the absence and the score the rule set gives |
| `ON_NOTICE` | Re-scored for the period | The contract has not ended | One entry and one `score`, because the partner is still placed with work |
| `SUSPENDED` | Not scored | Allocation is suspended and no new work is placed | Nothing; the previous score stands and the reason is recorded in the run report |
| `EXITED` | Not scored | The partner has left the panel | Nothing; the recall of its work is R-UNI-26's |
| Any | Contract end before the period | `contract_end` is before the cut-off date | Nothing; the partner is not re-scored |

| Run step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The monthly cut-off arrives, or the run is started by hand | The period is taken from the score product | Checking |
| Checking | The ACE batch status is read | The product is current | Reading |
| Checking | The product is stale or missing | X4 | Closed, nothing read, MSG-P1-001 |
| Reading | The partners, the instructions and the score rows are read | At least one partner is scored | Evaluating |
| Evaluating | The rule set in force is applied | The version is found | Recording |
| Evaluating | No version is in force | X8 | Waiting, nothing written |
| Recording | The entry is written | The transaction commits | Publishing |
| Recording | The entry write fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Publishing | `partner.score` is written | The same transaction commits | Done |

The run states are its own and no state value of the case, of an instruction or of the panel is added by this story (ASM-5415).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner and agency manager (RW-AGENCYMG) | The "also uses" role of FSD S9 A2.8.3.3 and the only role with CRUDA on Partner portal in TSD S9 T6.1: reads SCR-36 and SCR-34 and may start a run by hand |
| The unattended run (rwb-partner service identity) | The primary actor of FSD S9 A2.8.3.3, "None; runs unattended": takes the act on the platform schedule under the service identity and holds no user right of its own |
| Case owner, team manager, litigation officer, enforcement owner, legal counsel, sale officer, NPA and asset manager, debt sale officer, guarantee officer (R or CRU on Partner portal) | Read the scorecard on both screens; they may not start a run |
| Partner-type users (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC: RU) | Read their own firm's score on the partner portal, scoped to their firm |
| Conduct and QA officer, compliance and PDPA officer, internal audit, risk and model risk officer (R) | Read the scorecard and the entry behind it for assurance |
| rwb-source-data (P1) | Owns the ACE score rows and their batch status; this story reads them on its contract |
| rwb-decision (P7) | Owns the scorecard rule set, its versions and the central ledger; this story evaluates them and records locally |
| rwb-access (P4) | Owns the roles, the capability rights and the lists of values this story reads through the guard |

No delegated authority limit applies: a scorecard approves nothing and pays nothing, and the only approval in the module is the fee approval of FEAT-PRM-09, which is not this story's.

### 11. Data

| BR Field ID | Entity | Owner | Use in this story |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | `partner` | S9, `rwb_partner` | **Read** code, name, type, panel status and contract end; **Write** `score` (DF-PRT-007, numeric(5,2)) with `updated_at` and `updated_by` only (ASM-5417) |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | S9, `rwb_partner` | **Read** only: `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code` and `fee_amount` as the measured work of the partner |
| None: library table | `decision_record` | Platform library in `rwb_partner` | **Write**: one hash-linked entry per partner and period, before anything else (DP-03) |
| None: library table | `idempotency_key` | Platform library in `rwb_partner` | The partner-and-period key and the outcome it holds |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` | ACE, read on P1 rwb-source-data's contract | Not read as a view and not landed here: the score rows arrive on the owner's contract with `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value`, `route_code`, `scored_at`, `source_system` and `data_as_of` (ASM-5414) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | Not written: the local entry is copied to the central ledger by its owner, and its identifier is not stored here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | Not read as a table: the scorecard rule set arrives loaded at its version in force (ASM-5416) |
| `LOV-PARTNER-TYPE`, `LOV-PANEL`, `LOV-INSTR-STATUS` | reference data and lists of values | P3 rwb-case (default ruling) | Read at their version; the values are those of TSD S9 T3.2 and none is added |

No new table, no new column and no migration: `partner` and `partner_instruction` arrive with the DB story of this service, `score` already exists, and `decision_record` and `idempotency_key` are library objects created in `rwb_partner` by the library's own migration (DP-03, DP-15). A scorecard table of one row per partner and month is not declared, because no source gives it and the entry carries the period (ASM-5417).

**No personal data.** The entry carries a partner code, a period, measures, a score, a rule version and a state. No name, address, contact value or identity number enters `rwb_partner`, the entry, a log or a workflow input; the ACE score rows carry an account key and a score, never a customer identity (BR9).

### 12. Contract

#### 12.1 REST operations provided

None owned. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The Ownership Map gives this service six operations and the published file `rwb-partner.yaml` names them: `GET /partners` (API-S9-001, Partner portal R), `POST /cases/{caseId}/instructions` (API-S9-002, C), `GET /partner/instructions` (API-S9-003, R), `POST /partner/instructions/{instructionId}/accept` (API-S9-004, U), `POST /partner/instructions/{instructionId}/results` (API-S9-005, U) and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006, C). All six belong to the panel, instruction, result and invoice stories of this service; the scorecard run is unattended and answers no screen request. The monthly score per partner against its measures is read on SCR-36 and has no operation of its own: it is Not specified in the source documents and carries the placeholder (GAP-3121; ASM-5419). A build that declares a scorecard write operation here fails the absence test of RWB-S9-E7011-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the ACE score rows of the accounts placed with a partner, and of the score product's batch status; operation name Not specified in the source documents (GAP-3121; ASM-5414) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The measured result of the partner: `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value`, `route_code`, `scored_at` and `data_as_of` (DF-ACE-270 to DF-ACE-279), and the batch status that guards the run (VR-S9-008-1); read only, faked |
| The read of the scorecard rule set in force with its package version; operation name Not specified in the source documents (GAP-3121; ASM-5416) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule rows and the package version the run applies and stamps on its entry (DF-REF-001 to DF-REF-015); read only, faked |

Both rows are one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). Both are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3121; ASM-5414, ASM-5416).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` and its event set is `InstructionIssued` (`rwb.partner.InstructionIssued.v1`, EV-20: `instructionId`, `partnerId`, `type`, `dueOn`) and `PartnerResultSubmitted` (`rwb.partner.PartnerResultSubmitted.v1`, EV-21: `instructionId`, `result`, `documents`), both of which belong to the instruction and the result stories of this service (Event and Messaging Design v5 EV-20 and EV-21; TSD S9 T5.2.1 and T5.3). A scorecard publishes no instruction and submits no result, and no catalogue row carries a score fact, so this story declares no producer group, no envelope and no outbox row, and RWB-S9-E7011-CON fails a build that adds one (ASM-5418).

#### 12.4 Events consumed

None. TSD S9 T5.2.2 states "Events this service consumes: None", and the Ownership Map gives S9 no consumed event. The monthly cut-off is the platform schedule of DP-10 and not a Kafka subscription, the score rows are read on a REST contract, and `AceDataReady` (EV-26) is consumed by case creation, reconciliation, payment matching, booking confirmation and the write-off scan and names no scorecard run (Event and Messaging Design v4 EV-26; ASM-5415).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ScorecardRun` | Scheduled activity set, one execution per period | `rwb-partner` in namespace `rwb-recovery` | The run from the cut-off or a manual start to the entry and the published score; its input is the period and its outcome the run report |
| `collectMeasuredResults` | Activity | `rwb-partner` | The batch-status check, the partners and instructions of this schema, and the score rows of rwb-source-data; the paired facts out |
| `evaluateScorecardRules` | Activity | `rwb-partner` | The scorecard rule set in force in; the measures, the score and the package version out |
| `publishScorecard` | Activity | `rwb-partner` | The entry, the `partner.score` write and the run report out, one transaction |

The run adds no workflow to the service: the Ownership Map gives S9 one workflow, `InstructionWorkflow`, and the scorecard does not extend it, because an instruction workflow is one instruction's SLA clock and outlives the month. The activity and run names are a target design choice fixed by no source document (ASM-5415).

#### 12.6 Schedules

None owned. The Ownership Map gives S9 no job (context pack ownership rows, Jobs: 0) and FSD S9 A2.8.4.4 declares "No background event", while FSD S9 A2.8.2 says the run receives "a completed ACE batch, an event or a timer" without choosing one. The monthly cut-off is therefore bound to the platform scheduling of DP-10 — a Temporal Schedule on queue `rwb-partner` — and its registration belongs to RWB-PLT-E1071 and to the OPS story of this key; the trigger itself is Not specified in the source documents (GAP-3121; ASM-5415). DP-10 is not in this key's pattern set, and the plan's H row omits `RWB-PLT-E1071-CON`.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `partner` | S9, `rwb_partner` | The partner of the panel; this story writes `score` and no other column |
| `partner_instruction` | S9, `rwb_partner` | The measured work placed with the partner; read only here |
| `partner_user` | S9, `rwb_partner` | The partner's portal users; not touched by this story |
| `decision_record` | Platform library in `rwb_partner` | The local hash-linked scorecard entry (DP-03) |
| `idempotency_key` | Platform library in `rwb_partner` | The partner-and-period key and the outcome it holds |

Not owned and never read as a table: `recovery_case`, `queue`, `assignment` and `timer` (P3), `interaction` and every `v_ace_*` view (P1), `rule_row` and `decision_log_entry` (P7), `document` (P5), and `invoice` and `notice` as their stories place them. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data score-read fake | The ACE score rows of partner `AG-2026-0034` scored on `2026-11-30` at `model_version` 2026-11 with `score_value` and `estimate_value`; the same rows with `data_as_of` 2026-10-31; a stale batch status; a partner with no rows; no answer inside 2 s; the operation name carries the placeholder (GAP-3121; ASM-5414) | AC1, X4, X5, X6 |
| rwb-decision rule-set fake | The scorecard rule set at version `SC-2026-11` with its measures, and a package with no version in force | AC1, X8 |
| rwb-partner partner fake | `AG-2026-0034` at `ACTIVE`, at `ON_NOTICE`, at `SUSPENDED` and at `EXITED`, and a partner whose contract ended before the cut-off | AC1, section 9 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC1, AC2, X1 |
| gateway-bff composite route fake | The merged SCR-36 and SCR-34 answer for the partners, with the scorecard slice of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The score-read operation name is a placeholder until rwb-source-data publishes it (GAP-3121; ASM-5414).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The ACE score read and the batch status of rwb-source-data, and the rule set of rwb-decision; one hop, 2 s each |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the instruction and result stories; the decision record rides the library's shared `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 scheduled activity set, 3 activities | `ScorecardRun` with `collectMeasuredResults`, `evaluateScorecardRules` and `publishScorecard` on `rwb-partner`; no workflow of its own and no Schedule registered here |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `scorecard`; front end `src/modules/recovery/partner/PartnerScorecard.tsx`, the SCR-36 fragment this story answers, read only.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the run: the entry commits before the score is published, and a failed write leaves the partner row as it was. DP-05 is how the ACE score of the legacy Data table reaches the run — on rwb-source-data's contract, because the views are read only by that service. DP-13 fixes the base of the service and gives the scorecard no element of its own, because all six operations belong to other stories. DP-19 is how SCR-36 and SCR-34 reach this service, one hop through the gateway. Two patterns the plan does not carry are real dependencies here and are recorded rather than added: DP-10, the monthly schedule (ASM-5415), and DP-04, the rule set loaded at its version (ASM-5416). DP-09 is absent and rightly so, because this step publishes nothing (ASM-5418).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ScorecardRun` | Scheduled activity set | Takes the period, applies the idempotency key, sequences the three activities and reports the run |
| `collectMeasuredResults` | Activity | Checks the batch status, reads the partners and instructions of this schema and the score rows of rwb-source-data, and pairs them by account |
| `evaluateScorecardRules` | Activity | Applies the scorecard rule set in force, computes the measures and the score, and returns the package version |
| `publishScorecard` | Activity | Writes the entry and `partner.score` in one transaction and returns the run report |
| `ScorecardEntryWriter` | Library adapter | Writes the hash-linked entry before any other effect and refuses the run when the write fails |
| `MeasuredResultClient` | Client | The score read of rwb-source-data, one hop, 2 s, breaker, no retry of its own |
| `PartnerReader` / `InstructionReader` | Repository | The panel partners and their instruction facts, read on this schema |
| `PartnerScorecard` | React component | Shows the monthly score against its measures on SCR-36, and the score beside the panel status on SCR-34, read only |

**Database and migrations.** No Flyway file. `partner` and `partner_instruction` arrive with the DB story of this service, `score` already exists on `partner`, and `decision_record` and `idempotency_key` are library objects created in `rwb_partner` by the library's migration (DP-03, DP-15). No measure is stored as a column: the entry carries the period and the measures (ASM-5417).

**Configuration and reference data.**

- The scorecard rule set and its measures: rule rows of rwb-decision read at their version (ASM-5416).
- `LOV-PARTNER-TYPE`, `LOV-PANEL` and `LOV-INSTR-STATUS`: reference data with their version, never a constant (TSD S9 T3.2).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The `ScorecardRun` entry point on `rwb-partner` with its period input, its idempotency key and the manual start behind the guard (AC1, X2).
2. `MeasuredResultClient` against its fake, with the 2 s budget, the breaker, the stale batch status and the unavailable path (AC1, X4, X5).
3. `PartnerReader` and `InstructionReader`, and the pairing of instruction facts with score rows, with the no-result path (AC1, X6).
4. `evaluateScorecardRules` over the rule set in force, with the version stamped and the unversioned-package path (AC1, X8).
5. `ScorecardEntryWriter` against the stub, with the failed-write path and MSG-P7-003 (AC2, X1).
6. `publishScorecard` with the `partner.score` write and the repeat path (AC1, X7).
7. The read-only scorecard fragment of `PartnerScorecard` on SCR-36 and SCR-34 through the composite route fake (AC1).
8. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read and no `rwb_case` read (X9, BR5, BR6).

**Feature flag.** `rwb.partner.monthly-scorecard-v1`, a flag of the platform library; off means the run ends without an entry and without a score, the screens show the last published score, and the instruction and result flows are unaffected.

**Done when.** The tests of section 16 pass, the run scores a synthetic panel in SIT, the entry carries its rule version, a stale product and a partner with no result open nothing and change nothing, a repeated period writes once, a forced entry failure leaves the score unchanged, no `v_ace_*` read and no foreign schema read exists in the build, and SCR-36 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the run is absent or invalid, for example no period, no partner code or no panel status (X3) | Enter {field}. |
| MSG-P1-001 | The score product is stale: the ACE batch for its source has not arrived, so the run is refused before any read (X4, VR-S9-008-1) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the Partner portal right starts the run by hand (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The scorecard entry cannot be written before the score is published (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The first, third and fourth IDs are those of the legacy message set of this key; MSG-P1-001 is the message VR-S9-008-1 gives the stale product. The text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded and no new one is added. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-36 Partner scorecard | Loading; scored | The monthly score per partner against its measures, with the period and the rule version, read only |
| SCR-34 Partner list | Loading; list | The partner with its panel status, contract end and latest score beside them, read only |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case and its owner and rwb-decision for the decision records; this story fixes only its own scorecard answer, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5419). The measures that SCR-36 plots are a placeholder, because no source publishes their element (GAP-3121). The stale, refused, not-recorded and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-011-01 | AC1 | Component | The synthetic panel partner `AG-2026-0034` with instructions in `DONE` and ACE score rows scored on `2026-11-30`; one entry, one score on `partner.score` and the rule version `SC-2026-11` asserted |
| TC-E7-011-02 | AC2 | Component | The decision-record stub stopped; no entry, no score and MSG-P7-003, and the partner row keeps its previous score |
| TC-E7-011-03 | AC2, X2 | Component | A role without the Partner portal right starting the run, and the unattended identity taking the same act; 403 with MSG-P4-002 and no score read |
| TC-E7-011-04 | AC2, X1 | Component | A forced decision-record write failure stops the run with MSG-P7-003 and leaves `partner.score` unchanged |

The four IDs are the legacy cases of RWB-E7-011 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`, and the legacy level `System` maps to `Component` because the artefact under test is the run against its contract fakes. The stale product, the no-result partner, the repeat and the unversioned-package paths are covered inside TC-E7-011-01 and by the new contract cases of RWB-S9-E7011-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the scorecard rule set, its measures, the partner types, the panel statuses and the instruction statuses stay rule rows or reference data read with their version.
- No personal data in `rwb_partner`, in an entry, a workflow input, a log or a prompt: a partner code, a period, measures, a score, a rule version and a state only.
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no other service's schema (BR5, BR6).
- The case, its route state, its instructions and their clocks stay with their owners: this story writes no case row, no timer row and no instruction row (BR3).
- One base, one topic, one queue and one login per service; this story adds no second topic, no event, no workflow and no registered Schedule (DP-13, DP-14).
- The record is written before the change and in its transaction; a failure leaves nothing behind (DP-03, R-UNI-39).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no `recovery_log` write and no data-lake path (DP-17).
- The run is unattended and holds no user right; a build that lets it act with a person's right fails the access test.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard, not by a fixed share (Must, E6) | The monthly scorecard, its entry and the published score | TC-E7-011-01, TC-E7-011-02 |
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum (Must, E7) | The measures recorded on the entry with their rule version | TC-E7-011-01 |
| REQ-S9-001 | Every partner type is managed on the same six points, including targets and incentives and performance reviews (Must, E6) | The scorecard as the performance point of every partner type | TC-E7-011-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the panel and the scorecard | TC-E7-011-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E7-011-01 |
| ADR-018 | No data lake; rwb-reporting read model from events | No Power BI feed from this service, and the scorecard event absence | TC-E7-011-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-E7-011-01 |
| ADR-022 | Local decision record plus central ledger | The scorecard entry written before the score | TC-E7-011-02, TC-E7-011-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-011, disposition Split (rework); feature FEAT-PRM-08 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Source text | Legacy RWB-E7-011; FSD S9 Partner management v4 A2.8 and Requirements served; TSD S9 Partner management v3 T0.1 to T0.4, T2, T3.0 to T3.3, T5.2, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-UNI-25, R-UNI-27, R-UNI-38 to R-UNI-40 and R-UNI-45; LDM and Data Dictionary v8 `partner`, `v_ace_score` and `rule_row`; Event and Messaging Design v5 EV-20, EV-21 and EV-26; Epics 3 to 8 Specification v3 FEAT-PRM-08 |
| Test cases | TC-E7-011-01 to TC-E7-011-04 |
| Feature and screens | FEAT-PRM-08, SCR-36 Partner scorecard and SCR-34 Partner list |
| Rules | R-UNI-38 and R-UNI-39 evaluated; R-UNI-25, R-UNI-27, R-UNI-40 and R-UNI-45 read |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-018, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the scorecard element, the consumed rows, the rights, the error set and the fakes: RWB-S9-E7011-CON.
- The panel, the fee schedule and their reference data: FEAT-PRM-02 and RWB-S9-E7002 (the panel story of this service).
- The allocation of work by measured return, and its override: FEAT-PRM-03 and FEAT-PRM-04.
- The receive of a partner result onto the case: FEAT-PRM-05.
- The agency fee matching and the fee approval: FEAT-PRM-07 and FEAT-PRM-09.
- The partner review, the notice on a missed target and the contract end with the work recall: FEAT-PRM-10, FEAT-PRM-11 and FEAT-PRM-12.
- The conduct check of partner contacts and complaints: FEAT-PRM-13.
- The ACE score rows, their batch record and their data product: rwb-source-data (P1), whose operation name this story does not publish.
- The scorecard rule set, its versions, the central ledger and the review target: rwb-decision (P7) and the registers (ASM-5416).
- The gateway-bff composite route and the screen field list of SCR-36: RWB-PLT-N001-CON and the edge stories.
- The reporting read model of the scorecard, which no event carries: rwb-reporting (P9) and the register row (GAP-3121; ASM-5418).
- The registration of the monthly schedule, the deployment of this capability, its flag, its dashboards, its alerts and its runbook: the OPS and INF stories of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
