<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-002 Structure ACE as a modular monolith

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT08; module creation DL05

### Context and problem

Three teams build in one service: the ACE team, the collection squad and the TechX recovery squads. Without boundaries, a change in one team's code breaks another's, and the service becomes hard to change.

### Decision drivers

- Squads can change their own module without coordinating every change
- One deployable service
- Boundaries that are checked, not agreed

### Options considered

1. Modular monolith: common, collection and recovery modules by folder, boundaries checked at build time
2. Separate services per team
3. One codebase with no module boundaries

### Decision

Option 1. Each module owns its tables and is reached only through its published interface or an application event. A boundary test fails the build on any violation.

### Consequences

- Good: one deployment and one database, with clear ownership of code and tables.
- Good: a recovery component the collection module needs can move to the common module by agreement.
- Bad: the boundary test and code owners must be in place before the squads start (DL37).

---
