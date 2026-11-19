<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->

# ADR-008 Trunk based development with feature flags

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT11; merge owner DL04

### Context and problem

Two squads release monthly from one repository. One squad's unfinished or failed change must not hold the other's release.

### Options considered

1. Trunk based development with short branches and feature flags
2. Long-lived squad branches merged before each release

### Decision

Option 1. Branches merge into main at least once a working day. Unfinished work is behind a flag. A flag that is off returns the previous code path. Untested code is not merged.

### Consequences

- Good: a change that fails SIT or UAT is switched off and the release goes ahead.
- Bad: flags must be listed, owned and removed after release.

---
