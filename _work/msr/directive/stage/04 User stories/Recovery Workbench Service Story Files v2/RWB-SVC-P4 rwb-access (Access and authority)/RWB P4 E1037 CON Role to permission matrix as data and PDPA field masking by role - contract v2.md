# RWB-P4-E1037-CON Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E1-037 for rwb-access — the published access and masking contract of the service: the matrix and masking loads, their approval, the two reads, the policy event and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-E1037-CON-L49, X20 RWB-P4-E1037-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (40 resolved, 67 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1037-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized in the story; the squad sizes it at refinement |
| Contract version | API Specification v5 rwb-access.yaml (x-module: P4), path base /api/recovery/access/v1 |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | rwb-case (RWB-P3) reference-data load of the parameters and LOV only; the permission matrix and DoA loads stay with rwb-access (P4) |
| Closed lists | LOV-ROLE-CLASS and LOV-SCOPE are closed lists per Reference Data v5; the roleClass and defaultScope enums in rwb-access.yaml stay |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P4-E1037-CON-14) |
| Integration dependencies | rwb-source-data (P1) data product contract for the masked read of v_ace_customer and v_ace_contact; the suite asserts the masking through P4 and P1 |
| Cache and failure rule | Cached permission and masking data is refreshed on AccessPolicyChanged and DoaLimitChanged; the cache lifetime is Not specified in the source documents (GAP-0161); when rwb-access does not answer the service refuses the action (deny by default, fail closed) |
| Partner roles | Partner role rows stay with P4; their codes, letters and default scope are Not specified in the source documents (GAP-0164); the partner user record, the instruction and the result stay with S9, which calls POST /authorise with its partner role code and holds the user-to-role link (GAP-0164) |
| OCR and field text | The classification of document_text.text_content and document_field.field_value is left to the data steward (GAP-0262); the OCR text and the field value never appear in an event, a workflow input or a log, and the page id appears only in a log |
| Permission matrix count | The legacy count of 756 rows is taken from the approved file; the role count and roster size are Not specified in the source documents (GAP-0778) |
| Masking-policy read | GET /api/recovery/access/v1/masking-policies (Reference data R); the policy decides clear or masked, and the data owner supplies the masked or last-four value (GAP-0778, GAP-1405) |
| Policy event | The payload of rwb.access.AccessPolicyChanged.v1 is Not specified in the source documents (GAP-1569) |
| Baseline and test fakes | The rwb_access baseline and the rwb-case case contract fake are Not specified in the source documents (GAP-0778) |
| Library artefact | Platform coordinate with major version 1; the coordinate is Not specified in the source documents (GAP-1404) |
| Cache time to live | The value and the parameter key are Not specified in the source documents (GAP-1404) |
| Authorise and masking payloads | The payload shapes of POST /authorise and of the masking-policy read are Not specified in the source documents (GAP-1404) |
| Interfaces and annotation | The guard, scope guard and mask applier are published with their types, and the personal-data annotation with its field-id attribute; the types are Not specified in the source documents (GAP-1405) |
| Access audit record | The audit record shape is Not specified in the source documents (GAP-1405) |
| Access-owner failure | Every access-owner failure maps to 503 with no business data (GAP-1405) |
| Masking answer | Row shape and field names are Not specified in the source documents (GAP-0915) |
| Authorise envelope | The request and answer shapes of POST /authorise are Not specified in the source documents (GAP-0925) |
| External dependencies | Platform library publishes the guard and the annotations at major version 1; artefact coordinates Not specified in the source documents (GAP-1404); the masker is the platform library |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-003, FR-P4-005, FR-P4-006, FR-P4-008, FR-P4-009, FR-P4-010, FR-P4-011, FR-P4-012, FR-P4-013, FR-P4-014, FR-P4-015, FR-P4-016, FR-P4-017, FR-P4-018, FR-P4-019, FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027, FR-P4-032, FR-P4-033, FR-P4-038) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner of rwb-access**, I want **the published access and masking contract of this service — the two load operations, the approve operation, the matrix and masking-policy reads, the approver rule, the five data objects, the error vocabulary, `rwb.access.AccessPolicyChanged.v1` and the fakes**, so that **its app stories and every service that authorises or masks build and test against one frozen contract from Day 1, while the policy rows stay in `rwb_access` and no consumer invents a shape of its own**.

The document is fixed before it is code. It fixes what a caller sends and what it receives on four operations, which fields of `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` appear in an answer, which status and message id each failure returns, when the policy event is published and what it may not carry, and which fakes let a consumer build while the access owner is still being built. This contract has no screen: the empty, loading, error and no-access states of P3 SCR-43 and SCR-47 belong to the P3 screen stories and are not restated here. Open decisions DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) stay open; each carries the assumptions listed, which the directive confirms.

**The division of this legacy key is fixed.** The guard, the masker and the `@PersonalData` annotation that every service binds are the platform library contract **RWB-PLT-E1037-CON** and its app story **RWB-PLT-E1037-APP**; this story publishes the **data-side contract** of `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` — the objects, their versions, the two loads and their approval, the two reads and the policy event — and implements none of the guard. RWB-P4-E1022-APP owns the sign-in and the session, RWB-P4-E1039-APP owns the access log and break-glass, and RWB-ITG-E1037-ITG owns the end-to-end proof. The permission matrix as data, the masking rules and the load and approve path are the deliverable of **RWB-P4-E1037-APP**, which also owns the thirteen legacy criteria; this story owns no legacy criterion, publishes new criteria only, and names the owner of the legacy criteria and of the fifteen legacy test cases of its key in section 18.

### 2. Business rationale

In the monolith the matrix, the masking rules, the scope rule and the guard sat in one package over one database: `recovery.access.matrix` read `permission`, `masking_rule`, `role` and `delegation_limit` in the same connection and answered a scope filter, a masked DTO and an `isUnmasked` call. There was one shape because there was one process. In the 19-service target the policy rows stay with one owner (DP-01) and the enforcement moves into a platform library that every service binds, so a consumer now depends on two published artefacts and must find in each exactly what it needs: the library gives it the guard, the masker and the annotation; the access owner gives it the policy data, the versions and the approval trail.

That is the gap this story closes. Without a published data-side contract a consumer guesses what `GET /masking-policies` returns, whether a permission answer carries letters or a set of booleans, which approver approves a masking version, and what a 403 means on the load path — and the guesses drift at the first policy change. With it, a consumer compiles and tests from Day 1 against fakes, and cannot quietly read a P4 table because the contract gives it no connection to do so. Architecture v5 slide 14 fixes the operations the contract publishes — `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `/masking-policies` — and the two events `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`; slide 41 keeps Recovery roles as data, scope, masking policy, the DoA table and the access log in `rwb_access`; and ADR-010 keeps the clear identity number inside ACE with no token store. The sign-in permission read is `GET /me/permissions`; API Specification v4 names it `GET /me/session`, and this contract maps `/me/session` to `GET /me/permissions` (GAP-0160).

**The division, in one paragraph.** The guard, the masker and the `@PersonalData` annotation, with the scope descriptor and the fakes that every service binds, are the artefact of **RWB-PLT-E1037-CON**; this story publishes the data-side contract of **`role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit`** — the two loads and their approval with the approver role from the parameter, the matrix read, the masking-policy read, the versions in force and the policy event — and the two artefacts meet at one point only: the masker reads the rules this contract publishes, and the guard reads the letters of the permission rows it publishes.

The values the criteria use are the legacy values unchanged: matrix version `PM-2026.11`, the next version `PM-2026.12` with 756 permission rows, masking versions `MASK-SIT-01` and `MASK-2026.11`, the role codes RW-REFADM, RW-SECADM, RW-COMPLY, RW-LEGAL, RW-CASEOWN, RW-PHONECOL and RW-COE, the field ids DF-ACE-073 `id_no_masked`, DF-ACE-074 `id_no_last4`, DF-ACE-059 `date_of_birth`, DF-ACE-078 `contact_value` and DF-ACE-079 `contact_value_masked`, the area `QUEUE_AND_ALLOCATION`, the letters C, R, U, D and A, the scopes OWN, TEAM, ALL and Placed cases (the four Key tab values; whether a region predicate is added is decided in the P4 and P3 design, GAP-0168), and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P1-002, MSG-P7-002, MSG-P7-003, MSG-GEN-004 and MSG-GEN-006. It supports REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011.

Two open points are carried as placeholders and register rows: the path and the right of the masking-policy operation, which Arch v5 slide 14 names without a path in the API Specification v5 or TSD P4 v3 appendix T-A — Not specified in the source documents (GAP-0779; ASM-1416) — and the payload of `rwb.access.AccessPolicyChanged.v1`, which no source fixes — Not specified in the source documents (GAP-0779; ASM-1417).

The request attributes of `POST /api/recovery/access/v1/authorise`, their types and the matrix version label in force at the release date are Not specified in the source documents (GAP-0990).

### 3. Preconditions

- Wave 1 and lane `CG-W1`: the contract is Day 1 by rule (Template and Rules §R5.7) and has no build dependency. `H`, `C`, `I` and `X` read None.
- Wave 1 readers build against the published authorise contract `C RWB-P4-E1037-CON` and the guard library `H RWB-PLT-E1037-CON` under DP-08; this contract's own rows stay None because it restates neither.
- Architecture v5 slide 14 fixes the access operations and the two events: `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions`, `GET /api/recovery/access/v1/doa-limits`, `/api/recovery/access/v1/masking-policies`, and `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`.
- Architecture v5 slide 41 keeps `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` with P4 rwb-access; the Ownership Map gives P4 the paths `GET /api/recovery/access/v1/admin/roles` and `GET /api/recovery/access/v1/admin/access-log` and no path for the load, approve or masking-policy operation.
- API Specification v5 declares `x-module: P4` for `/admin/reference-loads`, `/admin/reference-loads/{loadId}/approve` and `/admin/roles`, and TSD P4 v3 appendix T-A names the same operations as API-P4-005, API-P4-006 and API-P4-007.
- ADR-010 and D-RCV-35 U1 fix the identity boundary the contract restates: the clear identity number never leaves ACE, there is no token store, and `id_no_last4` is the clearest identity value any role can receive.
- Parameters `rwb.refload.approver.permission=RW-SECADM` and `rwb.refload.approver.masking_rule=RW-COMPLY` are in the catalog of rwb-case (RWB-E1-042, DP-06), and `LOV-CAPABILITY`, `LOV-SCOPE` and `LOV-ROLE-CLASS` are in the reference data of rwb-case (DP-07).
- The decision record is written through the local decision-record library of RWB-PLT-E1027-CON with decision code `AC-VERS` for a version approval (DP-03).
- The `rwb_access` baseline of RWB-PLT-E1044-CON holds the five tables and their dictionary rows; the baseline migration is the service template's, because WP B-P4-01 carries no DB story for this legacy key (DP-15, ASM-1418).
- The masking-shape function `recovery.ace_mask_value` and the `recovery.v_ace_*` columns are the ACE team's and RWB-P1-E1069-APP's; the contract names their field ids and owns no value.
- The six non-human actors SY-CASEWF, SY-RULES, SY-RECOVERY, SY-OCR, SY-DECLOG and SY-AGENT are resolved through `POST /api/recovery/access/v1/authorise` with their SY role code and their managed identity as the subject; the credential type is left to the P4 contract story (GAP-0166).
- The masking-shape function stays in the recovery view schema with the views, the masking policy rows stay in `rwb_access` (P4), and `rwb-source-data` applies the mask in the view and in its responses (GAP-0248).
- Personal-field reads are logged through the ACE Common PII logging path to the SOC (INT-34); the Recovery business-event topics are separate and carry no personal data (GAP-0264).
- A partner user is created and ended by the S9 `rwb-partner` administrator; the roles it holds are P4 role rows granted by the P4 role owner, and both actions are written to the access log (GAP-2041).
- The screen response level is owned by RWB-PLT-EDGE, and the partner gateway is read as RWB-PLT-EDGE with S9 `rwb-partner` behind it (GAP-2063).
- The access log row records the version the owning service applied at the time of the event; the registry in rwb-decision stays the source of each version and its effective date (GAP-2076).
- No approval stops the build: the contract is Draft (realignment v1) and is frozen when the consumers pass their contract tests (R-UNI-38 applies to the version, not to the document).

### 4. Flow

1. Fix the four operations on the base `/api/recovery/access/v1`: the matrix load, the approve, the matrix read and the masking-policy read, each with its method, path, purpose, access right, request, answer and idempotency.
2. Fix the load shape: a multipart body with the file, the `table` value ("permission" or "masking_rule") and `validFrom`, answered 201 with the load id, the table, the `validFrom`, the status "Loaded" and the row count.
3. Fix the approve shape: no body, answered 200 with the version Approved; the approver role is the one the parameter names for the table, the caller may not be the loader, and the decision code is `AC-VERS`.
4. Fix the matrix read: for each role in force, its role code, its permission rows with the capability area and the letters, its default scope, the matrix version and the conflict version of its pairs, and no person.
5. Fix the masking-policy read: for each rule in force, the field id, the role code, `unmasked`, the masking version, `valid_from` and `valid_to`, and the statement that a field with no rule is masked and that a rule may not name the clear identity number.
6. Fix the error vocabulary: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-GEN-004 and MSG-P7-002, 422 with MSG-P1-002 and the failed check in the detail, 503 with MSG-GEN-006 and MSG-P7-003, all as RFC 9457 problem responses.
7. Fix the event: `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, published on the approval of a matrix or a masking version, carrying the version label, the change kind and the effective date, and no personal value.
8. Fix the negative statements: the contract owns no guard and no masker (those are RWB-PLT-E1037-CON), holds no session and no password (RWB-P4-E1022-APP), keeps no token (ADR-010) and owns no partner table (S9).
9. Publish the fakes of section 12.8 and wire the contract test into the build of the app stories of this service and of the consumers.
10. Publish the contract document with the nine tables of section 12 and record its version and its compatibility rule.
11. The separation-of-duty check path, its payloads, the role-conflict operation paths, their rights and the conflictVersion field name are Not specified in the source documents (GAP-0796); this conflicts with the four-operation count in item 1 and AC1 and is flagged for the next revision.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer asks for a path the contract does not publish | The answer is 404 with MSG-P4-003 and no shape is guessed | MSG-P4-003 | AC1 |
| X2 | A matrix file misses a role, repeats a role and area, or holds a letter outside C, R, U, D, A and "-" | The load is refused in full with the failed check named and the version in force stays | MSG-P1-002 | AC2 |
| X3 | The caller of approve is not the role the parameter names for the table | Refused with 403 before the change | MSG-P4-002 | AC2 |
| X4 | The caller of approve is the person who loaded the version | Refused as a conflict and the version stays Loaded | MSG-P7-002 | AC2 |
| X5 | The decision record cannot be written | The approval does not take effect and nothing is published | MSG-P7-003 | AC2, AC4 |
| X6 | A masking rule names the clear identity number, or a field id that is not personal, or an unknown role code | The whole masking version is refused and the rule is named | MSG-P1-002 | AC3 |
| X7 | A consumer reads the matrix with no Platform administration R, or the masking rules with no Reference data R | Refused with 403 and the right named; a caller with no Workbench role gets 401 | MSG-P4-002; MSG-P4-001 | AC3, AC6 |
| X8 | A consumer treats the contract as the guard or the masker | The contract test fails: the guard, the masker and the annotation are RWB-PLT-E1037-CON's | None | AC5 |
| X9 | A consumer waits for a payload field the contract does not fix | The build fails the contract test rather than inventing the field | None | AC1, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; the contract refers to the parameter, reference-data, decision-record and library artefacts by name only |
| Negotiable | The payload details of the policy event and the right of the masking-policy read are agreed at the contract freeze; the four operations, the five objects, the approver rule and the vocabulary are fixed by the sources |
| Valuable | Unblocks the app stories of this service and every consumer that authorises or masks, from Day 1, against one frozen contract and its fakes |
| Estimable | Four operations, two load shapes, one approve shape, two reads, one event, one error vocabulary and six fakes |
| Small | Fits two weeks with its contract tests |
| Testable | Every criterion below is a contract test that the build of this service and of a consumer runs |

### 7. Acceptance criteria

```gherkin
Feature: The access and masking contract of rwb-access

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given permission matrix version "PM-2026.11" is in force and masking version "MASK-SIT-01" is in force
    Given RW-CASEOWN holds "R" in Queue and allocation and RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11"
    Given the parameter "rwb.refload.approver.permission" is "RW-SECADM" and "rwb.refload.approver.masking_rule" is "RW-COMPLY"

  Scenario: AC1 The contract is published and the five data objects are fixed (new, D-RCV-60)
    Given the contract document of RWB-P4-E1037-CON is published as version 1 with the nine tables of section 12
    When a consumer reads it to build an authorise or a masking call
    Then it names the four operations of section 12.1 with their method, path, access right, request, answer and idempotency, all on the base /api/recovery/access/v1
    Then it names `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` with their field ids of the dictionary and their owner P4 rwb-access
    Then it names the matrix version and the masking version in every answer that carries a policy row, and the conflict version of a role pair
    Then no answer carries a person, a user identity of a named individual or an entitlement of a person
    Then a consumer that asks for a path the document does not publish is answered 404 with MSG-P4-003 and the shape stays unpublished

  Scenario: AC2 The two loads and the approve operation are fixed (new, D-RCV-60)
    Given a multipart body with a matrix file, table "permission" and validFrom "2026-12-01"
    When a caller holding Reference data C posts it to /api/recovery/access/v1/admin/reference-loads
    Then the answer is 201 with the load id, table "permission", validFrom "2026-12-01", status "Loaded" and the row count of the file
    Then a file that fails a check is answered 422 with MSG-P1-002 and the failed check in the detail, and no row of it is stored
    Then a caller without Reference data C is answered 403 with MSG-P4-002, and a repeated Idempotency-Key returns the first answer
    When a caller posts to /api/recovery/access/v1/admin/reference-loads/{loadId}/approve with no body
    Then the answer is 200 with the version Approved, the effective date and one decision record entry with decision code "AC-VERS" through RWB-PLT-E1027-CON
    Then a caller who does not hold the approver role the parameter names for the table is answered 403 with MSG-P4-002
    Then a caller who loaded the version is answered 409 with MSG-P7-002, a load that is not Loaded is answered 409 with MSG-GEN-004, and an unknown load is answered 404 with MSG-P4-003
    Then an approval whose decision record cannot be written is answered 503 with MSG-P7-003 and the version stays Loaded

  Scenario: AC3 The masking-policy read and the masked-versus-clear rule are fixed (new, D-RCV-60)
    Given masking version "MASK-SIT-01" in which only RW-CASEOWN may see DF-ACE-078 in clear, and no rule covers DF-ACE-059
    When a consumer holding Reference data R calls GET /api/recovery/access/v1/masking-policies for the fields and roles of its session
    Then the answer carries, for each rule in force, the field id, the role code, "unmasked", the masking version, "validFrom" and "validTo"
    Then the rule for RW-CASEOWN and DF-ACE-078 answers unmasked true and the field for DF-ACE-059 answers no rule
    Then the document states that a field with no rule is masked, that a masked field is filled from the masked view column or the last-four value, and that the clearest value a rule may name is id_no_last4
    Then a masking load whose rule names the clear identity number, a field id that is not personal or an unknown role code is refused whole with MSG-P1-002 and the rule named
    Then a caller without Reference data R is answered 403 with MSG-P4-002 and a caller with no Workbench role 401 with MSG-P4-001

  Scenario: AC4 The policy event is fixed (new, D-RCV-60)
    Given a matrix version "PM-2026.12" or a masking version whose approval commits
    When the approval transaction commits
    Then one event rwb.access.AccessPolicyChanged.v1 is published on rwb.access.events.v1 with the change kind, the version label, the effective date and the approver reference
    Then the event carries no field value, no person, no case id and no permission letter of a role
    Then a repeated delivery of the event changes nothing in a consumer that records it in its inbox
    Then an approval whose decision record cannot be written publishes no event, and the contract states that the two facts are one transaction
    Then no other event name is published by this service: rwb.access.DoALimitChanged.v1 belongs to the DoA story of the same service

  Scenario: AC5 The division from the platform library contract is fixed (new, D-RCV-60)
    Given the published contract of RWB-P4-E1037-CON and the published contract of RWB-PLT-E1037-CON
    When a consumer reads both to build one authorise call and one masked field
    Then the guard, the masker, the scope descriptor and the @PersonalData annotation are found only in RWB-PLT-E1037-CON, with their fakes
    Then the data of role, permission, masking_rule, role_conflict and delegation_limit, the two loads, the approve, the two reads and the policy event are found only in this contract
    Then this contract holds no session, no password and no token: the session is RWB-P4-E1022-APP's and the token store does not exist (ADR-010)
    Then this contract owns no partner table: partner, partner_user and partner_instruction are S9 rwb-partner's
    Then a consumer that expects a guard or a masker here fails the contract test, and one that expects a policy row there fails the library test

  Scenario: AC6 The error vocabulary, the default deny and the fakes are fixed (new, D-RCV-60)
    Given the six published fakes: matrix file, masking file, decision record, parameters, reference data and approver
    When the contract test of this service and of a consumer runs against them
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002, 404 answers MSG-P4-003, 409 answers MSG-GEN-004 or MSG-P7-002, 422 answers MSG-P1-002 with the failed check, and 503 answers MSG-GEN-006 or MSG-P7-003
    Then every error is an RFC 9457 problem response with "messageId" set and no personal value, no internal path and no token in the body, the log or the trace
    Then the fakes answer the allow, the refuse, the unavailable and the malformed case, so no test needs a running rwb-access, rwb-case or rwb-decision
    Then a consumer that maps a failure to an allow, or caches a failed or malformed answer, fails the contract test
    Then the fake set is the same for every consumer and no fake holds a production value
```

These criteria are new and test only the contract deliverable in the title. No legacy criterion is copied: legacy AC1 to AC13 of RWB-E1-037 belong to RWB-P4-E1037-APP, where they are carried verbatim with their origin tag, and the end-to-end form of the same outcome belongs to RWB-ITG-E1037-ITG (section 18).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The permission matrix version in force is the only source of what a role may do, and a capability area with "-" refuses every action in it | permission.letters (DF-REF-043), matrix_version (DF-REF-044); REQ-ACA-003; CTL-09 |
| BR2 | A matrix load is checked whole — every active role once for each of the 14 capability areas, letters from C, R, U, D, A or "-", known role codes — and a file with any error is refused in full | LOV-CAPABILITY; FSD P4 BR-P4-004; TSD P4 v3 T3.1 |
| BR3 | A version is approved by the role the parameter names for its table and never by the person who loaded it; the decision record is written before the change takes effect | Parameters rwb.refload.approver.*; Admin and access model section 3.3; CTL-05; CTL-06 |
| BR4 | The matrix answer carries role code, capability area, letters, matrix version, default scope and conflict version, and no person | TSD P4 v3 API-P4-007; FSD P4 A2.4 field catalog; NFR-039 |
| BR5 | A personal data field is masked unless the masking rule in force lets one of the session's roles see it; a masked field is filled from the masked view column or the last-four value, and a field with no rule is masked | Masking rules reference table; DL26; CTL-11; REQ-ACA-005; DF-ACE-073, DF-ACE-079 |
| BR6 | A masking rule names a field id that is personal and belongs to a `recovery.v_ace_*` view or a Workbench table, and a rule that names the clear identity number is refused | RWB-E1-069; Data Tier Map section 7; BR10 |
| BR7 | There is no tokenization and no token store; the clear identity number never leaves ACE and `id_no_last4` is the clearest value a rule or an answer may carry | ADR-010; Data Tier Map section 7; D-RCV-35 U1 |
| BR8 | A matrix or a masking version that reaches Approved is published as `rwb.access.AccessPolicyChanged.v1` with the version, the change kind and the effective date, and no personal value | Arch v5 slide 14 and slide 20; ASM-1417 |
| BR9 | Every operation declares the right it needs and a failure is a refusal, never an allow: 401 with no role, 403 without the letter, 503 when a dependency fails | TSD P4 v3 T-A; DP-08; ADR-020 |
| BR10 | The guard, the masker, the scope descriptor and the annotation are RWB-PLT-E1037-CON's and are not restated or re-implemented here | Arch v5 slide 10 and slide 35; RWB-PLT-E1037-CON |
| BR11 | This contract owns no session, no password, no token and no partner table, and it writes no table of P3 or P7 | DP-01; DP-02; Ownership Map; ADR-010 |
| BR12 | No business value is a constant in the contract or in its fakes: letters, scopes, masking positions, approver roles, versions and effective dates are data or parameters | FSD P4 BR-P4-004; BR-P4-005; DP-06; DP-07 |
| BR13 | A published version of the document is never edited in place: a breaking change is a new major version with a migration note and a new pin | Arch v5 slides 20 and 38; RWB-PLT-NF02-APP |
| BR14 | The delegation table, its versions and its holders stay in rwb-access (P4); the routing rule (lowest covering level, no-holder rule, one-level-up escalation) belongs to rwb-decision (P7) and reads the level, the holder and the substitute on this contract (read budget Not specified in the source documents (GAP-1251)); the approval stores delegation_limit_id, approval_level and limit_version only, with no join, view or foreign key into rwb_access | Ownership Map v1; Arch v5 slides 14 and 41; TSD P4 v3; TSD P7 v2 T3.3; RWB-E2-013 section 11 |
| BR15 | The service holds the delegation version in a local read-through cache, warmed at start before readiness and refreshed on DoaLimitChanged, with the effective date as the switch; no table is copied, and an alert fires when the cached version is older than the version in force | Arch v5 slides 14 and 41 (rwb.access.events.v1); legacy section 3 and section 13 |
| BR16 | The authorise request carries caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt; it is version v1 with BACKWARD compatibility, so a case service adds an attribute without breaking the access service; the answer, the way the field list travels and whether a sync is authorised once for the manifest or once per item are Not specified in the source documents (GAP-0952) | Arch v5 slide 14; FSD P4 A2.4 and A2.14; TSD P4 v3 T-A; RWB-E2-015 section 12 |

### 9. State transitions

The contract holds no case status and no stored object; it fixes the states of a version and the shape of the answer a state produces. The version states are LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P4 v3 T3.2, and the `state` column of the standard record columns holds them.

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Contract document | Version 1 | A backward-compatible addition to an answer or a fake | Version 1, minor | Consumers build unchanged against the pinned version |
| Contract document | Version 1 | A breaking change to a path, an answer or the event payload | Version 2 with a migration note | A consumer moves only by changing the pin and passing the contract test |
| Matrix or masking version | No version | A load passes every check | LOADED | The load answer is 201 with the row count and the version label; no version is in force |
| Matrix or masking version | LOADED | The table's approver role approves it and the decision record is written | APPROVED | 200 with the effective date and one published policy event |
| Matrix or masking version | LOADED | A failed approval | LOADED or REFUSED | 403, 409, 422 or 503 with its message id; nothing published and the version in force unchanged |
| Matrix or masking version | APPROVED | The effective date arrives | IN_FORCE | Every new session resolves it and the answer names it |
| Matrix or masking version | IN_FORCE | A later version is approved | SUPERSEDED | The later version answers from its date and the older rows stay readable for audit |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-access contract owner (any team, per U3) | Publishes the document, the four operations, the five objects, the vocabulary, the event and the fakes; owns version 1 and every later version |
| The app stories of this service (RWB-P4-E1037-APP and the contract dependencies of its consumers) | Implement the contract and pass the contract test; raise a change request instead of a local override |
| RW-REFADM Reference data administrator | Loads a matrix or a masking version (Reference data C); approves none |
| RW-COE Center of excellence analyst | Holds Reference data C and may load; may not approve |
| RW-SECADM Security administrator | Approves a permission version, as the approver role the parameter names for the `permission` table |
| RW-COMPLY Compliance and PDPA officer | Sets the masking values and approves a masking version, as the approver role the parameter names for the `masking_rule` table (DL26) |
| RW-AUDIT Internal audit | Reads every version and the approval entries; changes nothing |
| RW-PLATADM Platform administrator | Reads the matrix through the administration view (Platform administration R) |
| Every service that authorises or masks | Builds against this contract and RWB-PLT-E1037-CON and passes both contract tests; reads no P4 table |
| No delegation of authority level applies | A permission, a masking rule and a version are not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034, DF-REF-035, DF-REF-036, DF-REF-037, DF-REF-038, DF-REF-039 | `role` (P4 rwb-access) | id, role_code, role_name, role_class, default_scope, entra_group | Named only: carried in the matrix answer as role code, class and default scope |
| DF-REF-040, DF-REF-041, DF-REF-042, DF-REF-043, DF-REF-044 | `permission` (P4 rwb-access) | id, role_id, capability_area, letters, matrix_version | Named only: the matrix answer and the matrix load shape |
| DF-REF-198, DF-REF-199, DF-REF-200, DF-REF-201, DF-REF-202, DF-REF-203, DF-REF-204 | `masking_rule` (P4 rwb-access) | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Named only: the masking load shape and the masking-policy answer |
| DF-REF-205, DF-REF-206, DF-REF-207, DF-REF-208, DF-REF-209, DF-REF-210, DF-REF-211 | `role_conflict` (P4 rwb-access) | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Named only: the conflict version travels in the matrix answer |
| DF-REF-016 to DF-REF-062 | `delegation_limit` (P4 rwb-access) | the DoA fields | Named only: the DoA table this contract lists as a P4 object; its rows are written and read by RWB-P4-E1038-APP and RWB-P4-E2013-APP |
| DF-ACE-073, DF-ACE-074, DF-ACE-059, DF-ACE-078, DF-ACE-079 | `recovery.v_ace_customer` and `recovery.v_ace_contact` (P1 rwb-source-data) | id_no_masked, id_no_last4, date_of_birth, contact_value, contact_value_masked | Named only: the field ids a masking rule may name; no value is carried by the contract |
| No data of its own | the contract | None | The document stores nothing and the fakes hold only synthetic values |

Field IDs are those of the Logical Data Model and Data Dictionary v9, and the ACE fields are those of Physical Schema v7. Every row is named and none is written by the contract: the document fixes which field appears in which answer and which owner it comes from (DP-01), and a rule that names the clear identity number has no place in it (BR6, BR7).

Roles, permissions, scope, masking and delegation stay with rwb-access; rwb-case keeps TEAM as reference data and keeps only role_code as a code, validated at load time over the authorise contract of rwb-access (DP-08). The column list of the role and permission rows above is the list this contract publishes for P4. The unmasking answer for `interaction.summary` comes from the masking-policy answer of rwb-access under DP-08; `data_product_access` is P1's data product access catalogue and holds no masking row of its own.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/reference-loads` | Load a matrix file (table "permission") or a masking file (table "masking_rule") with `validFrom`; the body is multipart with the file, the table and the date; the answer is 201 with id, table, validFrom, status "Loaded" and rows | Reference data C (TSD P4 v3 API-P4-005; API Specification v5 `x-module: P4`) | `Idempotency-Key`; the same key returns the first answer |
| POST | `/api/recovery/access/v1/admin/reference-loads/{loadId}/approve` | Approve a loaded version with the approver role the parameter names for its table, after maker and checker and the decision record; the answer is 200 with the version Approved and its effective date | Reference data A as declared; the approver role in force (TSD P4 v3 API-P4-006) | `Idempotency-Key`; a repeat approve of an Approved version answers 409 and writes nothing |
| GET | `/api/recovery/access/v1/admin/roles` | The matrix in force: for each role, its role code, its permission rows with capability area and letters, its default scope, its conflict version and the matrix version | Platform administration R (TSD P4 v3 API-P4-007; the Ownership Map path) | Not applicable, read only |
| GET | `/api/recovery/access/v1/masking-policies` | The masking rules in force for the fields and roles of the session: field id, role code, `unmasked`, masking version, `validFrom`, `validTo` | Reference data R (Arch v5 slide 14 names the operation; the right is assumed, GAP-0779; ASM-1416) | Not applicable, read only |

All four paths sit on `/api/recovery/access/v1` (DP-13). The two load and approve operations keep the legacy shape of RWB-E1-037 section 12 and the path that API Specification v5 (`x-module: P4`) and TSD P4 v3 appendix T-A name; the R-PREC default ruling gives generic reference data to P3, so the contract states that these two operations carry **this service's own two tables only** and that lists, queues, timers, templates and parameters load through rwb-case (GAP-0779; ASM-1414). `GET /admin/roles` is one operation with one contract answered by two slices of this service: the role, class, scope and conflict fields by RWB-P4-E1019-APP and the permission rows and matrix version by RWB-P4-E1037-APP (ASM-1419). `GET /masking-policies` is the operation Arch v5 slide 14 names; neither the API Specification v5 nor TSD P4 v3 appendix T-A gives it a path, so the base rule of §R4 is applied and the gap is recorded.

Answers carry the dictionary field names DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204 and DF-REF-205 to DF-REF-211, and the conflict version travels with each conflict pair. Errors: 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 or MSG-P7-002; 422 MSG-P1-002 with the failed check in the detail; 503 MSG-GEN-006 or MSG-P7-003. Both loads accept `Idempotency-Key`; the two reads are read only.

#### 12.2 REST operations consumed

None. This service consumes no REST operation to answer the four operations: the parameters and the lists reach it through the client libraries of DP-06 and DP-07, the decision record is written through RWB-PLT-E1027-CON, and the session arrives in the caller's token. A consumer's call to this contract is one hop with a 2 s budget and a breaker, under DP-11.

#### 12.3 Events published

| Event | Topic | Payload | When |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | The change kind (`matrix` or `masking`), the version label, the effective date and the approver reference; no field value, no person, no case id and no letter of a role | On the commit of an approval of a matrix or a masking version, in the same transaction as the decision record (BR8) |

The payload shape is not fixed by any source — Not specified in the source documents (GAP-0779; ASM-1417) — and the contract forbids a personal value in it (BR7, NFR-040). The contract also states that the publish uses the outbox of the service baseline and that DP-09 and RWB-PLT-TE006-CON are not part of this slice (ASM-1420). `rwb.access.DoALimitChanged.v1` is published by RWB-P4-E1038-APP and is not published here.

#### 12.4 Events consumed

None. rwb-access is a reference-data owner in Arch v5 slide 14 (events: none) and reads the version in force from its own schema; this contract opens no subscription and writes no inbox row.

#### 12.5 Workflows and activities

None. The four operations are synchronous REST in the caller's thread and the approval is one transaction. The six-monthly access review is a Temporal Schedule on the `rwb-access` queue owned by RWB-P4-AD008-APP; DP-10 is referred to by this contract and no workflow, activity or Schedule is registered here (ASM-1421).

#### 12.6 Schedules

None. No Temporal Schedule and no quartz job belongs to the contract: a version takes effect on a date that the answer resolves, and the review Schedule of JOB-18 is RWB-P4-AD008-APP's.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This contract |
|---|---|---|---|
| `role` | `rwb_access` | P4 | Named; the matrix answer carries role code, class and default scope |
| `permission` | `rwb_access` | P4 | Named; the matrix load and the matrix answer |
| `masking_rule` | `rwb_access` | P4 | Named; the masking load and the masking-policy answer |
| `role_conflict` | `rwb_access` | P4 | Named; the conflict version of a role pair |
| `delegation_limit` | `rwb_access` | P4 | Named; its own contract is RWB-P4-E1038-CON |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline; the policy event writes one outbox row |
| `decision_log_entry`, `approval` | `rwb_decision` | P7 | **Never written**; the approval entry goes through the decision-record library (DP-03) |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | `rwb_case` | P3 | **Never read by SQL**; reached through DP-06 and DP-07 |
| `partner`, `partner_user`, `partner_instruction` | `rwb_partner` | S9 | **Never read and never written** (Ownership Map) |

The contract names the five P4 tables and owns none of another service's; no foreign key crosses a schema and no answer carries a row of a table outside `rwb_access`. This contract creates no table: the DDL, keys, indexes, dictionary rows and the Flyway baseline of the five tables are those of RWB-P4-E1001-APP, and the rwb_access baseline named by sibling stories is the version this story applies. The masking rows, the role list and the permission matrix stay in `rwb_access`; no other service holds a copy of them or reads them by SQL, and a consumer takes the answer of POST /api/recovery/access/v1/authorise.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this contract |
|---|---|---|
| Matrix file fake | The multipart body of the matrix load | The version "PM-2026.12" with 756 rows that gives RW-LEGAL "R" in Queue and allocation, the refused file "PM-2026.13" with a duplicate row and the letters "RX" (AC2) |
| Masking file fake | The multipart body of the masking load | "MASK-SIT-01", in which only RW-CASEOWN sees DF-ACE-078 in clear, no rule for DF-ACE-059, and a refused rule naming the clear identity number (AC3) |
| Decision-record fake | RWB-PLT-E1027-CON | The written entry with code `AC-VERS`, the unavailable store, and the assertion that no value and no case reach it (AC2, AC4) |
| Parameters fake | RWB-P3-E1042-CON | "rwb.refload.approver.permission" = "RW-SECADM", "rwb.refload.approver.masking_rule" = "RW-COMPLY", "rwb.access.membership-refresh-minutes" = 5 (AC2, AC6) |
| Reference-data fake | RWB-P3-E1043-CON | `LOV-CAPABILITY` with 14 areas, `LOV-SCOPE` with OWN, TEAM, REGION and ALL, `LOV-ROLE-CLASS`, each with a version (AC2, AC3) |
| Approver fake | The approver rule of the approve operation | The table's approver, the loader who may not approve, a caller with no approver role, and the unavailable decision record (AC2, AC6) |

The six fakes are published with the contract document so that the app stories of this service and every consumer build and test with no running rwb-access, rwb-case or rwb-decision (AC6).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations under `/api/recovery/access/v1` | 0 | OpenAPI 3.1; one hop, 2 s timeout, breaker; the two reads are read only |
| Kafka | 1 event on `rwb.access.events.v1` | 0 | `rwb.access.AccessPolicyChanged.v1` on approval, through the baseline outbox |
| Temporal | 0 | 0 | No workflow, activity or Schedule; JOB-18 is RWB-P4-AD008-APP's |
| File | 0 at run time | 0 | The matrix and masking files arrive in the multipart body of the load operation |

### 13. Solution plan

**Package.** The contract lives with the service: `th.co.scb.ace.workbench.recovery.access.matrix`, module `matrix`, with the OpenAPI 3.1 document, the request and answer records of the four operations, the error vocabulary, the event schema and the six fakes as resources of the module. Service base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` (not used here). The implementation is RWB-P4-E1037-APP's.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract names the five P4 tables and no table of another service | none |
| DP-02 | `recovery_svc` login | One login per service: the contract states that the per-service rwb-access login serves the four operations | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. Referred to; the app story of this key carries the dependency | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The contract names the view field ids a rule may use and reads no view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, for the two approver roles and the refresh interval | referred to; the consuming story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, for `LOV-CAPABILITY`, `LOV-SCOPE` and `LOV-ROLE-CLASS` | referred to; the consuming story carries the dependency |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. This contract declares the rights the guard enforces and restates neither the guard nor its decision | referred to; the consuming story carries the dependency |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. Referred to for the sibling six-monthly access review (JOB-18, RWB-P4-AD008-APP); no Schedule is registered here | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout: the four operations fix the one-hop shape and the fakes | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`: every path is on `/api/recovery/access/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The contract adds no migration and states that the two unique indexes are the app story's | referred to; the consuming story carries the dependency |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The contract has no export and no lake endpoint | none |
| DP-19 | Screen, ace-web | gateway-bff composite route: the route renders the 403, the 404 and the masked field the contract fixes; SCR-43 and SCR-47 are not built here | referred to; the consuming story carries the dependency |

The H and C dependencies named in the last column belong to RWB-P4-E1037-APP and to the consumers; this contract story has no build dependency of its own, which is why its `H`, `C`, `I` and `X` rows read None. The metadata rows stay as the work package fixes them; the dependencies each DP row adds are recorded in the table above and are built against the fakes of section 12.8 from Day 1.

**Hardware and software change.** The contract replaces the in-process call of the monolith's `recovery.access.matrix` package with four REST operations and one Kafka event: the matrix and the masking rules are asked of their owner instead of being read from the same connection, and the policy change reaches consumers as an event rather than as a restart. It adds no schema, no topic, no queue, no Schedule and no bucket beyond what the service and the platform already have, so no new hardware is implied.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| OpenAPI document | Document | The four operations of section 12.1, their requests, answers, errors and idempotency (AC1, AC2, AC3) |
| Load and approve shapes | Record set | The multipart load, the table value, the validFrom, the 201 answer and the 200 approve answer with the effective date (AC2) |
| Matrix answer | Record set | The role code, permission rows with area and letters, default scope, conflict version and matrix version, with no person (AC1, AC4 of the app story) |
| Masking-policy answer | Record set | The field id, role code, unmasked flag, masking version and validity of each rule in force (AC3); the masking rules travel in this answer and rwb-case applies them when it builds the export |
| Authorise answer | Record set | The scope kind and the case-scope predicate, applied by the service to the case ID of each entry inside the query; the chain-mismatch incident goes to the Compliance queue read from platform configuration |
| Error vocabulary | Document | The six statuses with their message ids and the RFC 9457 problem shape (AC6) |
| Event schema | Schema | `rwb.access.AccessPolicyChanged.v1` with the change kind, the version and the effective date, and the prohibition on a personal value (AC4) |
| Division statement | Document | The one paragraph of section 2 and the negative statements of AC5 |
| Fakes and fixtures | Test asset | The six fakes of section 12.8 (AC6) |

**Build steps**

1. Write the OpenAPI document with the four operations, their access rights, requests, answers and statuses; run the contract test of a consumer against it (AC1, AC2, AC3).
2. Write the load and approve shapes and prove the 201, the 422 with the failed check, the 403 of the approver role, the 409 of the loader and the 503 of the decision record (AC2).
3. Write the matrix and masking-policy answers and prove that every policy row carries a version and that no answer carries a person (AC1, AC3).
4. Write the error vocabulary and the RFC 9457 shape; prove the six statuses and that no body, log or trace carries a personal value (AC6).
5. Write the event schema and prove that an approval publishes one event and that a failed decision record publishes none (AC4).
6. Write the division paragraph and the negative statements, and prove that the guard and masker are absent here and the policy rows absent from the library contract (AC5).
7. Publish the six fakes with their allow, refuse, unavailable and malformed cases, and wire the contract test into the build of RWB-P4-E1037-APP and of a consumer (AC6).

**Done when.** The six criteria pass as contract tests; the four operations and the nine tables of section 12 name their owner from the Ownership Map; the six fakes are published with the document; and RWB-P4-E1037-APP and one consumer build and pass their contract tests against the published version.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The caller holds no Recovery Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without the letter an operation declares, or approve by a role that is not the table's approver | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A path the contract does not publish, or a record outside the role's scope | This case is not in your scope. |
| MSG-P1-002 | A matrix or masking file fails a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | The loader calls approve on their own load | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The approval cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | A second approve of an Approved load, or a load that is not Loaded | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The store is unavailable | {system} is not available. Your request is queued and will be retried. |

The message ids and their wording are copied unchanged from RWB-E1-037; the contract adds no message of its own, and the Thai text of each follows DL10. Every error is an RFC 9457 problem response with `messageId` set; for MSG-P4-002 the `{action}` value names the action and never a case fact or a field value, and for MSG-P1-002 the `{check}` value names the failed check.

### 15. Screens and states

No screen of its own. What the contract fixes for the screens of the 19 services is the status and the message id a screen receives (401, 403 with MSG-P4-002, 404 with MSG-P4-003, 503 with no business data), the masked value a field carries, and the rule that no screen error reveals a token, an internal path or a personal value. SCR-43 Roles and access and SCR-47 Personal data are Epic 8 and out of scope (DP-19), and the route that renders them is RWB-PLT-N001-CON's. The states of SCR-43 (empty, loading, error, no access) are Not specified in the source documents (CG-ALL-5012). The states of SCR-47 empty, error and no access are Not specified in the source documents (CG-ALL-5013); its loading state is as the screen specification gives it.

The states an administrator sees through the contract are the states of a version: Loaded with its row count, Approved with its approver and effective date, in force from that date, superseded by a later version, or refused with the failed check named.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P4-E1037-CON-01 | AC1, AC3 | Contract | The published document against a consumer's generated client; the four operations and the five objects; the 404 of an unpublished path; the `Role` and `MaskingPolicy` answers with DF-REF-034 to DF-REF-044 and DF-REF-198 to DF-REF-204 |
| TC-P4-E1037-CON-02 | AC2 | Contract | A matrix file with 756 rows and validFrom "2026-12-01"; the refused file "PM-2026.13"; the approver, the loader, the unknown load and the unavailable decision record, through the six fakes |
| TC-P4-E1037-CON-03 | AC3 | Contract | "MASK-SIT-01" with RW-CASEOWN clear on DF-ACE-078, no rule for DF-ACE-059, and a refused rule naming the clear identity number; the values "XXXXXX5678" and "0123" |
| TC-P4-E1037-CON-04 | AC4 | Contract | One approved matrix version and one approved masking version; the event with its change kind, version and effective date; a repeated delivery; the failed decision record with no event |
| TC-P4-E1037-CON-05 | AC5, AC6 | Contract | The two published contracts compared by the contract test; the six statuses with their message ids; the six fakes with their allow, refuse, unavailable and malformed cases |
| TC-P4-E1037-CON-06 | BR11; section 12.7 tables | Contract | Each table of section 12.7 in `rwb_access` and one table outside it, through the contract's fakes; the outside table is refused and no foreign key crosses a schema |
| TC-P4-E1037-CON-07 | BR1 to BR13 | Contract | Each rule of section 8 exercised once through the contract's fakes, one case per rule, BR1 to BR13 |

No test of this story is an integration copy: the contract is exercised against its own fakes, never against a live service, and no `-ITG` id belongs to it. The five contract test cases are new and carry no legacy cover.

The fifteen legacy test cases of RWB-E1-037 are `TC-E1-037-01`, `TC-E1-037-02`, `TC-E1-037-03`, `TC-E1-037-04`, `TC-E1-037-05`, `TC-E1-037-06`, `TC-E1-037-07`, `TC-E1-037-08`, `TC-E1-037-09`, `TC-E1-037-10`, `TC-E1-037-11`, `TC-E1-037-12`, `TC-E1-037-13`, `TC-E1-037-14` and `TC-E1-037-15`; they are owned and executed by RWB-P4-E1037-APP, with their end-to-end copies in RWB-ITG-E1037-ITG, and none of them is restated here.

### 17. Guardrails

- No business value in the contract or in a fake: letters, scopes, masking positions, approver roles, versions and effective dates are data or parameters (BR12).
- No personal data in a payload, a fixture, an example or a log: the answers carry field ids and version labels, and the policy event carries no value (BR7, BR8).
- The contract owns no guard and no masker: the guard, the masker, the scope descriptor and the annotation are RWB-PLT-E1037-CON's and are not restated here (BR10).
- No session, no password, no token and no partner table: the session is RWB-P4-E1022-APP's, the token store does not exist and partners are S9's (BR11, BR7).
- Every failure is a refusal: 401, 403, 404, 409, 422 and 503 with their message id, never an allow (BR9).
- A published version is never edited in place; a breaking change is a new major version with a migration note and a new pin (BR13).
- No statement names a table outside `rwb_access` and no answer carries a row of another service's table (DP-01).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-003 | Permission matrix as data, the only source of rights | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR2, BR3, BR4 | TC-P4-E1037-CON-01, TC-P4-E1037-CON-02 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR5, BR6, BR7 | TC-P4-E1037-CON-01, TC-P4-E1037-CON-03 |
| REQ-ACA-007 | Access outside the matrix refused and recorded | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR9, BR11 | TC-P4-E1037-CON-01, TC-P4-E1037-CON-05, TC-P4-E1037-CON-06 |
| REQ-ACA-009 | A user sees only the cases their role and scope allow | Epic 1, 3.4 | FEAT-ACA-14 | All recovery processes | BR4, BR5 | TC-P4-E1037-CON-01 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | Epic 2, 3.4 | FEAT-ACA-13 | All recovery processes | BR3, BR8, BR9 | TC-P4-E1037-CON-02, TC-P4-E1037-CON-04 |
| REQ-ACA-006 | Every read of a personal data field written to the access log | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR5, BR8 | TC-P4-E1037-CON-03 |
| Legacy TC-E1-037-01 to TC-E1-037-15 | The fifteen legacy test cases of RWB-E1-037 | Epic 1, 3.4; Epic 2, 3.4; Program, 5.4 | FEAT-ACA-04, FEAT-ACA-05, FEAT-ACA-13, FEAT-ACA-14 | All recovery processes | BR1 to BR11 | owned and executed by RWB-P4-E1037-APP; the -ITG copies are RWB-ITG-E1037-ITG's |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1037-APP | App development | H: implements the four operations, the two loads, the approve path and the policy event against this contract, and owns legacy AC1 to AC13 |
| RWB-PLT-E1037-CON, RWB-PLT-E1037-APP | Contract, App development | The guard, masker and annotation artefact every service binds; this contract publishes the data that artefact reads |
| RWB-P4-E1022-APP | App development | The sign-in and the session; the contract states that it holds neither |
| RWB-P4-E1039-APP | App development | The access log, the refusal entry and break-glass |
| RWB-P4-E1019-APP, RWB-P4-E1038-APP | App development | The role, class and conflict rows of the matrix answer; the DoA table this contract names |
| RWB-P4-E2019-CON | Contract | The partner identity contract; this contract owns no partner table |
| RWB-ITG-E1037-ITG | Integration | The end-to-end proof of the same outcome across P4, P1, P3 and the library |

| Legacy reference | Where it is kept |
|---|---|
| The two load operations and the approve operation (legacy section 12) | Section 12.1 and 12.2, with the legacy shape kept |
| The matrix, the masking rules and the version in force (legacy sections 4, 8 and 11) | Sections 4, 8, 11 and 12 |
| The approver rule with maker and checker and the failure of the decision record (legacy BR3, BR9 and exceptions X4 to X6) | Sections 5, 8 and 9 |
| The masking rule and the identity boundary (legacy BR6, BR10 and BR12) | Sections 8, 11 and 12.1 |
| The messages of the legacy story | Section 14 |
| The legacy criteria and the fifteen legacy test cases (legacy sections 7 and 16) | Owned by RWB-P4-E1037-APP, with the end-to-end copies in RWB-ITG-E1037-ITG |
| The legacy out of scope list (legacy section 19) | Section 19 |

### 19. Out of scope

- The implementation of the four operations, the two loaders, the approval service and the policy event: RWB-P4-E1037-APP.
- The guard, the masker, the `@PersonalData` annotation, the scope descriptor and their fakes: RWB-PLT-E1037-CON and RWB-PLT-E1037-APP.
- The sign-in, the multi-factor check, the group-to-role answer and the session: RWB-P4-E1022-APP.
- The access log store, its search and export, the refusal entries and break-glass: RWB-P4-E1039-APP.
- The role, class, default scope and conflict rows of the matrix answer: RWB-P4-E1019-APP.
- The DoA table and its lookup: RWB-P4-E1038-APP and RWB-P4-E2013-APP.
- The DoA event `rwb.access.DoALimitChanged.v1`: the DoA story of this service.
- The generic reference-load path for lists, queues, timers, templates and parameters: rwb-case (P3) under DP-06 and DP-07.
- The partner identity and the partner portal: S9 rwb-partner and RWB-P4-E2019-CON.
- The administration screens SCR-43 Roles and access and SCR-47 Personal data: Epic 8 (FEAT-ADM-01, FEAT-ADM-14), rendered by RWB-PLT-N001-CON.
- The masking values for each role and field: Compliance, DL26.
- The six-monthly access review list (JOB-18, CTL-10): RWB-P4-AD008-APP.
- The token store, which does not exist: ADR-010.
- The end-to-end proof across the wave 1 services: RWB-ITG-E1037-ITG.
