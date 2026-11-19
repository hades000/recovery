# Increment Card — INC-029-epic-1-RWB-TE-008

**RWB-TE-008 — Decision log hash chain check**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-029` |
| Title | Decision log hash chain check |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-008` |
| RUN_ID | `INC-029-epic-1-RWB-TE-008` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P7 Decision center and log |
| Story type | Enabler |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-008, RWB-TE-007 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P7 Decision center and log. **Build group:** P7.

## Scope

**Story:** As an **internal auditor (RW-AUDIT)**, I want **a nightly job that recomputes the whole decision log hash chain, records the result with the last hash, and reports a break to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

**Main flow:**
1. Quartz: fires JOB-14 at 02:00 Asia/Bangkok for the business date of the previous day.
2. Job (HashChainCheckJob): checks that JOB-13 for the same business date has ended; if not, waits and checks again every 5 minutes until 04:00, then runs and records that JOB-13 had not ended.
3. Job: reads the highest chain_seq at the start and fixes it as the end of the run; entries appended later are checked the next night.
4. Job: calls HashChainVerifier over chain_seq 1 to the end in batches of 1,000, recomputing each entry_hash and checking each prev_hash.
5. Job: counts every entry that fails and keeps the first.
6. Job: writes the job run record with type JOB-14, business date, status and checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count.

**Out of scope:**
- The store, the hash computation and the on-demand verifier (RWB-E1-008).
- The check of each entry returned by an audit query (RWB-E2-005).
- The decision log copy to the data lake (RWB-E1-014, JOB-13).
- Detecting a broken chain as a control breach through the administration screens (Epic 8, FEAT-ADM-10).

**Business outcome and value hypothesis:** The decision log is evidence only while nobody can change an entry unseen. The database refuses updates and deletes (RWB-E1-008), but a change made outside the service, for example by a database administrator, is found only by recomputing the chain. This story runs that check as JOB-14 every night after the decision log copy, records each run with its last hash, and tells Compliance of a break, an incomplete run or an intact chain. It meets REQ-DRI-003 and NFR-035 and supports control CTL-06. The measure is a daily check with a same-day report: target 100 percent of nights.

**Constraints and guardrails:**
- No business value in code: times and batch size are parameters.
- No personal data in logs, tests or prompts; reports name entry IDs and chain_seq only.
- No read of another module's tables; the job reads only decision_log_entry.
- The job never writes to decision_log_entry and never repairs an entry.
- One canonical form implementation, shared with the store.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 008 Decision log hash chain check v1.md` |
| Requirement IDs | REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, sections 5.7 and 6.6 |
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
| SY-DECLOG Decision log writer | The job runs under this service identity and reads the log (Decision log C and read through the store) |
| RW-COMPLY Compliance and PDPA officer | Receives every report; owns the job (batch.txt) and its parameters |
| RW-AUDIT Internal audit | Reads the run records (Platform administration R); may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts; reruns the job (Platform administration U) |
| RW-SECADM Security administrator | Receives the break incident with Compliance |

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
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.decision.hash-check`.
- **Critical path:** No; **depends on:** RWB-E1-008, RWB-TE-007.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: times and batch size are parameters.
  - No personal data in logs, tests or prompts; reports name entry IDs and chain_seq only.
  - No read of another module's tables; the job reads only decision_log_entry.
  - The job never writes to decision_log_entry and never repairs an entry.
  - One canonical form implementation, shared with the store.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 008 Decision log hash chain check v1.md` |
| Specification | `output/INC-029-epic-1-RWB-TE-008/specify/spec.md` |
| Compliance validation | `output/INC-029-epic-1-RWB-TE-008/specify/compliance-validation.md` |
| Agent run log | `output/INC-029-epic-1-RWB-TE-008/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-029-epic-1-RWB-TE-008/plan/` (TBC) |
| Implementation evidence | `output/INC-029-epic-1-RWB-TE-008/implement/` (TBC) |
| API / functional test reports | `output/INC-029-epic-1-RWB-TE-008/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-029-epic-1-RWB-TE-008/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-029-epic-1-RWB-TE-008/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 008 Decision log hash chain check v1.md` |
| Output run | `output/INC-029-epic-1-RWB-TE-008/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
