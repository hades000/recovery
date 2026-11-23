"""Write the candidate gap and assumption rows for WP B-TECH-05 (one JSON object per line)."""
import json
from pathlib import Path

GAPS = [
 dict(title="Environment names for per-service deployment",
  source="05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx; Recovery Workbench Architecture v5 Text Extract v1; Recovery Workbench Microservice Ownership Map v1",
  section="2. Environments; 3. What runs in each environment (Temporal server); 3.2 Per-service deployment; 6.1 Environment parameters",
  description="Version 4 names four environments (DEV, SIT, UAT and PROD) for one service and leaves one environment token unresolved: the parameter temporal.target reads rwb-temporal-frontend.{env}.svc.cluster.local:7233. Architecture v5 turns that service into 19 services, each with an API deployment and a worker deployment in each environment, but no source gives the name a service or its two deployments take inside an environment: the Helm release name, the Kubernetes deployment names and the DNS name. No source says either whether the token {env} resolves to one value per environment or to a different value for each service and environment. Version 5 keeps the four environment names, keeps {env} character for character, and adds no per-service name.",
  evidence="Environment and Deployment Design v4 section 2: 'DEV | Build and developer testing | Synthetic only | On every merge into main | Squads' and the other three rows. Section 3 Temporal server row: 'Official Temporal Helm chart, Helm release rwb-temporal in the ACE namespace, one cluster per environment on the ACE AKS clusters'. Section 6.1: 'temporal.target | rwb-temporal-frontend.{env}.svc.cluster.local:7233 | Temporal worker and WorkflowGateway'. Architecture v5 slide 8: 'RECOVERY · 19 SERVICES · namespace rwb-recovery' and slide 8 notes: '19 services in the rwb-recovery namespace, each an api and a worker deployment'. Architecture v5 slide 33 notes: 'an API deployment (2 pods for availability, scaled on CPU or requests if ever needed) and a worker deployment scaled by KEDA'. Ownership Map v1, sheet Services, columns Code, Service, Name, Wave, Schema, REST base, Topic, Queue.",
  type="Missing", area="Infrastructure", severity="P2", needed_by_wave="0", legacy_ref="",
  owner_role="SCB IT infrastructure lead", asm="ASM-B-TECH-05-2",
  proposed="Fix one naming convention with SCB IT and the ACE platform team: a Helm release per service, a deployment name for the API part and one for the worker part, a service DNS name, and the value of {env} for each of DEV, SIT, UAT and PROD. Record the convention in this document and in the service template specification, and apply it to the 19 services before the wave 1 infrastructure story is accepted."),

 dict(title="Kubernetes namespace of the 19 services against the namespace of the Temporal release",
  source="05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx; Recovery Workbench Architecture v5 Text Extract v1; Recovery Workbench Temporal and Drools Design Text Extract v1",
  section="1. The design on one page; 3. What runs in each environment; 3.1 Temporal platform",
  description="Version 4 puts the single recovery service in the ACE namespace and installs the Temporal chart as Helm release rwb-temporal in the ACE namespace. Architecture v5 draws the 19 services in a Kubernetes namespace named rwb-recovery, and the Temporal and Drools design repeats that placement. The two sources do not settle whether the Recovery services leave the ACE namespace, whether rwb-recovery is the only new namespace, or whether the Temporal release stays in the ACE namespace next to the services it serves. Version 5 places the 19 services in rwb-recovery and keeps the Temporal release in the ACE namespace exactly as version 4 records it, and raises the placement as a gap.",
  evidence="Environment and Deployment Design v4 section 1: 'The ACE service on the shared ACE AKS clusters'. Section 3 Service row: 'The ACE Spring Boot service with the recovery module, in the ACE namespace'. Section 3 Temporal server row: 'Helm release rwb-temporal in the ACE namespace'. Architecture v5 slide 8: 'ACE AKS CLUSTER · SHARED' with 'RECOVERY · 19 SERVICES · namespace rwb-recovery'. Architecture v5 slide 8 notes: '19 services in the rwb-recovery namespace'. Temporal and Drools design slide 20 notes: 'Production: official Helm chart on ACE AKS with mTLS (README), Temporal 1.30+'. Neither source states the namespace of the Temporal release under the 19-service split.",
  type="Conflict", area="Infrastructure", severity="P2", needed_by_wave="0", legacy_ref="",
  owner_role="SCB IT infrastructure lead", asm="ASM-B-TECH-05-3",
  proposed="Agree the namespace layout with the ACE platform team: one rwb-recovery namespace for the 19 services and their deployments, and either the same namespace or a platform namespace for the rwb-temporal Helm release. Record the choice in this document, in the service template and in the Helm chart values of the release."),

 dict(title="Temporal server is pinned at 1.28.1 but Nexus and Worker Versioning need 1.30 or later",
  source="05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx; Recovery Workbench Architecture v5 Text Extract v1; Recovery Workbench Temporal and Drools Design Text Extract v1",
  section="3. What runs in each environment (Temporal server); 3.1 Temporal platform",
  description="Version 4 records Temporal server 1.28.1 and Temporal Java SDK 1.31.0 as the versions SCB IT approved, and every version change as a platform change under the release process. Architecture v5 and the Temporal and Drools design both require 1.30 or later, because Nexus and Worker Versioning do not exist in 1.28.1, and Architecture v5 lists the upgrade from 1.28.1 as a Wave 0 action. No source states which version is approved for the target, so version 5 keeps 1.28.1 as recorded and states that the two features are not used in the Epic 1 and Epic 2 scope. A decision is needed before a workflow uses Nexus, which includes the restructure calculator call into ace-collection, or before Worker Versioning is required for a release.",
  evidence="Environment and Deployment Design v4 section 3 Temporal server row: 'Server and Java SDK versions are pinned to the SCB IT approved release: Temporal server 1.28.1 and Temporal Java SDK 1.31.0'. Section 3.1: 'a change of either version is a platform change under the release process'. Architecture v5 slide 23 note: 'Upgrade from 1.28.1 to 1.30 or later for Nexus and Worker Versioning'. Architecture v5 slide 31 risks: 'Temporal upgrade from 1.28.1 | No Nexus, no Worker Versioning | Upgrade to 1.30+ in Wave 0'. Temporal and Drools design slide 1 and slide 20 notes: 'Version 1.30+ for Nexus and Worker Versioning' and 'Temporal 1.30+'. Risks and Assumptions v4 row R-18 keeps the version approval open.",
  type="Conflict", area="Platform", severity="P2", needed_by_wave="0", legacy_ref="",
  owner_role="SCB IT architecture", asm="ASM-B-TECH-05-6",
  proposed="Submit the version list for approval again and pin the approved 1.30 or later server and its matching Java SDK in Wave 0, with the upgrade tested in SIT as a one-minor-version upgrade. Until the approval lands, keep 1.28.1 and keep every Nexus call, including the restructure calculator, out of the scope of a release."),

 dict(title="The 19 database logins and the per-service connection budget are not named",
  source="05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx; Recovery Workbench Architecture v5 Text Extract v1",
  section="3. What runs in each environment (ACE read role); 5. Database changes",
  description="Version 4 names two database roles only: recovery_svc, the single recovery service login, and ace_view_owner, the NOLOGIN role that owns the views. Architecture v5 requires 19 schemas and 19 logins on the ACE PostgreSQL server with a connection budget per service and no cross-schema access, and asks the ACE team and the DBA for it. No source gives the login names, the naming rule for them, the size of a connection pool per service or the total connection budget, so version 5 keeps recovery_svc as the login of rwb-source-data, because the ACE Source Views v1 grants name that role, and leaves the other 18 logins and every pool size unset.",
  evidence="Environment and Deployment Design v4 section 3 ACE read role row: 'recovery_svc, the recovery service role: SELECT on recovery.v_ace_* only, no direct public read, no write. ace_view_owner: a NOLOGIN ACE role'. Section 3 Temporal persistence row: 'owned by temporal_svc'. Architecture v5 slide 8: '19 Recovery schemas, one login and connection pool each'. Architecture v5 slide 39 decision 2: '19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access | Owner: ACE team, DBA'. Architecture v5 slide 33 notes: 'The ACE database sees capped pools per service.'",
  type="Missing", area="Platform", severity="P2", needed_by_wave="0", legacy_ref="",
  owner_role="ACE team, DBA", asm="ASM-B-TECH-05-5",
  proposed="Have the DBA fix the login name per schema, the pool size per service and the total connection budget, and add them to this document and to the ACE DB story of each service. Keep recovery_svc as the name of the rwb-source-data login so that the ACE Source Views v1 grants stay valid, and state the rule for the other 18 names."),

 dict(title="Per-service CPU, memory and autoscaling thresholds are not stated",
  source="05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx; Recovery Workbench Architecture v5 Text Extract v1",
  section="3.2 Per-service deployment; 7. Resilience and recovery",
  description="Version 4 gives no sizing at all, because one service ran on the ACE pattern. Architecture v5 gives the shape of the two deployments, 2 pods for the API part and KEDA scaling of the worker part on the task-queue backlog or consumer lag down to zero, and names the bursty services (document OCR and agent runs), but it gives no CPU or memory request and limit, no KEDA threshold, no maximum replica count and no pod disruption budget for any of the 19 services. Version 5 therefore states the shape and the count of deployments and leaves every figure unset; a worker that can scale to zero and an API part that must keep 2 pods also need a stated minimum and maximum per environment.",
  evidence="Environment and Deployment Design v4 section 7: 'Availability | 99.9% in business hours | Proposed, DL11'. Architecture v5 slide 33 notes: 'an API deployment (2 pods for availability, scaled on CPU or requests if ever needed) and a worker deployment scaled by KEDA on the Temporal task-queue backlog or Kafka consumer lag, down to zero for bursty work such as OCR or agent runs'. Architecture v5 slide 4: 'api + worker deployment'. No source gives a request, a limit, a threshold or a replica maximum.",
  type="Missing", area="Infrastructure", severity="P3", needed_by_wave="1", legacy_ref="",
  owner_role="SCB IT infrastructure lead", asm="ASM-B-TECH-05-4",
  proposed="Set the request and limit, the KEDA threshold and the replica minimum and maximum for the API part and the worker part of each service from the volume forecast, starting with the bursty services rwb-document, rwb-agent, rwb-case and rwb-payment, and record them in the Helm values and in the infrastructure story of each service."),

 dict(title="Kafka cluster ownership, sizing and the Event Hubs fallback are not decided",
  source="Recovery Workbench Architecture v5 Text Extract v1; 05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx",
  section="3. What runs in each environment (Kafka); 1. The design on one page",
  description="Version 4 has no Kafka row at all, because the design then used an outbox without a broker. Architecture v5 makes Kafka the event broker, gives the topic settings of every service topic (12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, retry 1 min, 10 min, 1 h then .dlt) and names Azure Event Hubs Premium as the fallback, but leaves the owner and the sizing of the cluster open, and the architecture team's first decision is exactly that: whether Recovery's topics sit on the bank Kafka platform ACE already uses. Version 5 states the topic settings and the fallback, and adds no owner beyond the roles Architecture v5 names.",
  evidence="Architecture v5 slide 9 notes: 'Kafka: topic per service rwb.<name>.events.v1, 12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, outbox and inbox, retry 1 min, 10 min, 1 h then .dlt; Event Hubs Premium is the fallback.' Architecture v5 slide 39 decision 1: 'Host Recovery's business-event topics on the bank Kafka platform ACE already uses (separate topics and ACLs from PII logging); fallback: Azure Event Hubs Kafka endpoint | Owner: Enterprise Architecture, ACE platform team'. Environment and Deployment Design v4 section 3: no Kafka row.",
  type="Missing", area="Infrastructure", severity="P1", needed_by_wave="0", legacy_ref="",
  owner_role="SCB IT infrastructure lead", asm="",
  proposed="Close Architecture v5 decision 1 in Wave 0: name the cluster that hosts the 19 service topics and rwb.decision-record.v1, its capacity and its retention, the team that runs it, the ACL model, and the trigger for the Event Hubs fallback. Record the answer in this document and in the event and messaging design."),

 dict(title="The shared Quartz tables are either kept by Epic 1 and Epic 2 or no longer used",
  source="05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx; Recovery Workbench Architecture v5 Text Extract v1; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
  section="3. What runs in each environment (Scheduler); 6. Feature flags",
  description="Version 4 keeps Quartz for the Epic 1 and Epic 2 scheduled jobs, keeps Spring Batch for their automated chains, and states that the Workbench adds no qrtz_ or batch tables and shares ACE's existing Quartz and Spring Batch tables. Architecture v5 says that the ACE shared Quartz and batch tables are no longer used by Recovery, because every job becomes a Temporal Schedule or an event-started workflow in the owning service, while the decision log and the ADR keep Quartz and the TimerScheduler port for Epic 1 and Epic 2 and the Ownership Map keeps JOB-05 as a timer check behind that port with no Temporal Schedule. The two positions can both be true only if the Epic 1 and Epic 2 jobs stay on the shared tables until their delta stories move them, and no source states that cut-over point. Version 5 keeps the built behaviour and states that the new services add no qrtz_ or batch tables.",
  evidence="Environment and Deployment Design v4 section 3 Scheduler row: 'Quartz for Epic 1 and Epic 2 scheduled jobs, and Spring Batch for their automated chains ... JOB-05 timer check runs on Quartz behind the TimerScheduler port ... The Workbench adds no qrtz_ or batch tables and shares ACE's existing Quartz and Spring Batch tables'. Architecture v5 slide 44: 'No shared Quartz tables: a Temporal Schedule or event-started workflow in the owning service; bank Airflow triggers the edges'. Architecture v5 slide 44 notes: 'The ACE shared Quartz and batch tables are no longer used by Recovery.' Decision Log v10 D-RCV-36 T2 and ADR-011 keep Quartz and the TimerScheduler port for Epic 1 and Epic 2. Ownership Map v1, sheet Jobs, JOB-05.",
  type="Conflict", area="Platform", severity="P2", needed_by_wave="1", legacy_ref="",
  owner_role="Solution architect", asm="ASM-B-TECH-05-7",
  proposed="State the cut-over in the scheduling design: which Epic 1 and Epic 2 jobs stay on the shared Quartz and Spring Batch tables, on which release they move to a Temporal Schedule or an event-started workflow, and who runs the shared tables once Recovery stops using them. Keep the TimerScheduler port until the JOB-05 delta story is accepted."),
]

ASMS = [
 dict(text="Recovery Workbench Environment and Deployment Design v5 is issued in Draft status with no approval recorded.",
  why="This run is the D-RCV-60 realignment: no human approval step is available, the run must not stop for one, and the overlay records the missing status as an assumption.",
  read="Every environment, deployment, pipeline gate, feature flag and parameter of v5 may be cited by the architecture, infrastructure and story documents of this run as the deployment design, with Draft status, and the approval is recorded afterwards by the owner of the architecture set.",
  gap="", applied_in="Metadata table, Status row", confidence="High",
  confirm="Solution architect", impact="An infrastructure or DevOps story that cites this document cites a document in Draft status until the approval is recorded."),

 dict(text="The four environment names stay DEV, SIT, UAT and PROD and the token {env} in temporal.target stays exactly as version 4 writes it; the per-service names inside an environment are left unset.",
  why="Architecture v5 adds the 19 services but names no environment, release or DNS name for any of them, and inventing a naming convention would put values in the deployment design that no source supports. The four names and the token are the values version 4 records.",
  read="Section 2 keeps the four rows and states that each of the 19 services is deployed in all four; section 6.1 keeps rwb-temporal-frontend.{env}.svc.cluster.local:7233 unchanged and records that no source resolves the token for a service. The placeholder is written where a per-service name would go.",
  gap="CG-B-TECH-05-1", applied_in="Section 2; section 3.2; section 6.1", confidence="High",
  confirm="SCB IT infrastructure lead", impact="Until the convention is fixed, an infrastructure story cannot name the Helm release, deployment or DNS record it creates, and the 19 services cannot be released to an environment under a fixed name."),

 dict(text="The 19 services are placed in one Kubernetes namespace named rwb-recovery in each environment, and the Temporal Helm release rwb-temporal stays in the ACE namespace as version 4 records it.",
  why="Architecture v5 draws the services in rwb-recovery and version 4 installs the Temporal release in the ACE namespace; neither source moves the other, so the two statements are kept side by side and the layout is raised as a gap.",
  read="Section 3 Services row and section 3.2 place the 19 services in rwb-recovery; section 3 Temporal server row and section 3.1 keep the release in the ACE namespace. Section 3 adds a paragraph that states the conflict and the placeholder.",
  gap="CG-B-TECH-05-2", applied_in="Section 1; section 3; section 3.1; section 3.2", confidence="Medium",
  confirm="ACE platform team", impact="If the services stay in the ACE namespace, the namespace row of every deployment, the network policy and the Helm values of the release change; if Temporal moves, the DNS name in temporal.target and the mTLS certificates change."),

 dict(text="Each service keeps the two-part shape of Architecture v5: an API deployment of 2 pods for availability and one worker deployment scaled by KEDA on the task-queue backlog or consumer lag, down to zero for bursty work; the estate is about 38 small deployments at rest.",
  why="Architecture v5 slides 8 and 33 give the two-part shape, the 2 pods and the KEDA scaling, and slide 33 counts about 38 small deployments for the 19 services. Version 4 has one deployment and no shape at all.",
  read="Section 3 Services row and section 3.2 state the shape, the 2 pods, the KEDA scaling and the count; no CPU, memory, threshold or replica maximum is written, and section 3.2 says so.",
  gap="CG-B-TECH-05-5", applied_in="Section 3 Services row; section 3.2 table", confidence="High",
  confirm="SCB IT infrastructure lead", impact="An infrastructure story can create the two deployments but cannot size them until the resources are agreed."),

 dict(text="One login per service, and recovery_svc stays the name of the rwb-source-data login because the ACE Source Views v1 grants use that role name; ace_view_owner and temporal_svc keep their names and grants.",
  why="Architecture v5 requires 19 logins but gives no names. recovery_svc, ace_view_owner and temporal_svc are the three role names the sources fix, and the ACE Source Views v1 script tells the reader to replace :recovery_role with the name fixed in this document, so renaming it would break the grants the views already use.",
  read="Section 3 ACE read role row, section 5 and section 3 Temporal grants row keep the three names and their grants, and state that the other 18 logins and their pool sizes are not specified.",
  gap="CG-B-TECH-05-4", applied_in="Section 3 ACE read role row; section 5 database changes", confidence="Medium",
  confirm="ACE team, DBA", impact="If the DBA renames recovery_svc, the Section A migration, the view conformance test and every connection string of rwb-source-data change with it."),

 dict(text="Temporal server 1.28.1 and Java SDK 1.31.0 stay the recorded versions until SCB IT approves a later release; Nexus and Worker Versioning are not used in the Epic 1 and Epic 2 scope.",
  why="Version 4 records 1.28.1 as the approved release and calls any version change a platform change, while Architecture v5 and the Temporal and Drools design need 1.30 or later for Nexus and Worker Versioning. No approved 1.30 version exists in the sources, so the recorded version is kept and the conflict is raised.",
  read="Section 3 Temporal server row, section 3.1 (two paragraphs on versions) and section 9 keep 1.28.1 and 1.31.0 and state the 1.30 floor and the features that are out of scope until the approval.",
  gap="CG-B-TECH-05-3", applied_in="Section 3 Temporal server row; section 3.1; section 9", confidence="Medium",
  confirm="SCB IT architecture", impact="A workflow that needs Nexus, including the restructure calculator call into ace-collection, cannot be built against the pinned server; if the upgrade slips, that integration waits."),

 dict(text="The new services add no Quartz or Spring Batch tables; the Epic 1 and Epic 2 jobs stay on the ACE shared Quartz and Spring Batch tables behind the TimerScheduler port until their own delta stories move them to a Temporal Schedule or an event-started workflow.",
  why="Version 4 keeps Quartz and Spring Batch for Epic 1 and Epic 2, while Architecture v5 retires the shared tables. The preservation rule keeps the built behaviour until a delta story changes it, and the Ownership Map keeps JOB-05 as a timer check with no Temporal Schedule, so both statements hold only with this cut-over.",
  read="Section 3 Scheduler row states both, names the 17 jobs that become a Schedule or an event-started workflow in the owning service, and section 9 records the change. No cut-over date is written.",
  gap="CG-B-TECH-05-7", applied_in="Section 3 Scheduler row; section 9", confidence="Medium",
  confirm="Solution architect", impact="Until the cut-over is stated, the operations run book does not know which jobs still need the ACE Quartz tables, and a decommission of those tables would break JOB-05 and the Epic 1 and Epic 2 chains."),

 dict(text="Every service owner is the owning service itself, taken row by row from the Microservice Ownership Map v1 (sheet Services), and every shared platform row names the role that Architecture v5 slide 39 or the source row names.",
  why="The Work Package requires the Ownership Map for every owner, and the map gives a code, a service, a wave, a schema, a REST base, a topic and a queue per service but no team. Architecture v5 slide 39 names the owner of each platform decision, and version 4 names the role of each shared row.",
  read="Section 3.2 has one row per service from the map; the paragraph after the section 3 table names the Kafka, Temporal, database and document owners with their basis; no person is named anywhere.",
  gap="", applied_in="Section 3.2; owners paragraph after section 3", confidence="High",
  confirm="Delivery lead", impact="Ownership is a suggestion only, per user decision U3; any team may pick up a story, and no story changes owner because of this document."),

 dict(text="No release date is written in version 5; the monthly production release window is the only cadence, and any date added later is tentative.",
  why="User decision U7 keeps dates unchanged and tentative and forbids raising a date as a gap. The four environment rows and the release rows of version 4 carry no calendar date, so none is added.",
  read="The paragraph after the metadata table and section 4.2 state the cadence and the tentative rule; section 2 keeps the v4 wording of the Deployed column.",
  gap="", applied_in="Metadata paragraph; section 4.2", confidence="High",
  confirm="Delivery lead", impact="A release plan that needs a date takes the monthly window as the cadence and marks every date it writes tentative."),

 dict(text="Each of the 19 services releases on its own tag, and gateway-bff releases with the services whose screens it composes; the monthly production window is shared with the collection squad.",
  why="Architecture v5 states that each service can be released, scaled, reused or replaced on its own, and version 4 keeps one production release at each month end shared with the collection squad. The two are combined so that the window stays and the unit of release becomes the service.",
  read="Section 1 Release row, section 4.2 Per-service release and Deploy to PROD rows state the per-service tag and the monthly window.",
  gap="", applied_in="Section 1 Release row; section 4.2", confidence="Medium",
  confirm="Release owner in the ACE team", impact="A release note that names one Workbench release no longer matches the pipeline; each release note lists the services it contains."),
]

for name, rows in (("gaps", GAPS), ("assumptions", ASMS)):
    p = Path("_work/msr") / name / "B-TECH-05.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for i, r in enumerate(rows, 1):
            r = dict(id=f"{'CG' if name == 'gaps' else 'ASM'}-B-TECH-05-{i}", **r, wp="B-TECH-05")
            order = (["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
                      "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"] if name == "gaps"
                     else ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"])
            f.write(json.dumps({k: r.get(k, "") for k in order}, ensure_ascii=False) + "\n")
    print("WROTE", p, len(rows), "rows")
