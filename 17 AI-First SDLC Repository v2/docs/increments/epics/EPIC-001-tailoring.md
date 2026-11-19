# Lifecycle Tailoring Record — EPIC-001 Foundation 1

| Epic ID | Path | Prepared by | Approved by | Date |
|---|---|---|---|---|
| `EPIC-001` | Greenfield development of the Workbench module with brownfield ACE integration constraints | FDE | Product Owner / FDA | 2026-11-16 |

**Applies to:** all 72 Epic 1 story increments (`INC-001`–`INC-072`). Each story card links to this
record; story-specific differences are recorded in the card's `Agents selected` section.

## Phase decisions

| # | Lifecycle phase | Classification | Reason | Applicable agents | Approval authority |
|---|---|---|---|---|---|
| 0 | Mobilise and assess | Mandatory | The increment record, path and approvals are required before any agent starts. | Context Builder | Product Owner |
| 1 | Discover and frame | Reusable | Discovery is approved in the document set v14. | None (reuse) | Product Owner |
| 2 | Contextualise | Mandatory | The agents need the re-baselined context package; no agent works from the raw document set alone. | Context Builder, Context Updater | Forward Deployed Engineer |
| 3 | Define requirements | Reusable | Lean BRD v3, Business Requirements v4 and the FSD v6 set are approved. The canonical requirement file is consolidated from them. | Requirement Intake Consolidator (consolidation only) | Product Owner, FDA |
| 4 | Design experience and architecture | Reusable | Target Architecture v6 and ADR-001–012 are approved. | Technical Specifier (consumes them) | Forward Deployed Architect |
| 5 | Create backlog and specification | Mandatory | Each active story needs an implementation-ready specification against the new baseline. | Technical Specifier, Compliance Reviewer | Product Owner |
| 6 | Plan and decompose | Mandatory | Each story needs a plan and tasks before code. | Implementation Planner, Compliance Reviewer | Forward Deployed Architect |
| 7 | Build | Mandatory | Code, migrations, tests and implementation evidence. | Implementation Builder | Forward Deployed Engineer |
| 8 | Validate | Mandatory | API, functional, system, regression, NFR, accessibility and UAT evidence. | API Tester, Functional Automation Test, QA, Compliance Reviewer | FDA, Quality Engineer, Security |
| 9 | Release | Mandatory | The monthly release and its gates. | Release owner, Technical Documenter | Forward Deployed Engineer |
| 10 | Operate and improve | Conditional | Applies after go-live. | Context Updater | Ops / System Manager |

## Skip and reuse records

### Phase 1 — Discover and frame

| Field | Value |
|---|---|
| Reason for reuse | Discovery is already approved; the Workbench problem, personas, journeys and value hypothesis are documented. |
| Existing approved artefact | Project Overview v4; Business Architecture v4; User Journeys v2; Case Journeys v3; Target Operating Model v3; Partner Operating Model v2; Stakeholder Map v3. |
| Owner | Product owner / business lead |
| Version or link | `docs/discovery/` |
| Approving authority | Product Owner |
| Risk created by the bypass | A user need that emerged after sign-off may be missed. |
| Controls applied downstream | The intake gap report and the Technical Specifier `CLAR-*` log capture new needs. |

### Phase 3 — Define requirements

| Field | Value |
|---|---|
| Reason for reuse | Lean BRD Epic 1 v3, Business Requirements Epic 1 v4 and Business Requirements Program v4 are approved at development detail. |
| Existing approved artefact | Lean BRD Epic 1 v3; Business Requirements Epic 1 v4; Business Requirements Program v4; Non-Functional Specification v3. |
| Owner | Product owner |
| Version or link | `docs/brds/`; `docs/prds/non-functional-specification.md` |
| Approving authority | Product Owner, FDA |
| Risk created by the bypass | Source documents use `REQ-*` IDs and the toolkit uses `FR-*`/`NFR-*`; the crosswalk must stay current. |
| Controls applied downstream | The intake consolidator creates the canonical requirement file and the source-ID crosswalk. |

### Phase 4 — Design experience and architecture

| Field | Value |
|---|---|
| Reason for reuse | Target Architecture v6, ADR-001–012, FSD v6 and TSD v5 are approved. |
| Existing approved artefact | `docs/architecture/decisions/`; `docs/prds/`; `requirement/legacy/05-technical-architecture/` |
| Owner | Solution architect |
| Approving authority | Forward Deployed Architect |
| Risk created by the bypass | Screen-level design evidence is document-based; there is no live Figma file. |
| Controls applied downstream | The spec records `DESIGN_EVIDENCE_STATUS: USER_STORY_SCREENSHOTS` and marks approximate visual values. |

## Mandatory-control checklist

| Control | Applies | Evidence |
|---|---|---|
| Human-started stages only | Yes | `CLAUDE.md` stage discipline; run logs. |
| Context read before specification | Yes | `CONTEXT-20261116`; context file index in `project-context.md`. |
| Story has a plan before code | Yes | Per-story `plan/plan.md`. |
| Test exists before code | Yes | Per-story plan and implementation evidence. |
| No production or personal data in prompts | Yes | `AGENTS.md` §4 and §10; PDPA lint. |
| No new dependency without plan approval | Yes | Plan gate; D-RCV-49 precedent. |
| Module boundary check | Yes | `RWB-TE-001` BND-1–BND-6. |
| Migration naming and schema lint | Yes | D-RCV-28 and `RWB-E1-044`. |
| No inbound source load | Yes | D-RCV-35; retirement register. |
| Temporal and Drools only as ADR-011/012 define | Yes | `AGENTS.md` §4; feature flags `rwb.p3.temporal`, `rwb.p3.drools`. |
