# Lifecycle Tailoring Record — EPIC-001 Foundation 1

| Epic ID | Path | Prepared by | Approved by | Date |
|---|---|---|---|---|
| `EPIC-001` | Greenfield development (new Workbench module) with brownfield ACE integration constraints | FDE | Product Owner / FDA (TBC) | 2026-11-04 |

**Applies to:** all 78 Epic 1 story increments (`INC-001`–`INC-078`). Each story card links to this
shared record; story-specific differences are recorded in the card's `Agents selected` section.

## Phase decisions

| # | Lifecycle phase | Classification | Reason | Applicable agents | Approval authority |
|---|---|---|---|---|---|
| 0 | Mobilise and assess | Mandatory | The increment card, path and approvals are required before any agent starts. | Context Builder | Product Owner |
| 1 | Discover and frame | Reusable | Project Overview, Business Architecture, User Journeys, Case Journeys, Target Operating Model and Partner Operating Model are approved discovery artefacts. | None (reuse) | Product Owner |
| 2 | Contextualise | Mandatory | The agents need the context package; no agent can work from the document set alone. | Context Builder, Context Updater | Forward Deployed Engineer |
| 3 | Define requirements | Reusable | Lean BRD Epic 1 v2, Business Requirements Epic 1 v3 and Business Requirements Program v3 are approved. The canonical requirement file is consolidated from them. | Requirement Intake Consolidator (consolidation only) | Product Owner, FDA |
| 4 | Design experience and architecture | Reusable | Target Architecture v4, ADR-001–009, FSD/TSD P1–P10, Design System v1, Screen Inventory v2 and Screen Specifications v1 are approved. | Technical Specifier (consumes them) | Forward Deployed Architect |
| 5 | Create backlog and specification | Mandatory | The Epic 1 stories need implementation-ready specifications. | Technical Specifier, Compliance Reviewer | Product Owner |
| 6 | Plan and decompose | Mandatory | Each story needs a plan and tasks before code. | Implementation Planner, Compliance Reviewer | Forward Deployed Architect |
| 7 | Build | Mandatory | Code, tests and implementation evidence. | Implementation Builder | Forward Deployed Engineer |
| 8 | Validate | Mandatory | API, functional, system, regression, NFR, accessibility and UAT evidence. | API Tester, Functional Automation Test, QA, Compliance Reviewer | FDA, Quality Engineer, Security |
| 9 | Release | Mandatory | The monthly release and the six gates. | Release owner, Technical Documenter | Forward Deployed Engineer |
| 10 | Operate and improve | Conditional | Applies after go-live; the run model and benefit tracking are in the set. | Context Updater | Ops / System Manager |

## Skip and reuse records

### Phase: 1 Discover and frame

| Field | Value |
|---|---|
| Reason for skipping / reuse | Discovery is already done and approved; the Workbench problem, personas, journeys and value hypothesis are documented. |
| Existing approved artefact | Project Overview v4; Business Architecture v4; User Journeys v2; Case Journeys v3; Target Operating Model v3; Partner Operating Model v2; Stakeholder Map v3. |
| Artefact owner | Product owner / business lead |
| Version or link | `docs/discovery/` |
| Approving authority | Product Owner |
| Risk created by the bypass | Discovery may miss a user need that emerged after the documents were signed. |
| Controls applied downstream | The intake gap report and the Technical Specifier `CLAR-*` log capture new needs; the context updater refreshes discovery. |

### Phase: 3 Define requirements

| Field | Value |
|---|---|
| Reason for skipping / reuse | Lean BRD Epic 1 v2, Business Requirements Epic 1 v3 and Business Requirements Program v3 are approved and at development detail. |
| Existing approved artefact | Lean BRD Epic 1 v2; Business Requirements Epic 1 v3; Business Requirements Program v3; Non-Functional Specification v2. |
| Artefact owner | Product owner |
| Version or link | `docs/brds/`; `docs/prds/non-functional-specification.md` |
| Approving authority | Product Owner, FDA |
| Risk created by the bypass | The source documents use `REQ-*` IDs and the toolkit uses `FR-*`/`NFR-*`; the crosswalk must be kept current. |
| Controls applied downstream | The intake consolidator creates the canonical requirement file and the source-ID crosswalk; the traceability matrix is reconciled by the Traceability Manager. |

### Phase: 4 Design experience and architecture

| Field | Value |
|---|---|
| Reason for skipping / reuse | The target architecture, nine ADRs, module FSD/TSD, design system, screen inventory and screen specifications are approved. |
| Existing approved artefact | Target Architecture v4; ADR-001–009; FSD P1–P10 v2; TSD P1–P10 v2; Design System v1; Screen Inventory v2; Screen Specifications v1; API Specification v2; Logical Data Model v6; Physical Schema v4. |
| Artefact owner | Solution architect / front-end lead / data steward |
| Version or link | `docs/architecture/decisions/`; `docs/prds/`; `requirement/legacy/05-technical-architecture/`; `requirement/legacy/06-data/` |
| Approving authority | Forward Deployed Architect |
| Risk created by the bypass | There is no live Figma file; the design evidence is the screen specification and prototype. |
| Controls applied downstream | The Technical Specifier records `DESIGN_EVIDENCE_STATUS: AVAILABLE` with `SOURCE: LOCAL_ARTIFACTS`; a UI story with no design evidence is blocked. |

## Mandatory controls confirmed

These gates apply regardless of tailoring. Tick when confirmed for the increment.

- [ ] Intake approval
- [ ] Context readiness
- [ ] Requirements approval
- [ ] Design and architecture approval
- [ ] Backlog and specification approval
- [ ] Plan approval (no implementation starts before the planning gate is satisfied)
- [ ] Pull request approval
- [ ] Quality approval
- [ ] Production readiness (no autonomous production promotion)

## Notes

- The epic is classified Greenfield for the module, with brownfield ACE integration constraints.
  The programme is not classified as a whole.
- The reused artefacts are confirmed suitable for this increment by the named approver before the
  specification gate. `TBC` means the name is not in the document set; it is not an approval.
- The agent chain is human-started at every stage. No stage runs automatically after another.
