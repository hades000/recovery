
Temporal in five layers: Recovery owns the top two, the platform the rest

The bottom layers are owned once by the platform team and reused by every workbench

L5

Domain workflows
CaseWorkflow + stage children: Treatment, Litigation, Debt sale …

each service team

L4

Activity contracts per service
on rwb-<svc>: EvaluateRules, RecordAndApply, Payment.postProceeds · Nexus

each service team

L3

Workflow kit (versioned library)
Approval · Human task with SLA · Saga runner · Scheduled job · Notify · Partner instruction

platform team

L2

Namespaces
ace-collection · rwb-recovery · next workbench: own quotas, certs, keys

platform team

L1

Temporal cluster
one per environment on ACE AKS · own DB · UI · codec server · 1.30+

platform team

Recovery-specific above · shared platform, owned once, below

WHERE S1–S9 USE THE KIT

Approval (DoA)

S1 route · S2, S3, S5–S7 approvals

Human task with SLA

every officer task and escalation

Saga runner

S2 settlement · S5 auction · S6 · S7

Scheduled job

JOB-16 write-off scan · overnight jobs

Partner instruction

law firms, vendors, agencies (S4, S5, S9)

WHERE DROOLS SITS

Inside L4 activities of the owning service, never in workflow code.
Rule models are governed once in rwb-decision and copied to each owner.

Another workbench gets a namespace and the kit, and writes only its own domain workflows.

12

Notes: From Recovery Microservice Architecture v5, slide 23.
L1 cluster: one Temporal cluster per environment on ACE AKS, own persistence database, UI, metrics and codec server; upgrade to 1.30 or later for Nexus and Worker Versioning.
L2 namespaces: one per workbench (ace-collection, rwb-recovery, the next one), each with its own retention, rate limits, certificates and encryption keys.
L3 workflow kit: a versioned library of generic templates with no business terms in their interfaces: Approval (maker-checker, DoA lookup as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job, Partner instruction.
L4 activity contracts: each service publishes typed activity interfaces on its queue rwb-<service>, plus Nexus endpoints for callers in other namespaces. EvaluateRules and RecordAndApply live here, in the service that owns the decision.
L5 domain workflows: CaseWorkflow and the stage workflows.

How S1 to S9 use the kit: Approval for route approval (S1), DoA approvals (S2, S3, S5, S6, S7) and rule sign-off; Human task with SLA for every officer task; Saga runner for settlement and deed in lieu (S2), auction (S5), debt sale (S6) and write-off posting (S7); Scheduled job for JOB-16 write-off scan (S7) and the overnight jobs; Partner instruction for law firms, auction vendors and agencies (S4, S5, S9); Agent run with rule fallback for the route agent and pricing agent (R-UNI-32).

