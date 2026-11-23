"""Build Build Notes Technical Enablers v3 from v2 (D-RCV-60). Scratch script, WP C-BNT."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "04 User stories" / "Recovery Workbench Build Notes Technical Enablers v2.md"
OUT = ROOT / "04 User stories" / "Recovery Workbench Build Notes Technical Enablers v3.md"

text = SRC.read_text(encoding="utf-8")

FRONT = """SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench build notes, the technical enablers

> **D-RCV-60.** This version applies decision D-RCV-60 and the Arch v5 target: 19 services inside ACE, one schema and login per service, Kafka with outbox and inbox, Temporal Schedules in place of Quartz, a local decision record with a central ledger, and no data lake. Each technical enabler now sits in the epic and story keys the realignment gives it. The Module line and every step of every entry stay as they are in v2, word for word, with release dates marked (tentative); the microservice change is carried in a realignment block under each Module line. RWB-TE-005 stays retired from D-RCV-36, and RWB-TE-007 is retired under D-RCV-60 with no new story. Owners follow the Ownership Map and the epic names follow Template and Rules section R5. Values the sources do not state are marked in place and listed in the gap and assumption registers (Template and Rules section R9).

> **D-RCV-36.** This version applies decision D-RCV-36. RWB-TE-005 is retired; its work moved to RWB-E1-073 (the scenario runner and the build gate) and the replacement notes sit in the Epic 1 build notes. The other technical enablers keep their existing content.

## Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| v2 | 16 November 2026 | D-RCV-36: RWB-TE-005 retired, its work moved to RWB-E1-073 and the Epic 1 build notes | Not recorded in the source |
| v3 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## Realignment map (D-RCV-60)

Every technical enabler keeps its legacy key, its title and its step text. The table gives the epic, the story keys, the target owner and the release of the new story set, from the Service Story Catalog v1 and the Ownership Map.

| Legacy key | Title | Epic (D-RCV-60) | Story keys | Service owner | Release |
|---|---|---|---|---|---|
| RWB-TE-001 | Recovery module folder and boundary test | RWB-PLT-TPL | RWB-PLT-TE001-APP; RWB-PLT-TE001-APP-2 | platform: the 19 service repositories from the template | 30 November 2026 (tentative) |
| RWB-TE-002 | Code owners for the recovery module | RWB-PLT-TPL | RWB-PLT-TE002-APP; RWB-PLT-TE002-OPS | platform: the 19 service repositories, ace-web and the architecture folder | 30 November 2026 (tentative) |
| RWB-TE-003 | Types and contract tests from the API specification | RWB-PLT-TPL | RWB-PLT-TE003-APP; RWB-PLT-TE003-APP-2 | platform: each service's own API file and client | 30 November 2026 (tentative) |
| RWB-TE-004 | Masked data in SIT and UAT | RWB-PLT-TPL; RWB-ITG-W1 | RWB-PLT-TE004-APP; RWB-ITG-TE004-ITG | rwb-source-data (P1) for the data; the loader is a tool outside the 19 services | 30 November 2026 (tentative) |
| RWB-TE-005 | (retired under D-RCV-36) | none | none; its work is RWB-E1-073 | not applicable | not applicable |
| RWB-TE-006 | Outbox and retry for outbound work | RWB-PLT-LIB; RWB-ITG-W1 | RWB-PLT-TE006-CON; RWB-PLT-TE006-APP; RWB-ITG-TE006-ITG | platform library, one copy in every service schema | 30 November 2026 (tentative) |
| RWB-TE-007 | Scheduled jobs on Quartz | retired (Template and Rules section R6) | none; dependencies point to RWB-PLT-E1071-CON | each owning service, through RWB-PLT-E1071 | not applicable |
| RWB-TE-008 | Decision log hash chain check | RWB-PLT-TPL; RWB-ITG-W1 | RWB-PLT-TE008-APP; RWB-ITG-TE008-ITG | rwb-decision (P7) for JOB-14; every service's own chain | 30 November 2026 (tentative) |
| RWB-TE-009 | Performance test harness | RWB-ITG-NFR | RWB-ITG-TE009-ITG | integration; QA team | 31 December 2026 (tentative) |
| RWB-TE-010 | Browser and accessibility tests | RWB-ITG-NFR | RWB-ITG-TE010-ITG | integration; QA team | 31 December 2026 (tentative) |
| RWB-TE-011 | PDPA lint for code, tests and logs | RWB-PLT-TPL | RWB-PLT-TE011-APP | platform; the field list is rwb-source-data's (P1) | 30 November 2026 (tentative) |
| RWB-TE-012 | Document storage containers | RWB-PLT-TPL | RWB-PLT-TE012-APP | rwb-document (P5) uses the containers | 30 November 2026 (tentative) |
| RWB-TE-013 | Agent runtime client with fallback | RWB-SVC-P10; RWB-SVC-P7; RWB-ITG-W1 | RWB-P10-TE013-CON; RWB-P10-TE013-APP; RWB-P10-TE013-OPS; RWB-P7-TE013-APP; RWB-ITG-TE013-ITG | rwb-agent (P10); rwb-decision (P7) for the ledger | 30 November 2026 (tentative) |

**How to read a realignment block.** "Delta, step by step" gives the target for the steps whose mechanism the microservice change alters. A step that is not named keeps the v2 text as the target. The story keys in the block are the specification; this document is the reading guide, as it was in v2.

"""

INTRO = ("Every flow step of every story in the technical enablers, written out in full so it can be followed "
         "without knowing the Workbench already. Each entry gives the step as the story states it, then what it means: "
         "who acts, what runs on its own, and what has to be built. The story remains the specification. Where the two "
         "differ, the story governs.")

DELTA = {
"RWB-TE-001": """
**Realignment (D-RCV-60).** Epic RWB-PLT-TPL service template and repositories, wave 0. Stories RWB-PLT-TE001-APP (preserved, as built) and RWB-PLT-TE001-APP-2 (delta), release 30 November 2026 (tentative). Suggested owner: TechX (suggested; any team may pick up this story). The target is 19 service repositories generated from one template, each with its own schema and login, and no repository compiles another (Arch v5 slides 20, 29 and 41).

Delta, step by step:

- Step 1: the 19 module packages become 19 services. Each repository carries one Java base package `th.co.scb.ace.workbench.recovery.<short without hyphen>` (Template and Rules section R4), with its `api` and `internal` packages inside it. There is no single recovery root package any more, and the front end folder `src/modules/recovery` stays in ace-web behind the gateway-bff composite route (DP-19).
- Step 2: the module map is held per service repository and lists that service's own packages only. A service's entry also carries its schema `rwb_<short with _>`, REST base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1` and Temporal task queue `rwb-<short>` (Ownership Map, Services).
- Step 3: ArchUnit keeps BND-4 and BND-5 inside a service. BND-1 and BND-2 point at the ACE Common and collection contracts instead of packages of one codebase, and BND-3 becomes the other service's published contract or an application event through the outbox, because the other module is now another repository with its own login (DP-01, DP-09, DP-11).
- Step 4: the front end rule becomes one rule per service: a screen reaches its owner service through the gateway-bff composite route and imports no other service's screen (DP-19; H RWB-PLT-N001-CON).
- Step 5: the guard covers each service's own base `/api/recovery/<short>/v1` and calls the rwb-access authorise contract instead of the common module's internal interface INT-34 (DP-08; H RWB-PLT-E1037-CON, C RWB-P4-E1037-CON). MSG-P4-002 is unchanged.
- Steps 6 to 8: the pipeline, the failure text and the fix are unchanged in intent. A cross-schema reference, and a Kafka record sent or consumed without the outbox and inbox library, join the rules that fail the build (RWB-PLT-TE001-APP-2).
""",
"RWB-TE-002": """
**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, wave 0. Stories RWB-PLT-TE002-APP (TechX suggested owner) and RWB-PLT-TE002-OPS (DevOps suggested owner), release 30 November 2026 (tentative). Repository protection now applies to each of the 19 service repositories plus ace-web, the migration folder and the architecture folder. Whether the split takes one code owners file per repository or one shared file is Not specified in the source documents (CG-C-BNT-4; ASM-C-BNT-4).

Delta, step by step:

- Step 1: the recovery back end path becomes the 19 service repositories created from RWB-PLT-TPL; the recovery test, recovery migration and recovery front end folders and `architecture/recovery-modules.yaml` stay as paths. The team handles stay `@scb-ace/ace-team` for the ACE Common path and `@scb-ace/techx-recovery-tech-leads` for the recovery paths, assumed until DL37 and DL36 are answered, as in v2.
- Step 2: CodeOwnersValidation runs in the pull request build of every repository, with the same three checks and the same text `owner {team} not found`.
- Step 3: the branch rule on main is set per repository by the ACE team repository administrator, with the same settings: a pull request, review from code owners, one approval, stale approvals dismissed, the author's own approval not counted.
- Steps 4 to 7 are unchanged in intent: the host takes the owner from the last matching pattern per changed path, and the merge waits for every owning team of the changed paths.
""",
"RWB-TE-003": """
**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, wave 0. Stories RWB-PLT-TE003-APP (preserved, as built) and RWB-PLT-TE003-APP-2 (delta), release 30 November 2026 (tentative). Suggested owner: TechX (suggested; any team may pick up this story).

Delta, step by step:

- Step 1: the one `api/recovery-api.yaml` becomes the 19 service API files plus gateway-bff and an index (Template and Rules section R8.4). Each file is linted in its own service's build with the same recovery rule set, and the rules of BR2 are unchanged.
- Step 2: generation runs per service, into `<ACE base package>.recovery.<short>.generated.web` and `.generated.model`. The generated packages are no longer shared between modules, because each service implements only its own interfaces.
- Step 3: one generated TypeScript client per service in `ace-web/src/modules/recovery/api/generated`; screens import through gateway-bff and never call a service base directly.
- Step 4: the generation steps sit before the compile step of each service, so a removed property still stops that service compiling.
- Step 5: OperationCatalog reads the service's own file and `rwb.release` is set per service; an operation whose first release belongs to a later service wave is pending in the services that do not own it.
- Step 6: RecoveryContractTest runs per service against its own contract fakes; `contract broken` and `undocumented status` are unchanged.
- Step 7: the role and permission data are read from rwb-access, which owns `role`, `permission` and `masking_rule` (Ownership Map), instead of a seed read in place by the monolith; the security administrator still owns the content. MSG-P4-002 is unchanged.
- Step 8: one report per service, with the gateway-bff report covering the composite routes. The 79 operations of v2 stay one total, now spread across the files; how they divide between the 19 services is Not specified in the source documents (CG-C-BNT-2; ASM-C-BNT-2). A failure in any service's report fails that build.
""",
"RWB-TE-004": """
**Realignment (D-RCV-60).** Stories RWB-PLT-TE004-APP (platform, RWB-PLT-TPL) and RWB-ITG-TE004-ITG (RWB-ITG-W1), release 30 November 2026 (tentative). The data belongs to the services: `sys_fields`, the extension tables and the interaction ledger are rwb-source-data's (P1), and every business table sits in the schema of its owner (Ownership Map; DP-01). The loader stays a tool outside the 19 services.

Delta, step by step:

- Steps 1 and 2 are unchanged: the PII service writes the files and the manifest, and the platform administrator (RW-PLATADM) starts the stage, which holds one advisory lock per environment under SY-DATALOAD behind the flag `rwb.dataengine.masked-copy`. Feature flags are a platform library object (Ownership Map).
- Step 3 is unchanged: the environment guard reads `rwb.maskedcopy.allowed-environments` and refuses DEV and PROD with MSG-P1-002 before any file is opened.
- Step 4: the masking rule version in force is read from rwb-access's masking policy, which owns `masking_rule` (Ownership Map), and `tools.masked_copy_load` stays in the tool's own schema `tools`.
- Step 5 is unchanged in its checks (CTL-02), now applied per service.
- Step 6: the `is_personal` tag is read through the rwb-source-data contract, which owns `sys_fields` (Ownership Map), instead of the loader opening the table; field DF-REF-105 and the three patterns are unchanged.
- Step 7: the staging object becomes one schema per service, `<schema>_next`; each service's swap runs only after the checks of all 19 services pass, one service at a time under the environment lock, so a refusal anywhere leaves every previous copy in use.
- Step 8: the load report gains one section per service, naming the service, the schema, the extract ID, the business date, the masking rule version, the rows per table and the check results.
- Step 9: the case record is read at `GET /api/recovery/case/v1/cases/{caseId}` (P3 rwb-case); the refusal of RW-REFADM with 403 and MSG-P4-002 is unchanged.
""",
"RWB-TE-006": """
**Realignment (D-RCV-60).** Epic RWB-PLT-LIB: RWB-PLT-TE006-CON and RWB-PLT-TE006-APP (wave 0), plus RWB-ITG-TE006-ITG (RWB-ITG-W1), release 30 November 2026 (tentative). The outbox, inbox and idempotency tables become library objects created in each service's own schema (Ownership Map: `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key`, owner PLT).

Delta, step by step:

- Step 1: OutboxWriter is the shared library call, and each service publishes into its own outbox inside its own transaction. The event types of EV-01 to EV-28 keep their names; on the wire they are `rwb.<short>.<Event>.v1` on the owner's topic (DP-14).
- Step 2: one `outbox_event` row and one `outbox_delivery` row per consumer, in the calling service's own schema. The Flyway migration is that service's own sequence (DP-15; H RWB-PLT-E1044-CON); the keys, the status check and the partial index are unchanged.
- Step 3 is unchanged: the change, the event and its deliveries commit together, now inside one service's schema.
- Step 4: JOB-11 is the outbox relay in every service, every minute, with no Quartz job (Ownership Map: JOB-11, PLT, no Temporal Schedule). The batch of 200, the row lock that skips held rows and the lowest open sequence per case and consumer are unchanged.
- Step 5: the consumer is another service reached on Kafka with a CloudEvents 1.0 header, and the inbox table `processed_event` answers the first-time question in place of a shared idempotency table. The stub consumer for the tests is unchanged.
- Steps 6 and 7: RETRY_SUCCEEDED and SYSTEM_UNAVAILABLE are published to `rwb.case.events.v1` and handled by rwb-case (P3); the retry ladder and the read of the delays on each attempt are unchanged.
- Step 8: RETRY_LIMIT_REACHED publishes the same case event, and the decision record is written by the calling service in its own schema through the local decision-record library, then published as DecisionRecorded to `rwb.decision-record.v1`; rwb-decision collects it into the central ledger (DP-03; RWB-PLT-E1027-CON). The one transaction of this step covers the delivery row, the record and the outbox row.
- Step 9: the admin endpoints read across services, so their owner after the split is Not specified in the source documents (CG-C-BNT-5; ASM-C-BNT-5). The rights, the page shape, 409 MSG-P2-022 and 404 are unchanged.
""",
"RWB-TE-007": """
> **Retired (D-RCV-60).** RWB-TE-007 is retired, as Template and Rules section R6 sets out: there is no new story, and every dependency on TE-007 points to RWB-PLT-E1071-CON. Quartz, its cluster job store and the shared job tables are replaced by Temporal Schedules in the owning service (Arch v5 slide 44). The nine steps stay in this document, word for word, so the as-built notes remain traceable; the table below gives the target for each step (ASM-C-BNT-1). The mechanism this section describes is out of date against Arch v5 slide 44 (CG-C-BNT-1).

| Step | v2 mechanism | Target under D-RCV-60 |
|---|---|---|
| 1 | DailyJobTrigger on LoadCompleted and on the completion of JOB-02 | AceDataReady (EV-26) starts DailyCaseRun in rwb-case; JOB-03 is a step of that run and JOB-04 an event-triggered workflow in rwb-source-data (Ownership Map: JOB-03 P3, JOB-04 P1) |
| 2 | JOB-05 Timer check every 5 minutes on cron in Asia/Bangkok | retired: durable timers inside each workflow, and no 5-minute timer check (Ownership Map: JOB-05, PLT) |
| 3 | Quartz cluster lock over one shared job store | one task queue per service, `rwb-<short>`, with the Schedule overlap policy that keeps one run at a time |
| 4 | job run log, JobRunRecorder.lastSucceeded, SKIPPED | the run record is the workflow history of the Schedule; a successful run for the business date answers the same question |
| 5 | dependsOn, WAITING and MSG-P3-031 | unchanged in intent, with the dependency an event or a completed child workflow |
| 6 | JobRunRecorder.start and finish, read on SCR-44 | workflow history of the Schedule plus the job monitor RWB-PLT-E1056-OPS; `/admin/jobs` in the owning service (DP-13) |
| 7 | CatchUpOnStart capped by `jobs.catch-up.max-dates` | the Schedule's catch-up window, capped the same way; the values come through the parameters contract of rwb-case (DP-06; H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON) |
| 8 | DeadlineWatcher at 07:00 | a second Schedule in rwb-case; the alert route RWB-PLT-E1056-OPS is unchanged |
| 9 | SCR-44 and `POST /admin/jobs/{jobId}/rerun` | per-service admin jobs endpoint under the owner's base (DP-13); 409 MSG-GEN-004, 403 MSG-P4-002 and 404 unchanged |
""",
"RWB-TE-008": """
**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, stories RWB-PLT-TE008-APP and RWB-ITG-TE008-ITG (RWB-ITG-W1), release 30 November 2026 (tentative). The check becomes a capability: one Temporal Schedule template in the workflow kit, one chain-check library in the service template, and one instance for the central ledger in rwb-decision (JOB-14: owner P7, mechanism Schedule, 02:00, Ownership Map).

Delta, step by step:

- Step 1: JOB-14 is a Temporal Schedule in rwb-decision, in namespace rwb-recovery on task queue rwb-decision; no Quartz table is written (DP-10; H RWB-PLT-E1071-CON).
- Step 2: the 01:00 copy is retired (RWB-E1-014 retired; Ownership Map: JOB-13 is continuous ingest on Kafka), so the run waits for the business date's ledger ingest to report complete instead of waiting for JOB-13. The latest start of 04:00 and the note on the run record are unchanged.
- Step 3: the end `chain_seq` is read per chain, inside the schema of the service whose instance runs; the central ledger's chain is read only through RWB-P7-E1008-CON (DP-01).
- Step 4: the canonical form is the shared local decision-record library (DP-03; RWB-PLT-E1027-CON), never a second copy.
- Step 5: the failing count and the first break are unchanged; the run reads one chain at a time and never writes to another service's table.
- Step 6: the run record is the workflow history of the Schedule, with the same fields (entries checked, last chain_seq, last entry_hash, result, first break, failing count), and not an ACE job run row.
- Steps 7 and 8: MSG-P7-007, MSG-P7-008 and MSG-P7-013 are unchanged, and a service with no chain instance is reported as not covered rather than intact.
- Step 9: the rerun is the Schedule's rerun under the owner's base, `/api/recovery/decision/v1/admin/jobs/{jobId}/rerun` (DP-13); a rerun is a new run, 409 MSG-GEN-004 and 403 MSG-P4-002 are unchanged.
""",
"RWB-TE-009": """
**Realignment (D-RCV-60).** Epic RWB-ITG-NFR, story RWB-ITG-TE009-ITG, release 31 December 2026 (tentative). Suggested owner: QA team (suggested; any team may pick up this story). The harness stays in `perf/recovery`, outside the service.

Delta, step by step:

- Steps 1 and 2 are unchanged: the release stage, the manual start by a squad member holding RW-TRIBE, the SIT lock, the refusal text and the 90 minute limit.
- Step 3: the open-case count is read at `GET /api/recovery/case/v1/cases` (P3 rwb-case); 23,600 open cases and the refusal text are unchanged.
- Step 4 is unchanged: the same roles and SIT test users, each calling through gateway-bff with the rights of its own role.
- Step 5: 410 virtual users, 10 ramp minutes, 60 steady minutes, 3 requests a minute and the MIX-2026.12 weights are unchanged; each call is one hop to the owner service with the 2 second timeout (DP-11). Which service owns each of the 7 operations of the mix is Not specified in the source documents (CG-C-BNT-3; ASM-C-BNT-3).
- Steps 6 to 8 are unchanged: per-operation percentiles, throughput and error rate over the steady hour, and the exclusive 2,000 ms and 1 percent limits.
- Step 9: the reload of the masked copy is the stage of RWB-PLT-TE004-APP, which loads the 19 schemas.
""",
"RWB-TE-010": """
**Realignment (D-RCV-60).** Epic RWB-ITG-NFR, story RWB-ITG-TE010-ITG, release 31 December 2026 (tentative). Suggested owner: QA team (suggested; any team may pick up this story).

Delta, step by step:

- Steps 1 to 9 are unchanged in intent: the stage, browsers.json, the sign-in per role, the six screens by their states by four browsers, the WCAG 2.1 A and AA scan in Thai and English, the keyboard check, the exception list, the single retry and the failing stage.
- The screens are composed by gateway-bff from the owner services (DP-19; H RWB-PLT-N001-CON), so a screen that calls a service base directly fails the front end build (RWB-PLT-TE001-APP-2).
- The MSG-P4-002 refusal on SCR-05 for RW-PHONECOL comes from rwb-access through the guard; the synthetic data set and the test users stay as v2 has them, in the stories of RWB-E1-065.
""",
"RWB-TE-011": """
**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, story RWB-PLT-TE011-APP, release 30 November 2026 (tentative). Suggested owner: TechX (suggested; any team may pick up this story).

Delta, step by step:

- Step 1: the personal field list is read from the `sys_fields` seed owned by rwb-source-data (P1, Ownership Map) and from the `x-personal-data: true` marking of the 19 service API files plus gateway-bff, instead of one specification. BR1 is unchanged.
- Step 2: the generated rules cover every service package `th.co.scb.ace.workbench.recovery.<short>` and the front end source; `pdpa-rules.yaml` and its six rules are unchanged.
- Steps 3 to 6 are unchanged, including the allow list approved by the TechX tech leads as code owners (RWB-TE-002).
- Step 7: the step runs in each repository's pull request build and on every build of main; the output format and the refusal to print a value found are unchanged.
""",
"RWB-TE-012": """
**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, story RWB-PLT-TE012-APP, release 30 November 2026 (tentative). The containers are used by rwb-document (P5) only, which owns `document`, `document_custody` and `retention_rule` (Ownership Map).

Delta, step by step:

- Step 1: the infrastructure template is unchanged and still creates `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` once per environment.
- Step 2: the Storage Blob Data Contributor role goes to the rwb-document managed identity (one login per service, DP-02) instead of a shared ACE service identity; SY-OCR and its three containers are unchanged, as are versioning, soft delete and the immutability policy.
- Step 3: StorageReadinessIndicator joins the rwb-document `/health` endpoint and reports ready only when the four containers and the `rwb-docs-legal` policy are present.
- Step 4: DocumentContainers and DocumentContainersConfig are published from rwb-document's `api` package; BlobStorageAdapter, the managed identity, the 10 second timeout and the blob name `{caseId}/{documentId}/v{docVersion}` are unchanged (DP-11, DP-02).
- Steps 5 and 6: WriteOnceViolationException, 409 MSG-P5-002 and ContentHashGuard are unchanged; the audit event for a refused overwrite goes through ACE Common.
- Step 7: SCR-44 and the platform administrator are unchanged; the readiness value is read from rwb-document.
""",
"RWB-TE-013": """
**Realignment (D-RCV-60).** Epic RWB-SVC-P10 rwb-agent, wave 1: RWB-P10-TE013-CON, RWB-P10-TE013-APP and RWB-P10-TE013-OPS, release 30 November 2026 (tentative), suggested owner TechX (TechX suggested; any team may pick up this story), with DevOps for the OPS story. The central ledger side is RWB-P7-TE013-APP (RWB-SVC-P7) and the integration copy is RWB-ITG-TE013-ITG (RWB-ITG-W1).

Delta, step by step:

- Step 1 is unchanged: the calling step works out its rule result first and brings it into the call (BR1).
- Step 2: AgentStepClient, AgentStepRequest, RuleResult and AgentStepOutcome are published from the rwb-agent `api` package, `th.co.scb.ace.workbench.recovery.agent.api`, and another service depends on that contract only (DP-20; C RWB-P10-TE013-CON).
- Steps 3 to 7 are unchanged in behaviour: autonomy mode, `timeout_seconds` and the 60 second wait, SHADOW and L1, and the fallback reasons TIMED_OUT and SCHEMA. `agent_policy` and `agent_run` belong to rwb-agent (P10, Ownership Map).
- Step 8: the calling service writes its decision record in its own schema through the local decision-record library and publishes DecisionRecorded to `rwb.decision-record.v1`; rwb-decision collects it into the central ledger within 5 minutes (DP-03; RWB-P7-TE013-APP is the ledger side). The migration becomes part of rwb-agent's own Flyway sequence and `agent_run` stays in rwb_agent (DP-15).
- Step 9 is unchanged: DecisionNotRecordedException, MSG-P7-003, R-UNI-39, and `agent_run.decision_log_id` left empty when the record cannot be written.
""",
}

# Split the source into front matter and sections.
m = re.search(r"^## RWB-TE-001 ", text, re.M)
assert m, "TE-001 heading not found"
body = text[m.start():]
head_old = text[:m.start()]

# Keep the v2 intro paragraph verbatim from the old head.
old_intro = [l for l in head_old.splitlines() if l.startswith("Every flow step of every story")]
assert old_intro, "intro paragraph not found"
assert old_intro[0] == INTRO, "intro paragraph differs from the expected v2 text"

# Mark the one release date inside the preserved text as tentative (rule 10).
old_rel = "which is E1 for the 30 November 2026 release"
assert body.count(old_rel) == 1
body = body.replace(old_rel, "which is E1 for the 30 November 2026 release (tentative)")

# Insert each delta block after the Module line of its section.
parts = re.split(r"(?m)^(## RWB-TE-\d{3} .*)$", body)
out = [parts[0]]
i = 1
while i < len(parts):
    heading, chunk = parts[i], parts[i + 1]
    key = heading.split()[1]
    assert key in DELTA, key
    lines = chunk.split("\n")
    # line 0 is the rest of the heading line; find the Module line
    idx = next(n for n, l in enumerate(lines) if l.startswith("Module: "))
    assert lines[idx + 1] == ""
    block = DELTA[key].strip("\n").split("\n")
    lines = lines[:idx + 2] + block + [""] + lines[idx + 2:]
    out.append(heading)
    out.append("\n".join(lines))
    i += 2
new_body = "".join(out)

result = FRONT + INTRO + "\n\n" + new_body
OUT.write_text(result, encoding="utf-8", newline="\n")
print("wrote", OUT)
print("lines", result.count("\n") + 1, "chars", len(result))
print("sections", len(re.findall(r"(?m)^## RWB-TE-", result)))
print("deltas", result.count("**Realignment (D-RCV-60).**"))
