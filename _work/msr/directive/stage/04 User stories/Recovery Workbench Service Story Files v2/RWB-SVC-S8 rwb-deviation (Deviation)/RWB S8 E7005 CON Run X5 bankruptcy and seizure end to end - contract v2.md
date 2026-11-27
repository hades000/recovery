# RWB-S8-E7005-CON Run X5 bankruptcy and seizure end to end - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7005-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E7005-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (base `/api/recovery/deviation/v1`) |
| Integration dependencies | rwb-integration carries the outside effects to Aric, NCB, EFS, LIT, SVAF and the partner portal, each as a contract dependency built against the published fake; no direct call from this service; interface identities Not specified in the source documents (GAP-1821) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E7-005 for rwb-deviation (S8). The deviation is published on Day 1 on base `/api/recovery/deviation/v1` (DP-13) with the two operations API-S8-001 and API-S8-002, the `DeviationRequest`, `Deviation` and `DeviationOutcome` schemas, the `deviation` DDL template, the `Idempotency-Key` rule, the decision-record element of DP-03, the case announcement shape, the two event payload shapes, the fakes and the drift test; the legacy acceptance criteria stay with RWB-S8-E7005-APP and RWB-ITG-E7005-ITG and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E7005-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 6 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-deviation (S8)**, I want **the published contract of the deviation resource as it carries the X5 bankruptcy and seizure case — the base `/api/recovery/deviation/v1` with API-S8-001 create and API-S8-002 patch, the `DeviationRequest`, `Deviation` and `DeviationOutcome` schemas with the fields DF-CAS-036 to DF-CAS-045, the `deviation` DDL template, the `Idempotency-Key` rule, the error envelope, the declared right of each operation, the decision-record element, the case announcement shape, the payload shapes of `DeviationRaised` and `DeviationCleared`, the fakes and the drift test** instead of the monolith's in-process controller and its one `recovery.deviation` table reached by a single base, so that **`RWB-S8-E7005-APP` and every other X1 to X7 story of this service build against one frozen, testable shape from Day 1, and a state, a code, a list value or an error status can never drift between rwb-deviation, rwb-case, rwb-litigation and rwb-comms without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 document of the deviation resource: the base, the two operations, the three object schemas, the problem schema, the security and the error set;
- the element set and the required set of the `Deviation` schema from DF-CAS-036 to DF-CAS-045 of TSD S8 T3.1, with the three list references of T3.2;
- the X5 sub-shape: `deviationCode = X5` required on the create, the paused state and the contact stop required, the handler and the outcome optional, and the outcome patch;
- the `deviation` DDL template with the columns, types and widths of TSD S8 T3.1 and the seven standard columns of T3.0, applied in this service's own schema, with no cross-schema key;
- the `Idempotency-Key` rule on the create and on the patch, the compatibility rule and the pinning rule;
- the shapes this service hands to rwb-case and reads back, and the payload shapes of the two events the catalogue assigns to this service;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the deviation. The evaluation of R-DEV-01, R-DEV-05 and R-DEV-15, the row write, the two durable timers, the case announcement and the event publication are `RWB-S8-E7005-APP`'s; the case, its stage clock and the work assignment are rwb-case's; the filing with the official receiver or the LED and the legal action are rwb-litigation's; and the contact stop belongs to rwb-comms's consumption of the same events. The document declares shapes and moves nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the deviation service has one base and one document for its deviations. The legacy key RWB-E7-005 wrote the deviation, the assignment, the timer, the legal action, the recovery case, the document and the decision log entry in one process against one `recovery` schema, with the base shared by every module. Five of those objects are now other services' rows and the two list vocabularies are reference data of a sixth, so each shape has to be fixed before the app story starts: the two operations and their bodies, the element set of the row, the columns a deviation writes, the decision record the service writes in its own transaction, the announcement it hands to rwb-case, and the two events it publishes.

The deviation is not several resources. TSD S8 gives one `deviation` table, one code list with seven values of which `X5` is one, one raised-by list with four values and one outcome list with three, and one DEVIATION machine with 22 rules over nine states. The X5 case is a deviation of that code, so a second resource, a second table or a per-code schema would fork the vocabulary and the state machine. This document therefore fixes the code, its required fields, its states and its outcome inside the one existing resource — which is also why no new column is invented here, and why the index set has to be carried as a gap rather than guessed (GAP-3060; ASM-5176).

The baseline also fixes the naming the checks require: schema `rwb_deviation`, login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1`, event names `rwb.deviation.<Event>.v1`, task queue `rwb-deviation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.deviation`. It keeps the operation IDs the TSD allocates, API-S8-001 and API-S8-002, which are also the two operations the legacy endpoint block names, so no operation is renumbered.

Three contested points are carried as gaps rather than decided quietly. The case contract publishes no operation name for the pause, the resume or the route fact, and Architecture v5 gives rwb-deviation no REST edge to rwb-litigation, so how the filing fact and the case answers travel is named but unfixed (GAP-3060; ASM-5177). The two event payloads are given three fields each by the Event and Messaging Design and no envelope schema, and DP-09 is not in this key's pattern set, so the outbox behind them is not in the metadata (GAP-3060; ASM-5179). And the mapping from the three outcome values to the states of TSD S8 T4 is stated nowhere (GAP-3060; ASM-5178).

It serves FEAT-DVF-05 "Run X5 bankruptcy and seizure end to end" through the shape of its deviation, and it traces to that feature until the Epics 3 to 8 PRD adds requirement identifiers, because the legacy master, the Epics 3 to 8 specification and TSD S8 T8 carry none for this key (GAP-3059; ASM-5170).

The object also keeps the DF-CAS identifier range of the data dictionary although this service owns it: the range is copied, not renumbered, and no source gives the deviation a range of its own (GAP-3060; ASM-5181).
The 400 and 409 refusals of API-S8-001 and API-S8-002 each carry a message-ID slot; the text of those two messages is Not specified in the source documents (GAP-3060).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the event names and the package follow the platform rule and not a local choice.
- The platform error envelope and its `messageId` extension are the platform baseline; where this document narrows them it does so explicitly. The envelope, its member names and its extension are reused and never redeclared.
- The reference lists of the deviation are the data of rwb-case and are read with their version: LOV-DEVIATION (`X1`, `X2`, `X3`, `X4`, `X5`, `X6`, `X7`), LOV-RAISED-BY (`SCREENING_AGENT`, `RULE`, `OFFICER`, `CUSTOMER_CONTACT`) and LOV-DEV-OUTCOME (`RETURNED`, `RE_ROUTED`, `CASE_ENDED`) of TSD S8 T3.2. The document names the list codes and their members as the TSD enumerates them, and the version in force is read at run time.
- The `deviation` row and its columns are the TSD S8 T3.1 row, DF-CAS-036 to DF-CAS-045, plus the seven standard columns of T3.0. No field outside that row is declared, because no source gives one for a deviation.
- The decision record is the local decision-record library's, `RWB-PLT-E1027-CON`, and its shape is not fixed here: this document names the element it needs and points to the library.
- The case contract of rwb-case is the document this baseline reads for the announcement shape it hands over; its operation and event names are absent (GAP-3060; ASM-5177).
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7 rule 1), and every consuming story of the service builds against it and its fake.
- The FSD S8 v3 and the TSD S8 v2 this baseline reads are In review with an empty sign-off table, and this document is not signed off either. The run of D-RCV-60 has no human approval step, so both slices of the key carry Status Draft (realignment v1) and the missing approval is recorded rather than waited for (GAP-3060; ASM-5175).

### 4. Flow

1. Draft the OpenAPI 3.1 document of the deviation resource on base `/api/recovery/deviation/v1`: API-S8-001 and API-S8-002 with their request and answer bodies, their rights and their error sets.
2. Fix the `Deviation` element set from DF-CAS-036 to DF-CAS-045 in camelCase, with the required set of TSD S8 T3.1 and the three list references of T3.2.
3. Fix the X5 sub-shape: `deviationCode = X5` required on the create with `raisedBy`, `pausedState` and `contactStop`, `handlerUserId` optional on the create and on the patch, and the outcome patch with `outcome`, `clearedAt` and the state the case returns to.
4. Write the `deviation` DDL template with the columns, the physical types, the widths, the keys and the standard columns; carry the index set as a gap.
5. Write the decision-record element and the case announcement shape this service hands over, with the placeholder on the operation names.
6. Write the payload shapes of `DeviationRaised` and `DeviationCleared` from the three fields each event carries, in the CloudEvents envelope of the naming rule.
7. Write the `Idempotency-Key` rule on the create, the versioning rule, the compatibility rule and the pinning rule.
8. Generate the fake set from the document and wire the drift test into the build of this story, of `RWB-S8-E7005-APP` and of every other X1 to X7 story of the service.
9. Publish v1 and record the pinned version of each consuming story.
10. Hand the baseline to `RWB-S8-E7005-APP`, to the sibling S8 stories that read the same resource, and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC8 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A value of `deviationCode`, `raisedBy` or `outcome` outside its list is sent | The document refuses it as an enumeration error at 422 and no row is written | MSG-GEN-001 | AC2 |
| X5 | The create is called without the `Idempotency-Key` header | The document refuses the request at 400 and the fake answers the same; no stored answer exists | None | AC4 |
| X6 | The document declares an operation of another service, a second base or a read of another service's table | The review fails the baseline; a consumed shape is described as consumed, never as provided | None | AC8 |
| X7 | The index set of `deviation` is guessed | The template carries the placeholder and the gap, and declares only the primary key | None | AC3 |
| X8 | A retired element reappears in the document | The absence test fails: no old monolith base, no second topic, no `recovery` schema and no legal-action field | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the TSD S8 and the platform envelopes only, and consumes no service |
| Negotiable | The index set, the case operation names, the outcome mapping and the outbox are settled with their owners; the base, the operation IDs, the columns and the list codes are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the other six deviation stories, which read the same resource and the same two events |
| Estimable | One OpenAPI document, one DDL template, three hand-over shapes, one fake set and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the deviation that carries X5 bankruptcy and seizure

  Background:
    Given the service naming rule of the platform library is in force
    Given the deviation of rwb-deviation is served on the base /api/recovery/deviation/v1
    Given the reference lists are LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME of TSD S8 T3.2, read with their version in force

  Scenario: AC1 The two deviation operations are declared with their legacy IDs and their schemas (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/deviations as API-S8-001 and PATCH /deviations/{deviationId} as API-S8-002, both under the base /api/recovery/deviation/v1 and owned by rwb-deviation
    Then the Deviation schema carries id, caseId, deviationCode, raisedAt, raisedBy, pausedState, handlerUserId, contactStop, clearedAt and outcome
    Then deviationCode names LOV-DEVIATION with its seven values, raisedBy names LOV-RAISED-BY with its four values and outcome names LOV-DEV-OUTCOME with its three values
    Then the document declares no second base, no second resource and no operation of another service
    Then every operation ID of TSD S8 T-A.1 is kept and no operation is renumbered

  Scenario: AC2 The X5 create, its answer and the outcome patch are fixed as shapes (new, D-RCV-60)
    Given the DeviationRequest, Deviation and DeviationOutcome schemas of the document
    When the X5 sub-shape is reviewed
    Then DeviationRequest requires deviationCode with X5 among the values of LOV-DEVIATION, raisedBy, pausedState and contactStop, and carries caseId from the path and handlerUserId as optional
    Then the create answers 201 with Deviation in state DEV_FLAGGED, and the answer carries the identifiers, the code, the raised date, the paused state and the contact stop of the row it wrote
    Then DeviationOutcome carries outcome of LOV-DEV-OUTCOME, clearedAt and the state the case returns to, and the patch answers 200 with the row in DEV_RESOLVED, DEV_REROUTE or CASE_ENDED
    Then no element of the request or the answer names a table, a column or a value outside TSD S8 T3.1, T3.2 and T4, and no separate resource is declared per deviation code
    Then a value of deviationCode, raisedBy or outcome outside its list is refused at 422 with MSG-GEN-001 naming the property
    Then the state element names the DEVIATION machine values of TSD S8 T4 and never a case state of rwb-case

  Scenario: AC3 The deviation columns and their indexes are declared and no column is added (new, D-RCV-60)
    Given the deviation DDL template of schema rwb_deviation
    When it is compared with TSD S8 T3.1 and T3.0
    Then the template declares DF-CAS-036 to DF-CAS-045 with their physical types, widths and required flags, and the seven standard columns
    Then case_id and handler_user_id are identifiers with no foreign key across schemas
    Then state is varchar(40) against the DEVIATION values of TSD S8 T4, deviation_code is varchar(3) against LOV-DEVIATION, raised_by is varchar(20) against LOV-RAISED-BY and outcome is varchar(20) against LOV-DEV-OUTCOME, each closed by its list and not by a check constraint of its members
    Then the index set beyond the primary key on id is Not specified in the source documents (GAP-3060; ASM-5176) and the template declares the primary key only
    Then the template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15)
    Then no table and no column outside this row is declared, and the holding of a written table is a new major version

  Scenario: AC4 The Idempotency-Key rule, the error envelope and the declared right of each operation are fixed (new, D-RCV-60)
    Given the operation table of the document
    When it is reviewed against TSD S8 T-A.1 and T-A.2
    Then API-S8-001 declares the Idempotency-Key header and a stored answer, and API-S8-002 declares no Idempotency-Key
    Then the error responses are 401, 403, 404, 409, 422 and 503 as the TSD rows give them, each with the platform problem document and one message ID per condition
    Then a body that cannot be parsed answers 400 with the same envelope, a code no S8 T-A row names and carried as a gap (GAP-3060; ASM-5180)
    Then the declared right is Case record U on both operations, with the scope applied and the role lists held by rwb-access
    Then a caller without the right is refused at 403 with MSG-P4-002 and changes nothing
    Then the document declares no right of its own invention and no role code as a constant

  Scenario: AC5 The decision-record element handed to the local library is fixed (new, D-RCV-60)
    Given the decision element of the document and the record format of DP-03
    When it is compared with RWB-PLT-E1027-CON
    Then the document names the decision record as the local library's element on the shared topic rwb.decision-record.v1 with the decision code, the rule ID, the rule version, the inputs reference, the final call, the decided time and the two hashes, and fixes none of the library's own fields
    Then the rule ID carries R-DEV-05 or R-DEV-15 and the version in force, and the decision code is read as a value of LOV-DECISION
    Then the record is written before the deviation changes, and a stopped chain leaves the row unchanged and answers 503 with MSG-P7-003
    Then the claim deadline of R-DEV-05 and the service level of R-DEV-20 are not fixed by the document: both are versioned reference rows and their values are Not specified in the source documents (GAP-3059; ASM-5171)
    Then no field of decision_log_entry of rwb-decision and no rule row is declared or written by this service

  Scenario: AC6 The case announcement shape and the two event payloads are fixed (new, D-RCV-60)
    Given the case element of the document and the event section
    When it is compared with R-DEV-01, R-DEV-15, R-DEV-19 and the event catalogue
    Then the announcement this service hands over carries the case reference, the deviation reference, the deviation code, the paused state, the rule ID and the version in force, and the outcome on a clear
    Then the answer shape carries the accepted or refused outcome and the state the case of record holds, and no case field is written here
    Then the operation name of the announcement and the field list of its answer are Not specified in the source documents (GAP-3060; ASM-5177)
    Then DeviationRaised carries caseid, deviationcode and raisedby and DeviationCleared carries caseid, deviationcode and outcome, each with the event name rwb.deviation.<Event>.v1 on rwb.deviation.events.v1
    Then the document declares no subscription of this service to rwb-litigation, rwb-decision or rwb-comms, because Architecture v5 slide 13 gives this service no such edge
    Then the document fixes no transition of the case and no case rule

  Scenario: AC7 The contract fakes answer the document and the drift test blocks a drifted build (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation or the element it serves
    Then the deviation fake answers the 201 create, the 200 patch, the 400, 401, 403, 404, 409, 422 and 503 refusals, and the repeated Idempotency-Key
    Then the case fake answers the accepted pause, the accepted route fact, the refusal from another state and a delayed answer
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the reference-data fake answers LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME at their version in force
    Then the event fake answers the two topic payloads in the CloudEvents envelope and a repeated delivery
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the boundary of the document are fixed (new, D-RCV-60)
    Given the naming and boundary section of the document
    When it is reviewed against the Template and Rules and the Ownership Map
    Then the base is /api/recovery/deviation/v1, the schema and the login are rwb_deviation, the topic is rwb.deviation.events.v1, the event names are rwb.deviation.<Event>.v1, the task queue is rwb-deviation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the document declares no read of another service's table, no cross-schema join and no v_ace_ view, and it names recovery_case, assignment, timer, legal_action, document, decision_log_entry and rule_row as other owners' consumed shapes only
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then the document names no second topic, no second queue, no `recovery` schema and no batch table
    Then the service owns one table, deviation, and the document declares no second table of its own
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome of `RWB-S8-E7005-APP` and they copy no criterion of the legacy story. The wave 4 harness that consumes this baseline copies none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/deviation/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | The two operations keep their TSD operation IDs API-S8-001 and API-S8-002, and no third operation of this resource is declared | TSD S8 T-A.1; legacy Endpoints block |
| BR3 | `deviation_code`, `raised_by` and `outcome` are declared as enumerations of LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME, and the code names the list, never a member list curated locally | TSD S8 T3.2; FSD S8 A2.14.3.1 (BR-S8-014) |
| BR4 | The state element names the DEVIATION values of TSD S8 T4 and never a case state of rwb-case; `DEV_FLAGGED`, `DEV_WITH_OWNER` and `DEV_REROUTE` are the deviation's | TSD S8 T4; legacy AC2 and AC3 |
| BR5 | A read declares no `Idempotency-Key`; the create declares it and stores its answer | TSD S8 T-A.1; Architecture v5 platform baseline |
| BR6 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules section R7.2 (s14) |
| BR7 | A schema change is additive within a major version; a breaking change is a new major version, and the holding of a written table is a breaking change | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR8 | The document lists only operations owned by rwb-deviation; a consumed operation or shape is described as consumed, never as provided | Ownership Map v1 |
| BR9 | The case, its stage clock and its work assignment are rwb-case's and the contact stop is rwb-comms's consumption of the same events; the document declares the announcement shape and no case field | R-DEV-01; Architecture v5 slide 13 (no S8 edge to S4, P6 or P7) |
| BR10 | No business value is fixed in the contract: the claim deadline, the service level, the Legal handler route, the index set and the list members stay data or reference data | TSD S8 T3.2; Template and Rules section R7.2 (s17) |
| BR11 | The decision record is the local library's element on the shared topic, never a new event of this service, and its fields are the library's | DP-03; Architecture v5 slide 42 (event 08) |
| BR12 | No personal data in a schema, an example or a fake: identifiers, list values, codes and dates only | TSD S8 T3.1; Architecture v5 slides 42 and 43 notes |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the X5 shape, the template and the hand-over shapes are described | In review |
| In review | Consumer sign-off | `RWB-S8-E7005-APP` and the sibling S8 stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a second field of the outcome patch | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, a column of the template changes, a list code changes or the state set changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

Three vocabularies are declared and none is moved here:

| Object | Values | Note |
|---|---|---|
| deviation.deviation_code | `X1`, `X2`, `X3`, `X4`, `X5`, `X6`, `X7` (LOV-DEVIATION) | Declared as the list reference; X5 is the code this key carries |
| deviation.raised_by | `SCREENING_AGENT`, `RULE`, `OFFICER`, `CUSTOMER_CONTACT` (LOV-RAISED-BY) | Declared as the list reference |
| deviation.outcome | `RETURNED`, `RE_ROUTED`, `CASE_ENDED` (LOV-DEV-OUTCOME) | Declared as the list reference; which of the three leaves which state is the app story's |
| deviation.state | `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE`, `DEV_RESOLVED`, `DEV_REJECTED`, `RESUMED`, `ROUTE_D6`, `CASE_ENDED` (TSD S8 T4) | Declared as the state set; the 22 moves between the values are the app story's |

The mapping from the three outcome values to the states of the DEVIATION machine is not given by any source read for this key, so the document names both vocabularies and fixes no pair: the mapping is Not specified in the source documents (GAP-3060; ASM-5178). The case's own states are rwb-case's and appear in this document only as the `pausedState` value the caller supplies, which is a copy of a case state and not a case transition.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI document, the DDL template and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (`RWB-S8-E7005-APP`, the other X1 to X7 stories of this service, and the rwb-case and rwb-comms owners whose shapes are declared) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the naming rule, the outbox library and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, an example or a fake |
| Business analyst of S8 | Confirms that the three lists and the state set are named as list codes and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_deviation` by the naming rule of DP-02; the document names the scheme and not a credential, and no role, level or mask is defined here. Each operation is authorised through the rwb-access authorise check of DP-08 with the right given in section 16 (TC-S8-E7005-CON-03); the check's operation name is Not specified in the source documents (DOR-RWB-S8-E7005-CON-6).

The contract has no screen of its own. The empty, loading, error and no-access states of SCR-06 and SCR-08 belong to RWB-S8-E7005-APP; section 15 lists them as Not specified in the source documents (DOR-RWB-S8-E7005-CON-10).

### 11. Data

The contract baseline declares shapes, not business values. The five rows of the second table below carry no BR Field ID because they are contract notes, not fields; the field rows are DF-CAS-036 to DF-CAS-045. Reference data read by this contract is named here: the three lists LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME, read under the reference-data contract of DP-06 and DP-07; the three parameters are the claim deadline, the service level and the Legal handler route, carried as versioned reference rows with the placeholder (GAP-3059).

| BR Field ID | Element | Type and width | Required | List |
|---|---|---|---|---|
| DF-CAS-036 | id | uuid | Yes | None |
| DF-CAS-037 | caseId | uuid | Yes | None |
| DF-CAS-038 | deviationCode | varchar(3) | Yes | LOV-DEVIATION |
| DF-CAS-039 | raisedAt | timestamptz | Yes | None |
| DF-CAS-040 | raisedBy | varchar(20) | Yes | LOV-RAISED-BY |
| DF-CAS-041 | pausedState | varchar(60) | Yes | None |
| DF-CAS-042 | handlerUserId | uuid | No | None |
| DF-CAS-043 | contactStop | boolean | Yes | None |
| DF-CAS-044 | clearedAt | timestamptz | No | None |
| DF-CAS-045 | outcome | varchar(20) | No | LOV-DEV-OUTCOME |
| T3.0 standard columns | state, version, created_at, created_by, updated_at, updated_by, is_active | boolean, varchar(40), integer, timestamptz, uuid | n/a | None |

| Item | Content |
|---|---|
| X5 sub-shape | `deviationCode = X5` required on the create; `raisedBy`, `pausedState` and `contactStop` required; `handlerUserId` optional on the create and on the patch; the outcome patch carries `outcome`, `clearedAt` and the state the case returns to |
| Index set | Beyond the primary key on `id` the set is Not specified in the source documents (GAP-3060; ASM-5176); the template declares the primary key only and the app story's two lookups are named there |
| Decision record | The element the library writes: the decision code, the rule ID and version, the inputs reference, the final call, the decided time and the two hashes. The library owns the fields and the chain (DP-03) |
| Case announcement | The shape handed to rwb-case with the case and deviation references, the code, the paused state, the rule and its version, and the answer read back; the operation name is absent (GAP-3060; ASM-5177) |
| Event payloads | `DeviationRaised`: `caseId`, `deviationCode`, `raisedBy`. `DeviationCleared`: `caseId`, `deviationCode`, `outcome`. Three fields each, as the Event and Messaging Design gives them; the outbox behind them is carried as GAP-3060 |

**No new table, no new column and no migration.** `deviation` is the TSD S8 T3.1 row and this document publishes its DDL template for the service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_deviation` by the library's migration and are named here, not declared. `recovery_case`, `assignment` and `timer` (rwb-case, P3), `legal_action` (S4), `document` (P5), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are other owners' and are named as consumed shapes only. `deviation.case_id` and `handler_user_id` are identifiers, not foreign keys across schemas (DP-01). The object keeps the DF-CAS identifier range of the dictionary although this service owns it; the range is copied, not renumbered (GAP-3060; ASM-5181).

**No personal data.** No element of this contract carries a name, an address, an identity number or an account number. The deviation code, the raised-by code, the state the case paused in and the outcome are not personal data, and the borrower is reached by the services that need it through rwb-source-data and never through this resource. The only identifier of a person is `handlerUserId`, a uuid platform user identifier with no name, address, identity number or account number; it is an identifier and not personal data under the data steward's confirmation in section 10. The X5 values that no source gives are carried as versioned reference rows with the placeholder (GAP-3059); the Case record is declared U on both operations, the widening of RW-LEGAL is left to rwb-access, the two catalogue events go through the platform outbox, and both slices are traced to FEAT-DVF-05 until the PRD adds identifiers.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). This story publishes both operations.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S8-001 | POST | `/cases/{caseId}/deviations` | `DeviationRequest`; `caseId` from the path; `deviationCode = X5` for this key | 201 with `Deviation` in state `DEV_FLAGGED` | Case record U, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S8-002 | PATCH | `/deviations/{deviationId}` | `DeviationOutcome` | 200 with `Deviation` | Case record U, scope applied | Not applicable | 401, 403, 404, 409, 422, 503 |

The purpose, request and response entities, rights and error statuses are those of TSD S8 T-A.1 and T-A.2 for API-S8-001 and API-S8-002, with the base renamed by DP-13. The service owns no third operation and no read operation: the queue of SCR-08 is read from the same two shapes through the composite route and the case list is rwb-case's.

#### 12.2 REST operations consumed

None: a contract document calls no service. The row below is the shape this service **hands over** and the answer it reads back; the document declares it, and the call is `RWB-S8-E7005-APP`'s.

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The case announcement and its answer | P3 rwb-case | The pause, the resume and the route fact with the rule and its version, and the accepted or refused answer | The operation name and the field list of the answer are Not specified in the source documents (GAP-3060; ASM-5177) |

The declaration is one hop with a 2 s timeout in the app story's implementation (ADR-020). No operation of another service is declared as provided here (BR8), and no call from rwb-deviation to rwb-litigation, rwb-decision or rwb-comms is declared, because Architecture v5 slide 13 gives this service no such edge (BR9).

#### 12.3 Events published

| Event | Topic | Payload | Consumer |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | `caseid`, `deviationcode`, `raisedby` | The timers that pause the stage clock, and communications for the contact stop |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | `caseid`, `deviationcode`, `outcome` | The timers that resume the stage clock, and communications |

The two events are the catalogue's (Event and Messaging Design v5; Architecture v5 slides 19 and 43 give rwb-deviation its topic), and this document fixes their names and payload shapes only. The document publishes nothing itself: the producer and its outbox row are `RWB-S8-E7005-APP`'s, and DP-09 is not in this key's pattern set, so the platform outbox story is not in the metadata and the point is carried as GAP-3060 with ASM-5179. The decision record is the local library's element on `rwb.decision-record.v1` (DP-03) and is not an event of this service.

#### 12.4 Events consumed

None by this document. The two case events the app story consumes — the filing fact `BANKRUPTCY_FILED` and the answers of the case announcement — are rwb-case's events on `rwb.case.events.v1`; their names are Not specified in the source documents (GAP-3060; ASM-5177), and the document declares no subscription and no inbox of its own.

#### 12.5 Workflows and activities

None. The document defines no workflow and no activity. `DeviationWorkflow` is the app story's, on task queue `rwb-deviation` in namespace `rwb-recovery`, with a child run per open deviation that can start at any time and pauses the stage clock (Temporal design slides 8 and 13); this baseline fixes only the names the app story registers, and the workflow's own type name and ID scheme are the design's.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared; the claim deadline of R-DEV-05 and the 10 working days of R-DEV-20 are durable timers of `DeviationWorkflow` and not Schedules of this service. The service owns no job (Ownership Map v1: jobs 0).

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| deviation | `rwb_deviation` | S8 | The DDL template of section 11: DF-CAS-036 to DF-CAS-045, the seven standard columns, the primary key on `id` and no cross-schema key (DP-01, DP-15) |
| decision_record | `rwb_deviation` | PLT library object applied in this schema | Named only: the shape is `RWB-PLT-E1027-CON`'s and the row is written in the caller's transaction (DP-03) |
| idempotency_key | `rwb_deviation` | PLT library object applied in this schema | Named only: the stored answer of the create |

The service owns one table. `recovery_case`, `assignment` and `timer` (P3), `legal_action` (S4), `document` (P5), `decision_log_entry` and `rule_row` (P7) are other owners' and appear only as consumed shapes. No table of another service is declared, read or keyed, and no `recovery` schema object is named as a table of this service.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Deviation fake | The two operations of 12.1 | A 201 create in state `DEV_FLAGGED`, a 200 patch to `DEV_RESOLVED` or `DEV_REROUTE`, and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second deviation |
| Case fake | The announcement shape of 12.2 | The pause accepted, the route fact accepted, the refusal from another state, and a delayed answer |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Reference-data fake | The three lists of 12.3 and section 11 | LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME at their version in force, and the claim-deadline and SLA rows at theirs |
| Event fake | The two payloads of 12.3 | `DeviationRaised` and `DeviationCleared` in the CloudEvents envelope, and a repeated delivery for the inbox test |
| Template application | The `deviation` DDL template | The table created twice in two throwaway schemas, with the standard columns, the primary key and no cross-schema reference |
| Drift test | Every fake against the document | A drifted fake fails the build |

The case fake is stubbed from the published documents of its owner and carries the placeholder until the missing operation name is confirmed (GAP-3060; ASM-5177).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed by this document | API-S8-001 and API-S8-002 provided; the case announcement of 12.2 is declared for the app story and called by nobody here |
| Kafka | 2 shapes declared, 0 published by this document | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; the producer and the outbox are the app story's (12.3) |
| Temporal | None | No workflow, activity or Schedule; `DeviationWorkflow` and its two durable timers are the app story's (12.5, 12.6) |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the deviation resource, the `DeviationRequest`, `Deviation` and `DeviationOutcome` schemas with the published types in `th.co.scb.ace.workbench.recovery.deviation.api`, the `deviation` DDL template as a resource, and the fake set with the drift test. The implementation behind it is `RWB-S8-E7005-APP`.

**This document declares shapes and moves nothing.** It fixes the names, the types, the widths, the required set, the list references, the `Idempotency-Key` rule, the two event payloads and the answer this service hands over. It writes no row, raises no deviation, pauses no clock, publishes no event and files nothing: every one of those acts is an application behaviour of `RWB-S8-E7005-APP`, and a contract that performed one would be a second implementation of the story. The DEVIATION state machine — which event moves `deviation.state` and what a refused step leaves on the row — is the app story's and is described in its section 9 only; this document states the vocabulary and the shapes and fixes no transition. The case's own pause and re-route are rwb-case's and are declared here as an announcement shape only.

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity and case | `id`, `caseId`, `pausedState` | all three yes |
| Code and origin | `deviationCode`, `raisedBy`, `raisedAt` | all three yes, the first two against their lists |
| Handling | `handlerUserId`, `contactStop` | `contactStop` yes, `handlerUserId` no |
| Clearing | `clearedAt`, `outcome` | no, each optional; `outcome` against its list |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-CAS field names in camelCase; the mapping is one to one and is checked by the drift test. No element exists for a deviation beyond this row, because no source gives one.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/deviation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-19 is the route the two screens use and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template as the schema and migration rules and add no dependency. DP-07 is not in this story's pattern set although three list codes are named; the lists are read as values in force through the reference data of rwb-case, and that read carries no dependency row (GAP-3060; ASM-5177). DP-09 is not in the set either, although two events are declared, and the outbox is carried as GAP-3060 with ASM-5179.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DeviationOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR7, BR12) |
| DeviationSchema | Published schema | `DeviationRequest`, `Deviation` and `DeviationOutcome` with the DF-CAS elements, the required set and the X5 sub-shape (BR3, BR4) |
| DeviationDdlTemplate | Resource | The `deviation` DDL: columns, types, keys, the primary key and the standard columns (BR3, BR10) |
| ProblemEnvelope | Reused schema | The platform problem document with the `messageId` extension (BR6) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR5) |
| HandOverShapes | Document | The case announcement with the placeholder on its operation name, and the two event payloads (BR9) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC7) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC7, AC8) |

**Database.** The template creates `deviation` in `rwb_deviation` only, with the physical types of TSD S8 T3.1 and the standard columns of T3.0. `case_id` and `handler_user_id` are identifiers with no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). The index set is carried as a gap and the primary key on `id` is the only index declared.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR3). The state set of the DEVIATION machine is named and the moves are the app story's (BR4). The right of each operation is declared and its role list is rwb-access data. The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the two operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the required set, the enumeration rule and an example; validate the example (AC2).
3. Write the `deviation` DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key (AC3).
4. Write the error section with the problem envelope and one message ID per condition, and the `Idempotency-Key` rule of the create (AC4).
5. Write the decision element and the case announcement shape with its placeholder, and the two event payloads (AC5, AC6).
6. Write the naming and boundary section and the absence tests for the old base, the second topic, the `recovery` schema and another service's table (AC8).
7. Generate the fake set and the drift test, and wire the drift test into the build of `RWB-S8-E7005-APP` and the sibling S8 stories (AC7).
8. Publish v1 and record the pinned version of this contract and of each consuming story (AC8).

**Feature flag.** `rwb.deviation.contract-v1`.

**Done when.** The document lints, the three schemas validate, the template applies twice, the fakes answer every status including the conflict and the repeated key, the drift test is green on the build of this story and of `RWB-S8-E7005-APP`, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing, or a value is outside its list (X4) | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written by the consuming story | 503 on the create and on the outcome patch, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S8-001 | Carried from the legacy message set of this key. It names the deviation and the handler on the raise, which the consuming story displays, so no path of this document raises it | Not raised here | {deviation} was raised. The case is with {handler}. |

The four texts are the legacy wording of RWB-E7-005 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the property it names. The 400, 401, 404, 409 and the platform 503 carry the platform problem document and no business message of this set, and the 400 code is not named by any S8 T-A row (GAP-3060; ASM-5180). The 409's message text is not stated in any source read for this key, so the document fixes only its status, its cause and its `messageId` slot.

### 15. Screens and states

No screen is built in this story. The contract serves two surfaces read through the gateway-bff composite route (DP-19), and it fixes the answer fields they read and nothing of their layout:

| Screen | State | What the contract serves |
|---|---|---|
| SCR-08 Deviation queue | Loading | Nothing: the placeholder while the route answers |
| SCR-08 Deviation queue | List | The X5 deviations of the case with `deviationCode`, `handlerUserId`, `raisedAt`, `pausedState`, `contactStop`, `clearedAt`, `outcome` and `state` |
| SCR-06 Raise deviation | Form | The create answer with the code, the raised-by, the paused state and the contact stop |
| SCR-06 Raise deviation | Saved | The 201 answer of API-S8-001 and the state `DEV_FLAGGED` |
| SCR-06 Raise deviation | Refused | The 403 with MSG-P4-002, and the 409 or 422 of a refused request |
| SCR-06 Raise deviation | Empty | Not specified in the source documents (CG-ALL-11557) |
| SCR-06 Raise deviation | Loading | Not specified in the source documents (CG-ALL-11557) |
| SCR-06 Raise deviation | Error | Not specified in the source documents (CG-ALL-11557) |
| SCR-06 Raise deviation | No access | Not specified in the source documents (CG-ALL-11557) |
| SCR-08 Deviation queue | Not recorded | The 503 with MSG-P7-003 |
| SCR-08 Deviation queue | Empty | Not specified in the source documents (CG-ALL-11558) |
| SCR-08 Deviation queue | Error | Not specified in the source documents (CG-ALL-11558) |
| SCR-08 Deviation queue | No access | Not specified in the source documents (CG-ALL-11558) |

The two screens and their `Loading; list` and `Form; saved` states are the ones the legacy screen block of RWB-E7-005 gives, copied unchanged. The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`; the transition behind each state is the app story's, and the case state the queue shows next to the deviation is rwb-case's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-005-01 | AC1, AC2 | Contract | The contract half of the legacy run: the create in state `DEV_FLAGGED`, the answer fields, the patch and the `X5` value of `deviationCode` |
| TC-E7-005-02 | AC1, AC5, AC6 | Contract | The contract half of R-DEV-05: the announcement shape with the rule and its version, the deadline as a reference row, and the accepted or refused answer |
| TC-E7-005-03 | AC1, AC6 | Contract | The contract half of R-DEV-15: the `BANKRUPTCY_FILED` trigger shape, the outcome `RE_ROUTED` and the route fact of `DEV_REROUTE` |
| TC-E7-005-04 | AC4, AC5 | Contract | The contract half of the not-recorded case: the library element, the 503 with MSG-P7-003 and the refused chain of the stub |
| TC-E7-005-05 | AC4 | Contract | The contract half of the access case: Case record U declared on both operations, and the 403 with MSG-P4-002 |
| TC-E7-005-06 | AC5, AC7 | Contract | The contract half of the forced-failure case: the stopped chain of the library stub and the drift test on a consuming build |
| TC-S8-E7005-CON-01 | AC1, AC2, AC8 | Contract | The document linted: the base, the two operation IDs, the Deviation elements, the X5 sub-shape, the three lists, the absence of the old base, of a second topic, of the `recovery` schema and of another service's table |
| TC-S8-E7005-CON-02 | AC3 | Component | The template applied in two throwaway schemas; DF-CAS-036 to DF-CAS-045, the standard columns, the types, the widths, the primary key and the absence of a cross-schema key asserted; a drifted hand-written table refused |
| TC-S8-E7005-CON-03 | AC4 | Contract | One problem body per status on each operation, the six statuses of the TSD rows, the 400 carried as a gap, the right per operation and the `Idempotency-Key` required on the create and refused absent |
| TC-S8-E7005-CON-04 | AC5, AC6, AC7 | Contract | The decision element, the announcement shape with its placeholder, the two event payloads in the CloudEvents envelope, the seven fakes against the document, and a drifted fake failing the build |
| TC-S8-E7005-CON-05 | AC3 | Component | Boundary of the section 12.7 tables: only `deviation`, `decision_record` and `idempotency_key` are created in two throwaway schemas; a table named in no row of section 12.7 is refused, and no cross-schema key is present |
| TC-S8-E7005-CON-06 | BR1 to BR12 (section 8) | Contract | Each business rule of section 8 asserted by the document lint, the fakes and the drift test; a rule without an assertion fails the build |
| TC-S8-E7005-CON-07 | AC9 | Contract | The rules BR1 to BR12 of section 8 checked for an assertion, as in TC-S8-E7005-CON-06; the proposed test is Not specified in the source documents (NEWAC-RWB-S8-E7005-CON-AC9) |

The first six identifiers are the legacy identifiers of RWB-E7-005 in their legacy order, carried here as the **contract half** of each case: they assert the shape each surface needs and not the business outcome, which `RWB-S8-E7005-APP` proves and `RWB-ITG-E7005-ITG` proves across the services. The seven `TC-S8-E7005-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The harness for RWB-ITG-E7005-ITG (SIT base hosts, fixture layout, synthetic case, deviation and legal-action keys, stub answer shapes, evidence format and retention, pass or fail gate) is Not specified in the source documents (GAP-0470); it is agreed at the wave 4 entry check, recorded in the harness README, and no business value is hard-coded.

### 17. Guardrails

- No business value in the contract: the claim deadline, the service level, the Legal handler route, the index set and the list members stay data or reference data, and no role code, list value or state member is written in code.
- No personal data in a schema, an example or a fake: identifiers, codes, list values and dates only.
- The contract names only `rwb_deviation` tables and only operations owned by rwb-deviation; the case announcement is a consumed shape, never a provided operation (DP-01, BR8).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No ACE view and no ACE table is declared or read, and no `recovery` schema object is named as a table of this service (DP-05, BR12).
- No workflow, no Schedule and no outbox row is declared by this document; the decision record is the library's element (12.3, 12.5, 12.6).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the index set, the case operation name, the outcome mapping, the outbox and the 400 code.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-3059; ASM-5170) | The X5 deviation is recorded, routed to Legal, held to its deadline and re-routed after the receiver reports | FEAT-DVF-05 | 04 Handle special situations | The two operations, the X5 sub-shape, the `deviation` template, the announcement shape and the two events | TC-E7-005-01 to TC-E7-005-06, TC-S8-E7005-CON-01 to TC-S8-E7005-CON-04 |
| FEAT-DVF-05 | Run X5 bankruptcy and seizure end to end | FEAT-DVF-05 | 04 Handle special situations | `deviationCode = X5`, the deadline row and the route fact of `DEV_REROUTE` | TC-S8-E7005-CON-01, TC-S8-E7005-CON-04 |
| R-DEV-05, R-DEV-15 | Assign to Legal and file before the deadline; route to litigation and then write-off after the receiver reports | FEAT-DVF-05 | 04 Handle special situations | The announcement shape, the rule ID and version of the decision element, and the outcome patch | TC-E7-005-02, TC-E7-005-03, TC-S8-E7005-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-005, disposition Split (rework) |
| Legacy criteria | AC2, AC3 and AC4 of the legacy story, owned by RWB-S8-E7005-APP; AC1 is owned by RWB-ITG-E7005-ITG; this baseline copies none of them |
| Legacy test cases | TC-E7-005-01 to TC-E7-005-06, carried here as the contract half of each surface |
| Requirement | The legacy master, the Epics 3 to 8 specification and TSD S8 T8 carry no REQ identifier for this feature, so both stories trace to FEAT-DVF-05 until the PRD adds the identifiers (GAP-3059). TSD S8 T8 does name REQ-S8-001 to REQ-S8-007 against FEAT-DVF-01, which is the X1 story of the same module |
| Screens | SCR-08 Deviation queue and SCR-06 Raise deviation, read through the gateway-bff composite route (DP-19) |
| Sibling slice | RWB-S8-E7005-APP: the two rule evaluations, the row, the two timers, the announcement and the two events |
| Sibling slices of the service | The X1 to X7 stories of this service, the screening stories of Epic 2, and the contract baselines `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON` it reuses |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the rule evaluation, the workflow, the activities, the row write and the announcement: `RWB-S8-E7005-APP`.
- The DEVIATION state machine, which event moves the deviation and what a refused step leaves on the row: `RWB-S8-E7005-APP` section 9.
- The case of record, its stage clock, its prescription clock, its work assignment and its case states: rwb-case (P3).
- The filing with the official receiver or the LED, the legal action and its court references: rwb-litigation (S4) and its own stories; this service has no edge to it.
- The contact stop, the letters and the calls raised by `DeviationRaised` and `DeviationCleared`: rwb-comms (P6).
- The central ledger, the rule packages and the rule registry: rwb-decision (P7); the local record is `RWB-PLT-E1027-CON`'s.
- The evidence pack and its documents: rwb-document (P5).
- The screening agent that may raise the flag: rwb-agent (P10) and the Epic 2 screening stories.
- The other six deviation codes: the sibling S8 stories, which read this same document and these same fakes.
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-08 and SCR-06: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, the chart values, the schema, the login and the flag: its own OPS story.
- The cross-service proof of the document against the live owners: the wave 4 integration harness.
