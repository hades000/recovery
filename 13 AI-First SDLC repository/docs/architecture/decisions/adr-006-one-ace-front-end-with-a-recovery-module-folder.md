<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->

# ADR-006 One ACE front end with a recovery module folder

- Status: Proposed
- Date: 28 October 2026
- Deciders: the ACE team
- Decision log: DL07

### Context and problem

ACE has one React front end. The recovery screens can live in a module folder of that front end, or the front end can be split into a workspace of modules.

### Decision drivers

- Squads work from 2 November
- One look and one sign-in for staff
- Types generated from the back end

### Options considered

1. One ACE front end with a recovery module folder
2. A workspace of front end modules with NX
3. A separate recovery front end

### Decision

Option 1 from 2 November. A move to option 2 is the ACE team's choice and does not change the recovery screens.

### Consequences

- Good: no wait for a front end restructure.
- Bad: code owners per folder are needed to keep squads out of each other's screens (DL37).

---
