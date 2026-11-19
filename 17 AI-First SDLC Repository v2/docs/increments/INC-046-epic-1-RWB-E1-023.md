# Increment Card — INC-046-epic-1-RWB-E1-023

**RWB-E1-023 — Case record view v1, read only**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-046` |
| Title | Case record view v1, read only |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-023` |
| RUN_ID | `INC-046-epic-1-RWB-E1-023` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 46 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-018, RWB-E1-024, RWB-E1-037, RWB-E1-039, RWB-E1-068, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read live from the ACE views by business key with the business date of each**, so that **I stop searching files and systems to understand a case**.

**Business outcome:** A case owner opens EFS, ALS, shared drives and team spreadsheets today to answer one question about a case. Under D-RCV-35 the Workbench holds no copy of the account, the customer or the contact point: the screen reads `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` by `account_key` and `person_key`. The identity number is already masked inside `v_ace_customer` (`id_no_masked` and `id_no_last4`) and the contact values are masked at the API by role (RWB-E1-037), so no clear personal value is copied into a Workbench table or a screen cache. This story puts the case, its accounts and arrears, its parties and contacts, its contact history and its documents on SCR-03, each section showing the ACE business date behind it, and writes every view of personal data to the access log. It meets REQ-OCC-007, REQ-RDF-009, REQ-ACA-005 and REQ-ACA-006.

**Main flow:**
1. Case owner: opens a case from SCR-02 Case list; SCR-03 shows the Loading state.
2. CaseRecordPage: calls GET /cases/{caseId}, GET /cases/{caseId}/accounts, GET /cases/{caseId}/parties, GET /cases/{caseId}/interactions and GET /cases/{caseId}/documents in parallel.
3. CaseAndWorkflowController: checks Case record R and the scope; out of scope returns 404.
4. CaseRecordQueryService: reads the header from recovery_case and the links from case_account and case_party.
5. CaseRecordQueryService: reads the account facts from `v_ace_account` by `account_key`, the customer facts from `v_ace_customer` by `person_key` and the contact points from `v_ace_contact` by `person_key` and `contact_type`; every row carries the ACE business date from `data_as_of` or from `v_ace_batch_status`.
6. CaseRecordQueryService: reads the collections history from `v_ace_efs_action` by `account_key` and the Workbench entries through InteractionLedgerReader (RWB-E1-068), and merges them into one contact history ordered by time, each row carrying its source system.

**Acceptance criteria:**
- AC1: Loads fast
- AC2: Data from ACE
- AC3: Customer and contacts from ACE
- AC4: Stale ACE batch
- AC5: Case outside the scope
- AC6: Document hub unavailable
- AC7: The access event cannot be written
- AC8: Masking by role
- AC9: Case on hold
- AC10: No documents and no contact history
- AC11: No copy of the account on the case
- AC12: An account link with no ACE row

**Out of scope:**
- The history timeline on the case view (RWB-E1-035).
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Writing a Workbench entry to the interaction ledger (RWB-E1-066, RWB-E1-067).
- Collateral and valuation sections (Epic 2, after the CCMS and SVAF ingestion lands in ACE).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-023-case-record-view-v1-read-only-v1.md` |
| Requirement IDs | REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006 |
| BRD section | Business Requirements Epic 1, sections 3.3, 3.4 and 3.6; Business Requirements Program, sections 5.1, 5.4 and 5.6 |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 open |
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
| RW-CASEOWN | Opens cases in scope Own (Case record R) |
| RW-TEAMMGR | Opens cases in scope Team |
| RW-PHONECOL | Opens cases in scope Own, read only, with masking |
| RW-CONDUCT, RW-AUDIT | Open every case (scope All) |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| recovery_svc, recovery service identity | Reads `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` through the P1 query; SELECT only |
| ACE team lead | Owns the ACE tables and columns behind the four views |

## Contract extract

| Endpoint | Request | Response | Errors | Authorization | |---|---|---|---|---| | GET /api/recovery/v1/cases/{caseId} | Path caseId | Case | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 503 | Case record R, scope applied | | GET /api/recovery/v1/cases/{caseId}/accounts | Path caseId | CaseAccount[] with accountNo, daysPastDue, totalBalance, dataAsOf read from `v_ace_account` by `account_key` (see additions) | Same | Case record R, scope applied | | GET /api/recovery/v1/cases/{caseId}/parties | Path caseId | CasePartyView[]: personKey, partyRole, displayName, customerNo, idNo or idNoLast4, category, contacts[] with contactType, contactKey, contactValue by role and dataAsOf (see additions) | Same | Case record R, scope applied | | GET /api/recovery/v1/cases/{caseId}/interactions | Path caseId; query channel, from, to, page, size | ContactHistoryPage: the ACE EFS entries from `v_…

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

- No business value in code: masking rules, labels and timeouts are data. - No personal data in logs, tests or prompts; test parties are synthetic and the application log holds case numbers only. - ACE data only through the `recovery.v_ace_*` views: account, customer, contact and collections history come from `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action`, and freshness from `v_ace_batch_status`. The recovery schema holds no foreign key into a `public` table. - The view holds no copy of a source record and caches no clear personal value; the identity number is masked inside the view and the contact values are masked at the API by role. - Personal fields are never shown when the access event cannot be written.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-023-case-record-view-v1-read-only-v1.md` |
| Specification | `output/INC-046-epic-1-RWB-E1-023/specify/spec.md` |
| Compliance validation | `output/INC-046-epic-1-RWB-E1-023/specify/compliance-validation.md` |
| Agent run log | `output/INC-046-epic-1-RWB-E1-023/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-046-epic-1-RWB-E1-023/plan/` |
| Implementation evidence | `output/INC-046-epic-1-RWB-E1-023/implement/` |
| API / functional test reports | `output/INC-046-epic-1-RWB-E1-023/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-046-epic-1-RWB-E1-023/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 12 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-023-case-record-view-v1-read-only-v1.md` |
| Output run | `output/INC-046-epic-1-RWB-E1-023/` |

