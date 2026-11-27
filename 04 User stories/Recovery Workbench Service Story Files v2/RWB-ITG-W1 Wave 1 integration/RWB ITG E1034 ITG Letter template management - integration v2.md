# RWB-ITG-E1034-ITG Letter template management

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1034-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-034 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Set by the squad at refinement; not specified in the source documents (DOR-RWB-ITG-E1034-ITG-16) |
| Patterns applied | DP01, DP07, DP13, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | rwb-comms 5.0.0 and rwb-source-data 5.0.0 (API Specification v5, info.version); the paths use /v1 |
| Integration dependencies | RWB-P1-E1015-APP, RWB-P6-E1034-APP (integration only, not build dependencies) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-OCC-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-034 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1034-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-034 letter template management on P6 rwb-comms — upload, approve, set current, withdraw and the merge-code, file-type and self-approval refusals — with the freshness stamp of the reference data product read from P1 rwb-source-data**, so that **Legal approval of letter wording and its effect are proved on the real wave 1 services with no change to the built behaviour**.

### 2. Business rationale

The legacy story is recorded as Moved (no impact). Its five operations, its three version states and its ten messages are unchanged in the target, and they change owner and base only. The template and merge_field tables belong to P6 rwb-comms (Ownership Map rows template and merge_field, both P6), the five operations are served under `/api/recovery/comms/v1` instead of the monolith base (DP-13), and SCR-33 Template approval is reached through gateway-bff (DP-19). Nothing in the built behaviour moves, so this story is proof and not rework.

One element of the story crosses a service boundary. The reference data behind the screen is shown with the freshness stamp that P1 rwb-source-data keeps for its data products (RWB-E1-015; RWB-P1-E1015-APP), and that stamp is read through the P1 data product contract. The merge field catalog itself is P6's own table set (DP-07), and the template body stays in the P6 schema with a write-once store (DP-01), so no other service reads a comms table.

The split is as follows. This ITG story owns no legacy acceptance criterion. Legacy AC1 to AC10 sit at component level with RWB-P6-E1034-APP, which builds the upload, the approval, the set-current rule, the withdrawal and the four refusals inside P6 rwb-comms. This story proves the same behaviour through the published P6 contract, adds AC11 for the role refusal at the contract edge and AC12 for the freshness stamp of the reference data product, and adds nothing to the built behaviour.

No service contract is faked. Every call goes to the real SIT service under its published wave 1 contract. Where the sources do not name the moved base and the route of the five operations, the suite asserts through the P6 contract and records the open point as Not specified in the source documents (GAP-0357; ASM-0458). The same holds for the composite route of SCR-33 through gateway-bff (GAP-0357; ASM-0459), for the data product whose stamp the catalog shows (GAP-0357; ASM-0460) and for the point at which a withdrawal holds generation (GAP-0357; ASM-0461).

The measure is unchanged from the legacy story: it serves REQ-OCC-002 and control CTL-14, because every notice is produced from the current Legal-approved version. It removes the developer from template changes and keeps the approver and the approval date on the version.

### 3. Preconditions

- RWB-P6-E1034-APP is done: the five operations, the three version states and the ten messages run on P6 rwb-comms and are in SIT.
- RWB-P1-E1015-APP is done: the freshness stamp per data product is published and deployed on P1 rwb-source-data.
- The P6 and P1 contracts are deployed under their per-service bases behind gateway-bff.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic templates and its synthetic users.
- The merge field catalog is loaded with codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE".
- Synthetic users hold RW-LITOFF and RW-LEGAL; the approver of a version holds RW-LEGAL with Documents A.
- The write-once storage for template bodies is available in SIT (DL27), and the allowed file-type list carries DOCX.
- The template DEMAND-MTG in language TH has version 2 Approved by "LEG-0001" with valid from 2026-11-01, and the suite clock reads 2026-11-20.
- No production data is used, no production copy is loaded and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds the synthetic templates and users of the harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: signs in as "LIT-0101" holding RW-LITOFF and as "LEG-0001" holding RW-LEGAL through gateway-bff.
3. Harness: reads the template list with GET /api/recovery/comms/v1/admin/templates and asserts version 2 of "DEMAND-MTG" "TH" as current with approver "LEG-0001".
4. Harness: uploads "demand-mtg-th-v3.docx" with POST /api/recovery/comms/v1/admin/templates using merge codes "CASE_NO" and "TOTAL_OUTSTANDING", and reads the new version in state Draft.
5. Harness: reads the body with GET /api/recovery/comms/v1/admin/templates/{templateId}/content and asserts the stored body and its merge codes.
6. Harness: approves version 3 with POST /api/recovery/comms/v1/admin/templates/{templateId}/approve and valid from 2026-11-20, then reads the list and asserts version 3 as current and version 2 still readable.
7. Harness: withdraws version 3 with POST /api/recovery/comms/v1/admin/templates/{templateId}/withdraw and reason "Wording under review", and reads the list again.
8. Harness: runs the negative cases — set current with no approver, self-approval, an unknown merge code, an empty code, a PDF, valid from in the past, two approvals within the same second and a repeated approval.
9. Harness: reads GET /api/recovery/source-data/v1/data-products/freshness and checks the stamp shown for the reference product of the template catalog against the value the template list carries.
10. Harness: writes the evidence report with each status, message, version number and state.
11. Harness: removes the synthetic fixtures and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Set current is chosen on a version with no approver | Refused; the version stays Draft and the earlier version stays current | MSG-P6-005 | AC2 |
| X2 | The uploader of a version tries to approve it | Refused with 409; the version stays Draft | MSG-P7-002 | AC3 |
| X3 | The body uses a merge code not in the catalog | Upload refused with 422; no version is created and no file is stored | MSG-P6-006 | AC4 |
| X4 | The template code is empty | Upload refused with 422; nothing is created | MSG-GEN-001 | AC5 |
| X5 | The file is not a DOCX file | Upload refused with 415; nothing is stored | MSG-P6-010 | AC6 |
| X6 | Valid from is before today | Approval refused with 422; the version stays Draft | MSG-GEN-003 | AC7 |
| X7 | Legal counsel withdraws the current version | The version moves to Withdrawn, the code and language have no current version and generation holds | MSG-P6-003 | AC8 |
| X8 | Two approvers act on the same version at once | The first wins; the second is refused with 409 and the version keeps one approval | MSG-GEN-004 | AC9 |
| X9 | Approve is sent twice with the same Idempotency-Key | The first response returns with 200 and one approval stays on the record | None | AC10 |
| X10 | A consumed call exceeds the 2 s timeout or returns a server error | The call is retried once under the suite policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC8, AC12 |
| X11 | The fixture set does not match the harness RWB-ITG-W1J01-ITG expectations, or the clock control cannot move the date | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the two APP stories and the published contracts of P6 and P1, not their source code |
| Negotiable | The template codes, languages, merge codes, file names and dates are fixture data; the story fixes the assertions and the call set |
| Valuable | Legal approval of letter wording and the freshness of the reference data are proved on the real services before wave 1 exits, with no change to the built behaviour |
| Estimable | One suite module, one template fixture pack, one state and version reader, one freshness reader and one evidence report |
| Small | Fourteen scenarios over two services; no service code and no schema change. Size or duration is not specified in the source documents (DOR-RWB-ITG-E1034-ITG-15); the squad sets it at refinement |
| Testable | Every scenario asserts a contract response, a version number, a version state or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Letter template management, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-comms and rwb-source-data are deployed in SIT with their published contracts behind gateway-bff
    Given user "LIT-0101" holds RW-LITOFF and user "LEG-0001" holds RW-LEGAL
    Given template "DEMAND-MTG" in language "TH" has version 2 Approved by "LEG-0001" with valid from 2026-11-01
    Given today is 2026-11-20
    Given the RWB-ITG-W1J01-ITG synthetic templates are loaded and no production data is used

  Scenario: AC1 A new version becomes current (new, D-RCV-60)
    Given "LIT-0101" uploads "demand-mtg-th-v3.docx" for "DEMAND-MTG" "TH" using merge codes "CASE_NO" and "TOTAL_OUTSTANDING"
    Then version 3 is created in state "Draft"
    When "LEG-0001" approves version 3 with valid from 2026-11-20
    Then version 3 has state "Approved", approver "LEG-0001" and an approval time on 2026-11-20
    Then GET /api/recovery/comms/v1/admin/templates returns version 3 as current for the code and language on that date
    Then version 2 stays readable with approver "LEG-0001"

  Scenario: AC2 Approval is required (new, D-RCV-60)
    Given version 3 is "Draft" with no approver
    When "LIT-0101" chooses set current on version 3
    Then the system refuses it with MSG-P6-005 naming "DEMAND-MTG" version 3
    Then version 2 stays current

  Scenario: AC3 The uploader cannot approve (new, D-RCV-60)
    Given "LEG-0001" uploaded version 4 of "RECALL-SSME" "TH"
    When "LEG-0001" approves version 4
    Then the call returns status 409 with MSG-P7-002
    Then version 4 stays "Draft"

  Scenario: AC4 An unknown merge code is refused at upload (new, D-RCV-60)
    Given "LIT-0101" uploads a body for "DEMAND-HP" "TH" using the merge code "LINE_ID", which is not in the merge field catalog
    When the upload is sent
    Then it returns status 422 with MSG-P6-006 naming "LINE_ID"
    Then no version of "DEMAND-HP" is created and no file is stored

  Scenario: AC5 A required field is empty (new, D-RCV-60)
    Given "LIT-0101" uploads a body with no template code
    When the upload is sent
    Then the upload returns status 422 with MSG-GEN-001 naming "template code"

  Scenario: AC6 The file type is not allowed (new, D-RCV-60)
    Given "LIT-0101" uploads "demand.pdf" for "DEMAND-MTG" "TH"
    When the upload is sent
    Then the upload returns status 415 with MSG-P6-010 naming "DOCX"

  Scenario: AC7 Valid from is before today (new, D-RCV-60)
    Given version 3 of "DEMAND-MTG" "TH" is "Draft"
    When "LEG-0001" approves it with valid from 2026-11-19
    Then the call returns status 422 with MSG-GEN-003 naming "valid from" and "today"

  Scenario: AC8 The current version is withdrawn (new, D-RCV-60)
    Given version 3 is Approved and current
    When "LEG-0001" withdraws version 3 with reason "Wording under review"
    Then version 3 has state "Withdrawn"
    Then GET /api/recovery/comms/v1/admin/templates returns no current version for "DEMAND-MTG" "TH" and reports the withdrawn state with MSG-P6-003
    Then version 2 is not made current again

  Scenario: AC9 Two approvals at the same time (new, D-RCV-60)
    Given version 3 is "Draft" at record version 1
    Given "LEG-0001" and "LEG-0002" both open it
    When both approve within the same second
    Then one approval succeeds
    Then the other returns 409 with MSG-GEN-004

  Scenario: AC10 A repeated approval request (new, D-RCV-60)
    Given "LEG-0001" approved version 3 with Idempotency-Key "7f1c0d2e-0001"
    When the same request is sent again with the same key
    Then the first response returns with status 200
    Then one approval exists for version 3 in the template record

  Scenario: AC11 A role without Documents A cannot approve (new, D-RCV-60)
    Given test user "LIT-0101" holds RW-LITOFF
    When the user calls POST /api/recovery/comms/v1/admin/templates/{templateId}/approve
    Then the call returns 403 with MSG-P4-002

  Scenario: AC12 The freshness stamp is shown with the templates (new, D-RCV-60)
    Given the reference data product of the template catalog has a last successful load on 2026-11-20
    When the suite calls GET /api/recovery/source-data/v1/data-products/freshness and reads the template list
    Then the stamp for that product is 2026-11-20 and the template screen reads the same value through gateway-bff (RWB-E1-015; DP-19)

  Scenario: AC13 The approval, path and stamp rules hold on the contract (new, D-RCV-60)
    Given user "LEG-0001" holds Documents A and user "LIT-0101" does not
    When each of the five operations is called on the contract paths of BR9
    Then no call reaches a monolith path
    Then approval is accepted only from a user holding Documents A (BR3)
    Then the stamp on the template list is the value read from the P1 freshness contract (BR10)

  Scenario: AC14 A consumed call fails or does not answer (new, D-RCV-60)
    Given the P1 freshness contract does not answer
    When the suite calls GET /api/recovery/source-data/v1/data-products/freshness and reads the template list
    Then the outcome is Not specified in the source documents (NEWAC-RWB-ITG-E1034-ITG-AC14)
```

**Target reading.** No scenario from AC1 to AC12 is new behaviour. AC1 to AC10 repeat the legacy wording through the P6 contract, which is why every one of them carries the origin tag of this run and no legacy tag. AC11 reads the role check at the contract edge, and AC12 is the only cross-service line: the stamp comes from the P1 contract and the template list carries the same value. The data product whose stamp the catalog shows is not named in the source documents (GAP-0357; ASM-0460). Build no set-current operation: the current version of a code and language on a date is the Approved version with the latest valid from on or before that date, derived on read. AC2 keeps its wording, and its refusal is served by the approve operation on a Draft version with MSG-P6-005 and status 422.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only an Approved version with an approver and approval time can become current | RWB-E1-034 BR1; REQ-OCC-002; CTL-14 |
| BR2 | The person who uploaded a version cannot approve it | RWB-E1-034 BR2; CTL-05; roles.txt separation of duty |
| BR3 | Approval needs Documents A, held by Legal counsel | RWB-E1-034 BR3; roles.txt permission matrix; DL28 |
| BR4 | Every merge code in the body is in the merge field catalog in force | RWB-E1-034 BR4; RWB-E1-046 BR4; Principle 1 |
| BR5 | Valid from is today or later | RWB-E1-034 BR5; MSG-GEN-003 rule; refdata.txt change process, step 5 |
| BR6 | A withdrawn version holds generation until a new version is approved, with no fallback to an earlier version | RWB-E1-034 BR6; R-LIT-04, R-LIT-06 |
| BR7 | Template bodies are stored write-once in this service's own Blob container, and only body_ref is kept on the template; a change is a new version | RWB-E1-034 BR7; CTL-12; DL27 |
| BR8 | Allowed body file types are a configuration list, DOCX in Epic 1; the body size limit is 10 MB; both are Epic 1 configuration defaults read as configuration, not in code, and the configuration owner confirms them before the first SIT run | RWB-E1-034 BR8; Principle 1 |
| BR9 | The five operations keep their request, response and message shapes on P6 rwb-comms under `/api/recovery/comms/v1` at the paths `/admin/templates`, `/admin/templates/{templateId}/content`, `/admin/templates/{templateId}/approve` and `/admin/templates/{templateId}/withdraw`, and no monolith path is called | DP-13; ASM-0458 |
| BR10 | The freshness stamp is read from the P1 data product contract and shown with the reference data on SCR-33 | RWB-E1-015; DP-07; ASM-0460 |

The behaviour of BR1 to BR8 is built by RWB-P6-E1034-APP. This story asserts it through the contract and changes none of it.

The four reference lists of the upload and the administration list (product group, channel, notice type and signature basis) are validated against the value sets loaded by the template catalogue story of the same service until the reference-data read through the rwb-case contract is declared on this key.

Open decisions apply to this story: DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863), DL27 (ASM-1771, ASM-2532, ASM-2709, ASM-2716) and DL28 (ASM-1861, ASM-1925, ASM-2093, ASM-2727). Each assumption is confirmed by the programme directive, and each decision remains open in the Decision Log. For template ownership, Architecture v5 slide 41 governs under the precedence rule.

The five operations are read from the P6 contract in the registry with their request, response, state and message unchanged. The freshness stamp is read from the P1 freshness contract. The resumption of generation held under R-LIT-04 stays with the P6 notice workflow and RWB-E1-052 and is not asserted here.

Template and merge_field belong to P6 rwb-comms under Architecture v5 slide 41. RWB-P6-E1034-APP keeps the Epic 1 upload and approve core word for word, and RWB-P6-AD017-APP delivers the Epic 8 administration surface (the paged list, the body download, the approve with a valid from date, and the withdraw with a reason and the litigation officer task).

### 9. State transitions

None for the case status. This story does not change a case status. It observes the template version state moving through the legacy table:

| From | Event | Condition | To |
|---|---|---|---|
| None | Upload | Checks pass | Draft |
| Draft | Approve | Approver is Legal counsel and not the uploader; valid from today or later | Approved |
| Approved | Withdraw | Reason entered | Withdrawn |

A withdrawn version leaves no current version for its code and language, and generation for that code and language holds until a new version is approved (R-LIT-04, R-LIT-06). The point at which the hold is enforced is not named in the source documents (GAP-0357; ASM-0461); the suite asserts the state through the P6 contract and leaves the hold to RWB-P6-E1034-APP and RWB-E1-052.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic templates and users, reads the evidence report |
| RW-LITOFF, litigation officer | Uploads a version (Documents C) and reads templates (Documents R); is refused set current and approve |
| RW-LEGAL, Legal counsel | Uploads, approves and withdraws a version (Documents CRUA); cannot approve an own upload |
| Other roles with Documents R, for example the case owner and the team manager | Read templates and the current version |
| RW-COMPLY, Compliance and PDPA officer | Reads templates (Documents R) |

No approval level from the delegation of authority applies; Legal approval of wording is a Documents A right. No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-045 to DF-REF-051 | template (P6 rwb-comms) | id, template_code, template_version, language, product_group, body_ref, approved_by_legal | Read through the P6 contract |
| DF-REF-063 to DF-REF-069 | template (P6 rwb-comms) | approved_by, approved_at, valid_from, channel, notice_type, signature_basis, merge_codes | Read through the P6 contract |
| Standard column | template (P6 rwb-comms) | state | Read through the P6 contract |
| Standard column | template (P6 rwb-comms) | created_by | Read through the P6 contract |
| DF-REF-253 | merge_field (P6 rwb-comms) | merge_code | Read through the P6 contract |
| Freshness stamp | data_product and data_product_load (P1 rwb-source-data) | last successful load | Read through the P1 contract |

The legacy story writes every template field from the upload path. In the target the write happens inside P6 rwb-comms, and the suite reads the same fields back through the five P6 operations; it never reads a schema and it never writes a template row. Field IDs are those in the Logical Data Model and Data Dictionary, taken from the field list of the legacy story. Every body in the suite carries synthetic wording and no personal data.

The data product whose stamp the catalog carries is Not specified in the source documents (GAP-0357; ASM-0460); the fixture names one product of the P1 set and the assertion compares the contract value with the value the template list shows.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, task queue `rwb-integration` and schema `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/comms/v1/admin/templates | P6 rwb-comms | Read the template versions, their state and the current version for a code and language |
| POST /api/recovery/comms/v1/admin/templates | P6 rwb-comms | Upload a body with its template code, language, product group, channel, notice type, signature basis and merge codes |
| GET /api/recovery/comms/v1/admin/templates/{templateId}/content | P6 rwb-comms | Read the stored body and its merge codes |
| POST /api/recovery/comms/v1/admin/templates/{templateId}/approve | P6 rwb-comms | Approve a version with valid from, and repeat the call with Idempotency-Key "7f1c0d2e-0001" |
| POST /api/recovery/comms/v1/admin/templates/{templateId}/withdraw | P6 rwb-comms | Withdraw a version with a reason |
| GET /api/recovery/source-data/v1/data-products/freshness | P1 rwb-source-data | Read the freshness stamp of the reference data product |

Every call is one hop on the owner's base with a 2 s timeout (ADR-020, DP-11). No monolith path is called (DP-13). The exact base and route of the five operations are Not specified in the source documents (GAP-0357; ASM-0458); the suite reads them from the P6 contract in the registry.

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

None. No event is produced or consumed by this story. Notice generation and its `NoticeGenerated` event belong to RWB-E1-052, and this story neither triggers nor waits for one.

#### 12.5 Workflows and activities

None. No workflow, activity or Nexus operation is started or awaited; the five operations and the freshness read are synchronous REST calls.

#### 12.6 Schedules

None. No Schedule is started, moved or waited for, and no shared scheduler table is read.

#### 12.7 Tables owned

None. The suite owns no table. template and merge_field belong to P6 rwb-comms and data_product and data_product_load belong to P1 rwb-source-data; the suite never reads either schema (DP-01).

#### 12.8 Contract fakes

None. Every call in section 12.2 goes to the real SIT service under its published wave 1 contract. No contract fake is named for rwb-comms or rwb-source-data, so no fake library version applies. The write-once body store and the pattern of the template file are P6's and are not stubbed. The freshness value is a synthetic P1 load of the harness data set, read back through the P1 contract; it is not a stub of the P1 contract.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 6 |
| Kafka | 0 | 0 |
| Temporal | 0 | 0 |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the twelve scenarios against SIT and holds no service code |
| Template fixture pack | Test data | The synthetic bodies for "DEMAND-MTG", "DEMAND-HP" and "RECALL-SSME" in language "TH", "demand-mtg-th-v3.docx", "demand.pdf" and the body with no template code |
| State and version reader | Assertion | Reads the list, the body, the approval and the withdrawal through the P6 contract and compares state, approver, approval time and current version |
| Freshness reader | Assertion | Reads GET /api/recovery/source-data/v1/data-products/freshness and compares the stamp with the value the template list carries |
| Evidence report | Report | Records per scenario the status, the message, the version number, the state and the stamp of the run |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | template, merge_field and the body reference sit in rwb_comms; data_product and data_product_load sit in rwb_source_data; the suite asserts through contracts only |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; reference data held as rows, not code | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The merge field catalog is P6's own row set read through the P6 contract; the lists a role sees come from P3; on the APP stories, not a build dependency of the suite |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | The five comms paths of section 12.2 |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff and reads the same template list and stamp the screen shows; no screen is built here |

The dependency-added column records the build dependency of the owning story. The H and C dependencies in the table belong to the owning APP stories and to the platform contract stories, not to this suite. The H, C, I and X lists of this story are exactly the metadata rows: no H, no C, no X, and the two I dependencies RWB-P1-E1015-APP and RWB-P6-E1034-APP. An ITG story waits on no build of its own.

The schemas rwb_comms and rwb_source_data belong to P6 rwb-comms and P1 rwb-source-data. This story owns no schema and reads them only through their contracts.

A withdrawal carries a reason that must be non-empty, and that reason is recorded in the local decision record of the withdrawal through the library. The non-empty check is the only rule until the business owner publishes a length and content rule. The template row keeps the shape of TSD P6 T3.1. The decision code and the rule id of a template approval and of a template withdrawal are Not specified in the source documents (GAP-1148) and stay unset.

When a withdrawn template holds a notice, RWB-P6-E1052-APP resumes generation on the current version at its next run. The operation, task code, target queue and fields of the litigation officer task are Not specified in the source documents (GAP-1149). This story neither repoints a notice nor closes a task.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT bases of P6 rwb-comms and P1 rwb-source-data through gateway-bff.
2. Build the template fixture pack with synthetic wording, and assert that no fixture holds a personal value.
3. Implement the state and version reader over the five P6 operations, with the current-version rule read on 2026-11-20.
4. Implement AC1 to AC10 in TC order: the upload, the body read, the approval, the list, the withdrawal and the eight refusals, and assert every status and every message.
5. Implement AC11 through the contract edge and AC12 through the freshness read, then compare the stamp with the value the template list carries.
6. Write the evidence report, remove the fixtures and run the suite in SIT against the wave 1 release candidate.

Done when: all twelve test cases pass in SIT against the published wave 1 contracts of P6 rwb-comms and P1 rwb-source-data, the five operations answer with their legacy request, response and message shapes, no monolith path is called, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | Set current on a version with no Legal approval | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P7-002 | The uploader approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P6-006 | A merge code is not in the catalog | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-P6-010 | The body file type is not allowed | This template file type cannot be loaded. Use {types}. |
| MSG-GEN-003 | Valid from is before today | {field} cannot be before {other}. |
| MSG-P6-003 | A withdrawn template is asked for | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-GEN-004 | Another person changed the version first | Someone else changed this record. Reload it to see their change. |
| MSG-P3-005 | Approve on a version that is not Draft, or withdraw on one that is not Approved | This case cannot move to {state} from {current}. |
| MSG-P4-002 | The role lacks the right | You cannot {action} here. Your role does not include it. |

The message IDs and wording are copied from RWB-E1-034. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-33 Template approval, capability area Documents, is read in this story and not built or tested. The suite reads the same state through the P6 contract.

| State | What the user sees and does |
|---|---|
| Draft | The litigation officer sees the uploaded version, its merge codes and the body preview; Legal counsel sees Approve with a valid from date |
| Approved | Everyone with Documents R sees the version, approver, approval time and valid from; Legal counsel sees Withdraw |
| Withdrawn | The version shows its withdrawal reason; no action is offered |
| Empty | Not specified in the source documents (DOR-RWB-ITG-E1034-ITG-10) |
| Loading | The common Loading state applies |
| Error | The common Error state applies |
| No access | Documents access is checked on every request; an action outside the role's permission is refused with MSG-P4-002. The screen layout for this state is Not specified in the source documents (DOR-RWB-ITG-E1034-ITG-10) |

Screen Specifications v1 names only the states Draft, Approved and Withdrawn for SCR-33; it does not define Empty or No access for this screen, and the common states Loading and Error apply (CG-ALL-316). The freshness stamp is shown above the list, and the suite compares the value it reads from the P1 contract with the value the template list carries on that path. The composite route of SCR-33 through gateway-bff is Not specified in the source documents (GAP-0357; ASM-0459); the suite reads the list and the stamp through gateway-bff and takes no screenshot.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-034-01-ITG | AC1, BR1, BR7 | Integration | "DEMAND-MTG" "TH" version 2 Approved with valid from 2026-11-01; upload of version 3 by "LIT-0101"; approval by "LEG-0001" on 2026-11-20; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-02-ITG | AC2, BR1 | Integration | "DEMAND-MTG" "TH" version 3 Draft with no approver; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-03-ITG | AC3, BR2 | Integration | "RECALL-SSME" "TH" version 4 uploaded by "LEG-0001"; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-04-ITG | AC4, BR4 | Integration | Body for "DEMAND-HP" "TH" using "LINE_ID", which is not in the merge field catalog; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-05-ITG | AC5 | Integration | Upload with no template code; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-06-ITG | AC6, BR8 | Integration | "demand.pdf" for "DEMAND-MTG" "TH"; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-07-ITG | AC7, BR5 | Integration | Valid from 2026-11-19 on 2026-11-20; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-08-ITG | AC8, BR6 | Integration | "DEMAND-MTG" "TH" version 3 Approved and current, withdrawn with reason "Wording under review"; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-09-ITG | AC9 | Integration | Two approvals on record version 1 by "LEG-0001" and "LEG-0002" within the same second; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-10-ITG | AC10 | Integration | Approve repeated with Idempotency-Key "7f1c0d2e-0001"; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-11-ITG | AC11, Access | Component | RW-LITOFF test user "LIT-0101" calls POST /api/recovery/comms/v1/admin/templates/{templateId}/approve; refused with 403 and MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-12-ITG | AC13, BR3, BR9, BR10 | Integration | "LEG-0001" holding Documents A and "LIT-0101" without it; the five operations called on the contract paths of BR9; the stamp on the template list compared with the P1 freshness contract; end-to-end: real services on the wave 1 contracts |
| TC-E1-034-13-ITG | AC14 | Integration | Freshness call that does not answer; Not specified in the source documents (NEWAC-RWB-ITG-E1034-ITG-AC14); end-to-end: real services on the wave 1 contracts |
| TC-ITG-E1034-ITG-12 | AC12 | End to end | The reference data product of the template catalog with a last successful load on 2026-11-20; GET /api/recovery/source-data/v1/data-products/freshness and the template list; end-to-end: real services on the wave 1 contracts |

The data of every case is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id; TC-ITG-E1034-ITG-12 is new in this run and is held with this story.

### 17. Guardrails

- No business value in code: the file types, the size limit, the merge codes, the template list and the case names are data or configuration, read through the owner's contract.
- No personal data in logs, evidence or fixtures: the synthetic bodies carry no customer name, account number or address value, and the evidence report holds user IDs, template codes and version numbers only.
- No cross-service table read: every assertion goes through the owner's contract, and the suite owns no table (DP-01).
- One hop and a 2 s timeout on every call (ADR-020).
- A stored body is never overwritten; a correction is a new version, and the suite asserts that the earlier version stays readable.
- The screen hides actions the role does not hold, and the server checks the right on every call; AC11 reads that check at the contract edge.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | The five P6 operations of section 12.2, MSG-P6-005, MSG-P7-002, MSG-P6-006, MSG-GEN-001, MSG-P6-010, MSG-GEN-003, MSG-P6-003, MSG-GEN-004, MSG-P3-005, MSG-P4-002 | TC-E1-034-01-ITG, TC-E1-034-02-ITG, TC-E1-034-03-ITG, TC-E1-034-04-ITG, TC-E1-034-05-ITG, TC-E1-034-06-ITG, TC-E1-034-07-ITG, TC-E1-034-08-ITG, TC-E1-034-09-ITG, TC-E1-034-10-ITG, TC-E1-034-11-ITG |
| RWB-E1-015 / the freshness stamp | The stamp per data product shown with the reference data | GET /api/recovery/source-data/v1/data-products/freshness and the template list through gateway-bff | TC-ITG-E1034-ITG-12 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed REST operations of section 12.2 | TC-E1-034-01-ITG, TC-E1-034-09-ITG |
| DP-07 | Reference data and LOV held as data | The merge field catalog read through the P6 contract, and the stamp shown with it | TC-E1-034-04-ITG, TC-ITG-E1034-ITG-12 |
| DP-19 | Screen through gateway-bff | The template list and the stamp read through gateway-bff | TC-ITG-E1034-ITG-12 |
| ASM-0458 | The five operations have a moved base and route on P6 | The five comms paths of section 12.2 | TC-E1-034-01-ITG to TC-E1-034-11-ITG |
| ASM-0460 | The reference data product behind the catalog is named by the fixture | GET /api/recovery/source-data/v1/data-products/freshness | TC-ITG-E1034-ITG-12 |
| ASM-0461 | Generation holds on a withdrawal; the hold is P6's and RWB-E1-052's | The Withdrawn state read through the P6 list | TC-E1-034-08-ITG |

The legacy AC1 to AC10 at component level belong to RWB-P6-E1034-APP, not to this story. The disposition is Moved (no impact), so no behaviour changes in this slice and every assertion reads behaviour the APP story builds.

### 19. Out of scope

- The P6 APP build and its unit and component tests (RWB-P6-E1034-APP).
- The catalog tables, the load checks and the TemplateCatalog interface (RWB-E1-046).
- Generating notices from a template (RWB-E1-052) and resuming held notices when a new version is approved (R-LIT-06, RWB-E2-021).
- The Compliance approval path for a template (FEAT-ADM-05, Epic 8).
- The build of the harness RWB-ITG-W1J01-ITG.
- The P1 contract baseline and the P1 deployment and runbook stories.
- NFR load and performance testing (RWB-ITG-NFR).
