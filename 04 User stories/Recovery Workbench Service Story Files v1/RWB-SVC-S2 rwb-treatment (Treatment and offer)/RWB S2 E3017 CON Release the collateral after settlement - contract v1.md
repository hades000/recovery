# RWB-S2-E3017-CON Release the collateral after settlement - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-017 for rwb-treatment. The legacy acceptance criteria stay with the application slice; every criterion here is new (D-RCV-60) and tests only the contract deliverable in the title. The contract publishes the release surface of the service on base `/api/recovery/treatment/v1` (DP-13): the `collateralRelease` section of the treatment answer as a compatible addition at major version 1, the schemas of `rwb.treatment.CollateralReleaseRequested.v1` and `rwb.treatment.CollateralReleased.v1` on topic `rwb.treatment.events.v1`, the read-only column contract of the four ACE views it depends on (DP-05), the error set and the fakes, with the section, the two events and the release vocabulary declared as the working read because no source gives them a shape (GAP-2683; ASM-4422). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3017-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-017 |
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
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner for rwb-treatment**, I want **the published contract of the collateral release — the `collateralRelease` section of the treatment answer with the release status, the securities and the rule version that decided them, the two release events on the service topic with their CloudEvents envelope and dedupe key, the read-only column contract of the four ACE views the facts come from, the error set, the release vocabulary, the compatibility rule and the fakes — instead of the monolith's one `recovery` schema and one in-process release call**, so that **the application slice, the gateway route, rwb-case's parent workflow, the platform release adapter and the wave 2 harness all build against one frozen release surface from Day 1, and no consumer invents a column, an event or a status that the source never gave**.

This story owns:

- the `collateralRelease` section of the treatment answer: its name, its properties, which of them are stored and which are computed per request, and the statement that it is an optional addition to the treatment resource of RWB-S2-E3001-CON;
- the schemas of the two events the release publishes, with their CloudEvents envelope, their dedupe key, their retry and `.dlt` topics and the rule that no personal data enters an event;
- the release vocabulary: the values a release status may take at run time, each tied to the read fact it comes from and never to an enumeration written in code;
- the read-only column contract of `v_ace_account`, `v_ace_payment`, `v_ace_collateral` and `v_ace_collateral_detail`, with the statement that the legacy `in_active` fact is a column of that read and is never derived in code;
- the error set, the compatibility rule, the pinning rule, the drift test and the fake set every consumer uses.

It does not own: the behaviour behind the section, which is RWB-S2-E3017-APP; the treatment resource, its create, its read and its element, which are RWB-S2-E3001-CON; the settlement offer and approval surfaces, which are RWB-S2-E3002-CON and RWB-S2-E3003-CON; the case status, the task and the timers, which are rwb-case's; the decision-record library, which is RWB-PLT-E1027-CON; the gateway-bff composite route, which is RWB-PLT-N001-CON; the CCMS outbound adapter, which is platform and rwb-integration work; and the ACE views themselves, their grant and their ingestion, which are P1's and the ACE DB stories'.

### 2. Business rationale

Legacy RWB-E3-017 had no contract to publish: the securities were rows read in the same process, the release was a call inside the same module, the decision log was a row beside them, and the two views were columns of the one schema. The microservice split removes that option. The facts now come from ACE views read by rwb-treatment, the instruction leaves as an event of this service and is carried to CCMS by a platform adapter outside the 19, the case status is moved by rwb-case, the answer is served by the gateway route, and the harness proves the path across services, so five consumers need the same answer to the same questions before any of them writes code.

**The division of the legacy key is fixed.** The legacy acceptance criteria **AC1, AC2 and AC4 stay with RWB-S2-E3017-APP** and **AC3 with RWB-ITG-E3017-ITG**; every criterion in section 7 is new and tests only the contract deliverable in this title. The treatment resource and its read are RWB-S2-E3001-CON's, the offer surfaces are the siblings' of the same module, and nothing of either is restated here.

The contract has to exist first for three reasons. The **result has no field anywhere**: TSD S2 T3.1 gives `treatment` DF-TRT-001 to DF-TRT-033 and none of them is a release status, a request reference or a released date, the functional specification's A2.17 has no field catalog at all, and the legacy data table names the view fields only as ranges, so without a published section one consumer reads a release state from a table that will never hold it and another computes one from `lien_rank` in code (GAP-2683; ASM-4422). The **instruction has no published shape and no named carrier**: the legacy story sends it "through the outbound interface to CCMS", the connection matrix of Architecture v5 slide 13 gives rwb-treatment no cell to P2 rwb-integration and none to Outside, and the Work Package records no C and no X dependency, so the instruction has to be published as an event of this service that a platform adapter carries, not as a call from this service into a source system (ASM-4424). And the **ACE read is a dependency with no publication**: DP-05 allows either the service's own views or the contract read of rwb-source-data, and the choice belongs in one document, not in five consumers' heads (ASM-4421).

The contract also fixes what it does not do: it declares no business table, adds no column, publishes no workflow and no Schedule, and publishes no write operation, because the officer takes no action in the release and the release is started by the rule on the case signal.

The fake is the Day-1 unblocker: the application slice, the gateway route, the parent workflow's closure path, the platform adapter and the harness can build the requested, released, not-applicable and not-confirmed answers before the live views, the live case workflow, the live payment events and the live rule packages exist (Template and Rules §R5.4 class C).

### 3. Preconditions

- The service identity is fixed by Template and Rules §R4 and the context pack: schema `rwb_treatment`, base `/api/recovery/treatment/v1`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13).
- The release section has no source shape: TSD S2 T3.1 carries no release field, FSD S2 A2.17 has no field catalog, and the legacy story names the view fields only as ranges DF-ACE-001 to DF-ACE-042, DF-ACE-043 to DF-ACE-054, DF-ACE-091 to DF-ACE-098 and DF-ACE-196 to DF-ACE-207, so the section and its properties are the working read of ASM-4422 (GAP-2683).
- The confirmation condition of the legacy AC1 is the `in_active` fact, and no named view field carries it; the contract therefore states that it is a column of the ACE read and not a derived value, and the column name is the working read of ASM-4421 (GAP-2683).
- The read of the four views is fixed as DP-05's own-view form, which adds no dependency; the alternative, the contract read of rwb-source-data, would be a C dependency and is named as the fallback in section 19 (ASM-4421).
- The carrier of the instruction is fixed: it leaves as an event of this service on `rwb.treatment.events.v1` and the adapter that delivers it to CCMS (INT-10) is platform and rwb-integration work, so the contract publishes an event schema and declares no call to a source system (ASM-4424).
- The target state of the closure is fixed: the stage reports an outcome and the parent `CaseWorkflow` moves the case to PLAN_COMPLETED, COLLATERAL_RELEASE_REQUESTED or CASE_CLOSED_SETTLED, so the contract publishes the section and the events and declares no case write (ASM-4420).
- The capability area "Treatment and offer" and right R are the access declaration of TSD S2 T6.1 and the legacy permission table; the check is the guard library's and the contract declares the right only (ASM-4398).
- RWB-S2-E3001-CON is named and not restated: the release section is declared as an optional addition to the treatment element of that contract, at the same major version, so its consumers see a compatible change.
- RWB-PLT-E1027-CON and RWB-PLT-N001-CON are published, so the contract can name the record write and the composite route without redeclaring either (DP-03; DP-19).
- The validation messages keep their legacy identifiers and texts, and no published catalogue defines their entry format, so the entry format is the working read.
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), sits in contract group `CG-W2`, and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the `collateralRelease` section: its name, its properties, the stored and the computed ones, and its place in the treatment answer of RWB-S2-E3001-CON.
2. The author fixes the two events: their names on the service topic, their payload properties, the CloudEvents envelope, the dedupe key, the retry and `.dlt` topics, and the rule that no personal data enters either.
3. The author fixes the release vocabulary: the status a release may show, the read fact each value comes from, and the statement that no value is an enumeration written in the document.
4. The author fixes the read-only column contract of the four views: the field identifiers, the column names the source gives and the `in_active` fact it does not.
5. The author fixes the error set: the status codes, the message identifiers and the texts, and the note that no idempotency key applies to a read while the event carries one for its dedupe.
6. The author writes the compatibility rule — an optional section may be added at the same major version, an event property may be added and never removed, and a breaking change raises major version 2 — and the pinning rule for the consumers.
7. The author writes the negative rules: no table, no column for a release status, no derivation of a status in code, no case write, no direct call to CCMS and no ACE write.
8. The lint and schema steps run: the operation reference compared against TSD S2 T-A.1, the section and the two events validated against the document and the event catalogue, the examples scanned for personal data, and the error table checked against the message identifiers.
9. The fake set is generated from the document: the requested, released, not-applicable and not-confirmed answers, the refusal answer, the failed record answer and the unpublished-instruction answer.
10. The contract test runs the fakes against the document on every change and fails the build on any drift; the document and the fakes are published at v1 and the consumers pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The section is published as required, or without a version tag on the treatment answer | The schema validation fails the build; the section is optional on the answer of RWB-S2-E3001-CON | None | AC1 |
| X2 | A release status is published as a column of `rwb_treatment`, or the document says the status is derived from `lien_rank` or `register_date` | The schema and lint steps fail the build; the status stays a property of the read and a value of the vocabulary | None | AC1, AC5 |
| X3 | An event is published without a dedupe key, with a personal field, or with a payload property that the section does not have | The schema and lint steps fail the build; an event property is added and never removed | None | AC2 |
| X4 | The document declares a call from this service to CCMS, or a case write on the closure | The lint fails the build; the instruction is an event and the closure is the parent's | None | AC2, AC3 |
| X5 | An error answer is published without a message identifier, or with a code the legacy story does not carry | The error-table check fails the build; every code is mapped to its identifier and its text | None | AC3 |
| X6 | A breaking change is made to a path, a property, an event name or the answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC4 |
| X7 | A consumer ships without the drift test, or its code drifts from the published schemas | The registry refuses the change and the drift test fails that consumer's build | None | AC6 |
| X8 | A value a consumer needs is named by no source — the section name, a property name, the `in_active` column or a release event name | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2683; ASM-4422) | Section 3 |

X1 and X6 are contract-governance paths, X2, X3 and X4 are the paths an invented column, event or call adds, X5 is the error rule, X7 is the drift rule of class C, and X8 is the reason the section, the events and the vocabulary are published as a working read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, two schemas and fakes; builds against nothing but the two named contracts, reads no business data and starts on Day 1 |
| Negotiable | The property names, the event payload names and the fixture set are open until v1 is frozen; the operation reference, the two event names, the error set and the compatibility rule are fixed |
| Valuable | Unblocks the application slice, the gateway route, the parent workflow's closure path, the platform adapter and the wave 2 harness on Day 1 and keeps the release status out of the schema |
| Estimable | One section, two event schemas, nine errors and codes, one vocabulary, two rules and seven fakes |
| Small | One sprint for the document, the schemas, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: collateral release contract

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the service base is /api/recovery/treatment/v1, the schema rwb_treatment and the topic rwb.treatment.events.v1
    Given the contract declares the release section, the two release events and the view column contract only

  Scenario: AC1 The release section is fixed as an optional addition to the treatment answer (new, D-RCV-60)
    Given the answer schema of the treatment read of RWB-S2-E3001-CON
    When the extended schema is validated
    Then the answer carries an optional collateralRelease section with releaseStatus, requestRef, requestedAt, releasedAt, checkedAt, collateralCount, collateralNo, assetKey, ruleId and ruleVersion
    Then the document states that releaseStatus is a value of the ACE read of v_ace_collateral and is never derived in code from lien_rank or register_date
    Then the document states that the section is an additive, backward-compatible change at major version 1 and that RWB-S2-E3001-CON owns the operation entry
    Then the document declares no table and no column for a release status, a request reference or a released date
    Then an example carries a status, a rule version and a date and no national identifier, account number or name

  Scenario: AC2 The two release events are published on the service topic with their envelope and dedupe key (new, D-RCV-60)
    Given the event schemas of the document and the topic rwb.treatment.events.v1
    When both schemas are validated against the event catalogue and the naming rule
    Then rwb.treatment.CollateralReleaseRequested.v1 carries the caseId, treatmentId, accountKey, the collateralNo and assetKey list, requestRef, requestedAt, ruleId and ruleVersion
    Then rwb.treatment.CollateralReleased.v1 carries the caseId, treatmentId, accountKey, the released collateralNo and assetKey list, releasedAt, checkedAt, ruleId and ruleVersion
    Then each schema carries a CloudEvents envelope with a stable dedupe key and declares the retry and .dlt topic of the service
    Then the document states that the instruction to CCMS is this event carried by the platform adapter and that no call from this service to CCMS is declared
    Then no property of either schema is a name, a national identifier, an account number or a free-text note

  Scenario: AC3 The read surface, its access right and its error set are fixed (new, D-RCV-60)
    Given the operation section of the document
    When it is validated against TSD S2 T-A.1 and the legacy permission table
    Then the document names the read of the treatment answer at GET /treatments/{treatmentId} as the only surface the section is served through, under capability area Treatment and offer with right R
    Then no write operation is published, because the release is started by rule R-RES-33, R-SET-20 or R-DIL-27 on the case signal and the officer takes no action in it
    Then the entry declares 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 with MSG-P7-003
    Then the document maps MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P7-009 to the answers that carry them and adds no message identifier
    Then an error answer carries the message identifier, the merge fields and the trace identifier only

  Scenario: AC4 Versioning separates a compatible addition from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to the published surface
    Then adding an optional property, an optional section or a new optional event property keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a breaking change to the operation reference, a required property, an event name, an error code or the answer raises major version 2 and v1 is never edited in place
    Then each consumer pins a published version and raises a change request rather than a private variant

  Scenario: AC5 The view column contract is read only, and no status is derived or stored (new, D-RCV-60)
    Given the data section of the document and the lint rule of the document
    When the view contract is validated
    Then the document lists v_ace_account with DF-ACE-001 to DF-ACE-042, v_ace_payment with DF-ACE-043 to DF-ACE-054, v_ace_collateral with DF-ACE-091 to DF-ACE-098 and v_ace_collateral_detail with DF-ACE-196 to DF-ACE-207, each marked read only
    Then the document states that the release holds SELECT on the four views and writes no ACE object
    Then the document states that the legacy in_active fact is a column of that read whose name no source fixes, so the name is the working read
    Then the document fixes the release vocabulary of section 9 and states that no value is an enumeration written in code
    Then the lint fails the build if the document declares a write, a table copy or a derivation of a fact in code

  Scenario: AC6 The fake answers the document and every consumer runs the drift test (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the release fake, the event fake, the error fake, the treatment resource fake, the composite route fake and the adapter fake
    Then the release fake answers a requested release, a released treatment, an account with no active security and a request still open at the read time
    Then the event fake answers a request event and a released event with their envelope and dedupe key, and an event with a personal field refused as invalid
    Then the error fake answers 403, 404, 422 and 503 with their message identifiers and no personal data
    Then the drift test fails the build of any consumer whose request, answer, event or error does not match section 12
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here, because **AC1, AC2 and AC4 of RWB-E3-017 are owned by RWB-S2-E3017-APP** and **AC3 by RWB-ITG-E3017-ITG**, and every identifier, rule, message and field range is taken from the legacy story, the TSD appendix or the rule set character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The release answer is one optional section of the treatment answer of RWB-S2-E3001-CON, at the same major version, and no consumer carries a private copy of it | GAP-2683; ASM-4422 |
| BR2 | The release status and the released date are values of the ACE read and are never derived in code and never stored in this schema | Legacy AC1; R-SET-21; DP-05; ASM-4421 |
| BR3 | The instruction to CCMS is an event of this service; the document declares no call from this service to a source system and no case write on the closure | ASM-4424; ASM-4420 |
| BR4 | Every release event carries a stable dedupe key and its retry and `.dlt` topic, so a redelivery is deduplicated and a failure is not lost | DP-09 semantics of the service template; §R4 |
| BR5 | The four views are read with SELECT only under DP-05; no ACE object is written and no view is copied into `rwb_treatment` | DP-05; DP-01 |
| BR6 | The contract declares the access right only; the check is the guard library's on capability area "Treatment and offer" | TSD S2 T6.1; ASM-4398 |
| BR7 | A published version is never edited: a compatible addition stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |
| BR8 | No value a business person may change is enumerated in the contract: the statuses, the due count and the confirmation limit are values in force, and the only values in the document are examples | BR-S2-017 |

**Where each rule lives in the target.** BR1 is the section table and the note on the operation reference. BR2 is the stored-versus-read column of every property and the lint rule of X2, and it is the reason the section exists at all rather than a set of columns. BR3 is the event section, the negative rule of X4 and the statement that the adapter is outside the 19. BR4 is the envelope table and the dedupe key of every event. BR5 is the view contract and the lint rule of AC5. BR6 is the access column and the error table. BR7 is the compatibility section and the pinning rule. BR8 keeps every status an example and never an enumeration.

### 9. State transitions

None at run time: a document and a schema have no state. Two vocabularies are fixed here, and the runtime transitions behind them are specified by RWB-S2-E3017-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Release answer | Not requested | No release event exists for the treatment; the section is absent or its status is empty |
| Release answer | Requested | The request event is published and the request reference and date are carried |
| Release answer | Released | The read shows every security of the account inactive and the released date is carried |
| Release answer | Not applicable | No active security is found for the account; the answer carries the checked time |
| Release answer | Undetermined | The read returns no security row at all and no release decision is possible |
| Event | Requested | `rwb.treatment.CollateralReleaseRequested.v1` is on the topic |
| Event | Released | `rwb.treatment.CollateralReleased.v1` is on the topic |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited in place |

The case states PLAN_RUNNING, PLAN_COMPLETED, PAYMENT_CLEARED, COLLATERAL_RELEASE_REQUESTED, CASE_CLOSED_SETTLED and ASSET_ON_BOOKS are rwb-case's and are named in the document only as the states the rule leads to.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the section and event schemas, the error table and the fakes |
| The service team of rwb-treatment | Consumes the contract, pins the version and raises a change request rather than a private variant |
| The rwb-treatment tech lead | Confirms that the section, the two events and the vocabulary are the ones the application slice fills and publishes |
| The rwb-case owner (P3) | Confirms that the closure of the case is the parent's and that no case write is declared |
| The P1 rwb-source-data owner | Confirms the read-only view contract and the fallback to its own contract read |
| The platform integration owner (P2) | Confirms that the adapter that delivers the instruction to CCMS subscribes to the two events and owns the transport |
| The platform edge owner | Confirms the composite route the two screens use, which this contract names and does not declare |
| The wave 2 integration harness owner | Confirms the fake set is enough to prove the cross-service path |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes the section, two event schemas, codes, message identifiers and examples; no customer, account or case value appears |
| Stored fields referenced | DF-TRT-003 `decision_log_id`, DF-TRT-013 `outcome` and DF-TRT-014 `outcome_at` of `treatment`, referenced through the section and declared by RWB-S2-E3001-CON, not redefined here |
| Read fields referenced | DF-ACE-001 to DF-ACE-042 of `v_ace_account`, DF-ACE-043 to DF-ACE-054 of `v_ace_payment`, DF-ACE-091 to DF-ACE-098 of `v_ace_collateral` and DF-ACE-196 to DF-ACE-207 of `v_ace_collateral_detail`, each read only |
| Personal data | None. The examples carry a status, a rule version, a date and a business key, and the actor and trace references are identifiers, never names |
| Tables published | None. The contract declares no table and no column; `treatment` is the application slice's and `decision_record` is the library's (DP-01; DP-03) |
| Field identifiers | The stored fields and the view fields carry the identifiers above; the section's own properties and the two event payloads carry none, because no source gives them one (GAP-2683; ASM-4422) |

The two places where the contract could leak a value are the release status and the event payload: the document therefore fixes that `releaseStatus` is a value of the read and never an enumeration of this contract and never a default, and that no event property carries a personal field, a free-text note or an amount.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). The contract declares the release section and names the one surface it is served through; the operation entry belongs to RWB-S2-E3001-CON and this contract adds an optional section to its answer at major version 1.

| Method | Path | Answer | Access | Idempotency |
|---|---|---|---|---|
| GET | `/treatments/{treatmentId}` | The treatment element of RWB-S2-E3001-CON with the optional `collateralRelease` section: `releaseStatus`, `requestRef`, `requestedAt`, `releasedAt`, `checkedAt`, `collateralCount`, `collateralNo`, `assetKey`, `ruleId` and `ruleVersion` | Treatment and offer, right R | Not applicable; the read changes no state |

No write operation is published. R-RES-33, R-SET-20 and R-DIL-27 start the release on the case signal, the branch reports its outcome to the parent `CaseWorkflow`, and the officer takes no action in it, so there is nothing to post or patch; the legacy endpoint table of RWB-E3-017 names the treatment create and the treatment read only, which is consistent with this surface (GAP-2683; ASM-4420, ASM-4422). The errors are 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 with MSG-P7-003. The reasons the section has no source shape, and whether the bank ever intended a separate release operation or a REST call to CCMS, are Not specified in the source documents (GAP-2683; ASM-4422).

#### 12.2 REST operations consumed

None. The contract declares the surface and calls no service: the case signal arrives on the parent's signal, the clearance arrives on the rwb-payment event, the facts are read from the four views, and the decision record is an in-process call of RWB-PLT-E1027-CON (DP-03; DP-05; ASM-4420). No call from this service to CCMS is declared, because the instruction is an event carried by the platform adapter (ASM-4424). This is why the Work Package records no C dependency for the pair.

#### 12.3 Events published

| Event | Topic | Payload properties | Envelope and delivery |
|---|---|---|---|
| `rwb.treatment.CollateralReleaseRequested.v1` | `rwb.treatment.events.v1` | `caseId`, `treatmentId`, `accountKey`, `collateralNo`, `assetKey`, `requestRef`, `requestedAt`, `ruleId`, `ruleVersion` | CloudEvents 1.0 envelope, stable dedupe key on `requestRef` and the release event, retry and `rwb.treatment.events.v1.dlt` |
| `rwb.treatment.CollateralReleased.v1` | `rwb.treatment.events.v1` | `caseId`, `treatmentId`, `accountKey`, `collateralNo`, `assetKey`, `releasedAt`, `checkedAt`, `ruleId`, `ruleVersion` | CloudEvents 1.0 envelope, stable dedupe key on the request reference and the release event, retry and `rwb.treatment.events.v1.dlt` |

The two schemas are the deliverable of AC2 and the two names are the working read of ASM-4422 (GAP-2683). Neither payload carries a name, a national identifier, an account number, an amount or a free-text note, and neither carries the title detail of `v_ace_collateral_detail`. The `.dlt` topic name follows the per-service pattern of §R4. `TreatmentApproved` (EV-10) and `TreatmentBooked` (EV-11) belong to the approval and booking stories and are referenced by the catalogue, not declared here.

#### 12.4 Events consumed

None declared. The contract declares no subscription; the three events the application slice consumes — `rwb.payment.PaymentCleared.v1`, `rwb.decision.RulePackageInForce.v1` (EV-30) and `rwb.deviation.DeviationRaised.v1` (EV-06) — belong to P8, P7 and S8 and are named in section 19, and the case status is a workflow signal and not an event of this contract (ASM-4420). The confirmation of a release is not an event at all: it is the re-read of the two collateral views (AC1 of the application slice).

#### 12.5 Workflows and activities

None. The contract declares no workflow and no activity. It states only that the section is filled and the two events published inside the activities of the release branch on the owner's own task queue, and that the decision record is called from that activity, so a replay reuses the recorded decision; the branch itself is RWB-S2-E3017-APP's release branch of `TreatmentWorkflow` on `rwb-treatment` (DP-12).

#### 12.6 Schedules

None. The contract declares no Temporal Schedule and no legacy Quartz job. The confirmation of a release is a re-read on a durable timer and on the ACE data-ready signal, and its interval and limit are values in force in the rule set, not part of the published surface. The service has no legacy Quartz job in this legacy key.

#### 12.7 Tables owned

None. The contract declares no table, no column and no key, and the negative rule is the deliverable: no release status, request reference, released date or confirmation time column exists in `rwb_treatment`, because no source gives one and a column would freeze a status that the rule set and the ACE read own (GAP-2683; ASM-4422; DP-01). `treatment` is RWB-S2-E3001-APP's business table, `decision_record` is the library object of RWB-PLT-E1027-CON, `decision_log_entry` is P7's ledger, and the case, the task and the timer are rwb-case's; all are named here only.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Release fake | The `collateralRelease` section on `GET /treatments/{treatmentId}` | A requested release, a released treatment with two securities, an account with no active security, and a request still open at the read time |
| Event fake | The two event schemas on `rwb.treatment.events.v1` | A request event and a released event with their envelope and dedupe key; an event carrying a personal field refused as invalid; a redelivery deduplicated on the same key |
| Error fake | The error table | 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 with MSG-P7-003, each with its identifier, its merge fields and a trace identifier |
| Treatment resource fake | The answer the section extends | The treatment element of RWB-S2-E3001-CON, referenced and not restated |
| Composite route fake | The gateway-bff composite route of RWB-PLT-N001-CON | One hop for SCR-14, joining the treatment read with its release section; a refused route for a role without right R |
| Decision-record fake | The library write the application slice makes | An accepted record with an entry reference; a refusal with MSG-P7-009 and the field; a failed write with MSG-P7-003 |
| Adapter fake | The platform adapter that carries the instruction to CCMS | An accepted instruction with a request reference; a transport failure that leaves the event unpublished for the relay to retry |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consumer rather than as a surprise at run time. The treatment resource fake, the composite route fake and the decision-record fake are the published contracts of their stories and are referenced here, not redeclared.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation reference, extended | 0 | OpenAPI 3.1 fragment; one hop to the service, 2 s timeout |
| Kafka | 2 event schemas | 0 | Service topic, CloudEvents envelope, dedupe key, retry and `.dlt` topic |
| SQL view | 4 read-only views referenced | 4 | SELECT only under DP-05; no write to any ACE object |
| Temporal | 0 | 0 | The contract states the section is filled in an activity and declares no workflow |
| File, Nexus | 0 | 0 | No file and no Nexus operation crosses the contract; the CCMS transport is the adapter's |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the OpenAPI fragment and the section schema in `th.co.scb.ace.workbench.recovery.treatment.api`, the two event schemas in the same package, the error table and the compatibility note in the contract document, and the fake set as a test asset. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2683; ASM-4422).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 enters the contract as one statement — the section is written with a record in the caller's transaction — and the H dependency sits on the application slice, which calls the library. DP-05 is the read-only column contract of the four views and the reason the release status is published as a read value. DP-13 is the base of the operation reference and the reason the legacy base appears nowhere in the document. DP-19 is the route the two screens use, named here so that the composite route fake has an owner.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentReadOpenApi` | OpenAPI 3.1 fragment | The one operation reference, its parameter, its errors, its access declaration and the note that it extends RWB-S2-E3001-CON |
| `ReleaseSectionSchema` | Answer schema | The ten properties of the section and the stored, read and computed note on each |
| `ReleaseEventSchemas` | Two event schemas | The request event and the released event, their payloads, envelope, dedupe key and `.dlt` topic |
| `AceViewContract` | Document table | The four views, their field identifiers, their read-only mark and the `in_active` fact whose column name no source fixes |
| `ReleaseVocabulary` | Document table | The five states of the answer and what each means, with no enumeration in code |
| `ErrorCatalogue` | Document table | The status codes, the message identifiers, the legacy texts and the merge fields |
| `CompatibilityNote` | Document section | The additive-versus-breaking rule, the pinning rule and the negative rules |
| `ReleaseFakeSet` | Test asset | The seven fakes of section 12.8 and the drift test every consumer runs |

**Database.** None. The contract creates no table, adds no column and declares no key; the negative rules of section 12.7 and of AC5 are the deliverable, and a review that finds a release status, a request reference or a released date column in `rwb_treatment` fails this story.

**Configuration and reference data.** The contract fixes no business value. The statuses, the due count and the confirmation limit are values in force in the rule set; the only values in the document are the example values, and they are marked as examples. Capability area "Treatment and offer" and right R are read from rwb-access through the guard library, which the application slice calls (ASM-4398). The grant on the four views is a DB story's (DP-05; ASM-4421).

**Build steps**

1. Write the operation reference, its access right and its errors, and lint that no write operation and no second form appear (AC3).
2. Write the `collateralRelease` section, its ten properties and the stored, read and computed note on each (AC1).
3. Write the two event schemas with their payloads, envelope, dedupe key and `.dlt` topic, and lint that no personal field and no amount enters either (AC2).
4. Write the `AceViewContract` table with the four field ranges and the `in_active` fact, and the lint that refuses a derivation in code (AC5).
5. Write the release vocabulary of section 9 and the note that no value is an enumeration in code (AC5).
6. Write the error table with the four identifiers and their legacy texts, and validate one answer per code (AC3).
7. Write the compatibility note, the pinning rule and the negative rules (AC4).
8. Generate the seven fakes and the drift test; wire the drift test into the build of RWB-S2-E3017-APP, the gateway route, the parent workflow's closure path, the platform adapter and the wave 2 harness (AC6).
9. Publish v1 and record the pinned version of each consumer.

**Feature flag.** `rwb.treatment.collateral-release-contract`.

**Done when.** The document, the section schema and the two event schemas validate, the operation lint passes with one read reference and no write, the error table matches the four legacy identifiers and texts, the seven fakes answer every example including the not-applicable answer and the open request, the drift test is green on the build of this story and on the build of the application slice, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, or the balance is not zero and no security is found for the account | Enter {field}. | 422 on the answer, or the not-applicable state of the section; the field name is carried |
| MSG-P4-002 | The role does not hold right R | You cannot {action} here. Your role does not include it. | 403, from the guard library |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, from RWB-PLT-E1027-CON |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. | 422, from RWB-PLT-E1027-CON, with the field |

The four texts are the legacy texts carried unchanged and the contract adds no message identifier. MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the offer messages of the module and are not part of this surface. The text shown while a release is requested and not yet confirmed has no source at all and is Not specified in the source documents (GAP-2683; ASM-4420). The entry format of each message in a published catalogue is Not specified in the source documents and is published as the working read. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. SCR-14 Treatment record and SCR-15 Settlement offer are reached through the gateway-bff composite route (DP-19), and the contract fixes only the answer those screens consume: the release status, the securities released with their business keys, the request and released dates, the read time and the rule version. The screen states of SCR-14 — Draft, submitted, approved, booked, broken — are the runtime states of the application slice and are named in section 9 only to keep the vocabulary apart.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3017-CON-01 | AC1 | Contract | The extended answer schema validated: the ten properties, the stored, read and computed note on each, the additive note on the version, the absence of a release column and a personal-data scan of the example |
| TC-S2-E3017-CON-02 | AC2 | Contract | The two event schemas validated against the catalogue and the naming rule: payloads, envelope, dedupe key, retry and `.dlt` topic; the lint that refuses a personal field, an amount and a call to CCMS |
| TC-S2-E3017-CON-03 | AC3 | Contract | The operation reference linted against TSD S2 T-A.1 and the legacy permission table: right R, 401, 403, 404, 422, 503, no write operation and no declared CCMS call |
| TC-S2-E3017-CON-04 | AC4 | Contract | One compatible addition and one breaking change against the registry in BACKWARD mode, for the answer and for an event property |
| TC-S2-E3017-CON-05 | AC5 | Contract | The four view ranges marked read only, the `in_active` fact marked as a read value, the release vocabulary fixed, and the lint that refuses a derivation of a fact in code |
| TC-S2-E3017-CON-06 | AC6 | Component | The seven fakes answering every example, including the not-applicable answer, the open request and the refused personal field; the drift test failing on a consumer that drifts |

The legacy test set of RWB-E3-017 — TC-E3-017-01 to TC-E3-017-06 — is carried by RWB-S2-E3017-APP and by the wave 2 integration harness, and no legacy id is renumbered here: these six are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the statuses, the due count and the confirmation limit are values in force in the rule set, and the only values in the document are examples, marked as examples.
- No personal data in a schema, an example, a fake, an event or a log: the examples carry a status, a rule version, a date and a business key, and the scan fails the build otherwise.
- No table, no column and no key in the contract: the release status, the request reference and the released date stay out of `rwb_treatment` (DP-01; GAP-2683; ASM-4422).
- No fact derived in code: the lint of AC5 fails any document or consumer that computes a release status from `lien_rank`, `register_date` or a balance arithmetic of its own (ASM-4421).
- No write operation, no case write and no call to CCMS: the release is started by rule, ends in a report, and the instruction is an event carried by the platform adapter (ASM-4420, ASM-4424).
- No event without a dedupe key and a `.dlt` topic: a consumer that cannot deduplicate a redelivery fails the drift test.
- ACE data only through the read-only views or the owner's contract: the view contract declares SELECT and no write, and no ACE object is copied (DP-05).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and a superseded marking.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Program 5.9 | FEAT-TRT-17 | 07 Route, settle and claim | BR1, BR2, BR3; R-RES-33, R-SET-20, R-SET-21 | TC-S2-E3017-CON-01, TC-S2-E3017-CON-02, TC-S2-E3017-CON-03 |
| Legacy test set RWB-E3-017 | TC-E3-017-01, TC-E3-017-02, TC-E3-017-03, TC-E3-017-04, TC-E3-017-05, TC-E3-017-06 | Program 5.9 | The legacy story's own feature FEAT-TRT-17 | 07 Route, settle and claim | The legacy rules R-RES-33, R-SET-20 and R-DIL-27 | Executed by RWB-S2-E3017-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3017-APP | App development | H consumer: fills the section, reads the four views, publishes the two events, writes the record and reports the outcome against this contract and its fakes; owner of legacy AC1, AC2 and AC4 |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment resource and its read, whose answer this contract extends with an optional section |
| RWB-S2-E3002-CON, RWB-S2-E3003-CON | Contract | Referred to: the settlement offer and approval surfaces of the same module, which are not declared here |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library the application slice calls in the caller's transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route the two screens use |
| RWB-ITG-E3017-ITG | Integration | Owner of legacy AC3 and of the cross-service proof of the release path, with the `-ITG` copies of the six legacy test cases |
| rwb-case (P3) | Service, wave 1 | The case, its status, the parent `CaseWorkflow` and the closure it performs on the reported outcome |
| P8 rwb-payment | Service, wave 2 | Publishes the clearance that starts R-SET-20 |
| P2 rwb-integration | Service, wave 1 | Owns the adapter that delivers the instruction to CCMS (INT-10) and follows the two event schemas |
| P1 rwb-source-data | Service, wave 1 | Owns the ACE read and the alternative contract read of the four views (ASM-4421) |
| Wave 2 integration harness | Integration | I: the cross-service proof of the release path against the live owners, with the `-ITG` copies of the legacy test set |

### 19. Out of scope

- The behaviour behind the section — the view read, the rule evaluation, the two event writes, the record write and the stage outcome: RWB-S2-E3017-APP.
- The treatment resource, its create, its read and its element: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The settlement offer, the floor and the approval below the floor: RWB-S2-E3002-CON, RWB-S2-E3003-CON and their application slices.
- The deed-in-lieu transfer and its asset record, whose completion leads to the release call of R-DIL-27: RWB-S2-E3012-APP and S5 rwb-asset.
- The case, its status, the parent `CaseWorkflow`, the closure and the task it raises: rwb-case (P3), which owns them (ASM-4420).
- The ACE views, their grant and their ingestion from CCMS: P1 rwb-source-data, P2 rwb-integration and the ACE DB stories; the fallback to the rwb-source-data contract read is theirs to price (ASM-4421).
- The adapter that delivers the instruction to CCMS (INT-10), its transport, its file or message format and its retry: the platform integration stories and P2 rwb-integration (ASM-4424).
- The decision-record library, its `MANDATORY` transaction, its chain and its envelope: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-15: RWB-PLT-N001-CON and the screen owners (DP-19).
- The RESTRUCTURE, SETTLEMENT and DEEDINLIEU rule packages, their authoring, their promotion and their version labels: P7 rwb-decision and the service-template runtime (ASM-4423).
- The three events the application slice consumes, `rwb.payment.PaymentCleared.v1`, `rwb.decision.RulePackageInForce.v1` and `rwb.deviation.DeviationRaised.v1`: their schemas belong to P8, P7 and S8.
- The error and message catalogue of the platform, the Thai texts and the incident route: the platform library stories (DL10).
- The cross-service proof of the release path and the `-ITG` copies of the legacy test set: the wave 2 integration harness and RWB-ITG-E3017-ITG.
