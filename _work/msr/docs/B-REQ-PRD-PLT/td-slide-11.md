
Runtime view: what runs where

Each of the 19 Recovery services has the same shape: its own Temporal worker and queue, an embedded Drools engine, its own schema

Officer / approver
Workbench screens

ONE RECOVERY SERVICE  (e.g. rwb-treatment; all 19 alike)

API
start case, approve

Temporal worker
polls rwb-treatment only

Drools engine
RuleEvaluator, model cache

Activities
EvaluateRules · RecordAndApply

Own schema
state + decision record

Outbox
→ Kafka

TEMPORAL CLUSTER  (shared, one per environment)

Frontend + history
remembers every step

own
persistence DB

Namespace rwb-recovery
one queue per service: rwb-case, rwb-treatment … (19)

ace-collection
Nexus: calculator

RULE GOVERNANCE  (rwb-decision, P7)

Rule models + central ledger
approve, publish EV-30 · seal decision records

1 click

2 poll queue

3 run step

4 ask

5 save

same transaction

Key

Temporal (runs)

Drools (decides)

People / approval

Data and log

ACE

Outside

Temporal remembers and waits; Drools answers inside a step; each service keeps its own state and decision records.

11

Notes: C4 container view, aligned to Recovery Microservice Architecture v5: Recovery stays part of ACE and is cut into 19 services, one per module (P1 to P10, S1 to S9). The slide shows one of them (for example rwb-treatment); all 19 have this shape. Each service packages its own Temporal worker and the embedded Drools runtime (KIE libraries only: drools-engine, drools-mvel, drools-decisiontables, drools-xml-support; no KIE Server, no Business Central, no KJAR - T3).

Temporal: one shared cluster per environment on ACE AKS with its own persistence database (no grant on the ACE database). Namespace rwb-recovery with one task queue per service (rwb-case, rwb-treatment, rwb-litigation and so on); each service's worker polls only its own queue and KEDA scales workers on backlog. ace-collection is ACE's namespace, reached through Nexus (for example the restructure calculator). Version 1.30+ for Nexus and Worker Versioning.

Data: the ACE PostgreSQL server, one schema and one login per service (rwb_<service>); no cross-schema joins. Temporal holds no case of record (T1). Payloads encrypted by the codec (AES-GCM, keys in Key Vault per namespace). Temporal UI behind Entra ID; RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode (break-glass).

One transaction: the service writes its state change, the decision record and the outbox row together. The outbox relay publishes to Kafka (rwb.<service>.events.v1 and rwb.decision-record.v1).

Rules: rwb-decision (P7) governs rule models (author, test, four-eyes approval, effective date) and keeps the central decision ledger. The owning service loads a version on RulePackageInForce (EV-30, on Kafka), verifies the checksum, swaps atomically and keeps the last good model on failure (cache max 20).

