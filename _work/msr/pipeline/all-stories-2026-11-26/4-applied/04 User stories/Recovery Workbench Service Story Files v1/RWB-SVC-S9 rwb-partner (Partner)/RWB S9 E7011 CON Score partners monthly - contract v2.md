# RWB-S9-E7011-CON Score partners monthly - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7011-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the monthly scorecard of rwb-partner, split from RWB-E7-011. It fixes the `partner` element with its `score` property and the measures slice that has no element, the two consumed rows of rwb-source-data and rwb-decision, the rights and the error set of the run and of the read, the fakes, and the four absences the step has — no operation, no event, no Schedule and no scorecard table — on the base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The `partner` element and its seven fields are declared unchanged, because TSD S9 T3.1 already carries `score` and the six operations of the service belong to the panel, instruction, result and invoice stories. The score read has no published operation name, the measures behind SCR-36 have no published element, the monthly trigger has no source and the plan's C row is empty although the run consumes two services (GAP-3122; ASM-5422 to ASM-5426). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E7011-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the monthly scorecard of rwb-partner — the unchanged `partner` element with its `score`, the consumed score and rule-set rows, the rights and the error set of the run and of the read, the fakes and the four absences**, so that **the app story, the SCR-36 scorecard slice and the partner-portal clients build against one fixed, testable contract on Day 1, and a field, a score shape or a right can never drift between rwb-partner, rwb-source-data and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, two consumed rows and the absences the step has. It declares no operation, no event and no Schedule of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy scorecard of RWB-E7-011 ran inside one process and one schema: it read the ACE score view, the partner, the rule row and the decision log without a boundary. The target splits them: rwb-source-data owns the ACE score rows and their batch record, rwb-decision owns the scorecard rule set and the central ledger, rwb-case owns the lists of values and the parameters, and rwb-partner owns the panel, the instructions and the score. Each boundary is a contract another team builds against, so the shapes have to be fixed before the app story starts: the score rows the run measures, the rule set it applies, the score it publishes and the rights of the read.

The baseline also fixes the naming the checks require: schema `rwb_partner`, login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules v1 §R4; context pack service row; TSD S9 T0.1). It records that rwb-partner holds no grant on `rwb_source_data`, `rwb_decision` or `rwb_case`, so the score rows and the rule set are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the baseline declares no operation for the scorecard, because the Ownership Map gives S9 six operations and all six belong to other stories of the service while the measures of SCR-36 are unpublished (GAP-3122; ASM-5422); the `partner` element is unchanged and the scorecard stores no measures of its own, because no source gives a scorecard table or column (ASM-5423); the two consumed rows carry placeholders because neither owner publishes an operation for a scorecard read and the plan's C row is empty (ASM-5424); and the monthly trigger has no source, so the baseline declares no Schedule and records the platform binding (ASM-5425).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is created in wave 4, so the business wave and the service wave agree and no W-MAP conflict is raised, with the date copied unchanged and marked tentative (ASM-5426).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, the `v_ace_score` rows are consumed from P1, `rule_row` and `decision_log_entry` are P7's, and `recovery_case` and `timer` are P3's. This document never declares another service's table or operation as its own.
- The published API file `rwb-partner.yaml` (5.0.0, 22 November 2026) is the artefact the fakes are generated from, and the six operationIds of TSD S9 T5.2.1 are the ones this baseline names.
- The two consumed reads are published with fakes so the rows name a real owner document; neither is a row of this story's dependency list, which is None, and the absences are recorded (GAP-3122; ASM-5424).
- The scorecard rule set and the lists of values are governed in rwb-decision and rwb-access; this baseline names them and declares none of them.
- TSD S9 T6.1 is the only rights source for this service, and it gives Partner portal R to twenty-two staff roles and RU to the partner-type users, with RW-AGENCYMG holding CRUDA; this baseline declares those rights and widens none.
- `partner` and `partner_instruction` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this step and record that it declares no operation for the scorecard, with the six operations of the service named as the other stories'.
2. Declare the `partner` element exactly as TSD S9 T3.1 and `rwb-partner.yaml` give it, with `score` as "Latest scorecard result", and record that no field carries a measure.
3. Declare the two consumed rows of rwb-source-data and rwb-decision with the fields the run measures and applies, and record that both operation names are unpublished.
4. Fix the scorecard-entry element of DP-03 with its attributes, its write order and its failure behaviour.
5. Publish the rights of the run and of the read, and record the unattended identity.
6. Publish the error set, the status codes and the message IDs of the run and of the read.
7. Publish the fakes of 12.8 and the four absence tests: no operation, no event, no Schedule and no scorecard table.
8. Fix the naming baseline and the boundary, then tag the baseline and hand it to RWB-S9-E7011-APP, the SCR-36 slice, the partner-portal clients and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside a list of values | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC2, AC4, AC7 |
| X2 | A field is renamed or removed within major version 1, or a list value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3 |
| X5 | The document declares an operation, an event, a Schedule, a scorecard table, a foreign table property or a new column of `partner` | The absence and boundary tests fail the build | None | AC1, AC2, AC7 |
| X6 | The rights of the run and of the read are not the ones TSD S9 T6.1 declares, or the unattended identity is given a user right | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | A measure, a threshold or a rule version is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-source-data and rwb-decision only |
| Negotiable | The element attribute names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S9-E7011-APP, the SCR-36 scorecard slice and the wave 4 harness on Day 1, and the rwb-source-data team on the same day |
| Estimable | One OpenAPI document, nine contract tables, five fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the monthly scorecard of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner is S9, of the ACE score rows is P1, of rule_row is P7 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no scorecard operation, no event and no Schedule and names the six operations as other stories' (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the monthly scoring of a partner or the publication of a scorecard
    Then it records GET /partners (API-S9-001), POST /cases/{caseId}/instructions (API-S9-002), GET /partner/instructions (API-S9-003), POST /partner/instructions/{instructionId}/accept (API-S9-004), POST /partner/instructions/{instructionId}/results (API-S9-005) and POST /partner/instructions/{instructionId}/invoices (API-S9-006) as the operations of the panel, instruction, result and invoice stories of this service, and the Ownership Map as giving S9 no seventh operation
    Then the monthly score per partner against its measures behind SCR-36 carries the placeholder, with an error set of 400, 401, 403 with MSG-P4-002, 404 and 503 and one message ID per condition (GAP-3122; ASM-5422)
    Then the absence test fails a build that declares a scorecard operation, a second base or a second topic

  Scenario: AC2 The partner element is declared unchanged and carries the score but no measure (new, D-RCV-60)
    Given the partner section of the baseline
    When it is compared with TSD S9 T3.0, T3.1 and T3.2 and with the Partner element of the API Specification
    Then the partner element declares the seven properties of DF-PRT-001 to DF-PRT-007: id, partnerCode, partnerName, partnerType, panelStatus, contractEnd and score, with the types and lengths TSD S9 T3.1 gives them
    Then id, partnerCode, partnerName, partnerType and panelStatus are required and contractEnd and score are optional, score is declared as a number described "Latest scorecard result", and the standard record columns of TSD S9 T3.0 are declared beside them
    Then partnerType is declared against LOV-PARTNER-TYPE with AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, and panelStatus against LOV-PANEL with ACTIVE, ON_NOTICE, SUSPENDED and EXITED, with the values TSD S9 T3.2 gives and none added
    Then the document records that no property carries a measure, a period, a threshold or a scorecard row, that this step adds no column and no migration, and that the measures of SCR-36 have no element (GAP-3122; ASM-5423)

  Scenario: AC3 The two consumed rows are declared with their fields and their placeholders (new, D-RCV-60)
    Given the consumed rows and the data boundary of the baseline
    When they are compared with rwb-source-data as the owner of the ACE score rows and with rwb-decision as the owner of the rule row
    Then the score read is declared as consumed from P1 rwb-source-data with the fields DF-ACE-270 to DF-ACE-279: score_key, account_key, model_code, model_version, score_value, estimate_value, route_code, scored_at, source_system and data_as_of, and with the batch status of the score product that guards the run
    Then the rule-set read is declared as consumed from P7 rwb-decision with the rule row fields DF-REF-001 to DF-REF-015 and the package version in force
    Then both operation names are Not specified in the source documents, both reads are one hop with a 2 s budget and a breaker, and the document records that the plan's C row is empty although the run consumes two services (GAP-3122; ASM-5424)
    Then the document declares no `v_ace_*` view, no ACE table, no `rule_row` property and no foreign table property, and records that TSD S9 T5.2.3 declares SQL provided 0 and consumed 0

  Scenario: AC4 The scorecard entry element is declared and written before the score (new, D-RCV-60)
    Given the entry section of the baseline
    When it is compared with the local decision-record library and with R-UNI-39
    Then one entry is declared per partner and period with the partner reference, the period, the measures with their values, the score, the rule-set code and its package version, and the run identity
    Then the entry is written through the library on the shared rwb.decision-record.v1 before partner.score is written, and a failed write leaves everything unchanged with MSG-P7-003
    Then the score is declared on `partner.score` only, and the document records that no measure, no period and no threshold is a schema default or a constant of the code
    Then the document records that the review target of FSD S9 A2.8.1 is set with DL22 and is reference data, and that no value is invented for it (GAP-3122; ASM-5423)

  Scenario: AC5 The rights, the roles and the unattended identity are fixed on the run and on the read (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T6.1 and with FSD S9 A2.8.3.3
    Then the read declares Partner portal right R, held by RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL and RW-TRIBE, and the partner-type users PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC RU, scoped to their own firm
    Then the manual start of a run declares no right of its own beyond the Partner portal rows of the matrix, and RW-AGENCYMG is the only role with CRUDA and the "also uses" role of FSD S9 A2.8.3.3
    Then the document records that the run runs unattended under the rwb-partner service identity, that the primary actor of the feature is "None; runs unattended", and that the identity holds no user right
    Then the access test fails a build that gives the unattended identity a user right or a role a right the matrix does not give

  Scenario: AC6 The element and the fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the score fake answers the ACE score rows of a synthetic partner scored on a period at a model version, the same rows one month older, a stale batch status, a partner with no rows and no answer inside 2 s
    Then the rule-set fake answers the scorecard rule set at its version and a package with no version in force, the entry stub answers a healthy chain and a stopped chain, and the partner fake answers a partner at ACTIVE, at ON_NOTICE, at SUSPENDED, at EXITED and with a contract ended before the cut-off
    Then the route fake answers the merged SCR-36 and SCR-34 payload with the scorecard slice of this service read once
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published, scheduled or stored twice (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1, the queue is rwb-partner and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction, partner_user and the library objects decision_record and idempotency_key, and the v_ace_score rows, rule_row, decision_log_entry, recovery_case and timer are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21) as the instruction and result stories'
    Then the document declares no Schedule of its own and no Quartz row and no shared job table, records that the monthly cut-off is bound to the platform scheduling of DP-10 and that the Ownership Map gives S9 no job, and records that the trigger is Not specified in the source documents (GAP-3122; ASM-5425)
    Then the document records that no scorecard table and no new column is declared, because the score is `partner.score` and the period is carried on the entry (ASM-5423)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E7011-APP and they copy no criterion of the legacy story, whose two criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `partner` element is this service's and is declared as TSD S9 T3.1 gives it, with `score` and no measure, no period and no threshold | Context pack ownership row `partner`; TSD S9 T3.1 and T3.2; `rwb-partner.yaml` Partner element; DP-01 |
| BR2 | The scorecard is declared as an entry written before the score, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S9 T2; R-UNI-39; legacy RWB-E7-011 AC1 and AC2 |
| BR3 | The ACE score rows stay with rwb-source-data: the contract declares the read as consumed and declares no `v_ace_score` property, no ACE table and no SQL grant | DP-05; TSD S9 T0.4 and T5.2.3; ASM-5424 |
| BR4 | The rule set and the central ledger stay with rwb-decision: the contract names the rule row and the package version and declares none of them as its own | Business Rules and Routing Logic v4 rows R-UNI-38 and R-UNI-39; ASM-5424 |
| BR5 | The case, its route state and its timers stay with rwb-case: the contract declares no `recovery_case` and no `timer` property and no case write | Context pack ownership rows; ASM-5422 |
| BR6 | No event belongs to this step: the contract declares no published event and no consumed event, and names `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) as the instruction and result stories' | Event and Messaging Design v5 EV-20 and EV-21; TSD S9 T5.2.1 and T5.3 |
| BR7 | No Schedule and no job belong to this step: the monthly cut-off is the platform's DP-10 Schedule and the Ownership Map gives S9 no job | Context pack ownership rows (Jobs 0); FSD S9 A2.8.4.4; ASM-5425 |
| BR8 | The rights are TSD S9 T6.1's and nothing wider: Partner portal R for the read, the same matrix for a manual start, and the run unattended under the service identity | TSD S9 T6.1; FSD S9 A2.8.3.3 |
| BR9 | The vocabulary is closed: the eight partner types, the four panel statuses and the six instruction statuses of TSD S9 T3.2 are declared and this step adds none | TSD S9 T3.2 |
| BR10 | No personal data in a schema, an example or a fake: a partner code, a period, a score, a model version and a rule version only | Template and Rules v1 §R7.2 (s17); LDM v8 |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules v1 §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes |
| BR13 | No measure, threshold, period or rule version is a schema default or a constant | FSD S9 A2.8.3.1 (BR-S9-008); ASM-5423 |

### 9. State transitions

The lifecycle of this document, not of a run:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the two consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-36 slice, the partner-portal clients and the rwb-source-data owner accept the document and the fakes | Baselined |
| Baselined | Additive change | An attribute is added within major version 1 | Baselined |
| Baselined | Breaking change | An attribute is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | An operation, an event, a Schedule, a scorecard table or a foreign table property | In review |

The run states of RWB-S9-E7011-APP and the panel states of `LOV-PANEL` are the app story's and this baseline declares them without moving any partner or any run: the states are the vocabulary on which `panelStatus` is declared, and the scorecard adds no state value.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of a consumed row and the reading of the trigger absence |
| Consuming teams (the app story, the SCR-36 slice, the partner-portal clients and the rwb-source-data owner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field and no customer identity is declared in an element or a fake |
| Compliance and PDPA officer | Confirms the review target the scorecard names as reference data, which is set with DL22 |

The per-service login behind the security scheme of the document is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007 as TSD S9 T3.1 gives them: `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end` and `score` |
| Required flags | `id`, `partner_code`, `partner_name`, `partner_type` and `panel_status` required; `contract_end` and `score` optional; the standard record columns of TSD S9 T3.0 declared beside them |
| Lists of values | `LOV-PARTNER-TYPE` with AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC; `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED; `LOV-INSTR-STATUS` read and not declared, as TSD S9 T3.2 gives them |
| Score property | `score`, numeric(5,2) in the table and a number in the document, described "Latest scorecard result" and written by the run only (DF-PRT-007) |
| Scorecard entry | The DP-03 entry attributes: partner reference, period, measures with their values, score, rule-set code and package version, and the run identity; no column of `partner` carries a measure (ASM-5423) |
| Consumed score shape | DF-ACE-270 to DF-ACE-279 of the `v_ace_score` rows, with the batch status of the score product, declared as consumed and faked (ASM-5424) |
| Consumed rule shape | DF-REF-001 to DF-REF-015 of the `rule_row` element and the package version in force, declared as consumed and faked |
| Fields with no source | The two operation names of the consumed reads and the measures element of SCR-36: Not specified in the source documents (GAP-3122; ASM-5424) |
| Review target | The scorecard target of FSD S9 A2.8.1, set with DL22 and declared as reference data with a placeholder (GAP-3122; ASM-5423) |
| Not declared here | the `v_ace_score` rows and every `v_ace_*` view (P1), `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), and the six operations API-S9-001 to API-S9-006 (the other stories of this service) |

The field-level formats of the entry are settled in the baseline review; this story fixes the element names, the unchanged `partner` element, the consumed fields and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The Ownership Map gives this service exactly six operations, `GET /partners` (API-S9-001, Partner portal R), `POST /cases/{caseId}/instructions` (API-S9-002, C), `GET /partner/instructions` (API-S9-003, R), `POST /partner/instructions/{instructionId}/accept` (API-S9-004, U), `POST /partner/instructions/{instructionId}/results` (API-S9-005, U) and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006, C), and every one of them is a write or a list of the panel, the instruction, the result or the invoice, which belongs to another story of this service. The scorecard run is unattended and takes no request, and the monthly score per partner against its measures behind SCR-36 is Not specified in the source documents and carries the placeholder (GAP-3122; ASM-5422). A build that declares a scorecard operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of the ACE score rows of the accounts placed with a partner, and of the score product's batch status (operation name Not specified in the source documents (GAP-3122; ASM-5424)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The measured result: `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value`, `route_code`, `scored_at`, `source_system` and `data_as_of`; read only, faked |
| The read of the scorecard rule set in force with its package version (operation name Not specified in the source documents (GAP-3122; ASM-5424)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule rows and the version the run applies and stamps on its entry; read only, faked |

Both rows are one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). They are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3122 with ASM-5424. The monthly cut-off is the platform Schedule of DP-10 and is declared in 12.6, not as a REST row.

#### 12.3 Events published

None. The service owns `InstructionIssued` (EV-20: `instructionId`, `partnerId`, `type`, `dueOn`) and `PartnerResultSubmitted` (EV-21: `instructionId`, `result`, `documents`) on `rwb.partner.events.v1`, and both are the issue and the result of an instruction, published by the instruction and result stories of this service (Event and Messaging Design v5; TSD S9 T5.2.1 and T5.3). A scorecard issues no instruction and submits no result, and no catalogue row carries a score fact, so this baseline declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5422).

#### 12.4 Events consumed

None. TSD S9 T5.2.2 states "Events this service consumes: None" and the Ownership Map gives S9 no consumed event. The score rows arrive on a REST contract, the cut-off is a Temporal Schedule and not a subscription, and `AceDataReady` (EV-26) names case creation, reconciliation, payment matching, booking confirmation and the write-off scan and no scorecard run. This baseline declares no consumer group, no subscription and no inbox of its own (ASM-5425).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ScorecardRun` | Scheduled activity set, one execution per period | `rwb-partner` in namespace `rwb-recovery` | The run from the cut-off or a manual start to the entry and the published score; its input, its guard and its report are declared, not built |
| `collectMeasuredResults` | Activity | `rwb-partner` | The batch status, the partners and instructions and the score rows in; the paired facts out |
| `evaluateScorecardRules` | Activity | `rwb-partner` | The rule set in force in; the measures, the score and the package version out |
| `publishScorecard` | Activity | `rwb-partner` | The entry, the `partner.score` write and the run report out, one transaction |

`InstructionWorkflow` is the service's only workflow and this step neither extends it nor adds a second: TSD S9 T0.2 counts one workflow and no job. The run and activity names are target design choices and no source document fixes them; no activity is registered by this story (ASM-5425).

#### 12.6 Schedules

None owned. The Ownership Map gives S9 no job and FSD S9 A2.8.4.4 declares "No background event", while FSD S9 A2.8.2 leaves the trigger as "a completed ACE batch, an event or a timer". The monthly cut-off is therefore bound to the platform scheduling of DP-10 on queue `rwb-partner`, its registration belongs to RWB-PLT-E1071 and the OPS story of this key, and the trigger is Not specified in the source documents (GAP-3122; ASM-5425). This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table of its own.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `partner` | S9 (`rwb_partner`) | The partner of the panel; the element the baseline declares with `score` and the app story writes |
| `partner_instruction` | S9 (`rwb_partner`) | The measured work placed with the partner; read by the run and declared in no element of this step |
| `partner_user` | S9 (`rwb_partner`) | The partner's portal users; declared as owned and not touched by this step |
| `decision_record` | PLT library, created in `rwb_partner` | The local hash-linked scorecard entry (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_partner` | The partner-and-period key and the outcome it holds |

The `v_ace_score` rows and every `v_ace_*` view (P1), `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7) and `document` (P5) are not owned by this baseline; it names them only as answers, rule versions or records of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data score-read fake | The ACE score rows of partner `AG-2026-0034` scored on `2026-11-30` at `model_version` 2026-11; the same rows with `data_as_of` 2026-10-31; a stale batch status; a partner with no rows; no answer inside 2 s; the operation name carries the placeholder (GAP-3122; ASM-5424) | AC3, AC6 |
| rwb-decision rule-set fake | The scorecard rule set at version `SC-2026-11` with its measures, and a package with no version in force | AC3, AC6 |
| rwb-partner partner fake | `AG-2026-0034` at `ACTIVE`, at `ON_NOTICE`, at `SUSPENDED`, at `EXITED` and with a contract ended before the cut-off | AC2, AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-36 and SCR-34 answer for the partners, with the scorecard slice of this service read once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The two operation names are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3122; ASM-5424).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The ACE score and batch-status read of rwb-source-data and the rule-set read of rwb-decision; one hop, 2 s each |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 are the instruction and result stories'; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 scheduled activity set and 3 activities declared, 0 registered | `ScorecardRun` on `rwb-partner`; no workflow of its own and no Schedule registered here |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no partner, no run and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the read and of a manual start, and five fakes.

**Deliverables.** The additive document `openapi/rwb-partner-v1.yaml` with the unchanged `partner` element and no scorecard operation, the contract README rows for the two consumed reads and their placeholders, the scorecard-entry schema of the library, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the score is answered. DP-05 is why the ACE score rows are a consumed row and not a view or a table. DP-13 moves the base of the service and adds no operation, because this step owns none. DP-19 is behind SCR-36 and SCR-34, whose screen model is the edge contract's. No other pattern is claimed: DP-10, the monthly schedule, and DP-04, the rule set at its version, are recorded as dependencies and not claimed, so neither appears in the metadata row and both are in the registers (GAP-3122; ASM-5424, ASM-5425).

**Build steps**

1. Record the absence of a scorecard operation and the six operations as the other stories', with the absent-operation test of AC1.
2. Publish the `partner` element with its seven properties, its five required flags and its two lists, and record the no-measure rule of AC2.
3. Record the two consumed rows of AC3 with their owners, their fields, the batch-status guard, the budget and the two placeholders.
4. Publish the scorecard-entry element of AC4, with the measures, the score, the rule-set version and the run identity, and validate it against the library schema.
5. Record the rights, the roles and the unattended identity of AC5.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline, the boundary and the four absences of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story, the SCR-36 slice, the partner-portal clients and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of an element is absent or invalid, or a body fails schema validation, or a list value is outside its enumeration | Enter {field}. |
| MSG-P1-001 | Carried from the legacy service level of this feature: the score product is stale, so the run is refused before any read, and no path of this baseline raises it | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | The role lacks the Partner portal right of the read or of the manual start, and the unattended identity is given a user right that the matrix does not give | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The scorecard entry cannot be written before the score is published | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The first, third and fourth IDs are those of the legacy message set of this key; MSG-P1-001 is the message VR-S9-008-1 gives the stale product. The text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded or added.

### 15. Screens and states

The contract serves the scorecard slice of SCR-36 Partner scorecard and the score column of SCR-34 Partner list through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner, its panel status and its score, rwb-case for the case and its owner, and rwb-decision for the decision records; this baseline fixes the rwb-partner answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5422). The measure list that SCR-36 plots is a placeholder, because no source publishes its element. The legacy screen table's two screens are accounted for: SCR-36 and SCR-34 are both answered by the `partner` element this baseline declares unchanged, the partner-portal screens PRT-01 to PRT-04 belong to the instruction and result stories, and the stale, refused and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-011-01 | AC1, AC2 | Contract | The synthetic partner `AG-2026-0034`; the contract half answers the unchanged element, the absent scorecard operation and the score property |
| TC-E7-011-02 | AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the entry element |
| TC-E7-011-03 | AC5 | Contract | A role without the Partner portal right and the unattended identity; the contract half answers the 403 with MSG-P4-002 and the rights of the read and of a manual start |
| TC-E7-011-04 | AC4, AC6 | Contract | A forced record failure and a drifted fake; the contract half answers the entry path and the drift test |
| TC-S9-E7011-CON-01 | AC1 | Contract | The document validates; no scorecard operation, no second base and no second topic are declared, and the six operations are named as the other stories' |
| TC-S9-E7011-CON-02 | AC2 | Contract | The `partner` element validates with its seven properties, its five required flags and its two lists; no measure, no period and no added state value |
| TC-S9-E7011-CON-03 | AC3 | Contract | The two consumed rows with their fields, their batch-status guard and their two placeholders; no view property and no ACE table |
| TC-S9-E7011-CON-04 | AC4 | Contract | The entry element with the measures, the score, the rule-set version and the run identity; the review target carries its placeholder |
| TC-S9-E7011-CON-05 | AC5 | Contract | Partner portal R for the read, the matrix for a manual start, and the unattended identity with no user right |
| TC-S9-E7011-CON-06 | AC6 | Contract | The five fakes match the document and a drifted fake fails the build |
| TC-S9-E7011-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event and a Schedule, and the boundary test for a `v_ace_*` path, a foreign table property and a scorecard table |

The four legacy cases are the legacy cases of RWB-E7-011 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E7011-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S9-E7011-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the measures, the thresholds, the period and the rule set stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: a partner code, a period, a score, a model version and a rule version only; no customer identity appears anywhere in the document.
- The ACE score rows stay with rwb-source-data, the case and its timers with rwb-case and the rule set and the ledger with rwb-decision: the document declares no `v_ace_*`, `recovery_case`, `timer`, `rule_row` or ledger property (BR3, BR4, BR5).
- This step owns no operation, no event and no Schedule: the document declares none for it and records the six operations as the other stories' (BR6, BR7, AC1).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The `partner` element is declared unchanged: a build that adds a measure, a period or a threshold column to it fails the absence test (BR1, ASM-5423).
- No scorecard table is introduced: the score is `partner.score` and the period rides the entry, so a second score card of record would fail the review (ASM-5423).
- The rights are TSD S9 T6.1's and are never widened in a contract, and the unattended identity keeps no user right (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard, not by a fixed share (Must, E6) | The `score` property, the scorecard entry and the two consumed rows | TC-E7-011-01, TC-S9-E7011-CON-02, TC-S9-E7011-CON-03, TC-S9-E7011-CON-04 |
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum (Must, E7) | The measures carried on the entry and the absence of a reporting feed | TC-S9-E7011-CON-04 |
| REQ-S9-001 | Every partner type is managed on the same six points (Must, E6) | The partner-type and panel vocabularies the element declares | TC-S9-E7011-CON-02 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E7011-CON-07 |
| ADR-018 | No data lake; rwb-reporting read model from events | No Power BI feed and no scorecard event declared | TC-S9-E7011-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S9-E7011-CON-03 |
| ADR-022 | Local decision record plus central ledger | The scorecard-entry element and the central ledger of P7 | TC-S9-E7011-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-011, disposition Split (rework); feature FEAT-PRM-08 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S9-E7011-APP; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S9-E7011-CON-01 to -07 |
| Feature and screens | FEAT-PRM-08, SCR-36 Partner scorecard and SCR-34 Partner list |
| Rules | R-UNI-38 and R-UNI-39 named from the Business Rules and Routing Logic v4 and governed in rwb-decision, with R-UNI-25, R-UNI-27, R-UNI-40 and R-UNI-45 read |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-014 (schema and login per service), ADR-018 (no data lake), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the measured-result read, the evaluation, the entry, the score and the run report: RWB-S9-E7011-APP.
- The six operations of the service and the stories that own them: the panel, instruction, result and invoice stories of rwb-partner.
- The panel, the fee schedule and their reference data: FEAT-PRM-02.
- The allocation of work by measured return and its override: FEAT-PRM-03 and FEAT-PRM-04.
- The receive of a partner result, the agency fee matching and the fee approval: FEAT-PRM-05, FEAT-PRM-07 and FEAT-PRM-09.
- The partner review, the notice and the contract end with the work recall: FEAT-PRM-10, FEAT-PRM-11 and FEAT-PRM-12.
- The ACE score rows, their batch record and the score product: rwb-source-data (P1), whose operation name this baseline does not publish.
- The scorecard rule set, its versions, the central ledger and the review target set with DL22: rwb-decision (P7) and the registers (GAP-3122).
- The case of record, its route state and the `timer` rows: rwb-case (P3).
- The gateway-bff composite route and the screen field list of SCR-36: RWB-PLT-N001-CON and the edge stories.
- The reporting read model of the scorecard, which no event carries: rwb-reporting (P9) and the register row (ASM-5422).
- The registration of the monthly schedule, the deployment of this capability, its flag, its dashboards, its alerts and its runbook: the OPS and INF stories of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
