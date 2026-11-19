---
run_id: INC-008-epic-1-RWB-E1-043
story: RWB-E1-043
title: Reference data service with versioned tables
stage: specify
agent: Technical Specifier
date: 2026-11-18
revision: 4 (remediation run 3 of REVIEW-RWB-E1-043-SPEC-003, findings 131-137 and G3-R01..G3-R05; orchestrator triage of 2026-11-18, round 3; rebased on RWB-TE-001 spec v4 and RWB-E1-042 spec revision 5)
status: SUCCESS_WITH_ASSUMPTIONS
previous: spec.run3.md (revision 3, 2026-11-18, failed spec gate 3 on one High, one Medium and five Low findings); spec.run2.md (revision 2); spec.run1.md (revision 1)
supersedes: _v2-baseline/specify/spec.md (historical; RUN_ID INC-009, D-RCV-47 schema basis; kept unchanged)
---

# Technical specification: RWB-E1-043 Reference data service with versioned tables

Every finding of spec gate 1 (`../review/spec-gate-review.md`, 101-119, G-R01..G-R10) and spec gate 2
(`../review/spec-gate-review-2.md`, 120-130, G2-R01..G2-R05), spec gate 3 (`../review/spec-gate-review-3.md`,
131-137, G3-R01..G3-R05), and the orchestrator rulings, are answered in `gate-response.md` (§1-§4 round 1,
§6 round 2, §7 round 3). Revisions 1 to 3 are kept as `spec.run1.md`, `spec.run2.md` and `spec.run3.md`. All triage and rulings come from the orchestrator, Claude Code, an AI agent; none is a
human decision.

## 0. Sources and conventions

All `requirement/legacy/` paths are in `17 AI-First SDLC Repository v2` (read only). Short tags are
used in the tables below.

| Tag | Document, version, location |
|---|---|
| S7 | Story file v7, RWB-E1-043 (file v2, 16 Nov 2026): `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| S7-001, S7-019, S7-022, S7-025, S7-028, S7-037, S7-039, S7-042, S7-045, S7-064, S7-069 | Story files v7 (same folder) of RWB-E1-001, -019, -022, -025, -028, -037, -039, -042, -045, -064, -069 |
| CARD | Increment card INC-008: `aisdlc/docs/increments/INC-008-epic-1-RWB-E1-043.md` |
| REQ | Canonical requirements REQ-RWB-002 v2.0 (16 Nov 2026): FR-RWB-011, FR-RWB-012, NFR-RWB-001..010, §10, §12 crosswalk: `17 AI-First SDLC Repository v2/requirement/RecoveryWorkbench_Requirements.md` |
| D35 / D36 | Client decisions D-RCV-35 and D-RCV-36: `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md`, `d-rcv-36-temporal-and-drools.md` (line 145 lists the E1-043 changes) |
| ADR3 | Architecture Decision Records v3 (ADR-010, ADR-012): `requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| DL10 | Decision Log v10 (D-RCV-28 migration rule): `requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| PS6 | Physical Schema v6 (16 Nov 2026): `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` (repository copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`) |
| API4 | API Specification v4.0.0 (16 Nov 2026): `api/recovery-api-v4.yaml` (load 3167, approve 3214, lists 3135, verify 4961, rollback 5004, `RollbackRequest` 9818) |
| MSG4 | Error and Message Standard v4: `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| TC7 | Test Cases v7, TC-E1-043-01..11: `requirement/legacy/09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md` |
| BS6 | Build Sequence Epic 1 and 2 v6: `requirement/legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| PACK | RWB-E1-042 clarification pack (§3.1, §3.7, §6.2, §7 OI-E1-042-001..011): `requirement/legacy/e1-042-migration-and-clarifications/rwb-e1-042-clarification-pack.md` |
| E42S | RWB-E1-042 spec revision 5 (2026-11-18, remediation run 3, rebased on RWB-TE-001 v4; still in its own gate round): `aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (§4.3 line 141, §7.1, §7.4, §11.2, §11.3, §12.1, §12.2 packages `casewf.config.api` and `access.api`, `ParameterKeys.byName(String key, Class<T> type)`, `ParameterLoadHandler`; §12.4; §12.5 check order; §12.7 `VersionDecisionRecorder` package-private in `casewf.config`, recorder failure 503 MSG-P7-003; §12.10 grants file `access/interim-capability-grants.csv`; §12.12 flag binding; SPEC-RWB-E1-042-005/-012/-017/-019/-020/-021/-022/-023/-025; CLAR-013). Revision 3 of this spec used its revision 4 |
| TE001 | RWB-TE-001 spec v4 (INC-002, passed its spec gate; owns the module map): `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` SPEC-RWB-TE-001-004 (e), -022 (d), -023; `shared-updates.md` SU-02, SU-08 (INC-008 row), SU-14 |
| DD8 | Logical Data Model and Data Dictionary v8: `requirement/legacy/06-data/recovery-workbench-logical-data-model-and-data-dictionary-v8-xlsx.md` (DF-REF-033, DF-REF-079, DF-REF-163, DF-REF-164; DF-WRK-038, DF-WRK-051, DF-WRK-052) |
| URP4 | Users, Roles and Permissions v4: `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` (role list; line 102 RW-DATASTEW Reference data RU) |
| E01S | RWB-E1-001 spec revision 2 (INC-009): `aisdlc/output/INC-009-epic-1-RWB-E1-001/specify/spec.md` (SPEC-RWB-E1-001-013..017, ASM-E1001-05, -12, -15, -19) and its gate reviews: round 1 findings 003, 004; round 2 (`review/spec-gate-review-2.md`) findings 014, 016, 017 |
| BLOG | `AI-SDLC-BUILD-LOG.md` §1, orchestrator decisions D-RUN-07 (23:26), D-RUN-08 (23:26), D-RUN-09 (23:41), D-RUN-10 (23:47), D-RUN-11 (23:49), D-RUN-12 (23:49), all 2026-11-17; gate triage of 2026-11-18 00:31 (run 2) and 00:58 (run 3) |
| CTX | `aisdlc/.github/contexts/backend-context.md` v2.0, `backend-standards.md` (BS-3.2, BS-4.4, BS-4.6, BS-7.2), `testing-standards.md` v2.0 §3; `aisdlc/.github/rules/security-quality-standards.md` |
| TE011 | Story file v7 RWB-TE-011 PDPA lint (§10 RW-COMPLY line, §12 Input) |
| S7-064 | Story file v7 RWB-E1-064 data dictionary (§3 precondition "accepts a load for table code `sys_fields`", §4 steps 2-3, §10, §11 DF-REF-105 `is_personal` Read, §12 `DataDictionaryLoader`) |
| PDPA | Personal Data Protection Design v2 (`requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md`); Data Classification and Personal Data Inventory v4 (`requirement/legacy/06-data/...-inventory-v4-xlsx.md`, DF-REF-166/167) |
| AUD | Phase 0 audit `aisdlc/evidence/phase0-standards-audit.md` (A-01, A-03, A-04, A-06, A-18) |
| AG | `AGENTS.md` v2 (repository root) |

- `A-nn` = labelled assumption in `assumptions.md`. `GAP-nn` = row in `document-gaps.md`.
- Precedence (RUN-BRIEF): D35/D36, then ADR3, then DL10, then S7, then older maps and drafts. The
  orchestrator decisions in BLOG are run rulings made by Claude Code (the AI orchestrator), not human
  decisions; they settle conflicts that no document settles.
- Dependencies follow D-RUN-08: this spec uses only code in this repository or delivered by an earlier
  story of BS6 (RWB-E1-042, order 3). Work of later stories is named as a seam (§"Seams").
- Requirement IDs of this story (S7 lines 20, 362-363): REQ-DRI-011, REQ-CWC-006; rules R-UNI-38 (BR3,
  BR6), CTL-08 (BR4), REQ-CWC-016 (BR7); feature FEAT-CWC-23. Canonical mapping: FR-RWB-011 (REQ).
  REQ-CWC-006 has no canonical FR in the REQ §12 crosswalk (GAP-29).

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — S7 §15 "No screen in this story" |
| Logic In Scope | `YES` |
| API In Scope | `YES` — S7 §12, §13 step 7; D-RUN-10 |
| API Impact Type | `NEW_API_REQUIRED` — first implementation of three operations already in API4: `POST /admin/reference-loads`, `/{loadId}/approve`, `/{loadId}/rollback`. No OpenAPI change. |
| Impacted Existing Nodes | `application.yaml` (key `rwb.p3.refdata-versions`, SPEC-018; no `RecoveryFlags` or `RecoveryProperties` change, TE001 SPEC-023); `backend/src/test/resources/architecture/recovery-modules.yaml` (casewf `published` list gains `refdata.api`, TE001 SU-08; SPEC-019); `RecoveryBoundaryTest` (SPEC-019); RWB-E1-042 resources `config/parameter-catalog.csv` (38 rows added, SPEC-029) and `access/interim-capability-grants.csv` (Reference data rows, SPEC-027; E42S §12.10). No change to `ApiExceptionHandler`, `ProblemFactory` (`access.internal`) or `ApiProblemException` (`access.api`) beyond what RWB-E1-042 delivers (E42S §12.2; TE001 SU-08). |
| New Nodes Required | P3 `recovery.casewf.refdata.api` (published as `@NamedInterface(name = "refdata.api", propagate = false)`, TE001 SU-08): `ReferenceVersionRegistry`, `ReferenceDataService`, `ReferenceDataReaders`, `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException`, `ReferenceTableHandler`, `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport`, `RowCheckFailure`. P3 `recovery.casewf.refdata.internal` (not published): registry and service implementations, `ReferenceTableHandlers` (handler map), `ReferenceRowCache`, `ReaderLogGate`, `ReferenceVersionLogger`, `ReferenceTableColumns`, `ReferenceRowCheck`, `ContentHasher`, entities and repositories, `RefdataSettings` (package-private module record, TE001 SPEC-023), `ReferenceDecisionRecorder` (package-private port) and `LoggingReferenceDecisionRecorder`, and the HTTP side: `ReferenceLoadController`, `ReferenceLoadDispatcher`, `ParameterLoadBranch`, `ActorIdResolver` (seam, A-07), `ReferenceLoadFileReader`, `ReferenceLoadAuthority`, `ReferenceLoadAudit` (port) and `LoggingReferenceLoadAudit` (TE001 SU-08: "Put the controller in the P3 refdata package"). P4 additions named by S7 §11 and §17 ("through the P4 published interface"): `recovery.access.api.ListOfValuesReader` and its interim implementation `recovery.access.internal.LovValueReader` (SPEC-002; A-41). Migration `V<seq>__rwb_e1_043_reference_versions.sql`. |
| Inherited Existing Behavior | Recovery Flyway bean, `${recoverySchema}`, lint (AUD A-04); JWT resource server, `/api/recovery/**` RW- role gate, 401 MSG-P4-001, principal claim `sub` (`SecurityConfig`); `ApiExceptionHandler` (`AccessDeniedException` → 403 MSG-P4-002, `NoResourceFoundException` → 404 MSG-P4-003); Modulith verify (RWB-TE-001). From RWB-E1-042 (order 3, E42S revision 5 §12.2): P3 `casewf.config.api` `ParameterService`, generated `ParameterKeys`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider`; P4 `access.api` `MessageResolver`, `CapabilityCheck`, `ApiProblemException` with message ID, `ApiError`. RWB-E1-042's `VersionDecisionRecorder` is package-private in `casewf.config` and is not used here (E42S §12.7; GAP-50). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
| Module scope (for the plan gate) | All story code is in P3 `casewf.refdata` (TE001 SU-08). P4 gets one published interface and its interim reader (S7 §11, §17) and the Reference data rows of the grants file; no `platform` change. Dependencies run P3 → P4 only (SPEC-019). AGENTS §7 still sends a plan that touches two modules back to the analyst; the plan gate must take that decision (gate finding 118). |

## User story intent interpretation

The reference data administrator loads one of 12 reference tables (S7 BR1) as a new, immutable,
dated version; a different person with the approve right for that table approves it; an approved
version can be rolled back in one call so the earlier version is in force again; services read the
approved version in force for a business date and log which version they used, naming themselves.
Business values move out of code into versioned rows (S7 §1, §2; REQ FR-RWB-011). The shared load
endpoint also routes `PARAMETER` loads to RWB-E1-042 (D-RUN-10) and codes that other modules own to
their registered handlers (D-RUN-11). Rule tables are excluded (D36 line 145; AG §4.9).

## Entry trigger and preconditions

| # | Precondition (S7 §3) | State in this repository | Handling |
|---|---|---|---|
| P1 | RWB-E1-044 done (Flyway with schema placeholder) | Recovery Flyway bean, `${recoverySchema}`, lint exist (AUD A-04) | Inherited |
| P2 | RWB-E1-042 done: `refdata.cache.ttl-seconds` (300, DL11) and the list of reference table codes | E42S revision 5 publishes `ParameterService`, `ParameterLoadHandler` (`casewf.config.api`) and `CapabilityCheck`, `MessageResolver`, `ApiProblemException` (`access.api`) (E42S §12.2); code not yet merged | Build after RWB-E1-042 merges (A-14, A-25). Table codes are this story's (E42S CLAR-022; SPEC-002) |
| P3 | LOV-REF-TABLE loaded with the 12 codes, no rule code | PS6 seeds 25 codes incl. 5 rule codes and HOLIDAY; `lov_value` is an RWB-E1-001 V0001 table present locally through the PS6 load (GAP-04, GAP-32) | SPEC-002 refuses any built-in code without a column definition |
| P4 | P4 load endpoint deployed | No endpoint code exists | Built here in P3 `casewf.refdata.internal` (TE001 SU-08; GAP-53): S7 §13 step 7; D-RUN-10 (SPEC-015, 016, 024) |
| P5 | Loader holds Reference data C; approver holds A (assumed RW-RISK) | PS6 and Users, Roles and Permissions v4: no role holds Reference data A (E42S §12.10) | SPEC-027, A-08, GAP-14, GAP-22 |
| P6 | Business date from the ACE batch record (`v_ace_batch_status`) | The view is RWB-E1-069's (BS6 order 10, S7-069 line 230); RWB-E1-042 publishes `BusinessDateProvider` with an interim implementation (E42S SPEC-023) | SPEC-017 uses the provider; replacing it is a seam (A-01, GAP-12, GAP-51) |

Triggers: an HTTP load, approve or rollback call (S7 §4 steps 1, 5; §9; D-RUN-10); a service call to
`ReferenceDataService` on engine start or cache expiry (S7 §4 step 8).

## Requirement-to-SPEC Logic Coverage

A row is `COVERED` only when this story builds and tests it. Requirement lines that another story
builds are listed in §"Requirement lines built by another story", with the owner and the citation.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| S7 BR1; D36 line 145 | 12 reference codes; list is data (LOV-REF-TABLE); no rule code; holiday from `v_ace_holiday` | 002, 021, 025 | DIRECT | Built-in code: in LOV-REF-TABLE and has a column definition. Handler codes: SPEC-025 | COVERED |
| S7 BR2 | One load = one version, max+1; never changed after write | 001, 007 | DIRECT | Trigger with narrow exemption list (SPEC-001) | COVERED |
| S7 BR3; R-UNI-38 | Version in force = APPROVED with latest valid_from ≤ business date | 011, 032 | DIRECT | ROLLED_BACK and VALIDATED never served; an approval changes nothing for a business date before `validFrom` (SPEC-032) | COVERED |
| S7 BR3, BR8, §9 row 4; S7-019 BR3, AC2, AC9; DD8 DF-REF-163/164 (finding 132) | Approval writes a new version effective from `validFrom`, never overwrites the version in force; reads by business date; versions independent (out-of-order approval); rollback of the latest approved version only | 010, 011, 024, 025, 032 | DIRECT | Handler contract keeps the same rule (SPEC-025 *Effective date*); TC-TM-01..04 | COVERED |
| S7 BR4; CTL-08 | Effective only after approval by a non-author | 008, 001 | DIRECT | Service check + DB CHECK | COVERED |
| S7 BR5 | Any failed check refuses the load in full | 003, 004, 005, 007 | DIRECT | One transaction | COVERED |
| S7 BR6 sentence 1 | valid_from before business date refused | 005 | DIRECT | Equal accepted (A-05) | COVERED |
| S7 BR6 sentence 2 (registry part) | Open cases keep the version they were decided under | 001, 008, 011 | DIRECT | Versions immutable and readable by `versions()`; no retroactive approval (A-17). Engine-side recording: §"built by another story" | COVERED |
| S7 BR7; REQ-CWC-016 | Every engine logs table code and version of every table it reads | 014 | DIRECT | Reader-bound service logs reader, table, version, business date on every read window | COVERED |
| S7 BR8 | Approval sets valid_to of replaced version | 010 | DIRECT | | COVERED |
| S7 BR9 | Engine with no version in force does not run | 012 | DIRECT | Exception + alert; engines stop on it (seam) | COVERED |
| S7 X1 / AC2 / AC5 | Author approval refused MSG-P7-002; stays VALIDATED, never served | 008, 011 | DIRECT | 409 | COVERED |
| S7 X2 / AC4 | Schema or key failure refused MSG-P3-027 naming row and column; nothing written | 003 | DIRECT | 422; every failed row listed in `detail` (G-R02) | COVERED |
| S7 X3 / AC6 | Past valid_from refused naming valid from | 005 | DIRECT | 422 | COVERED |
| S7 X4 / AC7 | Same table, valid_from, hash: return first load, write nothing | 006, 025 | DIRECT | 201 same body (A-06); a handler code may supply its own repeat message, 409 (A-38) | COVERED |
| S7 X5 / AC8 | Concurrent approvals: one wins, other MSG-GEN-004 | 009 | DIRECT | Optimistic lock | COVERED |
| S7 X6 / AC9 | No version in force: alert with MSG-P3-027 | 012 | DIRECT | | COVERED |
| S7 X7 / AC10 | Header-only file refused MSG-GEN-001 naming "rows" | 004 | DIRECT | 422 | COVERED |
| S7 AC1 | v4 approved with 5 rows; v3 keeps 4 rows, valid_to 2026-11-30; served by date | 007, 010, 011 | DIRECT | v3 read through `versions()` | COVERED |
| S7 AC3 | Case service and allocation engine each write one line per table; no customer identifier | 014, 021 | DIRECT | Two reader-bound consumers sharing one cache (TC-03) | COVERED |
| S7 §9 row 3 | VALIDATED → APPROVED | 008 | DIRECT | | COVERED |
| S7 §9 row 4; FR-RWB-011 "load/rollback path" | APPROVED → ROLLED_BACK; earlier version in force again | 024 | DIRECT | Built here (gate finding 101; D-RUN-10) | COVERED |
| S7 §10 RW-REFADM, RW-COE | Load right C; RW-COE only for tables it owns | 027 | DIRECT | Per-table loader list, fail closed: RW-COE has no built-in table by default (A-31) | COVERED |
| S7 §10 RW-RISK; API4 approve "approver role for the load's table" | Approve right A, per table | 027 | DIRECT | Per-table approver list as data (G-R03) | COVERED |
| S7 §11, §17 | DF-REF-159..171, 181..184 written; DF-REF-028/029 read through the P4 published interface | 001, 002 | DIRECT | `access.api.ListOfValuesReader` (P3 → P4) | COVERED |
| S7 §12 load | 201; 401/403/409/422/503; idempotency | 015, 006 | DIRECT | | COVERED |
| S7 §12 approve | 200; 401/403/404/409/503; repeat 200 same body | 016, 008 | DIRECT | | COVERED |
| S7 §12 interfaces | `ReferenceVersionRegistry`, `ReferenceDataService`, records, exception; no events | 007..012, 024, 025 | DIRECT | §12 signatures verbatim; `rollback` and the handler SPI added | COVERED |
| S7 §13 DB | Tables, constraints, append-only trigger | 001 | DIRECT | Guarded DDL | COVERED |
| S7 §13 step 2 | Column definitions from the RWB-E1-042 catalog; row check | 003, 029 | DIRECT | Catalog file + generator + this migration (G-R04) | COVERED |
| S7 §13 cache | TTL from `refdata.cache.ttl-seconds`; never serves non-APPROVED | 013 | DIRECT | | COVERED |
| S7 §13 step 6 (logger) | One line per table read | 014 | DIRECT | Engine start-up calls: seam | COVERED |
| S7 §13 step 7; D-RUN-10; D-RUN-11 | Load, approve and rollback endpoints wired; dispatch by table code | 015, 016, 024, 025, 026, 030 | DIRECT | Code in P3 `casewf.refdata.internal` (TE001 SU-08; GAP-53) | COVERED |
| S7 §13 flag | `rwb.p3.refdata-versions`; off = previous path | 018 | DIRECT | | COVERED |
| S7 §13 done-when (boundary) | No read of the two tables outside `casewf.refdata` | 019 | DIRECT | Plus dependency direction P3 → P4 only (TE001 SPEC-022 (d)) | COVERED |
| S7 §14 | MSG-P3-027, P7-002, GEN-001, GEN-004, P4-002 (+ P3-015, P4-003) | 020 | DIRECT | Text through RWB-E1-042 `MessageResolver` | COVERED |
| S7 §16 TC-11; TC7 TC-E1-043-11 | RW-CASEOWN load refused MSG-P4-002; nothing changes; refusal is logged | 015, 027, 028 | DIRECT | | COVERED |
| S7 §17 | No business literal, no personal data in logs, no foreign table read, append only, cache only APPROVED, no rule table | 001, 013, 014, 019, 021, 023 | DIRECT | | COVERED |
| API4 approve "decision log entry AC-VERS" | Approval recorded with AC-VERS | 008 | DIRECT | Through this story's package-private `ReferenceDecisionRecorder` (interim log, E42S §12.7 pattern; failure 503 MSG-P7-003); store and writer are seams | COVERED |
| REQ FR-RWB-011; REQ-DRI-011 | Versioned lists, valid-from/to, author/approver, maker-checker, load/rollback path | 001..013, 024 | DIRECT | | COVERED |
| REQ-CWC-006 | Roles, teams, queues and capacity as versioned reference data | 002, 007, 025 | DIRECT | Tables ROLE, TEAM, QUEUE served; queue content RWB-E1-019 | COVERED |
| REQ FR-RWB-012; BS-4.4 | Every admin action writes an access-log entry | 028 | DIRECT | Interim log sink; persistent access log RWB-E1-039 (seam) | COVERED |
| REQ NFR-RWB-005 | Method security, RBAC, audit | 015, 016, 024, 027, 028 | DIRECT | | COVERED |
| REQ NFR-RWB-006 | No personal data in logs/tests | 014, 023, 028 | DIRECT | | COVERED |
| REQ NFR-RWB-008 | Logs, metrics | 012, 014, 028 | DIRECT | | COVERED |
| REQ NFR-RWB-009 | Flag-off path | 018 | DIRECT | | COVERED |
| AUD A-06 | Flags and parameters are config literals | 013, 018, 027, 029 | DIRECT | | COVERED |
| DL10 D-RCV-29 (registry part) | Later dictionary changes are reference loads through RWB-E1-043 | 025, 027, 028, 031 | DIRECT | Registry and generic checks: route, version log, maker-checker, per-code lists, audit with change summary (TC-HD-04). The `sys_fields` handler and the `is_personal` protection are RWB-E1-064's (§"built by another story") | COVERED |
| Existing platform | 401 for no RW- role; Problem rendering; Flyway lint | — | INHERITED_EXISTING_BEHAVIOR | `SecurityConfig`, `ApiExceptionHandler`, `RecoveryMigrationLintTest` | COVERED |

Rows: 49. All `COVERED`; none `BLOCKED`. Revision 2's rows "S7 §10 RW-REFADM, RW-AUDIT reads" and "S7 §13
done-when (SIT)" moved to the next table (gate finding 123). Revision 4 adds the effective-date row (finding 132).

### Requirement lines built by another story (not counted as covered here)

| Source line | What is not built here | Owner (BS6 order) | Citation |
|---|---|---|---|
| S7 §10 "The same person may not hold RW-REFADM and RW-RISK" | Person-level separation of duty when roles are assigned | RWB-E1-022 (26), separation-of-duty version SOD-2026.11; RWB-E1-037 (27) | S7-022 line 88; S7-037 §13. Per-load maker-checker is built here (SPEC-008) |
| S7 §10 SY-RULES; D36 line 145 | Reading reference values as Drools facts | RWB-E1-072 (36) | D36 line 145; reads through `ReferenceDataReaders.forReader` (SPEC-014) |
| S7 §10 RW-REFADM, RW-AUDIT reads; §12 `GET /admin/lists/{listCode}` | Read of versions with author and approver by a person (HTTP). This story delivers and tests only the Java read `versions()` (SPEC-011) | Not named in any v7 story (GAP-34); open item to the BA | S7 §12, §13 step 7 (not a build step); S7-025 line 272 also calls it |
| S7 §13 done-when (SIT) | Version 1 of each of the 12 tables loaded and approved before SIT exit: content and column definitions | DELEGATION_LIMIT RWB-E1-038 (22); ROLE, TEAM, QUEUE RWB-E1-019 (25); DOCUMENT_TYPE RWB-E1-025 (30); PRODUCT_PARAMETER, SERVICE_LEVEL RWB-E1-045 (31); TEMPLATE RWB-E1-046 (32); LEGAL_PERIOD Legal, used by RWB-E1-028 (47); PRODUCT, REGION, EXPOSURE_BAND: none named (GAP-43) | SPEC-022; S7-028 lines 41, 46 |
| S7 §15 | Load result listed in the daily data quality report | RWB-E1-011 (57); its v7 story is silent (GAP-33) | S7 §15 |
| S7 BR6 sentence 2 (engine part), BR7/BR9 engine calls, §13 step 6 hooks | Engines read at start through `forReader`, stop on `NoVersionInForceException`, and record the version used with each decision | RWB-E1-018 (38), RWB-E1-020 (41), RWB-E1-028 (47); decision record RWB-E1-027 (20) | S7 §13 step 6; A-02 |
| API4 approve AC-VERS (persistent entry) | Decision log store and writer | RWB-E1-008 (12), RWB-E1-027 (20) | E42S §4.3 row 2 |
| REQ FR-RWB-012 (persistent entry) | Access log store | RWB-E1-039 (28) | AUD A-18; S7-039 |
| S7 §3 business date from `v_ace_batch_status` | The real `BusinessDateProvider` implementation | Story that reads the view after RWB-E1-069 (10) delivers it | E42S §4.3 row 6, CLAR-015; S7-069 line 230 (A-01) |
| S7 §10 RW-RISK A in the matrix | Permission matrix change | RWB-E1-037 (27) | S7 §10 "loaded through RWB-E1-037" |
| API4 `/verify` | Verify operation | No v7 behaviour (GAP-11) | API4 line 4961 |
| API4 load checklist fields, MSG-P3-022 | Change checklist | RWB-E2-041 | S7 §19 |
| DL10 D-RCV-29 (handler) | `sys_fields` handler adapting `DataDictionaryLoader`, its two catalog keys and its approver | RWB-E1-064 (13) | S7-064 §3, §4, §12; D-RUN-08, D-RUN-11; GAP-40 |
| S7-064 §11 (`is_personal` Read); orchestrator rulings 2026-11-18 | Runtime protection of `is_personal` marks against a dictionary load and its rollback | RWB-E1-064 (13); open item owner RW-COMPLY | SPEC-031 |
| TE011 §12 | PDPA lint of committed SQL, fixtures and logs (not a runtime check) | RWB-TE-011 (6) | GAP-38 |
| S7-019 flow step 5, BR3, AC9 | Applying the QUEUE and QUEUE_MEMBER versions in force to the `queue` and `queue_member` tables on the valid-from date (`QueueVersionApplier`, daily and on approval or rollback) | RWB-E1-019 (25) | SPEC-025 *Effective date*; SPEC-032 |

## Seams (D-RUN-08)

| Seam | Earlier story that provides it (used here) | Later story that replaces or uses it |
|---|---|---|
| Parameter values, catalog keys, PARAMETER loads | RWB-E1-042 `ParameterService`, `ParameterKeys`, `ParameterLoadHandler` (E42S §12.2) | — |
| Capability check C/A/U | RWB-E1-042 `access.api.CapabilityCheck` + interim grants file `access/interim-capability-grants.csv` (E42S SPEC-020, §12.10) | RWB-E1-037 replaces the implementation; RWB-E1-022 `AccessCheck` (S7-022 §12) |
| Business date | RWB-E1-042 `casewf.config.api.BusinessDateProvider` (interim Asia/Bangkok date, E42S SPEC-023) | Reader of `v_ace_batch_status` after RWB-E1-069 (A-01); that reader adds a P3 → P1 edge (E42S §4.3; GAP-51) |
| Message text | RWB-E1-042 `access.api.MessageResolver` (PACK §6.2, OI-E1-042-004) | Message table (GAP-06) |
| LOV-REF-TABLE codes | This story: `access.api.ListOfValuesReader` with the interim `access.internal.LovValueReader` (S7 §11, §17; A-41) | P4 owner, when `lov_value` reads are given a permanent home |
| AC-VERS decision entry | This story: package-private `ReferenceDecisionRecorder` port in `casewf.refdata.internal` with an interim log adapter (SPEC-008; A-43). RWB-E1-042's `VersionDecisionRecorder` is not published (E42S §12.7; GAP-50) | RWB-E1-027 replaces both adapters with a call to P7 `DecisionLogWriter` (E42S §12.7) |
| Admin-action and refusal audit | This story: `ReferenceLoadAudit` port, logging adapter (SPEC-028) | RWB-E1-039 (AC-DENY on 403) |
| Handlers for other modules' codes | This story: `ReferenceTableHandler` SPI and its contract (SPEC-025) | RWB-E1-001 (`data_product`), RWB-E1-064 (`sys_fields`), RWB-E1-019 (QUEUE, QUEUE_MEMBER), RWB-E1-025 (DOCUMENT_TYPE), others |
| Reader-bound reads | This story: `ReferenceDataReaders` (SPEC-014) | Engine stories, RWB-E1-072 |
| Dictionary loads (D-RCV-29) | This story: registry and generic checks only (SPEC-031) | RWB-E1-064 `sys_fields` handler with the `is_personal` protection (open item RW-COMPLY) |
| Governed change of the access lists | This story: `rwb.refload.*` keys out of reach of any load; change by reviewed catalog change (SPEC-026, A-39) | RWB-E1-037 (27), a path with its own approver (open item) |
| Actor ID of the caller | This story: `ActorIdResolver` (A-07) | RWB-E1-022 (26) session user |

## SPEC definitions (Backend Specification)

### Frontend Specification

`NOT_APPLICABLE`. S7 §15: no screen; SCR-39, SCR-40, SCR-42 are Epic 8 (S7 §19). The three endpoints
are backend-only and called by HTTP clients (`contracts/frontend-integrations.json`).

### Backend Specification

**SPEC-RWB-E1-043-001 Schema migration.** One file `V<seq>__rwb_e1_043_reference_versions.sql` in
`backend/src/main/resources/db/modulemigration/recovery/`, line 1 `-- Story: RWB-E1-043`, schema only
as `${recoverySchema}` (DL10 D-RCV-28; D-RUN-07; S7 §13's `${schema}` is GAP-18). `<seq>` is assigned
by the orchestrator at merge; no number is fixed here (D-RUN-07). The file is guarded so it gives one
end state on an empty schema and on the PS6 baseline (GAP-02, GAP-25):
- `reference_version`: `CREATE TABLE IF NOT EXISTS` with all PS6 columns (incl. `rollback_reason
  varchar(400)`, `verified_by`, `verified_at`, `verify_note`) and the 7 standard columns. Constraints
  added if absent: `uk_reference_version UNIQUE (table_code, version_no)` (PS6); `UNIQUE (table_code,
  valid_from, content_hash)`; `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`;
  `CHECK (status <> 'ROLLED_BACK' OR rollback_reason IS NOT NULL)`; partial unique index on
  `(table_code, valid_from) WHERE status = 'APPROVED'` (S7 §13); index on `load_id`.
- `reference_row`: `CREATE TABLE IF NOT EXISTS` with PS6 columns; `uk_reference_row UNIQUE (row_key)`
  dropped if present and `UNIQUE (version_id, row_key)` added (S7 §13; GAP-01: PS6's key makes AC1
  impossible); `fk_reference_row_version_id ... ON DELETE RESTRICT` and `ix_reference_row_version_id`
  kept (PS6).
- Append-only triggers (S7 §13, §17): `BEFORE UPDATE OR DELETE` on `reference_row` refuses always;
  `BEFORE UPDATE OR DELETE` on `reference_version` refuses DELETE (A-04) and any UPDATE that changes a
  column other than `status`, `approver_user_id`, `approved_at`, `valid_to`, `rollback_reason`,
  `version`, `updated_at`, `updated_by`. `is_active`, `state`, `created_at`, `created_by` are frozen;
  this is narrower than S7 §13 ("the standard columns") and recorded as a deviation (A-33; gate finding
  114). `is_active` stays `true` and is never read by resolution.
- The file holds no `CREATE SCHEMA`, `CREATE ROLE`, `GRANT`, `REVOKE` or `SET search_path`, and no `R__`
  script exists (lint). It seeds no row in `reference_version`, `reference_row` or `lov_value`.
- One guarded `INSERT ... ON CONFLICT (param_key) DO NOTHING` block of the 38 `parameter_catalog` rows
  of SPEC-029, generated from the same `config/parameter-catalog.csv` lines (E42S line 106: "A new key
  also needs a migration in the story that adds it"; E42S CLAR-003). No `parameter_value` row: the
  catalog default is served with `versionNo 0` (E42S SPEC-007).

**SPEC-RWB-E1-043-002 Table-code check (built-in path).** A code that is not `PARAMETER` (SPEC-026) and
has no registered handler (SPEC-025) is accepted only when (a) it is an active `value_code` of
`LOV-REF-TABLE` returned by P4's published `ListOfValuesReader.activeCodes("LOV-REF-TABLE")` (`access.api`,
`Set<String> activeCodes(String lovCode)`; interim implementation `access.internal.LovValueReader` reads
`lov_value` with `lov_code = 'LOV-REF-TABLE'` and `is_active`; S7 §11 DF-REF-028/029 and §17 "through the
P4 published interface"; table present through the PS6 load, GAP-32; A-41) and (b) its column definition is not the
empty token (SPEC-003). (a) fails → MSG-P3-027 `{check}` = "table code is not a reference table";
(b) fails → MSG-P3-027 `{check}` = "no column definition for the table"; both 422, nothing written.
This refuses the 5 rule codes and HOLIDAY that PS6 seeds, because no catalog key exists for them
(GAP-04). The read is a P3 → P4 call, the direction RWB-TE-001 allows (TE001 SPEC-022 (d); SPEC-019;
A-10). Revision 3's `ReferenceTableCodeSource` (a P3 SPI implemented in P4) is withdrawn because it made P4
depend on P3 (finding 131). Review 3 suggested moving the LOV read into P3; S7 §11 and §17 require the
P4 published interface, so the reader stays in P4 and P3 calls it.

**SPEC-RWB-E1-043-003 Column definitions and row check.** `ReferenceTableColumns` reads the definition
of a code through `ParameterService` with the generated key `refdata.columns.<code>` (code lower case,
underscore kept, as in S7-037 line 46 `rwb.refload.approver.masking_rule`; looked up by name, A-26),
value type STRING (S7 §13 step 2; SPEC-029). Grammar (A-34):
`name:TYPE[:R][:K]` items joined by `;`, `TYPE ∈ STRING|INTEGER|DECIMAL|BOOLEAN|DATE|CODE`, `R` =
required, `K` = key column; the default `none` means "no definition". The value must fit
`parameter_value.param_value varchar(400)` (PS6; GAP-30). The `K` columns form `row_key` (joined by
`|`, max 200 chars, PS6). `ReferenceRowCheck` checks every data row: required present, value parses to
its type, unknown column refused, `row_key` unique in the file. Every failure is collected. A load with
any failure is refused in full, 422 MSG-P3-027: `{check}` names the first failing data row (1-based,
header excluded; A-11) and column, `field` = that column (AC4 "row 12", `limit_days`), and `detail`
lists every failed row and column, capped at 100 entries with the total count (RWB-E1-019 flow step 3
"names every failed row"; G-R02; A-11). Nothing is written. For a handler code this check runs only
when a definition exists (SPEC-025 L12; A-37).

**SPEC-RWB-E1-043-004 Empty file.** No data rows (header only or zero bytes) → 422 MSG-GEN-001,
`{field}` = `rows`, `field` = `rows` (S7 X7, AC10, §12). Checked before the row check.

**SPEC-RWB-E1-043-005 Valid-from check.** `validFrom` < business date (SPEC-017) → 422 MSG-P3-027,
`{check}` = "valid from is before the business date" (same text as E42S §12.5 row 3), `field` =
`validFrom` (S7 BR6, X3, AC6). Equal is accepted (A-05). Missing or unparseable `validFrom` → 422
MSG-GEN-001 `{field}` = `validFrom` (A-12; 400 is not used, GAP-28).

**SPEC-RWB-E1-043-006 Content hash and idempotency.** `content_hash` = lower-case hex SHA-256 of the
canonical rows: sorted by `row_key`; each row JSON with sorted keys and type-normalised values; joined
by `\n`; UTF-8 (S7 §13 step 3; A-13). A value that does not parse to its type is hashed as its trimmed
text; a stored version passed every check, so such a file never matches one. Order (SPEC-025 L9-L11;
finding 133): after the file is read and has rows, and **before** the valid-from check: (1) a version with the same `(table_code,
valid_from, content_hash)` exists → return it unchanged, write nothing, 201 with the same body, any
status (S7 X4, AC7; A-06), or, for a handler code whose `repeatMessage` is present, 409 with that message
(SPEC-025 L9; A-38); so a repeat answers the same way for any business date, as RWB-E1-001 AC10 needs
(S7-001 AC10); (2) after the valid-from check (SPEC-005), an APPROVED version of the table with this
`valid_from` → 409 MSG-P3-027 `{check}` = "an approved version already has this valid from" (S7 §12).

**SPEC-RWB-E1-043-007 Record version.** `recordVersion(tableCode, validFrom, authorUserId, loadId, rows)`
(S7 §12, verbatim) in one transaction: `version_no` = max + 1 per table under a transaction-scoped
lock (A-15); one `reference_version` (VALIDATED, `row_count`, `content_hash`, `load_id`,
`author_user_id`) and one `reference_row` per data row (`row_key`, `row_data` jsonb). `loadId` is a new
UUID per HTTP call; the response `id` is `load_id` (API4 `ReferenceLoad.id`). A unique-key race is
re-read: the identical case returns the existing load, otherwise 409 MSG-GEN-004 (A-15). For a handler
code, `handler.validate` runs after the generic checks pass (SPEC-025).

**SPEC-RWB-E1-043-008 Approve.** `approve(loadId, approverUserId)` (S7 §12): unknown `loadId` → 404
MSG-P4-003 (S7 §12; wording GAP-27); `approverUserId` null → 409 MSG-P7-002 (S7 X1); approver = author
→ 409 MSG-P7-002, stays VALIDATED (S7 AC2); status APPROVED → 200 current body, nothing written (S7 §12
idempotency); status ROLLED_BACK → 409 MSG-P3-027 `{check}` = "only a validated load can be approved"
(A-16); `validFrom` < business date → 409 MSG-P3-027 (A-17); APPROVED twin with the same `valid_from`
→ 409 MSG-P3-027 (partial unique index; A-16). Success, in one transaction: status APPROVED,
`approver_user_id`, `approved_at` = now (Asia/Bangkok), SPEC-010, cache eviction (SPEC-013), for a
handler code `handler.apply(loadId, file, validFrom)` (SPEC-025, SPEC-032), and one call to this
story's package-private port `ReferenceDecisionRecorder.recorded(String decisionCode, String table,
UUID loadId, LocalDate validFrom, UUID approverUserId)` in `casewf.refdata.internal`
(`@Transactional(propagation = MANDATORY)`, the E42S §12.7 pattern) with decision code `AC-VERS` (API4
line 3233). Its interim adapter `LoggingReferenceDecisionRecorder` writes one INFO line
`event=DECISION_RECORDED decisionCode=AC-VERS table=<code> loadId=<id> validFrom=<date>`, with no user ID
(BS-4.6; A-30). A recorder failure rolls the approval back and answers 503 MSG-P7-003 (MSG4 line 208;
E42S §12.7, SPEC-RWB-E1-042-025). RWB-E1-042's `VersionDecisionRecorder` is package-private in
`casewf.config` (E42S §12.7), so it is not called (GAP-50; A-32, A-43). RWB-E1-027 replaces the adapter
with a call to P7 `DecisionLogWriter`. Approval writes a new version only; it never changes the rows of
another version or what a business date before `validFrom` reads (SPEC-032). Response 200
`ReferenceLoad` status APPROVED. The approve right is enforced at the endpoint (SPEC-027).

**SPEC-RWB-E1-043-009 Concurrent approval.** The approve update is conditional on the `version` read
(JPA `@Version`). The loser gets 409 MSG-GEN-004 and writes nothing (S7 X5, AC8, §13 step 4).

**SPEC-RWB-E1-043-010 Replaced version.** In the approve transaction, the APPROVED version of the same
table with the greatest `valid_from` < new `valid_from` gets `valid_to` = new `valid_from` − 1 day
(S7 BR8, AC1). If an APPROVED version with a later `valid_from` exists, the new version's `valid_to` =
that `valid_from` − 1 day (A-18). Each version is independent, so approval out of `valid_from` order is
allowed (SPEC-032). No row of another version changes (trigger, SPEC-001). Resolution uses SPEC-011 only.

**SPEC-RWB-E1-043-011 Version in force and versions.** `versionInForce(tableCode, businessDate)` = the
APPROVED version with the greatest `valid_from` ≤ `businessDate`; VALIDATED and ROLLED_BACK are never
returned (S7 BR3, §17). `rows(...)` returns `VersionedRows` (rows ordered by `row_key`).
`versions(tableCode)` returns all versions, newest first, any status, with author, approver,
`approved_at` and `rollback_reason` (S7 §12; AC1 v3 read; RW-AUDIT and RW-REFADM read in Java).
`IN_FORCE` is derived, never stored (A-19).

**SPEC-RWB-E1-043-012 No version in force.** `rows`/`versionInForce` throw
`NoVersionInForceException(tableCode, businessDate)` (S7 §12), write one ERROR line with
`messageCode=MSG-P3-027`, the reader name (SPEC-014), table code and business date, and increment the
counter `rwb.refdata.no_version_in_force` tagged `table` (S7 X6, AC9; A-03). A caller that gets the
exception does not start its run (S7 BR9); engines that must do so are later stories (A-02).

**SPEC-RWB-E1-043-013 Cache.** `ReferenceRowCache` keyed by `(tableCode, businessDate)`; TTL =
`refdata.cache.ttl-seconds` through `ParameterService` (E42S §12.4: 300, required); no YAML literal.
Only APPROVED results are cached; `NoVersionInForceException` is not cached. Approve and rollback evict
every entry of the table after commit (A-20). No new dependency (AG §4.4).

**SPEC-RWB-E1-043-014 Reader-bound version logging.** Published `ReferenceDataReaders` (P3 api):
`ReferenceDataService forReader(String readerName)` and `boolean enabled()` (SPEC-018). `readerName`
must match `^[a-z][a-z0-9-]{1,39}$` and names a component (for example `case-service`,
`allocation-engine`, `sy-rules`), never a person (A-29); an invalid name throws
`IllegalArgumentException`. The returned service has the S7 §12 signatures. `ReferenceVersionLogger`
writes one INFO line `event=REFERENCE_READ reader=<name> table=<code> version=<n> validFrom=<date>
businessDate=<date>` for every `rows(...)` or `versionInForce(...)` call of a bound service, on cache
hit and miss alike, except that a repeat of the same `(reader, table, version, businessDate)` within one
cache TTL window is not logged again (`ReaderLogGate`, A-29). So each engine writes one line per table
at start and after each expiry (S7 AC3, BR7, §13 step 6). The line carries no row content, no user ID
and no customer identifier (S7 §17; BS-4.6). The plain `ReferenceDataService` bean (S7 §12) behaves as
`forReader("unnamed")`; engine stories must use `forReader` (shared update).

**SPEC-RWB-E1-043-015 Load endpoint (code in P3 `casewf.refdata.internal`; API4 tags the operation P4).** `POST /api/recovery/v1/admin/reference-loads`, multipart
(`file` CSV or XLSX one sheet, `table`, `validFrom` ISO date) (S7 §12; API4).
`@PreAuthorize("@referenceLoadAuthority.mayLoad(authentication, 'Reference data', 'C', #table)")`
(names area and right: AG §3.3, BS-3.2; SPEC-027). `ReferenceLoadFileReader` turns the file into
`List<Map<String,Object>>` with the header row as column names (CSV RFC 4180 UTF-8; XLSX first sheet;
A-21). Author = the actor ID from `ActorIdResolver` (`casewf.refdata.internal` seam: the `oid` claim when it is a UUID,
else `sub` when it is a UUID, else 401 MSG-P4-001; RWB-E1-022 replaces it; A-07; finding 127).
`ReferenceLoadDispatcher` routes by `table`
(SPEC-030). Responses: 201 `ReferenceLoad {id, table, validFrom, status, rows}`; 401 MSG-P4-001
(existing filter); 403 MSG-P4-002; 409/422 per SPEC-002..006; 503 when the store or the business date
is unavailable (A-01, A-22). Errors are `application/problem+json` (API4 Problem). Missing `file`,
`table` or `validFrom` → 422 MSG-GEN-001 naming the field (A-12; GAP-28). `mayLoad` grants the table right
when `table` is absent or blank, so a load with no `table` gets 422 MSG-GEN-001 `{field}` = `table`, not
403 (SPEC-025 L3; finding 136). The 404 of a branch whose flag is off (SPEC-018) and the 500 of a handler
defect (SPEC-025) are not listed in API4 for this operation (GAP-48).

**SPEC-RWB-E1-043-016 Approve endpoint (P3 `casewf.refdata.internal`).** `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`,
no body. `@PreAuthorize("@referenceLoadAuthority.mayApprove(authentication, 'Reference data', 'A', #loadId)")`.
Approver = actor ID (A-07). Dispatch by `loadId` per SPEC-030. Responses per SPEC-008/009: 200, 401,
403, 404, 409, 503 (store, business date, or decision recorder MSG-P7-003).

**SPEC-RWB-E1-043-017 Business date.** The business date for SPEC-005, SPEC-008 and SPEC-024 comes from
RWB-E1-042's published `casewf.config.api.BusinessDateProvider` (same module; E42S SPEC-023; interim:
today in Asia/Bangkok). This
story does not read `v_ace_batch_status`: the view is RWB-E1-069's (BS6 order 10, S7-069 line 230), a
later story (D-RUN-08). The rule for the real implementation (greatest `business_date` with
`is_complete = true`) is passed to its owner (A-01; GAP-12). A provider failure → 503 MSG-P3-027
`{check}` = "no business date". Read callers pass their own business date (S7 §12).

**SPEC-RWB-E1-043-018 Feature flag.** `rwb.p3.refdata-versions` in `application.yaml`, default `false`,
`true` in the local profile (S7 §13; AG §3.13). It is not added to `RecoveryFlags` or `RecoveryProperties`:
RWB-TE-001 replaces `RecoveryProperties` with package-private module records (TE001 SPEC-023), and
RWB-E1-042 binds its own flag only by `@ConditionalOnProperty` (E42S §12.12). Binding (finding 131; A-44):
the write-side beans `ReferenceTableHandlers` and `LoggingReferenceDecisionRecorder` carry
`@ConditionalOnProperty(prefix = "rwb.p3", name = "refdata-versions", havingValue = "true")`;
`ReferenceDataReaders.enabled()` and the registry's write methods read `RefdataSettings`, a package-private
record in `casewf.refdata.internal` bound to prefix `rwb.p3`; the controller and dispatcher carry
`@ConditionalOnExpression("${rwb.p3.refdata-versions:false} or ${rwb.p3.configservice:false}")`.
Behaviour (gate finding 119):
- Read side always present: `ReferenceDataService` and `ReferenceDataReaders` beans exist whatever the
  flag, so a later story that injects them starts either way. `ReferenceDataReaders.enabled()` returns
  the flag; a caller that sees `false` keeps its previous source (S7 §13 "Off: the engines read the
  reference values loaded before this story"; today no engine reads reference data, A-23).
- Write side gated: the registry's `recordVersion`, `approve` and `rollback` and the handler path run
  only when the flag is on.
- Controller: mapped when `rwb.p3.refdata-versions` **or** RWB-E1-042's `rwb.p3.configservice` is on
  (D-RUN-10: one shared endpoint). A request routed to a branch whose flag is off gets 404 MSG-P4-003,
  as if the operation were absent (D-RCV-36 flag rule as cited in E42S SPEC-021). Both off → no mapping,
  404.

**SPEC-RWB-E1-043-019 Module boundary and dependency direction (finding 131).** The module map is RWB-TE-001
v4's (TE001 SPEC-022 (d): P3 `casewf` depends on P2 `integration` and P4 `access`; neither may depend on
`casewf`; `ModulithTest` rejects a cycle, D-RCV-11). All code of this story is in P3 `casewf.refdata`; the
published package is `casewf.refdata.api`, declared `@NamedInterface(name = "refdata.api", propagate =
false)` and added to the casewf `published` list of `recovery-modules.yaml` in the same merge request
(TE001 SU-08; SPEC-004 (e): no public type directly in a module base package). Every edge this story adds:

| From | To | Types | Module edge | Allowed by |
|---|---|---|---|---|
| `casewf.refdata.internal` | `access.api` | `CapabilityCheck`, `MessageResolver`, `ApiProblemException`, `ApiError`, `ListOfValuesReader` | P3 → P4 | TE001 SPEC-022 (d) (same direction as `casewf.admin` → `access.api`) |
| `casewf.refdata.internal` | `casewf.config.api` | `ParameterService`, `ParameterKeys`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider` | inside P3 | E42S §12.2 |
| `casewf.refdata.internal` | `casewf.refdata.api` | own published types | inside P3 | — |
| `access.internal.LovValueReader` | `access.api` | `ListOfValuesReader` | inside P4 | — |

No P4 or P2 type refers to a `casewf` type, so P4 → P3 does not exist and there is no P3 ↔ P4 cycle.
Later edges, added by their own stories: P1 `dataengine` handlers of RWB-E1-001 and RWB-E1-064 →
`casewf.refdata.api` (P1 → P3); the P3 QUEUE handler of RWB-E1-019 (`casewf.queues`) is inside P3. Today no
P3 → P1 edge exists (TE001 SPEC-022 (d)), so these add no cycle. E42S §4.3 plans a P3 → P1 business-date
reader of RWB-E1-069's views; together with the P1 handlers that would be a P1 ↔ P3 cycle. Recorded as
GAP-51 with an open item for the tech lead and the RWB-TE-001, RWB-E1-001, RWB-E1-064 and RWB-E1-069
owners (alternative: the SPI in `access.api`, which S7-001 §12 names); Blocker = No for this story.
`RecoveryBoundaryTest` gains two rules: (1) no class outside `recovery.casewf.refdata` references
`ReferenceVersionEntity`, `ReferenceRowEntity` or their repositories, and no native SQL outside it names
`reference_version`/`reference_row` (S7 §13 done-when; AG §3.11); (2) no class in `recovery.access..` or
`recovery.integration..` depends on `recovery.casewf..`. `ModulithTest.verify()` stays green. The
PARAMETER branch calls only RWB-E1-042's published `ParameterLoadHandler` and never reads
`parameter_value` (AG §3.11; D-RUN-10) (A-24).

**SPEC-RWB-E1-043-020 Messages.** Story messages are rendered by RWB-E1-042's `access.api.ApiProblemException`
with message ID, status, placeholders and `field`, and `access.api.MessageResolver` (E42S §10.2, §12.2; interim seam per PACK
§6.2 and OI-E1-042-004; GAP-06). MSG-P3-027 uses MSG4's wording "The version in force is unchanged"
(GAP-05). MSG-P4-003's case wording is kept for an unknown load (GAP-27).

| ID | HTTP | `{placeholders}` | Used by |
|---|---|---|---|
| MSG-P3-027 | 422 / 409 / 503 | `table`, `check` | SPEC-002, 003, 005, 006, 008, 012, 017, 024 |
| MSG-GEN-001 | 422 | `field` (`rows`, `validFrom`, `file`, `table`, `reason`) | SPEC-004, 005, 015, 024 |
| MSG-P7-002 | 409 | — | SPEC-008 |
| MSG-P7-003 | 503 | — | SPEC-008 (decision recorder failure; MSG4 line 208; E42S §12.7) |
| MSG-GEN-004 | 409 | — | SPEC-007, 009, 024 |
| MSG-P3-015 | 409 | `table` | SPEC-024 (MSG4: "There is no earlier version of {table} to return to.") |
| MSG-P4-001/002/003 | 401/403/404 | `action` for P4-002 | SPEC-015, 016, 024, 027 (existing `ApiError`) |

**SPEC-RWB-E1-043-021 Holiday and rule exclusion.** No code path loads, stores or serves HOLIDAY or a
rule table. The holiday calendar is ACE data in `v_ace_holiday` (S7 BR1; D35). No `rule_row` or
`rule_package*` access (S7 §11; D36; AG §4.9). Registering a handler for `PARAMETER` or registering the
same code twice fails start-up (SPEC-025).

**SPEC-RWB-E1-043-022 First versions in SIT (seam; finding 123).** S7 §13 done-when asks for version 1
of each of the 12 tables approved before SIT exit. This story delivers and tests the load and approve
path (TC-E1-043-01..10). The content and column definitions come from later stories (BS6 order):
DELEGATION_LIMIT RWB-E1-038 (22); ROLE, TEAM, QUEUE RWB-E1-019 (25); DOCUMENT_TYPE RWB-E1-025 (30);
PRODUCT_PARAMETER and SERVICE_LEVEL RWB-E1-045 (31; S7-028 line 41); TEMPLATE RWB-E1-046 (32);
LEGAL_PERIOD owned by Legal and first read by RWB-E1-028 (47; S7-028 line 46); PRODUCT, REGION and
EXPOSURE_BAND have no named owner (GAP-43). The line is therefore listed under §"Requirement lines built
by another story", not COVERED. This story's own SIT exit is judged on its test cases; the release SIT
exit for the 12 tables waits on the latest content story (RWB-E1-028, order 47) and on owners for the
three unowned tables (open item).

**SPEC-RWB-E1-043-023 Test data.** All fixtures synthetic and story-tagged; user IDs are random UUIDs
standing for U-REF-01, U-RSK-01, U-RSK-02 (S7 §7); no real name, ID or account (RUN-BRIEF; CTX
testing §2).

**SPEC-RWB-E1-043-024 Rollback.** Registry operation (added to the published `ReferenceVersionRegistry`):
`ReferenceVersion rollback(UUID loadId, UUID actorUserId, String reason)`. Endpoint
`POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback`, body API4 `RollbackRequest {reason}`,
optional `Idempotency-Key` header (S7 §9 row 4; REQ FR-RWB-011; API4 line 5004; S7-019 §12; D-RUN-10).
`@PreAuthorize("@referenceLoadAuthority.mayRollback(authentication, 'Reference data', 'U', #loadId)")`.
Rules, in order:
1. `reason` missing, blank or over 400 characters after trim → 422 MSG-GEN-001 `{field}` = `reason`
   (S7-019 §12; PS6 `rollback_reason varchar(400)`; E42S §7.4).
2. Unknown `loadId` (after SPEC-030) → 404 MSG-P4-003.
3. Status ROLLED_BACK → 200 with the current body, nothing written (S7-019 §12 "a repeat returns the
   first result"; state-based, the header is accepted and not stored; A-27).
4. Status VALIDATED → 409 MSG-P3-027 `{check}` = "only an approved load can be rolled back" (E42S §8
   row text).
5. A later APPROVED version of the same table exists (greater `valid_from`) → 409 MSG-P3-027 `{check}` =
   "only the latest approved version can be rolled back" (S7 §9 "A later version is rolled back"; A-27).
   The latest approved version may be rolled back whether or not it is already in force: S7-019 AC2 rolls
   back the version in force (version 3) so that version 2 is in force again, and BR5 asks for one call.
   The orchestrator's protective default (refuse once effective) applies only where the sources are
   silent; here S7-019 AC2 speaks, so the story rule is followed and the difference is GAP-52.
6. No earlier APPROVED version of the table → 409 MSG-P3-015 `{table}` (S7-019 X4, AC7; MSG4).
7. A handler code whose handler does not support rollback → 409 MSG-P3-027 `{check}` = "rollback is not
   available for this table" (SPEC-025).
Effect, one transaction: status ROLLED_BACK, `rollback_reason`, `updated_by` = actor, `updated_at`
(S7-019 AC2 "records the rollback with the caller, the time and the reason"); the restored version (the
APPROVED version with the greatest `valid_from` before the rolled-back one) gets `valid_to` = NULL. For a
version not yet in force, nothing changes for any business date before its `valid_from`; for a version in
force, the restored version answers from the next read (SPEC-032); for a handler code, `handler.onRolledBack(...)` with the
restored version's rows (S7-019 flow step 8, re-apply); optimistic lock loss → 409 MSG-GEN-004. After
commit the table's cache entries are evicted and the next read serves the restored version (S7-019 BR5).
Response 200 `ReferenceLoad` status ROLLED_BACK. A later identical reload of the rolled-back content
with the same `valid_from` returns the ROLLED_BACK load (SPEC-006 rule 1); a new `valid_from` is needed
to load it again (A-27). `PARAMETER` rollbacks go to RWB-E1-042 (SPEC-026). Rule-package rollback is
RWB-E1-073's (D36 line 145; S7 §9). Rollback is a single-person action by a holder of U on the table's
loader list (S7-019 flow step 8 has RW-REFADM call it): it restores a version that a non-author already
approved and is not a new approval, so no second person is needed (A-27; finding 125).

**SPEC-RWB-E1-043-025 Handler registry and its contract for codes other modules own (D-RUN-11; gate
finding 120; RWB-E1-001 gate 2 finding 014).** Published SPI in `casewf.refdata.api` (TE001 SU-08: "the
handler registry goes in" that package). The first three
methods are verbatim from S7-001 §12; the rest are defaults this story adds (A-37, A-38):

```java
public interface ReferenceTableHandler {
    String tableCode();
    ValidationReport validate(ReferenceLoadFile file);
    int apply(UUID loadId, ReferenceLoadFile file, LocalDate validFrom);
    default List<String> keyColumns() { return List.of(); }
    default Optional<HandlerMessage> repeatMessage(ReferenceLoadFile file) { return Optional.empty(); }
    default boolean supportsRollback() { return false; }
    default void onRolledBack(UUID rolledBackLoadId, UUID restoredLoadId,
                              ReferenceLoadFile restoredFile, LocalDate restoredValidFrom) {
        throw new UnsupportedOperationException();
    }
    default List<String> changeSummary(ReferenceLoadFile file) { return List.of(); }
}
public record ReferenceLoadFile(String tableCode, LocalDate validFrom, List<String> columns,
                                List<Map<String, Object>> rows) {}
public record HandlerMessage(String messageCode, Map<String, String> placeholders) {}
public record RowCheckFailure(int row, String column, String messageCode, Map<String, String> placeholders) {}
public record ValidationReport(List<RowCheckFailure> failures) { public boolean ok() { return failures.isEmpty(); } }
```

`RowCheckFailure.row` is the 1-based data row (header excluded); `0` means the file as a whole.
`column` may be null; it becomes the Problem `field`.

*Registration.* Another module registers a handler by publishing a Spring bean of this type behind its
own feature flag. `ReferenceTableHandlers` (P3 internal) builds the map `tableCode → handler` at
start-up; a second bean for the same code, or a bean for `PARAMETER`, fails start-up naming both classes.
A handler code needs no LOV-REF-TABLE row (D-RUN-11; GAP-31). The registry decides handler vs built-in;
the dispatcher only separates `PARAMETER` (SPEC-030).

*Load checks, in this order; the first failure answers and nothing is written on any refusal:*

| # | Check | Refusal |
|---|---|---|
| L1 | Authenticated; actor ID resolved (SPEC-015) | 401 MSG-P4-001 |
| L2 | Area right Reference data C (`CapabilityCheck`, SPEC-027) | 403 MSG-P4-002, audit |
| L3 | `table` present and not blank (finding 136: before any table right) | 422 MSG-GEN-001 `{field}` = `table` |
| L4 | Caller's role in `rwb.refload.loader.<code>`; a missing key or empty value refuses | 403 MSG-P4-002, audit |
| L5 | Registry branch flag on (SPEC-018) | 404 MSG-P4-003 |
| L6 | `file` and `validFrom` present and parseable | 422 MSG-GEN-001 `{field}` |
| L7 | File readable (CSV or XLSX, SPEC-015) | 422 MSG-P3-027 `{check}` = "the file cannot be read" |
| L8 | At least one data row (SPEC-004) | 422 MSG-GEN-001 `{field}` = `rows` |
| L9 | Repeat: a version with the same `(table, validFrom, content_hash)` exists (SPEC-006); runs before L10 so it answers the same for any business date (finding 133) | `repeatMessage` present → 409 Problem with that message ID and placeholders, nothing written (A-38); absent → 201 with the existing body |
| L10 | `validFrom` ≥ business date (SPEC-005) | 422 MSG-P3-027 |
| L11 | No APPROVED version of the table with this `validFrom` (SPEC-006) | 409 MSG-P3-027 |
| L12 | Column definition and row check (SPEC-003), only when `refdata.columns.<code>` exists and is not `none` | 422 MSG-P3-027 |
| L13 | `handler.validate(file)` | 422 with the first failure's `messageCode`, `placeholders` and `field`; `detail` = every failure's rendered text, in order, joined by "; ", capped at 100 with the total (as SPEC-003) |
| L14 | `row_key` unique in the file (safety net after `validate`) | 422 MSG-P3-027 `{check}` = "row key repeated" |
| L15 | Record the VALIDATED version (SPEC-007); audit DONE with `changeSummary` (SPEC-028) | — |

- `row_key` for a handler code = the `keyColumns()` values joined by `|`; if empty, the `K` columns of
  the definition (L12); if neither, the 6-digit data row number (A-37). `content_hash` uses that key
  (SPEC-006).
- *Message pass-through.* The registry renders the handler's own message ID and placeholders through
  RWB-E1-042's `ApiProblemException` and `MessageResolver` (SPEC-020); it never maps them to MSG-P3-027.
  MSG-P3-027 is used only for the registry's own checks (L7, L10, L11, L12, L14). An `ApiProblemException`
  thrown by `validate`, `apply` or `onRolledBack` is returned unchanged. Any other exception from
  `validate` is a defect → 500 with `traceId`, nothing written; from `apply` or `onRolledBack` → the
  transaction rolls back, 409 MSG-GEN-004. Each message ID a handler uses must be in RWB-E1-042's message
  catalog (owning story's task).
- *Repeat raised by a handler (finding 133).* The repeat of RWB-E1-001 AC10 is decided by L9 through
  `repeatMessage`, before the valid-from check, so it holds for any business date. A handler may also
  return MSG-P1-011 from `validate` for the wider S7-001 X7 case (a file equal to the version in force
  under a different `validFrom`); that refusal is a pass-through 422 at L13, after L10 (GAP-44).
- *Approve.* L1, L2 (A), approver list `rwb.refload.approver.<code>`, flag, unknown `loadId` 404, author
  409 MSG-P7-002, then SPEC-008's checks. Then one transaction: status APPROVED, `valid_to` (SPEC-010),
  `apply(loadId, file, validFrom)` with the stored rows, `ReferenceDecisionRecorder` AC-VERS (SPEC-008).
  After commit: cache eviction, audit DONE with `changeSummary`.
- *Effective date (finding 132; SPEC-032).* `apply` runs in the approve transaction, which may be days
  before `validFrom`. The handler stores the version as a dated version keyed by `validFrom` and never
  overwrites or changes a row that a reader gets for a business date before `validFrom`; its readers
  select by business date (S7 BR3; S7-019 BR3 and AC9). The data dictionary gives the handler tables
  their date columns: `data_product.valid_from` "comes into force" (DD8 DF-REF-079), `queue_member`
  `valid_from`/`valid_to` (DD8 DF-WRK-051/052). A handler whose target table holds only the current state
  (for example `queue`, DD8 DF-WRK-038 `table_version`) does not change that table in `apply`; it applies
  the version in force on its valid-from date with its own job that reads `versionInForce(code,
  businessDate)` (S7-019 flow step 5 `QueueVersionApplier`). Versions are independent, so `apply` for an
  earlier `validFrom` approved after a later one must not change the later version's rows.
  `onRolledBack` follows the same rule. The registry proves the rule with a dated test handler
  (TC-TM-01..04); each owning story tests its own handler against it (shared update).
- *Rollback.* SPEC-024 rules; rule 7 refuses when `supportsRollback()` is false. In the transaction,
  `onRolledBack(rolledBack, restored, restoredFile, restoredValidFrom)` with the restored version's rows.
  Rollback is a single-person action by a U holder on the loader list (A-27).
- Hash and version history stay in this story's tables (E01S ASM-E1001-05).

*What the owning story supplies (and nothing else is needed from it):*
1. The handler bean behind its own flag; while it is absent the code is unknown and refused with 422
   MSG-P3-027 "table code is not a reference table".
2. Two `parameter_catalog` rows, `rwb.refload.loader.<code>` and `rwb.refload.approver.<code>`
   (CODE_LIST, BUSINESS, GLOBAL, `required=false`, environments DEV,SIT,UAT,PROD, owner RW-RISK, default
   the roles its story names), in `config/parameter-catalog.csv` and as `INSERT ... ON CONFLICT
   (param_key) DO NOTHING` in its own migration (E42S line 106).
3. Its message IDs in RWB-E1-042's message catalog.
4. Optionally `refdata.columns.<code>`; it is not required (A-37). When present, L12 runs before the
   handler, so a handler that wants its own messages to lead keeps it to types and keys, or omits it.

*`data_product` (RWB-E1-001, BS6 order 9).* Not refused by design (D-RUN-11). Conforming handler:
`keyColumns` = `product_code`; `validate` returns its K0-K5 failures with its own IDs (MSG-GEN-001,
MSG-P3-027 for its K0, MSG-P1-003, MSG-P1-004, MSG-P1-007; S7-001 X4-X6; E01S SPEC-013), which reach the
caller unchanged at 422; `repeatMessage` = MSG-P1-011 `{source}` = "data product catalog", `{date}` =
`validFrom` (S7-001 X7), so a repeat answers 409 MSG-P1-011 and writes nothing; no
`refdata.columns.data_product` row (E01S SPEC-013 "E1-043 holds no column definition"); catalog defaults
loader `RW-REFADM` (S7-001 X8) and approver `RW-DATASTEW` (S7-001 flow step 9) (A-40); no LOV-REF-TABLE
row. S7-001 X7 defines a repeat as a file matching "the version in force"; this registry tests the same
`(table, validFrom, hash)`; the difference is GAP-44. All S7-001 refusals are 422; the repeat is 409 here
(GAP-44).

*QUEUE and QUEUE_MEMBER (RWB-E1-019).* Its `ReferenceTableCheck` maps onto `validate` (MSG-P1-002 row and
check, MSG-GEN-002 field, min, max: S7-019 AC4, AC5), its `ReferenceRollbackHandler` onto
`supportsRollback`/`onRolledBack` (G-R01, G-R02; GAP-08, GAP-39). Its `QueueVersionApplier` stays its
own job: it applies the version in force to `queue` and `queue_member` on the valid-from date, daily and
after approval or rollback (S7-019 flow step 5, BR3, AC9), so `apply` and `onRolledBack` do not change
those current-state tables early (*Effective date*). QUEUE is also a built-in code with a column
definition, so L12 runs first; to keep its own messages leading RWB-E1-019 sets a definition with types
and keys only. QUEUE_MEMBER is a handler code and needs no LOV-REF-TABLE row (D-RUN-11), although
S7-019 line 38 says it "is added to" the list; recorded as GAP-49 with a note to RWB-E1-019.

- `changeSummary` names, without row values or personal data, what a load changes (for example
  `DF-TST-001 owner_role`); the registry adds the items to the version log line and the audit events of
  that load (SPEC-028, SPEC-031; A-35). Default: nothing.
- The SPI lives in P3 `casewf.refdata.api`, not P4 as S7-001 §12 says, because RWB-TE-001 SU-08 puts the
  handler registry there and the P3 registry calls it; P4 never depends on P3 (TE001 SPEC-022 (d); GAP-36;
  the latent P1 ↔ P3 risk is GAP-51).

**SPEC-RWB-E1-043-026 PARAMETER branch (D-RUN-10).** `ParameterLoadBranch` (`casewf.refdata.internal`)
calls only RWB-E1-042's published `casewf.config.api.ParameterLoadHandler` (E42S revision 5 §12.2, §11.2;
same module; AG §3.11):
`load(InputStream csv, validFrom, authorUserId)`, `approve(loadId, approverUserId)`,
`rollback(loadId, reason, userId)`, `find(loadId)`. It maps `ParameterLoadResult` to `ReferenceLoad`
(`loadId` → `id`; 201 on load, also when `repeat = true`; 200 on approve and rollback) and lets the
`ApiProblemException` refusals of E42S §10.2 through unchanged. The bean is obtained through an
`ObjectProvider`; absent (RWB-E1-042 flag off, E42S SPEC-021) → 404 per SPEC-018. The method checks of
SPEC-027 apply to `PARAMETER` as to any table. Behaviour that differs from this story's registry on the
same endpoint (repeat approve → 409 MSG-GEN-004 and repeat rollback → 409 MSG-P3-027 in E42S) is
recorded (GAP-35).

*Access-list keys are out of reach of any reference load (gate finding 122).* Before calling `load`,
`ParameterLoadBranch` reads the `key` column of the CSV (header `key,environment,value`, E42S SPEC-012)
with the reader of SPEC-015. If any key starts with `rwb.refload.`, the whole load is refused: 422
MSG-P1-002 `{source}` = `PARAMETER`, `{date}` = `validFrom`, `{check}` = "key <k> cannot be changed by a
reference load" (the E42S §12.5 refusal pattern), `field` = `key`; `ParameterLoadHandler.load` is not
called; one REFUSED audit event. A file the branch cannot read is passed to `load`, which refuses it (E42S
X5). Because no load can carry these keys, no PARAMETER approval or rollback can change them (seeded
catalog rows have no `loadId`, E42S E6), and the `PARAMETER` approver list cannot widen itself. The lists
change only by a catalog-file change in a pull request reviewed by the catalog owner and a named reviewer,
with the matching row in that story's migration (E42S flow step 1; AG §8), until RWB-E1-037 delivers a
governed path with its own approver (A-39; GAP-41; open item). SEC-15 tests it.

**SPEC-RWB-E1-043-027 Rights per table (fail closed).** `ReferenceLoadAuthority` (`casewf.refdata.internal`,
bean name `referenceLoadAuthority`), used by every method check:
- Area right: RWB-E1-042's `access.api.CapabilityCheck` for area "Reference data" and the right named in the
  annotation (C load, A approve, U rollback). This story adds the Reference data rows to RWB-E1-042's
  interim grants file `backend/src/main/resources/access/interim-capability-grants.csv` (E42S §12.10): the Reference data column of Users,
  Roles and Permissions v4, which agrees with the PS6 permission seed (RW-COE and RW-REFADM CRUD; RW-LEGAL,
  RW-AGENCYMG, RW-DATASTEW, RW-COMPLY RU; R for the other seeded roles, for example RW-TEAMMGR and
  RW-CASEOWN; no A), plus `A` for every approver role a v7 story names: RW-RISK (S7 §10 "Assumed"),
  RW-COE (E42S CLAR-013 default, parameter owner), RW-DATASTEW (S7-001 flow step 9), RW-TEAMMGR (S7-019
  flow step 4), RW-COMPLY and RW-SECADM (S7-037 line 46). This story adds all six, so no later story edits
  the grants file before RWB-E1-037 replaces it (A-08; finding 126). Area A alone approves nothing: the
  table right below decides. RWB-E1-037 replaces the
  implementation (E42S §12.10). No role literal in Java (AG §3.2; AUD A-03).
- RW-DATASTEW (finding 134; GAP-46): Story v7 RWB-E1-001 §10 and RWB-E1-064 §10 give it Reference data U,
  and URP4 line 102 and PS6 give it RU, while S7 §10 and API4 approve need A. The higher-precedence
  source for this operation is the story file v7 of this story (S7 §10: the approver holds A), which
  API4 repeats, so approval needs A and RW-DATASTEW approves only through the interim A row of A-08.
  That row is an assumption, not a source grant; RWB-E1-037 decides the matrix (open item).
- Table right: the caller's role authorities must intersect the CODE_LIST parameter
  `rwb.refload.loader.<code>` (load, rollback) or `rwb.refload.approver.<code>` (approve), read through
  `ParameterService` (pattern of S7-037 §13 `rwb.refload.approver.*`; G-R03). Defaults (SPEC-029):
  loader `RW-REFADM` for the 12 tables and `RW-COE,RW-REFADM` for `PARAMETER` (E42S PRE-4); approver
  `RW-RISK` for the 12 tables and `RW-COE,RW-RISK` for `PARAMETER` (S7 §10; E42S CLAR-013). RW-COE gets
  no built-in table until its tables are named by a reviewed catalog change (S7 §10 "tables it owns";
  gate finding 104; SPEC-026; A-31, A-39). A handler code's defaults are set by its owning story
  (SPEC-025). A missing key or empty value refuses.
- For approve and rollback, the table is resolved from `loadId` (SPEC-030); an unknown `loadId` passes
  the table right so that the controller returns 404, but still needs the area right.
- A refusal returns `false`, so the existing handler answers 403 MSG-P4-002, and records one audit event
  first (SPEC-028).

**SPEC-RWB-E1-043-028 Admin-action and refusal audit.** `ReferenceLoadAudit` (port in `casewf.refdata.internal`) with one interim
adapter `LoggingReferenceLoadAudit` writes one structured line `event=REFERENCE_LOAD_AUDIT` per load,
approve and rollback, both done and refused (BS-4.4; REQ FR-RWB-012; TC7 TC-E1-043-11 "the refusal is
logged"; G-R07). Fields: `operation` (LOAD, APPROVE, ROLLBACK), `table`, `loadId` (absent for a refused
load), `area` = Reference data, `right`, `outcome` (DONE, REFUSED), `messageCode`, `traceId`, and `changes`
(the handler's `changeSummary` items, SPEC-025, SPEC-031). No user ID,
row content or reason text (BS-4.6; A-30; same practice as E42S SPEC-019; the inventory v4 classes
DF-REF-166/167 author and approver as staff identifiers, personal). Refusals are recorded in
`ReferenceLoadAuthority` (SPEC-027) and in the controller for 4xx business refusals. RWB-E1-039 (order
28) replaces the adapter with the access log and its AC-DENY entry (seam). Until then a refused attempt
cannot be attributed to an actor from this story's records; only `traceId` links it to its request.
Backend context v2.0 (line 138) says structured logs carry the user ID, while BS-4.6 and the inventory v4
treat staff IDs as personal: recorded as GAP-42 with an open item for the DPO (finding 129).

**SPEC-RWB-E1-043-029 Catalog entries through RWB-E1-042's catalog file.** This story adds 38 rows to
`backend/src/main/resources/config/parameter-catalog.csv` in its pull request, reviewed by the catalog
owner (S7-042 flow step 1, §13; E42S §7.1; G-R04), so RWB-E1-042's generator emits the keys
(E42S SPEC-005) and its `CatalogCompletenessCheck` passes (E42S SPEC-003: every row has owner, type and a
default). Rows (all kind BUSINESS, scope GLOBAL, `required=false`, environments DEV,SIT,UAT,PROD,
`secret=false`, `value_source=TABLE`, used_by `recovery.casewf.refdata`):

| Keys | Count | value_type | default | owner_role |
|---|---|---|---|---|
| `refdata.columns.<code>` for the 12 S7 BR1 codes | 12 | STRING | `none` | RW-REFADM |
| `rwb.refload.loader.<code>` for the 12 codes and `parameter` | 13 | CODE_LIST | `RW-REFADM`; `parameter`: `RW-COE,RW-REFADM` | RW-RISK |
| `rwb.refload.approver.<code>` for the 12 codes and `parameter` | 13 | CODE_LIST | `RW-RISK`; `parameter`: `RW-COE,RW-RISK` | RW-RISK |

`required=false` keeps RWB-E1-042 BR7 (required parameters at start-up) green; the defaults fail closed
(no definition → load refused; lists → least access). Owners are assumptions (A-09, A-31). The same rows
go into this story's migration (SPEC-001). The 12 definition values are then loaded through the
PARAMETER branch (SPEC-026) and approved before the first table load; this is how the definitions are
loaded (gate finding 103). The 26 list keys are refused in any PARAMETER load (SPEC-026), so their values
are the catalog defaults (A-39). A handler code's two list keys come with its owning story; its
`refdata.columns.<code>` key is optional (SPEC-025).

**SPEC-RWB-E1-043-030 Dispatch.** `ReferenceLoadDispatcher` (`casewf.refdata.internal`), D-RUN-10 and D-RUN-11:
- Load by `table`: `PARAMETER` → SPEC-026; a code with a registered handler → registry handler path
  (SPEC-025); otherwise → registry built-in path (SPEC-002), which refuses unknown codes with 422
  MSG-P3-027 "table code is not a reference table". The registry decides handler vs built-in; the
  dispatcher only separates `PARAMETER`.
- Approve and rollback by `loadId`: `reference_version.load_id` (through the registry's published
  `find`-style read `versionByLoadId`, A-28) → registry; else `ParameterLoadHandler.find(loadId)` present
  → SPEC-026; else 404 MSG-P4-003. `load_id` values are UUIDs generated by each store, so a collision is
  not handled beyond this order (A-28).

**SPEC-RWB-E1-043-031 Data-dictionary loads: registry part only (D-RCV-29; gate finding 121; RWB-E1-001
gate 2 finding 017; orchestrator rulings of 2026-11-18).** DL10 D-RCV-29 says "Later dictionary changes
are reference loads through RWB-E1-043". RWB-E1-064 (BS6 order 13, after this story) owns the dictionary:
its v7 story loads table code `sys_fields` through `POST /admin/reference-loads` and its approve call
(S7-064 §3, §4 steps 2-3) and publishes `DataDictionaryLoader` (S7-064 §12). Under D-RUN-08 and D-RUN-11
the dependency runs the other way from S7-064 §12 ("called by the reference data service"): RWB-E1-064
registers a `ReferenceTableHandler` for `sys_fields` that adapts its own loader, and this story never
calls P1 code (GAP-40). This story publishes the registry and runs its generic checks, and nothing more
for the dictionary:
- Route, version log and maker-checker: a `sys_fields` load is a handler-code load (SPEC-025) with an
  immutable `reference_version` (SPEC-001, 007), approval by a non-author whose role is in
  `rwb.refload.approver.sys_fields` (SPEC-008, 027), and the lists fail closed: until RWB-E1-064 seeds its
  two keys every `sys_fields` load and approval is refused.
- Audit: the handler's `changeSummary` items are written in the LOAD, APPROVE and ROLLBACK audit events
  (SPEC-028), field IDs only, never a value. Built and tested with a synthetic handler (TC-HD-04).
- This story never writes `sys_objects` or `sys_fields` (AG §3.11) and holds no dictionary rule.

*Stated requirement on RWB-E1-064 (seam; protective, so it applies unless RW-COMPLY rules otherwise).*
S7-064 §11 lists DF-REF-105 `sys_fields.is_personal` as Read, and RW-COMPLY "Owns which fields are
personal through the data dictionary (DL26)" (TE011 §10). So the `sys_fields` handler must: (a) in
`validate`, refuse a file whose `is_personal` value for an existing field differs from the value in
force, 422 MSG-P1-002 `{check}` = "is_personal cannot be changed by a load" (S7-064 X3 uses MSG-P1-002);
(b) never write `is_personal` in `apply` or `onRolledBack`, so a rollback cannot restore an earlier mark;
(c) set `rwb.refload.approver.sys_fields` to RW-COMPLY, which is inferred from TE011 §10 ("Owns which
fields are personal") and not named by any source as the dictionary approver (A-36). Story v7 RWB-E1-069
line 203 and DL10 name a data architect as an approver, but URP4 has no role code for one, so no role is
named for it and no code is invented (finding 135; GAP-47). Which governed path
may change a mark is an open item owned by RW-COMPLY (TE011 §10; DL26). All in `shared-updates.md`.

*RWB-TE-011.* Its lint covers committed SQL, fixtures and logs only; it is not a runtime check and is
asked for nothing by this story (GAP-38).

**SPEC-RWB-E1-043-032 Effective date and version independence (finding 132; G3-R01).** Sources: S7 BR3
(version in force = APPROVED with the latest `valid_from` ≤ business date), BR8, §9 row 4; S7-019 BR3 ("takes
effect on its valid from date after approval"), AC2, AC9 (version 3 approved with valid from 2026-12-15 is
used from that date, version 2 before it); DD8 DF-REF-163/164 (`valid_from`; `valid_to` set when the next
version is approved). Decision Log v10 has no further rule. Rules:
1. Approval writes a new APPROVED version effective from its `validFrom` and never changes the rows of
   the version in force or of any other version (trigger, SPEC-001; SPEC-008, 010).
2. Every read selects by business date (SPEC-011), so nothing a reader gets changes before `validFrom`;
   the cache is keyed by business date and evicted on approval (SPEC-013).
3. Versions are independent: a version with an earlier `validFrom` may be approved after a later one;
   `valid_to` of each is recomputed (SPEC-010; A-18) and each date reads the right version.
4. Rollback withdraws only the latest approved version (greatest `valid_from`), in force or not yet in
   force; a later approved version → 409 MSG-P3-027; no earlier version → 409 MSG-P3-015 (SPEC-024;
   GAP-52).
5. Handler codes follow the same rules through the handler contract (SPEC-025 *Effective date*; A-42).
Tests TC-TM-01..04.

## Field-level behaviour matrix

| Field (DF ID, S7 §11) | Source | Rule | Error |
|---|---|---|---|
| `table` → `table_code` (DF-REF-160) | request | SPEC-030, 002, 025; ≤ 30 chars (PS6) | 422 MSG-P3-027; missing → MSG-GEN-001 |
| `validFrom` → `valid_from` (DF-REF-163) | request | ISO date ≥ business date | 422 MSG-P3-027; missing → MSG-GEN-001 |
| `file` → rows | request | ≥ 1 data row; each row passes the column definition (and handler) | 422 MSG-GEN-001 / MSG-P3-027 |
| `reason` → `rollback_reason` | request (rollback) | non-blank, ≤ 400 | 422 MSG-GEN-001 |
| `version_no` (DF-REF-161) | computed | max + 1 per table | — |
| `status` (DF-REF-165) | computed | VALIDATED, APPROVED, ROLLED_BACK | — |
| `author_user_id` (DF-REF-166) | actor ID (A-07) | A-07 | 401 if absent |
| `approver_user_id` (DF-REF-167) | actor ID (A-07) | ≠ author; DB CHECK | 409 MSG-P7-002 |
| `approved_at` (DF-REF-168) | clock | set on approve | — |
| `valid_to` (DF-REF-164) | computed | SPEC-010, SPEC-024 | — |
| `row_count` (DF-REF-169) | computed | data rows written | — |
| `content_hash` (DF-REF-170) | computed | SPEC-006, char(64) | — |
| `load_id` (DF-REF-171) | registry | new UUID per load | — |
| `updated_by` / `updated_at` | actor ID / clock | set on approve and rollback | — |
| `reference_row.row_key` (DF-REF-183) | computed | key columns, unique per version | 422 MSG-P3-027 |
| `reference_row.row_data` (DF-REF-184) | file | jsonb of typed values | — |

## Status-transition matrix

| From | Event | Condition | To | SPEC |
|---|---|---|---|---|
| none | load | all checks pass, no identical load | VALIDATED | 007 |
| none | load | any check fails | not written | 002-006, 025 |
| none | load | identical load exists | unchanged (existing returned, 201; or 409 with a handler's repeat message) | 006, 025 |
| VALIDATED | approve | approver ≠ author, rights per table, `validFrom` ≥ business date, no APPROVED twin | APPROVED (in force from `validFrom`) | 008, 027, 032 |
| VALIDATED | approve | author or no approver | VALIDATED (409) | 008 |
| APPROVED | approve | any | APPROVED (200, no change) | 008 |
| APPROVED | rollback | latest APPROVED of the table (in force or not yet), earlier APPROVED exists, rights, reason | ROLLED_BACK; earlier version in force | 024, 032 |
| APPROVED | rollback | a later APPROVED version exists | APPROVED (409 MSG-P3-027) | 024 |
| APPROVED | rollback | no earlier APPROVED version | APPROVED (409 MSG-P3-015) | 024 |
| ROLLED_BACK | rollback | any | ROLLED_BACK (200, no change) | 024 |
| ROLLED_BACK | approve | any | ROLLED_BACK (409) | 008 |
| VALIDATED | rollback | any | VALIDATED (409) | 024 |

No case status changes (S7 §9).

## Exceptional-case behaviour

| Case | Behaviour | HTTP / message |
|---|---|---|
| Rule code or HOLIDAY as `table` | refused | 422 MSG-P3-027 |
| `data_product` before RWB-E1-001 registers its handler | refused as unknown code | 422 MSG-P3-027 |
| Two VALIDATED loads with the same `valid_from`; second approved | refused (partial unique index) | 409 MSG-P3-027 (A-16) |
| Approve after the business date passed `valid_from` | refused; author reloads | 409 MSG-P3-027 (A-17) |
| Parallel identical loads | one written, other returns it | 201 (A-15) |
| Handler `apply` fails on approval | approval rolled back | handler's problem, else 409 MSG-GEN-004 |
| Database unavailable / business date unavailable | no write | 503 (A-22, A-01) |
| Column definition missing (`none`) for a built-in code | refused | 422 MSG-P3-027 |
| Handler code without a column definition | handler `validate` is the only structure check | handler's message ID, 422 |
| `PARAMETER` load with an `rwb.refload.*` key | refused, `ParameterLoadHandler` not called | 422 MSG-P1-002 |
| Handler `validate` throws a non-API exception | defect, nothing written | 500 with `traceId` |
| Loader or approver key missing for a code | refused | 403 MSG-P4-002 |
| Branch flag off | operation absent | 404 MSG-P4-003 (SPEC-018; not in API4, GAP-48) |
| Load with no `table` | refused before any table right | 422 MSG-GEN-001 `table` (finding 136) |
| Repeat after the business date passed `validFrom` | same answer as before the date | 201 existing body, or 409 with a handler's repeat message (finding 133) |
| Future-dated version approved | stored; served from `validFrom`; earlier dates unchanged | 200 (SPEC-032) |
| Decision recorder fails on approve | approval rolled back | 503 MSG-P7-003 |

## API change assessment

| Operation | API4 | Delta | Notes |
|---|---|---|---|
| `POST /admin/reference-loads` | exists (P4, Reference data C) | none | Dispatch by table (SPEC-030). API4 checklist fields and MSG-P3-022 are RWB-E2-041 (S7 §19); `table`/`validFrom` not `required` (GAP-16) |
| `POST /admin/reference-loads/{loadId}/approve` | exists (P4, A) | none | API4 "Check the approver role for the load's table" (SPEC-027); AC-VERS through the seam (SPEC-008) |
| `POST /admin/reference-loads/{loadId}/rollback` | exists (P4, U, `RollbackRequest`) | none | Built here (SPEC-024; D-RUN-10) |
| `GET /admin/lists/{listCode}` | exists (P4, R) | not built | GAP-34 |
| `POST /admin/reference-loads/{loadId}/verify` | exists (U) | not built | GAP-11 |

Contract tests against API4 for the three operations (CTX testing §3 "API story"). 400 is not used:
API4 and S7 §12 list 422 for validation (GAP-28). API4 tags the operations P4; the code is in P3
`casewf.refdata` (TE001 SU-08; GAP-53). API4 lists no 404 for the load or 500 for any of the three; this
spec answers 404 when a branch flag is off and 500 for a handler defect (GAP-48; request to the API owner).

## Seed ownership (orchestrator note)

| Rows | Owner | Evidence |
|---|---|---|
| `parameter_catalog` bootstrap rows and values (incl. `refdata.cache.ttl-seconds`) | RWB-E1-042 | E42S §12.4 |
| `parameter_catalog` 38 rows of SPEC-029 | RWB-E1-043 (catalog file + this migration) | E42S line 106, CLAR-003 |
| `lov_value` LOV-REF-TABLE and other LOVs, `role`, `permission` | RWB-E1-001 (V0001 per PS6 header and DL10 D-RCV-28) | PS6 lines 5125-5149 |
| `reference_version` / `reference_row` | none by migration: loaded through the endpoint | S7 §13 "Configuration and reference data" |
| Content of the 12 tables and their column definitions | the table's story: DELEGATION_LIMIT RWB-E1-038; ROLE/TEAM/QUEUE RWB-E1-019; PRODUCT_PARAMETER and SERVICE_LEVEL RWB-E1-045; DOCUMENT_TYPE RWB-E1-025; TEMPLATE RWB-E1-046; LEGAL_PERIOD Legal (RWB-E1-028 reads it); PRODUCT, REGION, EXPOSURE_BAND none named (GAP-43) | S7 §19; S7-028 lines 41, 46; story files v7 of those stories |
| `parameter_catalog` rows for a handler code (`rwb.refload.loader/approver.<code>`) | the owning story (catalog file + its migration) | SPEC-025 |

## A-06 split (flags and parameters as config literals)

| Item | This story | Stays with |
|---|---|---|
| Cache TTL | `refdata.cache.ttl-seconds` through `ParameterService` (SPEC-013) | — |
| Column definitions, loader and approver lists | catalog keys and values (SPEC-027, SPEC-029) | content: table owners |
| Business values of the 12 tables | versioned rows (SPEC-001..011) | content: owning stories |
| Flag `rwb.p3.refdata-versions` | existing config-property pattern (SPEC-018) | flag table: RWB-E1-047 (BS6 order 16) |

## NFR applicability (REQ-RWB-002 v2.0)

| NFR | Applies | Reason |
|---|---|---|
| NFR-RWB-001 Availability | No new target | Service inherits the platform's availability; the cache keeps reads working for one TTL when the database is slow |
| NFR-RWB-002 Performance | No target to test | No source gives a target for reference reads; reads are served from the cache (SPEC-013) |
| NFR-RWB-003 Throughput | N/A | Loads are rare admin actions; no volume target in S7 |
| NFR-RWB-004 Recovery | Inherited | Data is in the `recovery` schema under the platform backup; no story-level target |
| NFR-RWB-005 Security | Yes | SPEC-015, 016, 024, 027, 028; security tests below |
| NFR-RWB-006 Privacy | Yes | SPEC-014, 023, 028 |
| NFR-RWB-007 Accessibility | N/A | No screen (S7 §15) |
| NFR-RWB-008 Observability | Yes | SPEC-012, 014, 028 |
| NFR-RWB-009 Operability | Yes | SPEC-018 |
| NFR-RWB-010 Retention | Partly | Versions and rows are never deleted (trigger, SPEC-001); no retention class for reference data exists in the sources, so no purge is built |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | S7 §15 | No screen; no frontend consumer | N/A |
| Backend | YES | REQUIRED | 80% lines, statements, branches, functions on new and changed recovery classes (BS-7.2; CTX testing §1) | SPEC-001..032 | New services, controller, dispatcher, authority, audit, recorder, checks, hasher | One test per AC1-AC10 and TC-E1-043-11; one per BR1-BR9; each exception row; each security test SEC-01..SEC-17; TC-TM-01..04, TC-RP-01, TC-FD-01, TC-DR-01, TC-BD-01; contract test per operation; migration tests (empty schema, PS6 baseline, re-run, constraint and trigger negatives, lint); integration tests under `@Tag("recovery-it")` |

## Test scenarios

| Test | Covers | Level | Synthetic data |
|---|---|---|---|
| TC-E1-043-01 | AC1, BR2, BR3, BR8 | IT | EXPOSURE_BAND v3 (4 rows, 2026-11-30), v4 (5 rows, 2026-12-01) |
| TC-E1-043-02 | AC2, BR4 | IT + API | DELEGATION_LIMIT 24 rows; author approves |
| TC-E1-043-03 | AC3, BR7 | IT | Two consumers `case-service` and `allocation-engine` share one cache; each reads QUEUE v7 and SERVICE_LEVEL v2; assert exactly one line per consumer per table naming the reader, and none on a second read in the TTL window; a new line after expiry; no identifier in any line; `v_ace_holiday` not read through this service |
| TC-E1-043-04 | AC4, BR5 | IT + API | SERVICE_LEVEL, row 12 `limit_days` = "five" and row 15 missing a key; `{check}` names row 12, `detail` lists both |
| TC-E1-043-05 | AC5, BR3, BR4 | IT | LEGAL_PERIOD v1 approved, v2 VALIDATED 2026-12-01 |
| TC-E1-043-06 | AC6, BR6 | API | LEGAL_PERIOD validFrom 2026-11-24, fixed business date 2026-11-25 |
| TC-E1-043-07 | AC7 | IT + API | REGION same file twice |
| TC-E1-043-08 | AC8 | IT | QUEUE v8, two parallel approvals |
| TC-E1-043-09 | AC9, BR9 | IT | TEAM with no approved version: exception, ERROR line, counter |
| TC-E1-043-10 | AC10, BR5 | API | DOCUMENT_TYPE header only |
| TC-E1-043-11 | Access | API | RW-CASEOWN load → 403 MSG-P4-002; nothing written; one REFUSED audit event (TC7 wording) |
| TC-RB-01 | SPEC-024 | IT + API | REGION v1, v2 approved; rollback v2 with reason → 200 ROLLED_BACK; v1 served; v1 `valid_to` NULL; `updated_by`, reason stored; cache evicted |
| TC-RB-02 | SPEC-024 | API | rollback v1 with no earlier → 409 MSG-P3-015; repeat rollback → 200 same body; VALIDATED → 409; not latest → 409; blank reason → 422 MSG-GEN-001 |
| TC-HD-01 | SPEC-025, 030 | IT | Test handler for synthetic code `test_table` with two failures (file level, then row 3) using fixture message IDs registered in the test message catalog: 422 with the first failure's message ID, placeholders and `field`, `detail` listing both in order, never MSG-P3-027; approve calls `apply` once in the transaction; `apply` throwing `ApiProblemException` leaves VALIDATED and returns its own message; rollback calls `onRolledBack`; handler without rollback → 409 |
| TC-HD-02 | SPEC-025 | Unit | Two handlers for one code, or one for `PARAMETER` → start-up fails |
| TC-HD-03 | SPEC-025, D-RUN-11 | API | `data_product` with no handler → 422 "table code is not a reference table". With a test handler for `data_product`, its two list keys and **no** `refdata.columns.data_product`: a valid file → 201; a file with an empty owner → 422 with the handler's MSG-P1-003 as `messageCode`; the same valid file twice → 409 MSG-P1-011, nothing written (not refused by design) |
| TC-HD-04 | SPEC-031 | IT | Synthetic handler `test_dictionary` whose `changeSummary` returns `DF-TST-001 owner_role`: the item appears in the LOAD, APPROVE and ROLLBACK audit events and no value appears; a `validate` refusal with a fixture message passes through; approval by a role outside `rwb.refload.approver.test_dictionary` → 403; no approver key → 403; rollback by one holder of U on the loader list restores the earlier version and calls `onRolledBack` |
| TC-HD-05 | SPEC-025 | IT | Handler without definition or `keyColumns`: `row_key` = row numbers; handler with `keyColumns` and a repeated key that `validate` let through → 422 MSG-P3-027 "row key repeated"; `validate` throwing a non-API exception → 500, nothing written; built-in code QUEUE with a definition and a test handler: a type failure answers MSG-P3-027 before `validate` runs |
| TC-PB-01 | SPEC-026, 030 | IT | Test double of `ParameterLoadHandler`: PARAMETER load → 201; approve and rollback of a PARAMETER `loadId` routed to it; its `ApiProblemException` passed through; bean absent → 404 |
| TC-FL-01 | SPEC-018 | IT | Flag off: read beans present, `enabled()` false; registry branch 404; with `rwb.p3.configservice` on, PARAMETER branch still served |
| TC-MG-01 | SPEC-001 | IT | Empty schema and PS6 baseline give one end state; UPDATE of `reference_row`, DELETE of `reference_version`, UPDATE of `created_by`/`is_active` refused; CHECK approver ≠ author; rolled back without reason refused |
| TC-BR1 | BR1, SPEC-002 | API | ALLOCATION and HOLIDAY as `table` → 422 |
| TC-TM-01 | SPEC-032, 025 (finding 132) | IT | REGION v1 in force; v2 approved with `validFrom` 2026-12-15 on business date 2026-12-01: reads for 2026-12-14 return v1, for 2026-12-15 return v2; v1 rows unchanged; a dated test handler's store holds v2 keyed by 2026-12-15 and its read for 2026-12-14 still returns v1 content |
| TC-TM-02 | SPEC-032, 010 | IT | REGION v2 (`validFrom` 2026-12-20) approved, then v3 (`validFrom` 2026-12-10) approved: 2026-12-05 → v1, 2026-12-12 → v3 (`valid_to` 2026-12-19), 2026-12-21 → v2; no row of v2 changed; test handler's v2 rows unchanged |
| TC-TM-03 | SPEC-024, 032 | IT + API | v2 approved, not yet in force: rollback → 200 ROLLED_BACK; v1 stays in force for every date; v1 `valid_to` NULL; test handler `onRolledBack` removes only v2 |
| TC-TM-04 | SPEC-024, 032 | IT + API | v3 in force (S7-019 AC2 shape): rollback → v2 in force from the next read; with v4 approved for a later date, rollback of v3 → 409 MSG-P3-027 "only the latest approved version"; only v1 → 409 MSG-P3-015 |
| TC-RP-01 | SPEC-006, 025 L9 (finding 133) | API | Test handler for `data_product` with `repeatMessage`; file loaded with `validFrom` 2026-11-30; business date moved to 2026-12-02; same file again → 409 MSG-P1-011, not 422 MSG-P3-027; built-in REGION same case → 201 existing body |
| TC-FD-01 | SPEC-015, 025 L3 (finding 136) | API | RW-REFADM load with no `table` → 422 MSG-GEN-001 `field` = `table`, no REFUSED audit; RW-CASEOWN with no `table` → 403 (area right L2) |
| TC-DR-01 | SPEC-008 | IT | `ReferenceDecisionRecorder` test double throws → 503 MSG-P7-003; version stays VALIDATED; handler `apply` rolled back; the interim line carries no user ID |
| TC-BD-01 | SPEC-019 (finding 131) | Unit | `ModulithTest.verify()` passes with `refdata.api` published; `RecoveryBoundaryTest` rule: no class in `recovery.access..` or `recovery.integration..` depends on `recovery.casewf..`; a fixture class in `access` that imports `casewf.refdata.api` fails the rule |
| TC-CAT-01 | SPEC-029 | Unit | `CatalogCompletenessCheck` passes with the 38 rows; migration catalog rows equal the CSV rows; every `rwb.refload.*` row is CODE_LIST with owner RW-RISK |

Security tests (gate finding 110; security-quality-standards "unauthorized, unauthenticated and
privilege-escalation"; testing-standards §3):

| Test | Endpoint | Case | Expected |
|---|---|---|---|
| SEC-01 | all | Reflection: every handler method of `ReferenceLoadController` has `@PreAuthorize` naming 'Reference data' and C, A or U; a fixture controller without it is reported by the same check | Check passes for the controller, fails for the fixture |
| SEC-02, -03, -04 | load, approve, rollback | No token | 401 MSG-P4-001 |
| SEC-05 | load | RW-CASEOWN (R only) | 403 MSG-P4-002, nothing written, one REFUSED audit event without user ID |
| SEC-06 | load | RW-COE on REGION (C, not in loader list) | 403, nothing written, audit |
| SEC-07 | approve | RW-REFADM (C, no A) | 403, stays VALIDATED, audit |
| SEC-08 | approve | RW-COE (A from grants) on REGION (not in approver list) | 403, audit |
| SEC-09 | rollback | RW-CASEOWN | 403, audit |
| SEC-10 | rollback | RW-LEGAL (U, not in loader list) | 403, audit |
| SEC-11 | load | RW-RISK (R) with `table=PARAMETER` | 403, audit |
| SEC-12 | approve | author holding A approves own load | 409 MSG-P7-002 |
| SEC-13 | approve, rollback | unknown `loadId` with the right | 404 MSG-P4-003 |
| SEC-14 | load, approve | business date provider fails | 503 MSG-P3-027; cache never holds a VALIDATED or ROLLED_BACK version (unit) |
| SEC-15 | load (PARAMETER) | RW-COE loads a file with row `rwb.refload.approver.region,SIT,RW-COE`; a second file with `rwb.refload.approver.parameter` | 422 MSG-P1-002 each; the `ParameterLoadHandler` test double gets no call; lists unchanged; REFUSED audit (finding 122) |
| SEC-16 | load | token with a non-UUID `sub` and a UUID `oid`; token with neither a UUID | author = `oid`; 401 MSG-P4-001 (finding 127) |
| SEC-17 | approve | RW-DATASTEW (interim A) approves a test-handler load whose approver list holds RW-DATASTEW; RW-DATASTEW approves a REGION load | 200; 403 with audit (finding 126) |

TC7 TC-E1-043-03 and -05 use HOLIDAY fixtures; S7 AC3/AC5 govern (GAP-03). 400 is not tested (GAP-28).

## Guardrails and out of scope

Guardrails: S7 §17 applies in full (SPEC-001, 013, 014, 019, 021, 023). Out of scope: S7 §19; the
lines in §"Requirement lines built by another story"; `/verify` and `GET /admin/lists` (GAP-11,
GAP-34); the real business-date, capability, decision-log and access-log implementations (seams).

## Owner acceptance needed before planning (gate findings 116, 130)

These assumptions change behaviour and need explicit owner acceptance at the plan gate. None has been
accepted: A-01 (business date rule; ACE batch owner); A-07 (actor ID claim; RWB-E1-022 owner); A-08
(interim A grants for six roles; Risk, access owner); A-09 and A-34 (definition keys and grammar; tech
lead, RWB-E1-042 owner); A-16 and A-17 (extra approve refusals not in S7 §12 or API4; BA, Risk); A-27
(rollback rules, single person; BA); A-31 (default loader and approver lists; access owner, Risk); A-33
(narrow trigger exemption; tech lead); A-37 and A-38 (handler contract: optional definition, `row_key`, repeat
message; tech lead, RWB-E1-001 and RWB-E1-019 owners); A-39 (access lists out of reach of loads; access
owner, Risk); A-40 (`data_product` list defaults; RWB-E1-001 owner); A-41 (LOV read through a new P4
interface; P4 owner, tech lead); A-42 (handler effective-date contract; tech lead, RWB-E1-001, RWB-E1-019
and RWB-E1-064 owners).

AI-orchestrator rulings this spec relies on, which need human ratification (not ratified; open item for
the engagement lead in `shared-updates.md`): D-RUN-08 (later-story work as seams, including the
`sys_fields` handler of RWB-E1-064); D-RUN-10 (this story owns the shared endpoint and the PARAMETER
branch; GAP-24 Blocker = No; rollback built here instead of RWB-E1-019 build step 5, GAP-10); D-RUN-11
(handler registry; GAP-31, GAP-36); D-RUN-12 (one creating migration per table, used in the RWB-E1-001
note); and the orchestrator rulings of 2026-11-18 (gate triage, the dictionary split of GAP-38, closing
finding 122 by design) and the round-3 triage of 2026-11-18 (placement, effective-date default,
Lows fixed under D-RUN-09). Human owners: the engagement lead, with the tech lead and the RWB-E1-001,
RWB-E1-019 and RWB-E1-064 owners.

## Clarification Log

No question is put to the user (L-RCV-03; RUN-BRIEF). Each item is answered from a source, a run
decision (BLOG) or a labelled assumption; owners' confirmations go to `shared-updates.md`.

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | S7 §13; PS6 `uk_reference_row` | Row-key uniqueness global or per version? | AC1 | S7 governs (GAP-01); RWB-E1-001 told (GAP-25) | RESOLVED | 001 |
| CLAR-002 | S7 BR1; PS6 LOV-REF-TABLE | Rule codes and HOLIDAY in the seeded list | Forbidden loads | Refused: no column definition (GAP-04) | RESOLVED | 002 |
| CLAR-003 | S7 §13 step 2; S7-042 §13 | Where column definitions live and how they enter the catalog | Row check | Catalog file + generator + this migration (A-09, A-34; G-R04) | RESOLVED_BY_ASSUMPTION | 003, 029 |
| CLAR-004 | S7 BR6 | valid_from = business date | AC6 boundary | Accepted (A-05) | RESOLVED_BY_ASSUMPTION | 005 |
| CLAR-005 | S7 §12; OI-E1-042-011 | Repeat-load status code | Contract | 201 same body (A-06) | RESOLVED_BY_ASSUMPTION | 006 |
| CLAR-006 | S7 §3; S7-069 | Business date source | BR6 check | RWB-E1-042 provider; rule handed to the view's reader (A-01) | RESOLVED_BY_ASSUMPTION | 017 |
| CLAR-007 | S7 §10; API4 approve; S7-019; S7-042 | Who holds A, per table | Approve | Area right through grants file + per-table lists (A-08, A-31; G-R03) | RESOLVED_BY_ASSUMPTION | 027 |
| CLAR-008 | S7 §9; FR-RWB-011; API4 `/rollback`; S7-019 §13 | Rollback owner | ROLLED_BACK | Built here (D-RUN-10 owns the endpoint; gate finding 101) | RESOLVED | 024 |
| CLAR-009 | S7 AC3/AC9, §13 step 6; BS6 | Engines built later | Hook calls | Reader-bound service and exception delivered; engines are seams (A-02) | RESOLVED_BY_ASSUMPTION | 012, 014 |
| CLAR-010 | S7 BR6 vs approve | Approve after valid_from passed | Retroactive version | Refuse (A-17) | RESOLVED_BY_ASSUMPTION | 008 |
| CLAR-011 | S7 §14; MSG4 | MSG-P3-027 wording | Text | MSG4 governs (GAP-05) | RESOLVED | 020 |
| CLAR-012 | S7-001, -019, -025 §12; E01S finding 003 | Handler interface for other modules' codes | Later stories | D-RUN-11 registry; full contract (check order, optional definition, message pass-through, repeat message) in SPEC-025 (A-37, A-38; GAP-39, GAP-44) | RESOLVED_BY_ASSUMPTION | 025 |
| CLAR-013 | S7-042 §12; S7 §13 step 7; E42S §11.2 | Shared endpoint ownership and dispatch | Load path | D-RUN-10: this story owns it; PARAMETER branch calls `ParameterLoadHandler` (GAP-24) | RESOLVED | 026, 030 |
| CLAR-014 | S7 §10 RW-COE | Which tables RW-COE owns | Load right | Fail closed: none until named by data (A-31) | RESOLVED_BY_ASSUMPTION | 027 |
| CLAR-015 | TC7 TC-11; BS-4.4; FR-RWB-012 | Refusal and admin-action logging | Audit | Interim log sink; RWB-E1-039 seam (A-30) | RESOLVED_BY_ASSUMPTION | 028 |
| CLAR-016 | DL10 D-RCV-29; S7-064 §3, §11, §12; TE011 §10, §12; orchestrator rulings 2026-11-18 | Dictionary changes and the `is_personal` mark through loads | PDPA control | Registry and generic checks here (SPEC-031); `sys_fields` handler and runtime protection of `is_personal` are RWB-E1-064's (seam, open item RW-COMPLY); TE-011 lint is not a runtime check (GAP-37, GAP-38, GAP-40) | RESOLVED_BY_ASSUMPTION | 025, 028, 031 |
| CLAR-017 | S7-037 BR3, line 46; E42S CLAR-013; gate finding 122 | Who may change the per-table loader and approver lists | Self-granting | No load may carry `rwb.refload.*` keys; change by reviewed catalog change until RWB-E1-037 (A-39; GAP-41) | RESOLVED_BY_ASSUMPTION | 026, 027, 029 |
| CLAR-018 | `SecurityConfig`; `infra/mock-oidc/config.json`; gate finding 127 | Which token claim is the user ID | 401 risk in SIT | `oid` if a UUID, else `sub` if a UUID, through a seam RWB-E1-022 replaces (A-07) | RESOLVED_BY_ASSUMPTION | 015, 016, 024 |
| CLAR-019 | S7 §12, §13; S7 §11, §17; TE001 SPEC-022 (d), SU-08; E42S rev 5 §12.2, §12.7; gate finding 131 | Which module holds the endpoints, the SPI and the LOV read, and how AC-VERS is recorded | Module cycle | All story code in P3 `casewf.refdata`; LOV read through `access.api`; local recorder port (A-41, A-43, A-44; GAP-50, GAP-51, GAP-53) | RESOLVED_BY_ASSUMPTION | 002, 008, 018, 019 |
| CLAR-020 | S7 BR3, §9; S7-019 BR3, AC2, AC9; DD8; gate finding 132 | When an approved future-dated version takes effect, out-of-order approval, which version can be rolled back | Early change of values in force | SPEC-032; handler contract (A-42; GAP-45, GAP-52) | RESOLVED_BY_ASSUMPTION | 024, 025, 032 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0] [ASSUMPTIONS: 44] [GAPS: 53, BLOCKERS: 0]` (open items for owners go to `shared-updates.md`; none blocks this story)

## Status reporting

MCP_STATUS_SUMMARY: Not applicable: no Figma, Jira or Confluence MCP is connected (RUN-BRIEF) and the story has no screen.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend reference-data service with the shared load, approve and rollback endpoints already in API Specification v4, all in P3 `casewf.refdata`; one P4 published interface for the LOV read; no screen; two-module plan-gate decision.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first implementation of API4 load, approve and rollback; no OpenAPI delta]
REQUIREMENT_COVERAGE_SUMMARY: 49 requirement rows mapped, built and tested here; 16 requirement lines assigned to other stories or open owners (not counted as covered); 35 source conflicts recorded, each settled by precedence, an AI-orchestrator run ruling (D-RUN-07..12, awaiting human ratification) or a labelled assumption.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 49] [COVERED_RULES: 49] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 35]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
