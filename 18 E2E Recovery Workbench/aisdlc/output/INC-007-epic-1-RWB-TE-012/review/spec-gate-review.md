# Spec gate review: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG` (findings `REVIEW-RWB-TE-012-SG-01` to `-11`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `agent-run-log.md` |
| Reviewer | Compliance Reviewer (spec gate), `.claude/agents/compliance-reviewer.md` with `aisdlc/RUN-BRIEF.md` |
| Date | 2026-11-17 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 1 High, 5 Medium, 5 Low (11 in all) |
| Handoff | **Blocked.** High and Medium findings block the Implementation Planner until the spec is fixed and re-reviewed (`aisdlc/.github/rules/pdlc.md`, Human Checkpoints). |

## 1. What was checked

**Inputs read.**
- Increment card `aisdlc/docs/increments/INC-007-epic-1-RWB-TE-012.md`.
- Story file RWB-TE-012 v1 (Epic 1 story files v7), `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-012-document-storage-containers-v1.md`, sections 1 to 19.
- RWB-E1-024 v1 (story files v7), sections 3 to 5, 12 and 13; RWB-E1-041 v1 (quarantine, SY-OCR, JOB-12).
- Rules: `specification-execution-gates.md`, `pdlc.md`, `security-quality-standards.md`, `traceability-standards.md`, `environment-standards.md`, `versioning-standards.md`, `architectural-standards.md`, `implementation-execution-gates.md`.
- Contexts: `backend-context.md`, `backend-standards.md`, `testing-standards.md`, `project-context.md` (P5); `AGENTS.md`; `README.md` ("Local versus target", "Decisions taken" 1 to 7); `aisdlc/evidence/phase0-standards-audit.md` (A-04); `aisdlc/docs/increments/story-defects.md` (RWB-TE-012 row); `aisdlc/requirement/Traceability_Matrix.md` row 007.
- The current RWB-TE-001 remediation spec `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` (written 23:40, after this spec), because TE-012 depends on TE-001.

**Code verified in this repository** (not taken from the spec): `documents/api/DocumentStore.java`, `documents/internal/BlobDocumentStore.java`, both `package-info.java`, `platform/internal/RecoveryProperties.java`, `platform/internal/SecurityConfig.java` (line 68 permits `/actuator/health/**`), `application.yaml`, `application-local.yaml`, `RecoveryBoundaryTest.java`, `RecoveryDatabaseIT.java` (line 61), `ModulithTest.java`, `backend/build.gradle.kts`, `.env.example`, `docker-compose.yml`, `scripts/dev.ps1`, and the JaCoCo report `backend/build/reports/jacoco/recoveryCoverageReport.xml`.

**Citation sample checked against the documents (all correct).**

| Spec citation | Verified text |
|---|---|
| Decision Log v10, D-RCV-31 | "through the published DocumentStorage interface"; "No blob is written except through DocumentStorage (RWB-TE-012)"; MSG-GEN-006 when the policy is absent |
| Decision Log v10, DL26 and DL27 | Both open; DL27 recommends option A, the ACE storage pattern with a write-once container |
| Controls Catalog v3, CTL-12 | Legal documents cannot be changed or deleted |
| NFR v3, NFR-028, NFR-029, NFR-053 | "periods not set" (Open DL26); write-once for legal types; "Encrypted" with no key type |
| FSD P5 v3, AC-ALT-P5-001-01 | `DOCUMENT_CHANGE_REFUSED` for each attempt "with the document ID and the caller", including attempts directly on the container |
| Audit and Logging Design v2 | "ACE audit log", "Every change made through the service", "ACE logging" |
| PDPA Design v2 §1, §8 | Case numbers are indirect identifiers; Southeast Asia, "Bank position to confirm" |
| Records Retention v2 §1, §2 | Legal DP10 "10 years after the case closes; write-once"; "Archive tier" only for archived records |
| Environment and Deployment v4 §6 | Flag table lists `rwb.p3.temporal` and `rwb.p3.drools` only |
| API Specification v4, `postCasesCaseidDocuments` | `/cases/{caseId}/documents` declares 201, 401, 403, 404, 413, 415, 422, 503 and no 409 |
| Physical Schema v6 | `document.id uuid`, `case_id uuid`, `storage_ref varchar(400)`, `doc_version integer NOT NULL DEFAULT 1`; DF-DOC-006 and DF-DOC-010 rows |
| Error and Message Standard v4 | MSG-P5-002, MSG-GEN-006 and MSG-P4-002 exist with the story's wording |
| Users, Roles and Permissions v4 | SY-OCR Documents CRU; identities RWB-{DEV,SIT,UAT,PROD}-SY-OCR |
| Security and Access Design v4 | "one identity per non-human actor"; "No secret in code, configuration or prompts" |
| Test Cases v7 | TC-TE-012-10 to -13 exist; TC-TE-012-13 is the RW-REFADM access case |
| `backend-context.md` §8, §11 | 30 s external timeout; "Blob geo-redundancy" |

**Baseline claims checked (all correct).** `DocumentStore` has no caller; `BlobDocumentStore` names blobs by document UUID, calls `createIfNotExists()` on first write, uses the full `DefaultAzureCredential` chain and sets no timeout; the `rwb.blob` block and container names `rwb-documents`/`rwb-documents-legal` appear in no document; the `build.gradle.kts` comment names a non-existent `DocumentStorageConfig`; the baseline config bean throws at startup when neither `rwb.blob.connection-string` nor `rwb.blob.endpoint` is set, which is why `RecoveryDatabaseIT` sets the property.

**What is correct.** The spec reads the story well:
- all 7 BRs, 12 ACs, 7 flow steps and X1 to X10 are mapped, and the seams to E1-024, E1-026, E1-041, E1-057 and E1-032 are named (D-RUN-08);
- the D-RCV-31 precedence over story §12 (DGAP-01) is applied correctly, and keeping `DocumentContainers` internal because it returns an Azure type (DGAP-02) is sound;
- the X9/AC12 ordering (hash first, conditional upload, re-check on race) settles the open story-defect row;
- no value is invented for region, redundancy, access tier or encryption key; they are required template parameters with recorded gaps;
- the AC9 "no document row" conflict with E1-024's COPY_PENDING insert (DGAP-17) is found and handed on as an open item;
- UUIDs in blob names (not case numbers) is the right PDPA call;
- no migration, no endpoint, no new dependency, no personal data, and the shared files are untouched.

The failures are in the module placement, the published contract's fit with its consumer, the health side effects, the local stack and the test and coverage plan.

## 2. Findings

### REVIEW-RWB-TE-012-SG-01: High. The module placement contradicts the story and the predecessor story's current spec

**Affects:** SPEC-006, -008, -010, -016, -018 ("`RecoveryBoundaryTest` ... pass unchanged"); DGAP-18; header and preconditions ("RWB-TE-001 (done)").

**Evidence**
- Story v7 §13: "Java package `recovery.dochub.storage`". The spec puts every type in `documents.api` and `documents.internal.storage` (DGAP-18), on the ground that "the TE-001 module map is under re-review; the code module is the baseline". That is not one of the RUN-BRIEF precedence rules or a documented default, so Blocker = No is not justified as written.
- RWB-TE-001 is earlier in Build Sequence v6 (D-RUN-08) and is not done: it is in spec remediation (`AI-SDLC-BUILD-LOG.md`, rows for 23:22:51). Its current spec `INC-002-epic-1-RWB-TE-001/specify/spec.md`:
  - SPEC-022 and the Relocation table (line 215-216): `documents.api.DocumentStore` moves to `dochub.api`; `documents.internal.BlobDocumentStore` with `BlobProperties` moves to `dochub.storage`; "the four baseline module packages cease to exist";
  - line 114 and SPEC-009: BND-5 becomes map-driven with `clientPackages` `dochub [storage]`, so `com.azure.storage` is allowed only in `dochub.storage`;
  - SPEC-026: `blobClientOnlyInDocumentsModule` is replaced;
  - SPEC-023: `RecoveryProperties` is replaced by per-module records.
- Consequences if TE-001 merges first, as the build order requires: `documents.internal.storage` fails the new BND-5; SPEC-016 deletes classes and edits a `RecoveryProperties` comment that no longer exist at those paths; SPEC-006's reliance on "the module sub-prefix rule in `RecoveryProperties`" and SPEC-018's "`RecoveryBoundaryTest` ... pass unchanged" are both false.

**Required fix**
- Place the code where story v7 §13 and the TE-001 spec put P5: `DocumentStorage`, `StoreRequest`/`BlobRef` (see SG-02), `StorageReadiness` and the two exceptions in `dochub.api`; `DocumentContainers`, the config, adapter, guard, mapper, readiness indicator, audit log and emulator bootstrap in `dochub.storage` (the TE-001 client package).
- State "RWB-TE-001 merged in this repository" as a precondition, and restate SPEC-016 as corrections to `dochub.api.DocumentStore` and `dochub.storage.BlobDocumentStore` after the relocation.
- Bind `rwb.dochub.*` in a P5 record without reference to `RecoveryProperties`, and read `rwb.environment` (SPEC-017) through P5's own binding, not another module's type.
- Replace "`RecoveryBoundaryTest` ... pass unchanged" with "passes under the TE-001 module map".
- Revise DGAP-18 to cite the TE-001 spec, and correct "Depends on RWB-TE-001 (done)" in the header.

### REVIEW-RWB-TE-012-SG-02: Medium. The published contract does not fit its named consumer RWB-E1-024

**Affects:** SPEC-010, -011, -015, -019; `contracts/backend-apis.json` (`published_java_interface`); CLAR-001.

**Evidence**
- RWB-E1-024 v1 §12 publishes, in the same P5 `api` package, `DocumentStore.store(StoreRequest request)` whose `StoreRequest` holds "caseId, documentType, source, intakeBlobRef, sha256, fields, partyId", and `addVersion`/`replaceContent` taking a `BlobRef file`. The spec defines a different top-level `StoreRequest` (caseId, documentId, docVersion, writeOnce, contentType, content) in the same package. The spec freed the name `DocumentStore` for E1-024 but takes `StoreRequest`, so the two stories collide.
- E1-024 flow step 1 hands over "the file in the intake container" and step 7 has `DocumentStorage.store` write it to `rwb-docs` or `rwb-docs-legal`. The spec's `store` takes only `byte[]`, and SPEC-015 makes `open()` refuse an intake `BlobRef`. The spec does not say how E1-024 gets intake bytes (through the internal `DocumentContainers`, or a copy operation on `DocumentStorage`), and the SPEC-019 seam table is silent on it.
- E1-024 persists `storage_ref` as text; `open(BlobRef)` needs a `BlobRef` with `sha256`, `size` and `existing`. No factory from `storage_ref` is defined, so each caller would rebuild the format itself.

**Required fix**
- Rename the TE-012 request type (for example `BlobWriteRequest`) or nest it in `DocumentStorage`, and say which of `BlobRef` E1-024 uses.
- Specify the intake-to-store path: either a `store` variant that copies from an intake `BlobRef`, or an explicit rule that P5 callers read intake through `DocumentContainers` and then call `store` with bytes. Add it to the SPEC-019 seam row for E1-024.
- Add `BlobRef.fromStorageRef(String)` (or equivalent) with validation, and a unit test for the round trip.

### REVIEW-RWB-TE-012-SG-03: Medium. The `documentHub` health component changes the root health status and can be driven by unauthenticated callers

**Affects:** SPEC-009, the Health component table, the readiness status matrix, ASM-TE012-08 and -09.

**Evidence**
- The flag defaults to `false` in `application.yaml` (SPEC-006, ASM-TE012-14), and with the flag off the component reports `OUT_OF_SERVICE`. Spring Boot's default status order is DOWN, OUT_OF_SERVICE, UP, UNKNOWN, and both DOWN and OUT_OF_SERVICE map to HTTP 503. So `/actuator/health` turns 503 in every environment where the flag is off, and also whenever the component is DOWN (for example a blank SY-OCR client ID). `scripts/dev.ps1 status` (line 107) reads `/actuator/health` and then prints "Backend not reachable". The spec covers only the probe groups (ASM-TE012-09), not the root aggregate.
- `SecurityConfig.java:68` permits `/actuator/health/**` without authentication. The spec re-evaluates readiness "on every read of the component": up to four storage calls, each with up to 10 s, on every anonymous health request. No cache or rate bound is set. That is a cost and denial-of-service path on an open endpoint.

**Required fix**
- Define the component's effect on the root aggregate: report flag-off as `UP` with detail `FLAG_OFF` (or `UNKNOWN`), or put `documentHub` in a named health group with the root excluding it, or set a status mapping. State the HTTP code of `/actuator/health` with the flag off.
- Re-evaluate from a cached readiness value with a bounded refresh (for example `management.endpoint.health.cache.time-to-live`, or a scheduled refresh with a minimum interval), so that an anonymous read cannot trigger storage calls on demand. Keep the "one re-evaluation inside `store()` while NOT_READY" rule.
- Add unit tests for both points.

### REVIEW-RWB-TE-012-SG-04: Medium. The rename breaks the local Docker stack and existing `.env` files; impacted nodes are incomplete

**Affects:** SPEC-016, SPEC-017; Change Scope "Impacted Existing Nodes"; ASM-TE012-11.

**Evidence**
- SPEC-016 renames only `RWB_BLOB_CONNECTION_STRING` in `.env.example`. It misses:
  - `.env.example:24` `RWB_BLOB_CONNECTION_STRING_DOCKER` (the `azurite` host variant);
  - `docker-compose.yml:135`, where the `backend` service sets `RWB_BLOB_CONNECTION_STRING: ${RWB_BLOB_CONNECTION_STRING_DOCKER}`;
  - `README.md:25` ("Azure Blob DocumentStore").
- `scripts/dev.ps1` (lines 28-31) copies `.env.example` to `.env` only when `.env` is absent, so every existing `.env` keeps the old name.
- The local profile sets the flag to `true`. With no emulator string and no `account-url`, SPEC-006/-007 validation fails startup. So `docker compose --profile app` and `./scripts/dev.ps1 backend` on an existing `.env` stop working, and with them the e2e stack.

**Required fix**
- List `docker-compose.yml` and both `.env.example` lines as impacted nodes, and rename both variables (for example `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` and `..._DOCKER`).
- Specify the upgrade path for an existing `.env`: `dev.ps1` adds the new key when missing, or the old name is accepted as a fallback for one release with a warning.
- Correct `README.md:25`, and add a startup test for the local profile with the emulator string set.

### REVIEW-RWB-TE-012-SG-05: Medium. The backend coverage gate is not achievable as declared, and two required metrics are missing

**Affects:** Unit Test Applicability (backend row); SPEC-018; `implementation-execution-gates.md` (Hard Gates); testing-standards §6.

**Evidence**
- The spec sets the gate as "80% line and branch on `th.co.scb.ace.demo.recovery` (`recoveryCoverageVerification`)". The current report `backend/build/reports/jacoco/recoveryCoverageReport.xml` measures the recovery package at **32.0% line (133/415) and 27.2% branch (25/92)**; INSTRUCTION is 31.6% and METHOD 30.4%. TE-012 deletes 41 uncovered `documents.internal` lines and adds new code, but cannot lift `platform`, `workflow` and `rules` (241 uncovered lines) on its own. The spec does not say whether the gate applies to the whole package (then it depends on another story, which is not named) or to changed code with "no global drop" (testing-standards §6).
- The compliance-reviewer instructions and `specification-execution-gates.md` require 80% for lines, statements, branches and functions where the native tool supports them. JaCoCo supports INSTRUCTION and METHOD; the spec and `build.gradle.kts` plan only LINE and BRANCH. D-RCV-06 and BS-7.2 say line/branch, so this is a rule conflict that the spec must state, not drop silently.
- `recoveryCoverageVerification` is not part of `test`, `check` or CI (`README.md:85-86`; `build.gradle.kts` wires only the report).

**Required fix**
- State the measured scope and how it passes: either "the whole recovery package, after the story that raises the baseline (name it) has merged", or "new and changed TE-012 classes at 80%, with no drop in the package totals", with a reference to testing-standards §6.
- Plan INSTRUCTION and METHOD at 80% alongside LINE and BRANCH, or record the D-RCV-06 conflict as a document gap with an owner.
- Say which command and task run the verification for this story.

### REVIEW-RWB-TE-012-SG-06: Medium. The unit test plan leaves the adapter's own logic and the integration-client cases untested in the gated suite

**Affects:** SPEC-018; SPEC-011, -014, -015, -017; `security-quality-standards.md` (Quality: integration clients, critical rules); AC11; X8.

**Evidence**
- Only the eight unit tests in SPEC-018 run in `test` and count toward coverage. These run only in the `recovery-it` Azurite tests, which are outside `test`, outside coverage and outside CI (D-RCV-44 requires them only for migration work):
  - `BlobStorageAdapter.store` routing (`writeOnce` to legal, otherwise standard);
  - flag-off and NOT_READY refusals with no storage call (SPEC-011 steps 1-2);
  - the `open()` container allow-list (AC11, X8, a no-I/O rule);
  - metadata `sha256` written at creation;
  - `LocalEmulatorBootstrap`.
- `DocumentAuditLog` has no test at all. That means nothing tests the event fields, logger name `recovery.audit`, `actorId` absent for system calls, or that no content or personal data is logged (story §17).
- `security-quality-standards.md` requires success, timeout, unavailable, malformed-response and retry/fallback tests for integration clients. The plan has timeout (unit) and unavailable (mapper only). It has no unit-level success path, no malformed or unexpected error code case (SPEC-013 "Anything else, rethrown"), and no test that SDK retries stay inside the overall timeout (SPEC-007).

**Required fix**
- Add unit tests (mocked `BlobContainerClient` or the JDK `HttpServer` stub) for the routing, both refusals, the `open()` allow-list, metadata, `DocumentAuditLog` and the emulator bootstrap.
- Add the integration-client cases: success, unexpected error code, and retry inside the timeout.
- State whether the Azurite `recovery-it` tests are a merge requirement for this story, and how they run.

### REVIEW-RWB-TE-012-SG-07: Low. The spec has no `Status: SUCCESS` line, and the run log reports a gate step that had not run

**Affects:** spec header; `agent-run-log.md`; `compliance-validation.md`; Change Scope.

**Evidence**
- `implementation-execution-gates.md` (Upstream Readiness) requires `Status: SUCCESS` in `spec.md`. The spec has "Spec complete; spec gate in `review/spec-gate-review.md`", and grep finds no `Status:` line.
- `agent-run-log.md` lists `review/spec-gate-review.md` as an output and says "Compliance Reviewer spawned as a general-purpose subagent". `compliance-validation.md` names the same. When this review started, the `review/` folder did not exist; the orchestrator ran the gate.
- "New Nodes Required" should be YES/NO (`specification-execution-gates.md` Step 3); the spec gives a list only.

**Required fix**
- Add `Status: SUCCESS` (or `BLOCKED`) as a line, and keep the gate result separate.
- Record the gate as `GATE_REVIEW: PENDING_ORCHESTRATOR` (RUN-BRIEF rule 6).
- Write "New Nodes Required: YES" before the list.

### REVIEW-RWB-TE-012-SG-08: Low. The FR, NFR and control IDs have no rows of their own in the coverage table

**Affects:** Requirement-to-SPEC Logic Coverage; `traceability-standards.md`; `specification-execution-gates.md` ("All FR-* and NFR-* are mapped to SPEC-*").

**Evidence**
- `FR-RWB-007`, NFR-029, NFR-053, CTL-12, CTL-09, REQ-DCM-002 and REQ-DCM-003 appear only in the header. None is a `REQ_REF` row with mapped SPEC IDs. NFR-053 (encryption at rest and in transit) maps in practice to SPEC-001 (TLS 1.2, platform encryption), but the table does not say so.

**Required fix**
- Add one row each, mapping to the SPEC IDs that meet them, so that the matrix row in `shared-updates.md` can carry SPEC-to-FR/NFR links.

### REVIEW-RWB-TE-012-SG-09: Low. The SCR-44 readiness display seam has no named owner

**Affects:** coverage row "§4 step 7"; Frontend Specification; `contracts/frontend-integrations.json`; D-RUN-08.

**Evidence**
- The spec and the contract say "the story that builds SCR-44". Several Epic 1 story files reference SCR-44 (RWB-E1-056 run books and monitoring, among others). D-RUN-08 asks for later-story work to be named as a seam.

**Required fix**
- Name the owning story from Build Sequence v6, or record the missing owner as a document gap with an open item.

### REVIEW-RWB-TE-012-SG-10: Low. The read path's access check and access log are not assigned

**Affects:** SPEC-010, SPEC-015; Security, privacy and performance; BS-4.4; `security-quality-standards.md` ("document access" audit).

**Evidence**
- `DocumentStorage.open()` is published, so any module can call it through `api`, and documents hold personal data.
- E1-024 step 8 places the Documents R and scope check and the PII access log on its endpoints. The spec does not say that `open()` is not an authorization point, or that every caller must apply the check and the access log.

**Required fix**
- Add a guardrail line saying that callers of `open()` own the right and scope check and the PII access-log entry (RWB-E1-024; RWB-E1-039 for the log).
- Optionally, restrict which modules may depend on `dochub.api` in the TE-001 map.

### REVIEW-RWB-TE-012-SG-11: Low. The emulator guard leans on a property that defaults to DEV, and the key exception needs its decision row first

**Affects:** SPEC-017; ASM-TE012-11; story §17 guardrail.

**Evidence**
- `application.yaml` sets `rwb.environment: ${RWB_ENVIRONMENT:DEV}`, so one of the four guard conditions is true by default in any environment.
- The other three conditions (the account name `devstoreaccount1`, a loopback or `azurite` host, and the connection-string property) keep the guard safe.
- Story §17 forbids a connection string "in code, configuration or the pipeline". The spec relies on a README "Decisions taken" row that the Builder adds later (shared-updates §5).

**Required fix**
- State that emulator mode also requires the `local` profile (or an explicit `rwb.dochub.storage.emulator=true`) in addition to the three checks.
- Make the README decision row a plan-gate item, so the deviation is on record before any code merges. The README's existing "Local versus target" Blob row is the precedent to cite.

## 3. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (§12). Managed identity only, with container-scope roles and no account-scope data role (SPEC-005, -007). The read path's ownership is SG-10 |
| Customer data protection | UUID blob names, no metadata beyond `sha256`, IDs-only logs. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` through the service (SPEC-014). Direct attempts are a recorded gap (DGAP-11). Untested (SG-06) |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | Not applicable: `UI In Scope: NO` and `NO_API_CHANGE` are verified against story §12 and §15. The 409/503 mappings are seams to E1-024/E1-026 |
| Secrets and environment configuration | No key, SAS or connection string outside the DEV emulator (SG-11). Rename gaps in SG-04 |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` is correct. Backend gate not achievable as declared (SG-05); plan gaps (SG-06). SIT system tests are correctly `PENDING_ENVIRONMENT` |
| Module boundaries | Conflicts with the TE-001 map (SG-01) |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | No new library. TE-001 dependency mis-stated (SG-01) |

## 4. Review-level document gap

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| TE012-SG-DG-01 | RWB-TE-012 story v1 (story files v7), §12 | The story defines only `DocumentContainers`; no source document gives the `DocumentStorage` signature. | Decision Log v10 D-RCV-31 and RWB-E1-024 v1 §13 name `DocumentStorage`; RWB-E1-024 v1 §12 passes `intakeBlobRef` and `BlobRef` to its store, so a copy from intake is implied but not stated. | No | The spec may define the signature, as long as it fits the E1-024 contract (SG-02). | Raised as SG-02 for the spec to settle; owner solution architect via DOCUMENT-GAPS. |

DGAP-18 needs its citation and rationale replaced (SG-01). The other DGAP rows (01 to 17) are evidenced and correctly marked non-blocking.

## 5. Inputs for the re-issued spec and the plan (not findings)

1. **Azurite in Testcontainers.** The compose file runs Azurite 3.37.0 with `--skipApiVersionCheck` because SDK 12.37.2 sends a newer service version. The `GenericContainer` in SPEC-018 needs the same flag.
2. **DGAP-03.** Confirm early in DEV that a container-level time-based policy can be set on `rwb-docs-legal` while account-level blob versioning is on. If Azure requires version-level immutability in that case, SPEC-004 and the readiness check (`hasImmutabilityPolicy`) change. Treat this as an early spike, not a SIT item.
3. **Timeout semantics.** An upload that times out on the client can still complete on the server. The design already copes, because E1-024's COPY_PENDING retry meets the guard's same-hash path. Keep a test for that sequence.
4. **Carried open items.** The six rows proposed in `shared-updates.md` §3 stand. Add one for SG-02 (the E1-024 contract fit) if it is resolved by a seam, not in this spec.

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 5] [LOW: 5]
BLOCKING: YES. SG-01 to SG-06 must be fixed in a re-issued spec (output/INC-007-epic-1-RWB-TE-012/specify/) and re-reviewed (review/spec-gate-review-2.md). SG-07 to SG-11 are Low and should be fixed in the same pass.
DOCUMENT_GAPS: 1 review-level gap (TE012-SG-DG-01), 0 blockers; DGAP-18 to be revised.
NEXT_STEP: Technical Specifier re-issues the spec on the RWB-TE-001 module map (dochub), then this gate is re-run. Do not start the Implementation Planner.
```
