# Increment Card — INC-053-epic-1-RWB-E1-068

**RWB-E1-068 — Interaction ledger read interface**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-053` |
| Title | Interaction ledger read interface |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-068` |
| RUN_ID | `INC-053-epic-1-RWB-E1-068` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-066 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **to read a case's ledger in one ordered sequence, filtered by channel, actor or date range**, so that **I can see what has happened to it before I decide anything**.

**Main flow:**
1. Case owner: opens SCR-03 Case record; the history panel calls GET /cases/{caseId}/interactions?page=0&size=50.
2. P3 interactions handler (API-P3-014): checks Case record R and calls InteractionLedgerReader.read() with the caller's context.
3. InteractionLedgerReader: checks the case is in the caller's scope through CaseScopeQuery.
4. InteractionLedgerReader: validates the filter (channel in LOV-CHANNEL, from not after to, size 1 to 200).
5. InteractionLedgerReader: reads the case's entries matching the filter, ordered by occurred_at, then case_seq.
6. InteractionLedgerReader: masks the summary field (is_personal) through the P4 masking interface for the caller's roles.

**Out of scope:**
- The full case timeline screen SCR-04 and the ledger as a timeline on the case (FEAT-ILG-09, RWB-E2-034).
- Recording entries (RWB-E1-066, RWB-E1-067).
- Masking rule values (DL26, Compliance) and the masking mechanism (RWB-E1-037).

**Business outcome and value hypothesis:** A case owner who decides a route, a settlement or a legal step must first know what was said, promised, sent and done on the case. One read interface returns the ledger in order with the source of each entry, filters it by channel, actor and date range, and masks personal content by role on the same rules as the case record. The case record view and every other consumer read through this interface, so there is one ordering and one masking rule for the history. Serves REQ-ILG-006, REQ-ILG-003 and REQ-ILG-014; NFR-070 (one case history read in under 2 seconds at its 2031 size; DL11).

**Constraints and guardrails:**
- No business value in code: page sizes are properties; channels and masking come from lists and rules.
- No personal data in logs, tests or prompts: summaries are never logged; test summaries are synthetic text.
- No read of another module's tables: scope comes from CaseScopeQuery and masking from MaskingPolicy; P3 reads the ledger only through InteractionLedgerReader.
- The read changes nothing in the ledger.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 068 Interaction ledger read interface v1.md` |
| Requirement IDs | REQ-ILG-006, REQ-ILG-003, REQ-ILG-014 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-003, REQ-ILG-006, REQ-ILG-014) |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the ledger of own cases (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the ledger of team cases (Case record R, scope Team) |
| RW-CONDUCT, RW-AUDIT and other roles with Case record R | Read the ledger of cases in their scope |
| RW-REFADM, reference data administrator | May not read (no Case record right) |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules that decide who sees the summary (DL26) |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.dataengine.ledger-read`.
- **Critical path:** No; **depends on:** RWB-E1-066.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: page sizes are properties; channels and masking come from lists and rules.
  - No personal data in logs, tests or prompts: summaries are never logged; test summaries are synthetic text.
  - No read of another module's tables: scope comes from CaseScopeQuery and masking from MaskingPolicy; P3 reads the ledger only through InteractionLedgerReader.
  - The read changes nothing in the ledger.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 068 Interaction ledger read interface v1.md` |
| Specification | `output/INC-053-epic-1-RWB-E1-068/specify/spec.md` |
| Compliance validation | `output/INC-053-epic-1-RWB-E1-068/specify/compliance-validation.md` |
| Agent run log | `output/INC-053-epic-1-RWB-E1-068/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-053-epic-1-RWB-E1-068/plan/` (TBC) |
| Implementation evidence | `output/INC-053-epic-1-RWB-E1-068/implement/` (TBC) |
| API / functional test reports | `output/INC-053-epic-1-RWB-E1-068/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-053-epic-1-RWB-E1-068/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-053-epic-1-RWB-E1-068/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 068 Interaction ledger read interface v1.md` |
| Output run | `output/INC-053-epic-1-RWB-E1-068/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
