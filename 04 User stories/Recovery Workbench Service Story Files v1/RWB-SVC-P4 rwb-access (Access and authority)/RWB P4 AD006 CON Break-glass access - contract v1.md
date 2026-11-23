# RWB-P4-AD006-CON Break-glass access

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-006 for rwb-access — the contract of the incident-bound break-glass grant: the activation, the end and the read operations, the `BreakGlassActivation` and `BreakGlassGrant` schemas, the session field of API-P4-012, the auto-expiry rule, the decision-record type and the envelope. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **tech lead**, I want **the published contract baseline of break-glass access: an OpenAPI 3.1 document for the activation, the end and the read of a grant, the `BreakGlassActivation` and `BreakGlassGrant` schemas with the incident, the area, the right, the scope, the reason of at least 20 characters, the window start and end, the approver reference, the state and the break-glass marker, the `breakGlass` field of the session, the auto-expiry rule, the decision-record type, one RFC 9457 error envelope with its message IDs, the contract tables of section 12 and the contract fakes**, so that **the app story builds on Day 1 against a fixed, testable contract, and every service that calls the guard learns exactly what a grant covers, for how long, and how an action under it is marked**.

This is the contract of the **grant lifecycle** of legacy RWB-AD-006, and it is the lifecycle half of that key. The access log that records the actions and the administration surface that lists the grants are legacy RWB-E1-039's and are contracted by RWB-P4-E1039-CON; the search and the export of the log are RWB-P4-AD007-CON's. **This document contracts the request, the approval reference, the activation, the marking, the end and the self-expiry of a grant, and nothing of the access log.**

What this document fixes is the shape of an emergency that can be audited: one incident, one caller, one area, one right, one scope, one reason, one window, one approval, one state and one marker. It fixes no business value: the window hours, the incident pattern and the reason bounds are data, and the value in force is quoted only where a criterion has to be observable.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story gave emergency access to a platform administrator with a row in a database and a screen of the monolith, and no document said what a grant covers, who approved it, when it ends or what an entry written under it looks like. In the target the grant is a row of `rwb_access` read by the guard of the same service on every call, and the estate's other services meet it only through the session they are handed, so the answer must be written down once: what a grant is, how long it lasts, what it raises, and how an action under it is marked.

Two properties shape the document. The first is that **a grant expires by the clock**: the document declares that a grant is in force only while its state is `ACTIVE` and the time is before its window end, so no reader may treat a row as an entitlement, and no consumer may expect a second message to tell it the grant has gone. The second is that **a grant is session state and not a policy change**, which is why the document publishes no event of its own: Architecture v5 slide 14 gives `rwb-access` exactly two business events, `AccessPolicyChanged` and `DoaLimitChanged` (slide 43), and both are cache refreshes for a value that persists; a grant ends by itself, so an event about it would tell a consumer to cache something that has already expired. The only message a grant produces is the decision-record entry, and that message belongs to the library of DP-03 on `rwb.decision-record.v1` (ASM-1495).

The third property is the boundary that the two halves of the key must not blur. The emergency access is only as good as its record: the grant is the entitlement and the access log is the evidence. This document therefore declares the marker — the grant id and the incident reference carried on the session and on every entry of the window — and leaves the entry itself to RWB-P4-E1039-CON, which already defines it. A reader of this document learns what it must stamp; a reader of that one learns where the stamp lands.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base path, the error envelope and the CloudEvents envelope follow the platform rule rather than a local choice.
- RWB-PLT-E1027-CON is published: the decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), whose entry is the record of every activation, every refusal and every end. The dependency is carried by the app story, RWB-P4-AD006-APP.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves SCR-43 and merges the grant read with the access-log read of RWB-P4-E1039-APP. The dependency is carried by the app story.
- RWB-P4-E1039-CON is published or in draft: the access-log entry that this document marks with the grant id and the incident reference. This document declares the marker and never restates the entry.
- `POST /admin/break-glass-grants` is API-P4-013 in TSD P4 v3 appendix T-A: purpose, request `BreakGlassActivation`, response `BreakGlassGrant`, right C of Platform administration, `Idempotency-Key` and errors 401, 403, 409, 422 and 503.
- The **end and read operations have no row in the ownership map and none in TSD P4 v3 appendix T-A**, so their paths, their rights and their answers are this revision's own decision — **Not specified in the source documents (GAP-0798; ASM-1494)**. This document fixes them as `POST /admin/break-glass-grants/{grantId}/end` with right C and `GET /admin/break-glass-grants/{grantId}` with right R.
- The grant has **no table and no field ids in any source**: it is not in TSD P4 v3 T3.1, where P4's tables are `role`, `permission`, `delegation_limit` and the rules, and it is not in the ownership map, whose only P4 tables are `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` — **Not specified in the source documents (GAP-0799; ASM-1493)**. This document fixes the field names and the types of the two schemas and leaves the physical column names to RWB-P4-AD006-DB.
- The incident register's owner and contract are **Not specified in the source documents (GAP-0797; ASM-1491)**; the document declares the open-incident rule and names the port, and the app story carries the Day-1 stub.
- The window in force is 4 hours and the reason is at least 20 characters: FSD P4 v3 AC-ALT-P4-009-01 activates at 10:30, gives a grant active until 14:30 and a group end of 18:00, and AC-EXC-P4-007-02 refuses a reason of 12 characters with the min 20 and max 1000 of MSG-GEN-002.
- The state vocabulary is `ACTIVE` and `ENDED` only, which is the vocabulary RWB-P4-E1039-DB already gives the grant table and the one this document declares; a refused request writes no row and therefore no third state.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and it holds in Contract group CG-W4 because the business epic EP08 is wave 4 in the W-MAP (§R5.6).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three grant operations under the base `/api/recovery/access/v1`, with the shared components the `rwb-access` operations use.
2. Draft the schema `BreakGlassActivation`: `incidentReference`, `iamRequestId`, `capabilityArea`, `rightCode`, `scopeCode`, `reason` (min length 20, max 1000) and `windowHours`, with the `Idempotency-Key` header.
3. Draft the schema `BreakGlassGrant`: `grantId`, `actorReference`, `incidentReference`, `iamRequestId`, `approverReference`, `capabilityArea`, `rightCode`, `scopeCode`, `reason`, `startsAt`, `endsAt`, `state`, `breakGlassMarker`, `decisionRecordEntryRef` and `endedAt`.
4. Declare the `breakGlass` field of the session of API-P4-012 as a component that carries the grant id, the incident, the area, the right, the scope, the start, the end and the state, and declare it absent when no grant is in force.
5. State the auto-expiry rule in the description of the three operations and of the session field: a grant is in force only while `state` is `ACTIVE` and the time is before `endsAt`; a call after `endsAt` is authorised on the caller's own letters; the row settles to `ENDED` on the next read and one `AC-BGOFF` entry records the end; no person and no job acts for the grant to end.
6. State the bound of a grant: one incident, one caller, one area, one right, one scope and one window, at most one `ACTIVE` grant per caller, and the state vocabulary `ACTIVE` and `ENDED`.
7. State the rights: Platform administration C for the activation and the end, R for the read, an active role required on every call, and the 401 and 403 of the default deny rule. The legacy Permission checks table gives Platform administration R; C is the letter of API-P4-013 in TSD P4 v3, which outranks the story master under R-PREC rule 6 over 9.
8. Agree the error envelope and the message mapping for 401, 403, 404, 409, 422 and 503, with the business texts of the legacy story where the message already exists.
9. Declare that no event name is published by this capability, name the decision-record type the library publishes on `rwb.decision-record.v1`, and state why a grant is not an `rwb.access.*` event.
10. Publish the contract tables of section 12 (nine sub-tables) and the contract fakes, then add the contract tests: schema validation, the bound and the expiry rule, the session field, the rights, the envelope, the owner declarations and the drift between a fake and the document.
11. Tag the baseline and hand it to RWB-P4-AD006-APP, to RWB-P4-E1037-CON for the guard, to RWB-P4-E1019-CON for the session field and to RWB-P4-E1039-CON for the marker.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A schema declares a person's name, an e-mail address, an identity number or a case fact | The review fails and the property is removed; the rule is a lint item of the document | None | AC2 |
| X3 | A field of the activation or of the grant has no source definition | The field is named by this document's own decision and the gap is carried | None | AC2 |
| X4 | The document declares a grant without a window end, or a state other than `ACTIVE` and `ENDED` | The review fails: a grant without an end is not a grant, and a third state is a row the app story would have to explain | None | AC3 |
| X5 | The document declares a grant that persists past its `endsAt`, or one that needs a message to end | The review fails: the clock is the authority and no message ends a grant | None | AC3 |
| X6 | The document declares a `rwb.access.*` event for a grant, or a second access event name | The review fails and the statement of 12.3 stands: no event name is published by this capability | None | AC4 |
| X7 | The session component declares a grant that is not in force, or omits the state | The contract test fails: the `breakGlass` field is present only while a grant is in force and it always carries its state | None | AC5 |
| X8 | The document declares an operation or a table of another service as provided | The review fails; the incident port and the access-log entry are documented as consumed or as referenced | None | AC6 |
| X9 | An error response carries no `messageId`, or a `messageId` not in the agreed set | The contract test fails and the merge is blocked | None | AC6 |
| X10 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it reads the ownership map, TSD P4 v3 appendix T-A, the platform envelopes, the access-log entry of RWB-P4-E1039-CON and the session of API-P4-012 only |
| Negotiable | The field-level detail of the two schemas, the session component and the decision-record payload are settled with the app story and the access-log contract; the base, the rights, the state vocabulary and the envelope are fixed by the target architecture and the Workbench |
| Valuable | Unblocks the app story, the guard and the access-log marker on Day 1 with a written answer to "what does a grant cover, until when, and how is an action under it marked" |
| Estimable | One document, two schemas, one session component, one decision-record declaration, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: The break-glass grant contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given a grant is one row of "break_glass_grant" in "rwb_access" bound to one open incident
    Given the state vocabulary of a grant is "ACTIVE" and "ENDED"

  Scenario: AC1 The OpenAPI 3.1 document describes the three grant operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access break-glass access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/break-glass-grants, POST /admin/break-glass-grants/{grantId}/end and GET /admin/break-glass-grants/{grantId} with the owner rwb-access
    Then the activation and the end declare Platform administration with the right C, and the read declares Platform administration with the right R
    Then every operation declares 401, 403, 404, 409, 422 and 503
    Then the activation and the end declare the Idempotency-Key header and the read declares none

  Scenario: AC2 The two schemas carry the incident, the bound, the reason, the window, the approval, the state and the marker (new, D-RCV-60)
    Given the schemas BreakGlassActivation and BreakGlassGrant of the document
    Then BreakGlassActivation carries incidentReference, iamRequestId, capabilityArea, rightCode, scopeCode, reason and windowHours
    Then BreakGlassGrant carries grantId, actorReference, incidentReference, iamRequestId, approverReference, capabilityArea, rightCode, scopeCode, reason, startsAt, endsAt, endedAt, state, breakGlassMarker and decisionRecordEntryRef
    Then reason is declared with a minimum length of 20 and a maximum of 1000
    Then endsAt is declared required and after startsAt, and state is declared as ACTIVE or ENDED
    Then breakGlassMarker is declared true on a grant in force and the marker of an entry is declared as the grantId and the incidentReference
    Then no schema, no parameter and no example declares a person's name, an e-mail address, an identity number or a case fact

  Scenario: AC3 A grant is in force by its clock and ends with no action by anyone (new, D-RCV-60)
    Given the descriptions of the three operations and of the state field
    Then the document states that a grant is in force only while state is ACTIVE and the time is before endsAt
    Then the document states that a call after endsAt is authorised on the caller's own letters and refused where the letter is missing
    Then the document states that the row settles to ENDED on the next read with one end entry, and that no person and no job acts for the grant to end
    Then the document states that at most one grant of a caller is ACTIVE and that a second activation answers 409
    Then the document states that a grant is never reactivated and that a new activation is a new grant with its own approval and incident
    Then no description requires an event, a job or a call for the grant to end

  Scenario: AC4 No event name is published by this capability (new, D-RCV-60)
    Given the events section of the document
    Then no rwb.access.* event name is declared for a grant
    Then the document states that Architecture v5 slide 14 gives rwb-access only AccessPolicyChanged and DoaLimitChanged, and that a grant is session state and not a policy change
    Then the decision-record type rwb.decision-record.DecisionRecorded.v1 is declared on the shared topic rwb.decision-record.v1 with the codes AC-BGON, AC-BGREF and AC-BGOFF, as the library's message and not as an event of this capability
    Then no payload carries a name, an e-mail address, an identity number or a case fact

  Scenario: AC5 The session of API-P4-012 carries the break-glass state (new, D-RCV-60)
    Given the session component of the document
    Then it declares breakGlass with grantId, incidentReference, capabilityArea, rightCode, scopeCode, startsAt, endsAt and state
    Then the field is declared present only while a grant of the caller is in force and absent otherwise
    Then the document states that the session read is the operation of RWB-P4-E1019-APP and RWB-P4-E1037-CON and that this capability fills its break-glass field
    Then the read declares the 401 and the 503 of API-P4-012 and adds no other failure

  Scenario: AC6 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any of the three operations
    Then the body carries the code, the message, the messageId, the traceId and the field list, with the problem media type
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 404 and 409 carry MSG-GEN-004, 422 carries MSG-GEN-001 or MSG-GEN-002 and 503 carries MSG-P7-003
    Then the message texts are the legacy texts where the message already exists
    Then the document states which condition has no message text in the sources, being the incident that is not open

  Scenario: AC7 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of section 12.8
    When a fake is compared with the document
    Then the grant fake answers the three paths of 12.1: the incident INC0004521 open, the approval IAM-778812, the activation at 10:30 with a window of 4 hours, the grant active until 14:30, the ended grant and the 409 of a second activation with a different key
    Then the incident-status stub answers one open incident, one closed incident and one reference that matches no incident
    Then the decision-record fake answers the entry append and the 503 with MSG-P7-003
    Then the access-log writer fake answers an entry carrying the grant id and the incident reference
    Then a contract test fails on any drift between a fake and the document, and no fake carries a name or an e-mail address
```

These seven criteria test the artefact only. No criterion restates a legacy acceptance criterion: the three legacy criteria of RWB-AD-006 are owned by RWB-P4-AD006-APP and are listed with their tests in section 16 as the cases this contract is the ground of.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path, table or event | DP-13; Architecture v5 slides 14 and 41 |
| BR2 | The activation is API-P4-013 with right C of Platform administration, request `BreakGlassActivation`, response `BreakGlassGrant`, `Idempotency-Key` and errors 401, 403, 409, 422 and 503 | TSD P4 v3 appendix T-A.2 |
| BR3 | A grant is bound to one incident, one caller, one area, one right, one scope and one window, and at most one grant of a caller is `ACTIVE` | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-ALT-P4-009-01 and AC-EXC-P4-007-05; ASM-1500 |
| BR4 | The reason is at least 20 characters and at most 1000, and the window is a number of hours from the activation, bounded by the end of the bank IAM group membership | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-ALT-P4-009-01 and AC-EXC-P4-007-02; ASM-1497 |
| BR5 | The approval is the security administrator's IAM request, named by its reference on the grant, with the approver reference beside it | TSD P4 v3 API-P4-013; ASM-1499 |
| BR6 | A grant is in force only while `state` is `ACTIVE` and the time is before `endsAt`; the clock is the authority and no message, job or person ends a grant | Legacy RWB-AD-006 AC3; ASM-1496 |
| BR7 | The state vocabulary is `ACTIVE` and `ENDED`; a refused activation writes no grant and therefore no third state | RWB-P4-E1039-DB constraint; ASM-1496 |
| BR8 | The marker of an action is the grant id and the incident reference on the session, on the authorisation call and on the entry | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-ALT-P4-009-01 |
| BR9 | No event name is published by this capability. Architecture v5 slide 14 gives `rwb-access` only `AccessPolicyChanged` and `DoaLimitChanged`, and a grant is session state, not a policy change | Architecture v5 slides 14, 20 and 43; ASM-1495 |
| BR10 | The end and the read are this revision's own decision at `POST /admin/break-glass-grants/{grantId}/end` and `GET /admin/break-glass-grants/{grantId}`, with rights C and R, because no ownership-map row and no TSD row exists | ASM-1494; GAP-0798 |
| BR11 | Error responses use one envelope and one message ID per condition, and the business texts are copied unchanged from the legacy story where the message exists | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR12 | No schema, parameter, example or fake declares a name, an e-mail address, an identity number or a case fact; the actor is a staff user reference | NFR-040; guardrails |
| BR13 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | The three operations, the two schemas, the session field and the event statement are described | The document validates and the contract tests pass | In review |
| In review | Consumer sign-off | RWB-P4-AD006-APP, RWB-P4-E1037-CON, RWB-P4-E1019-CON and RWB-P4-E1039-CON accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

A grant has its own states — `ACTIVE` and `ENDED` — and they are the app story's data states; the document declares them and does not move them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document, the two schemas, the session component, the event statement and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version, and confirms the expiry rule against the architecture |
| Security administrator and the audit representative | Review and sign off the rights, the bound of a grant and the marking rule |
| Tech lead of the guard of RWB-P4-E1037 | Reviews the expiry rule and the `breakGlass` field, because the guard is the consumer that applies both |
| Tech lead of the access log of RWB-P4-E1039 | Reviews the marker, because its writer stamps the grant and the incident on the entry |
| Tech lead of the session of RWB-P4-E1019 | Reviews the `breakGlass` field of API-P4-012, because the session read is that story's operation |
| Data steward | Confirms that no personal data property is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Activation | `incidentReference`, `iamRequestId`, `capabilityArea` (one of the 14), `rightCode` (one of C, R, U, D, A or a dash), `scopeCode` (OWN, TEAM, REGION, ALL), `reason` (min 20, max 1000), `windowHours`; the `Idempotency-Key` header |
| Grant | `grantId`, `actorReference`, `incidentReference`, `iamRequestId`, `approverReference`, `capabilityArea`, `rightCode`, `scopeCode`, `reason`, `startsAt`, `endsAt`, `endedAt`, `state` (`ACTIVE`, `ENDED`), `breakGlassMarker`, `decisionRecordEntryRef` |
| Session field | `breakGlass` with `grantId`, `incidentReference`, `capabilityArea`, `rightCode`, `scopeCode`, `startsAt`, `endsAt`, `state`; absent when no grant is in force |
| Marker on an entry | The `grantId` and the `incidentReference` the access-log entry of RWB-P4-E1039-CON carries; the entry itself is not redefined here |
| Lists and codes | The capability areas of `LOV-CAPABILITY` (DF-REF-042), the letters of `permission` (DF-REF-043) and the scopes of `LOV-SCOPE` (DF-REF-038); the document names them and enumerates none in a schema |
| Window | The window hours are data; the value in force is 4 hours (FSD P4 v3 AC-ALT-P4-009-01), and the parameter code is **Not specified in the source documents (GAP-0798; ASM-1492)** |
| Incident | The reference of the open incident and its open state; the pattern and the register's owner are **Not specified in the source documents (GAP-0797; ASM-1491)** |
| Decision-record entry | The activation, the refusal and the end entries with the codes `AC-BGON`, `AC-BGREF` and `AC-BGOFF`, written through the library of DP-03; their fields are the library's and are not redefined here |

Three values the sources do not fix are this baseline's decision and are carried as placeholders. The two operations the sources never name are fixed here as BR10 — **Not specified in the source documents (GAP-0798; ASM-1494)**. The grant table and its field ids do not exist in any source, so the two schemas are named here and the physical columns are the DB story's — **Not specified in the source documents (GAP-0799; ASM-1493)**. The incident pattern and the register are **Not specified in the source documents (GAP-0797; ASM-1491)**.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/break-glass-grants` | `BreakGlassActivation` in with the `Idempotency-Key` header; `BreakGlassGrant` out, `ACTIVE` with its window | Platform administration C (API-P4-013) |
| POST | `/admin/break-glass-grants/{grantId}/end` | `BreakGlassGrant` out, `ENDED` with its ended time; the `Idempotency-Key` header; a repeated end returns the grant as it stands | Platform administration C (this revision's decision) |
| GET | `/admin/break-glass-grants/{grantId}` | `BreakGlassGrant`: the actor, incident, approval, area, right, scope, reason, window, state, marker and entry reference | Platform administration R (this revision's decision) |

Errors for all three: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 unknown grant (MSG-GEN-004), 409 a second active grant or a repeated key answered differently (MSG-GEN-004), 422 a missing or invalid field (MSG-GEN-001) or a length outside its bounds (MSG-GEN-002), 503 the record entry not written (MSG-P7-003) or the incident register not answering. The activation and the end are idempotent by `Idempotency-Key`; a same key returns the first answer. Major version 1 sits in the path (BR13).

The session `GET /me/session` (API-P4-012) is the service's operation of RWB-P4-E1019-APP and RWB-P4-E1037-CON; this document declares its `breakGlass` component and changes no other field of it. The access-log read `GET /admin/access-log` (API-P4-008) is RWB-P4-E1039-CON's and RWB-P4-AD007-CON's and appears nowhere here.

#### 12.2 REST operations consumed

None. The three operations are answered from `rwb_access`; the open state of the incident arrives through the incident-status port declared in this document as a port and not as a service call, and its owner is **Not specified in the source documents (GAP-0797; ASM-1491)**. Nothing else is consumed: no other service is called on the caller's thread, and the 2 s budget of DP-11 is not spent.

#### 12.3 Events published

None. **No event name is published by this capability.** Architecture v5 slide 14 gives `rwb-access` exactly two business events, `AccessPolicyChanged` and `DoaLimitChanged`, and slide 43 publishes them to all services for a cache refresh; **a break-glass grant is session state and not a policy change**, because it changes no permission row, no scope and no delegation limit, and because it ends by its own clock, so a consumer that refreshed on it would cache an entitlement that had already expired. The two readers of a grant are the guard and the session read, both inside this service and both reading `rwb_access` on the call (BR9, ASM-1495).

The one message a grant produces is the decision-record entry, and that message is the library's: `rwb.decision-record.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, written by the library of DP-03 (RWB-PLT-E1027-CON) in the CloudEvents 1.0 envelope, with the decision codes `AC-BGON`, `AC-BGREF` and `AC-BGOFF`, the actor reference, the incident, the area, the right, the scope, the window and the time. This document declares the codes and the fact; it declares no producer and no topic of its own, and no message carries a name, an e-mail address, an identity number or a case fact.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this capability adds no subscription.

#### 12.5 Workflows and activities

None. The three operations are synchronous REST answers in the caller's thread with no workflow, no activity and no signal, and the settle of an expired grant is one `UPDATE` inside the read transaction. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. Nothing about a grant runs on a clock other than the row's own `endsAt`: there is no expiry job and no Schedule, because the time check of the guard and the settle of the next read make a job unnecessary and a lost job harmless (BR6).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `break_glass_grant` | P4 (`rwb_access`); no row in the ownership map — **Not specified in the source documents (GAP-0799; ASM-1493)** | The grant: actor, incident, approval, area, right, scope, reason, window, state, ended time and marker; written by the activation, the end and the settle, read by the guard and the read |
| `role` | P4 (`rwb_access`) | The role code and the default scope of the caller (DF-REF-035, DF-REF-038); read only |
| `permission` | P4 (`rwb_access`) | The Platform administration letters and the capability areas of the caller (DF-REF-042, DF-REF-043); read only |
| the access log of RWB-P4-E1039-DB | P4 (`rwb_access`), RWB-P4-E1039-DB | Appears nowhere in this contract: the marker is stamped by the writer of RWB-P4-E1039-APP on the entry that contract defines |
| `decision_log_entry`, `approval` | P7 (`rwb_decision`) | Appear nowhere; the local entry is the library's and the central ledger is P7's |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Appear nowhere; the lists travel as codes and this capability reads no parameter contract (DP-01, DP-06 not applied) |
| `partner_user` | S9 (`rwb_partner`) | Appears nowhere; the ownership map gives partner users to S9 |

No foreign key crosses a schema, and the contract names no table outside `rwb_access`. The incident reference is a value and never a key.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` break-glass WireMock | The three paths of 12.1: the incident `INC0004521` open, the approval `IAM-778812`, the activation at 10:30 with a window of 4 hours and a grant `ACTIVE` until 14:30, the ended grant with its ended time, the stored answer for a repeated `Idempotency-Key`, 409 for a second activation with a different key, 404 for an unknown grant, 422 with MSG-GEN-001 and MSG-GEN-002, 403 with MSG-P4-002 and 503 with MSG-P7-003 | App story, contract tests, wave 4 harness |
| Incident-status stub | One open incident, one closed incident, and one reference that matches no incident | App story, contract tests |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | App story, contract tests |
| Access-log writer fake (RWB-P4-E1039-CON) | An entry carrying the grant id and the incident reference on an action inside the window | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed | The activation, the end and the read provided; one hop, 2 s timeout; the incident check is a port and not a call on this thread |
| Kafka | 0 published, 0 consumed | No event name of this capability; the library's `rwb.decision-record.DecisionRecorded.v1` is declared as a type, not as an event of this contract |
| Temporal | None | No workflow, activity or Schedule in this contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-break-glass-v1.yaml` (OpenAPI 3.1) with the three operations and the shared components, the schemas `BreakGlassActivation` and `BreakGlassGrant`, the session component `breakGlass` as a fragment for the API-P4-012 document of RWB-P4-E1019-CON, the `contract/error-envelope.yaml` with the agreed message IDs, the event statement of 12.3, the incident-status port declaration, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

A contract story adds no build dependency of its own: each DP above is **referred to; the consuming story carries the dependency**, and that story is RWB-P4-AD006-APP, whose H row carries RWB-PLT-E1027-CON and RWB-PLT-N001-CON. DP-03 is contracted as the entry the document declares on `rwb.decision-record.v1`; DP-05 is contracted as a bounded statement — this capability reads no ACE view, because a grant needs no party and no account, and the ACE group the emergency path depends on is the bank IAM's; DP-13 is the base of the document; DP-19 is the composite route that serves SCR-43.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The three operations and the two schemas of section 11, with the page-free single-resource answers and the `Idempotency-Key` on the two commands.
3. The bound and the expiry rule in the description of the three operations: one incident, one caller, one area, one right, one scope, one window, one `ACTIVE` grant per caller, the clock as the authority, and the settle on the next read (BR3, BR6, BR7).
4. The `breakGlass` session component and its absence rule, as a fragment for the API-P4-012 document.
5. The rights of the two commands and of the read, and the 401 and 403 of the default deny rule; the note that the legacy R of the permission check is the read's letter and C is the activation's.
6. The error envelope and the message-ID mapping, with the legacy texts copied unchanged and the one condition that has no text in the sources named.
7. The statement of 12.3: no event name is published, the library's decision-record type is declared with its three codes, and the reason a grant is not a policy change.
8. The four fakes and the stub fixtures of section 12.8.
9. The seven contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the consumer sign-off note of the app story, the guard, the session and the access log.

**Feature switch.** The contract carries no switch. The three operations are operations of the service; the activation is a command guarded by the C letter and the IAM approval, and nothing about a grant is behind a flag.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD006-APP | The three provided operations, the two schemas, the bound, the expiry rule and the four fakes |
| RWB-P4-E1037-CON and RWB-P4-E1037-APP, the guard | The `breakGlass` state, the expiry rule and the letters a grant adds |
| RWB-P4-E1019-CON and RWB-P4-E1019-APP, the session | The `breakGlass` component of API-P4-012 and its absence rule |
| RWB-P4-E1039-CON and RWB-P4-E1039-APP, the access log | The marker: the grant id and the incident reference on the entry of an action |
| The wave 4 harness | The fakes of 12.8 and the incident-status stub |

The deprecation window of a published field and the retention of the contract fakes are **Not specified in the source documents (GAP-0798; ASM-1494)**.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the four fakes answer every declared path, and the app story, the guard, the session and the access log have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without Platform administration C for the activation or the end, or without R for the read; or a call after the window end without the letter the action needs | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A grant of the caller is in force; the banner and the session | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, the incident is not open, the approval reference is unknown, or the area, the right or the scope is not a value of its list | Enter {field}. |
| MSG-GEN-002 | The reason or the window is outside its bounds | {field} must be between {min} and {max}. |
| MSG-GEN-004 | A second active grant, a repeated key answered differently, or an unknown grant | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision-record entry could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text, taken from the legacy story where the message already existed, and MSG-P4-004 carries the end time of the grant as its {time}. The one condition with no text in any source of this read set is the incident that exists and is not open: the document declares the 422 with MSG-GEN-001 naming `incidentReference`, and the text for that condition is **Not specified in the source documents (GAP-0797; ASM-1491)**.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | List | The grant read: the grants of the caller and of the estate that its letter reaches, with incident, area, right, scope, start, end and state |
| SCR-43 Roles and access | Activate | The activation request and the field-level 422 answers of the checks |
| SCR-43 Roles and access | Active | MSG-P4-004 with the end time, and the `breakGlass` field of the session |
| SCR-43 Roles and access | Activated | The written grant with its window, its state and its entry reference |
| SCR-43 Roles and access | Ended | The grant `ENDED` with its ended time; MSG-P4-004 is gone and the `breakGlass` field is absent |
| SCR-43 Roles and access | Refused | The 403 with MSG-P4-002 and no grant, and the 401 with MSG-P4-001 |
| SCR-43 Roles and access | Access log | The entries of the window, each carrying the grant id and the incident, through the access-log operation of RWB-P4-E1039-APP on the same composite route |
| SCR-43 Roles and access | Not available | The 503 with MSG-P7-003 |

The screens are served by the gateway-bff composite route (DP-19), which calls the grant read and the access-log read in parallel, one hop each, and merges the answers. The composite route specification, the screen field list and the column order are **Not specified in the source documents (GAP-0798; ASM-1494)**; the document fixes the grant side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-006-01 | AC1 | Contract | Legacy test "Granted with an incident" on the contract side: the incident `INC0004521`, the approval `IAM-778812`, the area `CASE_RECORD`, the right `U`, the scope `ALL`, a reason of 46 characters and a window of 4 hours are the values of the fixture; the activation answers a grant `ACTIVE` until 14:30 with the marker, so the app story can prove the behaviour; the behaviour itself is tested there at End to end |
| TC-AD-006-02 | AC2 | Contract | Legacy test "Refused without an incident" on the contract side: an incident that is not open is declared refused with 422 and MSG-GEN-001 naming `incidentReference`, no grant is declared as written, and the refusal entry is declared on `rwb.decision-record.v1` |
| TC-AD-006-03 | AC3 | Contract | Legacy test "Ends on its own" on the contract side: the document declares the clock as the authority over `endsAt`, the settle to `ENDED` on the next read and the absence of any event, job or call that ends a grant; the fixture shows the grant in force before the end and out of force after it |
| TC-AD-006-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": a caller with no Platform administration letter is declared refused on all three operations, and the document declares the 403 with MSG-P4-002 and the refusal entry |
| TC-AD-006-05 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the document declares the 503 with MSG-P7-003 and the fake answers it, so no consumer treats a refused activation as written |

The five legacy test cases are kept with their IDs and their legacy Covers values, and the legacy test name is written in the Data column. The Level column follows Template and Rules §R7.2: the three grant operations, the bound and the expiry rule are tested against the artefact at Contract, the legacy Access row stays Component, and the legacy Principle 5 row stays NFR. The behaviour of each case in the running service is RWB-P4-AD006-APP's at End to end, and the full test with its Given, When and Then is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD006-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in the contract: the window hours, the incident pattern and the reason bounds are data, the lists travel as codes, and the document fixes names and types only.
- No personal data in a schema, an example or a fake: the actor is a staff user reference and the reason is the only free text; a name or an e-mail address in the document fails the review (BR12).
- The contract names only `rwb-access` tables and operations owned by `rwb-access`, and no operation or table of another service (DP-01, BR1).
- One REST base and no event name of the capability's own: a document that declares an `rwb.access.*` event for a grant fails the review (DP-13, BR9).
- A grant without an end is not a grant: the document declares `endsAt` required and after `startsAt`, and the state vocabulary is `ACTIVE` and `ENDED` (BR6, BR7).
- The clock is the only authority over the window, so no consumer reads a row as an entitlement and no job is trusted to end a grant (BR6).
- The access-log entry is declared by its owner and only the marker is declared here, so the two contracts cannot drift into two entry shapes.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- Every example and every fake is synthetic; no production incident, person or entitlement is copied into a schema or a fake.

### 18. Traceability

The Work Package carries the requirement list of this key as empty, and TSD P4 v3 T8 maps REQ-ACA-008 to the sign-in story RWB-E1-022; FSD P4 v3 records REQ-ACA-008 as "A break-glass path exists for an emergency, needs its own approval, and writes to the access log", must, first in E1, with FEAT-ACA-09 and FEAT-ACA-10. This contract is the ground of the path and of its own approval; the access-log half is RWB-P4-E1039-CON's.

| Feature | Contract element | Test cases |
|---|---|---|
| FEAT-ACA-09, use break-glass access with an incident reference | The activation, the incident reference and the bound of 12.1 and 12.7 | TC-AD-006-01, TC-AD-006-02 |
| The own-approval rule of REQ-ACA-008 | The `iamRequestId` and the `approverReference` of the two schemas (BR5) | TC-AD-006-01 |
| The self-expiry the legacy criterion asks for | The clock rule of BR6 and the settle of 12.1 | TC-AD-006-03 |
| The default deny rule and the recorded refusal | The 401 and 403 of 12.1 and the decision-record type of 12.3 | TC-AD-006-02, TC-AD-006-04 |
| The record-before-change rule | The 503 with MSG-P7-003 and the entry reference of the written grant | TC-AD-006-05 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1, AC2 and AC3 | The behaviour of RWB-P4-AD006-APP; this contract carries the elements they are tested against, and section 16 keeps their test cases |
| `20 characters` of the reason, the window and the open incident | Sections 3, 7, 11 |
| The Data table: `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7 |
| The permission check Platform administration and the roles that hold it | Section 12.1, section 8 (BR2, BR10) |
| MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-002, MSG-GEN-004, MSG-P7-003 | Section 14, exception paths |
| Screen SCR-43 Roles and access | Section 15 |
| Legacy test cases TC-AD-006-01 to TC-AD-006-05 | Section 16 |

### 19. Out of scope

- The implementation of the three operations, the checks, the window, the guard extension, the record entries and the settle: RWB-P4-AD006-APP.
- The grant table, its constraints, its indexes, its retention and the per-service login: RWB-P4-AD006-DB.
- The access log, its entry shape, its writer and the administration surface that lists the grants: RWB-P4-E1039-CON, RWB-P4-E1039-APP and RWB-P4-E1039-DB. This contract declares only the marker that the entry carries.
- The access-log search and export: RWB-P4-AD007-CON and RWB-P4-AD007-APP.
- The session read itself and its other fields, the permission matrix, the masking rows and the role conflicts: RWB-P4-E1019-CON, RWB-P4-E1037-CON, RWB-P4-E1037-APP and RWB-P4-E1019-APP. This contract declares the `breakGlass` component only.
- The separation-of-duty check at sign-in and the sign-in: RWB-P4-AD005-CON, RWB-P4-AD005-APP and RWB-P4-E1022-APP.
- The reference data and the parameter values of the estate, and any parameters contract: P3 rwb-case; this contract declares no parameter read and no table of it.
- The central decision ledger and its query: P7 rwb-decision; the local entry is the library's.
- `partner_user`: S9 rwb-partner.
- The bank IAM's group administration and approval workflow, and the incident register: Entra ID, the bank IAM (INT-21) and the incident owner, which no source fixes (GAP-0797; ASM-1491).
- The deployment of the capability: the Helm values, the topic ACLs, the dashboards and the runbook.
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD006-ITG.
- The field-level completeness of the two schemas beyond what section 11 fixes (GAP-0798; ASM-1494).
