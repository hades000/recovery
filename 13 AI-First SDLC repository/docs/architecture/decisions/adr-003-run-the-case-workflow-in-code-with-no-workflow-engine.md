Status: Superseded by ADR-011 (D-RCV-36, 16 November 2026).

<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->

# ADR-003 Run the case workflow in code, with no workflow engine

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT09, DT10

### Context and problem

A recovery case lives for months or years and mostly waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The case model has 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries. The question is whether a workflow engine such as Temporal holds the case, or the case is held as data and moved by code.

### Decision drivers

- Long human waits, which a workflow engine holds poorly
- Cases that outlive several releases, so in-flight versioning matters
- One case language shared with the collection module
- Skills the ACE team and TechX already have

### Options considered

1. Case state as rows in the ACE database, moved by code, timers on Quartz, automated chains on Spring Batch with an outbox
2. Temporal, with one workflow execution per case
3. A commercial case management engine

### Decision

Option 1. The case is modeled in CMMN 1.1 terms. Case, stage, task and timer state are rows. A wait of weeks is a row with a state and a stored due date. Temporal is not used; adding it later for a self-contained automation task needs its own decision record.

### Consequences

- Good: no extra runtime for SCB to operate; a change to a handler is an ordinary release; state does not replay.
- Good: case terms mean the same in both modules.
- Bad: retry and compensation for automated chains are built with Spring Batch and an outbox.

---
