SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# B-REQ-PRD-P2 source notes (scratch)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date 22 November 2026.

Sources read for the PRD:

- BRD Program v4 (extract): sections 1, 2, 3, 4, 5.2, 6.1 to 6.12, 7, 8, 9.
- BRD Epic 1 v4 (extract): section 3.2 P2 Integration and the change note.
- FSD P2 Integration v3 (extract of FSD v6): A1.1 to A1.6, A2.1 to A2.7, Requirements served.
- Architecture v5 Text Extract v1: slides 4, 7, 8, 11, 12, 13, 16, 32, 37, 38, 41, 42, 43, 44.
- Temporal and Drools Design Text Extract v1: read for the dispatch and rule position; it carries no rwb-integration row.
- Ownership Map v1: Services, Tables (interface_config, outbound_item, job_catalog), Endpoints, Events, Jobs, Workflows, Rulings.
- _work/msr/plan/ownership.json: P2 rows of api (11), tables (3); no P2 event, job or workflow row.
- _work/msr/plan/split_plan.json: stats (1034 slices, 358 legacy) and the legacy rows whose primary is P2.
- _work/msr/plan/ids.json: D-RCV-60, ADR-013 to ADR-023, DL44 to DL49.
- Story Template and Rules v1: R1, R3, R4, R5.1 to R5.7, R8.1, R9.
- For consistency only (read, not copied): the story files of RWB-SVC-P2 already written by B-P2-01.

Rulings used in the PRD (each has a candidate assumption row):

1. Arch v5 beats the FSD on the data lake (INT-19 delivered by rwb-reporting, INT-20 continuous ingest in rwb-decision).
2. Only rwb-source-data reads the thirty ACE views.
3. Job ownership follows the Ownership Map, and the service registers no Temporal Schedule.
4. The window belongs to the bank scheduler and the attempt ladder to the service.
5. FileDelivered and FileFailed are this service's events, unnumbered in the sources.
6. The INT-25 rows travel in the request manifest from rwb-debtsale.
7. Retry numbers stay interface configuration rows.

Counts: CAP 8, FR 22, NFR 13, AC 14, Q 7; CG 15, ASM 19.
