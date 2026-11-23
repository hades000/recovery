
Recovery Workbench: 19 services inside the ACE platform

Service boundaries, contracts and call types, the event broker and a reusable Temporal layer

For the architecture team   |   v5 · November 2026

Notes: Purpose: agree the target service architecture of Recovery Workbench with the architecture team.

What changed since v4 (feedback from the review): Recovery stays part of ACE (same AKS cluster, App Gateway and ACE Common shared services, as in recovery-architecture.pptx); recovery-core is split further into 19 services, one per business module, so each can be repurposed later; no database per service: Recovery uses the ACE database with one schema per service; no connection to the data lake; Kafka is proposed as the event broker; the Temporal layer is redrawn so it can be reused by other workbenches.

The 19 icons are the 19 Recovery services. The main part is diagrams and contracts; tables are in the appendix.

