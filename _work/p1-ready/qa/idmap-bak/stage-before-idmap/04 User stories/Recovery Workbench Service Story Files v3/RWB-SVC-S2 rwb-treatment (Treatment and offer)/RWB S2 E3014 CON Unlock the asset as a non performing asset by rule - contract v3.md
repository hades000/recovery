# RWB-S2-E3014-CON Unlock the asset as a non performing asset by rule - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-014 for rwb-treatment (S2). The asset-unlock decision is published on Day 1 as the `AssetUnlock` element of the treatment representation on base `/api/recovery/treatment/v1` (DP-13), with its value rules, its decision-record group, the no-new-table rule, the compatibility rule and the fakes; the four legacy acceptance criteria stay with RWB-S2-E3014-APP, and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S2-E3014-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3014-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not set in the story; the squad sizes it at refinement |
| Contract version | v1, base path /api/recovery/treatment/v1 (DP-13) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the asset-unlock decision — the `AssetUnlock` element of the treatment representation (`inspectionOutcome`, `unlockDecision`, `unlockDecidedAt`, `assetRef`, `ruleId`, `ruleVersion`), its required set and its value rules with the from-states and event codes of R-DIL-22 and R-DIL-23, the decision-record group with decision code D6.4, the rule that no new table is created for the inspection, the unlock or the release, the read right, the compatibility rule and the fakes** instead of the monolith's `recovery_case.status` move, its direct read of `v_ace_npa_asset` and its `decision_log_entry` row in the one shared `recovery` schema, so that **RWB-S2-E3014-APP, the deed-in-lieu stage of RWB-S2-E3012-APP and the wave 2 harness build and test on Day 1 against one frozen answer, and no team adds a table for the unlock**.

This story owns one element and nothing else:

- the element's field list, its required set, its types and its value rules, mapping each field to the `treatment` column it is recorded on or to the request context it comes from;
- the trigger rule of R-DIL-22 (from WITH_FIELD_INSPECTION, event INSPECTION_COMPLETED, condition checklist, photographs and bills captured) and the answer rule of R-DIL-23 (from ASSET_UNLOCK_DECISION, event AUTO_UNLOCK_PASSED, condition that the unlock rule passes in about 95% of cases), with their target states as the case reports them and not as this service writes them;
- the decision-record group: decision code D6.4, the rule ID, the package version and the two library exceptions;
- the no-new-table rule, the no-ACE-view rule and the no-event rule of the release, each with the owner of the fact named;
- the read right under the capability area "Treatment and offer", the compatibility and pinning rule, and the fakes with the drift test.
- the screen states of SCR-14 and SCR-16 (empty, loading, error, no access): owned by the screen owners, not this story.

It does not own: the unlock step, the activity, the repository, the four columns and the tests against them, which are RWB-S2-E3014-APP; the treatment resource and its operations, which are RWB-S2-E3001-CON; the deed-in-lieu element set beyond this element — the transfer price, the asset reference of the transfer and its instant — which is RWB-S2-E3012-CON; the offer and draft-terms operations, which are RWB-S2-E3002-CON and RWB-S2-E3003-CON; the case status, the case task and the case signal, which are rwb-case's (P3); the DEEDINLIEU package, its rows and its version, which are rwb-decision's (P7); the ACE NPA-asset read, which is rwb-source-data's (P1); the asset record and the asset list, which are rwb-asset's (S5); the roles and scope data, which are rwb-access's (P4); the composite route and the screen field list, which are the platform edge story's and the screen owners'.

### 2. Business rationale

The monolith had no contract for the unlock: the S2 service moved `recovery_case.status` itself, read `v_ace_npa_asset` from the `recovery` schema, compared the inspection facts with the rule and wrote `decision_log_entry` in the same schema (FSD S2 A2.14.2; TSD S2 T2 and T3.1). Nothing about that arrangement could be tested alone or reused, and three different readers of the answer existed: the officer's screen, the transfer step that follows the case, and the asset list that FEAT-AST-02 fills. In the 19-service target each of them needs the same answer from one place, and none of them may read a table of this service or of another.

D-RCV-60 replaces three inputs and one output, and this document is where each is written down. The case status and the inspection capture become a fact of the case signal the parent forwards (ASM-4401). The NPA-asset facts become rwb-source-data's, and because the connection matrix gives rwb-treatment no call to rwb-source-data, they too arrive as facts and no `v_ace_*` view is read here (DP-05; ASM-4402). The decision becomes a local record in the same transaction through RWB-PLT-E1027-CON (DP-03; ADR-022). The output becomes an element with a field list, a required flag on each field, a value rule and a set of fakes.

The contract has to exist before the code for two reasons. The deed-in-lieu stage and the unlock step are two stories that must agree on one answer before either is written, or the treatment row grows two pairs of columns. And the no-new-table rule is what keeps the unlock from becoming a `treatment_unlock` (a refused name, not a dictionary object) or an `inspection` table: the inspection capture is already a document of rwb-document and a fact of the signal, and the answer already belongs on the treatment row next to the record that says which rule and which version produced it.

The division of the legacy key is fixed. This WP delivers the **contract**; the **implementation** is RWB-S2-E3014-APP and the **cross-service proof** is RWB-ITG-W2. The four legacy acceptance criteria **stay with RWB-S2-E3014-APP** and are not copied here: every criterion in section 7 is new (D-RCV-60) and tests only the contract deliverable in this title. The fake is the Day-1 unblocker: the unlock step, the stage and the harness prove the pass, the fail and the rollback before a live rwb-case, rwb-decision or rwb-asset exists.

### 3. Preconditions

- R-DIL-22 and R-DIL-23 fix the trigger and the answer, character for character: WITH_FIELD_INSPECTION, INSPECTION_COMPLETED, "checklist, photographs and bills captured", "Run the asset unlock rule", ASSET_UNLOCK_DECISION; ASSET_UNLOCK_DECISION, AUTO_UNLOCK_PASSED, "unlock rule passes, about 95% of cases", "Release the asset for transfer", AWAITING_TRANSFER (Business Rules and Routing Logic v4).
- TSD S2 T4 carries the same two rows in the DEEDINLIEU state machine, so the from-state, the event and the target state are the ones the source lists and not this contract's invention.
- TSD S2 T3.1 fixes DF-TRT-001 to DF-TRT-033 and gives the inspection, the unlock answer, the unlock instant and the asset reference no field and no column; TSD S2 T3.0 fixes the seven standard record columns of the table the element is recorded on (GAP-2677; ASM-4405).
- FSD S2 A2.14.3.1 names the decision code D6.4 in the rule workbook's decision-point column and BR-S2-014 fixes that no value a business person may change is written in code; the decision code, the event codes and the state names are therefore values in force (ASM-4406).
- The consumer reads the element on the treatment representation of RWB-S2-E3001-CON, whose read operation declares right R of the capability area "Treatment and offer" and whose errors are 401, 403, 404 and 503 with the RFC 9457 problem body (TSD S2 T-A.1, API-S2-002; TSD S2 T6.1).
- The decision record is the platform library's: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; this document names the writer and declares no record element of its own (DP-03).
- The screens reach the element through the gateway-bff composite route, so the contract fixes the element and declares no path and no route (DP-19; RWB-PLT-N001-CON).
- No source names an event for the unlock or the release and no source gives the element a field list, so both are the working read of this document (GAP-2677; ASM-4405; ASM-4407).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), it sits in contract group CG-W2 and it is published at status Draft (realignment v1), the source FSD and TSD being in review with no PRD yet (ASM-4408).

### 4. Flow

1. The contract author fixes the element: `inspectionOutcome`, `unlockDecision`, `unlockDecidedAt`, `assetRef`, `ruleId` and `ruleVersion`, with the column or the request context each maps to and the required flag each carries.
2. The author fixes the value rules: `unlockDecision` carries the event code the package returned and names no member of a list the contract holds; `inspectionOutcome` carries the capture fact of the signal; `assetRef` carries the reference of the NPA-asset facts of DF-ACE-208 to DF-ACE-219 and copies no other field.
3. The author fixes the trigger and the answer sections with the two routing rows verbatim, their from-states, their events, their conditions and the target states they report.
4. The author writes the boundary section: the case status is rwb-case's, the asset record and the asset list are rwb-asset's, the package and the ledger are P7's, the capture is rwb-document's, and no event is published.
5. The author writes the decision-record group with decision code D6.4, the rule ID and the package version, and the failure rule that joins the caller's transaction.
6. The author writes the read right, the versioning and pinning section: an added optional element keeps major version 1, a renamed or removed element or a changed value rule raises major version 2 under a new base segment.
7. The lint and schema steps run: the field names compared with the treatment representation and the TSD, the values compared with the routing workbook, and the example scanned for personal data.
8. The fake set is generated from the document: a complete element, one per missing required field, the pass, the fail, the incomplete capture and the two library exceptions.
9. The drift test is generated and wired into the build of RWB-S2-E3014-APP and of RWB-S2-E3012-APP.
10. The document and the fakes are published at v1, and the pinned version of this contract and of each consuming story is recorded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A team adds a `treatment_unlock` (a refused name, not a dictionary object) or an `inspection` table, or a second write path for the answer | The boundary and drift checks fail the build; the element is the only published shape of the answer | None | AC1 |
| X2 | An element is named after anything other than the published name, or a required element is published optional | The schema validation fails the build | None | AC1 |
| X3 | The trigger or the answer is published with a from-state, an event or a condition other than the two rows of R-DIL-22 and R-DIL-23 | The rule lint fails the build | None | AC2 |
| X4 | The element is declared on a path of its own, or a case status or an asset element is declared in it | The boundary test fails the build | None | AC3 |
| X5 | The record is declared with a propagation other than `MANDATORY`, or a refusal is published as an ordinary answer | The record lint and the drift test fail the build; a failure rolls the caller's transaction back | MSG-P7-003 | AC4 |
| X6 | A published element is removed, renamed or retyped, or a value rule changes under version 1 | The change raises major version 2 under a new base segment; v1 is never edited in place | None | AC5 |
| X7 | A consuming build ships without the drift test, or ships a private variant of an element | The registry refuses the change and the drift test fails the build | None | AC6 |
| X8 | A value the consumer needs is fixed by no source — the field list of the element, the value domain of `unlockDecision` or the announcement of the release | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2677; ASM-4405) | AC7 |

X1 to X7 are the boundary, schema, rule, envelope, record, versioning and drift failures of a contract build; X8 is the boundary this key records, because the source fixes the two rules and nothing about the shape of the answer.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes an element, a value rule and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The field order, the example values, the widths and the fake technology are open until v1 is frozen; the field names, the required set, the two rules, the decision code and the no-new-table rule are fixed |
| Valuable | Unblocks the unlock step, the deed-in-lieu stage and the wave 2 harness on Day 1 and keeps a second shape of the answer out of the service plan |
| Estimable | One element, two value rules, one decision-record group, one boundary section and one fake set |
| Small | One sprint for the document, the fakes and the drift test |
| Testable | Each criterion of section 7 is one schema, rule-lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the asset-unlock decision contract of rwb-treatment

  Background:
    Given the contract document is published with major version 1 on the base of rwb-treatment
    Given the treatment of a case is owned by rwb-treatment in schema rwb_treatment
    Given the case status stays rwb-case's and reaches the step on the case signal

  Scenario: AC1 The AssetUnlock element and its required set are published, and no table is created (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated against the treatment representation, the TSD and the routing workbook
    Then it publishes AssetUnlock with inspectionOutcome, unlockDecision, unlockDecidedAt, assetRef, ruleId and ruleVersion
    Then inspectionOutcome, unlockDecision and unlockDecidedAt are required once the step has run, and assetRef, ruleId and ruleVersion are optional
    Then inspectionOutcome, unlockDecision, unlockDecidedAt and assetRef record on the treatment row of rwb_treatment, and ruleId and ruleVersion mirror the decision record
    Then the document declares that no table is created for the inspection, the unlock or the release, and names decision_record as the library object of DP-03 and the asset as rwb-asset's
    Then a document that adds a treatment_unlock or an inspection table, or drops a required element, fails the schema and boundary checks

  Scenario: AC2 The trigger and the answer are fixed with the values of the two rules (new, D-RCV-60)
    Given the rule section of the contract document
    When it is linted against R-DIL-22 and R-DIL-23
    Then the trigger is a case in WITH_FIELD_INSPECTION with the event INSPECTION_COMPLETED and the condition checklist, photographs and bills captured, and the target state it reports is ASSET_UNLOCK_DECISION
    Then the answer is a case in ASSET_UNLOCK_DECISION with the event AUTO_UNLOCK_PASSED and the condition that the unlock rule passes in about 95% of cases, and the target state it reports is AWAITING_TRANSFER
    Then unlockDecision carries the event code the package returned and names no member of a list this contract holds
    Then the decision code D6.4 and the package version are carried on the element and on the record, and no threshold is stated as a value of this contract
    Then a published rule with another from-state, event or condition fails the lint

  Scenario: AC3 The element rides the treatment representation, declares no path and no event, and carries right R (new, D-RCV-60)
    Given the boundary and access section of the document
    When it is linted against the treatment resource and the connection matrix
    Then the element is a component of the treatment representation of RWB-S2-E3001-CON on GET /treatments/{treatmentId} and the contract declares no path and no new operation
    Then the read right is Treatment and offer R under the scope rule, and the document declares no role list and no check of its own
    Then the document declares no case status, no case table, no asset record, no capture element and no event for the unlock or the release
    Then it names the case status as rwb-case's, the asset record and the asset list as rwb-asset's, the capture as rwb-document's, the package and the ledger as P7's and the ACE facts as rwb-source-data's
    Then a document that declares a path of its own, a case status element or an unlock event fails the boundary test

  Scenario: AC4 The decision-record group is fixed and a failure leaves no change (new, D-RCV-60)
    Given the record section of the document
    When a pass, a fail and a failed write are put through it
    Then the record is written through DecisionRecordWriter with decision code D6.4, the rule ID and the package version in force
    Then the propagation is MANDATORY, so the record joins the caller's transaction with the treatment columns and the outbox row
    Then a refused field answers MSG-P7-009 with the field name and a failed write answers MSG-P7-003, and in both cases nothing changes
    Then the central decision_log_entry is named as P7's ledger and is neither written nor read by the consumer

  Scenario: AC5 A compatible change keeps major version 1 and a breaking change raises version 2 (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element or to a value rule
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a removed or renamed element, a new required element, a changed value rule or a path change raises major version 2 under a new base segment
    Then v1 is never edited in place and stays readable after v2 is published
    Then each consuming story pins the published version and a private variant fails its drift test

  Scenario: AC6 The fakes answer the document and the drift test runs on both sides (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the element fake, the rule fake and the drift test
    Then the element fake answers a complete element in ASSET_UNLOCK_DECISION with a pass, a complete element with a fail, an element whose inspection outcome is missing and an element with no decision yet
    Then the rule fake answers the two rows with their from-states, events and target states, and a case in a state no row expects
    Then the record fake answers an accepted record, a refusal with MSG-P7-009 and an unavailable writer with MSG-P7-003
    Then the drift test fails on any difference between the fake and sections 12 and 13 of the document, in this story and in RWB-S2-E3014-APP and RWB-S2-E3012-APP

  Scenario: AC7 A value no source fixes is published as the working read and the gap stays open (new, D-RCV-60)
    Given the value of the answer, the field list or the announcement that no source fixes
    When it is linted against sections 12 and 13 of the document
    Then the value is published as the working read of the assumption and the gap stays open
    Then the value carries the reference Not specified in the source documents (GAP-2677; ASM-4405)
    Then a value published as settled without that reference fails the lint

  Scenario: AC8 Every business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules table of section 8 of the document
    When it is traced against the criteria of section 7 and the test cases of section 16
    Then each of BR1 to BR11 names at least one criterion and one test case
    Then a rule with no criterion or no test fails the traceability check

  Scenario: AC9 The provided operation answers 401, 403 and 404 for the three failures and returns no element (new, D-RCV-60)
    Given the read of the treatment representation on GET /treatments/{treatmentId}
    When it is called without a valid credential, without the Treatment and offer R right, and for a treatmentId that does not exist
    Then the answers are 401, 403 and 404 in that order
    Then no element is returned on any of the three answers
```

These six criteria are new and test only the contract deliverable. **The four legacy acceptance criteria of RWB-E3-014 stay with RWB-S2-E3014-APP** and are not repeated here, and every identifier, state, event and condition is taken from Business Rules and Routing Logic v4 and TSD S2 T4, character for character. The field list, the required set and the value domain of `unlockDecision` are the working read of ASM-4405, ASM-4406, ASM-B2-S2-009-7, ASM-B2-S2-009-8 and ASM-B2-S2-009-9 (GAP-2677).

**Open decision DL10.** The open decision DL10 is carried with its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863, which the directive confirms; the decision itself stays open and is not closed by this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The element is `AssetUnlock` with six fields, three required once the step has run, and it is recorded on the `treatment` row of `rwb_treatment` | GAP-2677; ASM-4405; TSD S2 T3.1 |
| BR2 | The trigger is R-DIL-22: WITH_FIELD_INSPECTION, INSPECTION_COMPLETED, checklist, photographs and bills captured, target ASSET_UNLOCK_DECISION | R-DIL-22; TSD S2 T4 |
| BR3 | The answer is R-DIL-23: ASSET_UNLOCK_DECISION, AUTO_UNLOCK_PASSED, the unlock rule passes in about 95% of cases, target AWAITING_TRANSFER | R-DIL-23; TSD S2 T4 |
| BR4 | `unlockDecision` carries the event code the package returned and the contract holds no member list; the decision code D6.4, the rule ID and the package version are values in force | BR-S2-014; ASM-4406 |
| BR5 | No table is created for the inspection, the unlock or the release: the capture is rwb-document's, the answer and its instant are treatment columns, and the record is the library's | GAP-2677; ASM-4405; DP-03 |
| BR6 | The case status stays rwb-case's and no case status is an element; the step reports the target state and the parent moves it | DP-01; ASM-4401 |
| BR7 | The asset record and the asset list stay rwb-asset's and the ACE NPA-asset facts stay rwb-source-data's; `assetRef` is a reference and no asset field is copied | DP-01; DP-05; ASM-4402; ASM-4407 |
| BR8 | The element is part of the treatment representation on `GET /treatments/{treatmentId}` and declares no path of its own; the read right is Treatment and offer R under the scope rule | TSD S2 T-A.1 API-S2-002; TSD S2 T6.1; DP-13 |
| BR9 | The record is written with propagation `MANDATORY`, and a refused or unavailable record leaves the caller's transaction uncommitted | DP-03; RWB-PLT-E1027-CON; Principle 5 |
| BR10 | A published element is never edited in place: a compatible change keeps major version 1 and a breaking change raises major version 2 under a new base segment | Template and Rules §R7.2; §R5.4 class C |
| BR11 | The document declares no event for the unlock or the release, because no source names one; the service's one catalogue event, EV-10, is the offer release stories' | TSD S2 T5.3; GAP-2677; ASM-4407 |

**Coverage.** BR1 is covered by AC1 and TC-S2-E3014-CON-01; BR2 and BR3 by AC2 and TC-S2-E3014-CON-02; BR4 by AC2 and AC6 with TC-S2-E3014-CON-02 and TC-S2-E3014-CON-06; BR5 by AC1 and AC6 with TC-S2-E3014-CON-01 and TC-S2-E3014-CON-06; BR6, BR7, BR8 and BR11 by AC3 and TC-S2-E3014-CON-03; BR9 by AC4 and TC-S2-E3014-CON-04; BR10 by AC5 and TC-S2-E3014-CON-05.

**Where each rule lives in the target.** BR1 and BR4 are the element section and the value rule of `unlockDecision`. BR2 and BR3 are the rule section, copied from the routing workbook. BR5 is the boundary section and the drift test. BR6 and BR7 are the ownership statements of the boundary section, which is what keeps a case column and an asset column out of the element. BR8 is the access section and the reuse of the sibling resource. BR9 is the record section and the two library exceptions. BR10 is the versioning section. BR11 is the no-event statement, recorded once so that no consumer waits for an announcement that no source defines.

### 9. State transitions

No runtime state is this contract's: the case states below are rwb-case's, and the contract publishes them as the values the two rules report, character for character (ASM-4401).

| Object | State or value | Meaning in the contract |
|---|---|---|
| Case status (rwb-case's) | WITH_FIELD_INSPECTION | The from-state of R-DIL-22, the state the trigger is proved against |
| Case status (rwb-case's) | ASSET_UNLOCK_DECISION | The target state R-DIL-22 reports, and the from-state of R-DIL-23 |
| Case status (rwb-case's) | AWAITING_TRANSFER | The target state R-DIL-23 reports on a pass |
| Case status (rwb-case's) | AWAITING_APPROVER_SUMMARY | The target of R-DIL-24 on a fail; the sibling stage's path, named here only as the neighbour |
| `unlockDecision` | the event code the package returned | Empty until the rule has decided; the event code AUTO_UNLOCK_PASSED or AUTO_UNLOCK_FAILED once it has |
| `inspectionOutcome` | the capture fact | Empty before the capture; the checklist, photograph and bill facts after it |
| Contract | v1 | The published version every consuming story pins |
| Contract | v2 | Raised by a breaking change under a new base segment; v1 stays readable and is never edited |

The treatment row's own lifecycle, its `state` column and the screen states Draft, submitted, approved, booked and broken are RWB-S2-E3001-APP's and the sibling stories'; this contract fixes the six fields and none of the states of the row. A new event code is a value in force of the rule package and a data change, not a contract change, because `unlockDecision` is published as a width and not as a closed list.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the value rules and the fakes |
| The service owner of rwb-treatment | Approves a breaking change and freezes a version |
| RWB-S2-E3014-APP and the deed-in-lieu stage of RWB-S2-E3012-APP | Consume the element, pin the version and raise a change request rather than a private variant |
| The rwb-case owner (P3) | Confirms that the two from-states, the two events and the two target states are the case's and that no case status is an element |
| The rwb-decision owner (P7) | Confirms the decision code D6.4, the rule ID and the package version as the values the element and the record carry, and that no event is declared |
| The rwb-asset owner (S5) | Confirms that the asset record, the asset list and FEAT-AST-02 are its own, and that `assetRef` is the only asset value published |
| The rwb-source-data owner (P1) | Confirms the ACE NPA-asset read and the fact set that reaches the step on the case signal |
| The rwb-access owner (P4) | Confirms the capability area and right R the element is read under |
| The platform API owner | Owns the problem envelope, the style guide and the registry this document validates against |
| Sale officer, RW-RESTRUCT, RW-CASEOWN and the other roles of TSD S2 T6.1 | Read the element through the treatment read; they hold no authoring right here |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

The rwb-access authorise check that enforces the read of the element is Not specified in the source documents (DOR-RWB-S2-E3014-CON-6; DP-08), and the document declares no check of its own.

No personal name, no email address and no credential appears in the document, an example or a fake. Where an actor must be named, the example carries a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes field names, the required set, the two rules and the messages; no customer, account, asset or case value appears |
| Shapes published | `AssetUnlock` with the six fields of section 12.1, the problem envelope reused from the platform, and the four `treatment` columns the element is recorded on |
| Personal data | None. `assetRef` is a reference, `ruleVersion` is a version label and the capture is described by its kind, never by its content |
| Tables published | None. The consumer writes the element against `treatment` in `rwb_treatment`; `decision_record` is the library object of RWB-PLT-E1027-CON, applied in the same schema |
| Field identifiers | DF-ACE-208 to DF-ACE-219 for the NPA-asset reference the element names; DF-TRT-001, DF-TRT-002 and DF-TRT-004 for the treatment it is recorded on; the element's own identifiers are Not specified in the source documents (GAP-2677; ASM-4405) |
| Retention | The element is kept with the treatment row for the life of the case record; the retention period of the element is Not specified in the source documents (GAP-2677; ASM-4405) |
| Reference data | None read. The element reads no list and no parameter; the reference-data contract is DP-06 and DP-07, and this contract names no parameter |

**Business rule references.** Business data published: BR4. Shapes published: BR1. Personal data: BR7. Tables published: BR5. Field identifiers: BR1. Retention: BR1. Reference data: DP-06 and DP-07, read as none.

**Names outside the source models.** `treatment_unlock` is a refused name and not a dictionary object. `inspection_outcome`, `unlock_decision`, `unlock_decided_at` and `asset_ref` are columns of the treatment row with no field ID in LDM v9 or Data Classification v5; their field IDs are Not specified in the source documents (DOR-RWB-S2-E3014-CON-7). `decision_record` is the library object of RWB-PLT-E1027-CON, not an entity of LDM v9.

The document is the one place where a business value could leak, so it fixes that the event codes and the decision code are named as values in force and that the examples carry synthetic identifiers of the same kind as the legacy `SYN` values.

### 12. Contract

#### 12.1 REST operations provided

None of its own. The element is a component of the treatment representation that RWB-S2-E3001-CON publishes on `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (API-S2-002 of TSD S2 T-A.1), and this contract fixes the component, not the path (DP-13). The two screens reach it through the gateway-bff composite route (DP-19).

**Element: `AssetUnlock`**

| Field | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `inspectionOutcome` | jsonb | Yes, once captured | `treatment.inspection_outcome` (no field ID) | The capture fact of the case signal: the checklist, the photographs and the bills, by kind and count |
| `unlockDecision` | varchar(30) | Yes, once decided | `treatment.unlock_decision` (no field ID) | The event code the package returned; no member list is held here |
| `unlockDecidedAt` | timestamptz | Yes, once decided | `treatment.unlock_decided_at` (no field ID) | The business instant of the answer |
| `assetRef` | varchar(60) | No | `treatment.asset_ref` (no field ID) | The `asset_ref` of DF-ACE-208 to DF-ACE-219 the release names; no other asset field is copied |
| `ruleId` | string | No | The decision record | The rule that produced the answer; present when the package reports one |
| `ruleVersion` | string | No | The decision record | The version of the DEEDINLIEU package in force |

The element is recorded against the `treatment` row and against no other record; it has no collection and no free-text field. Its own BR Field IDs have no row in the Logical Data Model, so the field names and the columns are the working read of ASM-4405 (GAP-2677), and the names are the ones the sibling deed-in-lieu element set uses, so one treatment carries one shape of the unlock.

#### 12.2 REST operations consumed

None. A contract document calls no service. The case status, the inspection capture and the NPA-asset facts reach the consumer on the case signal the parent `CaseWorkflow` forwards (ASM-4401; ASM-4402), and the rule package reaches it on `rwb.decision.RulePackageInForce.v1` (ASM-4403). Each of them is a fact of the consuming story, and this contract adds no dependency of its own.

#### 12.3 Events published

None. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its one catalogue event, EV-10 `TreatmentApproved`, is the offer release's (TSD S2 T5.3). No source names an event for the unlock or the release of the asset for transfer, so the contract declares none and the release travels to rwb-asset as the case fact the parent carries (GAP-2677; ASM-4407). The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this contract (DP-03).

#### 12.4 Events consumed

None by this contract. The package event and the case signal are consumed by RWB-S2-E3014-APP and never by a document; the contract names neither as a subscription.

#### 12.5 Workflows and activities

None of its own: the contract defines no workflow, no activity and no task queue. What it fixes is the element the unlock step of `TreatmentWorkflow` writes and the value rule it applies, with the decision code and the record group the activity carries, so that both sides of the answer are written down in one place.

#### 12.6 Schedules

None. The contract declares no Schedule: the trigger is an event of the case signal, not a scan, and the legacy key owns no job in the context pack's ownership rows (context pack S2, Jobs row: None).

#### 12.7 Tables owned

None. The element is written by the consumer against `treatment` in `rwb_treatment`, a table of this service created on its own Flyway sequence, and `decision_record` is the platform library object of DP-03 applied in the same schema. The contract creates no table, declares no column of its own and adds no foreign key; `decision_log_entry` is P7's ledger in `rwb_decision` and is named only, never written or read here.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The `AssetUnlock` shape | A complete element in ASSET_UNLOCK_DECISION with a pass; a complete element with a fail; an element with no inspection outcome; an element with no decision yet |
| Rule fake | The two rows of R-DIL-22 and R-DIL-23 | The trigger and the answer with their from-states, events and target states; a case in a state no row expects; a version with no row at all |
| Value fixture | The values in force | The event codes INSPECTION_COMPLETED, AUTO_UNLOCK_PASSED and AUTO_UNLOCK_FAILED, the decision code D6.4 and the state names, of their owners |
| Decision-record fake | The record group of AC4 | An accepted record with the rule and package versions; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |
| Problem fakes | The error set of the read | One `application/problem+json` body per status, each with its `messageId` |
| Drift fixture | The contract test | One accepted and one refused body per section of the document, on the build of this story and of the two consuming stories |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming build rather than as a surprise in SIT. The element fake and the rule fake are what make Day 1 possible for RWB-S2-E3014-APP, RWB-S2-E3012-APP and RWB-ITG-W2.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the element rides the treatment read of a sibling contract | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches the read through gateway-bff (DP-19) |
| Kafka | 0 | 0 | The service topic is named and no event type is declared here; no unlock or release event exists in any source |
| Temporal | 0 | 0 | The contract declares no workflow and no activity; it fixes the element the unlock step writes |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element and record types in `th.co.scb.ace.workbench.recovery.treatment.api`, the value rules and the versioning rule in the contract document, and the fake set with the drift test as a test resource. The implementation that writes the element is RWB-S2-E3014-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2677; ASM-4405).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the writer behind the record group and declares no record element | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract or the service's own ACE views; `assetRef` is the only asset value and it names a fact, never a view | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the element rides the treatment read on that base | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the element is reached through it and the contract declares no route | referred to; the consuming story carries the dependency |

DP-13 is the base the element is served on, and DP-03 and DP-19 are named and not declared: the record is the library's and the route is the platform edge story's. DP-05 is the rule that keeps the ACE NPA-asset facts outside this service: the facts arrive on the case signal and `assetRef` is the only trace (ASM-4402). The embedded Drools runtime, the guard, the outbox and inbox library and the workflow kit are the service template's wave-0 capabilities, so nothing this contract refers to adds a build dependency of its own (ASM-4403).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AssetUnlockContract | Document | The element, the required set, the two value rules, the boundary, the record group and the versioning section (BR1 to BR11) |
| AssetUnlockSchema | Published schema | `AssetUnlock` with the six fields and their flags (BR1) |
| RuleSection | Document | The two routing rows, their from-states, events, conditions and target states (BR2, BR3) |
| RecordGroup | Document | Decision code D6.4, the rule ID, the package version and the two library exceptions (BR9) |
| Fake set and fixtures | Test asset | The element, rule, record and problem answers used by every consuming build (AC6) |
| DriftTest | Test asset | The comparison of a consuming build against sections 12 and 13 (AC6) |

**Database.** The contract creates no table. The consumer records the element on `treatment` in `rwb_treatment` with `inspection_outcome`, `unlock_decision`, `unlock_decided_at` and `asset_ref` on the service's own Flyway sequence, and `decision_record` is the library object applied in the same schema (DP-15; DP-03). `asset_ref` is a cross reference to the NPA asset by business key with no foreign key, and no other schema is named.

**Configuration and reference data.** The from-states, the event codes, the decision code D6.4, the state names and the 95% expectation are values in force of their owners and are read, never set here (BR4; ASM-4406). The capability area and right R are declared once and their role lists are rwb-access data (BR8). The problem envelope and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the element section with the six fields, the required set and the column mapping; validate it against the treatment representation (AC1).
2. Write the two value rules from the routing rows, with the value domain of `unlockDecision` and the version stamp (AC2).
3. Write the boundary and access section: no path, no case status, no asset element, no event, right R (AC3).
4. Write the record group with decision code D6.4 and the two exceptions (AC4).
5. Write the versioning and pinning section with one compatible and one breaking example (AC5).
6. Generate the fake set and the drift test, and wire the drift test into the build of RWB-S2-E3014-APP and of the deed-in-lieu stage of RWB-S2-E3012-APP (AC6).
7. Publish v1 and record the pinned version of this contract and of each consuming story (AC5).

**Feature flag.** `rwb.treatment.asset-unlock-contract`.

**Done when.** The element validates, the two value rules match the routing workbook character for character, the boundary test keeps every case status, asset field and event out of the document, the fakes answer the pass, the fail, the missing capture and the two record exceptions, the drift test is green on the build of this story and of the two consuming stories, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not hold right R of the treatment read on which the element is served | You cannot {action} here. Your role does not include it. | 403 of the sibling read, problem body with `messageId` MSG-P4-002 |
| MSG-P4-003 | The case or the treatment is outside the caller's scope, or does not exist | This case is not in your scope. | 404 of the sibling read, problem body with `messageId` MSG-P4-003 |
| MSG-P7-003 | The decision record cannot be written and the answer is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record failure; nothing is committed |
| MSG-P7-009 | The record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. | The record refusal, with the field name |
| MSG-GEN-001 | A required element of the capture is missing | Enter {field}. | The capture guard; no rule fires |
| MSG-GEN-006 | The service is unavailable | {system} is not available. Try again in a few minutes. | 503 of the sibling read |

The texts are the legacy and platform texts carried unchanged, and this contract adds no message identifier of its own: it publishes the status and the `messageId` slot of each, and the problem envelope is the platform's. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: it publishes an element. SCR-16 Deed in lieu (Checks; appraisal; approved; transferred; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8731)) shows the inspection outcome, the unlock answer and the asset reference; SCR-14 Treatment record (Draft; submitted; approved; booked; broken; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8730)) shows the treatment the answer was recorded on. Both are reached through the gateway-bff composite route, which calls this service's treatment read and the case read in one hop each (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this contract fixes only the elements the read returns.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3014-CON-01 | AC1 | Contract | The element validated against the treatment representation and the TSD: the six fields, the required set, the four column mappings, and a refused `treatment_unlock` table and a missing required field |
| TC-S2-E3014-CON-02 | AC2 | Contract | The two routing rows linted: the from-states, the events, the conditions, the target states, the value domain of `unlockDecision` and the decision code D6.4; a row with another from-state refused |
| TC-S2-E3014-CON-03 | AC3 | Contract | The boundary and access lint: no path of its own, right R declared, and a refused case status element, asset element and unlock event |
| TC-S2-E3014-CON-04 | AC4 | Component | A pass, a fail and a failed write through the record fake: `MANDATORY`, MSG-P7-009 with the field, MSG-P7-003 and no commit |
| TC-S2-E3014-CON-05 | AC5 | Component | A compatible change and a breaking change against the registry fake; the pinned version recorded for the two consuming stories |
| TC-S2-E3014-CON-06 | AC6 | Component | The element and rule fakes against the document, and the drift test on the build of RWB-S2-E3014-APP and of the deed-in-lieu stage of RWB-S2-E3012-APP |
| TC-S2-E3014-CON-07 | AC7 | Contract | The field list and the value domain checked against sections 12 and 13, and a value published as settled without its gap reference refused |
| TC-S2-E3014-CON-08 | AC8 | Contract | The section 8 rule table traced to the criteria and the test cases; a rule with no criterion or no test refused |
| TC-S2-E3014-CON-09 | AC9 | Component | The read on GET /treatments/{treatmentId} without a credential, without the right and for an unknown treatmentId: 401, 403 and 404, with no element returned |

The legacy test set TC-E3-014-01 to TC-E3-014-06 is carried by RWB-S2-E3014-APP and by the wave 2 integration harness, and these six are the contract's own tests; no legacy id is renumbered here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the event codes, the decision code, the state names and the 95% expectation are values in force, named and never fixed as constants or as a list this document holds (BR4).
- No personal data in a schema, an example, a fake or a log: `assetRef` is a reference, the capture is described by kind and count, and the personal-data scan fails the build otherwise.
- No table for the inspection, the unlock or the release: the element lives on `treatment`, the capture is rwb-document's and the record is the library's (BR5).
- No cross-schema reference and no foreign key across services: `asset_ref` is a business-key cross reference and the boundary test fails the build otherwise.
- No case status, no case table and no case column in the element (BR6; DP-01).
- No asset field beyond `assetRef`, and no ACE view: the facts are rwb-source-data's and arrive on the case signal (BR7; DP-05).
- No path of its own and no new right: the element rides the sibling read and declares right R (BR8).
- No record element: the record is the library's, its propagation is `MANDATORY`, and a failed write leaves nothing changed (BR9).
- No event for the unlock or the release: no source names one, and none is invented (BR11).
- A published version is never edited in place: a breaking change raises major version 2 under a new base segment with a migration note (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-007 | An asset accepted under a deed in lieu is unlocked as a non performing asset by rule, with exceptions summarized for the approver | Business Requirements Program, section 5.9 | FEAT-TRT-14 | 07 Route, settle and claim | R-DIL-22; R-DIL-23 | TC-S2-E3014-CON-01 to TC-S2-E3014-CON-06 |
| Legacy test set RWB-E3-014 | TC-E3-014-01, TC-E3-014-02, TC-E3-014-03, TC-E3-014-04, TC-E3-014-05, TC-E3-014-06 | Business Requirements Program, section 5.9 | FEAT-TRT-14 | 07 Route, settle and claim | R-DIL-22; R-DIL-23 | Executed by RWB-S2-E3014-APP and the wave 2 harness; not owned here |

REQ-S2-007 is the requirement the sibling deed-in-lieu story traces for the same two rules; FEAT-TRT-14 is the feature of this contract (FSD S2 A2.14), and TSD S2 T8 maps its ten requirement IDs to FEAT-TRT-01 generically, so the trace runs on the feature code until the C1 PRD allocates the requirement of the unlock (GAP-2677; ASM-4408).

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3014-APP | App development | H consumer: implements the unlock step, the four columns and the record against this element and its fakes |
| RWB-S2-E3012-APP | App development | Consumer: the deed-in-lieu stage that calls the step and owns the transfer and the approver path; builds against the same element with no build dependency on this story |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment resource whose read serves the element, its right R and its error set |
| RWB-S2-E3012-CON | Contract | Sibling: the rest of the deed-in-lieu element set; the four unlock names are shared so one treatment carries one shape |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library behind the record group; this contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route the two screens use |
| RWB-P3-E2004-CON, P3 rwb-case | Contract, App development | Referred to: the case status, the case signal and the two from-states this element never carries |
| P7 rwb-decision | App development | Referred to: the DEEDINLIEU package, its rows and its version |
| P1 rwb-source-data | App development | Referred to: the ACE NPA-asset read behind `assetRef` |
| S5 rwb-asset, FEAT-AST-02 | App development | Referred to: the asset record and the asset list the release leads to |
| RWB-ITG-W2 | Integration | The end-to-end proof of the unlock against the live owners, held by the wave 2 harness |

### 19. Out of scope

- The implementation behind the element — the unlock step, the activity, the repository, the four columns and the tests: RWB-S2-E3014-APP.
- The treatment resource and its two operations, its error set and its fakes: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The rest of the deed-in-lieu element set, the event reference of the offer release and the transfer facts: RWB-S2-E3012-CON and RWB-S2-E3012-APP.
- The offer operation, the draft-terms change and the submit-for-approval operation: RWB-S2-E3002-CON and RWB-S2-E3003-CON.
- The failed unlock and its approver path, R-DIL-24 to R-DIL-26, with the three-working-day clock and the agent summary: the sibling stage and rwb-decision's `ApprovalWorkflow`.
- The case status, the case signal and the case table: rwb-case (P3); the case status is named in section 9 and is never an element.
- The DEEDINLIEU package, its rows, its version and the central ledger: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The ACE NPA-asset read and its grant: rwb-source-data (P1) and ACE; the element names `assetRef` and no other field.
- The asset record, the asset list and FEAT-AST-02: rwb-asset (S5) and rwb-integration (P2).
- The roles, the rights and the scope data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-14 and SCR-16: the platform edge story and the screen owners (DP-19).
- An event for the unlock or the release, and any table for the inspection, the unlock or the release (GAP-2677; ASM-4407).
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof of the element against the live owners: the wave 2 integration harness.
