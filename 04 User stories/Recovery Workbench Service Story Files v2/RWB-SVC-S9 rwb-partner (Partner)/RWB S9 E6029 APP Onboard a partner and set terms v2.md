# RWB-S9-E6029-APP Onboard a partner and set terms

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6029-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-F |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E6029-APP-16) |
| Contract version | 5.0.0 (rwb-partner.yaml, API Specification v5, info version) |
| Depends on (build) | RWB-S9-E6029-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | Partner gateway |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the onboarding slice of RWB-E6-029 in rwb-partner. Legacy AC2 is kept word for word; the command writes one `partner` row in `rwb_partner`, records the decision first (DP-03), serves API-S9-001 on `/api/recovery/partner/v1` (DP-13) and answers SCR-34 and SCR-35 through the gateway-bff composite route (DP-19). AC1 is RWB-ITG-E6029-ITG's. The write has no published operation, `partner_user` has no published field list and no field links a partner to its terms; all three are recorded as gaps and assumptions. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E6029-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 16 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)**, I want **to take a partner onto the panel with its contract, fee schedule, service levels and scope**, so that **partners are placed, paid and measured by rule**.

This is the onboarding slice of legacy RWB-E6-029 (FSD S9 A2.1, FEAT-PRM-01). It owns:

- AC2 of the key, verbatim with its origin tag, and the two exception paths the FSD publishes for the feature;
- the command behind the panel: VR-S9-001-1, the uniqueness of `partner_code`, the type, panel status and contract end, as one `partner` row within DF-PRT-001 to DF-PRT-007 (§11);
- the portal user of the firm in `partner_user`, the third table of S9, where access is requested (ASM-5343);
- the decision record, written before the row changes (DP-03; legacy AC2);
- the panel read API-S9-001 `GET /partners` and the served states of SCR-34 and SCR-35 (DP-13, DP-19);
- the read of `LOV-PANEL` and `LOV-PARTNER-TYPE` with their version, so no value is a constant (ASM-5345).

It does not own: AC1 and its cross-service evidence (RWB-ITG-E6029-ITG); the shape of the write and the read, the `Partner` element, the rights, the error set and the fakes (RWB-S9-E6029-CON); the panel and fee schedule as reference data (RWB-S9-E6030-APP) and the sibling stories of FEAT-PRM-03 to FEAT-PRM-15; the case and its states (rwb-case, P3); documents (P5); access (P4); the partner gateway of the edge; and the deployment of this build.

### 2. Business rationale

The objective, the problem and the metric are unchanged: the feature takes a partner onto the panel with its contract, fee schedule, service levels and scope (FSD S9 A2.1.1), because "Partners are instructed and paid by email and spreadsheet; allocation is not based on performance" (FSD S9 A1.3), and the measure is "Placements by scorecard | 100 percent | Decision log and Workbench records | Monthly". The requirements served are REQ-S9-001 to REQ-S9-004 and REQ-S9-008 (TSD S9 T8) and the plan carries none (GAP-3106). What D-RCV-60 changes is who owns the panel, where the terms live and who writes the record.

- **The panel is this service's.** `partner`, `partner_instruction` and `partner_user` are the three tables of `rwb_partner`, and no other service writes them (DP-01).
- **The terms are data.** The contract end is the only term the table carries (DF-PRT-006); the fee schedule, the service levels and the scope are the reference data of FEAT-PRM-02 (FSD S9 A2.2) and no field links a partner to their version (ASM-5341).
- **The decision comes first.** A failed record write leaves the panel unchanged with MSG-P7-003, as AC2 asks and AC-EXC-S9-001-02 repeats (DP-03; TSD S9 T2).
- **The write has no published operation.** API-S9-001 is the only panel operation in the inventory (TSD S9 T-A.1), so the story names the missing one rather than inventing it (ASM-5340).
- **The portal user is a firm's.** NFR-050 scopes a partner account to its own cases with multi-factor authentication (TSD S9 T7), so it holds no bank role and no customer data.
- **Contract end is not recall.** R-UNI-26, R-UNI-28 and R-UNI-29 recall open cases on exit, insolvency and conduct (Business Rules and Routing Logic v4); that is RWB-S9-E7015-APP's and RWB-S9-E7016-APP's.
- **Two edges, one service.** Staff reach rwb-partner through the gateway-bff composite route (DP-19) and firms through the partner gateway on FAPI 2.0 (Architecture v5 slide 8), which no dependency row carries (ASM-5346).

### 3. Preconditions

- RWB-S9-E6029-CON is published: the `Partner` element, the required list, the two enumerations, the rights, the error set, the `Idempotency-Key` rule and the fakes, with the write's placeholder (GAP-3106; ASM-5340).
- `partner`, `partner_instruction` and `partner_user` exist in `rwb_partner` from the DB story, with the standard columns of TSD S9 T3.0; this story adds no table, no column and no migration.
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the command with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the composite route, one hop (DP-19).
- The reference-data read answers the two lists at their version; its operation name is Not specified in the source documents (GAP-3106; ASM-5345).
- The access rows of "Partner portal" and its rights are those of TSD S9 T6.1, read through the guard; this story builds no guard.
- FEAT-OCC-13 is a feature dependency of the business epic and no build dependency, and its owner is named by no S9 source (GAP-3106).
- The service runs as its own login on `rwb_partner`, with no grant on another `rwb_*` schema and none on a `v_ace_*` view (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; RWB-S9-E6029-CON tags it when its tests pass.

### 4. Flow

1. The officer opens SCR-34 and chooses to onboard a partner; the guard checks "Partner portal" with right C before any read (FSD S9 A2.1.2 step 1; DP-19).
2. The service reads `LOV-PANEL` and `LOV-PARTNER-TYPE` at their version and keeps no copy (TSD S9 T3.2; ASM-5345).
3. The officer enters `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end` and, where access is opened, the firm's portal user (FSD S9 A2.1.3.2; TSD S9 T3.1).
4. VR-S9-001-1 validates every required field with MSG-GEN-001; `partner_code` must be unique, and a duplicate answers 409 with no row and no record (TSD S9 T-A.2).
5. `PartnerOnboardingService` builds the outcome with the two list versions in force and the caller's scope (FSD S9 A2.1.2 step 2).
6. `PartnerDecisionRecordWriter` writes one record **before any change**: the partner code, type, panel status, contract end, list versions, outcome and decided-at time; a failed write stops the command (DP-03; legacy AC2).
7. `PartnerRepository` inserts the `partner` row in one transaction with the record and the idempotency row, `score` empty for RWB-S9-E7011-APP (DF-PRT-001 to DF-PRT-007).
8. Where access was requested, one `partner_user` row is inserted for the firm, scoped as NFR-050 gives it and holding no bank role (ASM-5343).
9. The command answers the `Partner` element; a repeated `Idempotency-Key` returns the stored answer and writes no second row (TSD S9 T-A.2).
10. SCR-34 and SCR-35 show the partner, its type and panel status from this service, read only, next to the case answers of rwb-case (DP-19).
11. The contract end is a date and not a trigger: nothing is recalled, no case is touched and no timer is set here (§9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing changes: no `partner` row, no `partner_user` row, no answer | MSG-P7-003 | AC2, TC-E6-029-02, TC-E6-029-04 |
| X2 | The role lacks the Partner portal right C | 403 before any read, no record | MSG-P4-002 | AC3, TC-E6-029-03, TC-E6-029-13 |
| X3 | A required field is empty or invalid | 422 with the field named, no record and no row | MSG-GEN-001 | AC4, TC-E6-029-01, TC-E6-029-07 |
| X4 | `partner_code` already exists | 409 with no row and no record | None named for the conflict | AC5, TC-E6-029-01, TC-E6-029-08 |
| X5 | A value is not in either list at its version | 422 with the field named; no value is coerced to a default | MSG-GEN-001 | AC6, TC-E6-029-01, TC-E6-029-09 |
| X6 | The list read or the record library misses 2 s, or its breaker is open | One retry, then 503 with the platform envelope; nothing written | None | AC7, TC-E6-029-01, TC-E6-029-10 |
| X7 | The same submission with the same `Idempotency-Key` | One row set, one record, one answer; the repeat is counted | None | AC8, TC-E6-029-01, TC-E6-029-11 |
| X8 | A statement reaches another schema, a `v_ace_*` view or a case row | The grant refuses it and the boundary test fails the build | None (pipeline log) | AC9, TC-E6-029-06, TC-E6-029-12, s17, BR6, BR7 |

X1 and X2 are the FSD paths, X3 to X5 the validations of VR-S9-001-1 and the lists, X6 to X8 the call type, the repeat and the boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against RWB-S9-E6029-CON, the list fake and the record stub, on its own schema |
| Negotiable | The command name, the decision code and the answer mapping are this story's; the fields, lists, messages and columns are fixed |
| Valuable | A partner reaches the panel with its type, state and contract end on the record |
| Estimable | One command, one record write, one repository, one list client, one controller, two fragments |
| Small | Two weeks with its tests on the fakes |
| Testable | Synthetic partners, plus the conflict, the invalid value, the refusal and the repeated key |

### 7. Acceptance criteria

```gherkin
Feature: Onboard a partner and set terms

  Background:
    Given the rwb-partner service runs as its own login on schema rwb_partner
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E6-029 AC2)
    Given the rwb-decision contract mock returns the local decision-record chain and its central ledger entry for a healthy write
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Role without right C is refused (exception X2) (new, D-RCV-60)
    Given the role lacks the Partner portal right C
    When the action is taken
    Then the answer is 403 with MSG-P4-002 before any read and nothing is recorded

  Scenario: AC4 Required field empty or invalid (exception X3) (new, D-RCV-60)
    Given a required field is empty or invalid
    When the action is taken
    Then the answer is 422 with the field named and no record and no row is written

  Scenario: AC5 Existing partner_code refused (exception X4) (new, D-RCV-60)
    Given a partner with the same partner_code already exists
    When the action is taken
    Then the answer is 409 and no row and no record are written

  Scenario: AC6 Value outside either list refused (exception X5) (new, D-RCV-60)
    Given a value is not in either list at its version
    When the action is taken
    Then the answer is 422 with the field named and no value is coerced to a default

  Scenario: AC7 List read or record library misses 2 s (exception X6) (new, D-RCV-60)
    Given the list read or the record library misses 2 s, or its breaker is open
    When the action is taken
    Then one retry is made, then 503 with the platform envelope, and nothing is written

  Scenario: AC8 Repeat submission with the same Idempotency-Key (exception X7) (new, D-RCV-60)
    Given the same submission is sent with the same Idempotency-Key
    When the action is taken
    Then one row set, one record and one answer exist and the repeat is counted

  Scenario: AC9 Statement reaches another schema or a v_ace_* view (exception X8) (new, D-RCV-60)
    Given a statement reaches another rwb_* schema, a v_ace_* view or a case row
    When the boundary test runs
    Then the grant refuses it and the build fails

  Scenario: AC10 Error answers 401, 403 and 404 of the provided operations (new, D-RCV-60)
    Given a request to a provided operation has no valid token, the role lacks the right, or it names a partner that does not exist
    When the action is taken
    Then the answer is 401 for no valid token, 403 for a role without the right or 404 for an absent partner, with the platform envelope and nothing written

  Scenario: AC11 Activity retried or timed out (exception X6) (new, D-RCV-60)
    Given the onboarding is a synchronous command with no activity and its consumed read is retried
    When the retry also misses 2 s
    Then the answer is 503 with the platform envelope and nothing is written

  Scenario: AC12 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed contract call fails or does not answer
    When the action is taken
    Then nothing is written and the answer is Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC13)

  Scenario: AC13 Status change the model does not allow is refused (new, D-RCV-60)
    Given a request changes ON_NOTICE, SUSPENDED or EXITED, which this service only reads
    When the action is taken
    Then the change is refused with Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC14) and nothing is written
```

The criterion is legacy AC2 with its origin tag and only its decision log wording changed; the added `Given` mocks the decision path, and the legacy term `decision log` is now the decision record of DP-03 in `rwb_partner` with the central ledger behind it. AC1 of the key, "takes a partner onto the panel with its contract, fee schedule, service levels and scope" and "the system writes the result to the decision log with the rule version", is owned by RWB-ITG-E6029-ITG; the command behind it is built here (sections 4, 8, 16).

### 8. Business rules

| Rule | Message |
|---|---|
| VR-S9-001-1 Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S9-001 No value a business person may change is written in code; it is read from reference data with its version | None |

Both rows are those of FSD S9 A2.1.3.1, copied character for character. Their story rule IDs are BR11 (VR-S9-001-1) and BR12 (BR-S9-001).

| ID | Rule | Source |
|---|---|---|
| BR1 | The panel is this service's: `partner` and `partner_user` are tables of `rwb_partner` and no foreign key leaves the schema | Ownership rows; TSD S9 T3.1, T3.3; DP-01 |
| BR2 | The record is written before the row changes, with the list versions in force; a failed write changes nothing with MSG-P7-003 | DP-03; TSD S9 T2; legacy AC2 |
| BR3 | The panel states and the partner types are reference data read with their version, never a constant or a coercion | BR-S9-001; TSD S9 T3.2; ASM-5345 |
| BR4 | The contract end is a date, not a trigger: no recall, no case write and no timer here | R-UNI-26; RWB-S9-E7015-APP |
| BR5 | The fee schedule, service levels and scope are reference data of FEAT-PRM-02, and no `partner` field links a partner to their version | FSD S9 A2.2; ASM-5341 |
| BR6 | No case and no ACE data is read or written: `recovery_case` is rwb-case's, every `v_ace_*` view is rwb-source-data's | DP-01, DP-05; TSD S9 T4 |
| BR7 | The service holds no grant on another `rwb_*` schema and none on a `v_ace_*` view; the boundary test fails a build that adds one | DP-01, DP-05; ASM-5346 |
| BR8 | One partner per `partner_code` and one row set per `Idempotency-Key` | TSD S9 T-A.2 |
| BR9 | A portal user is scoped to its own firm's cases with multi-factor authentication and holds no bank role | TSD S9 T7 NFR-050; T6.1 |
| BR10 | No person name, address, contact value or identity number enters a row, the record, a log or an answer | Template and Rules §R7.2 (s17) |

Coverage: BR1 TC-E6-029-06; BR2 AC2, TC-E6-029-04; BR3 AC6, TC-E6-029-01; BR4 TC-E6-029-01; BR5 TC-E6-029-05; BR6 AC9, TC-E6-029-06; BR7 AC9, TC-E6-029-06; BR8 AC5, AC8, TC-E6-029-01; BR9 AC3, TC-E6-029-03; BR10 TC-E6-029-05; BR11 AC4, TC-E6-029-01; BR12 AC6, TC-E6-029-01.

Rules with no criterion of their own (BR1, BR4, BR5, BR10) are traced to tests only: BR1 is an architecture constraint held by the boundary test TC-E6-029-06, and BR4, BR5 and BR10 by the test rows named in the coverage line above.

### 9. State transitions

The partner has a panel state of its own; the case route state is rwb-case's and untouched (BR6). The vocabulary is the published list `LOV-PANEL` (TSD S9 T3.2).

| From (`partner.panel_status`) | Event | Condition | To | Written by |
|---|---|---|---|---|
| None, no row | Onboarding | The command validates and the record is written | `ACTIVE` | this story |
| `ACTIVE` | A panel or fee schedule change | A new version in force | unchanged | RWB-S9-E6030-APP |
| `ACTIVE` | A missed target | FEAT-PRM-11 | `ON_NOTICE` | RWB-S9-E7014-APP |
| `ACTIVE`, `ON_NOTICE` | An upheld conduct breach | R-UNI-29 | `SUSPENDED` | RWB-S9-E7016-APP |
| `ACTIVE`, `ON_NOTICE`, `SUSPENDED` | The contract ends or the panel is exited | R-UNI-26 | `EXITED`, with the recall | RWB-S9-E7015-APP |

| From (command) | Event | Condition | To |
|---|---|---|---|
| Idle | The officer submits the partner | Right C and the fields validate | Reading the lists |
| Reading the lists | The lists answer at their version | The values are in them | Recording |
| Recording | The record is written | The write commits | Writing |
| Writing | The rows are inserted | The transaction commits | Answered |
| Recording, Writing | The record or the transaction fails | X1 | Idle, nothing changed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | "Partner portal" CRUDA (TSD S9 T6.1) and right C: onboard a partner, set its type, panel state and contract end, read the panel; primary role of FSD S9 A2.1.3.3 |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL | "Partner portal" RA: read the panel and approve where a sibling asks; the FSD names the Head of Litigation and the Head of Asset Liquidity as also-users |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | "Partner portal" CRU: the legacy table gives them R, T6.1 gives CRU, so their C may create a partner |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | "Partner portal" R: read the panel, in scope |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | "Partner portal" RU through the partner gateway: a firm reads its own record and may not onboard |
| rwb-partner service identity | Runs the command, reads the lists, writes the record and rows, answers the read; no other schema grant |

The rights are the rows of TSD S9 T6.1 and nothing wider. DP-08 is not in this pattern set: the capability area and right are declared per operation and the guard is a service-template capability. Capability area PARTNER_PORTAL; each operation is guarded by the rwb-access authorise check of the service template for its declared right. The write right is C, the create right of the CRUDA row, and no operation in T-A.1 names it (ASM-5340).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id | Write, the partner reference |
| DF-PRT-002 | partner (S9, `rwb_partner`) | partner_code | Write, entered and unique |
| DF-PRT-003 | partner (S9, `rwb_partner`) | partner_name | Write, the registered name of the firm |
| DF-PRT-004 | partner (S9, `rwb_partner`) | partner_type | Write, a value of `LOV-PARTNER-TYPE` |
| DF-PRT-005 | partner (S9, `rwb_partner`) | panel_status | Write, a value of `LOV-PANEL` |
| DF-PRT-006 | partner (S9, `rwb_partner`) | contract_end | Write, the date entered |
| DF-PRT-007 | partner (S9, `rwb_partner`) | score | Write empty: RWB-S9-E7011-APP fills it |
| Standard columns | partner, partner_user (S9) | `is_active` to `updated_by`, seven columns | Write, with the optimistic lock of `version` |
| Not specified in the source documents (GAP-3106; ASM-5343) | partner_user (S9) | the portal user of the firm | Write, one row where access is requested |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, in `rwb_partner`) | rule id, rule version, inputs, outcome, decided at | Write through the library, before the row changes |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (S9) | id, case_id, partner_id, instruction_type, dates, status, result_code, fee_amount | Not written here: the instruction stories. case_id is a business key with no foreign key (ADR-014); its type is Not specified in the source documents (GAP-1838) |
| `LOV-PANEL`, `LOV-PARTNER-TYPE` | reference data (P3 by default ruling) | four panel states; eight partner types | Read with their version; field IDs Not specified in the source documents (ASM-5345) |
| DF-CAS-001 to DF-CAS-023, DF-REF-001 to DF-REF-015 | recovery_case (P3), rule_row (P7) | case and rule columns | Not read as tables, not written (BR6) |

Field IDs are those of TSD S9 T3.1 and the Logical Data Model and Data Dictionary. **No new table, no new column and no migration**: the two tables arrive with the DB story, and `decision_record` and `idempotency_key` are DP-03 library objects created in `rwb_partner`.

**No personal data.** A partner is a firm: a code, a registered name, a type, a state and a date. The portal user carries the firm's identity and no customer identity; every fixture is synthetic (s17, NFR-050).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the behaviour behind the two operations whose shape RWB-S9-E6029-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST or PATCH | `/partners` (method and path Not specified in the source documents (GAP-3106; ASM-5340)) | The seven properties of DF-PRT-001 to DF-PRT-007 in, the `Partner` element of 201 or 200 out | Partner portal, right C, scope applied | `Idempotency-Key` header |
| GET | `/partners` | `Partner[]` filtered by type and status (API-S9-001) | Partner portal, right R, scope applied | Not applicable |

The read answers 401, 403 with MSG-P4-002 and 503; the write adds 409 for a duplicate code and 422 with MSG-GEN-001. API-S9-001 is also the panel read that RWB-S9-E6030-CON declares for FEAT-PRM-02, so the two baselines must stay identical on its shape and this story adds the onboarding write. API-S9-002 to API-S9-006 belong to sibling stories and are neither built nor declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The reference-data read of the two lists at their version (operation name Not specified in the source documents (GAP-3106; ASM-5345)) | `/api/recovery/case/v1` | P3 rwb-case | The panel states and partner types in force, with their version, on every validation; faked |

One hop, 2 s, one GET retry with jitter and a breaker (ADR-020). The row is class C in fact while the plan's C row is None (ASM-5345). The record is not a call: it is the DP-03 library on `rwb.decision-record.v1`, carried as RWB-PLT-E1027-CON.

#### 12.3 Events published

None. The service owns `rwb.partner.events.v1` with its retry and `.dlt` topics, and its event set carries `InstructionIssued` (`EV-20`, `instructionId`, `partnerId`, `type`, `dueOn`), which the instruction story publishes. Onboarding issues no instruction, so no event, producer group or outbox row is declared and a build that adds one fails the absence test; the outbox is the DP-09 library the pattern set does not carry (ASM-5344).

#### 12.4 Events consumed

None. `PartnerResultSubmitted` (`EV-21`, `instructionId`, `result`, `documents`) is consumed from the partner portal by RWB-S9-E6033-APP, and its target name `rwb.partner.PartnerResultSubmitted.v1` follows §R4 and is published in no catalogue (ASM-5344). Onboarding waits for no event.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow per instruction, the child of `CaseWorkflow` in the stages that instruct a partner | `rwb-partner` | The service's only workflow (ownership rows); the instruction stories', not registered here |
| None | None (no activity) | `rwb-partner` | Onboarding is a synchronous command in its own transaction; no activity is added |

Workflow ID form and start rule: Not specified in the source documents (CG-ALL-11783); the catalog row gives neither a form nor a start rule.

#### 12.6 Schedules

None. The ownership rows give S9 no job: the contract end is a date and the recall it may start is RWB-S9-E7015-APP's under R-UNI-26.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm on the panel; one row per partner |
| partner_user | S9 (`rwb_partner`) | The portal user of the firm; one row where access is requested |
| decision_record | PLT library, in `rwb_partner` | The local hash-linked record of the onboarding (DP-03) |
| idempotency_key | PLT library, in `rwb_partner` | The key of the repeat and the answer it holds |
| outbox_event | PLT library, in `rwb_partner` | Present; this story writes no row to it (§12.3) |

Not owned and never read as a table: `partner_instruction` free of this story's writes, `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5). No foreign key leaves `rwb_partner` (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Reference-data fake | The four states and eight types at their version; a value outside both; no answer beyond 2 s | AC2, X5, X6 |
| Local decision-record stub | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-34 answer, loading and list | §15, TC-E6-029-01 |
| Partner-gateway fake | The firm's own scope, and a token of another firm refused | BR9, TC-E6-029-03 |
| rwb-case fake | Not specified in the source documents (DOR-RWB-S9-E6029-APP-22) | Not specified in the source documents (DOR-RWB-S9-E6029-APP-22) |

The fakes are test-only and the consumed read keeps its placeholder until its owner confirms it (GAP-3106; ASM-5345).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The write and `GET /partners` on `/api/recovery/partner/v1`; the list read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `EV-20` and `EV-21` are sibling stories' |
| Temporal | 1 workflow named, 0 registered | `InstructionWorkflow` on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.partner`, module `onboarding`; front end `src/modules/recovery/partner/PartnerPanel.tsx`, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the legacy AC2 tests; DP-13 moves the base and no shape; DP-19 is how SCR-34 and SCR-35 reach the service. These three are the whole pattern set and no fourth is added: DP-07, the list read, is a real dependency the plan holds in neither row (GAP-3106; ASM-5345).

**Dependencies the tables add and the plan does not hold.** The list read is class C in fact (DP-07 would add `RWB-PLT-E1043-CON` and `C RWB-P3-E1043-CON`) and the C row is None, so the story builds on its fake. The partner gateway is a second surface and not a row (ASM-5346), and the DP-09 outbox is recorded, not added (ASM-5344). The H row stands.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerOnboardingController` | Controller | The two operations, the right, the `Idempotency-Key` and the problem mapping |
| `PartnerOnboardingService` | Service | VR-S9-001-1, the code uniqueness, the panel outcome and the list versions |
| `PartnerDecisionRecordWriter` | Library adapter | The record before any change; refuses the command on a failed write |
| `PartnerRepository` | Repository | The `partner` and `partner_user` rows in one transaction with the idempotency row |
| `ReferenceDataClient` | Client | The two lists, one hop, 2 s, breaker, one GET retry |
| `PanelQueryService`, `PartnerPanel` | Service, component | The panel read, and the two fragments with their refusal and not-recorded states |

**Database and migrations.** None: the tables arrive with the DB story and the record and key are library objects (DP-03). No column is added for a fee schedule, a service level, a scope or a list version (ASM-5341).

**Configuration and reference data.** The lists are read with their version (ASM-5345); the capability area and rights are rwb-access rows read through the guard; the 2 s budget and the single hop are ADR-020.

**Build steps**

1. The controller and the two operations, with the right and the `Idempotency-Key` (AC2, X2, X7).
2. `ReferenceDataClient` against its fake, with the outside-the-list and no-answer paths (X5, X6).
3. `PartnerOnboardingService` with VR-S9-001-1 and the 409 (X3, X4).
4. `PartnerDecisionRecordWriter` against the stub, with the failed-write path (AC2, X1).
5. `PartnerRepository` with one transaction, the optional `partner_user` row and the idempotency row (§11).
6. `PanelQueryService` and `PartnerPanel` on both screens through the route fake (§15).
7. The boundary test: nothing outside `rwb_partner`, no `v_ace_*` read, no write to a sibling schema (X8).

**Feature flag.** `rwb.partner.onboarding-v1`; off means the write answers 503 with the flag named and the panel read is unaffected.

**Done when.** The tests of section 16 pass, a partner is onboarded on synthetic lists in SIT with one row, one record and one answer, a duplicate and an invalid value write nothing, a forced record failure changes nothing, and SCR-34 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is empty or invalid, or a value is not in force (X3, X5) | Enter {field}. |
| MSG-P4-002 | A role without right C calls the write (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are those of the legacy message set and of FSD S9 A2.1.3.1, copied unchanged. The 409 of a duplicate code has no message ID in any source (GAP-3106).

### 15. Screens and states

SCR-34 Partner list and SCR-35 Placement and allocation are served through the gateway-bff composite route (DP-19), which calls rwb-partner for the panel and rwb-case for the case; this story fixes the rwb-partner answers only, and the route specification belongs to RWB-PLT-N001-CON. The partner gateway serves the same operations to a firm on FAPI 2.0, scoped to its own record (ASM-5346).

The legacy states are "Loading; list". This story serves the list with the new partner, its type and panel status, and the loading state of the composite answer; the refusal, invalid and not-recorded states read the messages of section 14. `ON_NOTICE`, `SUSPENDED` and `EXITED` are read only here. SCR-35 shows the partner as a choice and allocates nothing (RWB-S9-E6031-APP).

**Screen states.** Screen Specifications v1 gives a loading state for SCR-34 and SCR-35. The empty, error and no-access states are Not specified in the source documents (CG-ALL-11788), and the empty-state wording is Not specified in the source documents (DOR-RWB-S9-E6029-APP-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-029-01 | AC4 to AC8; the command and the panel: one partner with its type, state and contract end in one row with one record; a duplicate code and an out-of-list value write nothing | Component | `PTN-2026-0001`, type `AGENCY`, `ACTIVE`, contract end `2028-03-31`; a repeated code; a type outside the list |
| TC-E6-029-07 | AC4 (X3): a required field is empty or invalid; 422 with the field named, no row and no record | Component | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC4) |
| TC-E6-029-08 | AC5 (X4): `partner_code` already exists; 409 with no row and no record | Component | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC5) |
| TC-E6-029-09 | AC6 (X5): a value not in either list at its version; 422 with the field named, no value coerced to a default | Component | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC6) |
| TC-E6-029-10 | AC7 (X6): the list read or record library misses 2 s or its breaker is open; one retry, then 503, nothing written | Component | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC7) |
| TC-E6-029-11 | AC8 (X7): the same submission with the same `Idempotency-Key`; one row set, one record, one answer | Component | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC8) |
| TC-E6-029-12 | AC9 (X8): a statement reaching another schema, a `v_ace_*` view or a case row is refused and fails the build | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC9) | Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC9) |
| TC-E6-029-02 | AC2 | Component | The record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-029-03 | AC3; access | Component | A role without right C: 403 with MSG-P4-002; a token of another firm refused |
| TC-E6-029-13 | AC3; access | Component | A role without right C: 403 with MSG-P4-002 before any read and no record written |
| TC-E6-029-04 | Principle 5 | NFR | A forced record failure: no `partner` row, no `partner_user` row, no answer |
| TC-E6-029-05 | Contract of the operations, events and activities of section 12; BR5, BR10 | Contract | Each operation, event and activity of section 12 against its published contract |
| TC-E6-029-06 | Boundary of the tables of section 12.7 (ASM-3438); AC9, BR1, BR6, BR7 | Boundary | Each table of section 12.7 and each `rwb_*` and `v_ace_*` grant; the build fails on a new grant |
| TC-E6-029-14 | AC10 | Component | A request with no valid token, a role without the right, and an absent partner: 401, 403 and 404 with the platform envelope |
| TC-E6-029-15 | AC11 | Component | The read retried and missing 2 s again: 503 with the platform envelope and nothing written |
| TC-E6-029-16 | AC12 | Component | A consumed contract call that fails or does not answer: nothing written; the answer is Not specified in the source documents (NEWAC-RWB-S9-E6029-APP-AC13) |
| TC-E6-029-17 | AC13 | Component | A request changing `ON_NOTICE`, `SUSPENDED` or `EXITED`: refused and nothing written |

The four legacy cases keep their IDs and order, with the Level column added. TC-E6-029-01 carries the Covers of AC1 because it proves that behaviour; the cross-service evidence and the `-ITG` copies belong to RWB-ITG-E6029-ITG. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases.

### 17. Guardrails

- No business value in code: the states, the types, the required fields and the contract end are reference data or request values.
- No personal data in the rows, the record, a log or an answer: a code, a firm's name, a type, a state and a date, with synthetic fixtures (s17, NFR-050).
- No ACE data: no `v_ace_*` grant and no ACE table read (DP-05, BR7).
- The case stays with rwb-case and the terms with FEAT-PRM-02: no case row, timer, fee schedule, service level, scope or document column (BR4, BR5, BR6).
- The record comes before the row and the command is idempotent (DP-03, BR2, BR8).
- One base, one topic, one queue, one schema and one login per service (DP-13, DP-14).
- No retired element returns: no Quartz row, no shared job table, the monolith base, no event published here and no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Feature | L3 process | Used in |
|---|---|---|---|---|
| Legacy story | RWB-E6-029, Split (rework); AC2 here, AC1 on RWB-ITG-E6029-ITG; FEAT-PRM-01 | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 1, 7, 16 |
| Feature | FEAT-PRM-01, module S9, epic E6, depends on FEAT-OCC-13, whose owner no S9 source names (GAP-3106) | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 1, 2, 3 |
| FSD S9 v3 | A1.3, A1.4, A2.1.1 to A2.1.4.3; VR-S9-001-1 and BR-S9-001; field catalog; roles; SCR-34 and SCR-35 | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 2, 3, 4, 5, 8, 14, 15 |
| TSD S9 v2 | T1, T2; T3.0 to T3.3; T4; T5.1 INT-24; T6.1, T6.2; T7 NFR-050; T8 REQ-S9-001 to -004 and -008; T-A.1, T-A.2 | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 3, 10, 11, 12, 13, 16 |
| Logical data model | DF-PRT-001 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023 | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 11 |
| Routing logic | R-UNI-26, R-UNI-28 and R-UNI-29 as the siblings' rows; `LOV-PANEL` | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 2, 8, 9 |
| Patterns | DP03, DP13, DP19; DP-07, DP-08 and DP-09 as recorded absences | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 13 |
| Gaps and assumptions | GAP-3106; ASM-5340, -2, -4, -5, -6, -7; the baseline gap GAP-3107 belongs to RWB-S9-E6029-CON | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | 1, 2, 3, 4, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | FEAT-PRM-01 | Not specified in the source documents (DOR-RWB-S9-E6029-APP-2) | all |

### 19. Out of scope

- AC1 and its cross-service journey: RWB-ITG-E6029-ITG.
- The shape of the write and the read, the element, the required list, the enumerations, the rights, the error set and the fakes: RWB-S9-E6029-CON.
- The panel, the fee schedule and the service levels as versioned reference data: RWB-S9-E6030-APP (FEAT-PRM-02).
- The allocation, override, partner result, agency placement and agency fee: RWB-S9-E6031-APP to RWB-S9-E6035-APP.
- The score, fee approval, review, notice, contract end and recall, and conduct check: RWB-S9-E7011-APP to RWB-S9-E7016-APP.
- The case and its states (P3), the access rows (P4), contract documents (P5) and notices (P6).
- The link between a partner and the version of its terms (GAP-3106; ASM-5341) and the method and path of the write (ASM-5340).
- The partner gateway and the composite route (RWB-PLT-N001-CON and the edge stories); the deployment, flag, dashboards, alerts and runbook (the operations story of this key).
