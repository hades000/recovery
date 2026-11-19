# Technical Specification — RWB-E1-052 Notice generation v1

| Field | Value |
|---|---|
| Story | RWB-E1-052 — Notice generation v1 |
| Epic / module | E1 / P6 Communications |
| RUN_ID | `INC-073-epic-1-RWB-E1-052` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-OCC-001); story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 052 Notice generation v1 v1.md`; FSD P6 A2.1; TSD P6 T3.1, T5.2 |
| Upstream IDs | REQ-OCC-001; FEAT-DRI-14; US-RWB-E1-052; R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40; CTL-06, CTL-12, CTL-14; DL16; DF-CAS-001..033, DF-LEG-015..032, DF-REF-046..257 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |
## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The PDF shows on SCR-30 Case documents; the task on SCR-01 My work; SCR-18 Notice approval is E2. |
| Logic In Scope | `YES` — template selection, merge resolution, PII detokenization, hold paths, DOCX→PDF render, footer, decision log, document store, notice row, idempotency and stale-data handling. |
| API In Scope | `NO` — no endpoint in Epic 1. The story publishes the internal `NoticeApi`; the E2 endpoint `POST /api/recovery/v1/cases/{caseId}/notices` will call the same service. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `notice` table (existing in Physical Schema v4, altered); `TemplateCatalog` (RWB-E1-046); `merge_field`; P3 case/task interfaces; P5 document hub; P7 decision log; ACE PII service. |
| New Nodes Required | `YES` — `NoticeEntity`, `NoticeRepository`, `NoticeGenerationService`, `MergeValueResolver`, `LetterRenderer`, `NoticeGeneratedPublisher`, `TemplateSelector`, `V1_052__notice_generation.sql`. |
| Inherited Existing Behavior | Approved template catalog (RWB-E1-046); decision log writer (RWB-E1-027); freshness stamp (RWB-E1-015); document store (RWB-E1-024); migration pattern (RWB-E1-044). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A notice is generated only from the current Approved template for its notice type, product group and language. | SPEC-RWB-E1-052-003, -016 | DIRECT | `TemplateSelector` filters by notice type, product group, language, LETTER and date. | COVERED |
| BR2 | A withdrawn template holds generation and raises a task to the litigation officer. | SPEC-RWB-E1-052-007 | DIRECT | Held with `TEMPLATE_WITHDRAWN`; task; MSG-P6-003. | COVERED |
| BR3 | A required merge value that is empty holds the notice, names the field and raises a task to the case owner. | SPEC-RWB-E1-052-006 | DIRECT | `merge_field.is_required`; hold reason is the merge code; MSG-P6-007. | COVERED |
| BR4 | The footer carries the case number, template code, template version and generation date. | SPEC-RWB-E1-052-008 | DIRECT | `LetterRenderer` adds the four items in order. | COVERED |
| BR5 | The generated PDF is a write-once document on the case. | SPEC-RWB-E1-052-010 | DIRECT | `DocumentHubApi.storeGenerated`; source GENERATED; write_once true. | COVERED |
| BR6 | A notice that cannot be written to the decision log is not generated. | SPEC-RWB-E1-052-009 | DIRECT | Decision log first; failure throws; no notice or document. | COVERED |
| BR7 | Sent type is NPL for a case at 90 days past due or more. | SPEC-RWB-E1-052-011 | DIRECT | `dpdAtEntry` + days since `entryDate`; NPL at 90+. | COVERED |
| BR8 | One notice per case, notice type, party and business date. | SPEC-RWB-E1-052-013 | DIRECT | `business_date` column and unique index; repeat returns the first notice. | COVERED |
| AC1 | Generate stores a PDF with the case number and amount, the footer, a Generated notice, the D7.1 decision log and `NoticeGenerated`. | SPEC-RWB-E1-052-002..005, -008..012 | DIRECT | End-to-end happy path. | COVERED |
| AC2 | A template with only a Draft version is refused with MSG-P6-005; no notice and no document. | SPEC-RWB-E1-052-003, -016 | DIRECT | `TemplateNotApprovedException` before any write. | COVERED |
| AC3 | A missing postal address holds the notice with reason `POSTAL_ADDRESS`, stores no document and raises a task with MSG-P6-007. | SPEC-RWB-E1-052-006 | DIRECT | Required value check; task to case owner. | COVERED |
| AC4 | A withdrawn template holds the notice with reason `TEMPLATE_WITHDRAWN` and raises a task with MSG-P6-003. | SPEC-RWB-E1-052-007 | DIRECT | Task to the litigation officer team. | COVERED |
| AC5 | A decision log failure fails the call with MSG-P7-003; no notice or document; incident under R-UNI-39. | SPEC-RWB-E1-052-009 | DIRECT | `DecisionNotRecordedException`; incident. | COVERED |
| AC6 | A repeated request on the same business date returns the existing notice; one notice and one document. | SPEC-RWB-E1-052-013 | DIRECT | Idempotency key on case, type, party and business date. | COVERED |
| AC7 | Stale account data generates from the stale date, records the data date and returns MSG-P1-001. | SPEC-RWB-E1-052-014 | DIRECT | `data_as_of` from P1; decision log input date; result message. | COVERED |
| AC8 | A party not on the case is refused with MSG-P4-003. | SPEC-RWB-E1-052-015 | DIRECT | Case party list check before template selection. | COVERED |
## User story intent interpretation

As a **litigation officer (RW-LITOFF)**, I want **demand, recall and guarantor notices generated from the Legal-approved template with the case data merged**, so that **letters are produced without re-keying**.

The story is the letter engine, not the screen and not the dispatch. It reads the case, party and account through their owners' interfaces, selects the current Legal-approved template, resolves only catalogued merge fields, detokenizes personal values into the PDF alone, writes the decision, stores the PDF write-once and leaves a notice in `Generated`. A missing value or a withdrawn template produces a held notice and a task, not a bad letter.
## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `NoticeApi.generate` called by SY-CASEWF in Epic 1, or by the E2 endpoint `POST /cases/{caseId}/notices`. |
| Preconditions | RWB-E1-046, RWB-E1-027 and RWB-E1-015 done; DEMAND, RECALL and GUARANTOR_NOTICE templates Approved for the synthetic product groups in TH; case, parties and contact points loaded; caller is SY-CASEWF or a person with Litigation C. |
| Input | `caseId`, `noticeType`, optional `partyId`, `language`, `requestedBy`, `businessDate`. |
| Output | Notice in `GENERATED` or `HELD`; write-once PDF; D7.1 decision log; task for a hold; `NoticeGenerated` in the outbox; `NoticeResult` with message codes. |
| Feature flag | `rwb.comms.notice-generation`. Off: `NoticeApi` is not published and no notice is generated; existing notices remain readable. |
## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `notice` | `case_id`, `party_id` | Request or borrower party | System writes | Case in scope; party on the case |
| `notice` | `notice_type` | Request, LOV-NOTICE | System writes | DEMAND, RECALL or GUARANTOR_NOTICE in E1 |
| `notice` | `template_id` | Selected template version | System writes | Current Approved LETTER template |
| `notice` | `document_id` | P5 document store | System writes | Null when held |
| `notice` | `sent_type` | Derived from days past due | System writes | NPL at 90+; otherwise BEFORE_NPL |
| `notice` | `state` | System | System writes | GENERATED or HELD in this story |
| `notice` | `hold_reason` | Merge code or `TEMPLATE_WITHDRAWN` | System writes | varchar(40) after CLAR-003 |
| `notice` | `business_date` | Request | System writes | Date; part of the idempotency key |
| `template` | `template_code`, `template_version`, `body_ref` | Catalog | Read-only | Approved and current on the business date |
| `merge_field` | `merge_code`, `source_entity`, `source_field`, `is_required`, `personal_data` | Catalog | Read-only | Version in force |
| `recovery_case` | `case_no`, `product_group`, `owner_user_id`, `entry_date`, `dpd_at_entry` | P3 case summary | Read-only | Used for merge, routing and sent type |
| `case_party`, `contact_point`, `loan_account` | party role, channel, token, total balance, `data_as_of` | P3/P1 interfaces | Read-only | Party on case; postal address; stale date recorded |
| `document`, `task`, `decision_log_entry` | All fields | P5/P3/P7 | System writes | GENERATED/write-once; task `Complete notice data`; D7.1/R-LIT-03 |
## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | Generate | Template Approved and every required merge value present | `GENERATED` | PDF stored; notice row; decision log; `NoticeGenerated` |
| — | Generate | A required merge value empty | `HELD` | Hold reason is the merge code; task to case owner; no document |
| — | TEMPLATE_WITHDRAWN | Current template Withdrawn and no later Approved | `HELD` | Hold reason `TEMPLATE_WITHDRAWN`; task to litigation officer; no document |
| — | Generate | No Approved template | No row | `TemplateNotApprovedException`; MSG-P6-005 |
| — | Generate | Decision log write fails | No row | `DecisionNotRecordedException`; incident |
| `GENERATED` | Dispatch | WIN acknowledgment (RWB-E1-055) | `SENT` | Owned by RWB-E1-055; this story writes `GENERATED` only |
| No case status change | — | — | — | This story does not change `recovery_case.status` |
## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event | SPEC |
|---|---|---|---|---|
| X1 | No Approved template | Refused; no notice and no document | MSG-P6-005 | SPEC-016 |
| X2 | Required merge value empty | Held with the field named; task; no document | MSG-P6-007 | SPEC-006 |
| X3 | Current template withdrawn | Held `TEMPLATE_WITHDRAWN`; task to litigation officer | MSG-P6-003 | SPEC-007 |
| X4 | Decision log write fails | Nothing stored; incident under R-UNI-39 | MSG-P7-003 | SPEC-009 |
| X5 | Same request twice on one business date | First notice returned; no second notice or document | None | SPEC-013 |
| X6 | Account data stale | Generate from the stale date; record it; result carries the message | MSG-P1-001 | SPEC-014 |
| X7 | Party not on the case | Refused; nothing created | MSG-P4-003 | SPEC-015 |
## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | None in Epic 1. The E2 operation `POST /api/recovery/v1/cases/{caseId}/notices` (Litigation C, first in E2) calls the same service. |
| Contract delta | None external. The internal `NoticeApi` is published with `generate`; the P6 catalog read is extended with `currentForNotice` (CLAR-001), an internal interface change. |
| Backward compatibility | Unchanged. |
| Authorization | Caller SY-CASEWF holds Litigation R and Documents R; a person needs Litigation C. 401/403 through ACE; MSG-P4-002; party outside the case MSG-P4-003. |
| Error behaviour | `TemplateNotApprovedException` MSG-P6-005; `PartyNotOnCaseException` MSG-P4-003; `DecisionNotRecordedException` MSG-P7-003; store unavailable MSG-GEN-006. |
| Versioning | No version change. |
## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; the PDF and task appear on existing screens. | Existing frontend tests stay green; no new test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR8; SPEC-RWB-E1-052-001..020 | New service, selector, resolver, renderer and publisher; the notice table is altered. | Each notice type; no Approved; withdrawn; missing required value; each merge source; PII token; footer; stale date; party not on case; decision log failure; document store failure; idempotent repeat; sent type at 89/90 dpd. |
## Detailed design
### Components

| Component | Type | Responsibility |
|---|---|---|
| `NoticeEntity` / `NoticeRepository` | Entity / Repository | Map `notice` with the new columns; find by idempotency key; insert and update. |
| `NoticeGenerationService` | Published interface | Implements `NoticeApi.generate`: steps 2 to 9. |
| `TemplateSelector` | Service | Calls `TemplateCatalog.currentForNotice` for notice type, product group, language, LETTER and business date. |
| `MergeValueResolver` | Service | Resolves each merge code through the owning module interface; detokenizes personal values through ACE PII. |
| `LetterRenderer` | Service | Fills the DOCX body and renders PDF with the four-item footer. |
| `NoticeGeneratedPublisher` | Service | Writes `NoticeGenerated` (EV-13) to the outbox in the same transaction. |
### Package and boundaries

Package `recovery.comms.notices`, folder `recovery/comms/notices`. Calls out: P3 `CaseWorkflowApi` for the case summary, parties and `raiseTask`; P1 `PartyApi.contactPoints` and `RecoveryDataApi.caseBalance`; P5 `DocumentHubApi.storeGenerated`; P7 `DecisionLogApi.write`; ACE `PiiService.detokenize`; P6 `TemplateCatalog`. No table of another module is read.
### Data and migration

- `V1_052__notice_generation.sql`: alters `notice` to add `party_id`, `template_id`, `hold_reason` and `business_date`; `hold_reason` is varchar(40) to hold any `merge_code` (CLAR-003).
- Adds `ck_notice_state` (`GENERATED`, `HELD`, `APPROVED`, `SENT`, `DELIVERED`, `UNSERVED`).
- Adds `ux_notice_generation (case_id, notice_type, party_id, business_date)`; this replaces the `created_at::date` expression in the story (CLAR-004).
- Reads `template`, `merge_field`, `recovery_case`, `case_party`, `party`, `contact_point` and `loan_account` through their owners; writes `notice`, `document` through P5, `task` through P3 and `decision_log_entry` through P7.
- No hard-coded notice type, template code, merge code, task code or sent-type mapping.
### Generation rules

1. Validate the request: case, notice type, language and business date; `partyId` optional (CLAR-002).
2. Read the case summary and parties through P3. If `partyId` is absent, use the borrower party; if the party is not on the case, throw `PartyNotOnCaseException` (MSG-P4-003).
3. Select the current LETTER template for the notice type, product group and language. No Approved → `TemplateNotApprovedException` (MSG-P6-005). Current withdrawn → write `HELD` with `TEMPLATE_WITHDRAWN` and raise a task to the litigation officer team (MSG-P6-003).
4. Resolve each merge code: read `source_entity` and `source_field`, call the owning interface, and detokenize a personal value through ACE PII (one PII Kafka access event per field). The merge snapshot stores tokens, never clear values.
5. A required value that is empty → write `HELD` with the merge code as hold reason, store no document, raise `Complete notice data` to the case owner (MSG-P6-007).
6. Render the DOCX to PDF with the footer: case number, template code, template version, generation date.
7. Write the D7.1 decision log entry with R-LIT-03, template code and version, merge snapshot reference and data date. A failed write → `DecisionNotRecordedException`, no notice, no document, incident R-UNI-39.
8. Store the PDF through P5 as a generated, write-once document; insert the notice row in `GENERATED` with document ID, notice type, sent type and `business_date`; write `NoticeGenerated` to the outbox in the same transaction.
### Order of writes and compensation

The decision log is written first, then the document, the notice row and the outbox in one transaction. A failed document store rolls back the notice and outbox; the decision log entry already written is followed by a correcting entry under R-UNI-24, because the log is append-only. A failed decision log write means no notice and no document at all.
### Sent type, events and security

`dpd = dpdAtEntry + days between entryDate and businessDate`; NPL at 90 or more, otherwise BEFORE_NPL (LOV-SENT-TYPE, DL16). When `loan_account.data_as_of` is before the business date, generation proceeds with that date, the decision log records it, and `NoticeResult.messageCodes` carries MSG-P1-001 naming DP01 and the date.

| Event | Payload | When |
|---|---|---|
| `NoticeGenerated` (EV-13) | `noticeId`, `caseId`, `noticeType`, `templateVersion` | After the notice row and document are committed; outbox in the same transaction. |

| Actor | Right | Scope |
|---|---|---|
| SY-CASEWF | Litigation R; Documents R; calls `NoticeApi.generate` | All |
| SY-DECLOG | Writes the D7.1 entry | All |
| RW-LITOFF | Litigation CRUA; Documents CRU; reads notice and PDF; receives the withdrawn-template task | Team |
| RW-CASEOWN | Litigation R; reads the notice; receives the missing-data task | Own |
| RW-LEGAL | Litigation RA; reads the notice | All |

The service checks Litigation before generation. Personal values are detokenized only into the PDF stream; logs, tests and prompts hold no personal data. Metrics: generated, held by reason, refused, render/decision-log/document failures, PII accesses. Alerts: decision log failure, render failure rate, holds older than one business day. Run book: failure signs, re-run after a corrected case, hold task queue (RWB-E1-056). One generation renders one PDF; no batch target is stated, record the SIT render time (DL11).
### Feature flag and rollback

`rwb.comms.notice-generation`. Off: `NoticeApi` is not published and no notice is generated; existing notices remain readable and E1-055 dispatch is off in the same release. Rollback: turn the flag off and redeploy the previous tag; the migration adds nullable columns and the new index, which the previous tag ignores.
## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-052-01 | AC1, BR1, BR4, BR5, BR7 | System | RC-2026-000123 Mortgage; P-0001 with postal address; DEMAND-MTG TH v2 | PDF with case number and 1,250,000.00 THB; footer; Generated; D7.1; NoticeGenerated |
| TC-E1-052-02 | AC2, BR1 | System | RC-2026-000456 Hire purchase; RECALL-HP TH v1 Draft | MSG-P6-005; no notice, no document |
| TC-E1-052-03 | AC3, BR3 | System | P-0001 with no postal address | Held `POSTAL_ADDRESS`; no document; task; MSG-P6-007 |
| TC-E1-052-04 | AC4, BR2 | System | DEMAND-MTG TH v2 Withdrawn | Held `TEMPLATE_WITHDRAWN`; task; MSG-P6-003 |
| TC-E1-052-05 | AC5, BR6 | System | Decision log store unavailable | MSG-P7-003; no notice or document; incident |
| TC-E1-052-06 | AC6, BR8 | System | Same request twice on 2026-11-25 | First notice returned; one notice and one document |
| TC-E1-052-07 | AC7 | System | Account product dated 2026-11-24 | Generated from that date; decision log records it; MSG-P1-001 |
| TC-E1-052-08 | AC8 | System | P-0999 not on the case | MSG-P4-003 |
| TC-E1-052-09 | Access, BR6 | Security/Resilience | Service identity without Litigation R; log forced to fail for 20 notices | 403 MSG-P4-002; none stored; 20 incidents |
| TC-E1-052-10 | BR4, BR3, BR7 | Unit | Thai body; required flag; dpd 89/90 | Thai and footer render; hold on empty required; NPL at 90 |
## Guardrails

- No business value in code: notice types, templates, merge codes, task codes and the sent-type mapping are data.
- No personal data in logs, tests or prompts; names and addresses are detokenized only into the PDF; the merge snapshot stores tokens; PII Kafka receives one access event per field.
- No read of another module's tables; case, party, account, task, document and decision log through their published interfaces; the PDF is never overwritten.
## Out of scope

- Dispatch to WIN and proof of delivery (RWB-E1-055, RWB-E2-021).
- Approval of demand and recall notices before dispatch (RWB-E2-014).
- The endpoint for a person to request a notice (RWB-E2-021).
- The litigation route rules that call generation in production (R-LIT-01 to R-LIT-03, Epic 5, DL24).
## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Epic 1 §3.6, §4 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40 | TC-E1-052-01..10 |
## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1, §4 step 3; SPEC-003 | `TemplateCatalog.current` takes a template code, but the story selects by notice type, product group and language. | The engine cannot pick a template without a selection rule. | Extend the P6 catalog interface with `currentForNotice(noticeType, productGroup, language, onDate)`: filter by notice type, product group, language, channel LETTER, state APPROVED and `valid_from <= onDate`; highest version wins. A null `product_group` matches every product group; a product-specific current template takes precedence. Internal interface change, not an API change. | RESOLVED | SPEC-003 |
| CLAR-002 | §12; AC2, AC4; SPEC-001, -015 | The request record carries `partyId`, but AC2 and AC4 call generation without a party. | Determines whether a party is mandatory and who is addressed. | `partyId` is optional. When absent, use the borrower party (`LOV-PARTY-ROLE` Borrower); if there is no borrower party, refuse with MSG-P4-003. | RESOLVED | SPEC-001, SPEC-015 |
| CLAR-003 | AC3; §13; SPEC-006, -018 | `notice.hold_reason` is varchar(30), while `merge_field.merge_code` is varchar(40); a long code cannot be stored as the hold reason. | A long merge code would fail the insert or truncate the reason. | Widen `hold_reason` to varchar(40) in `V1_052__notice_generation.sql`; AC3's `POSTAL_ADDRESS` is unchanged. | RESOLVED | SPEC-006, SPEC-018 |
| CLAR-004 | BR8; §13; SPEC-013, -018 | BR8 and AC6 say "business date", but the unique index uses `created_at::date`; a generation after midnight could duplicate the previous business date. | Determines whether the idempotency key is stable across midnight. | Add `notice.business_date date` and make `ux_notice_generation (case_id, notice_type, party_id, business_date)`. `created_at` is audit only. | RESOLVED | SPEC-013, SPEC-018 |
| CLAR-005 | AC8; §14; SPEC-015 | MSG-P4-003 says "This case is not in your scope", which is a scope message, not a party-mismatch message. | The user sees a misleading reason for a bad party. | Reuse MSG-P4-003 as the story requires; a P6-specific party message is a later content change. The refusal is correct even if the wording is broad. | RESOLVED | SPEC-015 |
| CLAR-006 | §11; SPEC-004 | Which source entities must `MergeValueResolver` support in v1? | The registry determines which merge codes can resolve. | The entities named in §11: `recovery_case`, `case_party`, `party`, `contact_point` and `loan_account`. Adding another source entity is a code change and is planned with the catalog. | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, the FSD/TSD, the data dictionary or the API schema. No item changes the business outcome; CLAR-004 removes a cross-midnight duplicate risk.
## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend notice story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New notice generation service, template selection, merge resolution, PDF render, decision log, document store and NoticeGenerated event; no E1 endpoint.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: internal published interface, no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 8 acceptance criteria and 7 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
