---
run_id: INC-008-epic-1-RWB-E1-043
story: RWB-E1-043
title: Reference data service with versioned tables
stage: specify
agent: Technical Specifier
date: 2026-11-18
revision: 6 (remediation run 5 of REVIEW-RWB-E1-043-SPEC-005, findings 147-150 and G5-R01; Lows fixed under D-RUN-09 as the orchestrator's round-4 stop rule allows; rebased on RWB-TE-001 spec v4 and RWB-E1-042 spec revision 9)
status: SUCCESS_WITH_ASSUMPTIONS
previous: spec.run5.md (revision 5, 2026-11-18, failed spec gate 5 on four Low findings); spec.run4.md (revision 4, 2026-11-18, failed spec gate 4 on one Medium and eight Low findings); spec.run3.md (revision 3, 2026-11-18, failed spec gate 3 on one High, one Medium and five Low findings); spec.run2.md (revision 2); spec.run1.md (revision 1)
supersedes: _v2-baseline/specify/spec.md (historical; RUN_ID INC-009, D-RCV-47 schema basis; kept unchanged)
---

# Technical specification: RWB-E1-043 Reference data service with versioned tables

Every finding of spec gate 1 (`../review/spec-gate-review.md`, 101-119, G-R01..G-R10) and spec gate 2
(`../review/spec-gate-review-2.md`, 120-130, G2-R01..G2-R05), spec gate 3 (`../review/spec-gate-review-3.md`,
131-137, G3-R01..G3-R05), spec gate 4 (`../review/spec-gate-review-4.md`, 138-146, G4-R01..G4-R03), spec gate 5
(`../review/spec-gate-review-5.md`, 147-150, G5-R01), and the orchestrator rulings, are answered in
`gate-response.md` (§1-§4 round 1, §6 round 2, §7 round 3, §8 round 4, §9 round 5). Revisions 1 to 5 are
kept as `spec.run1.md` to `spec.run5.md`. All triage and rulings come from the orchestrator, Claude Code, an AI agent; none is a
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
| PS6 | Physical Schema v6 (16 Nov 2026): `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` (repository copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`); `data_product` lines 815-834 (`uk_data_product UNIQUE (product_code)`, one `valid_from`, no `valid_to`), `sys_fields` lines 919-944 (`uk_sys_fields UNIQUE (field_id)`, no date column), `sys_field_version` (`UNIQUE (field_id, field_version)`, no date column) |
| API4 | API Specification v4.0.0 (16 Nov 2026): `api/recovery-api-v4.yaml` (load 3167, approve 3214, lists 3135, verify 4961, rollback 5004, `RollbackRequest` 9818) |
| MSG4 | Error and Message Standard v4: `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| TC7 | Test Cases v7, TC-E1-043-01..11: `requirement/legacy/09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md` |
| BS6 | Build Sequence Epic 1 and 2 v6: `requirement/legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| PACK | RWB-E1-042 clarification pack (§3.1, §3.7, §6.2, §7 OI-E1-042-001..011): `requirement/legacy/e1-042-migration-and-clarifications/rwb-e1-042-clarification-pack.md` |
| E42S | RWB-E1-042 spec revision 9 (2026-11-18, remediation run 7, applies D-RUN-19; file `spec.md` last written 2026-11-18 05:16:37 +07:00 and read for this revision; its own gate had not passed when read): `aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (§4.3 line 144 `PARAMETER` SPI seam row and line 150 business-date seam; A-51; §12.14 R7-1; §12.12 T-2 line 948, which adds `access.api.CatalogParameterReader` with nested `Value` to T-TE001-14 under D-RUN-19; §10.1 and §12.2 `MessageResolver.english(String messageId, Map<String, String> placeholders)` and `thai(String messageId, Map<String, String> placeholders)`, each returning `String`; §10.2 the form `ApiProblemException(HttpStatus status, String messageId, Map<String, String> placeholders, String field, String detail, Throwable cause)` with accessors `status()`, `messageId()`, `field()`, `detail()`, an optional `detail` rendered in place of the EN text, and its guards; §12.2 `CapabilityCheck.has(Authentication, String area, String right)` and `require(Authentication, String area, String right, String action)`, which throws `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)` (SPEC-RWB-E1-042-020); packages `casewf.config.api` and `access.api`; `ParameterKeys.byName(String key, Class<T> type)`; `ParameterLoadHandler`; §12.4; §12.5 check order; §12.7 `VersionDecisionRecorder` package-private in `casewf.config`, recorder failure 503 MSG-P7-003; §12.10 grants file `access/interim-capability-grants.csv`; §12.12 flag binding; TC-E1-042-05..07, -10, -11, -16..-20, -23 and TC-45 (T-TE001-14 extended); SPEC-RWB-E1-042-005/-012/-017/-019/-020/-021/-022/-023/-025/-026; CLAR-013) and its `shared-updates.md` rows at lines 25, 26, 32, 39 and 83. Revision 4 of this spec used its revision 5 and revision 5 used its revision 7 (kept as `spec.run6.md`, file 2026-11-18 04:58:18); every name used here is unchanged in revision 9 (findings 144, 148) |
| TE001 | RWB-TE-001 spec v4 (INC-002, passed its spec gate; owns the module map): `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` SPEC-RWB-TE-001-004 (e), -022 (d), -023, -025 (public types of each published package) and test T-TE001-14 (line 279); `shared-updates.md` SU-02, SU-08 (INC-008 row), SU-14 |
| DD8 | Logical Data Model and Data Dictionary v8: `requirement/legacy/06-data/recovery-workbench-logical-data-model-and-data-dictionary-v8-xlsx.md` (DF-REF-033, DF-REF-071 `product_code` UK, DF-REF-079, DF-REF-163, DF-REF-164; DF-WRK-038, DF-WRK-051, DF-WRK-052) |
| URP4 | Users, Roles and Permissions v4: `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` (role list; line 102 RW-DATASTEW Reference data RU) |
| E01S | RWB-E1-001 spec revision 2 (INC-009): `aisdlc/output/INC-009-epic-1-RWB-E1-001/specify/spec.md` (SPEC-RWB-E1-001-013..017, ASM-E1001-05, -12, -15, -19) and its gate reviews: round 1 findings 003, 004; round 2 (`review/spec-gate-review-2.md`) findings 014, 016, 017 |
| BLOG | `AI-SDLC-BUILD-LOG.md` §1, orchestrator decisions D-RUN-07 (23:26), D-RUN-08 (23:26), D-RUN-09 (23:41), D-RUN-10 (23:47), D-RUN-11 (23:49), D-RUN-12 (23:49), all 2026-11-17; gate triage of 2026-11-18 00:31 (run 2), 00:58 (run 3) and 04:55 (run 4); D-RUN-18 (2026-11-18 04:55, decisions table line 41: the reference-load handler SPI is published by P4 `access.api`; ratification by the recovery tech lead is an open item); D-RUN-19 (2026-11-18 05:10, line 42: parameter reads outside P3 through `access.api`, used here only for the T-TE001-14 set) |
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
| Impacted Existing Nodes | `application.yaml` (key `rwb.p3.refdata-versions`, SPEC-018; no `RecoveryFlags` or `RecoveryProperties` change, TE001 SPEC-023); `backend/src/test/resources/architecture/recovery-modules.yaml` (casewf `published` list gains `refdata.api`, TE001 SU-08; SPEC-019); `RecoveryBoundaryTest` (SPEC-019); RWB-TE-001 test T-TE001-14 (changed: its expected sets are extended in this merge request, never relaxed; SPEC-019, finding 139); RWB-E1-042 resources `config/parameter-catalog.csv` (38 rows added, SPEC-029) and `access/interim-capability-grants.csv` (Reference data rows, SPEC-027; E42S §12.10). No change to `ApiExceptionHandler`, `ProblemFactory` (`access.internal`) or `ApiProblemException` (`access.api`) beyond what RWB-E1-042 delivers (E42S §12.2; TE001 SU-08). |
| New Nodes Required | P3 `recovery.casewf.refdata.api` (published as `@NamedInterface(name = "refdata.api", propagate = false)`, TE001 SU-08): `ReferenceVersionRegistry`, `ReferenceDataService`, `ReferenceDataReaders`, `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException`. P3 `recovery.casewf.refdata.internal` (not published): registry and service implementations, `ReferenceTableHandlers` (handler map), `ReferenceRowCache`, `ReaderLogGate`, `ReferenceVersionLogger`, `ReferenceTableColumns`, `ReferenceRowCheck`, `ContentHasher`, entities and repositories, `RefdataSettings` (package-private module record, TE001 SPEC-023), `ReferenceDecisionRecorder` (package-private port) and `LoggingReferenceDecisionRecorder`, and the HTTP side: `ReferenceLoadController`, `ReferenceLoadDispatcher`, `ParameterLoadBranch`, `ActorIdResolver` (seam, A-07), `ReferenceLoadFileReader`, `ReferenceLoadAuthority`, `ReferenceLoadAudit` (port) and `LoggingReferenceLoadAudit` (TE001 SU-08: "Put the controller in the P3 refdata package"). P4 additions: `recovery.access.api.ListOfValuesReader` and its interim implementation `recovery.access.internal.LovValueReader`, named by S7 §11 and §17 ("through the P4 published interface"; SPEC-002; A-41); and the reference-load handler SPI `recovery.access.api.ReferenceTableHandler` (with its nested enum `Dating`), `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport` and `RowCheckFailure`, published by P4 under D-RUN-18 as S7-001 §12 says (SPEC-025; types only, no P4 implementation). Migration `V<seq>__rwb_e1_043_reference_versions.sql`. |
| Inherited Existing Behavior | Recovery Flyway bean, `${recoverySchema}`, lint (AUD A-04); JWT resource server, `/api/recovery/**` RW- role gate, 401 MSG-P4-001, principal claim `sub` (`SecurityConfig`); `ApiExceptionHandler` (`AccessDeniedException` → 403 MSG-P4-002, `NoResourceFoundException` → 404 MSG-P4-003); Modulith verify (RWB-TE-001). From RWB-E1-042 (order 3, E42S revision 9 §10.2, §12.2; names unchanged since revision 7): P3 `casewf.config.api` `ParameterService`, generated `ParameterKeys`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider`; P4 `access.api` `MessageResolver`, `CapabilityCheck`, `ApiProblemException` with its status-and-message-ID form (optional `detail`), `ApiError`. RWB-E1-042's `VersionDecisionRecorder` is package-private in `casewf.config` and is not used here (E42S §12.7; GAP-50). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
| Module scope (for the plan gate) | All story code is in P3 `casewf.refdata` (TE001 SU-08). P4 gets the LOV read interface and its interim reader (S7 §11, §17), the handler SPI types (D-RUN-18; S7-001 §12) and the Reference data rows of the grants file; no `platform` change. This story adds P3 → P4 edges only; later P1 handlers depend on P4 and never on P3 (SPEC-019; D-RUN-18). AGENTS §7 still sends a plan that touches two modules back to the analyst; the plan gate must take that decision (gate finding 118). |

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
| P2 | RWB-E1-042 done: `refdata.cache.ttl-seconds` (300, DL11) and the list of reference table codes | E42S revision 9 publishes `ParameterService`, `ParameterLoadHandler` (`casewf.config.api`) and `CapabilityCheck`, `MessageResolver`, `ApiProblemException` (`access.api`) (E42S §12.2); code not yet merged | Build after RWB-E1-042 merges (A-14, A-25). Table codes are this story's (E42S CLAR-022; SPEC-002) |
| P3 | LOV-REF-TABLE loaded with the 12 codes, no rule code | PS6 seeds 25 codes incl. 5 rule codes and HOLIDAY; `lov_value` is an RWB-E1-001 V0001 table present locally through the PS6 load (GAP-04, GAP-32) | SPEC-002 refuses any built-in code without a column definition |
| P4 | P4 load endpoint deployed | No endpoint code exists | Built here in P3 `casewf.refdata.internal` (TE001 SU-08; GAP-53): S7 §13 step 7; D-RUN-10 (SPEC-015, 016, 024) |
| P5 | Loader holds Reference data C; approver holds A (assumed RW-RISK) | PS6 and Users, Roles and Permissions v4: no role holds Reference data A (E42S §12.10) | SPEC-027, A-08, GAP-14, GAP-22 |
| P6 | Business date from the ACE batch record (`v_ace_batch_status`) | The view is RWB-E1-069's (BS6 order 10, S7-069 line 230); RWB-E1-042 publishes `BusinessDateProvider` with an interim implementation (E42S SPEC-023) | SPEC-017 uses the provider; replacing it is a seam (A-01, GAP-12); its P3 → P1 read is allowed under D-RUN-18 (GAP-51) |

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
| S7 BR3, BR8, §9 row 4; S7-019 BR3, AC2, AC9; DD8 DF-REF-163/164 (finding 132) | Approval writes a new version effective from `validFrom`, never overwrites the version in force; reads by business date; versions independent (out-of-order approval); rollback of the latest approved version only | 010, 011, 024, 025, 032 | DIRECT | Handler contract: `DATED` handlers keep the same rule; `CURRENT_STATE` handlers are approved and applied only on `validFrom` (SPEC-025 *Effective date*, SPEC-032 rule 6; finding 138); TC-TM-01..05 | COVERED |
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
done-when (SIT)" moved to the next table (gate finding 123). Revision 4 adds the effective-date row (finding 132); revision 5 extends it to current-state handlers (finding 138).

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
| Business date | RWB-E1-042 `casewf.config.api.BusinessDateProvider` (interim Asia/Bangkok date, E42S SPEC-023) | Reader of `v_ace_batch_status` after RWB-E1-069 (A-01); it may call P1 (a P3 → P1 read), which D-RUN-18 allows because P1 never depends on P3 (E42S §4.3; GAP-51) |
| Message text | RWB-E1-042 `access.api.MessageResolver` (PACK §6.2, OI-E1-042-004) | Message table (GAP-06) |
| LOV-REF-TABLE codes | This story: `access.api.ListOfValuesReader` with the interim `access.internal.LovValueReader` (S7 §11, §17; A-41) | P4 owner, when `lov_value` reads are given a permanent home |
| AC-VERS decision entry | This story: package-private `ReferenceDecisionRecorder` port in `casewf.refdata.internal` with an interim log adapter (SPEC-008; A-43). RWB-E1-042's `VersionDecisionRecorder` is not published (E42S §12.7; GAP-50) | RWB-E1-027 replaces both adapters with a call to P7 `DecisionLogWriter` (E42S §12.7) |
| Admin-action and refusal audit | This story: `ReferenceLoadAudit` port, logging adapter (SPEC-028) | RWB-E1-039 (AC-DENY on 403) |
| Handlers for other modules' codes | This story: `access.api.ReferenceTableHandler` SPI (published by P4, D-RUN-18) and its contract (SPEC-025) | RWB-E1-001 (`data_product`), RWB-E1-064 (`sys_fields`), RWB-E1-019 (QUEUE, QUEUE_MEMBER), RWB-E1-025 (DOCUMENT_TYPE), others |
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
findings 133, 140): (1) **early repeat, only for a handler code that supplies a repeat message**: after the
file is read and has rows and **before** the valid-from check, a version with the same `(table_code,
valid_from, content_hash)` exists and the handler's `repeatMessage(file)` is present → 409 with that
message, nothing written (SPEC-025 L9; A-38), so RWB-E1-001 AC10 holds for any business date (S7-001
AC10); (2) for every other code the story order holds (S7 §13 build step 3 and flow step 3: the validity
checks, then the hash and the idempotent return): after the valid-from check (SPEC-005), a version with the
same `(table_code, valid_from, content_hash)` → return it unchanged, write nothing, 201 with the same body,
any status (S7 X4, AC7; A-06), so an identical file whose `validFrom` has passed is refused 422 as S7 X3
and AC6 expect; (3) then an APPROVED version of the table with this `valid_from` → 409 MSG-P3-027
`{check}` = "an approved version already has this valid from" (S7 §12). The departure from the story
order in (1) is recorded as GAP-56.

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
→ 409 MSG-P3-027 (partial unique index; A-16); for a handler code whose handler declares
`Dating.CURRENT_STATE` (SPEC-025), `validFrom` > business date → 409 MSG-P3-027 `{check}` = "it can be
approved only on its valid from date <validFrom>", nothing written, status stays VALIDATED, `apply` not
called (SPEC-032 rule 6; finding 138). Success, in one transaction: status APPROVED,
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
RWB-E1-042 binds its own flag only by `@ConditionalOnProperty` (E42S §12.12). Binding (findings 131, 143; A-44): only the controller and the dispatcher are conditional, both with
`@ConditionalOnExpression("${rwb.p3.refdata-versions:false} or ${rwb.p3.configservice:false}")`. Every
other bean of this story is registered whatever the flag: the registry, `ReferenceTableHandlers` (built
from `List<ReferenceTableHandler>`, empty when no handler bean exists), `LoggingReferenceDecisionRecorder`,
`ReferenceDataService`, `ReferenceDataReaders`, `ReferenceLoadAuthority`, `LoggingReferenceLoadAudit` and
`ParameterLoadBranch` (which takes `ObjectProvider<ParameterLoadHandler>`, SPEC-026). Behaviour is gated by
`RefdataSettings`, a package-private record in `casewf.refdata.internal` bound to prefix `rwb.p3`
(`refdataVersions`, default `false`): `ReferenceDataReaders.enabled()` returns it and the registry's write
methods refuse when it is off. No bean of this story is missing in any flag combination, so the context
starts with the flag off and the previous code path stays (AG §3.13; TC-FL-01).
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

**SPEC-RWB-E1-043-019 Module boundary and dependency direction (findings 131, 139, 141; D-RUN-18).** The module map is
RWB-TE-001 v4's (TE001 SPEC-022 (d): P3 `casewf` depends on P2 `integration` and P4 `access`; neither may
depend on `casewf`; every module that uses `ApiError` or `ApiProblemException` depends on P4, so P4 may depend
on none of them; `ModulithTest` rejects a cycle, D-RCV-11). All code of this story is in P3 `casewf.refdata`;
its published package is `casewf.refdata.api`, declared `@NamedInterface(name = "refdata.api", propagate =
false)` and added to the casewf `published` list of `recovery-modules.yaml` in the same merge request (TE001
SU-08; SPEC-004 (e): no public type directly in a module base package). Under D-RUN-18 (orchestrator run
decision, 2026-11-18 04:55; ratification by the recovery tech lead is an open item, R24) the reference-load
handler SPI is published by P4 in `access.api`, as S7-001 §12 line 222 says ("published interface of P4 that
P1 implements"); the registry stays in P3 and collects the handler beans by that P4 type. Every edge this
story adds:

| From | To | Types | Module edge | Allowed by |
|---|---|---|---|---|
| `casewf.refdata.internal` | `access.api` | `CapabilityCheck`, `MessageResolver`, `ApiProblemException`, `ApiError`, `ListOfValuesReader`, `ReferenceTableHandler`, `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport`, `RowCheckFailure` | P3 → P4 | TE001 SPEC-022 (d) (same direction as `casewf.admin` → `access.api`) |
| `casewf.refdata.internal` | `casewf.config.api` | `ParameterService`, `ParameterKeys`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider` | inside P3 | E42S §12.2 |
| `casewf.refdata.internal` | `casewf.refdata.api` | own published types | inside P3 | — |
| `access.internal.LovValueReader` | `access.api` | `ListOfValuesReader` | inside P4 | — |

The SPI types refer only to JDK types and to each other; no P4 type refers to a `casewf` or `dataengine`
type. Edges that later stories add, and why none closes a cycle:

| From | To | Story (BS6 order) | Allowed by |
|---|---|---|---|
| P1 `dataengine` handlers (`data_product`, `sys_fields`) | P4 `access.api` (SPI, `ApiProblemException`) | RWB-E1-001 (9), RWB-E1-064 (13) | D-RUN-18; TE001 SPEC-022 (d) |
| P3 handlers (QUEUE, QUEUE_MEMBER) | P4 `access.api` | RWB-E1-019 (25) | TE001 SPEC-022 (d) |
| P3 readers | P1 published reads: S7-028 flow step 3 ("through the P1 interface"); S7 §12 line 270 (the working-day calculator reads `v_ace_holiday` "through the P1 query of RWB-E1-028"); the business-date reader of E42S §4.3 | RWB-E1-028 (47); the business-date story after RWB-E1-069 (10) | D-RUN-18 |
| P1 | P3 | none: forbidden; a P1 handler imports nothing from `casewf..` | D-RUN-18 |

The edges run P3 → P1, P3 → P2, P3 → P4 and P1 → P4; nothing points into P3 from another module and P4
points to neither P1 nor P3, so the graph has no cycle (GAP-51 settled for the build by D-RUN-18).
`RecoveryBoundaryTest` gains three rules: (1) no class outside `recovery.casewf.refdata` references
`ReferenceVersionEntity`, `ReferenceRowEntity` or their repositories, and no native SQL outside it names
`reference_version`/`reference_row` (S7 §13 done-when; AG §3.11); (2) no class in `recovery.access..` or
`recovery.integration..` depends on `recovery.casewf..`; (3) no class in `recovery.dataengine..` depends on
`recovery.casewf..` (D-RUN-18). `ModulithTest.verify()` stays green.

*RWB-TE-001 test T-TE001-14 (changed test, findings 139, 148).* T-TE001-14 pins the public types of every
published package and the `casewf` named interfaces (TE001 SPEC-025; T-TE001-14, line 279). This story
extends its expected sets in the same merge request and relaxes no assertion. The rule: each set is the
set RWB-E1-042's merge leaves, plus exactly this story's additions; nothing else changes. After RWB-E1-042
(order 3; E42S revision 9 TC-45 and §12.12 T-2) and this story (order 8) the expected sets are:
- `access.api`: RWB-E1-042's merged set, which at its revision 9 is `ApiError`, `ApiProblemException`
  (TE001 SPEC-025), `MessageResolver`, `CapabilityCheck` and `CatalogParameterReader` with its nested
  record `CatalogParameterReader.Value` (E42S; D-RUN-19); plus this story's `ListOfValuesReader`,
  `ReferenceTableHandler` (with nested `Dating`), `ReferenceLoadFile`, `HandlerMessage`,
  `ValidationReport` and `RowCheckFailure` (D-RUN-18). If RWB-E1-042 merges with a different set, this
  story adds the same six types to that set.
- `casewf` named interfaces: `api`, `config.api` (E42S), `refdata.api` (this story), `rules`, `timers`,
  `workflow`.
- `casewf.refdata.api` public types: `ReferenceVersionRegistry`, `ReferenceDataService`,
  `ReferenceDataReaders`, `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException`.
- Every other published package (including `casewf.config.api`): as TE001 SPEC-025 and E42S leave it.

RWB-E1-042 merges first (BS6 order 3), so this story edits the sets as RWB-E1-042 leaves them; the
coordination is row R29 of `shared-updates.md`. The PARAMETER branch calls only RWB-E1-042's published
`ParameterLoadHandler` and never reads `parameter_value` (AG §3.11; D-RUN-10) (A-24).

**SPEC-RWB-E1-043-020 Messages.** Story messages are raised as RWB-E1-042's `access.api.ApiProblemException` in
its form `ApiProblemException(HttpStatus status, String messageId, Map<String, String> placeholders, String
field, String detail, Throwable cause)` (E42S revision 9 §10.2; findings 144, 148). `detail` is set only for the
multi-failure text of SPEC-003 and SPEC-025 L13, which this story caps at 100 entries with the total; it is
null otherwise, and `messageId` is never null here. `access.internal.ApiExceptionHandler` renders the
Problem, taking the text from `access.api.MessageResolver.english(messageId, placeholders)` and
`thai(messageId, placeholders)` (E42S §10.1, §12.2; interim seam per PACK §6.2 and OI-E1-042-004; GAP-06).
This story never calls `ProblemFactory`. The 403 uses the `ApiError` form (SPEC-027). MSG-P3-027 uses MSG4's wording "The version in force is unchanged"
(GAP-05). MSG-P4-003's case wording is kept for an unknown load (GAP-27).

| ID | HTTP | `{placeholders}` | Used by |
|---|---|---|---|
| MSG-P3-027 | 422 / 409 / 503 | `table`, `check` | SPEC-002, 003, 005, 006, 008, 012, 017, 024, 032 |
| MSG-GEN-001 | 422 | `field` (`rows`, `validFrom`, `file`, `table`, `reason`) | SPEC-004, 005, 015, 024 |
| MSG-P7-002 | 409 | — | SPEC-008 |
| MSG-P7-003 | 503 | — | SPEC-008 (decision recorder failure; MSG4 line 208; E42S §12.7) |
| MSG-GEN-004 | 409 | — | SPEC-007, 009, 024 |
| MSG-P3-015 | 409 | `table` | SPEC-024 (MSG4: "There is no earlier version of {table} to return to.") |
| MSG-P4-001/002/003 | 401/403/404 | `action` for P4-002: "load reference data", "approve reference data", "roll back reference data" (SPEC-027; A-45) | SPEC-015, 016, 024, 027 (existing `ApiError`) |

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
with the same `valid_from` follows SPEC-006: while `validFrom` is not before the business date it returns
the ROLLED_BACK load with 201 (SPEC-006 rule (2)); for a handler code with a repeat message it answers 409
with that message (rule (1), for example MSG-P1-011 for `data_product`); once `validFrom` has passed,
any other code is refused 422 MSG-P3-027 at L10. A new `valid_from` is needed to load it again (A-27;
finding 150). `PARAMETER` rollbacks go to RWB-E1-042 (SPEC-026). Rule-package rollback is
RWB-E1-073's (D36 line 145; S7 §9). Rollback is a single-person action by a holder of U on the table's
loader list (S7-019 flow step 8 has RW-REFADM call it): it restores a version that a non-author already
approved and is not a new approval, so no second person is needed (A-27; finding 125).

**SPEC-RWB-E1-043-025 Handler registry and its contract for codes other modules own (D-RUN-11, D-RUN-18;
gate findings 120, 138, 140, 141; RWB-E1-001 gate 2 finding 014).** The SPI is published by P4 in
`access.api` (D-RUN-18; S7-001 §12 line 222 "published interface of P4 that P1 implements"); the registry
that collects and calls the handlers stays in P3 `casewf.refdata.internal` (TE001 SU-08). The first three
methods are verbatim from S7-001 §12; the rest are defaults this story adds (A-37, A-38, A-42):

```java
// package th.co.scb.ace.demo.recovery.access.api  (P4, published; D-RUN-18)
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
    enum Dating { DATED, CURRENT_STATE }
    default Dating dating() { return Dating.CURRENT_STATE; }
}
public record ReferenceLoadFile(String tableCode, LocalDate validFrom, List<String> columns,
                                List<Map<String, Object>> rows) {}
public record HandlerMessage(String messageCode, Map<String, String> placeholders) {}
public record RowCheckFailure(int row, String column, String messageCode, Map<String, String> placeholders) {}
public record ValidationReport(List<RowCheckFailure> failures) { public boolean ok() { return failures.isEmpty(); } }
```

`RowCheckFailure.row` is the 1-based data row (header excluded); `0` means the file as a whole.
`column` may be null; it becomes the Problem `field`.

`dating()` declares how the handler's target table holds versions (finding 138; A-42). `DATED`: the table
can hold several versions of a key, each with its own date, so `apply` can store a future version without
changing what is read before `validFrom`. `CURRENT_STATE`: the table holds one row per key with no date
range, so any write changes the values in force at once. The default is `CURRENT_STATE`, the protective
reading: a handler that does not declare its kind is never applied early. `data_product` (PS6
`uk_data_product UNIQUE (product_code)`, one `valid_from`, no `valid_to`; DD8 DF-REF-071 UK, DF-REF-079) and
`sys_fields` (PS6 `uk_sys_fields UNIQUE (field_id)`, no date column) are `CURRENT_STATE` (GAP-54, GAP-55);
`queue_member` (`valid_from`, `valid_to`; DD8 DF-WRK-051/052) can be `DATED`.

*Registration.* Another module registers a handler by publishing a Spring bean of the P4 type
`access.api.ReferenceTableHandler` behind its own feature flag; the handler depends on P4 only, never on P3
(D-RUN-18). `ReferenceTableHandlers` (P3 internal) builds the map `tableCode → handler` at
start-up; a second bean for the same code, or a bean for `PARAMETER`, fails start-up naming both classes.
A handler code needs no LOV-REF-TABLE row (D-RUN-11; GAP-31). The registry decides handler vs built-in;
the dispatcher only separates `PARAMETER` (SPEC-030).

*`PARAMETER` is not an SPI handler (finding 149; GAP-57).* `PARAMETER` stays a dispatcher branch:
`ParameterLoadBranch` (P3, this story's `casewf.refdata.internal`) takes `ObjectProvider<ParameterLoadHandler>`,
answers 404 MSG-P4-003 when no bean exists, and implements no `access.api` type (SPEC-026, SPEC-030;
D-RUN-10). The reasons are in the sources: RWB-E1-042 keeps the version, maker-checker and repeat rules of
`PARAMETER` behind `ParameterLoadHandler` with its own `parameter_value.load_id` (E42S §4.3 line 144,
SPEC-017), while the registry path records its own `reference_version` row and calls `validate` and
`apply`, which would create the second load record that E42S §12.14 R7-1 rules out; and the flag-off
result E42S SPEC-021 and R7-1 require is met by the branch. D-RUN-18's wording ("P3 (RWB-E1-042) handlers
implement it") and E42S A-51 and §4.3 line 144 (a P3 adapter `ParameterLoadBranch` "implements it")
describe the SPI route instead; this spec departs from that wording, records it as GAP-57 and asks
RWB-E1-042 and the orchestrator to align (shared update R32). The departure changes no class name: the
adapter is `ParameterLoadBranch` in both texts. A handler bean for `PARAMETER` therefore still fails
start-up (TC-HD-02).

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
| L9 | Early repeat, **only for a handler code whose `repeatMessage(file)` is present**: a version with the same `(table, validFrom, content_hash)` exists (SPEC-006); runs before L10 so it answers the same for any business date (findings 133, 140; GAP-56) | 409 Problem with that message ID and placeholders, nothing written (A-38) |
| L10 | `validFrom` ≥ business date (SPEC-005) | 422 MSG-P3-027 |
| L11 | For every other code, in the story order (S7 §13 build step 3, flow step 3): a version with the same `(table, validFrom, content_hash)` exists → idempotent return; else an APPROVED version of the table with this `validFrom` (SPEC-006) | repeat: 201 with the existing body, nothing written (A-06); approved twin: 409 MSG-P3-027 |
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
- *Repeat raised by a handler (findings 133, 140).* The repeat of RWB-E1-001 AC10 is decided by L9 through
  `repeatMessage`, before the valid-from check, so it holds for any business date. Only a handler code
  that supplies a repeat message takes this early path. Built-in codes, handler codes without a repeat
  message and `PARAMETER` (RWB-E1-042's own order) keep the S7 §13 order, so an identical file whose
  `validFrom` has passed is refused at L10 (S7 X3, AC6). The early path departs from S7 §13 step 3 for those
  handler codes only (GAP-56; A-38). A handler may also
  return MSG-P1-011 from `validate` for the wider S7-001 X7 case (a file equal to the version in force
  under a different `validFrom`); that refusal is a pass-through 422 at L13, after L10 (GAP-44).
- *Approve.* L1, L2 (A), approver list `rwb.refload.approver.<code>`, flag, unknown `loadId` 404, author
  409 MSG-P7-002, then SPEC-008's checks, the last of which refuses a `CURRENT_STATE` handler's version
  while `validFrom` is after the business date (409 MSG-P3-027). Then one transaction: status APPROVED, `valid_to` (SPEC-010),
  `apply(loadId, file, validFrom)` with the stored rows, `ReferenceDecisionRecorder` AC-VERS (SPEC-008).
  After commit: cache eviction, audit DONE with `changeSummary`.
- *Effective date (findings 132, 138; SPEC-032).* `apply` runs in the approve transaction. What it may do
  depends on `dating()`:
  - `DATED`: the approve transaction may be days before `validFrom`. The handler stores the version keyed
    by `validFrom` and never overwrites or changes a row that a reader gets for a business date before
    `validFrom`; its readers select by business date (S7 BR3; S7-019 BR3 and AC9). Versions are
    independent, so `apply` for an earlier `validFrom` approved after a later one must not change the later
    version's rows. `onRolledBack` follows the same rule. Proved with a dated test handler (TC-TM-01..04).
  - `CURRENT_STATE`: the registry calls `apply` only when `validFrom` is on or before the business date.
    While `validFrom` is later, approval is refused with 409 MSG-P3-027 `{check}` = "it can be approved
    only on its valid from date <validFrom>"; the version stays VALIDATED and `apply` is not called
    (SPEC-008). A-17 also refuses an approval once `validFrom` has passed, so a current-state version is
    approved on its valid-from date and applied at once: `apply` writes the current rows with that date
    (S7-001 flow step 10: "writes the 14 rows in one transaction with the valid from date"). If the
    approver misses the date, the author reloads with a new `validFrom`. Out-of-order approval cannot
    happen, because an earlier `validFrom` has passed by the time a later one is approved and A-17 refuses
    it. Rollback (SPEC-024) withdraws the latest approved version, which is in force, and `onRolledBack`
    writes the restored version's rows at once (S7-019 flow step 8, re-apply). No owner job and no schema
    change is needed. As for every code, a table has at most one APPROVED version per `validFrom` (L11,
    SPEC-008, the partial unique index of SPEC-001), so a same-day correction of a current-state table
    needs a rollback of that day's version first (when the handler supports rollback), after which a
    corrected file with the same `validFrom` can be loaded and approved; otherwise it waits for a later
    `validFrom` (finding 147). Proved with a current-state test handler (TC-TM-05).
  The registry's own `reference_version` and `reference_row` hold every version, dated, for both kinds, so
  `versions()` and the version log are the same for both. Each owning story tests its own handler against
  the kind it declares (shared update).
- *Rollback.* SPEC-024 rules; rule 7 refuses when `supportsRollback()` is false. In the transaction,
  `onRolledBack(rolledBack, restored, restoredFile, restoredValidFrom)` with the restored version's rows.
  Rollback is a single-person action by a U holder on the loader list (A-27).
- Hash and version history stay in this story's tables (E01S ASM-E1001-05).

*What the owning story supplies (and nothing else is needed from it):*
1. The handler bean (type `access.api.ReferenceTableHandler`) behind its own flag, declaring `dating()`
   (`CURRENT_STATE` unless its table holds dated versions; A-42); while it is absent the code is unknown and
   refused with 422 MSG-P3-027 "table code is not a reference table".
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
(GAP-44). `dating()` = `CURRENT_STATE` (the default; PS6 `uk_data_product`; GAP-54): approval on the
valid-from date writes the 14 rows with `data_product.valid_from` = `validFrom` (S7-001 flow step 10). The
handler reads only its own tables and imports nothing from `casewf` (D-RUN-18).

*QUEUE and QUEUE_MEMBER (RWB-E1-019).* Its `ReferenceTableCheck` maps onto `validate` (MSG-P1-002 row and
check, MSG-GEN-002 field, min, max: S7-019 AC4, AC5), its `ReferenceRollbackHandler` onto
`supportsRollback`/`onRolledBack` (G-R01, G-R02; GAP-08, GAP-39). It declares `dating()` (A-42):
`queue_member` has `valid_from` and `valid_to` (DD8 DF-WRK-051/052), so `DATED` fits it; `queue` holds one
row per queue with a `table_version` (DD8 DF-WRK-038), and S7-019 flow step 5 has RWB-E1-019's own
`QueueVersionApplier` apply the version in force to it on the valid-from date (BR3, AC9). If RWB-E1-019
keeps that applier, `DATED` holds for both codes; if not, it declares `CURRENT_STATE`. The choice is
RWB-E1-019's; this story asks for no job (*Effective date*). QUEUE is also a built-in code with a column
definition, so L12 runs first; to keep its own messages leading RWB-E1-019 sets a definition with types
and keys only. QUEUE_MEMBER is a handler code and needs no LOV-REF-TABLE row (D-RUN-11), although
S7-019 line 38 says it "is added to" the list; recorded as GAP-49 with a note to RWB-E1-019.

- `changeSummary` names, without row values or personal data, what a load changes (for example
  `DF-TST-001 owner_role`); the registry adds the items to the version log line and the audit events of
  that load (SPEC-028, SPEC-031; A-35). Default: nothing.
- The SPI lives in P4 `access.api`, as S7-001 §12 says, under D-RUN-18 (finding 141); the registry that
  calls it stays in P3 `casewf.refdata` (TE001 SU-08). P4 defines the types and implements none of them, and
  no P4 type refers to P1 or P3, so P4 still depends on neither; P1 and P3 handlers depend on P4 only
  (SPEC-019; GAP-36 and GAP-51 settled for the build by D-RUN-18, pending tech-lead ratification).

**SPEC-RWB-E1-043-026 PARAMETER branch (D-RUN-10).** `ParameterLoadBranch` (`casewf.refdata.internal`)
calls only RWB-E1-042's published `casewf.config.api.ParameterLoadHandler` (E42S revision 9 §12.2, §11.2;
same module; AG §3.11):
`load(InputStream csv, validFrom, authorUserId)`, `approve(loadId, approverUserId)`,
`rollback(loadId, reason, userId)`, `find(loadId)`. It maps `ParameterLoadResult` to `ReferenceLoad`
(`loadId` → `id`; 201 on load, also when `repeat = true`; 200 on approve and rollback) and lets the
`ApiProblemException` refusals of E42S §10.2 through unchanged. The bean is obtained through an
`ObjectProvider`; absent (RWB-E1-042 flag off, E42S SPEC-021) → 404 per SPEC-018. The method checks of
SPEC-027 apply to `PARAMETER` as to any table. Behaviour that differs from this story's registry on the
same endpoint (repeat approve → 409 MSG-GEN-004 and repeat rollback → 409 MSG-P3-027 in E42S) is
recorded (GAP-35). The PARAMETER cases RWB-E1-042 asks to run through the endpoint (E42S `shared-updates.md`
row 25: its TC-05..07, 10, 11, 16-20, 23) run against the real `ParameterLoadHandler` in TC-PB-02 (finding
145). This branch is not an implementation of the P4 handler SPI (SPEC-025 *`PARAMETER` is not an SPI
handler*; GAP-57).

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
- Area right: RWB-E1-042's `access.api.CapabilityCheck.require(authentication, "Reference data", right,
  action)` with the right named in the annotation (C load, A approve, U rollback) and the operation's
  action: "load reference data", "approve reference data" or "roll back reference data" (A-45; finding
  142; E42S SPEC-020 uses "read parameters" the same way). This story adds the Reference data rows to RWB-E1-042's
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
  and URP4 line 102 and PS6 give it RU, while S7 §10 and API4 approve need A. RUN-BRIEF ranks all v7 story
  files at one level, so precedence does not settle this; the operation owner's story (S7 §10: the
  approver holds A), which API4 repeats, is followed, settled by assumption A-08 (finding 146): approval
  needs A and RW-DATASTEW approves only through the interim A row of A-08.
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
- Refusal (finding 142): the authority records one REFUSED audit event (SPEC-028) and throws
  `new ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)`, the form
  `CapabilityCheck.require` throws (E42S SPEC-020). For the area right it catches the exception `require`
  throws, audits and rethrows it; for the table right it throws the same form itself. Thrown from the
  `@PreAuthorize` expression it is not an `AccessDeniedException`, so `access.internal.ApiExceptionHandler`
  renders 403 MSG-P4-002 with `{action}` filled ("You cannot load reference data here. Your role does not
  include it."), not the "do this" of the shared forbidden branch (`ApiExceptionHandler.forbidden`, code as
  read 2026-11-18). The methods return `true` when the caller holds both rights.

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
registers an `access.api.ReferenceTableHandler` (P4 SPI, D-RUN-18; `dating()` = `CURRENT_STATE`, GAP-55) for
`sys_fields` that adapts its own loader, and this story never
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

**SPEC-RWB-E1-043-032 Effective date and version independence (findings 132, 138; G3-R01, G4-R01, G4-R02).** Sources: S7 BR3
(version in force = APPROVED with the latest `valid_from` ≤ business date), BR8, §9 row 4; S7-019 BR3 ("takes
effect on its valid from date after approval"), AC2, AC9 (version 3 approved with valid from 2026-12-15 is
used from that date, version 2 before it); DD8 DF-REF-163/164 (`valid_from`; `valid_to` set when the next
version is approved); PS6 `data_product` and `sys_fields` (one row per key) and S7-001 flow step 10 (the
handler writes the rows at approval). Decision Log v10 has no further rule. Rules:
1. Approval writes a new APPROVED version effective from its `validFrom` and never changes the rows of
   the version in force or of any other version (trigger, SPEC-001; SPEC-008, 010).
2. Every read selects by business date (SPEC-011), so nothing a reader gets changes before `validFrom`;
   the cache is keyed by business date and evicted on approval (SPEC-013).
3. Versions are independent: a version with an earlier `validFrom` may be approved after a later one;
   `valid_to` of each is recomputed (SPEC-010; A-18) and each date reads the right version.
4. Rollback withdraws only the latest approved version (greatest `valid_from`), in force or not yet in
   force; a later approved version → 409 MSG-P3-027; no earlier version → 409 MSG-P3-015 (SPEC-024;
   GAP-52).
5. A handler code that declares `DATED` follows rules 1-4 through the handler contract (SPEC-025
   *Effective date*; A-42).
6. A handler code that declares `CURRENT_STATE` (the default; `data_product` and `sys_fields`, whose PS6
   tables hold one row per key: GAP-54, GAP-55) is applied only on or after its `validFrom`: approval is
   refused with 409 MSG-P3-027 while `validFrom` is after the business date, so with A-17 it is approved
   and applied on its valid-from date; out-of-order approval cannot occur; rollback re-applies the restored
   version at once; one APPROVED version per `validFrom` holds as for every code, so a same-day
   correction needs a rollback first (SPEC-008, SPEC-024, SPEC-025; finding 147).
Tests TC-TM-01..05.

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
| VALIDATED | approve | approver ≠ author, rights per table, `validFrom` ≥ business date, no APPROVED twin; for a `CURRENT_STATE` handler code also `validFrom` ≤ business date | APPROVED (in force from `validFrom`) | 008, 027, 032 |
| VALIDATED | approve | author or no approver | VALIDATED (409) | 008 |
| VALIDATED | approve | `CURRENT_STATE` handler code, `validFrom` > business date | VALIDATED (409 MSG-P3-027) | 008, 032 |
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
| Repeat after the business date passed `validFrom` | handler code with a repeat message: same answer as before the date; any other code: refused as past-dated (S7 X3, AC6) | 409 with the handler's repeat message (findings 133, 140); otherwise 422 MSG-P3-027 |
| Future-dated version approved | stored; served from `validFrom`; earlier dates unchanged | 200 (SPEC-032) |
| Future-dated version of a `CURRENT_STATE` handler code approved before its date | refused; approve on the valid-from date, or reload with a new `validFrom` once it has passed (A-17) | 409 MSG-P3-027 (SPEC-008; SPEC-032 rule 6) |
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
| Backend | YES | REQUIRED | 80% lines, statements, branches, functions on new and changed recovery classes (BS-7.2; CTX testing §1) | SPEC-001..032 | New services, controller, dispatcher, authority, audit, recorder, checks, hasher | One test per AC1-AC10 and TC-E1-043-11; one per BR1-BR9; each exception row; each security test SEC-01..SEC-17; TC-TM-01..05, TC-RP-01, TC-FD-01, TC-DR-01, TC-BD-01, TC-PB-02, TC-FL-01 (start-up in every flag combination); contract test per operation; migration tests (empty schema, PS6 baseline, re-run, constraint and trigger negatives, lint); integration tests under `@Tag("recovery-it")` |

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
| TC-PB-02 | SPEC-026, 030; E42S `shared-updates.md` row 25 (finding 145) | IT `@Tag("recovery-it")` | Real RWB-E1-042 `ParameterLoadHandler` (`rwb.p3.configservice` on), synthetic users on the PARAMETER lists, every call through the three HTTP endpoints, each with E42S's expected result: TC-E1-042-05 (out of range → 422 MSG-GEN-002), -06 (not INTEGER → 422 MSG-P1-002), -07 (author approves → 409 MSG-P7-002), -10 part (a) (rollback with reason → 200, earlier version in force), -11 (future version in force from its date; `created_by` and `updated_by`), -16 (same content twice → 201 with the same `id`), -17 (different value, approved twin → 409 MSG-P3-027), -18 (blank reason → 422 MSG-GEN-001 `reason`), -19 (no earlier version → 409 MSG-P3-015), -20 (two concurrent approvals → one 200, one 409 MSG-GEN-004), -23 (unknown key, empty file, past `validFrom` → 422 MSG-P1-002, MSG-GEN-001, MSG-P3-027). E42S TC-10 part (b) (forced commit failure) is not an HTTP case and stays in E42S |
| TC-FL-01 | SPEC-018 (finding 143) | IT | The application context starts in each flag combination: both off; only `rwb.p3.configservice` on; only `rwb.p3.refdata-versions` on; both on. Flag off: read beans present, `enabled()` false, `ReferenceTableHandlers` present and empty, registry write methods refuse, registry branch 404; with only `rwb.p3.configservice` on, the PARAMETER branch is served and the registry branch answers 404 |
| TC-MG-01 | SPEC-001 | IT | Empty schema and PS6 baseline give one end state; UPDATE of `reference_row`, DELETE of `reference_version`, UPDATE of `created_by`/`is_active` refused; CHECK approver ≠ author; rolled back without reason refused |
| TC-BR1 | BR1, SPEC-002 | API | ALLOCATION and HOLIDAY as `table` → 422 |
| TC-TM-01 | SPEC-032, 025 (finding 132) | IT | REGION v1 in force; v2 approved with `validFrom` 2026-12-15 on business date 2026-12-01: reads for 2026-12-14 return v1, for 2026-12-15 return v2; v1 rows unchanged; a dated test handler's (`dating()` = `DATED`) store holds v2 keyed by 2026-12-15 and its read for 2026-12-14 still returns v1 content |
| TC-TM-02 | SPEC-032, 010 | IT | REGION v2 (`validFrom` 2026-12-20) approved, then v3 (`validFrom` 2026-12-10) approved: 2026-12-05 → v1, 2026-12-12 → v3 (`valid_to` 2026-12-19), 2026-12-21 → v2; no row of v2 changed; test handler's v2 rows unchanged |
| TC-TM-03 | SPEC-024, 032 | IT + API | v2 approved, not yet in force: rollback → 200 ROLLED_BACK; v1 stays in force for every date; v1 `valid_to` NULL; test handler `onRolledBack` removes only v2 |
| TC-TM-04 | SPEC-024, 032 | IT + API | v3 in force (S7-019 AC2 shape): rollback → v2 in force from the next read; with v4 approved for a later date, rollback of v3 → 409 MSG-P3-027 "only the latest approved version"; only v1 → 409 MSG-P3-015 |
| TC-TM-05 | SPEC-008, 024, 025, 032 rule 6 (findings 138, 147) | IT + API | Current-state test handler for synthetic code `test_current` (default `dating()`, no repeat message, `supportsRollback` true; a test table with one row per key); v1 approved earlier and in force; business date 2026-12-01: (a) v2 loaded with `validFrom` 2026-12-03 and approved on 2026-12-01 → 409 MSG-P3-027 "it can be approved only on its valid from date 2026-12-03", status VALIDATED, `apply` not called, the test table still holds v1's values; (b) business date moved to 2026-12-03, approve v2 → 200 APPROVED, `apply` called once, the test table holds v2's values; (c) business date moved to 2026-12-04, v3 loaded with `validFrom` 2026-12-04 and approved the same day → 200 APPROVED, applied at once, the test table holds v3's values; (d) v4 loaded on 2026-12-04 with `validFrom` 2026-12-05 (VALIDATED), business date moved to 2026-12-06, approve v4 → 409 MSG-P3-027 (A-17), table unchanged; (e) rollback of v3 (the latest approved version) → 200 ROLLED_BACK, `onRolledBack` writes v2's rows at once; (f) a corrected v5 with `validFrom` 2026-12-04 on business date 2026-12-04, loaded while v3 is APPROVED → 409 MSG-P3-027 "an approved version already has this valid from" (one approved version per date) |
| TC-RP-01 | SPEC-006, 025 L9, L11 (findings 133, 140) | API | (a) Test handler for `data_product` with `repeatMessage`; file loaded with `validFrom` 2026-11-30; business date moved to 2026-12-02; same file again → 409 MSG-P1-011, nothing written; (b) built-in REGION, same case → 422 MSG-P3-027 "valid from is before the business date" (S7 X3, AC6), nothing written; (c) REGION, same file again before the date passes → 201 with the existing body (S7 AC7); (d) test handler without `repeatMessage`, same case as (a) → 422 MSG-P3-027 |
| TC-FD-01 | SPEC-015, 025 L3 (finding 136) | API | RW-REFADM load with no `table` → 422 MSG-GEN-001 `field` = `table`, no REFUSED audit; RW-CASEOWN with no `table` → 403 (area right L2) |
| TC-DR-01 | SPEC-008 | IT | `ReferenceDecisionRecorder` test double throws → 503 MSG-P7-003; version stays VALIDATED; handler `apply` rolled back; the interim line carries no user ID |
| TC-BD-01 | SPEC-019 (findings 131, 139, 141) | Unit | `ModulithTest.verify()` passes with `refdata.api` published and the SPI in `access.api`; T-TE001-14 passes with the expected sets of SPEC-019 (RWB-E1-042's merged set plus this story's six `access.api` types) and fails when any other public type is added to `access.api` or `casewf.refdata.api`; `RecoveryBoundaryTest`: no class in `recovery.access..` or `recovery.integration..` depends on `recovery.casewf..`, and no class in `recovery.dataengine..` does; a fixture class in `access` or in `dataengine` that imports `casewf.refdata.api` fails the rule |
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

Every 403 above and in TC-E1-043-11 also asserts `detail` = MSG-P4-002 with `{action}` = the operation's
action: load "load reference data", approve "approve reference data", rollback "roll back reference data"
(for example "You cannot load reference data here. Your role does not include it."), never "do this"
(finding 142; A-45).

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
interface; P4 owner, tech lead); A-42 (handler effective-date contract and the `DATED` / `CURRENT_STATE` declaration with its
protective default; tech lead, data owner, RWB-E1-001, RWB-E1-019 and RWB-E1-064 owners).

AI-orchestrator rulings this spec relies on, which need human ratification (not ratified; open item for
the engagement lead in `shared-updates.md`): D-RUN-08 (later-story work as seams, including the
`sys_fields` handler of RWB-E1-064); D-RUN-10 (this story owns the shared endpoint and the PARAMETER
branch; GAP-24 Blocker = No; rollback built here instead of RWB-E1-019 build step 5, GAP-10); D-RUN-11
(handler registry; GAP-31, GAP-36); D-RUN-12 (one creating migration per table, used in the RWB-E1-001
note); and the orchestrator rulings of 2026-11-18 (gate triage, the dictionary split of GAP-38, closing
finding 122 by design) and the round-3 triage of 2026-11-18 (placement, effective-date default,
Lows fixed under D-RUN-09), the round-4 triage of 2026-11-18 04:55 (current-state handlers refused before
`validFrom`, the early repeat limited to handler codes with a repeat message) and D-RUN-18 (handler SPI
published by P4; recovery tech-lead ratification open, R24). Human owners: the engagement lead, with the tech lead, the data owner and the RWB-E1-001,
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
| CLAR-019 | S7 §12, §13; S7 §11, §17; TE001 SPEC-022 (d), SU-08; E42S rev 7 §12.2, §12.7; gate findings 131, 141; D-RUN-18 | Which module holds the endpoints, the SPI and the LOV read, and how AC-VERS is recorded | Module cycle | All story code in P3 `casewf.refdata`; LOV read and handler SPI in `access.api` (D-RUN-18); local recorder port (A-41, A-43, A-44; GAP-36, GAP-50, GAP-51, GAP-53, GAP-57) | RESOLVED_BY_ASSUMPTION | 002, 008, 018, 019 |
| CLAR-020 | S7 BR3, §9; S7-019 BR3, AC2, AC9; DD8; PS6 `data_product`, `sys_fields`; S7-001 flow step 10; gate findings 132, 138 | When an approved future-dated version takes effect, out-of-order approval, which version can be rolled back | Early change of values in force | SPEC-032; handler contract with `DATED` / `CURRENT_STATE` (A-42; GAP-45, GAP-52, GAP-54, GAP-55) | RESOLVED_BY_ASSUMPTION | 024, 025, 032 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0] [ASSUMPTIONS: 45] [GAPS: 57, BLOCKERS: 0]` (open items for owners go to `shared-updates.md`; none blocks this story)

## Status reporting

MCP_STATUS_SUMMARY: Not applicable: no Figma, Jira or Confluence MCP is connected (RUN-BRIEF) and the story has no screen.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend reference-data service with the shared load, approve and rollback endpoints already in API Specification v4, all in P3 `casewf.refdata`; P4 published types for the LOV read and the handler SPI (D-RUN-18); no screen; two-module plan-gate decision.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first implementation of API4 load, approve and rollback; no OpenAPI delta]
REQUIREMENT_COVERAGE_SUMMARY: 49 requirement rows mapped, built and tested here; 16 requirement lines assigned to other stories or open owners (not counted as covered); 39 source conflicts recorded, each settled by precedence, an AI-orchestrator run ruling (D-RUN-07..12, D-RUN-18 and D-RUN-19, awaiting human ratification) or a labelled assumption.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 49] [COVERED_RULES: 49] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 39]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
