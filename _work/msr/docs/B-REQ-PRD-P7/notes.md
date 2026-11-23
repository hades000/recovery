# B-REQ-PRD-P7 working notes (scratch)

Sources read (read-only):
- 03 Requirements and specifications/PRD/ none for P7 (P1 and P4 exist as house style)
- FSD P7 Decision center and log v3 (extract): A1.1-A1.4, A2.1-A2.35, Requirements served, Screens, Appendix A and B
- TSD P7 Decision center and log v2: T3.1 (decision_log_entry 22 fields; approval 22 fields), T3.2 lists, T-A.1 API-P7-001..008
- BRD Program v4 §5.7 (REQ-DRI-001..005, 009..012; REQ-APD-001..011; REQ-ILG-001..014), §6 NFR, §8 release plan, §9 DL
- Arch v5 extract: slides 14 (P7 block), 20/26/27/28 (local record + central ledger, rules governance, strict mode), 41 (P7 row), 42-43 (EV-08, EV-09, EV-13, EV-28, EV-30), 44 (JOB-13, JOB-14, JOB-20)
- Temporal and Drools design v1: rule governance block, JOB-20, EV-30, checksum/cache 20, strict mode at four pivots
- Ownership Map (plan/ownership.json): P7 tables approval, decision_log_entry, rule_package, rule_package_version, rule_row, rule_test_case; interaction -> P1; delegation_limit -> P4; notice/template -> P6; EV-08/09/30, JOB-13/14/20, ApprovalWorkflow -> P7
- Template and Rules v1: R1, R3, R5 (R5.5 DP table, R5.6 wave map), R8.1, R8.2, R9
- ids.json: D-RCV-60 already allocated; no new decision IDs needed in this PRD

Realignment moves recorded:
1. Interaction ledger (FSD FEAT-ILG-01..10, REQ-ILG-001..014) -> P1 rwb-source-data (DP-18 default ruling).
2. REQ-DRI-009 data-lake copy and FEAT-DRI-06 -> removed (ADR-018); ingest continuous from Kafka (JOB-13).
3. FEAT-DRI-14..17 notices, letter templates, template catalog, proof of delivery -> P6/P5/P2.
4. Rule evaluation FEAT-DRI-07 local (embedded Drools kit, DP-04); registry stays P7.
5. FEAT-DRI-08 decision service -> owning services answer; P7 serves approval and the record.

Counts: CAP 18, FR 36, NFR 22, AC 22, OQ 12, ROL 10, JRN 6. CG 12 rows, ASM 14 rows.
