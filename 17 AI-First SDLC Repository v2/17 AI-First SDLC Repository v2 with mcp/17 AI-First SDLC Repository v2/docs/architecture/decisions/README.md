# Architecture decision records

Source: `requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md`
(16 November 2026). The full text of all twelve ADRs is in that file; the canonical per-ADR files are
below. ADR-003, ADR-004 and ADR-005 are kept for history and are superseded.

| ADR | Title | Status | File |
|---|---|---|---|
| ADR-001 | Build the Workbench as a module of ACE | Accepted | `adr-001-build-the-workbench-as-a-module-of-ace.md` |
| ADR-002 | Structure ACE as a modular monolith | Accepted | `adr-002-structure-ace-as-a-modular-monolith.md` |
| ADR-003 | Run the case workflow in code, with no workflow engine | Superseded by ADR-011 | `adr-003-run-the-case-workflow-in-code-with-no-workflow-engine.md` |
| ADR-004 | Hold every rule as versioned data | Superseded by ADR-012 | `adr-004-hold-every-rule-as-versioned-data.md` |
| ADR-005 | Take data through COLLINS and file loads | Superseded by ADR-010 | `adr-005-take-data-through-collins-and-file-loads.md` |
| ADR-006 | One ACE front end with a recovery module folder | Proposed | `adr-006-one-ace-front-end-with-a-recovery-module-folder.md` |
| ADR-007 | Build the document hub in the Workbench | Accepted | `adr-007-build-the-document-hub-in-the-workbench.md` |
| ADR-008 | Trunk based development with feature flags | Accepted | `adr-008-trunk-based-development-with-feature-flags.md` |
| ADR-009 | Append-only, hash-chained decision log | Proposed | `adr-009-an-append-only-decision-log-that-blocks-an-action-it-cannot-record.md` |
| ADR-010 | Read source data from the ACE database through read-only views | Accepted, 15 Nov 2026 | `adr-010-read-source-data-from-the-ace-database-through-read-only-views.md` |
| ADR-011 | Run case workflows on Temporal, with case data in the ACE database | Accepted, 16 Nov 2026 | `adr-011-run-case-workflows-on-temporal-with-case-data-in-the-ace-database.md` |
| ADR-012 | Evaluate rules with embedded Drools from versioned rule packages | Accepted, 16 Nov 2026 | `adr-012-evaluate-rules-with-embedded-drools-from-versioned-rule-packages.md` |
| ADR-RCV-001 | Recovery API style (`/api/recovery/v1`, plain JSON) | Accepted | `ADR-RCV-001-recovery-api-style.md` |
| — | ACE architecture decision | Reference | `ace-architecture-decision.md` |

**Reading order for a story:** ADR-001/002 (platform and boundaries) → ADR-010 (data boundary) →
ADR-011/012 (workflow and rules) → ADR-008/009 (delivery and audit) → the story's own decision field.
