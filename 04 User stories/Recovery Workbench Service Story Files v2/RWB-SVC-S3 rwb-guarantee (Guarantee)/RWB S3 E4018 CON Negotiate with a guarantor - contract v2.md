# RWB-S3-E4018-CON Negotiate with a guarantor - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-018 for rwb-guarantee. The legacy acceptance criteria stay with the application slice; every criterion here is new (D-RCV-60) and tests only the contract deliverable. The contract publishes the guarantee claim surface on base `/api/recovery/guarantee/v1` (DP-13) — the two operations the ownership rows give the service, the `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` elements of TSD S3 T-A.2, the negotiation facts that are request context and never columns, the `subrogationShare` element that no source names, the error set, the compatibility rule and the fakes — and it records that no read operation is published, that the GUARANTEE `state` and the LOV-CLAIM-STATUS `status` are two vocabularies, and that the negotiation body is a working read (GAP-2729, GAP-2730; ASM-4529, ASM-4530, ASM-4533). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 7 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Contract version | v1 (published; every consumer pins v1) |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S3-E4018-CON-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner for rwb-guarantee**, I want **the published contract of the guarantee claim — the two operations on the service base, the `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` elements, the negotiation facts that travel with a request and are never stored, the `state` and `status` vocabularies kept apart, the single `subrogationShare` element, the error set with the `Idempotency-Key` rule, the compatibility rule and the fakes — instead of the monolith's one `recovery` schema, one set of in-process interfaces and one undivided status column**, so that **the application slice, the claim-preparation slices, the gateway-bff route, the decision-record library and the wave 3 integration harness all build against one frozen claim surface from Day 1**.

This story owns:

- the two operation entries — `POST /cases/{caseId}/guarantee-claims` and `PATCH /guarantee-claims/{claimId}` — on base `/api/recovery/guarantee/v1`, with their access right, their request and answer elements, their errors and the `Idempotency-Key` on the create (DP-13);
- the `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` elements, and the note that fixes, for each property, whether it is stored or context-only;
- the `state` property of the answer, which carries the GUARANTEE state of TSD S3 T4, and the `status` property, which carries LOV-CLAIM-STATUS, as two named vocabularies that are never merged;
- the `subrogationShare` element, which the subrogation answer carries because the legacy criterion records the share against the case and no source gives it a name or a type;
- the error set with MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P7-009 mapped to status codes, and the `Idempotency-Key` rule with its repeat answer;
- the compatibility rule, the pinning rule and the drift test, and the fake set every consumer uses.

It does not own: the behaviour behind the two operations, the range check, the two subrogation outcomes and the record write, which are RWB-S3-E4018-APP; the claim preparation, the checklist and the filing of FEAT-GUA-01 and FEAT-GUA-02; the balance claim of FEAT-GUA-03; the demand notice of FEAT-GUA-05; the closing of the guarantee of FEAT-GUA-07; the decision-record library, which is RWB-PLT-E1027-CON; the gateway-bff composite route, which is RWB-PLT-N001-CON; the case, its status and its party record, which are rwb-case's; and the ACE views, which are rwb-source-data's.

### 2. Business rationale

Legacy RWB-E4-018 negotiated with a guarantor through one screen, two endpoints whose paths began with the shared base, and one `recovery` schema in which the claim row, the case and the decision log row sat in one process; there was nothing to publish and nothing to fake. The microservice split removes that option. The claim is now written by rwb-guarantee, its stage is a child of `CaseWorkflow` of rwb-case, the screen reaches it through gateway-bff, and the wave 3 harness proves the path across services, so four consumers need the same answer to the same questions before any of them writes code.

The contract has to exist first for four reasons. **The service publishes exactly two operations**: the ownership rows of S3 give rwb-guarantee `POST /cases/{caseId}/guarantee-claims` and `PATCH /guarantee-claims/{claimId}` and no third; the negotiation is therefore carried on the `PATCH` of the claim and no new operation is invented for it (GAP-2730; ASM-4533). **No read operation is published**: the same rows give the service no read, so SCR-17 cannot read the claim through this service, and the contract has to say so and hand the screen to the composite route rather than leave a caller guessing (GAP-2730; ASM-4533). **The negotiation facts have no home**: the approved range, the outcome and the share appear in the rules R-GUA-23, R-GUA-24 and R-GUA-29 and in the legacy criterion, while `guarantee_claim` stops at DF-TRT-022 and carries no range, no outcome and no share; if the body is not fixed, one consumer will send a range and another will store it (GAP-2728; ASM-4529). And **the two state vocabularies collide**: the legacy story moves the case to `SUBROGATION_POSITION`, TSD S3 T4 moves the GUARANTEE claim through the same names, and `LOV-CLAIM-STATUS` publishes a third list — so the contract must publish `state` and `status` as separate properties before any consumer writes a mapper (GAP-2729; ASM-4530).

The contract also fixes what it does not do: it declares no table, adds no column for the range or the notice expiry, publishes no event of its own, declares no workflow and no Schedule, and copies no part of the claim-preparation or the notice slice.

The fake is the Day-1 unblocker: the application slice, the claim-preparation slices, the gateway route and the harness can build the negotiation, the two subrogation answers, the refusal, the repeated key and the error answers before the live service, the live case workflow or the live payment exists (Template and Rules §R5.4 class C).

### 3. Preconditions

- The service identity is fixed by Template and Rules §R4 and the context pack: schema `rwb_guarantee`, base `/api/recovery/guarantee/v1`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery` (DP-13).
- The two operations are the ones the S3 ownership rows give the service, and the three element names are those of TSD S3 T-A.2 — `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` — copied character for character.
- The negotiation body and the `subrogationShare` element are the working read of the assumption, because no source document gives the negotiation a field list, a column or an element name (GAP-2728, GAP-2730; ASM-4529).
- Capability area "Treatment and offer" with right C for the create and right U for the patch is the access declaration of TSD S3 T6.1 and T-A.2; the check is the guard library's and the contract declares the right only.
- The error codes are the ones TSD S3 T-A.2 lists — 401, 403, 404, 409, 422, 503 — and the message identifiers are the legacy story's, with MSG-P7-009 added from the library.
- RWB-PLT-E1027-CON is published, so the contract can name the decision-record write the application slice makes in the same transaction, without redeclaring the library (DP-03).
- RWB-PLT-N001-CON is published, so the contract can name the composite route SCR-17 uses, without declaring a route (DP-19).
- The claim-preparation slices are named only: the create operation is published here and the behaviour behind it is theirs, so one contract answers for the whole claim shape.
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), sits in contract group `CG-W3`, and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the two operation entries: the method, the path on the service base, the access right, the request element, the answer element, the errors and the idempotency rule of each.
2. The author fixes `GuaranteeClaimRequest`: `claimType`, `claimDeadline`, `claimedAmount` and the optional `filedAt` of the claim field catalog of the functional specification.
3. The author fixes `GuaranteeClaimUpdate`: `paidAmount`, `status`, `state`, the negotiation outcome, the outcome date and `subrogationShare`, and states for each one whether it is stored or context-only.
4. The author fixes the answer `GuaranteeClaim`: the eight claim fields of DF-TRT-015 to DF-TRT-022, the `state` of TSD S3 T4, the `subrogationShare` and the standard version and timestamps.
5. The author fixes the two state vocabularies and the rule that `state` and `status` are never merged and never mapped inside the contract.
6. The author fixes the error set: the status codes, the message identifiers and their texts, and the `Idempotency-Key` rule with its repeat answer.
7. The author writes the compatibility rule — what a consumer may rely on and what raises a major version — and the pinning rule for the consumers.
8. The author records the negative rules: no read operation in v1, no table, no range or expiry column, no event and no workflow.
9. The lint and schema steps run: the operation entries compared against the ownership rows and TSD S3 T-A.1, the three schemas validated against the OpenAPI document, the examples scanned for personal data, and the error table checked against the legacy message identifiers.
10. The fake set is generated from the document and the contract test runs it on every change; the document and the fakes are published at v1 and every consumer pins the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document publishes a third operation, or a read operation of its own, or drops one of the two | The lint fails the build; only the two entries the ownership rows give are published | None | AC1 |
| X2 | An element of the update has no place in the schema, or the document adds a range, an outcome or an expiry column | The schema validation fails the build; the facts are declared context-only and no table is declared | None | AC2 |
| X3 | The answer merges `state` and `status`, or publishes one without the other | The lint fails the build; both properties are required and the note that separates them is required | None | AC3 |
| X4 | The subrogation answer is published without `subrogationShare`, or with a type the schema does not fix | The answer schema fails the build; the element is required on the subrogation answer | None | AC3 |
| X5 | An error answer is published without a message identifier, or with a code the legacy story does not carry | The error-table check fails the build; every code is mapped to its identifier and its text | None | AC4 |
| X6 | The `Idempotency-Key` is declared optional on the create, or a repeat is declared to store a second row | The lint fails the build; the header is required on the create and a repeat returns the first answer | None | AC4 |
| X7 | A breaking change is made to a path, an element, an error code or the answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X8 | A consumer ships without the drift test, or its code drifts from the published schemas | The registry refuses the change and the drift test fails that consumer's build | None | AC6 |
| X9 | A consumer needs a value no source names — the share type, the outcome vocabulary or the range element | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2730; ASM-4529) | AC3, AC7 |

X1 and X7 are contract-governance paths, X2 to X6 are the paths a missing, merged or invented element adds, X8 is the drift rule of class C, and X9 is the reason the negotiation body is published as a working read and not as a value found in a source.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The example values, the property order and the fixture set are open until v1 is frozen; the two paths, the elements, the two vocabularies, the errors and the compatibility rule are fixed |
| Valuable | Unblocks the application slice, the claim-preparation slices, the gateway route and the wave 3 harness on Day 1 and keeps the range and the share out of the schema |
| Estimable | Two operations, three elements, one answer, four messages, two rules and six fakes |
| Small | One sprint for the document, the schemas, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: guarantee claim contract

  Background:
    Given the rwb-guarantee contract document is published with major version 1
    Given the service base is /api/recovery/guarantee/v1, the schema rwb_guarantee and the topic rwb.guarantee.events.v1
    Given the contract declares the guarantee claim surface only, and no claim preparation and no notice

  Scenario: AC1 The claim surface is the two operations of the ownership rows and no read (new, D-RCV-60)
    Given the operation section of the contract document
    When it is validated against the S3 ownership rows and TSD S3 T-A.1
    Then it publishes POST /cases/{caseId}/guarantee-claims for opening a claim, under capability area Treatment and offer with right C
    Then it publishes PATCH /guarantee-claims/{claimId} for recording the claim result, under the same capability area with right U
    Then no other operation and no read operation is declared, so the screen read is the composite route's and not this service's
    Then the change note records that the negotiation is carried on the PATCH of the claim and that no third operation is invented for it
    Then the lint fails the build if a third operation or a read operation appears

  Scenario: AC2 The elements are fixed and the negotiation facts are not stored (new, D-RCV-60)
    Given the request schemas of the two operations and the schema of the service
    When the schemas are validated
    Then GuaranteeClaimRequest carries claimType, claimDeadline, claimedAmount and filedAt
    Then GuaranteeClaimUpdate carries paidAmount, status, state, the negotiation outcome, the outcome date and subrogationShare
    Then the outcome is recorded against the claim and the party reference of the case, and the case-level record of the party stays with rwb-case
    Then the document states that the approved range, the notice expiry and the rule package version are request context facts and are not columns of rwb_guarantee
    Then the document declares no table and no column for a range, an outcome or an expiry
    Then an example carries amounts, dates and codes and no account number, national identifier or name

  Scenario: AC3 The answer keeps state and status apart and carries the TCG share (new, D-RCV-60)
    Given the answer schema of the two operations
    When one subrogation answer and one refusal answer are validated
    Then GuaranteeClaim carries the eight claim fields of DF-TRT-015 to DF-TRT-022, state, subrogationShare and the standard version and timestamps
    Then state carries the GUARANTEE state of TSD S3 T4 and status carries LOV-CLAIM-STATUS
    Then the document states that the two vocabularies are never merged and never mapped inside the contract, and that the screen labels are the screen's own
    Then a subrogation answer carries subrogationShare, whose name and type are the working read of the assumption
    Then a refusal answer carries RESIDUAL_TO_ROUTE as its state and no share
    Then SUBROGATION_POSITION and RESIDUAL_TO_ROUTE are read as the guarantee claim state of TSD S3 T4 on the state property, and the three vocabularies are kept apart

  Scenario: AC4 The error set and the Idempotency-Key rule are fixed (new, D-RCV-60)
    Given the error section of the document
    When each declared answer is validated
    Then the operations declare 401, 403 with MSG-P4-002, 404, 409 on a state conflict, 422 with MSG-GEN-001 and 503
    Then the document maps MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P7-009 to the answers that carry them, keeps their legacy texts and adds no message identifier
    Then the create requires the Idempotency-Key header and a repeated key answers with the first result and stores no second row
    Then the patch declares no idempotency key, as TSD S3 T-A.2 API-S3-002 states
    Then an error answer carries the message identifier, the merge fields and the trace identifier only
    Then the message catalogue entry format is fixed once with the platform library stories and is not restated in the contract

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then a backward-compatible change keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a breaking change to a path, a required element, an error code or the answer raises major version 2 and v1 is never edited in place
    Then each consumer pins a published version and raises a change request rather than a private variant

  Scenario: AC6 The fake answers the document and every consumer runs the drift test (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the claim fake, the negotiation fake, the subrogation fake, the error fake, the composite route fake and the decision-record fake
    Then the claim fake answers a created claim and a patched claim with the two vocabularies and the share
    Then the error fake answers 403, 422 and 503 with their message identifiers and no personal data
    Then the composite route fake answers one hop for SCR-17 and the decision-record fake answers an accepted record and a failed write
    Then the drift test fails the build of any consumer whose request, answer or error does not match section 12

  Scenario: AC7 A consumer value no source names is published as a working read and the gap stays open (new, D-RCV-60)
    Given a consumer that needs the share type, the outcome vocabulary or the range element
    When the contract is validated against the sources
    Then the value is published as the working read of the assumption and carries its assumption tag
    Then the gap GAP-2730 and the assumption ASM-4529 stay open and no value is invented for them
    Then the document names the value as not specified in the source documents where no source gives it

  Scenario: AC8 Each business rule BR1 to BR8 is carried by a criterion and a test (new, D-RCV-60)
    Given the business rules of section 8
    When each rule is traced to the contract and to the criteria
    Then BR1, BR2, BR3 and BR7 are carried by AC1, BR4 by AC3, BR5 by AC2 and AC3, BR6 by AC2 and BR8 by AC5
    Then each rule has a test row in section 16
    Then an architecture rule with no contract surface is carried by a guardrail or boundary test

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given the claim with a current state under the GUARANTEE state of TSD S3 T4
    When a patch proposes a state change that the model does not allow from that state
    Then the answer is 409 on a state conflict, as declared in AC4
    Then the claim keeps its current state and no row is changed
    Then the document adds no message identifier for the refusal
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here, because **AC1 to AC4 of RWB-E4-018 are owned by RWB-S3-E4018-APP**, and every identifier, path element, field identifier and message is taken from the ownership rows, the TSD appendix or the legacy story character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The claim surface is exactly two operations on the service base: the create under right C with an idempotency key, and the patch under right U | DP-13; S3 ownership rows; TSD S3 T-A.1 API-S3-001 and API-S3-002 |
| BR2 | No read operation is published in v1; SCR-17 is composed by the gateway-bff composite route | GAP-2730; ASM-4533; DP-19 |
| BR3 | The negotiation is carried on the patch of the claim; no third operation is created for it | GAP-2728; ASM-4529 |
| BR4 | `state` carries the GUARANTEE state of TSD S3 T4 and `status` carries LOV-CLAIM-STATUS; the contract never merges or maps them | GAP-2729; ASM-4530 |
| BR5 | `subrogationShare` is published on the update and on a subrogation answer, and its name and type are the working read, because the legacy criterion records the share and no source names it | GAP-2730; ASM-4529 |
| BR6 | The approved range, the notice expiry and the package version travel as request context and are never columns of `rwb_guarantee` | GAP-2728; ASM-4529; DP-01 |
| BR7 | The contract declares the access right only; the check is the guard library's on capability area "Treatment and offer", performed through the rwb-access authorise check (DP-08) | TSD S3 T6.1; DP-08 |
| BR8 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |

Coverage: BR1, BR2, BR3 and BR7 are covered by AC1 and TC-S3-E4018-CON-01; BR4 by AC3 and TC-S3-E4018-CON-03; BR5 by AC2 and AC3, with TC-S3-E4018-CON-02 and TC-S3-E4018-CON-03; BR6 by AC2 and TC-S3-E4018-CON-02; BR8 by AC5 and TC-S3-E4018-CON-04. AC8 and TC-S3-E4018-CON-07 cover all eight rules as a single check.

**Where each rule lives in the target.** BR1 and BR7 are the operation table with its access column, and the guard is called by the application slice, not by the contract. BR2 is the negative rule of section 12.1 and the reason the composite route is named: the contract deliberately publishes no read, so no consumer builds against one. BR3 is the sentence that keeps the negotiation on the existing path instead of adding an operation the ownership rows do not give. BR4 is the two properties and the note that separates them, and it is the one place where a consumer could silently merge three vocabularies. BR5 is the one element whose name is not in a source, so it is published with the assumption tag and kept single. BR6 keeps the contract out of the schema, and BR8 is the compatibility section and the pinning rule.

### 9. State transitions

None at run time: a document and a schema have no state. Three vocabularies are fixed here and the runtime transitions behind them are specified by RWB-S3-E4018-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Claim answer | `PREPARING`, `FILED`, `DEFECT`, `PAID`, `REJECTED` | The `status` property, the values of LOV-CLAIM-STATUS |
| Claim answer | `CLAIM_PAID`, `CLAIM_PART_PAID`, `SUBROGATION_POSITION`, `RESIDUAL_TO_ROUTE` | The `state` property, members of the GUARANTEE state set of TSD S3 T4 |
| Create request | New | The `Idempotency-Key` was not presented before; a claim row may be written |
| Create request | Repeated | The key was presented before; the first answer is returned and nothing is stored |
| Patch request | Accepted | The negotiation outcome is inside the approved range carried on the request context |
| Patch request | Refused | The answer carries an error code with its message identifier and merge fields |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited in place |

The screen labels of SCR-17 — Not due, due, submitted, paid, refused — are the screen's own and are not a third vocabulary of this contract (GAP-2729; ASM-4530).

PATCH is the HTTP operation of the `Patch request` rows, and `SUBROGATION_POSITION` is a member of the GUARANTEE `state` set, not of LOV-CLAIM-STATUS. The closed list LOV-CLAIM-STATUS keeps its five values (GAP-2729; ASM-4530).

The empty, loading, error and no-access states of SCR-17 are not specified in the source documents (DOR-RWB-S3-E4018-CON-10); this contract declares no screen state.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the three schemas, the error table and the fakes |
| The service team of rwb-guarantee | Consumes the contract, pins the version and raises a change request rather than a private variant |
| The rwb-guarantee tech lead | Confirms that the two operations are the ones the application slice and the claim-preparation slices build |
| The solution architect | Confirms the negative rules — no read, no third operation, no table — against the S3 ownership rows and TSD S3 T-A.1 |
| The rwb-case owner (P3) | Confirms that the case status and the case-level keeping of the TCG share are the parent's, and that the contract carries neither |
| The platform edge owner | Confirms the composite route that serves SCR-17 without a read operation of this service |
| The wave 3 integration harness owner | Confirms the fake set is enough to prove the cross-service path |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes operation entries, three element schemas, codes, message identifiers and examples; no customer, account or case value appears. BR Field ID: None |
| Request context facts published | The approved range, the notice expiry and the rule package version on the request; all of them context-only. BR Field ID: Not specified in the source documents (DOR-RWB-S3-E4018-CON-7) |
| Stored fields referenced | The claim fields DF-TRT-015 to DF-TRT-022 and the standard columns of T3.0, referenced through the elements and declared by RWB-S3-E4018-APP, not redefined here. BR Field ID: DF-TRT-015 to DF-TRT-022 |
| Field identifiers | The eight claim fields carry DF-TRT-015 to DF-TRT-022; `state` and `status` carry the T3.0 column and DF-TRT-022; `subrogationShare` carries no field identifier, because no source gives it one (GAP-2730; ASM-4529). BR Field ID: as stated in this row; the identifier for `subrogationShare` is Not specified in the source documents (DOR-RWB-S3-E4018-CON-7) |
| Personal data | None. The examples carry amounts, dates, codes and a share, and the actor and trace references are identifiers, never names. P2 fields flagged as personal data: Not specified in the source documents (DOR-RWB-S3-E4018-CON-11). BR Field ID: None |
| Tables published | None. The contract declares no table and no column; `guarantee_claim` is the application slice's and `decision_record` is the library's (DP-01, DP-03). The guarantee, the guarantor pursuit and the subrogation position are entity groups of schema `rwb_guarantee` named after Arch v5 slide 18 ('TCG and insurance claims, guarantor notices and pursuit'); the physical table set is fixed by the S3 DB story, with the Ownership Map rows added in the same change (GAP-1721). BR Field ID: None |
| ACE data | None, and no `v_ace_*` view is named as a source of the contract (DP-05). BR Field ID: None |
| Reference data read | LOV-CLAIM-STATUS (TSD S3 T3.2) for `status` and the GUARANTEE state of TSD S3 T4 for `state`; the parameters are Not specified in the source documents (DOR-RWB-S3-E4018-CON-20), and the reference-data contract is DP-06 and DP-07. BR Field ID: None |

The one place where the contract could leak a value is the share: the document therefore fixes that `subrogationShare` is a property of the update and of the subrogation answer, that it is never an enumeration and never a default, and that no example value is presented as a value in force.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). The contract declares the claim surface only: the claim preparation, the filing and the notice are other slices that use the same two operations.

| Method | Path | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest` | `GuaranteeClaim` | Treatment and offer, right C | `Idempotency-Key` header required; a repeat returns the first answer |
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` | `GuaranteeClaim` | Treatment and offer, right U | Not applicable, as TSD S3 T-A.2 API-S3-002 states |

Two operations and no more: the S3 ownership rows give the service exactly these two, so the contract publishes no read, no delete and no separate negotiation endpoint, and the negotiation travels on the patch (GAP-2730; ASM-4533). The error codes are those of TSD S3 T-A.2 — 401, 403, 404, 409, 422, 503 — and the reference to the claim is the path parameter, never a body field. Whether a read operation is added to the service later, and which owner decides it, are Not specified in the source documents (GAP-2730; ASM-4533).

#### 12.2 REST operations consumed

None. The contract declares the surface and calls no service: the case, its status, the party reference and the approved range arrive on the stage signal that the parent `CaseWorkflow` forwards, and the decision record is an in-process call of RWB-PLT-E1027-CON (DP-03; ASM-4529).

#### 12.3 Events published

None. The topic of the service is `rwb.guarantee.events.v1` with event names `rwb.guarantee.<Event>.v1` (DP-14), and the S3 ownership rows give the service no event. The contract publishes no event schema and declares no outbox row.

#### 12.4 Events consumed

None. The contract declares no subscription. The payment that triggers a subrogation reaches the stage as a signal the parent forwards, and the event that would carry it is named by no source (GAP-2728; ASM-4531).

#### 12.5 Workflows and activities

None. The contract declares no workflow and no activity. It states only that the patch is written inside an activity of `GuaranteeClaimWorkflow` on the owner's own task queue and that the decision record is called from that activity, so a replay reuses the recorded decision; the workflow itself is RWB-S3-E4018-APP's (DP-03).

#### 12.6 Schedules

None. The contract declares no Temporal Schedule and no legacy Quartz job; the ownership rows give the service no job, and the claim deadline and the notice expiry are durable timers inside the workflow and not part of the published surface.

#### 12.7 Tables owned

None. The contract declares no table, no column and no key. It states the negative rules that matter: the approved range, the notice expiry, the negotiation outcome and the package version have no place in `rwb_guarantee`, because no source gives them one and storing them would copy another owner's facts into this schema; and `guarantee_claim` stops at DF-TRT-022 today, so `subrogationShare` is published as an element and its column is the application slice's (GAP-2728, GAP-2730; ASM-4529, ASM-4535; DP-01). `guarantee_claim` is RWB-S3-E4018-APP's business table and `decision_record` is the library object of RWB-PLT-E1027-CON; `decision_log_entry` is P7's ledger and is named here only.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Claim fake | `POST /cases/{caseId}/guarantee-claims` and `PATCH /guarantee-claims/{claimId}` | A created claim with `status` PREPARING and `state` of the GUARANTEE set; a patched claim with the outcome written |
| Negotiation fake | The patch of the negotiation | An outcome inside the approved range; an outcome outside it with 422 and the field |
| Subrogation fake | R-GUA-23 and R-GUA-24 answers | A claim at `CLAIM_PAID` and one at `CLAIM_PART_PAID`, each answering `SUBROGATION_POSITION` with `subrogationShare`; a refusal answering `RESIDUAL_TO_ROUTE` with no share |
| Repeated-key fake | The idempotency rule of the create | The first answer returned for a repeated `Idempotency-Key`, with no second row and no second record |
| Error fake | The error table | 403 with MSG-P4-002, 404, 409 on a state conflict, 422 with MSG-GEN-001, 503 with MSG-P7-003, each with its identifier, its merge fields and a trace identifier |
| Composite route fake and decision-record fake | RWB-PLT-N001-CON and RWB-PLT-E1027-CON | One hop for SCR-17 joining the case read with the claim the stage holds; an accepted record with an entry reference and a failed write with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consumer rather than as a surprise at run time. The route and record fakes are published by their own stories and are referenced here, not redeclared.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operation entries on `/api/recovery/guarantee/v1` | 0 | OpenAPI 3.1 fragment; one hop to the service, 2 s timeout; no read operation |
| Kafka | 0 event schemas | 0 | The service topic is named; this contract declares no event |
| Temporal | 0 | 0 | The contract states the write happens in an activity and declares no workflow |
| File | 0 | 0 | No file crosses the contract; INT-29 is not a file path of this service |

### 13. Solution plan

**Package.** Contract artefact of rwb-guarantee: the OpenAPI fragment and the three element schemas in `th.co.scb.ace.workbench.recovery.guarantee.api`, the error table and the compatibility note in the contract document, and the fake set as a test asset. Service base `/api/recovery/guarantee/v1`, schema `rwb_guarantee`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery`. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2730; ASM-4533).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 enters the contract as one statement — the patch is a state change whose record is written in the caller's transaction — and the H dependency sits on the application slice, which calls the library. DP-05 is the negative rule of section 11: no `v_ace_*` view is a source of the contract, because the legacy customer read is dropped (ASM-4532). DP-13 is the base of the two operations and the reason the legacy base appears nowhere in the document. DP-19 is the route that serves SCR-17, named here because no read operation is published for the screen to call.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimOpenApi` | OpenAPI 3.1 fragment | The two operation entries, their parameters, their errors and their access declaration |
| `GuaranteeClaimRequestSchema` | Request schema | `claimType`, `claimDeadline`, `claimedAmount`, `filedAt` |
| `GuaranteeClaimUpdateSchema` | Request schema | `paidAmount`, `status`, `state`, the negotiation outcome, the outcome date, `subrogationShare`, with the stored and context-only note on each |
| `GuaranteeClaimSchema` | Answer schema | The eight claim fields, `state`, `status`, `subrogationShare` and the standard version and timestamps |
| `ErrorCatalogue` | Document table | The status codes, the message identifiers, the legacy texts and the merge fields |
| `CompatibilityNote` | Document section | The negative rules, the compatible versus breaking rule and the pinning rule |
| `ClaimFakeSet` | Test asset | The six fakes of section 12.8 and the drift test every consumer runs |

**Database.** None. The contract creates no table, adds no column and declares no key; the negative rules of section 12.7 are the deliverable, and a review that finds a range, an outcome or an expiry column in `rwb_guarantee` fails this story.

**Configuration and reference data.** The contract fixes no business value. The approved range, the notice expiry and the scheme values are values in force in the owner's data; the only values in the document are examples, and they are marked as examples. Capability area "Treatment and offer" and rights C and U are read from rwb-access through the guard library, which the application slice calls.

**Build steps**

1. Write the two operation entries, their access rights and the idempotency rule; lint that no third or read operation appears (AC1).
2. Write `GuaranteeClaimRequest` and `GuaranteeClaimUpdate` and the stored-versus-context note for every property (AC2).
3. Write `GuaranteeClaim` with `state`, `status` and `subrogationShare` and the note that separates the vocabularies (AC3).
4. Write the error table with the four identifiers and their texts, and the repeated-key rule; validate one answer per code (AC4).
5. Write the compatibility note, the negative rules and the pinning rule (AC5).
6. Generate the six fakes and the drift test; wire the drift test into the build of RWB-S3-E4018-APP, the claim-preparation slices, the gateway route and the wave 3 harness (AC6).
7. Publish v1 and record the pinned version of each consumer.

**Feature flag.** `rwb.guarantee.claim-contract`.

**Done when.** The document and the three schemas validate, the operation lint passes with exactly two entries and no read, the error table matches the four message identifiers and texts, the six fakes answer every example including the two subrogation answers and the repeated key, the drift test is green on the build of this story and on the build of the application slice, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, the negotiation outcome among them | Enter {field}. | 422, with the field name |
| MSG-P4-002 | The role does not hold right C or right U | You cannot {action} here. Your role does not include it. | 403, from the guard library |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, from RWB-PLT-E1027-CON |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. | 422, from RWB-PLT-E1027-CON, with the field |

The first three texts are the legacy texts of RWB-E4-018 carried unchanged, and MSG-P7-009 is the library's; the contract adds no message identifier and renames none. The entry format of each message in a published catalogue is Not specified in the source documents and is published as the working read (GAP-2730; ASM-4533). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. SCR-17 Guarantee claim is reached through the gateway-bff composite route (DP-19), and the contract fixes only the answers that screen consumes: the claim with its `state`, its `status` and its `subrogationShare` after a patch. Because the service publishes no read operation, the route composes the case read of rwb-case with the claim the stage holds, and that composition is the edge contract's (GAP-2730; ASM-4533). The screen states — Not due, due, submitted, paid, refused — are the screen's own and are named in section 9 only to keep the three vocabularies apart. The states empty, loading, error and no access are Not specified in the source documents (CG-ALL-8935).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S3-E4018-CON-01 | AC1 | Contract | The two operation entries linted against the S3 ownership rows and TSD S3 T-A.1; the access rights; the negative rules for a third operation and for a read |
| TC-S3-E4018-CON-02 | AC2 | Contract | `GuaranteeClaimRequest` and `GuaranteeClaimUpdate` validated; the stored and context-only note on every property; the absence of a column and a field identifier for the range, the outcome and the expiry; a personal-data scan of the examples |
| TC-S3-E4018-CON-03 | AC3 | Contract | One subrogation answer and one refusal answer validated: the eight claim fields, `state`, `status`, `subrogationShare`, the note that separates the vocabularies and the standard columns |
| TC-S3-E4018-CON-04 | AC4, AC5 | Contract | One answer per error code with its identifier and merge fields; the required `Idempotency-Key` and the repeat answer; one compatible and one breaking change against the registry in BACKWARD mode |
| TC-S3-E4018-CON-05 | AC6 | Component | The six fakes answering every example, including the two subrogation answers, the repeated key, the 403 and the 503; the drift test failing on a consumer that drifts |
| TC-S3-E4018-CON-06 | AC7 | Contract | A consumer request needing the share type, the outcome vocabulary or the range element; the working-read tag on each value; the open gap GAP-2730 and ASM-4529 |
| TC-S3-E4018-CON-07 | AC8 | Contract | Each rule BR1 to BR8 traced to its criterion and its test row; the architecture rule checked by the guardrail or boundary test |
| TC-S3-E4018-CON-08 | AC9 | Contract | A patch proposing a state the model does not allow from the current state; the 409 state-conflict answer; the claim row unchanged |

The legacy test set of RWB-E4-018 — TC-E4-018-01 to TC-E4-018-06 — is carried by RWB-S3-E4018-APP and by the wave 3 integration harness, and no legacy id is renumbered here: these five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the approved range, the notice expiry and the scheme values are values in force in the owner's data, and the only values in the document are examples, marked as examples.
- No personal data in a schema, an example, a fake or a log: the examples carry amounts, dates, codes and a share, and the scan fails the build otherwise.
- No table, no column and no key in the contract: the range, the outcome and the expiry stay out of `rwb_guarantee` (DP-01; ASM-4529).
- No third operation and no read operation: the lint of X1 fails any document that publishes one.
- No merged state vocabulary: `state` and `status` are two properties and the contract maps neither.
- No event and no outbox row of the contract's own: the service topic is named and the ownership rows give it no event.
- No REST call and no workflow in the contract: the record is written in process inside an activity and the case status stays the parent's.
- No ACE view: the contract names no `v_ace_*` view as a source, because the legacy customer read is dropped (DP-05; ASM-4532).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and a superseded marking.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-005 | A guarantor who answers a demand enters the same treatment paths as a borrower | Epic 4 BRD, S3 module | FEAT-GUA-06 | D6.5, D6.6 Guarantee claim | BR1, BR3, BR4 | TC-S3-E4018-CON-01, TC-S3-E4018-CON-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4018-APP | App development | H consumer: implements the two operations, the range check, the two subrogation outcomes and the record write against this contract and its fakes; owner of the legacy acceptance criteria |
| The claim-preparation slices of FEAT-GUA-01, FEAT-GUA-02 and FEAT-GUA-03 | App development | Consumer of the create and of the `status` vocabulary; the filing and the balance claim are theirs |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library the application slice calls in the caller's transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-17 without a read operation of this service |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status, the party reference and the case-level keeping of the TCG share; the contract carries none of them |
| rwb-source-data (P1) | Service, wave 1 | Owns the ACE views; the contract names none of them (DP-05) |
| rwb-payment (P8) | Service, wave 2 | Produces the guarantee payment that triggers a subrogation; no event of it is declared here |
| Wave 3 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners, with the `-ITG` copies of the six test cases |

Open decision DL10 (the Thai texts of the error and message catalogue, see section 19) is still open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 19. Out of scope

- The behaviour behind the two operations — the range check, the two subrogation outcomes, the refusal and the record write: RWB-S3-E4018-APP.
- The claim preparation, the checklist and the filing of FEAT-GUA-01 and FEAT-GUA-02, and the balance claim of FEAT-GUA-03: their own slices.
- The demand to the guarantor and co-borrowers, its template and its expiry: the FEAT-GUA-05 slice.
- Closing the guarantee and the case under R-GUA-26 and returning the residual under R-GUA-25: the FEAT-GUA-07 slice.
- The insurance claim on a collateral event: the FEAT-GUA-08 slice.
- The table `guarantee_claim`, its columns and the `subrogationShare` column: RWB-S3-E4018-APP and the per-service Flyway sequence (DP-01).
- The decision-record library, its `MANDATORY` transaction, its chain and its envelope: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The gateway-bff composite route, the screen field list of SCR-17 and the read the screen needs: RWB-PLT-N001-CON and the screen owners (GAP-2730; ASM-4533).
- The case, its status, its party record and the case-level keeping of the TCG share: rwb-case (P3).
- The GUA rule package, its authoring, its promotion and its version labels: P7 rwb-decision and the service-template runtime.
- The ACE views and the customer, account and payment data behind them: rwb-source-data (P1).
- The event that carries a guarantee payment and any subscription to it: the payment story and the event catalogue.
- The error and message catalogue of the platform, the Thai texts and the incident route: the platform library stories (DL10).
- The cross-service proof of the claim and the `-ITG` copies of the legacy test set: the wave 3 integration harness.
