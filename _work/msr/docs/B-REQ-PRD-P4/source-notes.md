# B-REQ-PRD-P4 source notes

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date 22 November 2026.

Scratch notes only. The output of this WP is `03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md`.

## Sources read

| Source | Use |
|---|---|
| `03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx` (extract `_work/msr/extract/Recovery Workbench Business Requirements Program v4.md`) | BR set REQ-ACA-001 to REQ-ACA-013 (section 5.4), REQ-CWC-018, REQ-RDF-010, outcomes (section 2), users (section 3) |
| `... Business Requirements Epic 1 v4.docx` | RWB-E1-022, RWB-E1-037, RWB-E1-038, RWB-E1-039 (section 3.4); release 30 November 2026 |
| `... Business Requirements Epic 2 v2.docx` | RWB-E2-019 (section 3.4); release 31 December 2026 |
| `... Epics 3 to 8 Specification v3.docx` | FEAT-ADM-01 to FEAT-ADM-14 (E8, module P4) |
| `... FSD P4 Access and administration v3.md` (v6 folder) | 30 features FEAT-ACA-01..16 and FEAT-ADM-01..14, A1.2, A2.1 to A2.30, AC ids, Requirements served (REQ-ACA-001..013) |
| `... TSD P4 Access and administration v3.md` | T3.1 objects and DF-REF ids, T3.2 LOVs, T6.1 RBAC matrix, T6.3 audit, T7 NFRs, T-A endpoint inventory |
| `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` slides 11, 14, 16, 20, 41, 42, 43, 44 | rwb-access contract, schema, topic, queue, wave, JOB-18, events, service-template rule, idempotency |
| `_work/msr/plan/ownership.json` (derived from `Recovery Workbench Microservice Ownership Map v1.xlsx`) | owners of role, permission, masking_rule, role_conflict, delegation_limit, access-log paths, lov_value, partner_user, rule_package*, workflows/smoke, JOB-18 |
| `_work/msr/plan/split_plan.json` (stats and legacy) | 358 legacy keys, 1,034 slices; P4 legacy keys and release per business epic |
| `_work/msr/plan/ids.json` | ADR-013..023, DL44..DL49, D-RCV-60 |
| `... Non Functional Specification v3.md` | NFR-001..NFR-078 values used in section 7 |
| `... Decision Log v10.md` | DL01, DL03, DL26, DL38, DL39, DL40, DL48, D-RCV-35, D-RCV-36 |
| `... Batch and Scheduling Design v4.md` | JOB-18 access review list, six-monthly, security administrator |
| `... Event and Messaging Design v4.md` | checked: no row for AccessPolicyChanged or DoaLimitChanged |
| `... Temporal and Drools Design Text Extract v1.md` slide 15 | rule governance central in rwb-decision, evaluation local |
| `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` | R1, R3, R5 (waves, DPs), R8.1 header, R9 placeholders |

## Ownership facts applied (Ownership Map)

| Object or path | Owner | Effect on the PRD |
|---|---|---|
| role, permission, masking_rule, role_conflict, delegation_limit | P4 rwb-access | kept as P4 data requirements |
| authorise, /me/permissions, /doa-limits, /masking-policies | P4 rwb-access (Arch v5 slide 14 and 41) | kept, no schema in any source (gap 5) |
| /admin/roles, /admin/access-log, /me/session, /admin/break-glass-grants | P4 | kept |
| /admin/lists/{listCode}, /admin/reference-loads (approve, verify, rollback) | P3 rwb-case | removed from P4 scope; dependency (gap 1) |
| rule_package, rule_package_version, rule_row, rule_test_case, rule-package paths, change report | P7 rwb-decision | removed from P4 scope; dependency (gap 2) |
| POST /admin/workflows/smoke | PLT platform library | removed from P4 scope (gap 3) |
| lov_value | P3 rwb-case | referenced only (gap 4) |
| partner_user | S9 rwb-partner | referenced only (gap 4) |
| feature flags, outbox_event, processed_event, idempotency_key, decision_record | PLT library, one copy per service schema | treated as platform constraints |
| JOB-18 access review list | P4 rwb-access, Schedule | kept as P4 operational requirement (gap 9) |

## Release map used (W-MAP R5.6 and split_plan)

| Business epic | Wave | Release (tentative) |
|---|---|---|
| EP01 | 1 | 30 November 2026 |
| EP02 | 2 | 31 December 2026 |
| EP03 | 2 | 31 January 2027 |
| EP04 | 3 | 28 February 2027 |
| EP05 | 3 | 31 March 2027 |
| EP06 | 4 | 30 April 2027 |
| EP07 | 4 | 31 May 2027 |
| EP08 | 4 | 30 June 2027 |

P4 service wave is 1 (Arch v5 slide 41). P4 legacy keys fall in wave 1 (E1 keys and E2-019), wave 2 (E2 keys) and wave 4 (AD-001..AD-016 and E8-006..E8-019).
