# Increment Card — INC-067-epic-1-RWB-E1-052

**RWB-E1-052 — Notice generation v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-067` |
| Title | Notice generation v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-052` |
| RUN_ID | `INC-067-epic-1-RWB-E1-052` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Must |
| Build order | 67 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-015, RWB-E1-018, RWB-E1-027, RWB-E1-046, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **demand, recall and guarantor notices generated from the Legal-approved template with the case data merged, the party and the notice address read from the ACE views by business key**, so that **letters are produced without re-keying and the address on the notice is the address ACE holds**.

**Business outcome:** Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. Under D-RCV-35 the Workbench holds no party and no contact point: the name comes from `v_ace_customer` by `person_key`, the notice address and phone come from `v_ace_contact` by the composite `contact_key` (`contact_type:key`), and the outstanding comes from `v_ace_account` by `account_key`. The clear identity number never leaves ACE, so it is never merged. This story merges those values into the current approved template, stores the PDF write-once on the case with the template version in the footer and records the decision. It serves REQ-OCC-001 and control CTL-14, and is the input to dispatch and proof of delivery (RWB-E1-055), where the WIN record is read from `v_ace_pod`. The FSD P6 measure "notices with proof of delivery, 100 percent" depends on it.

**Main flow:**
1. Caller: calls NoticeApi.generate with case ID, notice type, `person_key` and language.
2. System: reads the case summary (case number, product group, status) through the P3 interface and the party role through `case_party` by `person_key`.
3. System: asks TemplateCatalog for the current LETTER template for the notice type, product group and language on the business date.
4. System: resolves each merge code through the interface that owns its source field: `CASE_NO`, `PRODUCT_GROUP` and `ENTRY_DATE` from P3; `CUSTOMER_NAME` from `v_ace_customer.first_name` and `.last_name` by `person_key`; `POSTAL_ADDRESS` and `PHONE` from `v_ace_contact` by `person_key` and `contact_type`; `TOTAL_OUTSTANDING` from `v_ace_account.total_balance` by the case's primary `account_key`. Each value carries the ACE business date of its view or batch.
5. System: if a required merge value is empty, holds the notice, names the field and raises a task to the case owner; stops.
6. System: renders the DOCX template to PDF and adds the footer: case number, template code, template version and generation date.

**Acceptance criteria:**
- AC1: Generated
- AC2: Template approval checked
- AC3: Missing field
- AC4: Withdrawn template holds the notice
- AC5: Decision log write fails
- AC6: Repeated request on the same business date
- AC7: Stale ACE account batch
- AC8: Person not on the case
- AC9: Proof of delivery read from ACE

**Out of scope:**
- Dispatch to WIN and proof of delivery capture (RWB-E1-055, RWB-E2-021); the delivery facts are read from `v_ace_pod`.
- Approval of demand and recall notices before dispatch (RWB-E2-014).
- The endpoint for a person to request a notice (RWB-E2-021).
- The litigation route rules that call generation in production (R-LIT-01 to R-LIT-03, Epic 5, DL24).
- Contract, credit approval and mortgage documents (RWB-E2-026).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-052-notice-generation-v1-v1.md` |
| Requirement IDs | REQ-OCC-001 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
| Decision | D7.1; D-RCV-35 (U1, U4); ADR-010; DL43 open |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Calls NoticeApi.generate (Litigation R, Documents R); reads `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod`; SELECT only |
| SY-DECLOG, decision log writer | Writes the D7.1 entry |
| RW-LITOFF, litigation officer | Reads the notice and the document (Litigation CRUA, Documents CRU); receives the task on a withdrawn template |
| RW-CASEOWN, case owner | Reads the notice (Litigation R) and receives the task on missing data |
| RW-LEGAL, Legal counsel | Reads the notice (Litigation RA) |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod` |

## Contract extract

No endpoint in Epic 1. POST /api/recovery/v1/cases/{caseId}/notices calls the same service from RWB-E2-021. **Published interface NoticeApi** (P6) ```java public interface NoticeApi { NoticeResult generate(NoticeGenerationRequest request) throws TemplateNotApprovedException, PartyNotOnCaseException, DecisionNotRecordedException; } public record NoticeGenerationRequest(UUID caseId, String noticeType, String personKey, String language, UUID requestedBy, LocalDate businessDate) {} public record NoticeResult(UUID noticeId, String state, UUID documentId, String holdReason, int templateVersion, List<String> messageCodes) {} ``` Calls out of the module, each through the owner's published interface: ```java CaseSummary CaseWorkflowApi.getCaseSummary(UUID caseId); // P3 List<CasePartyView> CaseWorkflowApi.getCaseParties(UUID caseId); // P3 UUID CaseWorkflowApi.raiseTask(UUID caseId, String taskC…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: notice types, templates, merge codes, task codes and the sent type mapping are data. - No personal data in logs, tests or prompts. The name and address reach the PDF only; the decision log holds a reference to the merge snapshot, and the snapshot holds the view column, the business key and the field ID of each value, never the value. - ACE data only through the `recovery.v_ace_*` views: the customer, the contact point, the account balance and the delivery facts come from `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod`. The recovery schema holds no foreign key into a `public` table. - The clear identity number never leaves ACE and is never merged into a notice. - The generated PDF is never overwritten; a correction is a new notice. - PII Kafka receives one access event per personal field read, through RWB-E1-039.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-052-notice-generation-v1-v1.md` |
| Specification | `output/INC-067-epic-1-RWB-E1-052/specify/spec.md` |
| Compliance validation | `output/INC-067-epic-1-RWB-E1-052/specify/compliance-validation.md` |
| Agent run log | `output/INC-067-epic-1-RWB-E1-052/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-067-epic-1-RWB-E1-052/plan/` |
| Implementation evidence | `output/INC-067-epic-1-RWB-E1-052/implement/` |
| API / functional test reports | `output/INC-067-epic-1-RWB-E1-052/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-067-epic-1-RWB-E1-052/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-052-notice-generation-v1-v1.md` |
| Output run | `output/INC-067-epic-1-RWB-E1-052/` |

