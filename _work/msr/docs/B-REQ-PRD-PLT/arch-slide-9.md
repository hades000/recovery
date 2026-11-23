
System architecture on one page: the full picture

Same design with the detail: Kafka settings, the five Temporal layers, the 19 schemas and a sample event

9

Notes: This is the one-page diagram for the architecture team; the editable source is 'Recovery System Architecture v5.excalidraw' next to this deck, and the high-resolution PNG prints on A3.

Read it top to bottom: staff and partners enter through the shared App Gateway; gateway-bff makes one REST hop to the owning service; each of the 19 services in namespace rwb-recovery publishes to its own Kafka topic, polls its own Temporal task queue and reads and writes only its own rwb_* schema on the ACE PostgreSQL server.

Kafka: topic per service rwb.<name>.events.v1, 12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, outbox and inbox, retry 1 min, 10 min, 1 h then .dlt; Event Hubs Premium is the fallback.

Temporal: shared with ACE, one cluster per environment. L1 cluster, L2 namespaces ace-collection and rwb-recovery, L3 versioned workflow kit, L4 activity contracts and Nexus (restructure.calculate in ACE), L5 domain workflows. Temporal keeps its own persistence database.

Data: only rwb-source-data reads the 30 recovery.v_ace_* views. Documents go to Blob with WORM through rwb-document only. The data lake and Power BI are not connected (INT-19 and INT-20 removed).

Airflow (amber, for discussion): the bank's scheduler, replacing Control-M, sits outside the cluster. (1) It runs the ACE ingestion DAG. (2) Its last task tells rwb-source-data the business date is ready, then waits for DailyCaseRun. (3) It opens the WIN and debt-buyer file windows. (4) It triggers report extracts in rwb-reporting. (5) It runs cutover loads and backfills. It calls APIs only and never reads rwb_* schemas.

The sample PaymentMissed event shows what travels on Kafka: CloudEvents headers, key caseId, IDs and facts only, no personal data.

