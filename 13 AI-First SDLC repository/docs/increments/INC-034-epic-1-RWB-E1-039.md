# Increment Card — INC-034-epic-1-RWB-E1-039

**RWB-E1-039 — Access log into the decision log and break-glass admin**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-034` |
| Title | Access log into the decision log and break-glass admin |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-039` |
| RUN_ID | `INC-034-epic-1-RWB-E1-039` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration, with P7 Decision center and log |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-008, RWB-E1-022, RWB-E1-027 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration, with P7 Decision center and log. **Build group:** P4.

## Scope

**Story:** As a **security administrator (RW-SECADM)**, I want **every sign-in, refusal, read of a case record or document and export written to the decision log store, and emergency access taken only under a break-glass grant approved in the bank IAM against an open incident, for a limited time, with every action marked**, so that **every access can be audited from one log and emergency access is controlled and reviewed**.

**Main flow:**
1. Person: signs in, or reads a case record, a document or a list, or exports a list.
2. Owning module: calls AccessEventPublisher.publish with the event, the case ID where there is one, and the field IDs returned with their masking position, or the filter and row count for a list or export.
3. Workbench (AccessLogWriter): writes one decision log entry with an access event code, the actor, the area, the result and the details in actions, in the same transaction as the read response is built; if the write fails, the read returns nothing.
4. Platform administrator (RW-PLATADM): raises a break-glass request in the bank IAM naming the open incident, the capability area, the scope and the reason; the security administrator approves it there, and the IAM adds the administrator to the break-glass group until the window ends.
5. RW-PLATADM: calls POST /admin/break-glass with the incident reference, the IAM request ID, the area, the right, the scope and the reason.
6. Workbench (BreakGlassService): checks the break-glass group, the incident reference pattern and the reason length; writes an AC-BGON entry; sets the session grant to end at the earlier of the window end and the group end.

**Out of scope:**
- Logging reads of the data lake copy (RWB-E1-016, data lake access by data product).
- The break-glass request, approval and review records, which are held in the bank IAM.
- A scheduled alert for an unreviewed break-glass use to the head of SCB IT security and Compliance (Epic 8, FEAT-ADM-12 Manage an incident).
- The Decision log query screen SCR-38 (RWB-E2-005) and the Roles and access screen SCR-43 (Epic 8).

**Business outcome and value hypothesis:** The bank cannot answer today who read a debtor's record on a given date, and administrators have standing access to production data. This story writes each access event into the append-only, hash-chained decision log, so access and decisions are queried together, and replaces standing access with a break-glass grant that names an incident, ends on its own and marks every action. It meets REQ-ACA-006 and REQ-ACA-008 and supports controls CTL-09 and CTL-11. The measure is reads of the case store and the document store written to the access log: target 100 percent (NFR-042).

**Constraints and guardrails:**
- No business value in code: the window, the incident pattern, the reason length and the review window are parameters.
- No personal data in logs, tests or prompts. Access events carry field IDs and the masking position, never values; the reason text is free text written by the administrator and must not hold customer data.
- No read of another module's tables; the access log is read through the P7 published interface.
- No right beyond the letters of RW-PLATADM without an active grant.
- The grant end is enforced on every request, not by a job.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 039 Access log into the decision log and break glass admin v1.md` |
| Requirement IDs | REQ-ACA-006, REQ-ACA-008 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Program, section 5.4 |
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
| RW-PLATADM Platform administrator | Requests break-glass in the bank IAM and activates an approved grant with POST /admin/break-glass (Platform administration C) |
| RW-SECADM Security administrator | Approves break-glass in the bank IAM and reviews each use; reads the access log (Platform administration R) |
| RW-COMPLY Compliance and PDPA officer | Reads the access log; receives unreviewed uses |
| RW-AUDIT Internal audit | Reads the access log and queries access to a case through the decision log; changes nothing |
| RW-COE, RW-DATASTEW | Read the access log (Platform administration R) |
| Every bank role | Generates access events by signing in, reading and exporting |
| SY-DECLOG Decision log writer | Writes the access events (Decision log C) |
| Head of SCB IT security | Receives a break-glass use not reviewed inside the window |

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
- **Feature flag:** `rwb.access.access-log`.
- **Critical path:** No; **depends on:** RWB-E1-008, RWB-E1-022, RWB-E1-027.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the window, the incident pattern, the reason length and the review window are parameters.
  - No personal data in logs, tests or prompts. Access events carry field IDs and the masking position, never values; the reason text is free text written by the administrator and must not hold customer data.
  - No read of another module's tables; the access log is read through the P7 published interface.
  - No right beyond the letters of RW-PLATADM without an active grant.
  - The grant end is enforced on every request, not by a job.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 039 Access log into the decision log and break glass admin v1.md` |
| Specification | `output/INC-034-epic-1-RWB-E1-039/specify/spec.md` |
| Compliance validation | `output/INC-034-epic-1-RWB-E1-039/specify/compliance-validation.md` |
| Agent run log | `output/INC-034-epic-1-RWB-E1-039/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-034-epic-1-RWB-E1-039/plan/` (TBC) |
| Implementation evidence | `output/INC-034-epic-1-RWB-E1-039/implement/` (TBC) |
| API / functional test reports | `output/INC-034-epic-1-RWB-E1-039/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-034-epic-1-RWB-E1-039/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-034-epic-1-RWB-E1-039/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 039 Access log into the decision log and break glass admin v1.md` |
| Output run | `output/INC-034-epic-1-RWB-E1-039/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
