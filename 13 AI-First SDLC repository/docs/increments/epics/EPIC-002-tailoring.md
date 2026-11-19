# Lifecycle Tailoring Record — EPIC-002 Foundation 2

| Epic ID | Path | Prepared by | Approved by | Date |
|---|---|---|---|---|
| `EPIC-002` | Brownfield enhancement of the Workbench module on ACE | FDE | Product Owner / FDA (TBC) | 2026-11-04 |

**Applies to:** all Epic 2 story increments when they are created. The numbering continues after the
78 Epic 1 story cards (`INC-079` onward unless the manifest assigns otherwise).

## Phase decisions

| # | Lifecycle phase | Classification | Reason | Applicable agents | Approval authority |
|---|---|---|---|---|---|
| 0 | Mobilise and assess | Mandatory | The increment card and approvals are required. | None | Product Owner |
| 1 | Discover and frame | Reusable | The discovery set from EPIC-001 is current; the Epic 2 delta is in the business requirements. | None (reuse) | Product Owner |
| 2 | Contextualise | Reusable | The context package from EPIC-001 is current; only the Epic 2 delta needs a Context Updater run. | Context Updater | Forward Deployed Engineer |
| 3 | Define requirements | Reusable | Business Requirements Epic 2 v2 is approved. | Requirement Intake Consolidator (consolidation only) | Product Owner, FDA |
| 4 | Design experience and architecture | Reusable | The target architecture, ADRs, FSD/TSD and design system are approved; Epic 2 adds screens and integrations within them. | Technical Specifier (consumes them) | Forward Deployed Architect |
| 5 | Create backlog and specification | Mandatory | The Epic 2 stories need implementation-ready specifications. | Technical Specifier, Compliance Reviewer | Product Owner |
| 6 | Plan and decompose | Mandatory | Each story needs a plan and tasks. | Implementation Planner, Compliance Reviewer | Forward Deployed Architect |
| 7 | Build | Mandatory | Code, tests and evidence. | Implementation Builder | Forward Deployed Engineer |
| 8 | Validate | Mandatory | API, functional, system, regression, NFR, accessibility and UAT. | API Tester, Functional Automation Test, QA, Compliance Reviewer | FDA, Quality Engineer, Security |
| 9 | Release | Mandatory | The December release and the six gates. | Release owner, Technical Documenter | Forward Deployed Engineer |
| 10 | Operate and improve | Conditional | After go-live; the run model and benefit tracking apply. | Context Updater | Ops / System Manager |

## Skip and reuse records

### Phase: 1 Discover and frame

| Field | Value |
|---|---|
| Reason for skipping / reuse | Discovery from EPIC-001 remains current; Epic 2 adds ownership, timers, approvals, notices and steering. |
| Existing approved artefact | Project Overview v4; User Journeys v2; Case Journeys v3; Target Operating Model v3; Stakeholder Map v3. |
| Artefact owner | Product owner |
| Version or link | `docs/discovery/` |
| Approving authority | Product Owner |
| Risk created by the bypass | A new Epic 2 user need may not be in the discovery set. |
| Controls applied downstream | The Epic 2 BRD and the Technical Specifier `CLAR-*` log capture it. |

### Phase: 2 Contextualise

| Field | Value |
|---|---|
| Reason for skipping / reuse | The EPIC-001 context package is current; only the Epic 2 delta needs updating. |
| Existing approved artefact | `.github/contexts/project-context.md`, `domain-context.md`, `frontend-context.md`, `backend-context.md`, `testing-standards.md`; `requirement/Context_RecoveryWorkbench.md`. |
| Artefact owner | FDE |
| Version or link | `.github/contexts/` |
| Approving authority | Forward Deployed Engineer |
| Risk created by the bypass | The Epic 2 partner identities and notice path may need new context that the Epic 1 package does not hold. |
| Controls applied downstream | Context Updater reviews the Epic 2 delta and records `CTX-UPDATE-*` entries. |

### Phase: 3 Define requirements

| Field | Value |
|---|---|
| Reason for skipping / reuse | Business Requirements Epic 2 v2 is approved. |
| Existing approved artefact | Business Requirements Epic 2 v2; Business Requirements Program v3; Non-Functional Specification v2. |
| Artefact owner | Product owner |
| Version or link | `docs/brds/business-requirements-epic-2.md` |
| Approving authority | Product Owner, FDA |
| Risk created by the bypass | The `REQ-*` to `FR-*`/`NFR-*` crosswalk must be maintained. |
| Controls applied downstream | The intake consolidator creates the Epic 2 canonical requirements and the crosswalk; the Traceability Manager reconciles. |

### Phase: 4 Design experience and architecture

| Field | Value |
|---|---|
| Reason for skipping / reuse | The target architecture, ADRs, FSD/TSD and design system are approved; Epic 2 adds screens and integrations within them. |
| Existing approved artefact | Target Architecture v4; ADR-001–009; FSD/TSD P1–P10 and S1–S9; Design System v1; Screen Inventory v2; Screen Specifications v1; API Specification v2. |
| Artefact owner | Solution architect / front-end lead |
| Version or link | `docs/architecture/decisions/`; `docs/prds/`; `requirement/legacy/05-technical-architecture/` |
| Approving authority | Forward Deployed Architect |
| Risk created by the bypass | No live Figma; the design evidence is local. The partner identity design is new in Epic 2. |
| Controls applied downstream | Technical Specifier uses `SOURCE: LOCAL_ARTIFACTS`; the partner identity design is reviewed by Security. |

## Mandatory controls confirmed

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

- Epic 2 is a brownfield enhancement of the module delivered in EPIC-001. It does not regenerate the
  BRD or the architecture; it consumes them.
- The shared Epic 2 items with the collection squad (notice path, contact stop, shared tasks) are
  recorded under DL30. If the split is not agreed, the affected stories stop at the planning gate.
- `TBC` means the name is not in the document set; it is not an approval.
