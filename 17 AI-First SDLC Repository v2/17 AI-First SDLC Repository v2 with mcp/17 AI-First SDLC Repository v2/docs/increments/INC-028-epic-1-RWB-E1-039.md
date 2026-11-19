# Increment Card — INC-028-epic-1-RWB-E1-039

**RWB-E1-039 — Access log into the decision log and break-glass admin**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-028` |
| Title | Access log into the decision log and break-glass admin |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-039` |
| RUN_ID | `INC-028-epic-1-RWB-E1-039` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration, with P7 Decision center and log |
| Story type | User story |
| Priority | Must |
| Build order | 28 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-008, RWB-E1-022, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration, with P7 Decision center and log.

## Scope

**Story:** As a **security administrator (RW-SECADM)**, I want **every sign-in, refusal, read of a case record or document and export written to the decision log store, and emergency access taken only under a break-glass grant approved in the bank IAM against an open incident, for a limited time, with every action marked**, so that **every access can be audited from one log and emergency access is controlled and reviewed**.

**Business outcome:** The bank cannot answer today who read a debtor's record on a given date, and administrators have standing access to production data. This story writes each access event into the append-only, hash-chained decision log, so access and decisions are queried together, and replaces standing access with a break-glass grant that names an incident, ends on its own and marks every action. It meets REQ-ACA-006 and REQ-ACA-008 and supports controls CTL-09 and CTL-11. The measure is reads of the case store and the document store written to the access log: target 100 percent (NFR-042).

**Main flow:**
1. Person: signs in, or reads a case record, a document or a list, or exports a list.
2. Owning module: calls AccessEventPublisher.publish with the event, the case ID where there is one, and the field IDs returned with their masking position, or the filter and row count for a list or export.
3. Workbench (AccessLogWriter): writes one decision log entry with an access event code, the actor, the area, the result and the details in actions, in the same transaction as the read response is built; if the write fails, the read returns nothing.
4. Platform administrator (RW-PLATADM): raises a break-glass request in the bank IAM naming the open incident, the capability area, the scope and the reason; the security administrator approves it there, and the IAM adds the administrator to the break-glass group until the window ends.
5. RW-PLATADM: calls POST /admin/break-glass with the incident reference, the IAM request ID, the area, the right, the scope and the reason.
6. Workbench (BreakGlassService): checks the break-glass group, the incident reference pattern and the reason length; writes an AC-BGON entry; sets the session grant to end at the earlier of the window end and the group end.

**Acceptance criteria:**
- AC1: Read logged
- AC2: Break-glass granted
- AC3: Export logged
- AC4: Document read logged
- AC5: Break-glass without an IAM grant is refused
- AC6: Break-glass with a missing incident or a short reason is refused
- AC7: A read that cannot be logged returns nothing
- AC8: Access audit query
- AC9: Refusals are written to the decision log
- AC10: A repeated activation does not open a second grant

**Out of scope:**
- Logging reads of the data lake copy (RWB-E1-016, data lake access by data product).
- The break-glass request, approval and review records, which are held in the bank IAM.
- A scheduled alert for an unreviewed break-glass use to the head of SCB IT security and Compliance (Epic 8, FEAT-ADM-12 Manage an incident).
- The Decision log query screen SCR-38 (RWB-E2-005) and the Roles and access screen SCR-43 (Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-039-access-log-into-the-decision-log-and-break-glass-admin-v1.md` |
| Requirement IDs | REQ-ACA-006, REQ-ACA-008 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Program, section 5.4 |
| Decision | None |
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
| RW-PLATADM Platform administrator | Requests break-glass in the bank IAM and activates an approved grant with POST /admin/break-glass (Platform administration C) |
| RW-SECADM Security administrator | Approves break-glass in the bank IAM and reviews each use; reads the access log (Platform administration R) |
| RW-COMPLY Compliance and PDPA officer | Reads the access log; receives unreviewed uses |
| RW-AUDIT Internal audit | Reads the access log and queries access to a case through the decision log; changes nothing |
| RW-COE, RW-DATASTEW | Read the access log (Platform administration R) |
| Every bank role | Generates access events by signing in, reading and exporting |
| SY-DECLOG Decision log writer | Writes the access events (Decision log C) |
| Head of SCB IT security | Receives a break-glass use not reviewed inside the window |

## Contract extract

**POST /admin/break-glass-grants** (new, recorded in the additions file) | Item | Value | |---|---| | Request | BreakGlassActivation: incidentReference, iamRequestId, capabilityArea (LOV-CAPABILITY), right (one of C, R, U), scope (LOV-SCOPE), reason (20 to 1000 characters) | | Response | 201 BreakGlassGrant: grantId (the AC-BGON entry ID), incidentReference, capabilityArea, right, scope, startsAt, endsAt | | Errors | 401 no session; 403 caller not RW-PLATADM or not in the break-glass group (MSG-P4-007); 409 a grant is already active (MSG-GEN-004); 422 field missing or invalid (MSG-GEN-001, MSG-GEN-002); 503 entry could not be written (MSG-P7-003) | | Authorization | Platform administration, right C, plus membership of the break-glass group | | Idempotency | Idempotency-Key header | **GET /api/recovery/v1/admin/access-log** (API-P4-008) | Item | Value | |---|---| | Request | Query: user,…

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

- No business value in code: the window, the incident pattern, the reason length and the review window are parameters. - No personal data in logs, tests or prompts. Access events carry field IDs and the masking position, never values; the reason text is free text written by the administrator and must not hold customer data. - No read of another module's tables; the access log is read through the P7 published interface. - No right beyond the letters of RW-PLATADM without an active grant. - The grant end is enforced on every request, not by a job.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-039-access-log-into-the-decision-log-and-break-glass-admin-v1.md` |
| Specification | `output/INC-028-epic-1-RWB-E1-039/specify/spec.md` |
| Compliance validation | `output/INC-028-epic-1-RWB-E1-039/specify/compliance-validation.md` |
| Agent run log | `output/INC-028-epic-1-RWB-E1-039/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-028-epic-1-RWB-E1-039/plan/` |
| Implementation evidence | `output/INC-028-epic-1-RWB-E1-039/implement/` |
| API / functional test reports | `output/INC-028-epic-1-RWB-E1-039/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-028-epic-1-RWB-E1-039/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 10 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-039-access-log-into-the-decision-log-and-break-glass-admin-v1.md` |
| Output run | `output/INC-028-epic-1-RWB-E1-039/` |

