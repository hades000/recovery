<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->

# ADR-009 An append-only decision log that blocks an action it cannot record

- Status: Proposed
- Date: 28 October 2026
- Deciders: the solution architect with Risk and Internal Audit

### Context and problem

Every recovery decision must be traceable for audit, testing and learning: the inputs, the rule and model versions, the recommendation, the approver, the actions and the outcome.

### Options considered

1. An append-only, hash-chained log in the ACE database, written before the action, with a failed write blocking the action
2. Application logs searched after the event

### Decision

Option 1. A correction is a further entry naming the original. Analysis reads a copy in the data lake, not the live log.

### Consequences

- Good: an auditor can test that every action carries a rule version and an approver.
- Bad: the decision log write is in the path of every action and must be fast and available. Retention is set by Compliance (DL26).
