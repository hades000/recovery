
Temporal in five layers: the bottom four are reusable by any workbench

Platform layers are owned once; each workbench writes only its own domain workflows

L5

Domain workflows
CaseWorkflow (rwb-case) · RouteDecision, Treatment, Litigation, AssetDisposal, DebtSale, WriteOff, Deviation

each service team

L4

Service activity contracts
Typed interface per service on queue rwb-<svc>, e.g. Payment.postProceeds, Partner.issueInstruction · Nexus endpoints

each service team

L3

Workflow kit (versioned library)
Approval (maker-checker, DoA) · Notify · Document intake · Agent run + fallback · Human task with SLA · Saga runner · Scheduled job · Partner instruction

platform team

L2

Namespaces
ace-collection · rwb-recovery · next workbench: own retention, quotas, certificates and codec keys

platform team

L1

Temporal cluster
One per environment on ACE AKS; own persistence DB; UI, metrics, codec server; version 1.30+

platform team

ANOTHER WORKBENCH REUSES IT IN FOUR STEPS

1

Get a namespace
platform team sets quotas, certificates and keys

2

Add the workflow kit
e.g. Approval with its own DoA table

3

Call existing services
activity contracts or Nexus, e.g. rwb-comms notice, rwb-document intake

4

Write only its domain workflows
everything below L5 is reused

Rules that keep it reusable
No business terms in L1-L3 interfaces
Kit versioned; workers pinned (Worker Versioning)
All I/O in activities; Continue-As-New at stage ends
Payloads encrypted by the codec (AES-GCM)

green = Recovery-specific (L5, and L4 contracts owned by each service)   blue = shared platform, owned once

A new workbench gets a namespace and composes the kit and existing services: it writes only its own domain workflows.

23

Notes: L1 cluster: one Temporal cluster per environment on the ACE AKS cluster, with its own persistence database, UI, metrics and codec server; operated by the platform team. Upgrade from 1.28.1 to 1.30 or later for Nexus and Worker Versioning.

L2 namespaces: one per workbench (ace-collection, rwb-recovery, and the next one). Namespaces isolate retention, rate limits, certificates and encryption keys. A new workbench is a new namespace, not a new cluster.

L3 workflow kit: a versioned library (semantic versioning) of generic workflow templates with no business terms in their interfaces: Approval (maker-checker, DoA lookup as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job, Partner instruction. Owned by the platform team; ACE can use it too.

L4 activity contracts: every service publishes a contract jar with typed activity interfaces on its task queue rwb-<service>, plus Nexus endpoints for callers in other namespaces. This is what makes a service reusable through Temporal.

L5 domain workflows: CaseWorkflow in rwb-case and stage workflows in the route services; specific to Recovery.

Rules for all layers: deterministic workflow code; all I/O in activities; Continue-As-New at stage ends and at least every 28 days; Worker Versioning for safe upgrades; payload codec AES-GCM.

