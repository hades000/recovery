<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-004 Hold every rule as versioned data

Superseded by ADR-012 on 16 November 2026. Rules are still versioned data, now authored as Drools XLS decision-table workbooks and evaluated by embedded Drools. This section is kept as the record of what was decided on 20 October 2026.

- Status: Superseded by ADR-012
- Date: 20 October 2026
- Deciders: SCB core team with Henka
- Decision log: DT02; Epic 1 rule scope DL24

### Context and problem

Thresholds, limits, routes, timers and templates change often. If they are written in code, every change needs a release, and the business waits a month to move a number. ACE has rule based logic in code and no rules engine.

### Decision drivers

- A business change without a code release
- An audit trail of which rule version decided each case
- Open cases kept on the version they were decided under

### Options considered

1. Rules as versioned rows, evaluated by a decision table component in the recovery module
2. A commercial or open source rules engine
3. Rules in Java code

### Decision

Option 1. Every rule, limit, threshold, template, name, queue, role, timer and route is a data row with a version, valid from and valid to dates, an approver and a test case, changed through a validated load. Each route set is a decision table with hit policy Unique. Code holds the behavior; data holds the choices.

### Consequences

- Good: a threshold moves on its effective date with no release, and rolls back the same way.
- Good: the decision log records the rule ID and version for every move.
- Bad: the evaluator, the load checks and the rule table tests are built by the squads.

---
