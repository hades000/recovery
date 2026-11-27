# RWB-S2-E3018-CON Generate the treatment document set - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-018 for rwb-treatment. The legacy acceptance criteria stay with the application slice; every criterion here is new (D-RCV-60) and tests only the contract deliverable. The contract publishes the document-set surface of the service on base `/api/recovery/treatment/v1` (DP-13): the optional `documentSet` section of the treatment answer as a compatible addition at major version 1, the set request element the stage hands to the rendering activity, the set status vocabulary, the error set and the fakes, with the section and the request declared as the working read because no source gives them a shape (GAP-2685; ASM-4428). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Release slice | Contract publishes in wave 2; the business release stays 31 January 2027 (tentative) (GAP-1709) |
| Legacy key | RWB-E3-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Open decisions | DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner for rwb-treatment**, I want **the published contract of the treatment document set — the `documentSet` section of the treatment answer with the four document types, the template code and the pinned version of each, the set status and the rule version that decided it, the set request element the stage hands to the rendering activity, the status vocabulary, the error set, the compatibility rule and the fakes — instead of the monolith's one `recovery` schema and one in-process document table**, so that **the application slice, the rendering activity, the gateway route and the wave 2 harness all build against one frozen set surface from Day 1, and no consumer invents a document type, a status or a personal field that the source never gave**.

This story owns:

- the `documentSet` section of the treatment answer: its name, its properties, which of them are stored and which are returned per request, and the statement that it is an optional addition to the treatment resource of RWB-S2-E3001-CON;
- the read operation the section is served through, named from the read of RWB-S2-E3001-CON on base `/api/recovery/treatment/v1`, with the access right and the error set, and the statement that no write operation is published (DP-13);
- the `DocumentSetRequest` element the stage hands to the rendering activity, with one entry per document type, the template code, the template version, the treatment and case references, the party count and the rule ID and version;
- the set status vocabulary and the completeness rule as contract terms, with the statement that no set state is stored as a column;
- the compatibility rule, the pinning rule and the drift test, and the fake set every consumer uses.

Reference data read: the four document types and their template versions are catalogue values under the reference-data contract (DP-06, DP-07). Parameters read: Not specified in the source documents (DOR-RWB-S2-E3018-CON-20).

It does not own: the behaviour behind the section, which is RWB-S2-E3018-APP; the rendering engine, the templates, the merge fields, the rendered body and the file custody, which are RWB-S2-E2026-APP, P5 rwb-document and P6 rwb-comms (ASM-4427); the treatment resource, its create, its read and its element, which are RWB-S2-E3001-CON; the offer surfaces of the module, which are RWB-S2-E3002-CON, RWB-S2-E3003-CON and RWB-S2-E3012-CON; the case status and the tasks, which are rwb-case's (ASM-4425); the decision-record library, which is RWB-PLT-E1027-CON; the gateway-bff composite route, which is RWB-PLT-N001-CON; and the ACE view, its grant and its ingestion, which are P1's and the ACE DB stories' (ASM-4426).

### 2. Business rationale

Legacy RWB-E3-018 had no contract to publish: the document rows, the treatment row and the decision log lived in one schema and one process, so the set of documents a treatment needed was a list in code and the template version a document carried was a column of the same table. The microservice split removes that option. The rows now belong to rwb-document, the templates to rwb-comms, the case status to rwb-case, the record to the local library, and the answer is served by the gateway route, so four consumers need the same answer to the same questions before any of them writes code.

**The criteria rest on FSD steps (GAP-1708).** The FSD S2 acceptance placeholders are not observable, so every criterion of section 7 is written from the FSD step, rule and field catalogue it covers, and the FSD owner replaces the placeholders at the next FSD version.

**The division of the legacy key is fixed.** The legacy acceptance criteria **AC1 to AC4 stay with RWB-S2-E3018-APP**; every criterion in section 7 is new and tests only the contract deliverable in this title. The treatment resource and its read are RWB-S2-E3001-CON's, the rendering call is RWB-S2-E2026-APP's against RWB-P5-E2026-CON, and nothing of either is restated here.

The contract has to exist first for three reasons. The **set has no field anywhere**: TSD S2 T3.1 gives `treatment` DF-TRT-001 to DF-TRT-033 and none of them is a document set, a set status, a template code or a template version, and the legacy data table names the document entity only as DF-DOC-001 to DF-DOC-011 in the same schema, so without a published section one consumer reads a set from a table that will never hold it and another keeps the list in code (GAP-2685; ASM-4428). The **rendering is another service's**: the four document types and the Legal-approved template version are P6's catalogue and P5's engine, so the request has to be published as an element the engine consumes, not as a table this service reads (ASM-4427). And the **party boundary is the risk**: the legacy set names the customer on each document, so the contract has to say that this service supplies keys and a count and never a name, an identifier or an address (ASM-4426).

The contract also fixes what it does not do: it declares no business table, adds no column, publishes no event of its own, declares no workflow and no Schedule, and publishes no write operation, because the set is composed by rule and the officer takes no separate action.

The fake is the Day-1 unblocker: the application slice, the rendering activity, the gateway route and the harness can build the complete, refused, incomplete and unmatched answers before the live catalogue, the live engine and the live rule packages exist (Template and Rules §R5.4 class C).

### 3. Preconditions

- The service identity is fixed by Template and Rules §R4 and the context pack: schema `rwb_treatment`, base `/api/recovery/treatment/v1`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13).
- The set section has no source shape: TSD S2 T3.1 carries no set, template-version or set-status field, FSD S2 A2.18 has no field catalog at all, and the legacy story names the document entity only as DF-DOC-001 to DF-DOC-011, so the section and its properties are the working read of ASM-4428 (GAP-2685).
- The four document types of the set are the catalogue's values with the Legal-approved template version in force; no source fixes the set composition per treatment type, so the request declares one entry per type the treatment requires and the composition itself is the catalogue's value, not a contract value (GAP-2685; ASM-4427).
- The rendering call is RWB-S2-E2026-APP's against RWB-P5-E2026-CON; the contract names that contract and does not restate it, so this document publishes an element the stage hands over and no REST operation of its own for the set (ASM-4427).
- The party boundary is fixed: the request carries the party count and the party keys, never a name, a national identifier, an address or a document number; the merged values on a document body belong to the engine (ASM-4426).
- The capability area "Treatment and offer" and the rights C and R are the access declaration of TSD S2 T6.1 and the legacy permission table; the check is the guard library's and the contract declares the rights only (ASM-4430).
- RWB-S2-E3001-CON is named and not restated: the set section is declared as an optional addition to the treatment element of that contract, at the same major version, so its consumers see a compatible change.
- RWB-PLT-E1027-CON and RWB-PLT-N001-CON are published, so the contract can name the record write and the composite route without redeclaring either (DP-03; DP-19).
- The validation messages keep their legacy identifiers and texts, and no published catalogue defines their entry format, so the entry format is the working read.
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), sits in contract group `CG-W2`, and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the `documentSet` section: its name, its properties, the stored and the returned ones, and its place in the treatment answer of RWB-S2-E3001-CON.
2. The author names the one read operation the section is served through, its access right, its errors and the statement that no write operation is published.
3. The author fixes the `DocumentSetRequest` element: one entry per document type with the template code and version, the treatment and case references, the party count and the rule ID and version, and the rule that no personal value appears.
4. The author fixes the set status vocabulary: complete, incomplete, refused and unmatched, with the statement that none of them is a column of `rwb_treatment`.
5. The author fixes the error set: the status codes, the message identifiers and the texts, and the note that the idempotency key of the rendering call is that contract's and not this one's.
6. The author writes the compatibility rule — an optional section may be added at the same major version and a breaking change raises major version 2 — and the pinning rule for the consumers.
7. The author writes the negative rules: no table, no column for a set status or a template version, no personal field, no document read and no write of another service's row.
8. The lint and schema steps run: the operation entry compared against TSD S2 T-A.1 and the treatment read, the section and the request validated against the OpenAPI document, the examples scanned for personal data, and the error table checked against the message identifiers.
9. The fake set is generated from the document: the complete deed-in-lieu set, the complete restructure agreement, the refused template, the missing type, the unmatched type and the refused field answers.
10. The contract test runs the fakes against the document on every change and fails the build on any drift; the document and the fakes are published at v1 and the consumers pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The section is published as required, or without a version tag on the treatment answer | The schema validation fails the build; the section is optional on the answer of RWB-S2-E3001-CON | None | AC1 |
| X2 | A set status or a template version is published as a column of `rwb_treatment`, or the document says the list of documents is kept in code | The schema and lint steps fail the build; the status and the request stay properties of the answer and the element | None | AC1, AC4 |
| X3 | A party name, a national identifier, an address or a document number appears in the request or the section | The personal-data scan fails the build; the request carries the party count and the keys only | None | AC2 |
| X4 | An error answer is published without a message identifier, or with a code the legacy story does not carry | The error-table check fails the build; every code is mapped to its identifier and its text | None | AC3 |
| X5 | A breaking change is made to a path, a property or the answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consumer ships without the drift test, or its code drifts from the published schemas | The registry refuses the change and the drift test fails that consumer's build | None | AC6 |
| X7 | A value a consumer needs is named by no source — a property name, a status value, a set composition or a reason code | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2685; ASM-4428) | AC7 |

X1 and X5 are contract-governance paths, X2, X3 and X4 are the paths an invented column, personal field or error adds, X6 is the drift rule of class C, and X7 is the reason the section, the status vocabulary and the request are published as a working read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing but the treatment read it extends, reads no business data and starts on Day 1 |
| Negotiable | The property names, the example values and the fixture set are open until v1 is frozen; the one read entry, the request element, the status vocabulary, the error set and the compatibility rule are fixed |
| Valuable | Unblocks the application slice, the rendering activity, the gateway route and the wave 2 harness on Day 1 and keeps the set out of the schema |
| Estimable | One section, one request element, one read entry, four statuses, four errors and six fakes |
| Small | One sprint for the document, the schemas, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: treatment document set contract

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the service base is /api/recovery/treatment/v1, the schema rwb_treatment and the topic rwb.treatment.events.v1
    Given the contract declares the document set section, the set request and the status vocabulary only

  Scenario: AC1 The set section is fixed as an optional addition to the treatment answer (new, D-RCV-60)
    Given the answer schema of the treatment read of RWB-S2-E3001-CON
    When the extended schema is validated
    Then the answer carries an optional documentSet section with setStatus, composedAt, ruleId, ruleVersion, reasonCode and a documents array
    Then each element of documents carries documentType, templateCode, templateVersion, documentId, docVersion and documentStatus
    Then the document states that setStatus, templateCode, templateVersion and documentId are returned per request and are never a column of rwb_treatment
    Then the document states that the section is an additive, backward-compatible change at major version 1 and that RWB-S2-E3001-CON owns the operation entry
    Then an example carries a type, a template code, a version, a status and a date and no national identifier, account number, address or name

  Scenario: AC2 The set request is fixed and carries no personal value (new, D-RCV-60)
    Given the request schema of the stage input and the lint rule of the document
    When the request element is validated
    Then DocumentSetRequest carries caseRef, treatmentRef, ruleId, ruleVersion and a documents array with documentType, templateCode, templateVersion and partyCount
    Then the document states that the party set is supplied as a count and as party keys, and that no name, national identifier, address or document number is supplied by this service
    Then the lint fails the build if the request declares a party name, a national identifier, an address, a document number or a document body
    Then the document states that the rendering call, its idempotency key, its timeout and its error set belong to RWB-P5-E2026-CON and are not declared here

  Scenario: AC3 The read surface, its access rights and its error set are fixed (new, D-RCV-60)
    Given the operation section of the document
    When it is validated against TSD S2 T-A.1 API-S2-002 and the legacy permission table
    Then exactly one operation entry is named, the read of the treatment answer at GET /treatments/{treatmentId}, under capability area Treatment and offer with right R
    Then no write operation is published, because the set is composed by rule R-DIL-14 or R-RES-10 on the case signal and the officer takes no separate action to produce it
    Then the entry declares 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, and declares no idempotency key because no state changes on the read
    Then the document maps MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P7-009 to the answers that carry them and adds no message identifier
    Then an error answer carries the message identifier, the merge fields and the trace identifier only

  Scenario: AC4 The set status vocabulary is fixed and carries no business value (new, D-RCV-60)
    Given the vocabulary section of the document and the lint rule of the document
    When a status is used in the section or in the request answer
    Then setStatus is one of COMPLETE, INCOMPLETE, REFUSED or UNMATCHED
    Then the document states that a status is a report of the evaluated rule set and is never a stored lifecycle and never a default
    Then the document states that the four document types and their template versions are catalogue values read at their version and are never enumerated as business values
    Then the lint fails the build if a document type, a template code or a template version is declared as a constant of this contract

  Scenario: AC5 Versioning separates a compatible addition from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to the published surface
    Then adding an optional property or an optional section keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a breaking change to the read entry, a required property, a status value, an error code or the answer raises major version 2 and v1 is never edited in place
    Then each consumer pins a published version and raises a change request rather than a private variant

  Scenario: AC6 The fake answers the document and every consumer runs the drift test (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the set fake, the request fake, the error fake, the treatment resource fake and the composite route fake
    Then the set fake answers a complete deed-in-lieu set of three documents, a complete restructure agreement, a set with one refused template, a set missing a type, an unmatched type and a set refused for a named field
    Then the error fake answers 403, 404, 422 and 503 with their message identifiers and no personal data
    Then the drift test fails the build of any consumer whose request, answer or error does not match section 12

  Scenario: AC7 A value no source names is published as a working read and the gap stays open (new, D-RCV-60)
    Given a consumer needs a property name, a status value, a set composition or a reason code that no source names
    When the value is added to the contract
    Then the value is published as the working read of its assumption and cites its gap identifier
    Then the gap stays open in the register until a source names the value
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here, because **AC1 to AC4 of RWB-E3-018 are owned by RWB-S2-E3018-APP**, and every identifier, rule, message and field range is taken from the legacy story, the TSD appendix or the rule set character for character.

### 8. Business rules

| ID | Covered by | Rule | Source |
|---|---|---|---|
| BR1 | AC1; TC-S2-E3018-CON-01 | The set answer is one optional section of the treatment answer of RWB-S2-E3001-CON, at the same major version, and no consumer carries a private copy of it | GAP-2685; ASM-4428 |
| BR2 | AC1; TC-S2-E3018-CON-01 | The set status, the template code, the template version and the document reference are returned per request and are never a column of this schema and never a list in code | ASM-4428; DP-01 |
| BR3 | AC2; TC-S2-E3018-CON-02 | The request carries the party count and the party keys, never a name, a national identifier, an address or a document number; the merged values on the body belong to the engine | ASM-4426, ASM-4427 |
| BR4 | AC3; TC-S2-E3018-CON-03 | One read operation is named under right R with its error set, and no write operation, because the set is composed by rule and ends in a report | R-DIL-14, R-RES-10; TSD S2 T-A.1 API-S2-002 |
| BR5 | AC4; TC-S2-E3018-CON-04 | The four document types and their Legal-approved template versions are catalogue values in force, read at their version and never enumerated by this contract | BR-S2-018; ASM-4427 |
| BR6 | AC3; TC-S2-E3018-CON-03 | The contract declares the access rights only; the check is the guard library's on capability area "Treatment and offer" | TSD S2 T6.1; ASM-4430 |
| BR7 | AC5; TC-S2-E3018-CON-04 | A published version is never edited: a compatible addition stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |
| BR8 | AC2; TC-S2-E3018-CON-02 | The rendering call, its contract, its idempotency key, its timeout and its error set are RWB-P5-E2026-CON's and are named, not restated; review and signature are requested through the P6 contract, and the answer holds only the document reference, never document content | ASM-4427 |

**Working read of the open composition (GAP-2684).** The set is composed per treatment type from the catalogue value in force. The rendering is handled by RWB-S2-E2026-APP against the published RWB-P5-E2026-CON; the activity name is Not specified in the source documents (GAP-2684), so this pair records no C dependency. The party set is read as keys and a count from the v_ace_customer view that P1 and the ACE DB stories own. The case trigger is Not specified in the source documents (GAP-2684). The set outcome travels in the answer section and the local decision record.

**Where each rule lives in the target.** BR1 is the section table and the note on the operation entry. BR2 is the stored-versus-returned column of every property and the lint rule of X2, and it is the reason the section exists at all rather than a set of columns. BR3 is the request table with the party count and the lint rule of X3. BR4 and BR6 are the operation table with its access column and the error table. BR5 is the catalogue note and the lint rule of AC4, which keeps every type and version a read value and never an enumeration. BR7 is the compatibility section and the pinning rule. BR8 is the note that the rendering call is another contract's and the reason this document publishes no operation for it.

### 9. State transitions

None at run time: a document and a schema have no state. Two vocabularies are fixed here, and the runtime transitions behind them are specified by RWB-S2-E3018-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Set answer | COMPLETE | Every type the treatment requires is present once, at the approved template version in force |
| Set answer | INCOMPLETE | A required type or a required value is absent; the answer names it |
| Set answer | REFUSED | The rendering refused the request; the answer carries the message identifier and the field |
| Set answer | UNMATCHED | No template covers the treatment type and the product group; the answer carries the reason code |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited in place |

The case states TRANSFER_PRICE_SET, OFFER_WITH_CUSTOMER_DIL, WITH_FCR_OFFICER and AWAITING_CREDIT_APPROVAL are rwb-case's and are named in the section only as the reason a set exists (ASM-4425).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the section and request schemas, the status vocabulary, the error table and the fakes |
| The service team of rwb-treatment | Consumes the contract, pins the version and raises a change request rather than a private variant |
| The rwb-treatment tech lead | Confirms that the one read entry, the request element and the status vocabulary are the ones the application slice fills |
| The owner of RWB-S2-E3001-CON | Confirms that the section is an optional addition to the treatment element at the same major version |
| The owner of RWB-S2-E2026-APP and of RWB-P5-E2026-CON | Confirms the request element is enough for the rendering activity and that the call, its key and its error set stay that contract's |
| The P6 rwb-comms owner of the template catalogue | Confirms that the document types and the approved template version are read at their version and never enumerated here |
| The P1 rwb-source-data owner | Confirms the read-only view boundary behind the party count |
| The wave 2 integration harness owner | Confirms the fake set is enough to prove the cross-service path |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

The one REST operation of this contract is authorised through the rwb-access authorise check on right R, capability area Treatment and offer (DP-08).

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | BR Field ID | Value |
|---|---|---|
| Business data published | Not specified in the source documents (DOR-RWB-S2-E3018-CON-7) | None. The document publishes one read entry, two schemas, four status values, four message identifiers and six examples; no customer, account or case value appears |
| Stored fields referenced | DF-TRT-003, DF-TRT-013, DF-TRT-014 | DF-TRT-003 `decision_log_id`, DF-TRT-013 `outcome` and DF-TRT-014 `outcome_at` of `treatment`, referenced through the section and declared by RWB-S2-E3001-CON, not redefined here |
| Read fields referenced | DF-ACE-055 to DF-ACE-074 | DF-ACE-055 to DF-ACE-074 of `v_ace_customer`, reached only as the party count and the party keys the request carries, read only (ASM-4426) |
| Fields of another service named, not read | DF-DOC-001 to DF-DOC-011 | DF-DOC-001 to DF-DOC-011 of `document` in `rwb_document`: the reference of each generated document arrives on the rendering result and is never read from that table (ASM-4427; DP-01) |
| Personal data | Not specified in the source documents (DOR-RWB-S2-E3018-CON-7) | None. The examples carry a type, a template code, a version, a status, a date and a business key, and the actor and trace references are identifiers, never names |
| Tables published | Not specified in the source documents (DOR-RWB-S2-E3018-CON-7) | None. The contract declares no table and no column; `treatment` is the application slice's and the decision-record library object, named only (DP-01; DP-03) |
| Field identifiers | Not specified in the source documents (DOR-RWB-S2-E3018-CON-7) | The stored fields and the view fields carry the identifiers above; the section's own properties carry none, because no source gives them one (GAP-2685; ASM-4428) |

Service entity groups (treatments, contracts, settlement and deed-in-lieu agreements, plan timers) are held by rwb-treatment as product requirements; no physical table name is fixed here (GAP-1698). The eight treatment catalogue fields treatment.case_id, decision_log_id, treatment_type, proposed_by, proposed_at, offer_amount, haircut_amount and installments are required as written, and the contract, agreement, plan timer and booking reference are held with their physical field list open until the data architect writes it with the DB story (GAP-1712).

The one place where the contract could leak a value is the party: the document therefore fixes that the request carries a count and keys, that a name, an identifier, an address and a document number are outside it, and that no example value is presented as a person.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). The contract declares the `documentSet` section and names the one operation it is served through; the operation entry belongs to RWB-S2-E3001-CON and this contract adds an optional section to its answer at major version 1.

| Method | Path | Answer | Access | Idempotency |
|---|---|---|---|---|
| GET | `/treatments/{treatmentId}` | The treatment element of RWB-S2-E3001-CON with the optional `documentSet` section: `setStatus`, `composedAt`, `ruleId`, `ruleVersion`, `reasonCode` and a `documents` array whose elements carry `documentType`, `templateCode`, `templateVersion`, `documentId`, `docVersion` and `documentStatus` | Treatment and offer, right R | Not applicable; the read changes no state |

No write operation is published. R-DIL-14 and R-RES-10 compose the set on the case signal, the stage hands the request to the rendering activity, and the officer takes no separate action to produce it, so there is nothing to post or patch; the legacy endpoint table of RWB-E3-018 names the treatment create and read only, which is consistent with this surface (GAP-2685; ASM-4425, ASM-4428). The errors are 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503. Why the set has no source shape, and whether the bank ever intended a separate set operation, are Not specified in the source documents (GAP-2685; ASM-4428).

#### 12.2 REST operations consumed

None. The contract declares the surface and calls no service: the case status arrives on the signal the parent forwards, the party count comes from this service's own view, the record is an in-process call of RWB-PLT-E1027-CON, and the rendering call is RWB-S2-E2026-APP's against RWB-P5-E2026-CON (DP-03; DP-05; ASM-4425, ASM-4427). This is why the Work Package records no C dependency for the pair.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its event `TreatmentApproved` (EV-10) belongs to the approval story of the module. This contract publishes no event schema and declares no outbox row.

#### 12.4 Events consumed

None. The contract declares no subscription; the two events the application slice consumes — `rwb.decision.RulePackageInForce.v1` (EV-30) and `rwb.deviation.DeviationRaised.v1` (EV-06) — belong to P7 and S8 and are named in section 19, and the case status is a workflow signal and not an event of this contract (ASM-4425).

#### 12.5 Workflows and activities

None. The contract declares no workflow and no activity. It states only that the section is filled inside an activity on the owner's own task queue, that the request is handed to a rendering activity on the same queue, and that the decision record is called from that activity, so a replay reuses the recorded decision; the branch itself is RWB-S2-E3018-APP's set branch of `TreatmentWorkflow` on `rwb-treatment`.

#### 12.6 Schedules

None. The contract declares no Temporal Schedule and no legacy Quartz job. The 14-day offer validity of R-DIL-14, the 3 working-day approval clock of R-RES-10 and the escalation limit of R-RES-13 are durable timers inside the workflow and values in force in the rule set, not part of the published surface.

#### 12.7 Tables owned

None. The contract declares no table, no column and no key, and the negative rule is the deliverable: no set-status, template-code, template-version or set-time column exists in `rwb_treatment`, because no source gives one and a column would freeze a value that the catalogue and the rule set own (GAP-2685; ASM-4428; DP-01). `treatment` is RWB-S2-E3001-APP's business table, the decision-record library object of RWB-PLT-E1027-CON, named only, `document` is rwb-document's, `decision_log_entry` is P7's ledger, and the case and the task are rwb-case's; all are named here only.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Set fake | The `documentSet` section on `GET /treatments/{treatmentId}` | A complete deed-in-lieu set of three documents, a complete restructure agreement, a set with one refused template, a set missing a type, an unmatched type and a set refused for a named field |
| Request fake | The `DocumentSetRequest` element | A request with one entry per required type, its template code, its version and the party count; a request with a party name refused as invalid |
| Error fake | The error table | 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with its identifier, its merge fields and a trace identifier |
| Treatment resource fake | The answer the section extends | The treatment element of RWB-S2-E3001-CON, referenced and not restated |
| Composite route fake | The gateway-bff composite route of RWB-PLT-N001-CON | One hop for SCR-15, joining the treatment read with its set section; a refused route for a role without the right |
| Rendering result fake | The result of the rendering activity of RWB-S2-E2026-APP | One document per requested type with its code and version; a refusal naming a field; a withdrawn template. Referenced from that story's contract, not redeclared (ASM-4427) |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consumer rather than as a surprise at run time. The treatment resource fake and the rendering result fake are the published contracts of their stories and are referenced here, not redeclared.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 read entry, extended | 0 | OpenAPI 3.1 fragment; one hop to the service, 2 s timeout |
| Kafka | 0 event schemas | 0 | The service topic is named; this contract declares no event |
| SQL view | 1 read-only view referenced | 1 | SELECT only under DP-05; the party count and keys, no personal value |
| Temporal | 0 | 0 | The contract states the section is filled in an activity and declares no workflow |
| File, Nexus | 0 | 0 | No file and no Nexus operation: the body, the blob and the retention are rwb-document's |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the OpenAPI fragment and the two element schemas in `th.co.scb.ace.workbench.recovery.treatment.api`, the error table and the compatibility note in the contract document, and the fake set as a test asset. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2685; ASM-4428).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 enters the contract as one statement — the section is written with a record in the caller's transaction — and the H dependency sits on the application slice, which calls the library. DP-05 is the read-only boundary behind the party count and the reason no personal field is published. DP-13 is the base of the read entry and the reason the legacy base appears nowhere in the document. DP-19 is the route the two screens use, named here so that the composite route fake has an owner.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentReadOpenApi` | OpenAPI 3.1 fragment | The one read entry, its parameter, its errors, its access declaration and the note that it extends RWB-S2-E3001-CON |
| `DocumentSetSectionSchema` | Answer schema | The six properties of the section, the six of a document element and the stored, returned and computed note on each |
| `DocumentSetRequestSchema` | Stage-input schema | One entry per required type, the template code and version, the references, the party count and the rule version |
| `SetStatusVocabulary` | Document table | COMPLETE, INCOMPLETE, REFUSED and UNMATCHED, with the note that none is a stored lifecycle |
| `ErrorCatalogue` | Document table | The status codes, the message identifiers, the legacy texts and the merge fields |
| `CompatibilityNote` | Document section | The additive-versus-breaking rule, the pinning rule and the negative rules |
| `DocumentSetFakeSet` | Test asset | The six fakes of section 12.8 and the drift test every consumer runs |

**Database.** None. The contract creates no table, adds no column and declares no key; the negative rules of section 12.7 and of AC1 are the deliverable, and a review that finds a set-status, template-code, template-version or set-time column in `rwb_treatment` fails this story.

**Configuration and reference data.** The contract fixes no business value. The document types and the Legal-approved template versions are catalogue values in force, and the three clocks are values in force in the rule set; the only values in the document are the example values, and they are marked as examples. Capability area "Treatment and offer" and the rights C and R are read from rwb-access through the guard library, which the application slice calls (ASM-4430). The grant on the view is a DB story's (ASM-4426).

**Build steps**

1. Write the one read entry, its access right and its errors, and lint that no write operation and no second form appear (AC3).
2. Write the `documentSet` section, its six properties, the six of a document element and the stored, returned and computed note on each (AC1).
3. Write `DocumentSetRequest` and the lint that refuses a name, an identifier, an address, a document number and a body (AC2).
4. Write the status vocabulary and the lint that refuses an enumerated type, template code or version (AC4).
5. Write the error table with the four identifiers and their legacy texts, and validate one answer per code (AC3).
6. Write the compatibility note, the pinning rule and the negative rules (AC5).
7. Generate the six fakes and the drift test; wire the drift test into the build of RWB-S2-E3018-APP, the rendering activity's consumer, the gateway route and the wave 2 harness (AC6).
8. Publish v1 and record the pinned version of each consumer.

**Feature flag.** `rwb.treatment.document-set-contract`.

**Done when.** The document and the two schemas validate, the operation lint passes with one read entry and no write, the error table matches the four legacy identifiers and texts, the lint refuses a personal field and an enumerated type, the six fakes answer every example including the refused template and the unmatched type, the drift test is green on the build of this story and on the build of the application slice, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, or the set is missing a type the treatment requires | Enter {field}. | 422 on the request, or the INCOMPLETE answer; the field name is carried |
| MSG-P4-002 | The role does not hold the right on the capability area | You cannot {action} here. Your role does not include it. | 403, from the guard library |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, from RWB-PLT-E1027-CON |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. | 422, from RWB-PLT-E1027-CON, with the field |

The four texts are the legacy texts carried unchanged and the contract adds no message identifier. MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the three offer messages of the module, are kept in RWB-S2-E3018-APP's validation table because the legacy story carries them, and are raised by the offer stories. The text shown when a template is withdrawn or a type has no template has no source at all and is Not specified in the source documents (GAP-2685; ASM-4428). The entry format of each message in a published catalogue is Not specified in the source documents and is published as the working read. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. SCR-15 Settlement offer and SCR-14 Treatment record are reached through the gateway-bff composite route (DP-19), and the contract fixes only the answer those screens consume: the set status, the documents with their type, template code, pinned version and reference, the rule version and the reason of a refused or incomplete set. The screen states of SCR-15 — Draft, below floor, approved, sent, accepted — and of SCR-14 — Draft, submitted, approved, booked, broken — are the runtime states of the application slice and are named in section 9 only to keep the vocabulary apart. SCR-14 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-8816). SCR-15 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-8817).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3018-CON-01 | AC1 | Contract | The extended answer schema validated: the six section properties, the six document properties, the stored, returned and computed note on each, the additive note on the version, the absence of a set column and a personal-data scan of the example |
| TC-S2-E3018-CON-02 | AC2 | Contract | `DocumentSetRequest` validated: the references, the rule and version, one entry per type with its code, version and party count; the lint that refuses a name, an identifier, an address, a document number and a body |
| TC-S2-E3018-CON-03 | AC3 | Contract | The one read entry linted against TSD S2 T-A.1 API-S2-002 and the legacy permission table: right R, 401, 403, 404, 422, 503, no idempotency key and no write |
| TC-S2-E3018-CON-04 | AC4, AC5 | Contract | The four statuses and the lint that refuses an enumerated type, code or version; one compatible addition and one breaking change against the registry in BACKWARD mode |
| TC-S2-E3018-CON-05 | AC6 | Component | The six fakes answering every example, including the refused template, the missing type and the unmatched type; the drift test failing on a consumer that drifts |
| TC-S2-E3018-CON-06 | AC7 | Contract | A value named by no source published as the working read with its assumption and its open gap; the gap register entry kept open |

The legacy test set of RWB-E3-018 — TC-E3-018-01 to TC-E3-018-06 — is carried by RWB-S2-E3018-APP and by the wave 2 integration harness, and no legacy id is renumbered here: these five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the document types, the template codes and the versions are catalogue values in force and the three clocks are values in force in the rule set, so the only values in the document are examples, marked as examples.
- No personal data in a schema, an example, a fake or a log: the request carries a party count and party keys, and the scan fails the build otherwise.
- No table, no column and no key in the contract: the set status, the template version and the completion time stay out of `rwb_treatment` (DP-01; GAP-2685; ASM-4428).
- No document read and no document write: `document` is rwb-document's, and the reference of each generated document arrives on the rendering result (ASM-4427).
- No write operation: the set is composed by rule and ends in a report, and the officer takes no separate action (ASM-4425).
- No event and no outbox row of the contract's own: the service topic is named and its event belongs to the approval story.
- ACE data only through the read-only view or the owner's contract: the contract declares the boundary and no ACE object is copied (DP-05).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and a superseded marking.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-006 | The credit application, contract and mortgage documents for a deed in lieu are generated from templates | Program 5.9 | FEAT-TRT-18 | 07 Route, settle and claim | BR1, BR2, BR4, BR5; R-DIL-14 | TC-S2-E3018-CON-01, TC-S2-E3018-CON-03 |
| REQ-S2-006 | The same set carries the restructure agreement through the approval route, and the request is the element the engine consumes | Program 5.9 | FEAT-TRT-18 | 07 Route, settle and claim | BR3, BR8; R-RES-10 | TC-S2-E3018-CON-02 |
| Legacy test set RWB-E3-018 | TC-E3-018-01, TC-E3-018-02, TC-E3-018-03, TC-E3-018-04, TC-E3-018-05, TC-E3-018-06 | Program 5.9 | The legacy story's own feature FEAT-TRT-18 | 07 Route, settle and claim | The legacy rules R-DIL-14 and R-RES-10 | Executed by RWB-S2-E3018-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3018-APP | App development | H consumer: fills the section, composes the set, records and reports against this contract and its fakes; owner of the legacy acceptance criteria |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment resource and its read, whose answer this contract extends with an optional section |
| RWB-S2-E3002-CON, RWB-S2-E3003-CON, RWB-S2-E3012-CON | Contract | Referred to: the offer surfaces of the same module, which are not declared here |
| RWB-S2-E2026-APP, RWB-P5-E2026-CON | App development, Contract | Referred to: the rendering activity and the generation call the request element feeds, whose shapes stay theirs (ASM-4427) |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library the application slice calls in the caller's transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route the two screens use |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status, the parent `CaseWorkflow` and the task of an incomplete set |
| P5 rwb-document, P6 rwb-comms | Service, wave 1 | Own the document rows, the engine and the template catalogue the set names |
| Wave 2 integration harness | Integration | I: the cross-service proof of the set path against the live owners, with the `-ITG` copies of the legacy test set |

### 19. Out of scope

- The behaviour behind the section — the set composition, the party read, the rule evaluation, the record write and the stage outcome: RWB-S2-E3018-APP.
- The treatment resource, its create, its read and its element: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The rendering call, its contract, its idempotency key, its timeout and its error set: RWB-S2-E2026-APP and RWB-P5-E2026-CON (ASM-4427).
- The templates, the merge fields, the Legal approval of a version and the document types: P6 rwb-comms and P5 rwb-document.
- The document rows, the rendered body, the file custody, the retention and the e-signature: P5 rwb-document and its stories.
- The offer, the transfer price, the floor and the second signature: RWB-S2-E3002-CON, RWB-S2-E3003-CON and RWB-S2-E3012-CON.
- The case, its status, the parent `CaseWorkflow` and the task it raises: rwb-case (P3), which owns them (ASM-4425).
- The ACE view, its grant and its ingestion: P1 rwb-source-data and the ACE DB stories (ASM-4426).
- The decision-record library, its `MANDATORY` transaction, its chain and its envelope: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-15: RWB-PLT-N001-CON and the screen owners (DP-19).
- The two events the application slice consumes, `rwb.decision.RulePackageInForce.v1` and `rwb.deviation.DeviationRaised.v1`: their schemas belong to P7 and S8.
- The cross-service proof of the set path and the `-ITG` copies of the legacy test set: the wave 2 integration harness.
