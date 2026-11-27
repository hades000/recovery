# RWB-S9-E6029-CON Onboard a partner and set terms - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6029-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of partner onboarding in rwb-partner, split from RWB-E6-029. It fixes the panel read API-S9-001 and the onboarding write on `/api/recovery/partner/v1` (DP-13), the `Partner` element with DF-PRT-001 to DF-PRT-007 and its required list, the two enumerations, the decision-record element of DP-03, the reference-data row, the rights of TSD S9 T6.1, the error set, the partner-gateway scope and the fakes. The write's method and path, the `partner_user` field list and the link between a partner and the version of its terms are not published by any source and carry the placeholder. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E6029-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of partner onboarding — the two operations on `/api/recovery/partner/v1`, the `Partner` element and its seven properties, the required list, the two enumerations, the decision-record element, the reference-data row, the rights, the error envelope and the fakes**, so that **the app story, SCR-34, SCR-35, the partner portal and the wave 4 harness build against one fixed, testable contract on Day 1, and a property or an answer shape can never drift between rwb-partner, rwb-case and rwb-decision without a failing build**.

It owns the surface only: it fixes shapes, rights and fakes and moves no row and no case. The behaviour behind the operations is RWB-S9-E6029-APP's, and AC1 of the legacy key is RWB-ITG-E6029-ITG's.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy onboarding crossed four boundaries at once: a partner portal screen, the panel rows, the decision log and the reference data of the panel. The target splits them: rwb-partner owns the partner and its portal users, rwb-case owns the reference data of the panel by default ruling, and rwb-decision owns the central ledger behind the local record. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the properties of `Partner` and their required list, the two published lists, the rights, the error envelope and the record.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition.

Three points are carried as gaps and assumptions rather than decided quietly: the onboarding write is not in the TSD inventory and its right is a mapping (ASM-5340); `partner_user` is S9's third table with no published field list (ASM-5343); and the fee schedule, the service levels and the scope have no linking column in `partner` (ASM-5341).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, topic, queue and event names follow the platform rule.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's. No table of another owner is declared here.
- The published shape of `EV-20` and `EV-21` is not part of this baseline; both belong to the instruction and result stories (ASM-5344).
- The `partner` and `partner_user` tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this feature: the panel read and the onboarding write, with their rights and error responses.
2. Fix the `Partner` element: the seven properties of DF-PRT-001 to DF-PRT-007, their types, their lengths and the required list the TSD gives.
3. Fix the two enumerations `LOV-PANEL` and `LOV-PARTNER-TYPE` as published lists, not as constants of a client (TSD S9 T3.2).
4. Fix the onboarding request element and the placeholder where the sources publish neither method nor path.
5. Record the decision-record element of DP-03, written before the row changes, and the reference-data row of the two lists.
6. Record the rights of TSD S9 T6.1, the naming baseline and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the required list, the enumerations, the `Idempotency-Key`, the error envelope, the absence of a `v_ace_*` read and of a case write, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S9-E6029-APP, SCR-34, SCR-35, the partner portal and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or answer body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a shape the sources do not give | The row carries the placeholder and the fake is derived from it | None | AC3, AC5 |
| X5 | A property or an enumeration is declared that no source publishes | The review fails the baseline and the absence test fails the build | None | AC2, AC5, AC7 |
| X6 | The document declares another service's operation, a `v_ace_*` view or a case row as its own | The review fails and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event of this feature or a second topic | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not those of TSD S9 T-A.1 and T6.1 | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S9 appendices and the published contracts only |
| Negotiable | The element names beyond the sources, the example values and the fixtures are settled in the baseline review; the base, topic, queue and schema are fixed |
| Valuable | Unblocks the app story, the two screens, the partner portal and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, four fakes and ten contract tests |
| Small | One sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of partner onboarding in rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_user is S9, of recovery_case is P3 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two operations are declared on the partner base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /partners answering Partner[] with the query filters type and status, and the onboarding write answering the Partner element, both under the base /api/recovery/partner/v1 and owned by rwb-partner
    Then the write declares the Idempotency-Key header and the repeated key answering the answer it created, and no path parameter beyond a future identifier
    Then the read answers 401, 403 and 503 as TSD S9 T-A.2 gives API-S9-001, and the write adds 409 and 422 with one envelope and one message ID per condition
    Then no instruction operation API-S9-002 to API-S9-006 is declared by this document

  Scenario: AC2 The Partner element and the two enumerations are fixed and no property is invented (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.1 and T3.2
    Then the Partner element declares id of format uuid, partnerCode of maximum length 20, partnerName of maximum length 160, partnerType of maximum length 15, panelStatus of maximum length 12, contractEnd of format date and score of the published numeric form
    Then the required list is partnerCode, partnerName, partnerType and panelStatus, and id in the answer, as the TSD gives the optionality of the seven fields
    Then partnerType is an enumeration of the eight values of LOV-PARTNER-TYPE and panelStatus an enumeration of the four values of LOV-PANEL, copied from TSD S9 T3.2
    Then no property is added for a fee schedule, a service level, a scope, a reference-data version or a contract start, because no source publishes one (GAP-3107; ASM-5341)
    Then the write's method and path are Not specified in the source documents (GAP-3107; ASM-5340) and carry the placeholder

  Scenario: AC3 The consumed reference-data row is declared and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the read of LOV-PANEL and LOV-PARTNER-TYPE is declared as consumed from P3 rwb-case, with the list code, the value and the version in force
    Then its operation name is Not specified in the source documents (GAP-3107; ASM-5345) and the row carries the placeholder
    Then the document declares no recovery_case property, no v_ace_* path and no grant on any rwb_* schema of another owner
    Then each consumed row is one hop with a 2 s budget and a breaker, and a GET is retried once with jitter (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T-A.1 and T6.1 and with the legacy permission table
    Then the read declares the capability area Partner portal with right R and scope applied
    Then the write declares right C, the create right of the CRUDA row of RW-AGENCYMG
    Then RW-AGENCYMG holds CRUDA, RW-HEADLIT, RW-HEADNPA and RW-HEADASL hold RA, the CRU and R roles hold what T6.1 gives them, and PT-AGENCY to PT-RAMC hold RU through the partner gateway
    Then a role without the right is described as refused with MSG-P4-002, and no wider right is declared for the write than the create right the table gives (ASM-5340)

  Scenario: AC5 The decision-record element and the portal user shape are declared with their placeholders (new, D-RCV-60)
    Given the decision and data sections of the baseline
    When they are compared with the library schema, TSD S9 T3.1 and the ownership rows of S9
    Then one decision record is declared per onboarding outcome with the partner code, the type, the panel status, the contract end, the two list versions, the outcome and the decided-at time
    Then the record is declared as written through the local library on rwb.decision-record.v1 before the partner row changes, and a failed write leaves the panel unchanged with MSG-P7-003
    Then the record carries no rule literal, no business value and no personal data
    Then partner_user is named as S9's third table with its field list Not specified in the source documents (GAP-3107; ASM-5343), and the portal scope follows NFR-050
    Then the document declares no table of this service beyond partner, partner_user and the library objects

  Scenario: AC6 The four fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the reference-data fake answers the four panel states and the eight types at their version, a value outside both and no answer beyond 2 s
    Then the decision-record stub answers a healthy chain and a stopped chain, the composite route fake answers SCR-34 in its loading and list states, and the partner-gateway fake scopes a firm's token to its own record
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the tables and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema and login are rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_user, decision_record, idempotency_key and outbox_event, and recovery_case, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this feature and no second topic, and it names InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21) as the sibling stories' (ASM-5344)
    Then the absence test fails a build that adds a published event, a second topic, a v_ace_* read, a case property or a terms column
```

These seven criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story, whose AC2 stays with the app story word for word and whose AC1 is RWB-ITG-E6029-ITG's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The panel is rwb-partner's: the contract declares the fields, the required list and the optionality of `Partner` and declares no other service's table | TSD S9 T3.1; ownership rows; DP-01 |
| BR2 | The decision record is declared as an element written before the row changes, through the local library; a failed write changes nothing | DP-03; TSD S9 T2; legacy AC2 |
| BR3 | The two lists are published enumerations copied from TSD S9 T3.2 and read at their version; no value is a constant of a client | BR-S9-001; ASM-5345 |
| BR4 | No case is declared: the contract declares no `recovery_case` property and no case write, and no ACE view is named as a source | DP-01, DP-05 |
| BR5 | The fee schedule, the service levels and the scope are reference data of FEAT-PRM-02; the contract declares no property and no link for them | FSD S9 A2.2; ASM-5341 |
| BR6 | No event is declared: `EV-20` and `EV-21` are the sibling stories', and DP-09 is not in the pattern set | TSD S9 T5.3; ASM-5344 |
| BR7 | A write declares the `Idempotency-Key` and stores its answer; no second topic and no second base is declared | TSD S9 T-A.2; DP-13, DP-14 |
| BR8 | No personal data in a schema, an example or a fake: a code, a firm's registered name, a type, a state and a date | Template and Rules §R7.2 (s17); NFR-050 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; no other service's base or topic is named as this one's | DP-13, DP-14; §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | ADR-020 |
| BR11 | The document lists only operations owned by rwb-partner; a consumed row is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The partner gateway scopes a firm's token to its own record; the baseline declares the scope and the edge owns the gateway | Architecture v5 slide 8; ASM-5346 |

### 9. State transitions

The lifecycle of this document, not of a partner:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operations, the element, the enumerations, the consumed row, the fakes and the record are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the partner portal and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the required list changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | An absence test of AC5 or AC7 fails | In review |

The state machine the document describes is the app story's: `ACTIVE`, `ON_NOTICE`, `SUSPENDED` and `EXITED` are `LOV-PANEL` values written by FEAT-PRM-01 and its siblings (TSD S9 T4 gives the module no case state machine). This baseline fixes the vocabulary and moves no row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the correction of the plan rows the baseline consumes, including the absent C row of the list read and the unplaced write operation |
| Consuming teams (the app story, SCR-34, SCR-35, the partner portal and the owners of rwb-case, rwb-access and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the gateway route this document reuses |
| Data steward | Confirms that no personal data field is declared in an element or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Partner element | `id` uuid, `partnerCode` varchar(20), `partnerName` varchar(160), `partnerType` varchar(15), `panelStatus` varchar(12), `contractEnd` date, `score` numeric(5,2), as DF-PRT-001 to DF-PRT-007 give them |
| Required list | `partnerCode`, `partnerName`, `partnerType` and `panelStatus`, and `id` in the answer; `contractEnd` and `score` are optional, as the TSD's required column gives them |
| Enumerations | `LOV-PANEL`: ACTIVE, ON_NOTICE, SUSPENDED, EXITED. `LOV-PARTNER-TYPE`: AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC, RAMC (TSD S9 T3.2) |
| Read filters | `type` and `status` of API-S9-001; the pagination of the platform, and no other parameter |
| Request element | The same seven properties; the element name, the method and the path are Not specified in the source documents (GAP-3107; ASM-5340) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Portal user | `partner_user` of S9 with its field list Not specified in the source documents (GAP-3107; ASM-5343); the scope follows NFR-050 |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `partner_instruction`'s instruction fields, a terms column and the later stories' data |

The field-level types of the request element are settled in the baseline review; this story fixes the property names, the required list, the enumerations and the additive rule of BR10. **No new table, no new column and no migration** is declared here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partners` | Query `type`, `status` in, `Partner[]` out (API-S9-001) | Partner portal, right R, scope applied | Not applicable |
| POST or PATCH | `/partners` (method and path Not specified in the source documents (GAP-3107; ASM-5340)) | The seven properties in, the `Partner` element of 201 or 200 out | Partner portal, right C, scope applied | `Idempotency-Key` header |

The read answers 401, 403 with MSG-P4-002 and 503 as TSD S9 T-A.2 gives API-S9-001; the write adds 404, 409 and 422 with MSG-GEN-001. API-S9-001 is also declared by RWB-S9-E6030-CON as the panel read of FEAT-PRM-02, so the two fragments must stay identical on its shape and this baseline adds the onboarding write; the instruction operations API-S9-002 to API-S9-006 are not declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use in the baseline |
|---|---|---|---|
| The reference-data read of `LOV-PANEL` and `LOV-PARTNER-TYPE` at their version (operation name Not specified in the source documents (GAP-3107; ASM-5345)) | `/api/recovery/case/v1` | P3 rwb-case | The list code, the value and the version in force that the two enumerations are validated against; faked |

One hop, 2 s, one GET retry with jitter and a breaker (ADR-020). The row is class C in fact while the plan's C row is None, and the absence is recorded (ASM-5345). The decision record is not a call: it is the DP-03 library on `rwb.decision-record.v1`, carried as RWB-PLT-E1027-CON.

#### 12.3 Events published

None. The service owns `rwb.partner.events.v1` with its retry and `.dlt` topics, and its event set carries `InstructionIssued` (`EV-20`, `instructionId`, `partnerId`, `type`, `dueOn`), which the instruction story publishes. Onboarding publishes nothing, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one (ASM-5344).

#### 12.4 Events consumed

None of this feature's own. `PartnerResultSubmitted` (`EV-21`, `instructionId`, `result`, `documents`) is consumed from the partner portal by RWB-S9-E6033-APP, and its target name `rwb.partner.PartnerResultSubmitted.v1` follows §R4 and is published in no catalogue (ASM-5344).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow per instruction, the child of `CaseWorkflow` in the stages that instruct a partner | `rwb-partner` in `rwb-recovery` | The service's only workflow (ownership rows); declared, not built and not registered here |
| None | Activity | `rwb-partner` | Onboarding is a synchronous command; no activity and no child workflow is declared |

#### 12.6 Schedules

None. The ownership rows give S9 no job, and no clock is declared: the contract end is a date and the recall it may start is RWB-S9-E7015-APP's under R-UNI-26. This baseline registers no Schedule and creates no Quartz row or shared job table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm on the panel, its fields, its required list and the two enumerations |
| partner_user | S9 (`rwb_partner`) | The portal user of the firm; shape not published (ASM-5343) |
| decision_record | PLT library, in `rwb_partner` | The local record of the onboarding (DP-03) |
| idempotency_key | PLT library, in `rwb_partner` | The key of the repeat and the answer it holds |
| outbox_event | PLT library, in `rwb_partner` | Present; this feature declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5) and `partner_instruction`'s instruction fields are not owned by this baseline and are named only as other owners' facts. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Reference-data fake | The four panel states and the eight types at their version; a value outside both; no answer beyond 2 s | AC1, AC3, AC6 |
| Local decision-record stub | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-34 answer, loading and list | AC6 |
| Partner-gateway fake | The firm's own scope, and a token of another firm refused | AC4, AC6 |

The fakes are test-only and are replaced by the real services in SIT; the consumed row keeps its placeholder until its owner confirms it (GAP-3107; ASM-5345).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | `GET /partners` and the onboarding write on `/api/recovery/partner/v1`; the list read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `EV-20` and `EV-21` are the sibling stories' |
| Temporal | 1 workflow declared, 0 registered | `InstructionWorkflow` on `rwb-partner` |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no partner, no row and no case. What it publishes is one OpenAPI 3.1 document, nine contract tables and four fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element written before the row changes; DP-13 moves the base and nothing else; DP-19 sits behind SCR-34 and SCR-35, whose screen model is the edge contract's. DP-07 and DP-09 are not in the pattern set: the lists are declared as a consumed row and the event set as the siblings' (GAP-3107; ASM-5344, ASM-5345).

**Dependencies the tables add and the plan does not hold.** The pattern table adds two H rows the plan already carries; it leaves out `RWB-PLT-E1043-CON` and `C RWB-P3-E1043-CON` of the list read, and `RWB-PLT-TE006-CON` of the outbox and inbox library. The consumed list row is a C dependency in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the `Partner` element, the required list, the lengths and the two enumerations of AC2, with the write's placeholder.
3. Record the consumed list row of AC3 with its owner, its budget and its placeholder.
4. Record the rights and the error envelope of AC4.
5. Record the decision-record element, the `partner_user` shape and its placeholder of AC5.
6. Publish the four fakes of AC6 and the drift test.
7. Record the naming baseline, the tables and the boundary of AC7, then tag the baseline and collect the sign-off.

The deliverables are `openapi/rwb-partner-v1.yaml`, the two elements, the contract README rows for the consumed row and its placeholder, and the fakes of 12.8.

**Done when.** The document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens, the partner portal and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are contract elements and the text is the legacy and FSD wording, copied unchanged. The 409 of a duplicate `partner_code` has no message ID in any source and is not bound to one here (GAP-3107).

### 15. Screens and states

The contract serves SCR-34 Partner list and SCR-35 Placement and allocation in their loading and list states through the gateway-bff composite route (DP-19), and the same operations to a firm through the partner gateway on FAPI 2.0, scoped to its own record (ASM-5346). This baseline fixes the rwb-partner answers only; the route specification and the screen field list belong to RWB-PLT-N001-CON and the edge stories. The refusal, invalid and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-029-01 | AC1, AC2 | Contract | The two operations, the `Partner` element, the required list, the lengths and the two enumerations; the contract half of the onboarding answer |
| TC-E6-029-02 | AC5, AC7 | Contract | The decision-record element and the absence of a published event; the contract half of the not-recorded path |
| TC-E6-029-03 | AC4 | Contract | A role without right C, and a firm token of another firm refused; 403 with MSG-P4-002 |
| TC-E6-029-04 | AC3, AC4 | Contract | The consumed list row and its placeholder; the rights of T6.1 and the envelope of the error set |
| TC-S9-E6029-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the `Idempotency-Key` and the error answers are present |
| TC-S9-E6029-CON-02 | AC2 | Contract | The element, the required list, the lengths and the two enumerations validate, and the write carries its placeholder |
| TC-S9-E6029-CON-03 | AC3, AC4 | Contract | The consumed row and its placeholder; the no-`recovery_case`, no-`v_ace_*` and no-other-base boundary |
| TC-S9-E6029-CON-04 | AC5, AC6 | Contract | The record element matches the library schema; the four fakes match the document and a drifted fake fails the build |
| TC-S9-E6029-CON-05 | AC7 | Contract | The naming baseline, the tables owned, and the absence of a published event, a second topic and a terms column |

The four legacy cases keep their IDs and order and are carried as the contract half: their Covers column names the criterion that fixes the surface each one exercises, and the business outcome of each is proved by RWB-S9-E6029-APP and, for AC1, by RWB-ITG-E6029-ITG. The five cases `TC-S9-E6029-CON-01` to `-05` are new, and no `-ITG` copy is written here.

### 17. Guardrails

- No business value in the contract: the states, the types, the required fields and the contract end are enumerations and properties, never a schema default or a branch of a client.
- No personal data in a schema, an example or a fake: a code, a firm's registered name, a type, a state and a date, with synthetic examples (s17, NFR-050).
- The case stays with rwb-case and the facts with their owners: no `recovery_case` property, no `v_ace_*` path and no other service's base or topic named as this one's (DP-05, DP-13, DP-14).
- The money and the instruction data stay with rwb-payment and the instruction stories: no invoice, result or proceeds property is declared here.
- The schedule stays declarative: this story registers no Schedule and creates no Quartz row or job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the gateway route come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-001 to REQ-S9-004, REQ-S9-008 | The partner is onboarded with its terms and the result recorded (FSD S9 A2.1, TSD S9 T8); the plan carries no requirement id for this slice (GAP-3107) | The element, the required list, the two enumerations and the consumed row | TC-E6-029-01, TC-E6-029-03, TC-S9-E6029-CON-01, TC-S9-E6029-CON-02 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E6029-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as the siblings' | TC-S9-E6029-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two operations and the consumed row with their budget and breaker | TC-S9-E6029-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S9-E6029-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-029, disposition Split (rework); feature FEAT-PRM-01 |
| Legacy criteria | AC2 owned word for word by RWB-S9-E6029-APP, AC1 by RWB-ITG-E6029-ITG; this baseline copies neither |
| Source text | Legacy RWB-E6-029; FSD S9 Partner management v3 A2.1 and A2.1.4; TSD S9 Partner management v2 T2, T3.1, T3.2, T6.1, T7 and T-A; API Specification v5, `Partner`; context pack S9 rows |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S9-E6029-CON-01 to -05 |
| Feature and screens | FEAT-PRM-01, SCR-34 Partner list and SCR-35 Placement and allocation |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the operations, the `partner` and `partner_user` rows, the record and the screen fragments: RWB-S9-E6029-APP.
- AC1 of the legacy key and its cross-service journey: RWB-ITG-E6029-ITG.
- The panel, the fee schedule and the service levels as versioned reference data: RWB-S9-E6030-APP (FEAT-PRM-02).
- The instruction operations API-S9-002 to API-S9-006 and `EV-20` and `EV-21`: the instruction and result stories of this service.
- The case of record (P3), the access rows (P4), documents (P5) and notices (P6).
- The link between a partner and the version of its terms (GAP-3107; ASM-5341) and the `partner_user` field list (ASM-5343).
- The partner gateway itself and its identity provider: the edge, not this baseline (ASM-5346). The composite route of SCR-34 and SCR-35: RWB-PLT-N001-CON.
- The deployment of this service, its flag, its dashboards and its runbook: the operations story of this key.
