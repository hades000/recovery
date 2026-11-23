
From the six-service proposal to 19: only recovery-core is split

Same platform roles as recovery-architecture.pptx; recovery-core is cut along its module lines

REFERENCE PROPOSAL · 6 SERVICES IN ACE

v5 · SHARED PLATFORM + 19 RECOVERY SERVICES

①  gateway-bff
Spring Cloud Gateway · Redis

②  workflow
Temporal, shared with ACE

③  recovery-core
modular monolith: all business modules

④  batch
Airflow: load, validate, report

⑤  document-service
OCR · Blob 2.8 TB

⑥  ai-agent
agents with rule fallback

Kept · shared BFF with Redis session; routes /api/recovery/*

Kept · shared Temporal + reusable workflow kit (L1-L3)

Kept as the bank's Airflow · overnight chain, files, extracts (to discuss)

rwb-document · P5

rwb-agent · P10

split

P3
Case

P7
Decision

P4
Access

S8
Deviation

S1
Valuation

S2
Treatment

S3
Guarantee

S4
Litigation

S5
Asset

S6
Debt sale

S7
Write-off

P6
Comms

P8
Payment

S9
Partner

P2
Integration

P1
Source data

P9
Reporting

Nothing new in the platform: recovery-core is cut along its module lines, so each module becomes its own service.

5

Notes: Reference: recovery-architecture.pptx proposes six services inside ACE: (1) gateway-bff (Spring Cloud Gateway, Redis session), (2) workflow on Temporal shared by ACE and Recovery, (3) recovery-core, a modular monolith holding the business modules on Azure PostgreSQL, (4) batch on Airflow (load, validate, report), (5) document-service (OCR, Blob, 2.8 TB), (6) ai-agent.

v5 keeps roles 1, 2 and 4 as shared platform, keeps 5 and 6 as rwb-document (P5) and rwb-agent (P10), and splits recovery-core into the other 17 module services. Business schedules (case creation, rule promotion, write-off scan) run as Temporal Schedules in the owning service; Role 4 becomes the bank's own Airflow, since the bank is moving from Control-M to Airflow (for discussion): it runs the cross-system overnight chain, fixed-window file transfers, report extracts and one-off bulk loads, and calls services through their APIs, never their schemas.

Why split further: each module becomes a unit that can be reused by another workbench, released alone and scaled alone.

