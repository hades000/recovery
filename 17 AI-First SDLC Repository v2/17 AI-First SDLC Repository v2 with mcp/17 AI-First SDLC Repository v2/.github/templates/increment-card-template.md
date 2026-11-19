---
title: Increment Card
description: "Template recording one bounded increment: project path, scope, reused artefacts, agents, approvals, rollback and evidence"
---

One card per bounded delivery increment. Create it during **Mobilise and assess** (lifecycle phase 0)
in `docs/increments/<increment-id>-<slug>.md` before any agent is started, and keep it current until
the increment is released. The card records the path, the starting context, what is reused, who
approves what, and how the change is rolled back.

---

## Identification

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| Increment ID       | `INC-XXX`                                                             |
| Title              |                                                                       |
| Programme / product|                                                                       |
| Jira epic / key    |                                                                       |
| RUN_ID             | Assigned when Technical Specifier starts; reused by all later stages  |
| Status             | Proposed / Mobilised / In delivery / Released / Closed                |

## Project type (playbook section 2.2)

| Question                                                        | Answer |
|-----------------------------------------------------------------|--------|
| Is this a completely new capability?                            |        |
| Does a running application already exist?                       |        |
| Are business requirements documented and approved?              |        |
| Is business logic embedded mainly in source code?               |        |
| Is the goal enhancement, replacement, modernisation or upgrade? |        |
| Is the target technology already approved?                      |        |
| Is there a current architecture and dependency inventory?       |        |
| Are user journeys and design-system standards available?        |        |
| Is the change primarily integration or localisation?            |        |
| Is a production-safe rollback path available?                   |        |
| Which lifecycle artefacts can be reused?                        |        |
| Which artefacts must be recovered or regenerated?               |        |

**Selected path:** Greenfield development / Brownfield enhancement / Modernisation & upgrade

**Starting context:** (business opportunity, approved backlog item, source code and architecture, ...)

## Scope

* In scope:
* Out of scope:
* Business outcome and value hypothesis:
* Constraints (policy, regulatory, technical, commercial):

## Reused approved artefacts

| Artefact | Owner | Version / link | Confirmed suitable for this increment (by, date) |
|----------|-------|----------------|--------------------------------------------------|
|          |       |                |                                                  |

## Lifecycle tailoring

Link to the completed tailoring record: `docs/increments/<increment-id>-tailoring.md`
(see `.github/templates/lifecycle-tailoring-record.md`).

## Owners and approvals

| Gate                                    | Accountable role                | Name | Decision / date |
|-----------------------------------------|---------------------------------|------|-----------------|
| Intake approval                         | Product Owner                   |      |                 |
| Context readiness                       | Forward Deployed Engineer       |      |                 |
| Requirements approval (BRD / PRD)       | Product Owner, FDA              |      |                 |
| Design and architecture approval        | Forward Deployed Architect      |      |                 |
| Backlog and specification approval      | Product Owner                   |      |                 |
| Plan approval                           | Forward Deployed Architect      |      |                 |
| Task approval                           | Forward Deployed Engineer       |      |                 |
| Pull request approval (code review)     | Forward Deployed Engineer       |      |                 |
| Quality and security gate               | FDA, Quality Engineer, Security |      |                 |
| Release readiness                       | Forward Deployed Engineer       |      |                 |
| Deployment approval                     | Product Owner / PM              |      |                 |
| Operate and learn review                | Ops / System Manager            |      |                 |

## Agents selected (playbook section 2.5)

| Lifecycle group            | Agent                      | Applicable / Optional / Not used | Reason |
|----------------------------|----------------------------|----------------------------------|--------|
| Requirements and discovery | Context Builder            |                                  |        |
| Requirements and discovery | BRD Builder                |                                  |        |
| Requirements and discovery | PRD Builder                |                                  |        |
| Design, backlog and spec   | Jira Backlog Manager       |                                  |        |
| Design, backlog and spec   | Technical Specifier        |                                  |        |
| Plan and build             | Implementation Planner     |                                  |        |
| Plan and build             | Implementation Builder     |                                  |        |
| Quality and release        | Compliance Reviewer        |                                  |        |
| Quality and release        | API Tester                 |                                  |        |
| Quality and release        | Functional Automation Test |                                  |        |
| Quality and release        | Azure Deploy pipeline      |                                  |        |

## Risk, rollback and stop signals

* Rollback route:
* Feature-control / coexistence strategy (modernisation):
* Stop and rollback signals:
* Open risks:

## Evidence links

| Evidence                      | Location                                   |
|-------------------------------|--------------------------------------------|
| Specification                 | `output/<RUN_ID>/specify/spec.md`          |
| Plan and tasks                | `output/<RUN_ID>/plan/`                    |
| Implementation evidence       | `output/<RUN_ID>/implement/`               |
| API / functional test reports | `output/<RUN_ID>/api-tests/`, `functional-tests/` |
| Review findings               | `output/<RUN_ID>/review/`                  |
| Traceability                  | `requirement/Traceability_Matrix.md`       |
| Release and deployment logs   |                                            |
