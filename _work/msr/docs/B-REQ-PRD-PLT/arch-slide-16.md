
Service contracts 3/7 · Agent, integration, document

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET /agent-runs/{id} · GET/POST /agent-policies (admin)
EVT  DocumentStored (intake) · CaseCreated (screening)
TMP  AgentRunWorkflow: 60 s, then rule result · Tool gateway: read-only calls for the agent

DB  writes schema rwb_agent: agent policies, prompts, runs, guardrails, evaluations
EVT  rwb.agent.events.v1: AgentRunCompleted
REST  Source data: tool: read case facts · Document: tool: read extracted fields · Enterprise AI endpoint: HTTPS private endpoint

P10 · rwb-agent
Agent runtime
queue rwb-agent
rwb.agent.events.v1

IN

OUT

REST  GET /interface-runs (operations) · POST /interface-runs/{id}/retry
EVT  (none: called as a task)
TMP  Act: deliverFile(manifest), receiveFile · Airflow window: WIN file 16:00, buyer files per lot

DB  writes schema rwb_integration: interface config, file runs, outbound items, ACE integration paths
EVT  rwb.integration.events.v1: FileDelivered, FileFailed
REST  Document: fetch file by ID (SAS link)
FILE  WIN (registered mail): daily outbound file (INT-14) · Debt buyers: per lot, encrypted (INT-25)

P2 · rwb-integration
Integration & files
queue rwb-integration
rwb.integration.events.v1

IN

OUT

REST  POST /documents (returns upload link) · GET /documents/{id}, /cases/{id}/documents · POST /documents/generate
EVT  AgentRunCompleted (classification)
TMP  DocumentIntakeWorkflow: OCR, classify, extract · Act: generate, seal · Schedule: retention

DB  writes schema rwb_document: metadata, custody, OCR text and fields, signatures, retention
EVT  rwb.document.events.v1: DocumentStored, DocumentFieldsExtracted
TMP  Agent: child: classify / extract run
FILE  Azure Blob (WORM): files, 2.8 TB by 2031

P5 · rwb-document
Document hub
queue rwb-document
rwb.document.events.v1

16

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-agent (P10, Agent runtime)
IN: REST GET /agent-runs/{id}; GET/POST /agent-policies (admin) | events DocumentStored (intake); CaseCreated (screening) | Temporal AgentRunWorkflow: 60 s, then rule result; Tool gateway: read-only calls for the agent
OUT: schema rwb_agent (agent policies, prompts, runs, guardrails, evaluations) | topic rwb.agent.events.v1: AgentRunCompleted | REST Source data: tool: read case facts · Document: tool: read extracted fields · Enterprise AI endpoint: HTTPS private endpoint

rwb-integration (P2, Integration & files)
IN: REST GET /interface-runs (operations); POST /interface-runs/{id}/retry | events (none: called as a task) | Temporal Act: deliverFile(manifest), receiveFile; Airflow window: WIN file 16:00, buyer files per lot
OUT: schema rwb_integration (interface config, file runs, outbound items, ACE integration paths) | topic rwb.integration.events.v1: FileDelivered, FileFailed | REST Document: fetch file by ID (SAS link) | FILE WIN (registered mail): daily outbound file (INT-14) · Debt buyers: per lot, encrypted (INT-25)

rwb-document (P5, Document hub)
IN: REST POST /documents (returns upload link); GET /documents/{id}, /cases/{id}/documents; POST /documents/generate | events AgentRunCompleted (classification) | Temporal DocumentIntakeWorkflow: OCR, classify, extract; Act: generate, seal · Schedule: retention
OUT: schema rwb_document (metadata, custody, OCR text and fields, signatures, retention) | topic rwb.document.events.v1: DocumentStored, DocumentFieldsExtracted | TMP Agent: child: classify / extract run | FILE Azure Blob (WORM): files, 2.8 TB by 2031

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

