# RWB-S9-E6030-CON Hold the partner panel and fee schedule as data — contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6030-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of RWB-E6-030 for rwb-partner (S9, service wave 4, business wave 4) is published as its own story so the app slice can build on Day 1. The baseline fixes the two panel reads on `/api/recovery/partner/v1` (DP-13), the `Partner` element with the fields of DF-PRT-001 to DF-PRT-007, `LOV-PANEL` and `LOV-PARTNER-TYPE`, the reference-data stamp that carries the version in force, the reference-data row consumed from rwb-case (DP-07), the decision-record element of DP-03, the error set and the five fakes. It declares no write operation, no event, no workflow and no Schedule, because no source publishes one for this key (GAP-3109; ASM-5348 to ASM-5359; ASM-5360, ASM-5361). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E6030-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **service team and the consumers of rwb-partner (the panel app slice, SCR-34 and SCR-35, the placement and scorecard stories and the wave 4 harness)**, we want **one tagged contract for the panel and its reference data — its two reads, its `Partner` element, its two lists, its version stamp, its consumed reference-data row, its error set and its fakes**, so that **the panel is built and tested in parallel on both sides of every boundary without waiting for the live services**.

This story owns the shapes and nothing else:

- the OpenAPI 3.1 fragment with `GET /partners` and `GET /partner/instructions` on the target base, their queries, their answer elements, their right, their scope and their error statuses (DP-13);
- the `Partner` element with the fields of DF-PRT-001 to DF-PRT-007 and the required flags of TSD S9 T3.1, and the `PartnerList` and `InstructionPage` answers of API-S9-001 and API-S9-003;
- the two closed lists `LOV-PANEL` and `LOV-PARTNER-TYPE` of TSD S9 T3.2, published as enumerations and bound to the version in force;
- the reference-data stamp: `listCode`, `version`, `values[]` and the `dataAsOf` instant, declared on every answer that names a list;
- the consumed reference-data row of rwb-case with its owner, its budget and its placeholder, and the decision-record element of DP-03 with its write-before-change rule and its failure behaviour;
- the error envelope, the message set of section 14, the naming baseline and the five fakes of section 12.8.

It does not own: any business outcome, row or answer instance (RWB-S9-E6030-APP); the firm record and its users (RWB-S9-AD022-APP); the six operations themselves, which the service contract baseline of rwb-partner declares and this fragment binds to its two reads (ASM-5359); the reference data and its lists (rwb-case, P3); the ledger and the rule rows (rwb-decision, P7); the roles (rwb-access, P4); and the implementations of the library, the edge route and the fakes' platforms, which are platform stories.

### 2. Business rationale

A contract is what lets wave 4 start on Day 1. The panel crosses three boundaries - the reference data of rwb-case, the decision record and the edge route - and the plan carries one C row for the first of them and none for the others, so without a tagged baseline the app slice would wait for live services and the wave would slip (GAP-3109; ASM-5349).

The baseline also settles the facts the sources leave open:

- the fee schedule and the service levels have no table of this service, so the baseline declares them as reference-data rows read at their version and not as an owned entity (GAP-3109; ASM-5348);
- no write operation is published for the panel, so the baseline declares two reads and records the absence rather than inventing a maintenance operation (GAP-3109; ASM-5350);
- the version has no column in DF-PRT-001 to DF-PRT-007, so it is declared as a stamp on the answer and on the decision record (GAP-3109; ASM-5350);
- `partner_user` has no field catalogue, so no element is declared for it (GAP-3109; ASM-5358).

The business effect is the one the legacy story promises - the panel, the schedule and the levels are data a business person may change, read with their version, and every change is recorded (BR-S9-002; legacy AC2) - and the baseline adds nothing to it. No business value is fixed here: the panel statuses, the partner types, the schedule and the levels stay reference data, so a business person changes them without a contract release.

### 3. Preconditions

- The service contract baseline of rwb-partner is in force: the six operations of TSD S9 T-A.1 on `/api/recovery/partner/v1`, the one error envelope and the one naming rule (ASM-5359).
- RWB-PLT-E1043-CON is published with the reference-data client schema, so the consumed reference-data row is declared against the library and not invented (DP-07).
- RWB-PLT-E1027-CON is published with its writer schema and stub, so the decision-record element is declared against the library (DP-03).
- RWB-PLT-N001-CON is published, so SCR-34 and SCR-35 are served on the composite route's terms and no screen contract is duplicated here (DP-19).
- TSD S9 T3.1, T3.2, T6.1, T6.2 and T-A.1 are available as the source of the element, the lists, the rights and the two operations; FSD S9 A2.2.3.2 gives the panel field catalogue.
- The path of the rwb-case reference-data read is Not specified in the source documents (GAP-3109; ASM-5349).
- No approval is needed to publish a Draft baseline; the tag is applied when the contract tests pass and the consumers sign off.

### 4. Flow

1. The fragment is drafted from TSD S9 T-A.1 and T-A.2: the two reads with their purposes, their queries, their answer elements and their error sets, on `/api/recovery/partner/v1` (DP-13).
2. The `Partner` element is written from DF-PRT-001 to DF-PRT-007 with the required flags of T3.1 and its two lists as published enumerations bound to the version in force.
3. The reference-data stamp is declared on every answer that names a list: `listCode`, `version`, `values[]` and `dataAsOf`.
4. The consumed row of rwb-case is recorded with its owner, its budget and its placeholder name.
5. The decision-record element is recorded against the library schema with the write-before-change rule and the MSG-P7-003 failure path.
6. The error set, the message texts, the Partner portal right R of both reads, the scope rule and the absence of an `Idempotency-Key` are recorded.
7. Five fakes are published, each answering the paths its consumers exercise, and the drift test compares each one with the document.
8. The baseline is reviewed by the panel app slice, the two screens, the placement and scorecard stories and the wave 4 harness, tagged and handed over.
9. A later additive change is published inside major version 1; a removal, a rename or a retype opens a new major version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer asks for a property this document does not declare | The answer fails schema validation at the consumer, not at the service | MSG-GEN-001 | AC1 |
| X2 | A fake drifts from the document | The drift test fails and the baseline returns to review | None (pipeline log) | AC6 |
| X3 | A `v_ace_*` property, a `recovery_case` property or an owned fee-schedule table appears in the document | The absence test fails the build and the change is refused | None (pipeline log) | AC4, AC6 |
| X4 | A write operation, a second topic, an event or a Schedule is declared | The absence test fails the build | None (pipeline log) | AC5, AC6 |
| X5 | A list value is fixed in the document instead of being bound to the version | The schema test fails and the value is moved to the enumeration reference | None (pipeline log) | AC3 |
| X6 | A property carries personal data | The schema test fails and the property is removed | None (pipeline log) | AC2 |

X1 to X6 are the failure paths of the artefact, not of a business transaction; the business failure paths are RWB-S9-E6030-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it starts on Day 1 from TSD S9, the Ownership Map and the four platform baselines and needs no running service |
| Negotiable | The element names, the wording of the descriptions and the shape of the fakes are the author's choice; the operations, the fields, the lists, the version stamp and the budgets are fixed by the sources |
| Valuable | The panel app slice, the two screens, the placement and scorecard stories and the wave 4 harness build on Day 1 against a tagged fragment and five fakes |
| Estimable | One OpenAPI fragment, one AsyncAPI absence note, nine contract tables, one contract README and five fake mapping sets |
| Small | Finished inside one week with the consumer sign-off |
| Testable | Each criterion is a validation of the document or a drift test of a fake, run in the pipeline |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the partner panel and its reference data

  Background:
    Given the platform naming and error library is in force
    Given ownership is read from the Ownership Map and Architecture v5: partner and partner_instruction are S9, lov_value and rule_row are P7 or P3 as the default ruling gives them, decision_log_entry is P7, every v_ace_* view is P1

  Scenario: AC1 The two panel reads are declared on the partner base with their shapes, rights and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-partner is produced with this change
    When it is validated against the OpenAPI 3.1 schema and the additive rule
    Then it validates with no error
    Then it declares GET /partners answering PartnerList and GET /partner/instructions answering InstructionPage, both under the base /api/recovery/partner/v1 and owned by rwb-partner
    Then GET /partners declares the query type and status and GET /partner/instructions declares the query status, page and size
    Then both declare the Partner portal right R with the scope applied and neither declares an Idempotency-Key
    Then the answers 401, 403, 503 are declared with the one error envelope and one message ID per condition of section 14
    Then no write operation is declared for the panel, the fee schedule or the service level and the absence is recorded (ASM-5350)

  Scenario: AC2 The Partner element, its required flags and its two lists are fixed (new, D-RCV-60)
    Given the panel section of the document
    When it is compared with TSD S9 T3.1 and T3.2 and FSD S9 A2.2.3.2
    Then the Partner element declares id, partner_code, partner_name, partner_type, panel_status, contract_end and score, which are DF-PRT-001 to DF-PRT-007
    Then id, partner_code, partner_name, partner_type and panel_status are required and contract_end and score are optional, as T3.1 gives them
    Then partner_type is bound to LOV-PARTNER-TYPE with its eight values and panel_status to LOV-PANEL with its four values
    Then no property is added for a fee schedule, a service level, a partner user, a case or a document, and those facts are named as other owners'
    Then no property carries personal data and no schema default carries a business value

  Scenario: AC3 The version in force is a declared stamp and no list value is a constant (new, D-RCV-60)
    Given the reference-data stamp of the document
    When it is compared with the reference-data contract of rwb-case and BR-S9-002
    Then every answer that names a list carries listCode, version, values[] and dataAsOf
    Then version is required, is a string and carries no example value that a business person may change
    Then the two lists are declared as references to the published enumerations at the version in force and not as a local copy of their values
    Then the schema test fails a build that hard-codes a list value or drops the version from an answer

  Scenario: AC4 The reference-data row consumed from rwb-case is declared and faked (new, D-RCV-60)
    Given the consumed rows of the document
    When they are compared with DP-07, the plan's C row RWB-P3-E1043-CON and the reference-data contract of rwb-case
    Then one row declares the list read of rwb-case with its list codes, its version, one hop and a 2 s budget
    Then its operation name is Not specified in the source documents (GAP-3109; ASM-5349) and the row is bound to the reference-data contract and faked
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on another owner's schema, and the boundary test fails a build that adds one
    Then no fee-schedule and no service-level table is declared as owned, and both are named as reference data of rwb-case (ASM-5348)

  Scenario: AC5 The decision element is declared and no write, event, workflow or Schedule is (new, D-RCV-60)
    Given the decision section and the absence section of the document
    When they are compared with the decision-record library schema and the Ownership Map rows of S9
    Then one decision record is declared per panel version load or panel change, with the version reference, the rule ID, the package version, the inputs reference, the outcome and the decided-at time, written before the panel row changes
    Then the element declares the failure behaviour MSG-P7-003 and one healthy and one stopped chain in its stub
    Then the document declares no write operation, no event of EV-20 or EV-21, no workflow, no Schedule and no job, and the absence tests fail a build that adds one
    Then the document names InstructionIssued and PartnerResultSubmitted as the service's two events and as other keys' (ASM-5351)

  Scenario: AC6 The five fakes and the naming baseline answer the document and hold the boundary (new, D-RCV-60)
    Given the fakes and the naming section of the document
    When each fake is compared with the operation or the element it serves, and each name with the platform naming rule
    Then five fakes answer the rwb-case reference data, the decision-record chain, the service's own contract mock, the composite route and the access rights
    Then the drift test compares every fake with the document and fails the build on any difference
    Then the schema is rwb_partner, the login is rwb_partner, the topic is rwb.partner.events.v1, the queue is rwb-partner and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the document names lov_value, rule_row, decision_log_entry and every v_ace_* view as other owners' and consumes them only through their contracts
```

These six criteria are new under D-RCV-60 and test the artefact only. They restate no business outcome of RWB-S9-E6030-APP and copy no legacy criterion: the legacy criterion this key owns stays with the app slice word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The panel is rwb-partner's and the fragment declares its fields, its two lists and their required flags on the `Partner` element only | Context pack ownership rows; TSD S9 T3.1 and T3.2 |
| BR2 | The fee schedule, the service levels and the two lists are reference data of rwb-case: the document declares the version stamp and the consumed row, and no owned table for them | DP-07; Template and Rules v1 R3 default ruling; ASM-5348 |
| BR3 | The decision record is declared as an element written before the panel row changes, through the local library; a failed write changes nothing | DP-03; TSD S9 T2; legacy AC2 of RWB-E6-030 |
| BR4 | Two reads and no write: the fragment declares no maintenance operation, because the Ownership Map publishes none for the panel | Context pack ownership rows; GAP-3109; ASM-5350 |
| BR5 | Both reads declare Partner portal R with scope applied; no read answers a firm the caller does not own | TSD S9 T6.1 and T-A.2 |
| BR6 | No event is declared: EV-20 and EV-21 are the instruction events of TSD S9 T5.3 and belong to other keys | Context pack Events; ASM-5351 |
| BR7 | The vocabulary is closed and versioned: the two lists are published as enumerations bound to the version in force, and no list value is a constant of the document | TSD S9 T3.2; FSD S9 BR-S9-002 |
| BR8 | No personal data in a schema, an example or a fake: the firm's registration data, codes, instants and a version only | Template and Rules v1 §R7.2 s17 |
| BR9 | A change is additive inside major version 1; a removal, a rename or a retype opens a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |

### 9. State transitions

The lifecycle of the document, not of a partner:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the element, the lists, the stamp, the consumed row, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The panel app slice, the two screens, the placement and scorecard stories and the wave 4 harness accept the fragment and the fakes | Baselined |
| Baselined | Additive change | A property or a status is added inside major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a published enumeration changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | A write, a `v_ace_*` property, an event, a Schedule or a hard-coded list value | In review |

The panel statuses the document describes are the app slice's to drive, over `LOV-PANEL` ACTIVE, ON_NOTICE, SUSPENDED and EXITED; this baseline fixes the vocabulary and moves no record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change and confirms the reference-data placeholder and the version stamp (GAP-3109) |
| Consuming teams (the panel app slice, SCR-34 and SCR-35, the placement and scorecard stories and the wave 4 harness) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the naming rule, the reference-data client schema, the decision-record library and the composite route this document reuses |
| Data steward | Confirms that no personal data property is declared in an answer, an element or a fake |

### 11. Data

The baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Partner element | `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score` (DF-PRT-001 to DF-PRT-007) |
| Required flags | `id`, `partner_code`, `partner_name`, `partner_type` and `panel_status`; `contract_end` and `score` optional |
| Lists | `LOV-PANEL` (ACTIVE, ON_NOTICE, SUSPENDED, EXITED) and `LOV-PARTNER-TYPE` (AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC, RAMC), published as enumerations bound to a version |
| Reference-data stamp | `listCode`, `version`, `values[]`, `dataAsOf`, declared on every answer that names a list |
| Answers | `PartnerList` for API-S9-001 and `InstructionPage` for API-S9-003 |
| Decision record | The library element of DP-03, written before the panel row changes |
| Consumed fields | The list values of `lov_value` (DF-REF-027 to DF-REF-033) and the rule rows of `rule_row` (DF-REF-001 to DF-REF-015), read at the version in force and never copied |
| Not declared here | `partner_user`, `recovery_case`, `timer`, `decision_log_entry`, any fee-schedule or service-level table and every `v_ace_*` view |
| Consumed with no source | The operation name of the reference-data read and the status-to-message mapping: Not specified in the source documents (GAP-3109; ASM-5349, ASM-5361) |

No table, no column and no migration is declared by this story; the schema and its Flyway sequence belong to the DB story of this service (DP-15).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The two rows are this fragment's; the four partner-portal operations of the service baseline belong to the instruction stories (ASM-5359).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partners` | Query `type`, `status`; `PartnerList` out (API-S9-001) | Partner portal, right R, scope applied | Not applicable |
| GET | `/partner/instructions` | Query `status`, `page`, `size`; `InstructionPage` out (API-S9-003) | Partner portal, right R, scope applied | Not applicable |

Both answer 401, 403 with MSG-P4-002 and 503, each in the platform error envelope. The operation ids are those of TSD S9 T-A.1 and the paths are the target base, not the monolith form. No write operation is declared for the panel, the fee schedule or the service level (GAP-3109; ASM-5350).

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The reference-data list read; operation name Not specified in the source documents (GAP-3109; ASM-5349) | P3 rwb-case (RWB-P3-E1043-CON) | `LOV-PANEL`, `LOV-PARTNER-TYPE` and the schedule and level values behind them, returned with the version in force; faked |

One hop with a 2 s budget, one GET retried once with jitter and a breaker per downstream (DP-07, DP-11, ADR-020). The plan's C row for this key sits on the app slice and is RWB-P3-E1043-CON; the fragment declares the row as consumed against its placeholder until the owner publishes it.

#### 12.3 Events published

None. The Ownership Map gives S9 EV-20 and EV-21 and both are the instruction events `InstructionIssued` and `PartnerResultSubmitted` of TSD S9 T5.3, on `rwb.partner.events.v1`; this baseline declares no envelope, no producer group and no outbox row, and the absence test fails a build that adds one (GAP-3109; ASM-5351).

#### 12.4 Events consumed

None. The panel and its version are read on the reference-data contract and not from an event; this baseline declares no consumer group, no subscription and no inbox row.

#### 12.5 Workflows and activities

None. `InstructionWorkflow` is the one workflow the Ownership Map gives S9 and it belongs to the instruction stories; the panel version load runs as a service command in one transaction and crosses no Temporal boundary, so this baseline declares no workflow element and no activity element (ASM-5350).

#### 12.6 Schedules

None. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table; the Ownership Map gives S9 no job.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `partner` | S9, `rwb_partner` | The panel row and the element both reads answer from |
| `partner_instruction` | S9, `rwb_partner` | The instructions of the firm behind `InstructionPage` |
| `decision_record` | Platform library in `rwb_partner` | The local hash-linked record of the version load (DP-03) |

`partner_user`, `lov_value`, `rule_row`, `decision_log_entry`, `timer`, `recovery_case` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case reference-data fake | The two lists and the schedule values at a version; a superseded version; no answer inside 2 s | AC3, AC4 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| rwb-partner contract mock (this baseline's own fake) | `PartnerList` and `InstructionPage` for a synthetic firm; a refused scope; a stale version | AC1, AC2, AC3 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer | AC1, AC6 |
| rwb-access rights fake | Partner portal R held and not held | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The reference-data placeholder is carried until its owner confirms it (GAP-3109).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The two reads on `/api/recovery/partner/v1`; the rwb-case reference-data read; one hop, 2 s |
| Kafka | None | No event declared; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | None | No workflow, no activity and no Schedule declared |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/partner/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-03 and DP-07 are declared here as elements and consumed rows; their H and C rows sit on the app slice, because a CON story carries no build dependency (R5.7.1). DP-13 moves the base of the two reads. DP-19 puts the two screens behind the composite route.

**Deliverables.** The additive fragment `openapi/rwb-partner-panel-v1.yaml`, the `Partner`, `PartnerList`, `InstructionPage` and `ReferenceDataStamp` elements, the two lists as published enumerations, the contract README rows for the consumed reference-data placeholder, the decision-record element against the library schema, and the five WireMock mapping sets.

**Build steps.** (1) Write the two reads and validate the additive rule. (2) Write the elements, their required flags and the two lists. (3) Write the version stamp and its tests. (4) Record the consumed row with its owner, its budget and its placeholder. (5) Record the decision element and the absence section. (6) Publish the five fakes and the drift test. (7) Record the naming baseline and the absence tests, tag the baseline and collect the sign-off.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, the drift and absence tests are green, and the consumers have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of a read is absent, invalid or fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Partner portal right R the read declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the panel row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The status-to-message mapping is not published by any source: 403 is the legacy refusal with MSG-P4-002 and 503 the platform envelope, and the rest carry the platform's own conditions (GAP-3109; ASM-5361). The text of every message is the legacy and FSD S9 wording, copied unchanged.

### 15. Screens and states

| Screen | States served | What the baseline fixes |
|---|---|---|
| SCR-34 Partner list | Loading; list | The `PartnerList` answer with panel status, contract end, score and the version stamp on `GET /partners` |
| SCR-35 Placement and allocation | Loading; list | The same panel answer and the `InstructionPage` of `GET /partner/instructions` |

The composite route is RWB-PLT-N001-CON's and also calls rwb-case for the case and its owner; this baseline fixes the rwb-partner answers only. The refusal and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-030-01 | AC1, AC2 | Contract | The two reads of a synthetic panel; the contract half answers `PartnerList` with the element, its required flags and its two lists |
| TC-E6-030-02 | AC1, AC5 | Contract | The stopped decision-record stub; the contract half answers the MSG-P7-003 path of the element |
| TC-E6-030-03 | AC1, AC4 | Contract | A role without Partner portal R and a malformed query; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-030-04 | AC3, AC4 | Contract | The reference-data fake with a current version, a superseded version and no answer inside 2 s |
| TC-S9-E6030-CON-01 | AC1, AC2 | Contract | The fragment validates; the two reads, the base, the required flags, the two lists and the three statuses are present |
| TC-S9-E6030-CON-02 | AC3, AC5 | Contract | The stamp is on every list-bearing answer; the absence tests for a write, an event, a workflow, a Schedule and a hard-coded list value |
| TC-S9-E6030-CON-03 | AC4, AC6 | Contract | The consumed row and its placeholder; the five fakes match the document and a drifted fake fails the build |

The four legacy ids are the legacy cases of RWB-E6-030 in their legacy order, carried as the contract half: each Covers value names the criterion that fixes the surface it exercises, and its business outcome is proved by RWB-S9-E6030-APP. The legacy level of these cases is not published per case, so each is mapped to `Contract` because the artefact under test is the contract (GAP-3109; ASM-5357). `TC-S9-E6030-CON-01` to `-03` are new. The full test text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ids; the `-ITG` copies belong to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the panel statuses, the partner types, the schedule and the levels stay reference data bound to a version, never a schema default or a code constant.
- No personal data in a schema, an example or a fake: the firm's registration data, codes, instants and a version only; every example is synthetic.
- The reference data stays with rwb-case: no owned fee-schedule or service-level table, no `v_ace_*` path, no `recovery_case` property (BR2, BR4).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The fragment lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a write, a consumed event, a second topic, a workflow, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Legacy | Contract | Test |
|---|---|---|
| RWB-E6-030 AC2 | AC5 (the decision element whose failure it asserts) | TC-E6-030-02, TC-S9-E6030-CON-02 |
| RWB-E6-030 AC1 | AC1, AC2, AC4 (the shapes that carry the panel and its reference data) | TC-E6-030-01, TC-E6-030-04, TC-S9-E6030-CON-01 |
| RWB-E6-030 TC-03 Access | AC1 (the right declared on both reads) | TC-E6-030-03 |
| RWB-E6-030 TC-04 Principle 5 | AC3, AC5 (the version stamp and the decision element with their failure paths) | TC-S9-E6030-CON-02, TC-S9-E6030-CON-03 |

| Source | What it supplies |
|---|---|
| TSD S9 T3.1, T3.2, T6.1, T6.2 and T-A.1 | The element, the two lists, the rights and the two operations |
| FSD S9 A2.2, A1.1, Requirements served and Screens | The feature, its constraints, REQ-S9-001 and REQ-S9-004, VR-S9-002-1, BR-S9-002 and the two screens |
| Context pack S9 and the ownership rows | The schema, base, topic, queue, the three owned tables and the two instruction events |
| Template and Rules v1 R3, R5.5, R5.7 and R7.3 | The default ruling on reference data, DP-03, DP-07, DP-13, DP-19, the rule that a CON story carries no build dependency and the fill order whose step 4 is unavailable (ASM-5360) |
| Split plan, slice RWB-S9-E6030-CON | The lane, the wave, the release and the empty dependency rows (GAP-3109) |

### 19. Out of scope

- Any business outcome: the panel row, the version load and its decision record instance (RWB-S9-E6030-APP).
- The firm record, its portal users and the contract-end recall (RWB-S9-AD022-APP).
- The four partner-portal operations of the service baseline, which the instruction stories build and the service baseline declares (ASM-5359).
- The shapes of the notice, the review, the conduct check, the fee approval, the monthly scorecard and the contract exit - each belongs to its own story of this service.
- The reference data of rwb-case and its lists (rwb-case); the ledger and the rule rows (rwb-decision); the roles (rwb-access); the case of record (rwb-case).
- The schema, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key); the composite route and the platform libraries, which are RWB-PLT-N001-CON's and the platform's.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
