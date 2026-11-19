---
description: Lifecycle governance for the SCBX AI-First SDLC - standard lifecycle, project paths, tailoring and human approval gates.
---

# Lifecycle Governance

These rules apply the SCBX AI-First SDLC Playbook to every bounded increment delivered with the
agents in this repository. They complement `pdlc.md` (stage-level review policy) with the
increment-level controls the playbook requires.

## Standard lifecycle

```text
0 Mobilise and assess -> 1 Discover and frame -> 2 Contextualise -> 3 Define requirements
-> 4 Design experience and architecture -> 5 Create backlog and specification
-> 6 Plan and decompose -> 7 Build -> 8 Validate -> 9 Release -> 10 Operate and improve
```

## Bounded increments

* Classify the bounded increment, not the programme: Greenfield development, Brownfield enhancement
  or Modernisation & upgrade. A programme may contain several paths; each increment records its own.
* Every increment has an increment card (`.github/templates/increment-card-template.md`) in
  `docs/increments/` before any agent is started.
* Every increment has a lifecycle tailoring record
  (`.github/templates/lifecycle-tailoring-record.md`). Phases are Mandatory, Conditional,
  Reusable, Skippable with evidence or Not applicable.
* Where a phase is skipped or an artefact is reused, record the reason, the approved artefact, its
  owner, version or link, the approving authority, the risk created and the downstream controls.
  Reused artefacts must be confirmed suitable for the increment, versioned and linked to it.

## Path emphasis

| Path          | Contextualise                                          | Define requirements                                                    |
|---------------|--------------------------------------------------------|------------------------------------------------------------------------|
| Greenfield    | Enterprise, domain, project and engineering context    | BRD and PRD from approved discovery outputs; business, product, architecture approval |
| Brownfield    | Existing requirements, architecture, APIs, dependencies, code, decisions, incidents, technical debt | Start from the approved change; clarify and update acceptance criteria. Do not regenerate BRD or PRD unless existing artefacts are incomplete or materially outdated |
| Modernisation | Current-state application, architecture, dependencies, engineering environment | Analyse the source, obtain SME verification, develop BRD and PRD, obtain architecture approval |

Contextualisation is never optional in practice. Discovery and requirements definition may be
optional for Brownfield when the change is already clearly described and approved.

## Human approval gates

Agents produce; named human roles approve. No stage proceeds on agent output alone.

| Gate                                 | After                                 | Accountable role                 |
|--------------------------------------|---------------------------------------|----------------------------------|
| Intake approval                      | Mobilise and assess                   | Product Owner                    |
| Context readiness                    | Contextualise                         | Forward Deployed Engineer        |
| Requirements approval                | Define requirements (BRD, PRD)        | Product Owner, FDA               |
| Design and architecture approval     | Design experience and architecture    | Forward Deployed Architect       |
| Backlog and specification approval   | Specify                               | Product Owner                    |
| Plan approval                        | Plan                                  | Forward Deployed Architect       |
| Task approval                        | Tasks                                 | Forward Deployed Engineer        |
| Pull request approval (code review)  | Implement                             | Forward Deployed Engineer        |
| Quality and security gate            | Test and validate                     | FDA, Quality Engineer, Security  |
| Release readiness                    | Build / ship                          | Forward Deployed Engineer        |
| Deployment approval                  | GreenLane CI/CD                       | Product Owner / PM               |
| Ongoing review                       | Operate and learn                     | Ops / System Manager             |

* No implementation begins until the approved plan satisfies the planning gate.
* No autonomous production promotion is permitted.
* Start a new chat session before each stage agent so the context for the new phase is clear.
* Review agent output as seriously as human-produced output. Review is a quality activity, not a
  formality.

## Context as a governed artefact

* Before using an agent, confirm the information needed for the task is approved, accessible,
  current and sufficiently specific.
* Supply the right context, not all available context: authoritative, approved requirements,
  architecture decisions, standards, constraints and acceptance criteria relevant to the task.
* Agents do not share the squad's background knowledge. Undocumented conventions and decisions must
  be made explicit in `.github/contexts/` or they will not be applied.

## Feedback loop

Capture rework, context gaps and repeated agent failures in the increment card and use them to
improve the shared context, specifications and ways of working. The Forward Deployed Engineer owns
this feedback loop.
