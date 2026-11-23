
Temporal at runtime: one cluster, a namespace per workbench, a queue per service

Workers run inside each service and poll only their own queue; the numbers show four typical calls

TEMPORAL CLUSTER · SHARED, ONE PER ENVIRONMENT (L1)

ace-collection (L2)

ace-case

ace-collect

ace-notify

Nexus handler
restructure.calculate

rwb-recovery (L2) · one task queue per service

rwb-case

rwb-litigation

rwb-partner

rwb-decision

rwb-treatment

rwb-valuation

rwb-guarantee

rwb-deviation

rwb-asset

rwb-debtsale

rwb-writeoff

rwb-payment

rwb-document

rwb-comms

rwb-integration

rwb-agent

rwb-source-data

rwb-reporting

rwb-access

1

2

3

4

Workers live in each service's worker deployment and poll only their own queue; KEDA scales them on backlog.

Codec (AES-GCM, Key Vault) on every client and worker; codec server for the UI.

1

Child workflow
CaseWorkflow starts LitigationWorkflow on rwb-litigation

2

Activity
Litigation calls Partner.issueInstruction on rwb-partner

3

Nexus operation
Treatment calls ACE's restructure calculator across namespaces

4

Signal from an event
PaymentMissed → case router → signalWithStart CaseWorkflow

One cluster, isolated namespaces, one queue per service: a service is reusable through its queue and contract, not its code.

24

Notes: Each Recovery service runs its own Temporal worker in its worker deployment, polling only task queue rwb-<service> in namespace rwb-recovery. KEDA's Temporal scaler adds workers when the queue backlog grows and can scale bursty queues (document OCR, agent runs) to zero.

(1) Child workflow: CaseWorkflow on rwb-case starts LitigationWorkflow on rwb-litigation (parent close policy ABANDON, so the stage survives the parent's Continue-As-New). (2) Activity: LitigationWorkflow calls Partner.issueInstruction on rwb-partner; the worker of rwb-partner executes it and writes its own schema. (3) Nexus: TreatmentWorkflow calls the restructure calculator as a Nexus operation exposed by ace-collection; the namespaces stay isolated. (4) Signal: a Kafka event (PaymentMissed) reaches rwb-case's case router, which uses signalWithStart on the CaseWorkflow.

Data converter: every client and worker uses the payload codec (AES-GCM, keys in Key Vault per namespace); the codec server lets authorised staff read payloads in the Temporal UI.

