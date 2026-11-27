# RWB-P4-E8009-CON Set the treatment policy by product

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8009-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E8009-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None declared; the P3 reference-load contract that the calls use is not declared in the metadata (GAP-0870) |
| Contract version | Major version 1 in the path `/api/recovery/access/v1`; the minor version is Not specified in the source documents (DOR-RWB-P4-E8009-CON-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-009 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 8 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **solution architect**, I want **the published contract baseline of the treatment policy edition of `rwb-access`: an OpenAPI 3.1 document for the upload and the read, the `ProductPolicyEdition` and `ProductPolicyEditions` schemas with the state set of LOV-VERSION-STATUS, the multipart request and the query parameters, one RFC 9457 error envelope with its message IDs, the consumed authorise, parameters and reference-load operations with their owners, one hop and the 2 s budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the administration screen through gateway-bff and the wave 4 harness can build against a fixed, testable boundary on Day 1, and the boundary states in writing that `rwb-access` is the door and that every band, floor and range stays with its owner**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-009 belong to RWB-P4-E8009-APP, and the ten criteria of section 7 test the document, the schemas, the state set, the envelope, the consumed declarations, the fakes, the table boundary, the versioning rule, the traceability of the rules and the 404 answer.

The boundary this baseline fixes is the D-RCV-60 split of RWB-E8-009: under the R-PREC default ruling the parameters and the reference data belong to P3 `rwb-case` (ASM-0071) and so do the reference-load operations (ASM-0041), while `rwb-access` provides the edition door and its record. The service facts are `rwb-access`, schema `rwb_access`, base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with the event names `rwb.access.<Event>.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

### 2. Business rationale

Contract-first REST, one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Here the contract also settles an ownership question the documents answer two ways: the legacy story wrote the policy number set into the monolith and named the rule-version endpoints, the TSD P4 v3 lists the list and reference-load paths in the access module, and the R-PREC default ruling puts parameters and reference data with `rwb-case`. A written contract is the only place where that split stops being an argument: the document declares the two operations `rwb-access` serves, declares the operations it consumes and their owners, declares that it writes no `lov_value`, `reference_version` or `reference_row` row and interprets no value of the edition, and states that the table code and the sheet names are reconciled at review before the baseline is frozen (GAP-0870; ASM-1577).

With the boundary fixed and faked, the app story builds without waiting for the `rwb-case` reference-load contract, the administration screen can be wired through gateway-bff on the same day, and a change on either side is caught by a contract test rather than in an integration window.

The baseline also fixes the one thing a reviewer of a policy change asks of it: an edition is identified by its product group, its policy version label, the load that holds it and its valid-from date, and nothing else is asserted about the values — so a printed record can be defended without the access service ever having held a band, a floor or a range.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), whose message carries the entry of an accepted edition.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19), which is the only consumer of the two operations.
- The platform error envelope and the RFC 9457 problem media type are the platform baseline; where this document narrows them it does so explicitly and never redefines them.
- The owners of the consumed operations come from the ownership map only: `GET /admin/parameters` and the reference-load operations are P3 `rwb-case`'s (ASM-0041), the load read is named as consumed and flagged, and the authorise operation is this service's own.
- The reference-load contract is not in this story's metadata contract-dependency list; the document declares the operations it consumes and the app story builds against that contract and its fake, with the missing dependency raised at D1 (GAP-0870; ASM-1577).
- The table code `product_policy` and the names of the three sheets of the workbook are Not specified in the source documents (GAP-0870; ASM-1577): the document carries both as named constants of the request and the review fixes them with the owner before the baseline is frozen.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document with the base path, the security scheme, the shared components and the two operations.
2. Fix the multipart request of the upload: the part `file`, the query `productGroup`, `policyVersion`, `validFrom` and `reason`, the required `Idempotency-Key`, and the named constants of the table code and the three sheets.
3. Fix `ProductPolicyEdition` and `ProductPolicyEditions`, including the state set of LOV-VERSION-STATUS and the rule that the read answers the state the owner reports and interprets no value.
4. Fix the product group as a value of LOV-PRODUCT, declared as reference data and never as a code list in the document.
5. Agree the error envelope and the message-ID mapping for 400, 401, 403, 409, 422 and 503, with the 422 that names the part or the field.
6. Declare the consumed operations with their owners, one hop and the 2 s client budget, and the flagged load read with its note.
7. State in the document that no band, floor or range is read, compared, cached or answered by `rwb-access`, and that no table of another service is named as this service's.
8. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
9. Add the contract tests: schema validation, the state set, the no-value check, the envelope and the message IDs, the consumed-owner check and the drift check between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-E8009-APP, the administration screen route of RWB-PLT-N001-CON and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 400, 401, 403, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A schema declares a band, a floor, a range, an amount, a percentage or a boundary | The check of AC2 fails and the field is removed before the tag | None | AC2 |
| X5 | The document declares the reference-load operations or the parameters read as provided by `rwb-access` | The review fails | None | AC5 |
| X6 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X7 | An example, a fake or a schema carries a name, an e-mail address or a personal field | The review and the pipeline refuse the document | None | AC6 |
| X8 | A state name outside LOV-VERSION-STATUS appears in the document | The check of AC3 fails and the name is corrected or the gap is raised | None | AC3 |
| X9 | The owner renames the load read or the parameters read | The contract test fails and the pinned version is raised at review | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema and the P3 contracts only |
| Negotiable | The sheet names, the table code and the exact wording of the 422 are settled with the owner and the product head at review; the two operations, the states, the envelope and the split are fixed by the target architecture |
| Valuable | Unblocks the app story, the administration route and the harness on Day 1, and writes down that the values have one owner |
| Estimable | One OpenAPI document, two schemas, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Treatment policy edition contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access side of the legacy journey is one workbook handed to the parameters owner and recorded by the door
    Given product group "MORTGAGE" is a value of LOV-PRODUCT and its version in force is read from the parameters contract

  Scenario: AC1 The OpenAPI 3.1 document describes the two operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the treatment policy edition is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/product-policies and GET /admin/product-policies/{productGroup} with the owner rwb-access
    Then the POST declares the multipart part file, the query productGroup, policyVersion, validFrom and reason, and the required Idempotency-Key header
    Then the POST names the Rules and parameters C letter and the read names the Rules and parameters R letter
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The edition, the read and the query are fixed, and no value is declared (new, D-RCV-60)
    Given the ProductPolicyEdition and ProductPolicyEditions schemas of the document
    When the schemas and the request of the document are reviewed
    Then the edition carries editionId, productGroup, policyVersion, loadId, state and validFrom
    Then the read carries productGroup, editions[], inForce with policyVersion and validFrom, chain and recordedAt
    Then productGroup is declared as one value of LOV-PRODUCT and the list is declared as reference data and not as a code list
    Then the document names the table code product_policy and the three sheets of the workbook as the constants of the request
    Then no schema, parameter, example or description carries a band, a floor, a range, an amount, a percentage or a boundary

  Scenario: AC3 The state set is the one of LOV-VERSION-STATUS and no value is interpreted (new, D-RCV-60)
    Given the state field of the edition schema
    When the POST /admin/product-policies or the read GET /admin/product-policies/{productGroup} returns an edition
    Then state is one of LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED
    Then the POST answers LOADED only, and the read answers the state the owner of the load reports
    Then the document states that rwb-access reads no value of the edition, compares none and answers none
    Then the document states that the version in force comes from the parameters contract and not from the edition file

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 400, 401, 403, 409, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 422 carries MSG-GEN-001 with the missing part of the workbook or the failing field, and 400 carries the malformed multipart answer
    Then 409 carries MSG-GEN-004 for a version the owner refuses, and 503 carries MSG-P7-003 for a record that cannot be written
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed with their owners (new, D-RCV-60)
    Given the authorise operation, the parameters read and the reference-load operations this service calls
    When the document is reviewed for each operation this service consumes
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters, POST /api/recovery/case/v1/admin/reference-loads and GET /api/recovery/case/v1/admin/reference-loads/{loadId} are declared as consumed with the owner P3 rwb-case
    Then the two reference-load operations and the parameters read carry the note that the metadata of this key names no P3 reference-load contract
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-case, rwb-decision or rwb-treatment is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no value and no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then no fake carries a band, a floor or a range value
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC7 The document declares no table of another service and no central ledger (new, D-RCV-60)
    Given the tables named in section 12.7 of the document
    When the table list of the document is reviewed
    Then every table named as this contract's is owned by P4 rwb_access
    Then no table of rwb_case, rwb_treatment or rwb_decision is named as this contract's
    Then a table of another service named as this contract's fails the build

  Scenario: AC8 A schema change is additive within major version 1 (new, D-RCV-60)
    Given the schemas of the document at major version 1
    When a schema of the document is changed
    Then an added field is accepted within major version 1
    Then a removed, renamed or retyped field or a removed state is refused as a new major version

  Scenario: AC9 Each business rule is traced to a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the Covered by column of each rule is reviewed
    Then every rule names at least one criterion of section 7
    Then every criterion named there has a test case row in section 16
    Then a rule with no criterion or no test case fails the build

  Scenario: AC10 A read of a product group with no edition answers 404 with the one envelope (new, D-RCV-60)
    Given the read operation GET /admin/product-policies/{productGroup} of the document
    When the read is made for a product group that has no edition
    Then it answers 404 with the one RFC 9457 problem response of AC4
    Then the response declares no edition and no value
```

These ten criteria test the artefact only. Neither legacy criterion of RWB-E8-009 is restated here: AC1 and AC2 belong to RWB-P4-E8009-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's base or path | DP-13; Architecture v5 slide 41 | AC1; TC-E8-009-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided, and its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-E8-009-CON-05 |
| BR3 | The document declares no table of another service and no central ledger; `lov_value`, `reference_version` and `reference_row` are P3's and `treatment` is S2's | DP-01; ASM-0071 | AC7; TC-E8-009-CON-07 |
| BR4 | The edition schema carries a product group, a policy version label, a load id, a state and a valid-from date, and no value of a band, a floor or a range | GAP-0870; ASM-1577 | AC2; TC-E8-009-CON-02 |
| BR5 | The state set is the one of LOV-VERSION-STATUS and the document declares no state of its own | TSD P4 v3 T3.2 and T4 | AC3; TC-E8-009-CON-03 |
| BR6 | Error responses use one envelope and one message ID per condition, and the business texts are copied unchanged from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4; TC-E8-009-CON-04 |
| BR7 | The POST requires the C letter and the read the R letter in Rules and parameters; the product head holds R only and proposes the edition, and the document states it | TSD P4 v3 T6.1; FSD P4 v3 A2.20.3.3; GAP-0870; ASM-1578 | AC1; TC-E8-009-CON-01 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field, or a removed state, is a new major version | Architecture v5 slide 42 | AC8; TC-E8-009-CON-08 |
| BR9 | No personal data in a schema, an example or a fake: references, codes, versions, load ids and dates only | NFR-040; DP-05 | AC6; TC-E8-009-CON-06 |
| BR10 | The document states that `rwb-access` interprets no value of the edition, and that the version in force is read from the parameters contract | REQ-DRI-010; REQ-S2-004; ASM-1577 | AC3; TC-E8-009-CON-03 |

### 9. State transitions

The contract has its own lifecycle, and it also declares the state set of a load.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the envelope and the consumed set are described | In review |
| In review | Consumer sign-off | The app story, the administration route and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, a status or a message ID is added within major version 1 | Baselined |
| Baselined | Breaking change | A field or a state is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

| State declared | Meaning in the contract | Who moves it on |
|---|---|---|
| `LOADED` | The owner stored and versioned the rows and answered the load; the edition waits for the load owner's approval | The approval on the console reference-load path (RWB-P4-AD010-APP) |
| `VALIDATED` | A value of LOV-VERSION-STATUS the owner may report; the document declares it and `rwb-access` never produces it | The owner |
| `APPROVED` | The load owner approved the version and its valid-from date has not arrived | The owner, from the valid-from date |
| `IN_FORCE` | The version the product group is decided under | The owner, on the valid-from date (R-UNI-38) |
| `SUPERSEDED` | A newer edition reached its valid-from date | The owner |
| `ROLLED_BACK` | The owner rolled the version back | The owner |
| `REFUSED` | The owner refused the version; nothing was stored | Terminal: a corrected workbook is a new edition |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version, and confirms the table code and the sheet names once they are reconciled with the owner |
| Tech lead of rwb-case (P3) | Reviews the consumed parameters read and reference-load operations as rwb-access uses them, and owns their definitions, the rows and the load state |
| Product head (Mortgage, HP, SSME) and RW-COE | Review the operation as the screen calls it: the product head proposes an edition and RW-COE holds the C letter that submits it (GAP-0870; ASM-1578) |
| Tech lead of the gateway-bff route | Reviews the two provided operations as the only ones the administration route calls |
| Data steward | Confirms that no personal data field is declared in a schema, an example or a fake, and that no value of the edition is declared |
| The risk and model risk officer (RW-RISK) | Confirms that the A letter is the load approval on the console path and not a right of this document |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `ProductPolicyEdition` | `editionId`, `productGroup`, `policyVersion`, `loadId`, `state`, `validFrom` | Not specified in the source documents (DOR-RWB-P4-E8009-CON-7) |
| `ProductPolicyEditions` | `productGroup`, `editions[]` of the edition with `recordedAt`, `inForce` with `policyVersion` and `validFrom`, `chain`, `recordedAt` | Not specified in the source documents (DOR-RWB-P4-E8009-CON-7) |
| Upload request | `multipart/form-data` part `file`; query `productGroup`, `policyVersion`, `validFrom`, `reason`; `Idempotency-Key` required; the table code `product_policy` and the three sheets named as constants | Not specified in the source documents (DOR-RWB-P4-E8009-CON-7) |
| State set | LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED, the values of LOV-VERSION-STATUS (TSD P4 v3 T3.2) | Not specified in the source documents (DOR-RWB-P4-E8009-CON-7) |
| Record | The decision-record entry of DP-03 with the edition id, the product group, the policy version, the load id, the valid-from date, the version in force and the caller reference (DF-DEC-001 to DF-DEC-018) | Not specified in the source documents (DOR-RWB-P4-E8009-CON-7) |
| Refusal | `messageId` MSG-P4-001, MSG-P4-002, MSG-GEN-001 with the part or the field, MSG-GEN-004 or MSG-P7-003, with the field list in the body | Not specified in the source documents (DOR-RWB-P4-E8009-CON-7) |

The field-level detail of the request — the header row of each sheet, the accepted media types of the workbook, the maximum size of an upload and the exact wording of the answer — is Not specified in the source documents (GAP-0870; ASM-1577) and is fixed by section 12.1 and confirmed with the owner and the product head before the endpoint is frozen. The record code of an edition is Not specified in the source documents (GAP-0870; ASM-1579) and the review fixes it with the ledger owner.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/product-policies` | `multipart/form-data` with the part `file` (the workbook: the bands sheet, the floors sheet and the ranges sheet), the query `productGroup`, `policyVersion`, `validFrom` and `reason`, and the required `Idempotency-Key`; answers 201 with `editionId`, `productGroup`, `policyVersion`, `loadId`, `state` `LOADED` and `validFrom`, and a `Location` naming the edition read | Rules and parameters C, scope applied |
| GET | `/admin/product-policies/{productGroup}` | `ProductPolicyEditions` with `productGroup`, `editions[]`, `inForce`, `chain` and `recordedAt`; the state of a load is the state the owner reports | Rules and parameters R, scope applied |

Errors for both: 401 no session (MSG-P4-001), 403 no letter in Rules and parameters (MSG-P4-002), 422 a required field empty, a product group not in its list, a part of the workbook missing or `validFrom` before the version in force (MSG-GEN-001, with the part or the field named), 409 the owner refuses the version (MSG-GEN-004), 503 the owner is unavailable or the record cannot be written (MSG-P7-003); the POST also declares 400 for a malformed multipart body. The POST requires the `Idempotency-Key` header and the read is not applicable on it. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field or a removed state is a new major version tested against the registry with BACKWARD compatibility (BR8). The table code `product_policy` and the names of the three sheets are declared as named constants of the request and are Not specified in the source documents (GAP-0870; ASM-1577).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters C and R answer behind both operations, cached for the request |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The version in force of the product group, its `valid_from` and its policy version label (DP-06) |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | The load: multipart `file`, `table` (`product_policy`) and `validFrom`; the owner stores and versions the rows and answers the load id and its state |
| GET | `/api/recovery/case/v1/admin/reference-loads/{loadId}` | P3 rwb-case | The state of a load for the read of the editions; the TSD P4 v3 appendix T-A has no load read, so it is named as consumed and flagged (GAP-0870; ASM-1577) |

None of the four is declared as provided by rwb-access, and no operation of `rwb-decision` or `rwb-treatment` appears in the document at all. The reference-load contract is not in the metadata contract-dependency list of RWB-P4-E8009-APP, and the document records the missing dependency as the gap of this key (GAP-0870; ASM-1577).

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of an accepted edition with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope: the edition id, the product group, the policy version, the load id, the valid-from date, the version in force and the caller reference |

Nothing is published on `rwb.access.events.v1` by this document: a treatment policy version is not an access policy, and `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 41) belong to the role, permission and delegation stories.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 41 (events IN: none), and the edition is a synchronous upload that needs no subscription.

#### 12.5 Workflows and activities

None. No workflow and no activity is part of this contract; the edition is one synchronous command with one downstream call, and the `rwb-access` queue carries other stories' work only.

#### 12.6 Schedules

None. Both operations are request-driven.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code the authority answer is read for |
| `permission` | P4 (rwb_access) | The Rules and parameters letters of a role and the matrix version |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The entry the document declares for an accepted edition |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in rwb_access | The outbox row of the record, the stored answer of the upload and no inbox row (DP-09) |

No table of another service is named as this contract's (DP-01): `lov_value`, `reference_version` and `reference_row` are P3 rwb_case's, `treatment` is S2 rwb_treatment's, `decision_log_entry` and the rule rows are P7 rwb_decision's, and the load, its state and the version in force arrive in contract answers.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case reference-load WireMock | `POST /admin/reference-loads` answering load "LOAD-2027-000118" in state `LOADED` for MORTGAGE and version "MORT-POL-2027.01"; a refusal of the version; a 503 and a timeout; `GET /admin/reference-loads/{loadId}` answering the same load and its state | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with product group MORTGAGE and version "MORT-POL-2026.04" in force from 1 July 2026, and the groups of LOV-PRODUCT with the version in force | App story, contract tests |
| authorise fake | `POST /authorise` with a granted answer for RW-COE holding the C and R letters in Rules and parameters, and a refused answer with MSG-P4-002 for RW-PRODHEAD with R only | App story, contract tests |
| decision-record fake | The append, the hash-link check, the chain read of the editions of a product group and a forced failure | App story, contract tests |
| gateway-bff fake | The administration route that uploads the workbook and reads the editions, with the empty, checked, refused, loaded and versions states | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The upload and the read provided; the authorise, parameters and two reference-load operations consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | 1 input | The workbook of the upload, passed through to the owner and not stored |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-productpolicy-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the `ProductPolicyEdition` and `ProductPolicyEditions` schemas with their examples, the multipart and query contract in the contract README, the state set of LOV-VERSION-STATUS, the paging-free read shape, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The reference-load call into `rwb-case` is a consumed operation whose contract is not in the metadata list, and it is built against that contract and its fake (GAP-0870; ASM-1577).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The upload with the multipart part, the four query parameters, the required `Idempotency-Key` and the named constants of the table code and the sheets.
3. The two schemas of section 11 and the state set of LOV-VERSION-STATUS, with the no-value rule stated in the description of the edition.
4. The consumed operations with their owners, the one-hop rule, the 2 s client budget and the note on the flagged load read.
5. The error envelope and the message-ID mapping for 400, 401, 403, 409, 422 and 503, with the texts copied unchanged from the legacy story where the message already existed.
6. The five fakes and the stub fixtures of section 12.8, all synthetic and all without a value of the edition.
7. The six contract tests, including a fake that carries a band or a personal field and must fail the build.
8. Baseline tag and the consumer sign-off note from the app story, the administration route and the harness.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; which product groups are editable is reference data and which version is in force is a parameter row, so the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8009-APP | The two provided operations, the two schemas, the state set, the part and field names of the 422 and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and the administration screen) | The two operations as the route uploads the workbook and reads the editions |
| The integration harness of the wave 4 access journey | The edition fields, the load id, the state and the fakes, as the evidence it records |

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path and carry no value and no personal data, and the app story, the administration route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the C letter posts an edition, or without the R letter reads the editions | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty, the product group is not in its list, a part of the workbook is missing, `validFrom` precedes the version in force, or the key is replayed with another file | Enter {field}. |
| MSG-GEN-004 | The parameters owner refuses the version | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. The 400 for a malformed multipart body is a response of the same envelope and carries no business text of its own, and the 422 names the part of the workbook or the field in its body so the screen can point at it.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| The administration screen of the edition (not named in the sources) | Empty | An empty `editions[]` and an `inForce` with the version in force from the parameters contract; no error |
| The administration screen of the edition | Checked | The upload control and the four fields of the request, with `validFrom` compared with the version in force |
| The administration screen of the edition | Refused before the owner | The 422 of the envelope with the missing part or the field |
| The administration screen of the edition | Refused by the owner | The 409 of the envelope with MSG-GEN-004 |
| The administration screen of the edition | Loaded | The 201 with the edition id, the policy version, the load id, `LOADED` and the valid-from date |
| The administration screen of the edition | Versions | `editions[]` with the policy version, the load id, the state and the valid-from date, and `inForce` at the top |
| The administration screen of the edition | Refused caller | The 403 of the envelope with MSG-P4-002 and no list |

No screen is named for this contract in the source documents (DOR-RWB-P4-E8009-CON-10): the contract declares no screen of its own, and the rows above are carried from the legacy story.

The screens are served by the gateway-bff composite route (DP-19), which calls the two operations and the parameters read in parallel, one hop each, and merges the answers. The route specification, the screen field list and the identification of the screen belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the product policy side of the merge only, and it declares no band, no floor and no range for the route to render.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-009-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the C and R letters and the six error responses are present; no foreign operation is provided |
| TC-E8-009-CON-02 | AC2 | Contract | The two schemas, the multipart part, the four query parameters, the named table code and the three sheets, and a check that no value of the edition is declared |
| TC-E8-009-CON-03 | AC3 | Contract | The state set of LOV-VERSION-STATUS, `LOADED` on the post, the owner's state on the read, and a check that an eighth state fails the build |
| TC-E8-009-CON-04 | AC4 | Contract | A 400, 401, 403, 409, 422 and 503 response each carry one problem envelope with a valid message ID and the part or field of a 422 |
| TC-E8-009-CON-05 | AC5 | Contract | Four consumed operations with their owners P4 and P3, one hop and the 2 s budget, the flagged load read and its note; none declared as provided |
| TC-E8-009-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; a fake carrying a band or a personal field fails the build |
| TC-E8-009-CON-07 | AC7 | Contract | Each table of section 12.7 is owned by P4 rwb_access; a table of another service named as this contract's fails the build (ASM-3438 boundary) |
| TC-E8-009-CON-08 | AC8 | Contract | A schema change that adds a field validates within version 1; a removed, renamed or retyped field or a removed state fails the build as a new major version |
| TC-E8-009-CON-09 | AC9 | Contract | BR1 to BR10 each name a criterion of section 7 and that criterion has a row in section 16; a rule without one fails the build |
| TC-E8-009-CON-10 | AC10 | Contract | A read of a product group with no edition answers 404 with one problem envelope and declares no edition |

### 17. Guardrails

- No business value in the contract: the product groups and the version in force stay reference data and parameter rows behind the document, and the document declares no band, floor, range, amount, percentage or boundary at all.
- No personal data in a schema, an example or a fake: user references, role codes, version labels, load ids, dates and times only (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the parameters, the reference data, the treatment and the ledger are consumed or absent, never named as this service's (DP-01, BR3).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- Every example in the document and every fixture of a fake is synthetic; no production policy workbook or extract is copied into a schema or a fake.
- The state set is the owner's and the document adds no state of its own (BR5): a state the owner does not report can never appear in the answer.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- The missing P3 reference-load contract is written down in the contract rather than silently assumed (GAP-0870; ASM-1577), so the review sees the dependency the metadata does not carry.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S2-004 | Settlement terms inside a rule-set range, anything outside needs approval | The edition as a versioned file handed to its owner, the valid-from date, and the state the owner reports | TC-E8-009-CON-02, TC-E8-009-CON-03 |
| REQ-DRI-010 | A parameter catalog holds every threshold, limit and name, versioned | The parameters read and the version in force as consumed operations; no value declared in the document | TC-E8-009-CON-02, TC-E8-009-CON-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation | The two operations as the administration route consumes them, with the C and R letters declared | TC-E8-009-CON-01, TC-E8-009-CON-05 |
| R-UNI-39 | A decision log entry that cannot be written blocks the action | The `rwb.decision.DecisionRecorded.v1` declaration and the 503 with MSG-P7-003 | TC-E8-009-CON-04, TC-E8-009-CON-06 |

| Legacy reference | Where it is kept |
|---|---|
| The legacy story statement, the bands, the floors and the ranges of a product | Section 1, section 12.1 |
| The legacy endpoints `/admin/rule-versions` and its approve | Not carried: P7 `rwb-decision` under ASM-0040 and RWB-P4-AD011-APP |
| The legacy permission table (C: RW-COE; A: RW-RISK) and the FSD primary role | Sections 7 and 10, with the conflict of GAP-0870 and ASM-1578 |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P7-003 | Section 14 and the exception paths of section 5 |
| The legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried as a screen the sources do not name for this feature |

### 19. Out of scope

- The implementation of the upload and the read (RWB-P4-E8009-APP).
- The bands, the floors, the ranges, their rows, their versioning and their approval: `rwb-case` (P3) under ASM-0071 and ASM-0041, and RWB-P4-AD009-APP and RWB-P4-AD010-APP on the console path.
- The rule-version endpoints the legacy story carried, the rule package registry and SCR-39: P7 `rwb-decision` under ASM-0040, and RWB-P4-AD011-APP and RWB-P4-AD012-APP.
- The treatment entity and the treatment policy of a case: S2 `rwb-treatment`.
- The delegation limits and SCR-41: RWB-P4-E1038-APP.
- The administration screen itself and its composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The central ledger, the query API over `rwb_decision` and the chain verification (P7 rwb-decision).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The cross-service journey harness and its evidence; no `-ITG` story is split from this legacy key here.
