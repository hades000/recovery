# Increment Card — INC-007-epic-1-RWB-TE-011

**RWB-TE-011 — PDPA lint for code, tests and logs**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-007` |
| Title | PDPA lint for code, tests and logs |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-011` |
| RUN_ID | `INC-007-epic-1-RWB-TE-011` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-TE-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.

**Main flow:**
1. Build: reads the personal fields from the sys_fields seed and the API specification.
2. Build: generates the lint rule set from the field list: Java getter names, entity class names, JSON property names and TypeScript property names.
3. Lint: scans `src/main` and the front end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.
4. Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.
5. Lint: checks that each entity with a personal field excludes it from its text form.
6. Lint: compares each finding with the allow list; an entry past its expiry does not excuse the finding.

**Out of scope:**
- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): the ACE pipeline, outside the recovery backlog.
- Masking rules by role at run time: RWB-E1-037.
- Masked data in SIT and UAT: RWB-TE-004.
- Which fields are personal and how long they are kept: DL26.

**Business outcome and value hypothesis:** Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero.

**Constraints and guardrails:**
- No business value in code: the personal field list comes from the dictionary; patterns and the allow list are configuration.
- No personal data in logs, tests or prompts; the lint itself prints field names only, and its own check digit fixtures are generated at run time and never stored.
- No read of another module's tables; the lint reads files only.
- An allow list entry always has an owner and an expiry date.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 011 PDPA lint for code tests and logs v1.md` |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Program, section 6.7 and section 6.9 |
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
| RW-TRIBE, tribe lead and squad members | Run the lint; propose an allow list entry by pull request |
| TechX tech leads (code owners, RWB-TE-002) | Approve allow list changes and rule changes |
| RW-COMPLY, Compliance and PDPA officer | Owns which fields are personal through the data dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |

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
- **Feature flag:** None. A build check has no runtime path to switch off.
- **Critical path:** No; **depends on:** RWB-TE-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the personal field list comes from the dictionary; patterns and the allow list are configuration.
  - No personal data in logs, tests or prompts; the lint itself prints field names only, and its own check digit fixtures are generated at run time and never stored.
  - No read of another module's tables; the lint reads files only.
  - An allow list entry always has an owner and an expiry date.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 011 PDPA lint for code tests and logs v1.md` |
| Specification | `output/INC-007-epic-1-RWB-TE-011/specify/spec.md` |
| Compliance validation | `output/INC-007-epic-1-RWB-TE-011/specify/compliance-validation.md` |
| Agent run log | `output/INC-007-epic-1-RWB-TE-011/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-007-epic-1-RWB-TE-011/plan/` (TBC) |
| Implementation evidence | `output/INC-007-epic-1-RWB-TE-011/implement/` (TBC) |
| API / functional test reports | `output/INC-007-epic-1-RWB-TE-011/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-007-epic-1-RWB-TE-011/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-007-epic-1-RWB-TE-011/specify/compliance-validation.md`) |
| Acceptance criteria | 0 — engineering enabler; no business ACs (see §7 note) |
| AC numbering | Not applicable — no ACs |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 011 PDPA lint for code tests and logs v1.md` |
| Output run | `output/INC-007-epic-1-RWB-TE-011/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
