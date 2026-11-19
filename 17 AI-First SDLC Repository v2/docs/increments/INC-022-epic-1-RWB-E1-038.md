# Increment Card — INC-022-epic-1-RWB-E1-038

**RWB-E1-038 — Delegation of authority table as reference data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-022` |
| Title | Delegation of authority table as reference data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-038` |
| RUN_ID | `INC-022-epic-1-RWB-E1-038` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration |
| Story type | User story |
| Priority | Must |
| Build order | 22 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-043, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration.

## Scope

**Story:** As a **Risk and model risk officer (RW-RISK)**, I want **the delegation of authority (which approval level may approve which decision, by product, principal amount and second condition) held as a versioned table that the approval router reads**, so that **approval limits change by an approved data load and every approval can be checked against the limit that applied on its date**.

**Business outcome:** Approval and authority governance is an audit finding, and limits today sit in the bank regulation and in people's heads. This story loads the 95 limits of Regulation 540031 as amended by Regulation 690070 (chapter 2 for problem loans, chapter 3 for assets held for sale) as versioned rows, and gives the approval router one lookup that returns the lowest approval level whose limit covers a decision, with the version used. It meets REQ-ACA-004 and REQ-APD-010 and is the data behind control CTL-04. The measure is decisions within the delegation of authority: target 100 percent (FSD P7 A2.1).

**Main flow:**
1. Reference data administrator (RW-REFADM): converts the Delegation of authority matrix to the load file: one row per limit and decision code, for MORTGAGE and SSME, amounts converted from THB million to baht.
2. RW-REFADM: calls POST /admin/reference-loads with table "delegation_limit", validFrom and the version name, for example DOA-2026.11.
3. Workbench (DelegationLimitLoader): validates the file whole and stores 218 rows with status Loaded.
4. Risk and model risk officer (RW-RISK): reviews the difference report and calls POST /admin/reference-loads/{loadId}/approve.
5. Workbench: checks that the approver holds RW-RISK and did not load the file; writes one decision log entry with decision code AC-VERS and no case; sets valid_to on the rows of the previous version to the day before the new valid from; marks the new version Approved.
6. Approval router (RWB-E2-013): calls DelegationOfAuthority.lowestLevel with the decision, the regulation item (one decision code can cover several items, for example D7.5 covers items 2.1.4, 2.1.6 and 2.1.9), the product, the amounts, the conditions and the decision date.

**Acceptance criteria:**
- AC1: Table loaded
- AC2: Lookup
- AC3: Change
- AC4: A file with an error is refused in full
- AC5: The loader cannot approve and only Risk may
- AC6: An approval that cannot be recorded does not take effect
- AC7: No limit covers the request
- AC8: The version valid on the decision date is used
- AC9: A write-off for a related party goes to the Board

**Out of scope:**
- Routing an approval to the holder of the level, the queue and escalation (RWB-E2-013).
- Names of holders and substitutes, and the chapter 8 limits for hire purchase and unsecured loans (Risk with the product heads, DL18).
- The rule that new credit to a problem loan takes the higher of the restructuring and credit authorities (Epic 3 restructure stories).
- The Delegation of authority screen SCR-41 and moving a limit through screens (Epic 8, FEAT-ADM-03).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-038-delegation-of-authority-table-as-reference-data-v1.md` |
| Requirement IDs | REQ-ACA-004, REQ-APD-010 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Epic 2, section 3.7 (REQ-APD-010); Business Requirements Program, sections 5.4 and 5.7 |
| Decision | D6.4 to D6.6, D7.1 |
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
| RW-REFADM Reference data administrator | Prepares and loads a delegation version (Reference data C). Approves none |
| RW-RISK Risk and model risk officer | Approves a delegation version (approver role for the table) |
| RW-PRODHEAD Product head | Agrees the limits for their product with Risk before the load; may not approve the load |
| Risk with the product heads | Name the holder and substitute of each level (DL18) |
| Approval levels L1 to L6 | Board of Directors, Executive Committee, Problem Asset Resolution Committee or Management Committee, Head of Recovery at function level, Recovery executive at division level, Recovery executive at department level (doa.txt, Levels sheet). Levels L1 to L3 approve by committee resolution recorded in the decision log; L4 to L6 approve in the Workbench |
| SY-RULES Drools evaluator | Calls the lookup for the approval router |
| RW-AUDIT Internal audit | Reads every version and its approval entry |

## Contract extract

**POST /api/recovery/v1/admin/reference-loads** (API-P4-005) | Item | Value | |---|---| | Request | Multipart: file, table "delegation_limit", validFrom | | Response | 201 ReferenceLoad: id, table, validFrom, status "Loaded", rows | | Errors | 401; 403 no Reference data C (MSG-P4-002); 409 version name exists (MSG-GEN-004); 422 validation failed (MSG-P1-002); 503 (MSG-GEN-006) | | Authorization | Reference data, right C | | Idempotency | Idempotency-Key header | **POST /admin/reference-loads/{loadId}/approve** (API-P4-006) | Item | Value | |---|---| | Request | None | | Response | 200 ReferenceLoad with status "Approved" | | Errors | 401; 403 caller is not RW-RISK (MSG-P4-002); 404 (MSG-P4-003); 409 caller loaded it (MSG-P7-002) or load not "Loaded" (MSG-GEN-004); 503 decision log write failed (MSG-P7-003) | | Authorization | api.yaml declares Reference data A, which no role holds; the…

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

- No business value in code: levels, limits, conditions, products and the approver role are data. - No personal data in logs, tests or prompts; holders are test user references in SIT and UAT. - No read of another module's tables; the router calls the published interface. - No limit is converted or rounded at lookup time; amounts are stored in baht with two decimals. - A version already approved is never edited; a change is a new version.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-038-delegation-of-authority-table-as-reference-data-v1.md` |
| Specification | `output/INC-022-epic-1-RWB-E1-038/specify/spec.md` |
| Compliance validation | `output/INC-022-epic-1-RWB-E1-038/specify/compliance-validation.md` |
| Agent run log | `output/INC-022-epic-1-RWB-E1-038/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-022-epic-1-RWB-E1-038/plan/` |
| Implementation evidence | `output/INC-022-epic-1-RWB-E1-038/implement/` |
| API / functional test reports | `output/INC-022-epic-1-RWB-E1-038/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-022-epic-1-RWB-E1-038/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-038-delegation-of-authority-table-as-reference-data-v1.md` |
| Output run | `output/INC-022-epic-1-RWB-E1-038/` |

