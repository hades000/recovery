# Architecture decisions

The eleven ADRs and the ACE architecture decision. Each ADR is one page in MADR form, with context,
drivers, options, decision and consequences. The source is
`requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v1.md`
for ADR-001 to ADR-009, and `05 Technical architecture/Recovery Workbench Architecture Decision
Records v3.md` in the parent set for ADR-011 and ADR-012.

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Build the Workbench as a module of ACE | Accepted | 27 October 2026 |
| ADR-002 | Structure ACE as a modular monolith with common, collection and recovery modules | Accepted | 27 October 2026 |
| ADR-003 | Run the case workflow in code, in CMMN 1.1 terms, with no workflow engine | Superseded by ADR-011 | 27 October 2026 |
| ADR-004 | Hold every rule as versioned data and evaluate it with a decision table component | Superseded by ADR-012 | 20 October 2026 |
| ADR-005 | Take data through COLLINS and file loads; call no system of record directly | Accepted | 27 October 2026 |
| ADR-006 | One ACE front end with a recovery module folder | Proposed | 28 October 2026 |
| ADR-007 | Build the document hub in the Workbench as the system of record for recovery documents | Accepted | 26 October 2026 |
| ADR-008 | Trunk-based development with feature flags | Accepted | 27 October 2026 |
| ADR-009 | An append-only, hash-chained decision log that blocks an action it cannot record | Proposed | 28 October 2026 |
| ADR-011 | Run case workflows on Temporal, with case data in the ACE database | Accepted | 16 November 2026 |
| ADR-012 | Evaluate rules with embedded Drools from versioned rule packages | Accepted | 16 November 2026 |
| - | ACE architecture decision | Accepted | - |

The ADRs are **reused** for EPIC-001 and EPIC-002; the playbook's Design experience and architecture
phase is not re-run. The reuse record is in `docs/increments/epics/EPIC-001-tailoring.md`.
