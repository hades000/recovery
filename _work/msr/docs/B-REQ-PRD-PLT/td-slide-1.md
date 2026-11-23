
Temporal + Drools: how a recovery case runs and decides

Simple first, with examples · then the technical detailed design for scenarios S1–S9 and the demo use case

Recovery Workbench · Detailed design · November 2026

Notes: Purpose: explain, simply and then in detail, how the Recovery Workbench uses Temporal (to run each case's journey) and Drools (to make each rule-based decision), across the nine recovery scenarios S1 to S9, and what the demo will show.

Architecture context comes from 'Recovery Microservice Architecture v5' (Recovery stays part of ACE; 19 services, one per module; one ACE database with a schema per service; Kafka as the event broker; one shared Temporal cluster in five layers, reusable by other workbenches; a parent CaseWorkflow with a child workflow per stage; rules governed in rwb-decision and run in the owning service; decision records written locally and sealed centrally) and the Temporal and Drools Change Register v1 (decisions T1 to T10, D-RCV-36).

