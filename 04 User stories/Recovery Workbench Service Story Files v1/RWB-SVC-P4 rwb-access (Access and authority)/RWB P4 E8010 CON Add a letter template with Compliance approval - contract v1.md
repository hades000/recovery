# RWB-P4-E8010-CON Add a letter template with Compliance approval

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-010 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the template approval gate of `rwb-access`: an OpenAPI 3.1 document for the approval and the history, the `TemplateApproval` and `TemplateApprovalHistory` schemas with the approving role code and no person, the state set of a template version as `rwb-comms` publishes it and the one approval state this gate records, one RFC 9457 error envelope with its message IDs, the consumed authorise, parameters and two `rwb-comms` operations with their owners and the 2 s budget, the contract tables of section 12 and the five contract fakes**, so that **the app story, the SCR-33 route, the `rwb-comms` team and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or `rwb-comms` to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-010 belong to RWB-P4-E8010-APP, and the six criteria of section 7 test the document, the schemas and the state set, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story approved a letter template inside a screen of the monolith, where the template, its approval and the decision log were rows of one schema and no other service had to agree on what "approved" meant. In the target the template is `rwb-comms`'s (Architecture v5 slide 41) and the approval of a version is a decision of the access service that has to reach the template owner as a call and has to leave a record that audit can read years later.

Two things must therefore be fixed once. The first is the boundary: which operation owns the state change (the P6 approve operation, API-P6-006) and which owns the authority and the record (this gate). The second is what the record says: the template id, the version, the approving **role code** and the time — and never the person — because the record of an approval is the evidence that REQ-OCC-002 asks for, and a record that carries the approver's name would copy personal data into a shared topic that every consumer of the decision record reads.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with `rwb-comms`, the parameters contract of `rwb-case` and the local decision-record library, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also states the one thing it is not: it defines no template, no notice and no merge field, and it names no table of `rwb-comms` as this service's. The two P6 operations appear in the document as consumed, which is what makes the split real.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two operations behind SCR-33 Template approval, and it is a consumer of this baseline.
- The `rwb-comms` template operations are described by TSD P6 v2 appendix T-A: API-P6-003 `GET /admin/templates`, API-P6-004 `POST /admin/templates` (a new version in state `DRAFT`), API-P6-005 `GET /admin/templates/{templateId}/content`, API-P6-006 `POST /admin/templates/{templateId}/approve` with a `TemplateApproval` request and a `Template` answer, and API-P6-007 `POST /admin/templates/{templateId}/withdraw`. The template table fields are TSD P6 v2 T3.1 DF-REF-045 to DF-REF-065 and its standard record columns T3.0. This document consumes two of those operations and defines none of them.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The approval entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields this gate records and no field of another service.
- The operations and their owners are taken from the ownership map only: the two operations of this document are P4's, the authorise operation is P4's, the parameters read is P3's and the two template operations are P6's. No table of another service is named as this service's (DP-01). The `rwb-comms` operations are consumed although this story's metadata carries no P6 contract dependency (GAP-0871; ASM-1580).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the approval and the history with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the two schemas.
2. Fix the `TemplateApproval` request and answer schemas with the fields of section 11: `templateId`, `templateVersion`, `productGroup`, `approvalReference`, `validFrom`, `reason` in, and `approvalId`, `templateId`, `templateVersion`, `productGroup`, `state`, `approvedByRole`, `approvedAt`, `validFrom` out — and no person field of any kind.
3. Fix the `TemplateApprovalHistory` schema and the query parameters of the read, with the page default and maximum held as parameter rows behind the contract.
4. Fix the state set: the template states `DRAFT`, `APPROVED` and `WITHDRAWN` as `rwb-comms` publishes them, and the one approval state this gate records, `APPROVED`; state in the document that only a version in `DRAFT` may be approved and that this service writes no template state.
5. Agree the error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-P7-002 carried as a message ID only.
6. Declare the consumed own authorise operation, the `rwb-case` parameters read and the two `rwb-comms` operations as consumed, each with its owner, one hop and the 2 s client budget; declare `POST /admin/templates`, `GET /admin/templates/{templateId}/content` and `POST /admin/templates/{templateId}/withdraw` as neither provided nor consumed here.
7. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
8. Add the contract tests: schema validation, the two schemas and their required fields, the state set, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-E8010-APP, the SCR-33 route of RWB-PLT-N001-CON, the `rwb-comms` tech lead and the harness of the wave 4 access journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares a template operation as provided here | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A schema carries a name, an e-mail address, a user reference of the approver or another personal field | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A state outside `DRAFT`, `APPROVED` and `WITHDRAWN` is declared for a template version, or a state is declared as written by this service other than the recorded approval `APPROVED` | The review refuses the document | None | AC3 |
| X6 | The document declares a template, notice or merge-field table as this service's, or declares the P6 approve operation as provided | The review refuses the document | None | AC3, AC5 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the P6 appendix T-A, the DP-03 entry schema and the P3 and P4 contracts only |
| Negotiable | The approval-reference shape and the page bounds are parameter rows behind the document; the base, the paths, the state set and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-33 route and the harness on Day 1, and keeps the person out of the record of an approval |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Add a letter template with Compliance approval contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the letter templates are held by rwb-comms and the approval gate of a template version is rwb-access's

  Scenario: AC1 The OpenAPI 3.1 document describes the approval and the history (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the template approval gate is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/template-approvals and GET /admin/template-approvals/{templateId} with the owner rwb-access
    Then the approval names Rules and parameters A, the history names Rules and parameters R, and both name their error responses 401, 403, 409, 422 and 503
    Then the approval requires an Idempotency-Key and the history is a read that carries none
    Then no operation of rwb-comms is declared as provided by rwb-access

  Scenario: AC2 The approval and history schemas are fixed and carry no person (new, D-RCV-60)
    Given the TemplateApproval and TemplateApprovalHistory schemas of the document
    Then the request carries templateId, templateVersion, productGroup, approvalReference, validFrom and reason, all required
    Then the answer carries approvalId, templateId, templateVersion, productGroup, state, approvedByRole, approvedAt and validFrom
    Then the history carries templateId, items of templateVersion, state, approvedByRole, approvedAt and approvalReference, page, size and total
    Then approvedByRole is a role code and no schema declares a name, an e-mail address or a user reference
    Then page and size are read from the parameters contract and never from code, and approvalReference is validated against a parameter row

  Scenario: AC3 The state set is fixed and this service writes no template state (new, D-RCV-60)
    Given the state set of a template version in the document
    Then state is one of DRAFT, APPROVED and WITHDRAWN as rwb-comms publishes it
    Then only a version in DRAFT may be approved, and a state that is not DRAFT is a 409
    Then the only state this service records on its own approval entry is APPROVED
    Then the document states that the state, approved_by, approved_at and valid_from of a version are written by rwb-comms and not by rwb-access
    Then the document names no template, notice or merge-field table as this service's
    Then no workflow and no Schedule is declared for the capability

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002 on an absent right and MSG-P7-002 on an approval by the author of the version
    Then 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then no operation declares a second error shape and MSG-P3-022 belongs to no response of this document

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the parameters read and the two template operations this service calls
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then GET /api/recovery/comms/v1/admin/templates/{templateId} and POST /api/recovery/comms/v1/admin/templates/{templateId}/approve are declared as consumed with the owner P6 rwb-comms
    Then each carries one hop and the 2 s client budget with a breaker
    Then POST /admin/templates, GET /admin/templates/{templateId}/content and POST /admin/templates/{templateId}/withdraw appear as neither provided nor consumed here
    Then no operation owned by rwb-comms, rwb-case or rwb-decision is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the template fake answers a version with its state, its product group and its author reference only, and no body and no merge field
    Then no schema, example or fake carries a name, an e-mail address or a personal field, and no answer of this service carries a user reference
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-010 belong to RWB-P4-E8010-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR4 | The schemas carry the fields of this gate and no field of another service: no template body, no merge field and no notice | DP-01; Ownership Map v1 (`template`, `notice`, `merge_field` = P6) |
| BR5 | The approving role is a role code; no schema, example, fake or entry of this contract carries a name, an e-mail address or a user reference of the approver | NFR-040; ASM-1582 |
| BR6 | The state set of a template version is `DRAFT`, `APPROVED` and `WITHDRAWN` as `rwb-comms` publishes it, and the only state this service records is `APPROVED`; the state change is the P6 approve operation's | API-P6-004, API-P6-006, API-P6-007; ASM-1580 |
| BR7 | The two `rwb-comms` operations are consumed with their owners, one hop and the 2 s budget, and the missing P6 contract dependency is carried in the gap and not added to the metadata | Ownership Map v1; GAP-0871; ASM-1580 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |
| BR9 | A write requires an `Idempotency-Key`; a replay answers the first answer and makes no second handoff | Architecture v5 slide 42; DP-09; API-P6-006 |
| BR10 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 |
| BR11 | The change checklist and the checksum of TSD P4 v3 T6.3 belong to a rule package version; this document declares no checklist field and no checksum field and no MSG-P3-022 | TSD P4 v3 T6.3; FSD P4 v3 A2.21 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the state set and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-33 route, the `rwb-comms` tech lead and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The P6 read or approve operation, or the parameters read, changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for a template version is `DRAFT`, `APPROVED` and `WITHDRAWN` with `rwb-comms` as its writer; the approval state this service records on its own entry is `APPROVED`, written once per version. The lifecycle of a rule package version — including `LOADED`, `REFUSED`, `SUPERSEDED` and `ROLLED_BACK` — is another capability's and is not declared here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the state set and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Compliance and PDPA officer, as the approver of a version | Reviews the approval operation, the approving role code and the four-eyes message ID |
| Tech lead of rwb-comms (P6) | Reviews the two operations as `rwb-access` consumes them and owns their definitions, their states and the approve schema |
| Tech lead of rwb-case (P3) | Reviews the parameters read as `rwb-access` uses it; owns its definition |
| Internal audit | Reviews the history fields, the absence of a person in the record and the stable order of the read |
| Data steward | Confirms that no name, e-mail address, personal field or approver user reference is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| `TemplateApproval` request | `templateId`, `templateVersion`, `productGroup`, `approvalReference` (validated against a parameter row), `validFrom` (a date), `reason`; all required |
| `TemplateApproval` answer | `approvalId`, `templateId`, `templateVersion`, `productGroup`, `state` (`APPROVED`), `approvedByRole` (a role code), `approvedAt` (the `approved_at` `rwb-comms` answered, DF-REF-064), `validFrom` (DF-REF-065) |
| `TemplateApprovalHistory` | `templateId`, `items[]` of `templateVersion`, `state`, `approvedByRole`, `approvedAt`, `approvalReference`, `page`, `size`, `total` |
| Template version, as consumed | `templateId` DF-REF-045, `template_code` DF-REF-046, `template_version` DF-REF-047, `language` DF-REF-048, `product_group` DF-REF-049, `body_ref` DF-REF-050, `approved_by_legal` DF-REF-051, `approved_by` DF-REF-063, `approved_at` DF-REF-064, `valid_from` DF-REF-065, and the standard record columns `state` and `created_by` of TSD P6 v2 T3.0 |
| Roles and letters | The approving role code and the capability areas of `role` DF-REF-034 to DF-REF-039 and `permission` DF-REF-040 to DF-REF-044, read behind the authorise answer |
| Record event | `rwb.decision-record.DecisionRecorded.v1` with the entry of an approval, from the DP-03 library |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 and MSG-P7-002 on a 403, MSG-GEN-004 on a 409, MSG-GEN-001 on a 422 and MSG-P7-003 on a 503 |

The exact request and answer field set of the two operations, the type and length of each field, the shape of `approvalReference` and the record code of an approval are Not specified in the source documents (GAP-0871; ASM-1580): FSD P4 v3 A2.21 names the journey and two rules (VR-P4-021-1, BR-P4-021) and no operation and no field, and the P6 appendix declares the template operations and not this gate. The read of a single template by its id is Not specified either — the ownership map and TSD P6 v2 appendix T-A declare `GET /admin/templates` with a code filter — so the path is fixed here and raised with the P6 owner (GAP-0871; ASM-1580). The approving role and the four-eyes rule are Not specified in the fields of the template table, which carries `approved_by` and no author: this document reads the author from the standard record column `created_by` of TSD P6 v2 T3.0 (ASM-1581). The P6 appendix also names its approve request `TemplateApproval` (API-P6-006); this document's `TemplateApproval` is the `rwb-access` approval of a version and the consumed P6 request is declared by reference to its operation, so the two are not confused in the document's components.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/template-approvals` | `TemplateApproval` in; `TemplateApproval` out in state `APPROVED` with `approvalId`, `approvedByRole`, `approvedAt`, `validFrom` and the `Location` of the history read | Rules and parameters A, and the caller is not the author of the version; `Idempotency-Key` required |
| GET | `/admin/template-approvals/{templateId}` | `TemplateApprovalHistory` out: one item per approved version with `templateVersion`, `state`, `approvedByRole`, `approvedAt` and `approvalReference`, paged | Rules and parameters R, scope applied |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002) and an approval by the author of the version (MSG-P7-002), 409 the version is not in `DRAFT` or its state moved before the handoff (MSG-GEN-004), 422 a required field empty or a value of the wrong shape (MSG-GEN-001), 503 `rwb-comms` cannot be reached or the entry cannot be written (MSG-P7-003). The approval is a write, so every request carries an `Idempotency-Key` and a replay answers the first answer with no second handoff (BR9); the history is a read and carries none. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The two paths are fixed here (GAP-0871; ASM-1580) and confirmed by the contract review before they are frozen. No template operation is declared as provided in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The A check behind the approval and the R check behind the history, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The approval-reference shape and the page bounds, with the version in force (DP-06) |
| GET | `/api/recovery/comms/v1/admin/templates/{templateId}` | P6 rwb-comms | The template version: its `templateVersion`, `state`, `authorReference` and `productGroup`, before the gate decides |
| POST | `/api/recovery/comms/v1/admin/templates/{templateId}/approve` | P6 rwb-comms | The handoff of the approval with its `valid_from` and the approval reference and the forwarded `Idempotency-Key`; P6 answers the template in state `APPROVED` |

None of the four is declared as provided by rwb-access. Of the two `rwb-comms` operations, the approve is API-P6-006 of the P6 appendix T-A and is consumed here; the read by id is not in that appendix, so it is the path this contract fixes and it is raised with the P6 owner in GAP-0871 and ASM-1580; this story's metadata contract-dependency list carries neither, which is the missing dependency of the same rows and is not added to the metadata. `POST /admin/templates`, `GET /admin/templates/{templateId}/content` and `POST /admin/templates/{templateId}/withdraw` appear nowhere in this document as provided or consumed.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of an approval with its template id, version, product group, approving role code, approval reference and time, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and `rwb.access.DoaLimitChanged.v1` is RWB-P4-E8008-APP's, and a template approval publishes neither (Architecture v5 slide 14); no template change is announced on `rwb.access.events.v1` by this gate, because the owner of the template announces its own changes.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, and the two operations of this contract need no subscription. The document declares no inbox and no consumer group, and no template or notice event is consumed.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the approval is synchronous and the four-eyes rule is a right. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only (BR10).

#### 12.6 Schedules

None. Both operations are request-driven, and the effective date of an approval is data and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code recorded as the approving role |
| `permission` | P4 (rwb_access) | The A and R letters of Rules and parameters and the role they are held through |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The approval entry the record event carries and the history the read answers |
| `idempotency_key` | PLT library, created in rwb_access | The stored request and answer of an approval, so one key answers one approval (DP-09; ASM-0074) |

No table of another service is named in the contract (DP-01): `template`, `notice` and `merge_field` are P6 rwb_comms's and their fields arrive in the consumed answer; `decision_log_entry` and the rule registry are P7 rwb_decision's; `case`, `task` and `lov_value` are P3 rwb_case's. No template table is created, copied or named as this service's, and the document holds no template body and no merge field (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| template fake | `GET /admin/templates/{templateId}` answering "TPL-SETTLE-EN" version "3" in `DRAFT` for `MORTGAGE` with author reference "U-6101", version "2" in `APPROVED`, a version in `WITHDRAWN` and a 503; `POST /admin/templates/{templateId}/approve` answering the template `APPROVED` with `approved_at` and `valid_from`, a 409 for a state that moved and the same answer for a repeated `Idempotency-Key` (GAP-0871; ASM-1580) | App story, contract tests, harness |
| authorise fake | `POST /authorise` with a granted answer for RW-COMPLY and RW-COE with A and for RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-CASEOWN with R only | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the approval-reference shape and the page bounds at the version in force | App story, contract tests |
| decision-record fake | The append of an approval, the hash-link check, a seeded history of versions "2" and "3" and a forced failure | App story, contract tests |
| gateway-bff fake | The composite route of SCR-33 with the template as `rwb-comms` answers it, the approval form and the history panel | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The approval and the history provided; the authorise, parameters and two template operations consumed; one hop, 2 s timeout |
| Kafka | 1 event type published, 0 consumed | `rwb.decision-record.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; a template body is downloaded through API-P6-005 and never through this document |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-template-approval-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the `TemplateApproval` request and answer schemas and the `TemplateApprovalHistory` schema with their examples, the state-set rule and the versioning rules in the contract README, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The two `rwb-comms` operations are consumed and faked, and the missing P6 contract dependency is carried in the gap row of the key and not added to this story's metadata (GAP-0871; ASM-1580).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two operations with the shapes of section 11: the request and the answer of the approval, the history and its paging, and the required fields.
3. The state set of BR6, stated in the document and in the contract README, with the ownership of each state named: `DRAFT`, `APPROVED` and `WITHDRAWN` by `rwb-comms`, and `APPROVED` recorded by this service on its own entry.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget, and the explicit statement that no template operation is provided here.
5. The error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the texts of the legacy messages and MSG-P7-002 as an ID only.
6. The five fakes and the stub fixtures of section 12.8, including the `DRAFT`, `APPROVED` and `WITHDRAWN` versions of "TPL-SETTLE-EN".
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the SCR-33 route, the `rwb-comms` tech lead and the harness.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8010-APP | The two provided operations, the two schemas, the state set and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-33) | The approval and the history as the form and the history panel call them |
| The `rwb-comms` tech lead | The two template operations as consumed, with the read-by-id path and the approve request, and that no template table or body is claimed here |
| The harness of the wave 4 access journey | The approving role code, the times and the approval reference, as the evidence it records |

The shape of `approvalReference` and the record code of an approval are Not specified in the source documents (GAP-0871; ASM-1580): the reference is validated against a parameter row and the record code is the library's approval code, and both are confirmed with Compliance and with the decision-record library owner before the operations are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, the `rwb-comms` tech lead has accepted the two consumed operations, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters A approves, or a role without R reads the history | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, `templateVersion` is not a whole number, `validFrom` is not a date, or `approvalReference` is not of the shape in force | Enter {field}. |
| MSG-GEN-004 | The template version is not in state `DRAFT`, or its state moved before the handoff | Someone else changed this record. Reload it to see their change. |
| MSG-P7-002 | The caller is the author of the version being approved | Not specified in the source documents (GAP-0871; ASM-1580) |
| MSG-P7-003 | `rwb-comms` cannot be reached, or the approval entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P7-002 carries a message ID and no text in this baseline, because TSD P4 v3 T6.3 states the four-eyes rule and not its wording; the message catalogue supplies the text before the operations are frozen. MSG-P3-022, the missing checklist item, is declared on no response of this document, because a template version carries no change checklist (BR11), and MSG-P4-003, the legacy scope message, is declared on no response either, because a letter template is not a case and this gate scopes no case.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-33 Template approval | Versions, list | The template as `rwb-comms` answers it, each version with its state |
| SCR-33 Template approval | Approval, form | `TemplateApproval` request with `templateId`, `templateVersion`, `productGroup`, `approvalReference`, `validFrom` and `reason` |
| SCR-33 Template approval | Approval, recorded | `TemplateApproval` answer in state `APPROVED` with `approvedByRole`, `approvedAt` and `validFrom` |
| SCR-33 Template approval | Approval, not a draft | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-33 Template approval | Approval, by the author | The 403 of the envelope with MSG-P7-002, the version unchanged |
| SCR-33 Template approval | Approval, refused | The 403 of the envelope with MSG-P4-002 |
| SCR-33 Template approval | History | `TemplateApprovalHistory` with the version, state, approving role code, time and approval reference of each approved version |
| SCR-33 Template approval | History, empty | An empty `items` with total 0 and no error |
| SCR-33 Template approval | Not recorded | The 503 of the envelope with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |

The screens are served by the gateway-bff composite route (DP-19), which shows the template from `rwb-comms` and calls the two operations of this contract, one hop each. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the P6 screen work; the document fixes the approval side of the merge only. The upload, the content download and the withdrawal of a version are `rwb-comms`'s and are not part of this document.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-010-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the rights A and R, the five error responses and the `Idempotency-Key` on the write are present; no template operation is provided |
| TC-E8-010-CON-02 | AC2 | Contract | The request and answer fields of `TemplateApproval` and the fields of `TemplateApprovalHistory`; the required fields; `approvedByRole` as a role code; no name, e-mail address or user reference |
| TC-E8-010-CON-03 | AC3 | Contract | The three template states, the one recorded approval state, the single writer of a version's state, and no template, notice or merge-field table named as this service's |
| TC-E8-010-CON-04 | AC4 | Contract | A 401, 403, 409, 422 and 503 response carry one problem envelope with a valid message ID, 403 carries MSG-P7-002 for an approval by the author, and MSG-P3-022 is on no response |
| TC-E8-010-CON-05 | AC5 | Contract | Four consumed operations with their owners P4, P3 and P6, one hop and the 2 s budget; the create, content and withdraw operations declared as neither provided nor consumed |
| TC-E8-010-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; the template fake carries no body and no merge field, and no schema or fake carries a name or a personal field |

### 17. Guardrails

- No business value in the contract: the approval-reference shape and the page bounds stay parameter rows behind the document, and the role codes stay rows of `role` and `permission`.
- No personal data in a schema, an example or a fake: template ids, versions, product groups, role codes, approval references and times only, and no approver user reference in any answer (BR5).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; `template`, `notice` and `merge_field` are `rwb-comms`'s and are consumed or absent, never named as this service's (BR4).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- One writer of a template state: the document states that the state, `approved_by`, `approved_at` and `valid_from` of a version are written by `rwb-comms` and never by this service (BR6).
- The two `rwb-comms` operations are consumed and faked, and the missing P6 contract dependency is carried in the gap rather than added to the metadata (BR7).
- Every example in the document is synthetic; no template body, notice or production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` is refused by the contract, and a replay never makes a second handoff.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices are generated from templates approved by Legal, with merge fields from case data and no re-keying | The approval operation as the only gate that authorises a version, and the state set with `rwb-comms` as the writer; the generation itself is P6's | TC-E8-010-CON-01, TC-E8-010-CON-03 |
| REQ-OCC-002 | Letter templates are versioned, and the Legal approval is recorded against the version | `TemplateApproval` with `templateVersion`, `approvedByRole`, `approvedAt` and `validFrom`, and the history read over the recorded approvals | TC-E8-010-CON-02, TC-E8-010-CON-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two operations as the SCR-33 route consumes them, with the four-eyes message ID and the refusal shapes | TC-E8-010-CON-04, TC-E8-010-CON-05 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 add a letter template with Compliance approval, the approval path and the record of who approved it | Sections 4, 7 (AC1, AC2), 11, 12.1, 12.2 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 7 (AC1, AC5), 10, 12.1, 14 |
| The legacy data rows `template` DF-REF-045 to DF-REF-051 and `role` DF-REF-034 to DF-REF-038 | Section 11, section 12.7 |
| The legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried to SCR-33 Template approval |
| Legacy key RWB-E8-010, story RWB-P4-E8010-APP, contract RWB-P4-E8010-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the approval and the history (RWB-P4-E8010-APP).
- The letter template itself and every P6 template operation: the upload of a version in `DRAFT`, the content download, the approve mechanics that write the state and `approved_at`, and the withdrawal (P6 `rwb-comms`; API-P6-003 to API-P6-007). This document consumes two of those operations.
- The generation of a letter or a notice from an approved template, its merge fields and its dispatch (FEAT-OCC-01 and the P6 stories).
- The central decision ledger, the query API over `rwb_decision` and the chain verification (P7 `rwb-decision`).
- The permission matrix, the role administration and the masking policy (RWB-P4-E1037-APP and the Epic 8 administration stories).
- The rule-change request, its seven-item checklist and its checksum (RWB-P4-E8007-APP and the registry of `rwb-decision`).
- The screen SCR-33 Template approval, its other panels and its composite route specification (RWB-PLT-N001-CON and the P6 screen work).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation, the `rwb-case` parameters read and the two `rwb-comms` operations are consumed and faked, never defined here.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
