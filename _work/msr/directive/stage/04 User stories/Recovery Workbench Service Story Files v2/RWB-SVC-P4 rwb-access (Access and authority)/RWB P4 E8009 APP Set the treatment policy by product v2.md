# RWB-P4-E8009-APP Set the treatment policy by product

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | To be sized by the squad at refinement (DOR-RWB-P4-E8009-APP-16) |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E8009-APP-23) |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BC |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8009-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-009 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 13 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **product head (RW-PRODHEAD; Mortgage, HP, SSME)**, I want **one treatment policy edition for my product uploaded as a workbook carrying the bands, the floors and the ranges, checked for its parts and its date, handed unchanged to the owner of the parameters and recorded with the load reference the owner answers**, so that **the treatment policy of a product changes without a code release, an edition cannot be put in by a caller without the Rules and parameters right, an edition that is incomplete or dated before the version in force is refused before it reaches the owner, and every accepted edition can be traced to the load that holds it**.

Inside `rwb-access` this is the treatment policy edition capability of the legacy story RWB-E8-009:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **The split, stated plainly.** Under the R-PREC default ruling the parameters and the reference data are P3 `rwb-case`'s (ASM-0071) and the reference-load operations are P3's too (ASM-0041). `lov_value`, `reference_version` and `reference_row` stay with that service, and so do the bands, the floors and the ranges themselves: this story never stores, parses into a table, compares or answers a single value of the edition. What it owns is the **door and the edition record**: the operation the administration screen calls, the authority check behind it, the shape check on the workbook and its date, the hand-over of the file to the owner, and the decision-record entry of every accepted edition.
- **Provided by this story**, under the access base of DP-13: `POST /api/recovery/access/v1/admin/product-policies` — `multipart/form-data` with the part `file` (the edition workbook: one sheet each for the bands, the floors and the ranges), the query `productGroup`, `policyVersion`, `validFrom` and `reason`, and the header `Idempotency-Key`; it authorises the Rules and parameters C letter, checks that the three row kinds are present and that the dates are ordered, hands the file **unchanged** to `POST /api/recovery/case/v1/admin/reference-loads` of `rwb-case` with the table code `product_policy` and `validFrom`, appends one decision-record entry with the returned `loadId`, the `productGroup` and the `policyVersion`, and answers 201 `editionId`, `productGroup`, `policyVersion`, `loadId`, `state` `LOADED` and `validFrom`. And `GET /api/recovery/access/v1/admin/product-policies/{productGroup}` — the editions of the product with the one in force, on the Rules and parameters R letter, reading the version in force through the parameters contract and the load state through the owner, and interpreting no value.
- **Consumed:** `POST /api/recovery/access/v1/authorise` (own service), `GET /api/recovery/case/v1/admin/parameters` (DP-06, the version in force of the product group), `POST /api/recovery/case/v1/admin/reference-loads` (the load itself), and `GET /api/recovery/case/v1/admin/reference-loads/{loadId}` (the state of a load, named as consumed and flagged by this story). One hop, 2 s timeout, a breaker per downstream.
- **Recorded, not stored:** an accepted edition appends one decision-record entry of the DP-03 library carrying the `editionId`, the `productGroup`, the `policyVersion`, the `loadId` read back from the owner, the `validFrom`, the version in force at the time and the caller reference — and no value of the edition and no personal data.
- **Not in this story:** the list version ingest of this service (RWB-P4-AD009-APP) and the approval of a load (RWB-P4-AD010-APP); the `lov_value`, `reference_version` and `reference_row` rows and the reference-load paths themselves (P3 `rwb-case`); the treatment entity (S2 `rwb-treatment`); the rule rows and the central decision ledger (P7 `rwb-decision`); and the treatment policy of a case, which is decided by the treatment service and not by this administration story.
- The administration screen that carries the edition is served through the gateway-bff composite route of DP-19; this story renders no screen of its own. Which screen carries it is Not specified in the source documents (GAP-0870; ASM-1577): the legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority, and the edition sits on neither of them.

### 2. Business rationale

The treatment policy of a product — the bands a case may be settled in, the floors a proposal may not go under, the ranges an officer may work inside — is the number set that decides whether a settlement is inside or outside the range the product allows, and a proposal outside it needs an approval (REQ-S2-004). Today that number set lives in documents and in people's heads, so a change needs a code release or a manual check, and nothing can show afterwards which set was in force when a case was decided (FSD P4 v3 A2.20.1). The legacy story asked for the product head to set the bands, floors and ranges and for the result to be written to the decision log with the rule version; it carried the rule-version endpoints, which are a different capability and are `rwb-decision`'s now.

In the target, a parameter catalog holds every threshold, limit and name, versioned and changed without a code release (REQ-DRI-010), and the parameters and reference data of the estate are `rwb-case`'s under the R-PREC default ruling. That leaves `rwb-access` with exactly one defensible job in this feature, and it is the job the administration screens need: be the door. The product head works the screen, the edition is checked for what an edition must have and for its date before it is worth the owner's time, the file goes to the owner unchanged so that only one service ever holds the values, and the access service records which edition it let in and which load holds it. That is what makes a policy change reviewable: one operation, one right, one record, one load reference, and no second copy of a versioned table in the access schema (DP-01).

The story serves REQ-S2-004 by making the range inside which settlement terms are negotiated a versioned row set loaded by its owner and recorded by the door, REQ-DRI-010 by keeping every threshold, limit and name in the parameter catalog rather than in this service, and REQ-ACA-013 by putting the edition on the administration screens for the product head and the security administrator. It supports the measure *rule and limit changes made without a code release*, target 100 percent (FSD P4 v3 A2.20.1), and it carries two universal rules: a version applies from its effective date (R-UNI-38) and no action proceeds unlogged (R-UNI-39).

The FSD makes the product head the primary role of the feature (FSD P4 v3 A2.20.3.3) and the TSD gives RW-PRODHEAD R only in Rules and parameters (TSD P4 v3 T6.1), while the legacy permission table gives the C letter to RW-COE and the A letter to RW-RISK. R-PREC puts the technical specification above the story master, so the product head proposes and the C letter stays RW-COE's. That reading is a conflict of the sources and is recorded as the gap of this key (GAP-0870; ASM-1578).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8009-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two operations, the `ProductPolicyEdition` and `ProductPolicyEditions` schemas, the state set of LOV-VERSION-STATUS, the error envelope and its message IDs, and the contract fakes. This story builds against it and changes no schema |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every accepted edition, hash-linked and written in the same transaction as the answer |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the version in force of a product group, read with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19), which serves the administration screen that uploads the workbook and reads the editions, one hop per call |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise operation and the refusal shape with MSG-P4-002 that every operation of this service uses; this story adds no path to it |
| The `rwb-case` reference-load contract and its fake | The two operations this story consumes: the load of the file with its table code and its valid-from date, and the read of a load and its state. It is not in this story's metadata contract-dependency list (GAP-0870; ASM-1577) |
| RWB-P4-AD009-APP and RWB-P4-AD010-APP (same service, other stories) | The list version ingest of this service and the approval of a load on the console path. This story neither replaces them nor depends on them: it is a second ingest, for another owner table, and the approval of the edition stays theirs |

Business preconditions carried from RWB-E8-009 and the P4 specifications:

- A product group is one value of LOV-PRODUCT: MORTGAGE, HIRE_PURCHASE, SSME or UNSECURED (TSD P4 v3 T3.2). It is reference data of `rwb-case` and is never a code list in this service.
- The edition workbook carries one sheet each for the bands, the floors and the ranges (RWB-E8-009 story statement, the three number sets of the feature). The sheet names, the header row and the column layout are Not specified in the source documents (GAP-0870; ASM-1577).
- The file is handed to the owner with the table code `product_policy` and `validFrom`. The table code is Not specified in the source documents (GAP-0870; ASM-1577); it is the name this story and its contract fix with the owner at review.
- The state names of a version are the values of LOV-VERSION-STATUS: LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (TSD P4 v3 T3.2 and T4).
- The rights in force are the ones of TSD P4 v3 T6.1: RW-COE holds CRUD in Rules and parameters, RW-RISK holds RA there, RW-PRODHEAD holds R there, and every other recovery role holds R or a dash. The legacy permission table that gives C to RW-COE and A to RW-RISK agrees on the two letters and disagrees on who is primary: the FSD names the product head (GAP-0870; ASM-1578).
- The version in force of a product group is a parameter row read through DP-06 with the version in force, and the edition is compared with its `valid_from` only; no band, floor or range is read by this service at all.

### 4. Flow

1. The product head opens the administration screen through the gateway-bff composite route of DP-19, picks the product group, picks the edition workbook, enters the policy version label, the valid-from date and a reason, and submits.
2. `POST /api/recovery/access/v1/admin/product-policies` arrives as `multipart/form-data` with the part `file`, the query parameters `productGroup`, `policyVersion`, `validFrom` and `reason`, and the header `Idempotency-Key`. The controller validates the query first: `productGroup`, `policyVersion` and `validFrom` are required, `validFrom` is an ISO date, and a missing or malformed one is 422 with MSG-GEN-001 naming the field; the file part is required and its absence is 422 naming `file`. Nothing is opened and no record is written when the query is refused.
3. The controller resolves the caller's role through the service's own `v_ace_iam_group` read and reads the `permission` row of that role in the capability area RULES_AND_PARAMETERS. A caller without the C letter is refused with 403 and MSG-P4-002, and the workbook is never opened, read or hashed, so a caller without the right cannot learn anything about a file (AC3).
4. The product group is checked against the groups the parameters contract answers at the version in force; no reference-data list is read, because this story's pattern list carries no DP-07 and its contract-dependency list no RWB-P3-E1043-CON, and the point is raised in the key's gap (GAP-0870; ASM-1577). A value that is not in that answer is 422 with MSG-GEN-001 naming `productGroup`, and the owner is not called.
5. `EditionShapeCheck` opens the workbook read-only and checks its shape, and only its shape: the three row kinds are present (the bands sheet, the floors sheet and the ranges sheet), each with its header row, and no cell is read as a business value beyond the row count and the presence of the header. A workbook that lacks one of the three parts is 422 with MSG-GEN-001 naming the missing part, and the owner is not called (AC4).
6. The date check: `validFrom` must not be earlier than the `valid_from` of the version in force of the same product group, read through DP-06. An edition dated before the version in force is 422 with MSG-GEN-001 naming `validFrom`, and the owner is not called (AC4). An edition dated after it is accepted; the gaps between versions are the owner's business and are not checked here.
7. Idempotency: the service looks up the `Idempotency-Key` and the digest of the file. A key already used with the same digest answers the edition it answered the first time with the same `editionId` and `loadId`, and hands nothing a second time to the owner. The same key with a different file is 422 with MSG-GEN-001 naming the key.
8. `ReferenceLoadClient` streams the file bytes unchanged to `POST /api/recovery/case/v1/admin/reference-loads` of `rwb-case`, with the table code `product_policy` and `validFrom`, one hop, a 2 s timeout and a breaker. This service writes no `lov_value`, `reference_version` or `reference_row` row and no row of its own for a band, a floor or a range: the bytes are passed through and are not stored locally (ASM-0071).
9. The owner answers the load with its `loadId` and its state. When the owner refuses the version, the answer to the caller is 409 with MSG-GEN-004, no edition is recorded and the version in force is unchanged (AC5). When the owner does not answer inside the 2 s budget or answers 5xx, the answer is 503 and nothing is recorded; the operator retries the same file with the same `Idempotency-Key`, which finds the owner's load and completes the record instead of loading a second time.
10. `EditionRecordWriter` appends one decision-record entry of the DP-03 library with the `editionId`, the `productGroup`, the `policyVersion`, the returned `loadId`, the `validFrom`, the version in force read in step 6 and the caller reference. The entry, the idempotency row and the answer commit in one local transaction. Where the entry cannot be written the transaction rolls back and the answer is withheld with 503 and MSG-P7-003, because an edition that is not recorded cannot be shown to have been let in (R-UNI-39; AC2).
11. The operation answers 201 with `editionId`, `productGroup`, `policyVersion`, `loadId`, `state` = `LOADED` and `validFrom`, and a `Location` header naming the edition read. The load waits for the owner's approval, which is not this story's.
12. `GET /api/recovery/access/v1/admin/product-policies/{productGroup}` answers the editions of the product on the Rules and parameters R letter: `editions[]` from the local chain (edition id, policy version, load id, state, valid from, recorded at), the one in force with its policy version and valid-from date read through the parameters contract, the chain name and the time of the answer. The state of a load is read through the owner's load read; no value of any edition is read, compared or answered.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `productGroup`, `policyVersion`, `validFrom` or the `file` part is missing | 422 naming the field or `file`; nothing is opened and nothing is recorded | MSG-GEN-001 | AC3 |
| X2 | The product group is not a value of LOV-PRODUCT | 422 naming `productGroup`; the owner is not called | MSG-GEN-001 | AC3 |
| X3 | One of the three parts of the workbook is missing | 422 naming the missing part (the bands, the floors or the ranges sheet); the owner is not called | MSG-GEN-001 | AC4 |
| X4 | `validFrom` is earlier than the `valid_from` of the version in force | 422 naming `validFrom`; the owner is not called | MSG-GEN-001 | AC4 |
| X5 | The caller holds no C letter in Rules and parameters | 403; the workbook is not opened, read or hashed and no entry is written | MSG-P4-002 | AC3 |
| X6 | The caller's session has ended | 401, no read of the file and no entry | MSG-P4-001 | AC3 |
| X7 | The parameters owner refuses the version | 409 with nothing recorded; the version in force is unchanged | MSG-GEN-004 | AC5 |
| X8 | The parameters owner does not answer inside the 2 s budget or answers 5xx | 503 with nothing recorded; a retry of the same file with the same key is safe | None (RFC 9457 problem with the trace identifier) | AC5 |
| X9 | The decision record cannot be written | The local transaction rolls back and the answer is withheld with 503; nothing is in force and no edition is answered | MSG-P7-003 | AC2 |
| X10 | A replayed request with a different file under the same `Idempotency-Key` | 422 naming the key; the first answer is not returned and nothing is handed again to the owner | MSG-GEN-001 | AC5 |
| X11 | The product head holds R only and submits an edition | 403 with MSG-P4-002; the product head proposes, and the edition is submitted by a holder of the C letter | MSG-P4-002 | AC3 |
| X12 | The read asks for a product group that is not a list value | 422 naming `productGroup`; no list and no chain is read | MSG-GEN-001 | AC5 |

No exception path of this story writes a band, a floor or a range: the values are the owner's, the file is passed through and the state names are the owner's. The approval of the load is not this story's either.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the contract of RWB-P4-E8009-CON and the fakes of the authorise, parameters, decision-record and reference-load contracts; no other story of the lane has to exist in the environment |
| Negotiable | The sheet names, the table code and the exact wording of the check messages are fixed with the owner at contract review; the two operations, the C and R letters, the three parts and the refuse-before-the-owner rule are fixed by the feature and the matrix |
| Valuable | One door and one record replace a number set held in documents, so a policy change is reviewable and the values keep one owner |
| Estimable | Two operations, one shape check, one date check, one idempotency store, one owner client, one record writer and one product-group read |
| Small | Fits two weeks with its tests; there is no table of its own, no workflow, no schedule, no event of its own and no approval in it |
| Testable | Each criterion has a component or contract test against the fakes, and the refusal and record rules are asserted on the answer and on the chain |

### 7. Acceptance criteria

```gherkin
Feature: Set the treatment policy by product

  Background:
    Given the environment is SIT
    Given test user "U-4301" holds RW-COE with the C letter in Rules and parameters
    Given test user "U-4302" holds RW-PRODHEAD with the R letter only in Rules and parameters
    Given the parameters contract answers product group "MORTGAGE" with version "MORT-POL-2026.04" in force from 1 July 2026

  Scenario: AC1 Set the treatment policy by product (legacy RWB-E8-009 AC1)
    Given the rwb-case contract mock returns load "LOAD-2027-000118" in state "LOADED" for product group "MORTGAGE" and version "MORT-POL-2027.01"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the product head set the bands, floors and ranges for their product
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-009 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller without the Rules and parameters C letter is refused and no file is read (new, D-RCV-60)
    Given test user "U-4302" holds RW-PRODHEAD with the R letter only
    When "U-4302" posts the MORTGAGE edition to POST /api/recovery/access/v1/admin/product-policies with policyVersion "MORT-POL-2027.01", validFrom "2027-01-01" and Idempotency-Key "k-901"
    Then the response is 403 with message MSG-P4-002 and the workbook is not opened
    Then the rwb-case reference-load operation is not called and no edition is recorded

  Scenario: AC4 An edition with a part missing, or a date before the version in force, is refused with its part or its field (new, D-RCV-60)
    Given a workbook for MORTGAGE that carries the bands and the ranges and carries no floors sheet
    When "U-4301" posts it to POST /api/recovery/access/v1/admin/product-policies with policyVersion "MORT-POL-2027.01" and validFrom "2027-01-01"
    Then the response is 422 with message MSG-GEN-001 naming the missing floors part
    Then the rwb-case reference-load operation is not called
    Given a workbook that carries the bands, the floors and the ranges with validFrom "2026-06-01", before the version in force of 1 July 2026
    When "U-4301" posts it with policyVersion "MORT-POL-2027.01"
    Then the response is 422 with message MSG-GEN-001 naming "validFrom"
    Then the rwb-case reference-load operation is not called and no edition is recorded

  Scenario: AC5 A version the owner refuses is answered 409 with nothing recorded, and an accepted edition is answered and recorded (new, D-RCV-60)
    Given the rwb-case contract mock refuses the load of version "MORT-POL-2027.01" for product group "MORTGAGE"
    When "U-4301" posts the edition with Idempotency-Key "k-902"
    Then the response is 409 with message MSG-GEN-004 and the version in force stays "MORT-POL-2026.04"
    Then no edition is recorded and the chain holds no entry for "k-902"
    Given the rwb-case contract mock returns load "LOAD-2027-000118" in state "LOADED" for product group "MORTGAGE" and version "MORT-POL-2027.01"
    When "U-4301" posts the same edition with Idempotency-Key "k-901"
    Then the response is 201 with an edition id, loadId "LOAD-2027-000118", state "LOADED" and validFrom "2027-01-01"
    Then exactly one decision-record entry is appended carrying productGroup "MORTGAGE", policyVersion "MORT-POL-2027.01" and loadId "LOAD-2027-000118"
    Then the entry carries no band, no floor, no range and no personal field

  Scenario: AC6 The edition is stored by rwb-case only and no business value is coded in this service (new, D-RCV-60)
    When "U-4301" posts an accepted edition of the MORTGAGE workbook
    Then no lov_value, reference_version or reference_row row is written by this service
    Then the product group and the version in force are read through the parameters contract and no such value is a constant in code

  Scenario: AC7 A request with no authenticated session is answered 401 and an unrecorded edition id is answered 404 (new, D-RCV-60)
    Given no authenticated session is held by the caller
    When the caller posts to POST /api/recovery/access/v1/admin/product-policies with policyVersion "MORT-POL-2027.01" and validFrom "2027-01-01"
    Then the response is 401 and no file is read
    When "U-4301" asks for an edition id that is not recorded at Not specified in the source documents (NEWAC-RWB-P4-E8009-APP-AC7)
    Then the response is 404

  Scenario: AC8 A call to the rwb-case reference-load operation that fails or does not answer records nothing (new, D-RCV-60)
    Given the rwb-case contract mock does not answer the load of version "MORT-POL-2027.01" for product group "MORTGAGE"
    When "U-4301" posts the edition
    Then the response is Not specified in the source documents (NEWAC-RWB-P4-E8009-APP-AC8)
    Then no edition is recorded, no decision-record entry is appended and the version in force stays "MORT-POL-2026.04"
```

AC1 and AC2 are the legacy criteria of RWB-E8-009, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the reference-load mock, so the edition is provable while the parameters owner is still a fake. AC3 to AC8 are new under D-RCV-60 and test only what this story adds.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A treatment policy edition is a workbook with one sheet each for the bands, the floors and the ranges, uploaded with a product group, a policy version label, a valid-from date and a reason | RWB-E8-009 story; FSD P4 v3 A2.20.2; GAP-0870; ASM-1577 |
| BR2 | The parameters and the reference data are `rwb-case`'s, and so are the bands, the floors and the ranges: this service writes no `lov_value`, `reference_version` or `reference_row` row and keeps no copy of a value | REQ-DRI-010; ASM-0071; DP-01 |
| BR3 | The file is handed to the owner unchanged, with the table code `product_policy` and `validFrom`, and this service reads no value out of it beyond the presence of its three parts | ASM-0041; GAP-0870; ASM-1577 |
| BR4 | Posting an edition requires the C letter in Rules and parameters and reading the editions requires the R letter; a role without the letter is refused with MSG-P4-002 and with no read of the file | TSD P4 v3 T6.1; REQ-ACA-013; BR-P4-020 |
| BR5 | The product head is the primary role of the feature and holds R only, so it proposes an edition; the C letter is RW-COE's and the A letter RW-RISK's, and R-PREC puts the technical specification above the story master | FSD P4 v3 A2.20.3.3; TSD P4 v3 T6.1; Template and Rules §R3; GAP-0870; ASM-1578 |
| BR6 | An edition is refused before the owner is called when a part of the workbook is missing or when its `validFrom` precedes the version in force; the refusal names the part or the field | AC4; FSD P4 v3 A2.20.3.1 VR-P4-020-1; ASM-1577 |
| BR7 | A version the parameters owner refuses is answered 409 with MSG-GEN-004, nothing is recorded and the version in force is unchanged | AC5; TSD P4 v3 T4 |
| BR8 | An accepted edition appends exactly one decision-record entry of the DP-03 library with the edition id, the product group, the policy version, the load id, the valid-from date, the version in force and the caller reference, and the entry carries no value of the edition and no personal data | R-UNI-39; DP-03; GAP-0870; ASM-1579 |
| BR9 | The record, the idempotency row and the answer commit in one local transaction; where the record cannot be written the answer is withheld with MSG-P7-003 and nothing is in force | R-UNI-39; FSD P4 v3 A2.20.4.3 AC-EXC-P4-020-02 |
| BR10 | A replay of the same file with the same `Idempotency-Key` answers the first edition and hands nothing a second time to the owner; the same key with a different file is refused | R-UNI-40; Architecture v5 slide 11 |
| BR11 | The state names are the values of LOV-VERSION-STATUS and the version in force is read through the parameters contract; no state name and no policy version label is a constant in code | TSD P4 v3 T3.2 and T4; REQ-DRI-010 |
| BR12 | No value that a business person may change is written in code: the product groups, the version in force and the dates are rows and reference data with a version | FSD P4 v3 BR-P4-020; wired by DP-06 |

Target-service statements that make the rules hold in `rwb-access`:

- BR2 and BR3 are the absence of a repository for a band, a floor or a range in this service, and the pass-through of the received bytes to the owner's contract: the file is never parsed into a row, and the record names the load rather than the file.
- BR4 is the authorise call of step 3 before the file is opened; the refusal is answered before a byte of the upload is read, so a caller without the C letter cannot probe a workbook.
- BR5 is a reading of the matrix and not a code path: the letters are `permission` rows, the product head holds R, and a role that needs the C letter gets a row and not a release.
- BR6 is `EditionShapeCheck` over the workbook and one comparison of `validFrom` with the `valid_from` of the version in force. The check is about presence and order only: whether a band, a floor or a range is well formed is the owner's check, and this story does not duplicate it.
- BR8 is the record appender of DP-03 inside the transaction that produces the answer, with the `loadId` read from the owner's answer.
- BR9 is that same transaction: a failed append rolls back the idempotency row and withholds the answer.
- BR10 is the idempotency row of the library keyed on the key and the file digest.
- BR11 and BR12 are reads through the parameters and reference-data clients at request time with the version in force; a new product group or a new version is data.

Which of the three parts counts as the "bands", the "floors" and the "ranges" part, and how each is recognised in the workbook, is Not specified in the source documents (GAP-0870; ASM-1577): this story requires one sheet per part with its header row and names the missing part in the refusal, and the review fixes the sheet names with the owner before the endpoint is frozen.

### 9. State transitions

This service holds no band, floor, range or version state of its own. The states below are the lifecycle of a load in `rwb-case`, which this story starts in `LOADED` or refuses before the owner is called; the approval and the rollback are other stories' and the owner's.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | An edition is posted and every check passes | The owner stores the rows and versions them | `LOADED` |
| (none) | An edition is posted and a part or a date check fails | 422 naming the part or the field; nothing reaches the owner | No load is created |
| (none) | An edition is posted and the owner refuses the version | 409 with MSG-GEN-004; nothing recorded | No load is created |
| `LOADED` | The load owner approves the version | A second person with the A letter, on the reference-load path of the console (RWB-P4-AD010-APP) | `APPROVED` |
| `APPROVED` | The valid-from date is reached | R-UNI-38: decisions from that date use the new version | `IN_FORCE` |
| `IN_FORCE` | A newer edition reaches its valid-from date | R-UNI-38 | `SUPERSEDED` |
| `IN_FORCE` | A rollback is recorded | The owner's rollback on the reference-load path | `ROLLED_BACK` |
| Any | The version is refused by its owner's own checks | None: a refusal is terminal and the next file is a new edition | `REFUSED` |

| Command | Condition | Outcome |
|---|---|---|
| Post an edition | C letter in Rules and parameters, the three parts present, the dates ordered, the owner answers `LOADED` | 201 with the load id and `LOADED`, one record entry, no value interpreted |
| Post an edition | No C letter | 403 MSG-P4-002, the file is not opened, no entry |
| Post an edition | A part is missing or `validFrom` precedes the version in force | 422 MSG-GEN-001 with the part or the field, no owner call, no entry |
| Post an edition | The owner refuses the version | 409 MSG-GEN-004, nothing recorded, the version in force unchanged |
| Post an edition | The owner does not answer | 503, nothing recorded, the same key retries safely |
| Post an edition | The record cannot be written | 503 MSG-P7-003, no answer, nothing in force |
| Read the editions | R letter in Rules and parameters, a product group of LOV-PRODUCT | 200 with the editions, the one in force and the chain |
| Read the editions | A product group that is not a list value | 422 MSG-GEN-001 naming `productGroup` |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | An accepted edition | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| Append-only local chain | A refusal before the owner, or a refusal by the owner | No entry: there was no edition to record |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE Center of excellence analyst | Holds CRUD in Rules and parameters (TSD P4 v3 T6.1) and therefore the C letter: it submits an edition for the product head and reads the editions; the legacy permission table names it for C too |
| Product head (Mortgage, HP, SSME), RW-PRODHEAD | The primary role of the feature (FSD P4 v3 A2.20.3.3). It holds R only in Rules and parameters, so it opens the screen, prepares the edition and proposes it; it submits nothing itself and is refused with MSG-P4-002 (GAP-0870; ASM-1578) |
| RW-RISK Risk and model risk officer | Holds RA in Rules and parameters (TSD P4 v3 T6.1) and therefore the A letter: it does not post an edition and does not read a load's approval here; the A letter decides a load on the console path, which is RWB-P4-AD010-APP's |
| RW-AUDIT Internal audit | Holds R in Rules and parameters: it reads the editions through the read and the entries through the decision record; it calls no write operation of this story |
| RW-SECADM Security administrator | Holds CRUDA in Platform administration and R in Rules and parameters: it reaches the administration screens as the reader of REQ-ACA-013 and reads the editions; it posts none |
| Every other recovery role | Holds R in Rules and parameters: it reads the editions and posts nothing |
| `rwb-access` itself | Reads `role` and `permission` in its own schema and the group of the caller through its own `v_ace_iam_group` ACE view; it writes no value of the edition and no personal data |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each; it holds no right of its own |
| `rwb-case` (P3) | Owns the parameters, the reference data and the load: this story calls its parameters read and its reference-load operations and owns none of them |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002, and the unauthenticated shape is 401 with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the Rules and parameters letters of the caller |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the edition entry: `decision_code` DF-DEC-003, `case_id` DF-DEC-002 empty for an administrative act, `inputs_ref` DF-DEC-008 with the edition id, the product group, the policy version, the load id, the valid-from date, the version in force and the caller reference, `actions` DF-DEC-014, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and its `DecisionRecorded` message | Write |
| (idempotency) | `idempotency_key` in `rwb_access` | the key, the file digest and the stored answer | Write and read |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | none of the edition's values: the list rows are the owner's | Not read from the schema and not read as a list; the product groups come from the parameters answer (GAP-0870; ASM-1577) |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb_case` | the load, its version, its state and the version in force | Read through the reference-load contract, never from a table |
| DF-TRT-001 to DF-TRT-014 | `treatment` of `rwb_treatment` (S2) | none: the treatment of a case is the treatment service's | Not read and not written |

No row of `treatment`, `decision_log_entry` or `rule_row` is read or written: the legacy data table of RWB-E8-009 named all three, and in the target the treatment is S2 `rwb-treatment`'s (Architecture v5 slide 41), the central decision ledger is P7 `rwb-decision`'s and the rule rows are its rule catalog's. The `role` row is read because the matrix is this service's data. No foreign key crosses a schema (DP-01). The field-level placement of the edition facts inside `inputs_ref` is fixed by the entry of the DP-03 library and by the schema of RWB-P4-E8009-CON; this story writes it and interprets no value of the edition. Field IDs are those of the Logical Data Model and Data Dictionary v9.

The record code of an edition — the value that tells the chain this entry is a treatment policy edition — is Not specified in the source documents (GAP-0870; ASM-1579): the story uses the library's administrative-change code and the contract review fixes the value with the ledger owner.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/product-policies` | P4 `rwb-access` | `multipart/form-data` part `file` (the edition workbook: the bands sheet, the floors sheet and the ranges sheet); query `productGroup`, `policyVersion`, `validFrom` (ISO date), `reason`; header `Idempotency-Key` | 201 `editionId`, `productGroup`, `policyVersion`, `loadId`, `state` (`LOADED`), `validFrom`; `Location` naming the edition read | 400 malformed multipart; 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004, the owner refused the version); 422 (MSG-GEN-001, naming the part or the field); 503 (MSG-P7-003, or the owner unavailable) | Rules and parameters C | `Idempotency-Key` required; a repeat with the same digest answers the first edition |
| GET | `/api/recovery/access/v1/admin/product-policies/{productGroup}` | P4 `rwb-access` | Path `productGroup`, a value of LOV-PRODUCT | `ProductPolicyEditions`: `productGroup`, `editions[]` (`editionId`, `policyVersion`, `loadId`, `state`, `validFrom`, `recordedAt`), `inForce` (`policyVersion`, `validFrom`), `chain`, `recordedAt` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001, naming `productGroup`); 503 (the owner unavailable) | Rules and parameters R | Not applicable, read only; no Idempotency-Key |

The two operations sit under the base `/api/recovery/access/v1` of DP-13. The TSD P4 v3 names the capability the legacy story wanted as API-P4-005 `POST /admin/reference-loads` with the request fields `file`, `table` and `validFrom` (T-A.2), and under the R-PREC default ruling that path and its rows are P3 `rwb-case`'s (ASM-0041); this service therefore keeps the console door under its own base and calls the owner operation of 12.2. The table code this story hands over is `product_policy`, and it is Not specified in the source documents (GAP-0870; ASM-1577): the review fixes it with the owner and with the reference data it names. The P3 reference-load contract is not a declared dependency of this story: the call is built against that contract and its fake, and the missing dependency is raised at D1 rather than added to the contract-dependencies row (GAP-0870).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own) | The Rules and parameters C and R answer behind the two operations, cached for the request; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The version in force of the product group, its `valid_from` and its policy version label, with the version in force (DP-06) |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 `rwb-case` | The load: multipart `file`, `table` (`product_policy`) and `validFrom`; the owner stores and versions the rows and answers the load id and its state |
| GET | `/api/recovery/case/v1/admin/reference-loads/{loadId}` | P3 `rwb-case` | The state of a load for the read of the editions. The TSD P4 v3 appendix T-A has the load and its approve, verify and rollback but no load read, so this operation is named as consumed and flagged: Not specified in the source documents (GAP-0870; ASM-1577) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the answers are cached for the request. The reference-load contract is not in this story's metadata contract-dependency list, and the story builds against that contract and its fake with the missing dependency raised at D1 (GAP-0870; ASM-1577). No operation of `rwb-decision`, `rwb-treatment` or `rwb-document` is called.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of an accepted edition: `editionId`, `productGroup`, `policyVersion`, `loadId`, `validFrom`, the version in force and the caller reference |

CloudEvents 1.0 envelope; the payload carries references, codes, versions and times, and no band, no floor, no range and no personal field. This story publishes no `rwb.access.<Event>.v1` message: a treatment policy version is not an access policy, and the two event types of the service — `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 41) — belong to the role, permission and delegation stories.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 41 (events IN: none), and the edition is a synchronous upload that needs no subscription. The version in force is read through the parameters contract when the answer needs it, not from an event.

#### 12.5 Workflows and activities

None. The edition is one synchronous command with one downstream call; it starts no workflow, signals none, registers no activity on the `rwb-access` queue and holds no state between requests beyond the record and the idempotency row.

#### 12.6 Schedules

None. The edition and the read are request-driven. The six-monthly access review list (JOB-18) and the delegation-of-authority load are Schedules of `rwb-access` and belong to other stories.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role and the class of the caller |
| `permission` | P4 (`rwb_access`) | Read only: the Rules and parameters letters of that role |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: one entry per accepted edition; read: the editions of the read |
| `outbox_event` | PLT library, created in `rwb_access` | Write: the outbox row of the record |
| `idempotency_key` | PLT library, created in `rwb_access` | Write and read: the key, the file digest and the stored answer |
| `processed_event` | PLT library, created in `rwb_access` | None: no event is consumed (DP-09) |
| `lov_value`, `reference_version`, `reference_row` | P3 (`rwb_case`) | Not read from the schema and not written: reference data of P3 under ASM-0071, reached through the reference-load contract only; no reference-data list is read, because this story's pattern list carries no DP-07 (GAP-0870; ASM-1577) |
| `treatment` | S2 (`rwb_treatment`) | Not read and not written: the treatment of a case is the treatment service's |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's |

This service creates no table for a band, a floor, a range or an edition: the values are the owner's and the edition is a record in the local chain. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case reference-load WireMock | the P3 reference-load contract (GAP-0870; ASM-1577) | `POST /admin/reference-loads` answering load "LOAD-2027-000118" in state `LOADED` for MORTGAGE and version "MORT-POL-2027.01"; a refusal of the version for the 409 of AC5; a 503 and a timeout for X8; `GET /admin/reference-loads/{loadId}` answering the same load and its state |
| parameters fake | RWB-PLT-E1042-CON, RWB-P3-E1042-CON | Product group MORTGAGE with version "MORT-POL-2026.04" in force from 1 July 2026, and the product groups of LOV-PRODUCT with the version in force |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | Granted for RW-COE with the C and R letters in Rules and parameters; refused with MSG-P4-002 for RW-PRODHEAD with R only and for RW-CASEOWN with R only |
| decision-record fake | RWB-PLT-E1027-CON | The append, the hash-link check, the chain read of the editions of a product group and the forced failure of AC2 |
| gateway-bff fake | RWB-PLT-N001-CON | The administration route that uploads the workbook and reads the editions, with the empty, loaded, refused and versions states |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2; consumed 4 | Base `/api/recovery/access/v1`; the authorise, parameters and two reference-load operations consumed; one hop, 2 s timeout, breaker |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision.DecisionRecorded.v1` through the DP-03 library; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | No workflow and no Schedule in this story |
| File | 1 input, 0 output | One `multipart/form-data` workbook per edition, passed through to the owner and not stored locally |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/productpolicy`, Java package `th.co.scb.ace.workbench.recovery.access.productpolicy`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process write of the policy number set against the monolith schema (DP-01 and DP-07: the values are the owner's, behind its own contract, and this service keeps none of them) and the ace-web screen that called the in-process method (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. The reference-load call into `rwb-case` is a consumed operation whose contract is not in the metadata list: it is built against that contract and its fake, and the missing dependency is the gap of this key (GAP-0870; ASM-1577).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ProductPolicyController` | Controller | The two operations: query validation, the `Idempotency-Key`, the multipart part, the RFC 9457 problem responses and the `messageId` on every refusal |
| `PermissionReader` | Service | The caller's `role` and `permission` rows in `rwb_access` and the Rules and parameters letters |
| `ProductGroupReader` | Service | The product groups and the version in force of a product group, through DP-06; no reference-data list is read |
| `EditionShapeCheck` | Service | The presence of the bands, the floors and the ranges sheet with their header rows, and the row counts; no business value is read |
| `EditionDateCheck` | Service | `validFrom` against the `valid_from` of the version in force |
| `ReferenceLoadClient` | Client | The pass-through of the file bytes to the owner's reference-load operation, one hop, 2 s, with the breaker |
| `EditionRecordWriter` | Service | The DP-03 entry of an accepted edition and its outbox row, in the transaction that produces the answer |
| `IdempotencyStore` | Service | The stored answer per `Idempotency-Key` and the file digest |
| `EditionReader` | Service | The editions of a product group from the local chain, the version in force from the parameters contract and the load state from the owner |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` are created by RWB-P4-E1037-APP and the library tables `outbox_event`, `processed_event` and `idempotency_key` by the service baseline in the per-service Flyway sequence of DP-15; this story reads and writes them.
- No repository of this module exposes a save, update or delete against a reference table: the rows of the edition are the owner's, and the only writes are the decision-record row, its outbox row and the idempotency row.
- The record, the outbox row and the idempotency row commit in one local transaction; a failure rolls them back and the answer is withheld with MSG-P7-003.
- The workbook is not stored: the bytes are streamed to the owner and the record names the load rather than the file.

**Configuration and reference data**

- The product groups of LOV-PRODUCT are reference data of `rwb-case`, answered through the parameters contract with the version in force; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so no reference-data list is read and the point is raised in the key's gap (GAP-0870; ASM-1577); no product group is a constant in code (BR12).
- The version in force of a product group with its `valid_from` and its policy version label is a parameter row read through DP-06 (RWB-P3-E1042-CON); the parameter key is Not specified in the source documents (GAP-0870; ASM-1577) and the contract review fixes it with the owner.
- No band, floor, range, amount, percentage or boundary is read, compared, cached or written by this story at all: the number set is the owner's and this story is the door.

**Build steps**

1. `ProductPolicyController` with the two paths, the multipart part, the `Idempotency-Key` requirement and the error envelope; contract test against RWB-P4-E8009-CON.
2. `PermissionReader` and the C and R letters in Rules and parameters: granted for RW-COE, refused with MSG-P4-002 for RW-PRODHEAD and RW-CASEOWN; tests for AC3 and X5.
3. `ProductGroupReader` over the parameters fake; the 422 naming `productGroup` and the version in force of a product group.
4. `EditionShapeCheck` with a workbook per part and a workbook missing one: the 422 naming the part and the proof that the owner is not called; tests for AC4.
5. `EditionDateCheck` with `validFrom` before, on and after the version in force; tests for the second half of AC4.
6. `ReferenceLoadClient` over the reference-load fake: the unchanged pass-through, the 409 of AC5, the 503 of X8 and the resume on the same key.
7. `EditionRecordWriter` and `IdempotencyStore`: one entry per accepted edition, the stored answer, the combined write failure of AC2 and the replayed key of X10.
8. `EditionReader` and `GET /admin/product-policies/{productGroup}` over the chain and the two consumed contracts; the 422 of X12.
9. The composite route check through the gateway-bff fake, with the six states of section 15, and a test that a new product group and a new policy version need no build.

**Feature switch.** The story carries no switch of its own. Which product groups may be edited is reference data, and which version is in force is a parameter row, so turning a product group off or on is a data change and not a flag.

**Done when.** The tests of section 16 pass; an edition of MORTGAGE is accepted by the fake in SIT with load "LOAD-2027-000118" in `LOADED` and one record entry carrying the product group, the policy version and the load id; a caller with R only is refused with MSG-P4-002 and the workbook is not opened; an edition missing the floors sheet and an edition dated before the version in force are refused with MSG-GEN-001 naming the part and `validFrom`, with no owner call; a version the owner refuses answers 409 with MSG-GEN-004 and nothing recorded; and a forced record failure answers 503 with MSG-P7-003 with nothing in force.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no Recovery Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no C letter in Rules and parameters on the post, or no R letter on the read | You cannot {action} here. Your role does not include it. | This story, on both operations; the file is not opened |
| MSG-P4-004 | Carried from the legacy story's message table; this story answers no break-glass branch | Emergency access is on until {time}. Every action is recorded. | Not produced here: the access event and the grant belong to other stories of this service |
| MSG-GEN-001 | A required query field or the file part is empty, the product group is not a list value, a part of the workbook is missing, `validFrom` precedes the version in force, or the key is replayed with another file | Enter {field}. | This story, with the part or the field named in the body |
| MSG-GEN-004 | The parameters owner refuses the version | Someone else changed this record. Reload it to see their change. | This story, on the 409 |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, after a failed record append |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 422 also carries `field` — or the part of the workbook — so the screen can point at the failing element without a second call. The business texts are copied unchanged from the legacy story where the message already existed; no new business text is written by this story.

### 15. Screens and states

The administration screen that carries the edition is served through the gateway-bff composite route of DP-19, which calls the two operations of this story and the parameters read in parallel, one hop each, and merges the answers. This story renders no screen of its own.

| Screen | State | What it shows |
|---|---|---|
| The administration screen of the edition (not named in the sources) | Empty | No edition is recorded for the product group: the versions list is empty and the upload control is offered to a caller with the C letter only |
| The administration screen of the edition | Checked | The workbook carries the bands, the floors and the ranges sheet with their header rows and `validFrom` is not before the version in force; the upload is enabled |
| The administration screen of the edition | Refused before the owner | The 422 of X3 or X4 with the missing part or the field `validFrom`, and the version in force unchanged |
| The administration screen of the edition | Refused by the owner | The 409 of X7 with MSG-GEN-004 and the invitation to reload the versions |
| The administration screen of the edition | Loaded | The 201 with the edition id, the policy version, the load id, `LOADED` and the valid-from date, shown as waiting for the owner's approval |
| The administration screen of the edition | Versions | The editions of the product group with their policy version, load id, state, valid-from date and recorded time, and the one in force at the top |
| The administration screen of the edition | Refused caller | The 403 with MSG-P4-002 for a caller with R only, and no list of files or editions of another product group |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority in its screen table although the edition sits on neither: SCR-39 carries the rule versions (RWB-P4-AD011-APP) and SCR-41 carries the delegation limits (RWB-P4-E1038-APP). The states of SCR-39 (empty, loading, error and no access) are Not specified in the source documents (CG-ALL-5490). For SCR-41 the loading, error and no access states are Not specified in the source documents (CG-ALL-5491), and its empty state is as Screen Specifications v1 gives it. Which screen carries the treatment policy edition, its field list and its route are Not specified in the source documents (GAP-0870; ASM-1577) and belong to RWB-PLT-N001-CON and to the Epic 8 screen work.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-009-01 | AC1, BR1, BR3 | Contract | A workbook with the bands, the floors and the ranges sheet for MORTGAGE, posted against the reference-load fake answering load "LOAD-2027-000118" in `LOADED` for version "MORT-POL-2027.01", and the 201 answered with the six fields |
| TC-E8-009-02 | AC2, BR9 | Component | The decision-record append forced to fail during an accepted edition: 503 with MSG-P7-003, no answer and nothing in force |
| TC-E8-009-03 | AC3, BR4, BR5 | Component | "U-4302" with RW-PRODHEAD and R only posts an edition: 403 with MSG-P4-002, the workbook is not opened, the owner is not called and no entry is written |
| TC-E8-009-04 | AC2, BR9 | NFR | The record store made unavailable during the upload: the transaction rolls back, the answer is withheld and the retry under the same key completes it without a second load |
| TC-E8-009-05 | AC4, BR6 | Component | A workbook without the floors sheet, a workbook with `validFrom` before the version in force, and a product group that is not a LOV-PRODUCT value: three 422 answers naming the part, `validFrom` and `productGroup`, with no owner call |
| TC-E8-009-06 | AC5, BR7, BR8, BR10, BR11 | Component | A version the owner refuses answers 409 with MSG-GEN-004 and nothing recorded; an accepted edition answers 201 with loadId "LOAD-2027-000118" and `LOADED` and appends one entry with productGroup "MORTGAGE", policyVersion "MORT-POL-2027.01" and that loadId; a replay with the same key and the same file answers the first edition |
| TC-E8-009-07 | BR2, BR3, BR12, ASM-3438 | Component | Each table of section 12.7 at its boundary: the workbook reaches the owner unchanged with no `lov_value`, `reference_version` or `reference_row` row written here; `role` and `permission` are read only; a new product group or version arrives as a parameters row and needs no code change |
| TC-E8-009-08 | AC6, BR2, BR12 | Component | The edition accepted for MORTGAGE: no `lov_value`, `reference_version` or `reference_row` row is written here, and the product group and the version in force are read through the parameters contract with no such value as a constant in code |
| TC-E8-009-09 | AC7 | Contract | A request with no authenticated session to POST /api/recovery/access/v1/admin/product-policies answers 401 and reads no file; an edition id not recorded answers 404 at Not specified in the source documents (NEWAC-RWB-P4-E8009-APP-AC7) |
| TC-E8-009-10 | AC8 | Component | The rwb-case reference-load fake does not answer for "MORT-POL-2027.01": the answer is Not specified in the source documents (NEWAC-RWB-P4-E8009-APP-AC8) and nothing is recorded or appended |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows of RWB-E8-009 are kept: TC-E8-009-01 for AC1, TC-E8-009-02 for AC2, TC-E8-009-03 for the legacy `Access` case, which is the refusal of AC3, and TC-E8-009-04 for the legacy `Principle 5` case, which is the forced record failure. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16; two rows are added for the new criteria of this story. The integration copy of the set is the wave 4 harness's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No value that a business person may change is written in code: the product groups, the version in force and the dates are rows and reference data with a version (BR11, BR12), and a test proves that a new product group and a new policy version need no build.
- No band, floor, range, amount, percentage or boundary is read, compared, logged or copied by this service: the edition is bytes it passes through, and the only things it reads out of the file are the presence of its three parts and their row counts (BR2, BR3).
- No personal data anywhere: the caller is a reference and a group from `v_ace_iam_group`, the record carries codes, versions, load ids, dates and the caller reference, and no name, e-mail address or personal field appears in the answer, the entry or the test data (NFR-040).
- No read of another service's tables (DP-01): `lov_value`, `reference_version` and `reference_row` are `rwb-case`'s, `treatment` is `rwb-treatment`'s, `decision_log_entry` and the rule rows are `rwb-decision`'s, and no join crosses a schema. The load, its state and the version in force arrive in contract answers.
- One owner for the values: only `rwb-case` stores and versions the edition rows, and this module has no write statement against a reference table, so a door cannot change a policy behind its owner's back.
- No answer without its record: the entry of an accepted edition commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR9, R-UNI-39).
- A refusal names what is wrong and nothing else: a refusal names the missing part or the field and never a band, a floor, a range, a case or another product group's edition, so it cannot be used to map the policy.
- The same bytes with the same key answer the same edition: the operation is idempotent on the key and the digest, so a retry after a timeout cannot load a second version (BR10, R-UNI-40).
- Every workbook used in development and in test is synthetic: no production policy extract is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval | Program, Product head; Epic 3 | FEAT-ADM-04 | A2.20 Set the treatment policy by product | BR1, BR2, BR3 | TC-E8-009-01, TC-E8-009-05 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Program, Data and reporting | FEAT-ADM-04 | A2.20 Set the treatment policy by product | BR2, BR11, BR12 | TC-E8-009-05, TC-E8-009-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 BRD | FEAT-ADM-04 | A2.20 Set the treatment policy by product | BR4, BR5 | TC-E8-009-03 |
| R-UNI-38 | A new version applies from its effective date | Universal rules | FEAT-ADM-04 | A2.20 | BR6, the state transitions of section 9 | TC-E8-009-05 |
| R-UNI-39 | A decision log entry that cannot be written blocks the action | Universal rules | FEAT-ADM-04 | A2.20 | BR8, BR9 | TC-E8-009-02, TC-E8-009-04 |
| R-UNI-40 | The same event twice with the same key is ignored and the idempotency hit recorded | Universal rules | FEAT-ADM-04 | A2.20 | BR10 | TC-E8-009-06 |

| Legacy reference | Where it is kept |
|---|---|
| As a product head (Mortgage, HP, SSME), I want the Workbench to let the product head set the bands, floors and ranges for their product | Section 1, section 2 |
| AC1 Set the treatment policy by product, word for word with its origin tag | Section 7, AC1; TC-E8-009-01 |
| AC2 Not recorded, word for word with its origin tag | Section 7, AC2; TC-E8-009-02 and TC-E8-009-04 |
| The legacy endpoints `/admin/rule-versions` and its approve | Moved: P7 `rwb-decision` under ASM-0040 and RWB-P4-AD011-APP; sections 1, 19 |
| The legacy data table `treatment`, `decision_log_entry`, `rule_row` and `role` | Section 11: `treatment` is S2's, the ledger and the rule rows are P7's, and only `role` and `permission` are this service's |
| The legacy permission table (Rules and parameters C: RW-COE; A: RW-RISK) and the FSD primary role | Section 10 and BR5, with the conflict of GAP-0870 and ASM-1578 |
| The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority | Section 15, carried as a screen the sources do not name for this feature |
| MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001, MSG-P7-003 | Section 14 and the exception paths of section 5 |
| Legacy test cases TC-E8-009-01 to TC-E8-009-04 | Section 16, extended with TC-E8-009-05 and TC-E8-009-06 |
| The guardrails of RWB-E8-009 | Section 17 |

### 19. Out of scope

- The bands, the floors, the ranges and their storage, versioning, approval and rollback: `rwb-case` (P3) under ASM-0071 and ASM-0041. This story hands the file over and reads no value of it.
- The list version ingest of this service (RWB-P4-AD009-APP) and the approval, verification and rollback of a load (RWB-P4-AD010-APP). This story neither replaces them nor depends on them.
- The rule-version load and its approval, and the rule package registry: `rwb-decision` (P7) under ASM-0040, and RWB-P4-AD011-APP and RWB-P4-AD012-APP in this service epic.
- The treatment and the treatment policy of a case: S2 `rwb-treatment` and the treatment service's own stories; this administration story sets the product-level number set and decides no case.
- The delegation limits and their load: RWB-P4-E1038-APP, and SCR-41 Delegation of authority.
- The administration home and the access log: RWB-P4-E8006-APP and RWB-P4-AD007-APP.
- The administration screen itself, its panels beyond the edition and its composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
