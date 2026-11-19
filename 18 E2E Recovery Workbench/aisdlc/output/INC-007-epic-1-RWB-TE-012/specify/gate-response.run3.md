# Gate response — RWB-TE-012 spec gate round 1

| Field | Value |
|---|---|
| Review answered | `review/spec-gate-review.md` (round 1: FAIL, 0 Critical, 1 High, 5 Medium, 5 Low; one review-level gap) |
| Triage | Orchestrator (Claude Code): held the story until RWB-TE-001 v4 passed its spec gate (`AI-SDLC-BUILD-LOG.md`, 2026-11-17T23:48:15), then released remediation run 1 (2026-11-18T00:39:15). No human acceptance is recorded or claimed |
| Re-issued | `spec.md` v2 and the other specify files; every changed file backed up as `*.run1.*` |
| Re-review | `review/spec-gate-review-2.md` |

## Round 1 findings

| Finding | Severity | Fix | Where |
|---|---|---|---|
| SG-01 Module placement | High | All code in `dochub.api` (published) and `dochub.storage` (TE-001 client package). Precondition "RWB-TE-001 merged"; header corrected. Evolution map: relocated `DocumentStore` → `DocumentStorage`, `BlobDocumentStore` → `BlobStorageAdapter` (renamed in place, not duplicated), nested `Config`/`BlobProperties` → `DocumentContainersConfig`/`DocumentStorageProperties` (`rwb.dochub`, P5's own record). No `RecoveryProperties`; `rwb.environment` no longer read. Boundary tests "pass under the RWB-TE-001 module map"; T-TE001-14 list updated; SPEC-024 tests carried. DGAP-18 withdrawn with the TE-001 citation | spec.md header, Baseline, Evolution map, SPEC-006, -008, -016, -017, -022; T-TE012-14, -16; DGAP-18 |
| SG-02 Contract fit with E1-024 | Medium | Request renamed `BlobWriteRequest`; `StoreRequest`/`StoredDocument`/`DocumentStore` left to E1-024. `store()` copies from an intake `BlobRef` (E1-024 steps 1 and 7). One `BlobRef(container, blobName)` used by E1-024, -041, -049; `BlobRef.fromStorageRef` with validation and a round-trip test | SPEC-010, -011, -019; field matrices; T-TE012-03, -04; DGAP-19; open item |
| SG-03 Health aggregate and anonymous reads | Medium | Flag off → `UNKNOWN` with `ready=false`/`FLAG_OFF`: root unchanged, HTTP 200 (sources: story §13 for "not ready", AGENTS.md §3.13 for the previous path). Flag on: `UP`/`DOWN` (root 503 when not ready, story §4 step 3, AC9). A health read makes no storage call; evaluation only on start (background), inside `store()` when not READY, and on `ContainerNotFound`. The "every read" claim is removed; no cache is added because no source or NFR asks for one | SPEC-009, -020; status matrix; T-TE012-08, -09; DGAP-21; ASM-TE012-08, -20, -24 |
| SG-04 Local stack and `.env` | Medium | Both `.env.example` lines renamed; `docker-compose.yml:135` changed; `dev.ps1` `Initialize-EnvFile` appends missing keys from `.env.example` (upgrade path); `README.md:25` corrected by the Builder; local-profile startup test; all listed as impacted nodes | SPEC-021; Change Scope; T-TE012-13; Builder evidence; shared-updates §5; ASM-TE012-22 |
| SG-05 Coverage gate | Medium | RWB-TE-001 v4 SPEC-020 applied: LINE, INSTRUCTION, BRANCH, METHOD at 80%, bundle, no exclusion, `test` data only, outside `check`. Command `./gradlew test recoveryCoverageVerification`. Baseline reaches the gate through RWB-TE-001 (precondition). This story: every `dochub` class ≥ 80% on the four counters and no bundle drop; tests named | SPEC-023; Unit Test Applicability; ASM-TE012-25 |
| SG-06 Unit tests | Medium | Added: routing, both refusals, `open()` allow-list, metadata, source check (T-04, -07); `DocumentAuditLog` (T-10); `LocalEmulatorBootstrap` (T-11); integration-client cases success, timeout, retry inside timeout, unexpected code, malformed response (T-12); timeout-then-retry same-hash (T-05). Azurite `recovery-it` tests required as merge evidence via `./scripts/dev.ps1 it`, with `--skipApiVersionCheck` | SPEC-018; ASM-TE012-23 |
| SG-07 Status line, run log, New Nodes | Low | `Status: SUCCESS` line; "New Nodes Required: YES"; run log and compliance-validation corrected: the orchestrator ran round 1; this run spawns round 2 as instructed | spec.md; agent-run-log.md; compliance-validation.md |
| SG-08 FR/NFR/CTL rows | Low | One row each for FR-RWB-007, REQ-DCM-003, REQ-DCM-002, NFR-029, NFR-053, CTL-12, CTL-09 | Coverage table; shared-updates §1 |
| SG-09 SCR-44 owner | Low | No owner story exists in Build Sequence v6; recorded as DGAP-20 with an open item | SPEC-019; DGAP-20; frontend contract |
| SG-10 Read path ownership | Low | Guardrail: `open()` is not an authorization point; callers own the Documents R and scope check and the PII access-log entry (E1-024 step 8, §17; E1-039) | SPEC-015; Guardrails; shared-updates §7 |
| SG-11 Emulator guard | Low | Guard needs `rwb.dochub.storage.emulator=true` (only in `application-local.yaml`, no env placeholder) plus the three connection-string checks; `rwb.environment` dropped. README decision row is a plan-gate item citing the "Local versus target" Blob row | SPEC-017; shared-updates §5; ASM-TE012-11 |
| TE012-SG-DG-01 | Review gap | Recorded as DGAP-19, Blocker = No (D-RCV-31 settles ownership; signature fitted to E1-024) | document-gaps.md; SPEC-010 |

## Review inputs (section 5) taken up

| Input | Action |
|---|---|
| 1. Azurite `--skipApiVersionCheck` | In SPEC-018 integration tests |
| 2. DGAP-03 early | SPEC-003: early DEV spike; open item "Needed by" moved to TE-012 build |
| 3. Timeout then COPY_PENDING | Exceptional cases; SPEC-012; T-TE012-05 |
| 4. Open item for the E1-024 contract | shared-updates §3 |

## Round 2 (2026-11-18): answers to `review/spec-gate-review-2.md`

Round 2 result: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 4]`. Under D-RUN-09 every finding is fixed in this run (remediation run 2). Backups: `*.run2.md` and `contracts/backend-apis.run2.json`.

| Finding | Fix in spec v3 | Where |
|---|---|---|
| SG-12 (Medium) E1-017 archive container | RWB-E1-017 (17) added to consumers; seam row "not delivered"; DGAP-22 (Blocker = No: D-RCV-35 retires SY-DATALOAD, TE-012 story defines four containers); open item to the solution architect with Compliance, needed by E1-017 specify; coverage row; CONTRADICTIONS: 1 | Header, coverage table, SPEC-019, CLAR-018, `document-gaps.md`, `shared-updates.md` §2, §3, §7 |
| SG-13 (Medium) D-RCV-31 re-store source and docVersion | `source` rule: intake, or standard container only with `writeOnce=true` and the same `{caseId}/{documentId}/v{docVersion}` name; other containers refused. "New docVersion" replaced by the same docVersion (D-RCV-31 settles it, so no gap). RWB-E1-054 (70) named beside RWB-E1-032. Tests added to T-TE012-04 | Field matrix, exceptional cases, SPEC-010, -011, -019, CLAR-019, ASM-TE012-21, `contracts/backend-apis.json` |
| SG-14 (Low) emulator property claim | Claim removed; the `local` profile (`Environment.acceptsProfiles`) is now a required condition; T-TE012-02 tests all five conditions | Properties table, SPEC-017, ASM-TE012-11, T-TE012-02 |
| SG-15 (Low) `DocumentContainers` with the flag off | Bean present, no client, accessors throw NOT_READY, `readiness()` FLAG_OFF; in T-TE012-02 and the seam rows | SPEC-008, -006, -016, -019, ASM-TE012-29 |
| SG-16 (Low) Azurite unreachable | Bootstrap logs one WARN, readiness NOT_READY `UNREACHABLE`, no startup failure or delay, re-run inside `store()`; `depends_on` left unchanged so the backend never needs Azurite to start (baseline property, A-04); T-TE012-11 case | SPEC-017, ASM-TE012-28 |
| SG-17 (Low) Bicep parsing | Template changed to ARM JSON with JSON parameter files, read by T-TE012-15 with the existing Jackson; test module and package named; no new tool | ASM-TE012-03, DGAP-09, CLAR-010, T-TE012-15, `shared-updates.md` §3 |
| Review gap TE012-SG2-DG-01 | Recorded as DGAP-22 | `document-gaps.md` |
| Review input 3 (T-TE012-13 unset case) | The property is set explicitly to blank | T-TE012-13 |

Triage of round 2: this stage continued under the orchestrator's (Claude Code) task brief, which allows one more self-run round. No human acceptance is recorded.
