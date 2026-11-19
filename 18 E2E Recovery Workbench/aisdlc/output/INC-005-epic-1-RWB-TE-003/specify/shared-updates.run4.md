# Shared updates proposed — INC-005-epic-1-RWB-TE-003 specify (remediation 3)

This stage did not edit any shared file (`RUN-BRIEF.md` rule 3). The orchestrator applies these rows in order, after the spec gate review-4 passes. If the gate fails, apply only §3.1 (status correction), with "pending spec gate review-4" replaced by the gate result. Remediation 2 adds NEW-TE003-F, amends OPEN-039 (generator options, `apiTooling` location), adds SPEC-022 and the tests T-TE003-34..36, adds the round-2 gap candidates and an audit-owner note for A-07 (D-RUN-15). The remediation-1 text is kept as `shared-updates.run2.md`. Remediation 3 (answers review-3) adds NEW-TE003-G and gap candidate TE003-SG4-DG-01, adds T-TE003-35 to the SPEC-013 row and the Audit and Logging Design v2 source to SPEC-013 and SPEC-022; the remediation-2 text is kept as `shared-updates.run3.md`.

## 1. `aisdlc/docs/open-items.md` — new rows

Proposed IDs follow OPEN-042. The orchestrator renumbers them if another run takes those numbers first; spec references use NEW-TE003-A..G.

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-043 (NEW-TE003-A) | Add `GET /platform/info` and `GET /admin/temporal/health` to the API specification (or retire them). Until then they are on the `outsideSpecification` allow-list in `api/recovery-api-implementation.yaml` (README decision 6), and `PlatformInfo` / `TemporalHealth` stay hand-written in `frontend/src/modules/recovery/api/platform.ts`. | RWB-TE-003, RWB-E1-071 | API owner | Next API Specification issue | INC-005 spec SPEC-001, -007; audit A-11 |
| OPEN-044 (NEW-TE003-B) | Assign a message ID for an unexpected server error (500) in the Error and Message Standard, or rule that a 500 carries none. API Specification v4 declares no 500 and the standard v4 §4 has no generic ID. | RWB-TE-003, all endpoint stories | Message standard owner (BA) | Before the first endpoint story that can return 500 is accepted | INC-005 spec §3.1 A-08; TE003-SG-DG-04 |
| OPEN-045 (NEW-TE003-C) | Name the owner and rule for request binding/validation errors: which status (400 or 422) an operation returns for malformed input when API v4 declares neither (e.g. `getCasesCaseidTimers`), and the message-table rows for MSG-GEN-001..003 with `field`. | First endpoint story with input; AISDLC-HARDENING | API owner / recovery tech lead | Before the first endpoint story with a request body or required parameter | INC-005 spec §3.1 A-08; TE003-SP-DG-03 |
| OPEN-046 (NEW-TE003-D) | Assign the dependency-scan and ZAP-baseline pipeline jobs required by testing standards §1 (Security row) to a story or an AISDLC-HARDENING change. No Epic 1 TE story owns them. | AISDLC-HARDENING | Recovery tech lead / security | Before SIT exit | INC-005 spec §3.1 A-09; TE003-SP-DG-04 |
| OPEN-047 (NEW-TE003-E) | Add the 401 / expired-session state to `QueryState.tsx` (FS-3.1) in the first story with a screen, or as hardening. | First Epic 1 screen story; AISDLC-HARDENING | Front-end lead | Before the first screen story's code gate | INC-005 spec §3.1 A-15 |
| OPEN-048 (NEW-TE003-F) | Decide whether recovery coverage verification (`./gradlew recoveryCoverageVerification`, four metrics at 80%, TE-001 v4 SPEC-020) becomes a CI job or part of `backend-unit`. Today D-RCV-28 (3) and D-RCV-40 keep it outside `check`, and the Builder runs it per story; a CI job is a pipeline change (D-RCV-05). TE-001 v4 SU-10 handed CI wiring to TE-003 and TE-011; TE-003 hands it on here. Not blocking. | RWB-TE-003, RWB-TE-011, every later story | ACE tech lead (owner of D-RCV-05) | Before SIT exit | INC-005 spec §3.1 A-09, SPEC-017; TE003-SG3-DG-03 |
| OPEN-049 (NEW-TE003-G) | Decide how the front end starts or forwards the trace (for example a W3C `traceparent` header from `ApiClientContext`), as Audit and Logging Design v2 §3 requires ("from the front end through the service"), and whether API Specification v4 must declare the header. Today the trace starts at the service (INC-005 spec SPEC-013). Not blocking. | First Epic 1 screen story; AISDLC-HARDENING | Front-end lead / solution architect | Before the first screen story's code gate | INC-005 spec SG4-03 fix, §16; TE003-SG4-DG-01 |

## 2. `aisdlc/docs/open-items.md` — amendments to existing rows

| ID | Amendment |
|---|---|
| OPEN-039 | Replace "confirm `api/recovery-api.yaml` is the canonical copy" with "confirm `api/recovery-api-v4.yaml` (SHA-256 `535cb46594190f0bf535a2ad3f034e9f50f987a92fe19c0524a2755f5923b891`) is the canonical copy". Add: "accept that `postAdminWorkflowsSmoke` (RWB-E1-071) is the one E1 operation enforced at TE-003 merge; the other 72 are pending with their story". Replace "P2 `generated.web`/`generated.model`" with "`th.co.scb.ace.demo.recovery.integration.generated.web`/`.model`, P2 named interfaces with `propagate = false` (RWB-TE-001 v4 spec SPEC-004 (d), SU-08)". Add: "approve spike results S-1..S-4; pin the OpenAPI Generator plugin and validator versions and re-check the generator options against the pinned version (`interfaceOnly`, `skipDefaultInterface`, `useTags`, `useSpringBoot4`, `useJackson3`, `requestMappingMode=none`, normalizer `SET_TAGS_TO_OPERATIONID`); approve the `apiTooling` source set in package `th.co.scb.ace.tooling.recoveryapi`, outside `th.co.scb.ace.demo` (INC-005 spec §7.5; fallback ASM-TE003-09)". |
| OPEN-040 | Add: "RWB-E1-022 also owns (a) method checks that name the capability area instead of a role or `isAuthenticated()` (audit A-03), and (b) the `{action}` value of MSG-P4-002 per language (audit A-08; Error and Message Standard v4 §3)". |
| OPEN-042 | Change "Raised in" reference `ASM-TE003-09` to `ASM-TE003-14` (assumption renumbered in the INC-005 remediation spec). |

## 3. `aisdlc/requirement/Traceability_Matrix.md`

### 3.1 §3 Story trace, row 005 — replace the status cell

`Spec re-issued 18 Nov 2026 (remediation 3, SPEC-RWB-TE-003-001..022), pending spec gate review-4; plan not current; source REQ-DRI-007, REQ-ACA-003; build not started; depends on RWB-TE-001 merged`

### 3.2 SPEC rows to add for RWB-TE-003 (BR-RWB-013 / FR-RWB-013)

| SPEC ID | Requirement source | Story ref | Test IDs | Code | Status |
|---|---|---|---|---|---|
| SPEC-RWB-TE-003-001 | REQ-DRI-007 | BR1, §12 | T-TE003-10, -11, -34 | — | Specified |
| SPEC-RWB-TE-003-002 | REQ-DRI-007 | BR2, AC3, Flow 1, X2 | TC-TE-003-03; T-TE003-14 | — | Specified |
| SPEC-RWB-TE-003-003 | REQ-DRI-007 | BR5, AC1, Flow 2, §12 | TC-TE-003-01; T-TE003-15 | — | Specified |
| SPEC-RWB-TE-003-004 | REQ-ACA-003 | BR4 | T-TE003-15 | — | Specified |
| SPEC-RWB-TE-003-005 | REQ-ACA-003 | BR4, AC8 | T-TE003-12, -13 | — | Specified |
| SPEC-RWB-TE-003-006 | REQ-DRI-007 | BR1, BR5, AC1, AC7, Flow 3 | TC-TE-003-01, -07; T-TE003-16 | — | Specified |
| SPEC-RWB-TE-003-007 | REQ-DRI-007 | BR1 | T-TE003-17 | — | Specified |
| SPEC-RWB-TE-003-008 | REQ-DRI-007 | BR3, Flow 5 | T-TE003-18 | — | Specified |
| SPEC-RWB-TE-003-009 | REQ-DRI-007 | BR3, AC5, AC6, X4, X5 | TC-TE-003-05, -06; T-TE003-19, -20 | — | Specified |
| SPEC-RWB-TE-003-010 | REQ-DRI-007 | Flow 5, §17 G3 | T-TE003-21 | — | Specified |
| SPEC-RWB-TE-003-011 | REQ-DRI-007 | BR2, BR3, AC2, AC4, Flow 6 | TC-TE-003-02, -04; T-TE003-22, -23 | — | Specified |
| SPEC-RWB-TE-003-012 | REQ-ACA-003 | BR4, AC8, Flow 7 | TC-TE-003-08, -09 (BLOCKED); T-TE003-24, -25 | — | Specified |
| SPEC-RWB-TE-003-013 | REQ-DRI-007 | BR2 (Audit and Logging Design v2 §3) | T-TE003-26, -35 | — | Specified |
| SPEC-RWB-TE-003-014 | REQ-DRI-007 | §13 step 2, AC1 | T-TE003-27 | — | Specified |
| SPEC-RWB-TE-003-015 | REQ-DRI-007 | Flow 8, §17 G2 | T-TE003-28 | — | Specified |
| SPEC-RWB-TE-003-016 | REQ-DRI-007 | §12 Trigger | T-TE003-29 | — | Specified |
| SPEC-RWB-TE-003-017 | REQ-DRI-007 | — (BS-7.2, D-RCV-06, D-RCV-28 (3), D-RCV-40; audit A-09) | T-TE003-30, -36 | — | Specified |
| SPEC-RWB-TE-003-018 | REQ-DRI-007 | §3, §12, §17 G3 | T-TE003-31 | — | Specified |
| SPEC-RWB-TE-003-019 | REQ-DRI-007 | BR5, §12 Idempotency | T-TE003-16, -32 | — | Specified |
| SPEC-RWB-TE-003-020 | REQ-DRI-007 | §17 G1, G2 | T-TE003-33 | — | Specified |
| SPEC-RWB-TE-003-021 | REQ-DRI-007 | AC1, AC7, X6 | TC-TE-003-01, -07 | — | Specified |
| SPEC-RWB-TE-003-022 | REQ-DRI-007 | — (Audit and Logging Design v2 §3, §6; BS-4.6, AGENTS §4.7; audit A-07, D-RUN-15) | T-TE003-35 | — | Specified |

### 3.3 §7 Evidence index, INC-005 row

Plan column: `not current (re-plan after spec gate review-4 PASS and RWB-TE-001 merge)`.

## 4. `aisdlc/DOCUMENT-GAPS.md` — candidate rows

Number as DG-0nn. Columns as the register (Stories affected = RWB-TE-003 unless stated; Raised by = INC-005 specify remediation 1 or 2 as marked; Found = 2026-11-17, or 2026-11-18 for remediation 2 rows).

| Candidate | Source row | Suggested owner |
|---|---|---|
| TE-003 front-end output path vs FS-4.2 | TE003-SG-DG-01 | BA (story file) |
| "One interface per tag" vs §17 G3 | TE003-SG-DG-02 | BA / solution architect |
| "Spring Boot 3" target | TE003-SG-DG-03 | BA (story file, Technical Enabler Build Notes v2) |
| No 500 response / no generic message ID / `Problem` without `required` | TE003-SG-DG-04 | API owner; message standard owner |
| "79 operations" stale | TE003-SG-DG-05 | BA |
| Step 5 / AC5 vs §13 "Done when" | TE003-SG-DG-06 | BA (Story Defects v4 row 93) |
| AC-P2-001-01 citation | TE003-SG-DG-07 | BA |
| BR5 citation ADR-006 | TE003-SG-DG-08 | Solution architect |
| `api/recovery-api.yaml` file name | TE003-SP-DG-01 | BA |
| In-memory test database | TE003-SP-DG-02 | BA |
| No 400/422 for malformed input on most operations | TE003-SP-DG-03 | API owner |
| No owner for dependency scan and ZAP | TE003-SP-DG-04 | Test lead |
| No Thai / per-call `{action}` source | TE003-SP-DG-05 | Message standard owner (affects RWB-E1-022) |
| Generated package at recovery root vs L-RCV-14 | TE003-SP-DG-06 | BA |
| E1-071 right U vs API v4 right C on `postAdminWorkflowsSmoke` (remediation 2, from gate round 2) | TE003-SG3-DG-01 | BA (RWB-E1-071) |
| E1-071 smoke response fields vs API v4 (remediation 2, from gate round 2) | TE003-SG3-DG-02 | BA; API owner |
| Coverage outside `check` (D-RCV-28 (3), D-RCV-40) vs audit A-09 and the README note; settled by precedence (remediation 2) | TE003-SG3-DG-03 | ACE tech lead (NEW-TE003-F) |
| No source for a coverage exclusion of generated code; measured (remediation 2) | TE003-SP2-DG-01 | Recovery tech lead |
| E1-071 §12 smoke request body, 409 and right U vs API v4 (remediation 2) | TE003-SP2-DG-03 | BA (RWB-E1-071); API owner |
| `X-Correlation-Id` in audit A-07 and backend context §7, absent from API v4 and the document set (remediation 2) | TE003-SP2-DG-04 | API owner |
| Audit and Logging Design v2 §3 trace ID "from the front end" with no front-end or API mechanism (remediation 3, from gate round 3) | TE003-SG4-DG-01 | Solution architect; front-end lead (NEW-TE003-G) |

## 5. `aisdlc/docs/decisions/decision-register.md` — notes (no new decision)

| Ref | Note |
|---|---|
| L-RCV-11 | Premise restated for this repository: one E1 operation (`postAdminWorkflowsSmoke`, RWB-E1-071) is already implemented and is `enforce: true` at TE-003 merge; an implemented operation with `enforce: false` fails the build. Baseline file `api/recovery-api-implementation.yaml` also holds `outsideSpecification` (README decision 6). Source: INC-005 spec SPEC-009, SPEC-001. |
| L-RCV-14 | P2 is `integration` (RWB-TE-001 v4 spec, Field-level behaviour matrix); generated packages are `integration.generated.web` and `.model`, named interfaces with `propagate = false`. Server generation is one interface per operation, abstract only, with no class-level mapping (INC-005 spec §7.1, SPEC-003). |
| D-RUN-15 | Audit A-07 is owned by RWB-TE-003 (INC-005 spec SPEC-022, SPEC-013); no `X-Correlation-Id` header (TE003-SP2-DG-04). |
| D-RCV-28 (3), D-RCV-40 | Applied unchanged: TE-003 adds its code to `recoveryCoverageVerification` and leaves the task outside `check` (INC-005 spec SPEC-017). |

## 6. `aisdlc/evidence/phase0-standards-audit.md` — owner note

Item A-07: owner RWB-TE-011 → **RWB-TE-003** (orchestrator decision D-RUN-15, `AI-SDLC-BUILD-LOG.md` §1, 2026-11-18T00:39). Scope taken: safe exception logging and `traceId` correlation (INC-005 spec SPEC-022, SPEC-013). Not built: `X-Correlation-Id` (TE003-SP2-DG-04). Apply only if the orchestrator keeps owner columns current in that evidence file.

## 7. Increment card and INDEX

None. `INC-005-epic-1-RWB-TE-003.md` and `INDEX.md` need no change from this stage; status moves are the orchestrator's after the gate.
