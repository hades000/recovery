<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-001 Build the Workbench as a module of ACE

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT07

### Context and problem

Recovery needs a case system from day 90 to close. ACE is the bank's collection engine and already runs sign-in, access control, audit and personal data logging, a case view and the restructure calculator. Building recovery as a separate application would give staff who work both collection and recovery two systems and two case views, and the bank two platforms to run.

### Decision drivers

- One case view for collection and recovery staff
- Reuse of what ACE already runs in production
- No integration cost between collection and recovery
- One platform for SCB IT to operate and secure

### Options considered

1. A module of ACE: one service, one repository, one front end
2. A separate recovery application on the ACE infrastructure pattern
3. A separate recovery application on its own platform

### Decision

Option 1. The Workbench is the recovery module of ACE.

### Consequences

- Good: sign-in, the bank IAM, access control, audit, PII and SOC logging come from ACE.
- Good: one case view across collection and recovery.
- Good: recovery takes ACE's data position, which is now an asset rather than a constraint: one copy of the source data, ingested by ACE and read through read-only views (ADR-010).
- Bad: the recovery and collection squads share one repository and one release, so merge ownership and release discipline matter (ADR-008, DL04).

---
