# RWB-S2-E3013-CON Check encumbrance and eligibility before negotiation - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-013 for rwb-treatment. The legacy acceptance criteria stay with the application slice; every criterion here is new (D-RCV-60) and tests only the contract deliverable. The contract publishes the readiness surface of the service on base `/api/recovery/treatment/v1` (DP-13): the `readiness` section of the treatment answer as a compatible addition at major version 1, the title-set task request the stage reports to the parent, the read-only contract of the three ACE views it depends on (DP-05), the error set and the fakes, with the section and the request declared as the working read because no source gives them a shape (GAP-2675; ASM-4396). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3013-CON |
| Work type | CON (Contract) |
| Size | Not specified in the source documents (DOR-RWB-S2-E3013-CON-16) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner for rwb-treatment**, I want **the published contract of the encumbrance and eligibility check — the `readiness` section of the treatment answer with the encumbrance, registration and title-set facts and the rule version that decided them, the title-set task request the stage reports to the parent, the read-only column contract of the three ACE views the facts come from, the error set, the compatibility rule and the fakes — instead of the monolith's one `recovery` schema and one in-process check**, so that **the application slice, the gateway route, rwb-case's parent workflow and the wave 2 harness all build against one frozen readiness surface from Day 1, and no consumer invents a column or a task that the source never gave**.

This story owns:

- the `readiness` section of the treatment answer: its name, its properties, which of them are stored and which are computed per request, and the statement that it is an optional addition to the treatment resource of RWB-S2-E3001-CON;
- the read operation entry the section is served through, on base `/api/recovery/treatment/v1`, with the access right, the error set and the note that it declares no write operation (DP-13);
- the `TitleSetTaskRequest` element the stage outcome carries, with the rule ID, the package version, the clock and the references, and the statement that the task itself is rwb-case's;
- the read-only column contract of `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_npa_asset`, with the statement that the encumbrance and title statuses are columns of that read and are never derived in code (DP-05);
- the compatibility rule, the pinning rule and the drift test, and the fake set every consumer uses.

It does not own: the behaviour behind the section, which is RWB-S2-E3013-APP; the treatment resource, its create, its read and its element, which are RWB-S2-E3001-CON; the settlement and deed-in-lieu offer surfaces, which are RWB-S2-E3002-CON and RWB-S2-E3012-CON; the case status, the task and the timers, which are rwb-case's; the decision-record library, which is RWB-PLT-E1027-CON; the gateway-bff composite route, which is RWB-PLT-N001-CON; and the ACE views themselves, their grant and their ingestion, which are P1's and the ACE DB stories'.

### 2. Business rationale

Legacy RWB-E3-013 had no contract to publish: the encumbrance and title facts were columns read in the same process, the task was a row in a table of the same schema, and the decision log was a row beside them. The microservice split removes that option. The facts now come from ACE views read by rwb-treatment, the status they lead to is moved by rwb-case, the answer is served by the gateway route, and the harness proves the path across services, so four consumers need the same answer to the same questions before any of them writes code.

**The division of the legacy key is fixed.** The legacy acceptance criteria **AC1 to AC4 stay with RWB-S2-E3013-APP**; every criterion in section 7 is new and tests only the contract deliverable in this title. The treatment resource and its read are RWB-S2-E3001-CON's, the offer surfaces are the siblings' of the same legacy key group, and nothing of either is restated here.

The contract has to exist first for three reasons. The **result has no field anywhere**: TSD S2 T3.1 gives `treatment` DF-TRT-001 to DF-TRT-033 and none of them is an encumbrance, a registration or a title-set status, the functional specification's A2.13 has no field catalog at all, and the legacy data table names the fields of the three views only as ranges, so without a published section one consumer reads a status from a table that will never hold it and another computes it from `lien_rank` in code (GAP-2675; ASM-4395, ASM-4396). The **task is not the service's**: R-SET-22 says "raise a task" and the connection matrix of Architecture v5 slide 13 gives rwb-treatment no call to rwb-case, so the request has to be published as an element the parent turns into a task, not as a write of this service (ASM-4394). And the **ACE read is a dependency with no publication**: DP-05 allows either the service's own views or the contract read of rwb-source-data, and the choice belongs in one document, not in four consumers' heads (ASM-4395).

The contract also fixes what it does not do: it declares no business table, adds no column, publishes no event of its own, declares no workflow and no Schedule, and publishes no write operation, because the officer takes no action in this step.

The fake is the Day-1 unblocker: the application slice, the gateway route, the parent workflow's title-set path and the harness can build the clear, blocked, resumed and missing-title answers before the live views, the live case workflow and the live rule packages exist (Template and Rules §R5.4 class C).

### 3. Preconditions

- The service identity is fixed by Template and Rules §R4 and the context pack: schema `rwb_treatment`, base `/api/recovery/treatment/v1`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13).
- The readiness section has no source shape: TSD S2 T3.1 carries no readiness field, FSD S2 A2.13 has no field catalog, and the legacy story names the view fields only as ranges DF-ACE-091 to DF-ACE-098, DF-ACE-196 to DF-ACE-207 and DF-ACE-208 to DF-ACE-219, so the section and its properties are the working read of ASM-4396 (GAP-2675).
- The encumbrance condition of R-DIL-02 and R-DIL-04 is `encumbrance_status`, and no named view field carries it; the contract therefore states that it is a column of the ACE read and not a derived value, and the column name is the working read of ASM-4395 (GAP-2675).
- The read of the three views is fixed as DP-05's own-view form, which adds no dependency; the alternative, the contract read of rwb-source-data, would be a C dependency and is named as the fallback in section 19 (ASM-4395).
- The target state of the task is fixed: the stage reports an outcome, the parent `CaseWorkflow` raises the task on the 5 working-day clock of R-SET-22 and moves the case status, so the contract publishes a request element and no task write (ASM-4394).
- The capability area "Treatment and offer" and right R are the access declaration of TSD S2 T6.1 and the legacy permission table; the check is the guard library's and the contract declares the right only (ASM-4398).
- RWB-S2-E3001-CON is named and not restated: the readiness section is declared as an optional addition to the treatment element of that contract, at the same major version, so its consumers see a compatible change.
- RWB-PLT-E1027-CON and RWB-PLT-N001-CON are published, so the contract can name the record write and the composite route without redeclaring either (DP-03; DP-19).
- The validation messages keep their legacy identifiers and texts, and no published catalogue defines their entry format, so the entry format is the working read.
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), sits in contract group `CG-W2`, and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the `readiness` section: its name, its properties, the stored and the computed ones, and its place in the treatment answer of RWB-S2-E3001-CON.
2. The author records the one read operation entry the section is served through, its access right, its errors and the statement that no write operation is published.
3. The author fixes the `TitleSetTaskRequest` element the stage outcome carries: the rule ID and package version, the case and treatment references, the clock and the reason code.
4. The author fixes the read-only column contract of the three views: the field identifiers, the column names the source gives and the two statuses it does not.
5. The author fixes the error set: the status codes, the message identifiers and the texts, and the note that no idempotency key applies because nothing is written.
6. The author writes the compatibility rule — an optional section may be added at the same major version and a breaking change raises major version 2 — and the pinning rule for the consumers.
7. The author writes the negative rules: no table, no column for a status, no derivation of a status in code, no case write, no task write and no ACE write.
8. The lint and schema steps run: the operation entry compared against TSD S2 T-A.1, the section and the request validated against the OpenAPI document, the examples scanned for personal data, and the error table checked against the message identifiers.
9. The fake set is generated from the document: the clear, blocked, resumed, missing-title and no-collateral answers, the refusal answer and the failed record answer.
10. The contract test runs the fakes against the document on every change and fails the build on any drift; the document and the fakes are published at v1 and the consumers pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The section is published as required, or without a version tag on the treatment answer | The schema validation fails the build; the section is optional on the answer of RWB-S2-E3001-CON | None | AC1 |
| X2 | A status is published as a column of `rwb_treatment`, or the document says a status is derived from `lien_rank` | The schema and lint steps fail the build; the statuses stay properties of the read | None | AC1, AC5 |
| X3 | The task is published as a write of this service, or the request carries no clock and no rule version | The lint fails the build; the request is an element of the stage outcome and its consumer is rwb-case | None | AC2 |
| X4 | An error answer is published without a message identifier, or with a code the legacy story does not carry | The error-table check fails the build; every code is mapped to its identifier and its text | None | AC3 |
| X5 | A breaking change is made to a path, a property or the answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC4 |
| X6 | A consumer ships without the drift test, or its code drifts from the published schemas | The registry refuses the change and the drift test fails that consumer's build | None | AC5 |
| X7 | A value a consumer needs is named by no source — the section name, a property name, the encumbrance column or the task reason code | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2675; ASM-4396) | AC7 |

X1 and X5 are contract-governance paths, X2, X3 and X4 are the paths an invented column, task or error adds, X6 is the drift rule of class C, and X7 is the reason the section and the request are published as a working read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing but the two named contracts, reads no business data and starts on Day 1 |
| Negotiable | The property names, the example values and the fixture set are open until v1 is frozen; the one operation entry, the request element, the error set and the compatibility rule are fixed |
| Valuable | Unblocks the application slice, the gateway route, the parent workflow's title-set path and the wave 2 harness on Day 1 and keeps the statuses out of the schema |
| Estimable | One section, one request element, one operation entry, four errors, two rules and six fakes |
| Small | One sprint for the document, the schemas, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: encumbrance and eligibility readiness contract

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the service base is /api/recovery/treatment/v1, the schema rwb_treatment and the topic rwb.treatment.events.v1
    Given the contract declares the readiness section, the title-set task request and the view column contract only

  Scenario: AC1 The readiness section is fixed as an optional addition to the treatment answer (new, D-RCV-60)
    Given the answer schema of the treatment read of RWB-S2-E3001-CON
    When the extended schema is validated
    Then the answer carries an optional readiness section with checkType, encumbranceStatus, registrationStatus, titleSetStatus, checkedAt, ruleId, ruleVersion, holdUntil, collateralNo and assetKey
    Then the document states that encumbranceStatus, registrationStatus and titleSetStatus are values of the ACE read and are never derived in code from lien_rank or register_date
    Then the document states that the section is an additive, backward-compatible change at major version 1 and that RWB-S2-E3001-CON owns the operation entry
    Then the document declares no table and no column for a status, a hold date or a check time
    Then an example carries a status, a rule version and a date and no national identifier, account number or name
    Then the decision code is the ruleId and ruleVersion that the evaluated package returned
    Then the statuses, the hold limit and the clocks are values in force and the only values in the document are examples

  Scenario: AC2 The title-set task request is an element of the stage outcome, not a write of this service (new, D-RCV-60)
    Given the stage-outcome schema and the lint rule of the document
    When the request element is validated
    Then TitleSetTaskRequest carries the case and treatment references, the ruleId R-SET-22, the ruleVersion, the clock of 5 working days as a value in force and the reason code
    Then the document states that rwb-case raises the task and the service reports the request, so no task row, no timer row and no case row is declared here
    Then the lint fails the build if the document declares a task write, a timer write or a case status write
    Then the request carries no personal data and names the subject by reference only
    Then the case states are moved by rwb-case and not by this service

  Scenario: AC3 The read surface, its access right and its error set are fixed (new, D-RCV-60)
    Given the operation section of the document
    When it is validated against TSD S2 T-A.1 API-S2-002 and the legacy permission table
    Then exactly one operation entry is published, the read of the treatment answer at GET /treatments/{treatmentId}, under capability area Treatment and offer with right R
    Then no write operation is published, because the check is started by rule R-DIL-01 on the case signal and the officer takes no action in it
    Then the entry declares 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, and declares no idempotency key because no state changes
    Then the document maps MSG-GEN-001, MSG-P7-003 and MSG-P7-009 to the answers that carry them and adds no message identifier
    Then an error answer carries the message identifier, the merge fields and the trace identifier only

  Scenario: AC4 Versioning separates a compatible addition from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to the published surface
    Then adding an optional property or an optional section keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a breaking change to the operation entry, a required property, an error code or the answer raises major version 2 and v1 is never edited in place
    Then each consumer pins a published version and raises a change request rather than a private variant

  Scenario: AC5 The view column contract is read only, and no status is derived or stored (new, D-RCV-60)
    Given the data section of the document and the lint rule of the document
    When the view contract is validated
    Then the document lists v_ace_collateral with DF-ACE-091 to DF-ACE-098, v_ace_collateral_detail with DF-ACE-196 to DF-ACE-207 and v_ace_npa_asset with DF-ACE-208 to DF-ACE-219, each marked read only
    Then the document states that the check holds SELECT on the three views and writes no ACE object
    Then the document states that the encumbrance and title-set statuses are columns of that read whose names no source fixes, so the names are the working read
    Then the lint fails the build if the document declares a write, a table copy or a derivation of a status in code
    Then no property of the section carries a personal field

  Scenario: AC6 The fake answers the document and every consumer runs the drift test (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the readiness fake, the task-request fake, the error fake, the treatment resource fake and the composite route fake
    Then the readiness fake answers a clear mortgage, an unresolved mortgage with a hold date, an HP asset clear in SCIS, a collateral-release case with title documents missing and a case with no collateral row
    Then the error fake answers 403, 404 and 503 with their message identifiers and no personal data
    Then the drift test fails the build of any consumer whose request, answer or error does not match section 12

  Scenario: AC7 A value no source names is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value a consumer needs is named by no source
    When the contract is validated
    Then the value is published as the working read of its assumption with the message Not specified in the source documents (GAP-2675; ASM-4396)
    Then the gap GAP-2675 stays open until a source names the value

  Scenario: AC8 Each business rule BR1 to BR8 has a covering criterion or test (new, D-RCV-60)
    Given the business rules table of section 8 of the document
    When the rule coverage line and the test table are read
    Then each rule BR1 to BR8 maps to one criterion AC1 to AC7 or one test in section 16
    Then a rule that is an architecture constraint is covered by a guardrail or boundary test
    Then a rule with no covering criterion or test fails the review of the document

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given the TSD S2 v2 transition table for R-SET-22 and R-DIL-01
    When a status change that the table does not allow is proposed in the contract
    Then the lint refuses the change
    Then the document declares no write of an encumbrance, registration or title-set status
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here, because **AC1 to AC4 of RWB-E3-013 are owned by RWB-S2-E3013-APP**, and every identifier, rule, message and field range is taken from the legacy story, the TSD appendix or the rule set character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The readiness answer is one optional section of the treatment answer of RWB-S2-E3001-CON, at the same major version, and no consumer carries a private copy of it | GAP-2675; ASM-4396 |
| BR2 | The encumbrance, registration and title-set statuses are values of the ACE read and are never derived in code and never stored in this schema | R-DIL-02, R-DIL-04, R-SET-22; DP-05; ASM-4395 |
| BR3 | The title-set task is rwb-case's: the stage reports a request with the rule, the version and the clock, and no task, timer or case write is declared | R-SET-22; ASM-4394 |
| BR4 | One read operation is published under right R with its error set, and no write operation, because the check is started by rule and ends in a report | R-DIL-01; TSD S2 T-A.1 API-S2-002 |
| BR5 | The three views are read with SELECT only under DP-05; no ACE object is written and no view is copied into `rwb_treatment` | DP-05; DP-01 |
| BR6 | The contract declares the access right only; the check is the guard library's on capability area "Treatment and offer" | TSD S2 T6.1; ASM-4398 |
| BR7 | A published version is never edited: a compatible addition stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |
| BR8 | No value a business person may change is enumerated in the contract: the statuses, the hold limit and the clocks are values in force, and the only values in the document are examples | BR-S2-013 |

**Where each rule lives in the target.** BR1 is the section table and the note on the operation entry. BR2 is the stored-versus-read column of every property and the lint rule of X2, and it is the reason the section exists at all rather than a set of columns. BR3 is the request table and the lint rule of X3. BR4 and BR6 are the operation table with its access column and the error table. BR5 is the view contract and the lint rule of AC5. BR7 is the compatibility section and the pinning rule. BR8 keeps every status an example and never an enumeration.

Rule coverage: BR1 and BR8 are covered by AC1; BR2 by AC1 and AC5; BR3 by AC2; BR4 and BR6 by AC3; BR5 by AC5; BR7 by AC4. The check is started by rule R-DIL-01 on the case signal and has no schedule and no batch trigger. Boundary (GAP-0736): this service owns the encumbrance and title check and its answer; rwb-case owns the case state, the title-set task and the decision record; the task timer value is Not specified in the source documents (GAP-0736) until a parameter is named.

Open decision DL10 stays open with assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863; the decision is not closed here.

### 9. State transitions

None at run time: a document and a schema have no state. Two vocabularies are fixed here, and the runtime transitions behind them are specified by RWB-S2-E3013-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Readiness answer | Clear | The encumbrance or registration status of the read is clear and the title set is present |
| Readiness answer | Blocked | The status is unresolved and the answer carries a hold date |
| Readiness answer | Title set missing | The title documents are absent and the answer carries the task request |
| Readiness answer | Undetermined | No collateral row is found for the case; the answer carries the unmatched outcome |
| Task request | Reported | The stage outcome carries the request; rwb-case raises the task |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited in place |

The case states ROUTE_APPROVED_DIL, EARLY_READINESS_CHECK, ENCUMBRANCE_BLOCKED, VALUATION_ORDERED and COLLATERAL_RELEASE_REQUESTED are rwb-case's and are named in the request only as the reason they lead to.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the section and request schemas, the error table and the fakes |
| The service team of rwb-treatment | Consumes the contract, pins the version and raises a change request rather than a private variant |
| The rwb-treatment tech lead | Confirms that the one operation entry and the request element are the ones the application slice fills |
| The rwb-case owner (P3) | Confirms that the task is raised by the parent workflow on the request and that no case write is declared |
| The P1 rwb-source-data owner | Confirms the read-only view contract and the fallback to its own contract read |
| The platform edge owner | Confirms the composite route the two screens use, which this contract names and does not declare |
| The wave 2 integration harness owner | Confirms the fake set is enough to prove the cross-service path |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

The one operation is guarded by the rwb-access authorise check under DP-08 on capability area Treatment and offer with right R; this contract declares the right and does not implement the check.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes one operation entry, two schemas, codes, message identifiers and three examples; no customer, account or case value appears |
| Stored fields referenced | DF-TRT-003 `decision_log_id`, DF-TRT-013 `outcome` and DF-TRT-014 `outcome_at` of `treatment`, referenced through the section and declared by RWB-S2-E3001-CON, not redefined here |
| Read fields referenced | DF-ACE-091 to DF-ACE-098 of `v_ace_collateral`, DF-ACE-196 to DF-ACE-207 of `v_ace_collateral_detail` and DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset`, each read only |
| Personal data | None. The examples carry a status, a rule version, a date and a business key, and the actor and trace references are identifiers, never names |
| Tables published | None. The contract declares no table and no column; `treatment` is the application slice's and `decision_record` is the library's (DP-01; DP-03) |
| Reference data | Parameters read: Not specified in the source documents (DOR-RWB-S2-E3013-CON-20). The reference-data contract is DP-06 and DP-07; the statuses, the hold limit and the clocks are values in force read under it |
| Field identifiers | The stored fields and the view fields carry the identifiers above; the section's own properties carry none, because no source gives them one (GAP-2675; ASM-4396). Rows of this table carry no BR Field ID, and the value is Not specified in the source documents (DOR-RWB-S2-E3013-CON-7). Test data comes from the fake set, not from the ACE views |

The one place where the contract could leak a value is the status: the document therefore fixes that `encumbranceStatus`, `registrationStatus` and `titleSetStatus` are values of the read, that they are never an enumeration of this contract and never a default, and that no example value is presented as the value of the rule set in force.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). The contract declares the readiness section and names the one operation it is served through; the operation entry belongs to RWB-S2-E3001-CON and this contract adds an optional section to its answer at major version 1.

| Method | Path | Answer | Access | Idempotency |
|---|---|---|---|---|
| GET | `/treatments/{treatmentId}` | The treatment element of RWB-S2-E3001-CON with the optional `readiness` section: `checkType`, `encumbranceStatus`, `registrationStatus`, `titleSetStatus`, `checkedAt`, `ruleId`, `ruleVersion`, `holdUntil`, `collateralNo` and `assetKey` | Treatment and offer, right R | Not applicable; the read changes no state |

No write operation is published. R-DIL-01 starts the check on the case signal, the check reports its outcome to the parent `CaseWorkflow`, and the officer takes no action in this step, so there is nothing to post or patch; the legacy endpoint table of RWB-E3-013 names the treatment read only, which is consistent with this surface (GAP-2675; ASM-4394, ASM-4396). The errors are 401, 403 with MSG-P4-002, 404 and 503. The reasons the section has no source shape, and whether the bank ever intended a separate readiness operation, are Not specified in the source documents (GAP-2675; ASM-4396).

#### 12.2 REST operations consumed

None. The contract declares the surface and calls no service: the route, the product group and the collateral keys arrive on the signal the parent forwards, the statuses are read from the three views, and the decision record is an in-process call of RWB-PLT-E1027-CON (DP-03; DP-05; ASM-4394). This is why the Work Package records no C dependency for the pair.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its events `TreatmentApproved` and `TreatmentClosed` belong to other stories. This contract publishes no event schema and declares no outbox row.

#### 12.4 Events consumed

None. The contract declares no subscription; the two events the application slice consumes — `rwb.decision.RulePackageInForce.v1` (EV-30) and `rwb.deviation.DeviationRaised.v1` (EV-06) — belong to P7 and S8 and are named in section 19, and the case status is a workflow signal and not an event of this contract (ASM-4394).

#### 12.5 Workflows and activities

None. The contract declares no workflow and no activity. It states only that the section is filled inside an activity on the owner's own task queue and that the decision record is called from that activity, so a replay reuses the recorded decision; the workflow itself is RWB-S2-E3013-APP's readiness branch of `TreatmentWorkflow` on `rwb-treatment` (DP-12).

#### 12.6 Schedules

None. The contract declares no Temporal Schedule and no legacy Quartz job. The 2 working-day lead clock, the 10 working-day hold and the 5 working-day title-set clock are durable timers inside the workflow and values in force in the rule set, not part of the published surface.

#### 12.7 Tables owned

None. The contract declares no table, no column and no key, and the negative rule is the deliverable: no encumbrance, registration, title-set or hold column exists in `rwb_treatment`, because no source gives one and a column would freeze a status that the rule set owns (GAP-2675; ASM-4396; DP-01). `treatment` is RWB-S2-E3001-APP's business table, `decision_record` is the library object of RWB-PLT-E1027-CON, `decision_log_entry` is P7's ledger, and the case, the task and the timer are rwb-case's; all are named here only.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Readiness fake | The `readiness` section on `GET /treatments/{treatmentId}` | A clear mortgage, an unresolved mortgage with a hold date, an HP asset clear in SCIS, a collateral-release case with title documents missing and a case with no collateral row |
| Task-request fake | The stage outcome element | A `TitleSetTaskRequest` with rule R-SET-22, its version, the 5 working-day clock and the reason code; a request with no clock refused as invalid |
| Error fake | The error table | 403 with MSG-P4-002, 404 and 503, each with its identifier, its merge fields and a trace identifier |
| Treatment resource fake | The answer the section extends | The treatment element of RWB-S2-E3001-CON, referenced and not restated |
| Composite route fake | The gateway-bff composite route of RWB-PLT-N001-CON | One hop for SCR-16, joining the treatment read with its readiness section; a refused route for a role without right R |
| Decision-record fake | The library write the application slice makes | An accepted record with an entry reference; a refusal with MSG-P7-009 and the field; a failed write with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consumer rather than as a surprise at run time. The treatment resource fake and the decision-record fake are the published contracts of their stories and are referenced here, not redeclared.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation entry, extended | 0 | OpenAPI 3.1 fragment; one hop to the service, 2 s timeout |
| Kafka | 0 event schemas | 0 | The service topic is named; this contract declares no event |
| SQL view | 3 read-only views referenced | 3 | SELECT only under DP-05; no write to any ACE object |
| Temporal | 0 | 0 | The contract states the section is filled in an activity and declares no workflow |
| File, Nexus | 0 | 0 | No file and no Nexus operation crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the OpenAPI fragment and the two element schemas in `th.co.scb.ace.workbench.recovery.treatment.api`, the error table and the compatibility note in the contract document, and the fake set as a test asset. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2675; ASM-4396).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 enters the contract as one statement — the section is written with a record in the caller's transaction — and the H dependency sits on the application slice, which calls the library. DP-05 is the read-only column contract of the three views and the reason the statuses are published as read values. DP-13 is the base of the operation entry and the reason the legacy base appears nowhere in the document. DP-19 is the route the two screens use, named here so that the composite route fake has an owner.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentReadOpenApi` | OpenAPI 3.1 fragment | The one operation entry, its parameter, its errors, its access declaration and the note that it extends RWB-S2-E3001-CON |
| `ReadinessSectionSchema` | Answer schema | The ten properties of the section and the stored, read and computed note on each |
| `TitleSetTaskRequestSchema` | Stage-outcome schema | The request the parent turns into a task, with the rule, the version, the clock and the reason code |
| `AceViewContract` | Document table | The three views, their field identifiers, their read-only mark and the two statuses whose column names no source fixes |
| `ErrorCatalogue` | Document table | The status codes, the message identifiers, the legacy texts and the merge fields |
| `CompatibilityNote` | Document section | The additive-versus-breaking rule, the pinning rule and the negative rules |
| `ReadinessFakeSet` | Test asset | The six fakes of section 12.8 and the drift test every consumer runs |

**Database.** None. The contract creates no table, adds no column and declares no key; the negative rules of section 12.7 and of AC5 are the deliverable, and a review that finds an encumbrance, registration, title-set or hold column in `rwb_treatment` fails this story.

**Configuration and reference data.** The contract fixes no business value. The statuses, the hold limit and the three clocks are values in force in the rule set; the only values in the document are the example values, and they are marked as examples. Capability area "Treatment and offer" and right R are read from rwb-access through the guard library, which the application slice calls (ASM-4398). The grant on the three views is a DB story's (DP-05; ASM-4395).

**Build steps**

1. Write the one operation entry, its access right and its errors, and lint that no write operation and no second form appear (AC3).
2. Write the `readiness` section, its ten properties and the stored, read and computed note on each (AC1).
3. Write `TitleSetTaskRequest` and the lint that refuses a task, timer or case write (AC2).
4. Write the `AceViewContract` table with the three field ranges and the two statuses, and the lint that refuses a derivation in code (AC5).
5. Write the error table with the four identifiers and their legacy texts, and validate one answer per code (AC3).
6. Write the compatibility note, the pinning rule and the negative rules (AC4).
7. Generate the six fakes and the drift test; wire the drift test into the build of RWB-S2-E3013-APP, the gateway route, the parent workflow's title-set path and the wave 2 harness (AC6).
8. Publish v1 and record the pinned version of each consumer.

**Feature flag.** `rwb.treatment.readiness-contract`.

**Done when.** The document and the two schemas validate, the operation lint passes with one read entry and no write, the error table matches the four legacy identifiers and texts, the six fakes answer every example including the blocked answer and the missing title set, the drift test is green on the build of this story and on the build of the application slice, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, or no collateral row is found for the case | Enter {field}. | 422 on the request, or the unmatched outcome of the answer; the field name is carried |
| MSG-P4-002 | The role does not hold right R | You cannot {action} here. Your role does not include it. | 403, from the guard library |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, from RWB-PLT-E1027-CON |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. | 422, from RWB-PLT-E1027-CON, with the field |

The four texts are the legacy texts carried unchanged and the contract adds no message identifier. The text shown when a route is blocked and held has no source at all and is Not specified in the source documents (GAP-2675; ASM-4394). The entry format of each message in a published catalogue is Not specified in the source documents and is published as the working read. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. SCR-16 Deed in lieu and SCR-14 Treatment record are reached through the gateway-bff composite route (DP-19), and the contract fixes only the answer those screens consume: the readiness section with its statuses, the rule version and the hold date, and the request that becomes the title-set task. The screen states of SCR-16 — Checks, appraisal, approved, transferred — are the runtime states of the application slice and are named in section 9 only to keep the vocabulary apart.

SCR-14 Treatment record, states empty, loading, error and no access: Not specified in the source documents (CG-ALL-8710).

SCR-16 Deed in lieu, states empty, loading, error and no access: Not specified in the source documents (CG-ALL-8711).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3013-CON-01 | AC1 | Contract | The extended answer schema validated: the ten properties, the stored, read and computed note on each, the additive note on the version, the absence of a status column and a personal-data scan of the example |
| TC-S2-E3013-CON-02 | AC2 | Contract | `TitleSetTaskRequest` validated: the references, R-SET-22, its version, the 5 working-day clock and the reason code; the lint that refuses a task, timer or case write |
| TC-S2-E3013-CON-03 | AC3 | Contract | The one operation entry linted against TSD S2 T-A.1 API-S2-002 and the legacy permission table: right R, 401, 403, 404, 503, no idempotency key and no write |
| TC-S2-E3013-CON-04 | AC4, AC5 | Contract | One compatible addition and one breaking change against the registry in BACKWARD mode; the three view ranges marked read only; the lint that refuses a derivation of a status in code |
| TC-S2-E3013-CON-05 | AC6 | Component | The six fakes answering every example, including the blocked answer, the missing title set and the no-collateral answer; the drift test failing on a consumer that drifts |
| TC-S2-E3013-CON-06 | AC7 | Contract | A value named by no source is published as the working read with the message Not specified in the source documents (GAP-2675; ASM-4396) and GAP-2675 stays open |
| TC-S2-E3013-CON-07 | AC8 | Contract | The rules BR1 to BR8 of section 8 and the rule coverage line read against sections 7 and 16 |
| TC-S2-E3013-CON-08 | AC9 | Contract | The TSD S2 v2 transition table for R-SET-22 and R-DIL-01; a proposed status change the table does not allow is refused by the lint |

The legacy test set of RWB-E3-013 — TC-E3-013-01 to TC-E3-013-06 — is carried by RWB-S2-E3013-APP and by the wave 2 integration harness, and no legacy id is renumbered here: these five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the statuses, the hold limit and the three clocks are values in force in the rule set, and the only values in the document are examples, marked as examples.
- No personal data in a schema, an example, a fake or a log: the examples carry a status, a rule version, a date and a business key, and the scan fails the build otherwise.
- No table, no column and no key in the contract: the statuses, the hold date and the check time stay out of `rwb_treatment` (DP-01; GAP-2675; ASM-4396).
- No status derived in code: the lint of AC5 fails any document or consumer that computes an encumbrance or title status from `lien_rank` or `register_date` (ASM-4395).
- No write operation and no task write: the check is started by rule and ends in a report, and the task is rwb-case's (ASM-4394).
- No event and no outbox row of the contract's own: the service topic is named and its events belong to other stories.
- ACE data only through the read-only views or the owner's contract: the view contract declares SELECT and no write, and no ACE object is copied (DP-05).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and a superseded marking.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-005 | Deed in lieu readiness, including the encumbrance check and an early valuation, is established before negotiation starts | Program 5.9 | FEAT-TRT-13 | 07 Route, settle and claim | BR1, BR2, BR4; R-DIL-01, R-DIL-02, R-DIL-04 | TC-S2-E3013-CON-01, TC-S2-E3013-CON-03 |
| REQ-S2-005 | The same readiness fact on the settlement side: a title set that cannot be re-created blocks the release | Program 5.9 | FEAT-TRT-13 | 07 Route, settle and claim | BR3; R-SET-22 | TC-S2-E3013-CON-02 |
| Legacy test set RWB-E3-013 | TC-E3-013-01, TC-E3-013-02, TC-E3-013-03, TC-E3-013-04, TC-E3-013-05, TC-E3-013-06 | Program 5.9 | The legacy story's own feature FEAT-TRT-13 | 07 Route, settle and claim | The legacy rules R-SET-22, R-DIL-01 and R-DIL-04 | Executed by RWB-S2-E3013-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3013-APP | App development | H consumer: fills the section, reads the views, writes the record and reports the task request against this contract and its fakes; owner of the legacy acceptance criteria |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment resource and its read, whose answer this contract extends with an optional section |
| RWB-S2-E3002-CON, RWB-S2-E3012-CON | Contract | Referred to: the offer surfaces of the same module, which are not declared here |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library the application slice calls in the caller's transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route the two screens use |
| rwb-case (P3) | Service, wave 1 | The case, its status, the parent `CaseWorkflow` and the task it raises on the request |
| P1 rwb-source-data | Service, wave 1 | Owns the ACE read and the alternative contract read of the three views (ASM-4395) |
| Wave 2 integration harness | Integration | I: the cross-service proof of the readiness path against the live owners, with the `-ITG` copies of the legacy test set |

### 19. Out of scope

- The behaviour behind the section — the view read, the rule evaluation, the record write and the stage outcome: RWB-S2-E3013-APP.
- The treatment resource, its create, its read and its element: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The settlement and deed-in-lieu offer surfaces, the price, the floor and the second signature: RWB-S2-E3002-CON, RWB-S2-E3003-CON and RWB-S2-E3012-CON.
- The asset unlock, the field inspection and the document set that follow this check: RWB-S2-E3014-APP, RWB-S2-E3015-APP and RWB-S2-E3018-APP.
- The case, its status, the parent `CaseWorkflow`, the task it raises and the timer it holds: rwb-case (P3), which owns them (ASM-4394).
- The ACE views, their grant, their ingestion from CCMS and the Land Office request: P1 rwb-source-data, P2 rwb-integration and the ACE DB stories; the fallback to the rwb-source-data contract read is theirs to price (ASM-4395).
- The decision-record library, its `MANDATORY` transaction, its chain and its envelope: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-16: RWB-PLT-N001-CON and the screen owners (DP-19).
- The DEEDINLIEU and SETTLEMENT rule packages, their authoring, their promotion and their version labels: P7 rwb-decision and the service-template runtime (ASM-4397).
- The two events the application slice consumes, `rwb.decision.RulePackageInForce.v1` and `rwb.deviation.DeviationRaised.v1`: their schemas belong to P7 and S8.
- The error and message catalogue of the platform, the Thai texts and the incident route: the platform library stories (DL10).
- The cross-service proof of the readiness path and the `-ITG` copies of the legacy test set: the wave 2 integration harness.
