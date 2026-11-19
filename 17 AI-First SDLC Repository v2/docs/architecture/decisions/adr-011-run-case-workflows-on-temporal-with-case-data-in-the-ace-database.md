<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-011 Run case workflows on Temporal, with case data in the ACE database

- Status: Accepted
- Date: 16 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-36; supersedes ADR-003

### Context and problem

A recovery case lives for months or years and mostly waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The case model has 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries.

ADR-003 held case, stage, task and timer state as rows and moved it with code. The waits, retries and automated chains are built by hand: rows in `timer`, JOB-05 to check them, Spring Batch chains and an outbox. Each of those is code the squads maintain, and a case that waits six months is a row someone must keep sweeping. The question is whether a workflow engine runs the case lifecycle, and where the case of record lives.

### Decision drivers

- Timers that fire once, months later, across a deploy, a restart and an upgrade
- Retries and compensation for multi-step automated chains without hand-built Batch and outbox code
- A case of record that no workflow history can delete or contradict
- A platform SCB IT can run inside ACE, on the ACE AKS clusters, with the ACE sign-in, audit and personal data controls
- Cases in flight that survive a change to workflow code
- One case language shared with the collection module (DT10)

### Options considered

1. Temporal, hybrid: Temporal runs the case lifecycle, and case data stays in the ACE database recovery schema
2. Temporal holding the case state in its own persistence
3. Keep the code approach: case state as rows, Quartz timers, Spring Batch chains and an outbox (ADR-003)

### Decision

Option 1. Temporal runs the case lifecycle from Epic 3, one workflow per case, with the workflow ID `case-{caseId}`. Durable timers, retries and automated multi-step chains are workflow and activity behaviour. The clusters are self-hosted on the shared ACE AKS clusters in the ACE namespace: one cluster per environment (DEV, SIT, UAT, PROD), deployed with the official Temporal Helm chart, on the pinned release SCB IT approves at build.

- Case data stays the system of record in the ACE database recovery schema. Temporal holds no case of record. A workflow history can expire or be archived without losing a case, and the case record view, the decision log and the reports read the rows they read today.
- The engine's own tables (`temporal`, `temporal_visibility`) are outside the Physical Schema, owned by role `temporal_svc`, and have no grant on the ACE database. `recovery_svc` has no grant on the Temporal databases.
- Namespace `rwb-recovery` per cluster. Task queues `rwb-case` for case workflows, `rwb-integration` for multi-step outbound chains and `rwb-platform` for smoke and health workflows.
- Search attributes are `CaseId`, `Stage`, `ProductGroup` and `QueueCode`, all Keyword and none personal. Payloads are encrypted by `PdpaPayloadCodec`, so history holds no clear personal data. Closed workflows are retained 30 days and archived to Blob in E2-039.
- The Web UI sits behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode through the codec server on a break-glass session. mTLS runs between worker, frontend and internal services.
- Quartz and Spring Batch keep every Epic 1 and Epic 2 job. JOB-05 runs behind the `TimerScheduler` port, so Epic 3 swaps in a Temporal implementation without changing a caller (T2). Temporal Schedules are not used in Epics 1 and 2.
- Workflow code is deterministic. Clock, random and I/O live in activities only. The worker polls through the Spring Boot starter under `SY-CASEWF`, and the feature flag `rwb.p3.temporal` starts or stops it.

### Consequences

- Good: durable timers, retries and multi-step chains replace hand-built timer, Batch and outbox machinery for the case lifecycle.
- Good: the case of record stays in the recovery schema, where the case engine, the decision log and the reports already read it.
- Good: one workflow per case gives replay, visibility and a stuck-workflow signal that a timer table cannot give.
- Good: the platform is a Helm release on clusters SCB IT already runs, with the ACE namespace, sign-in and audit controls.
- Good: the `TimerScheduler` port lets Epic 3 replace the Quartz implementation without a caller change, so Epics 1 and 2 are not blocked on the engine.
- Bad: SCB IT takes a new operational load: cluster operations, server and SDK upgrades, backup and restore of two databases, certificate rotation and on-call for four environments.
- Bad: the Epic 1 date is under pressure. The platform (E1-070) and the worker (E1-071) land in Epic 1 before the first case workflow in Epic 3, so Epic 1 carries the platform cost and the date risk without the case benefit.
- Bad: workflow code must be deterministic and versioned. A change is gated by the replay test (E2-040), old builds finish old workflows, and a non-deterministic change is a release defect, not a code review comment.
- Bad: two persistence estates with their own backup, restore, access and monitoring paths, and a second place a personal data incident can start.

---
