# Wave 2 edit log: TSD pack v4 and ERD v4

Agent: Wave 2 writer (ACE re-base). Date: 15 November 2026.
Inputs read: ACE DB Alignment Change Register v1 sections 2 to 6, ACE Data Tier Map v1, ACE Source Views v1.sql, Tier 4 sources (Physical Schema v5, LDM v7, CDM v6).

## 1. 05 Technical architecture\Recovery Workbench Technical Specifications by Module v4.zip

19 members, same names and order as v3.zip. 6 members changed, 13 byte-for-byte identical. P1 47,800 chars; P2 36,767; P3 45,883; P8 11,065; S1 13,481; S5 20,073; pack 116 KB.

### Member 1, P1 Recovery data engine (v2 member, internal version 3)
- Document control: version 3, 15 November 2026, D-RCV-35 and ADR-010, revision rows, related documents.
- Existing capability check: inbound source data REUSE by ACE ingestion; read path; freshness; reconciliation; dictionary.
- T1 and T2 re-written around the read model: AceViewReader, FreshnessMonitor, ReconciliationService, DictionaryService, ExtensionWriter; load adapter and DQ engine removed.
- T3.0 note that views carry no standard columns.
- T3.1 split: 3.1.1 catalogue of the 30 views (Tier, ACE objects, business key, use), 3.1.2 the 4 extension tables (party_ext DF-EXT-001..012, contact_point_ext 013..026, account_ext 027..035, valuation_ext 036..049), 3.1.3 retained metadata and operations tables (data_product, data_product_access, data_product_load, data_contract, sys_objects, sys_fields, sys_field_version, reconciliation_result, lake_copy_watermark, retention_rule, case_list_row, dp_treatment, dp_guarantee_claim).
- Removed from the model: 11 source copies and 9 load/DQ/tracker tables; a paragraph lists them and retires their field IDs.
- data_product_load now sourced from v_ace_batch_status (business_date, completed_at, record_count, is_complete).
- T3.2: 7 lists retired; LOV-CONTACT-TYPE added; LOV-REFRESH widened to BY_VERSION.
- T3.3: 12 relationships, including 4 extension 1:1 business-key links; no FK into ACE.
- T5.1: P1 owns no inbound interface; read path and INT-19 outbound. T5.3: AceDataReady / AceDataLate replace LoadCompleted / LoadRefused.
- T7: NFR-013, 014, 015, 018 re-based to the ACE batch and v_ace_account. T8: D-RCV-35 row.
- Appendix T-A: API-P1-003 to API-P1-008 retired in place; 001, 002 and 010 re-worded. Appendix T-B: DL43 added.

### Member 2, P2 Integration (v2 member, internal version 3)
- Adopted outbound-only: T1 scope, T1.1 ACE read path rules, T2 OutboundFileAdapter and OutboxRelay, T3 interface_config outbound only, interface_run and interface_signoff removed, party_product read from v_ace_party_product, outbound_item, processed_event, idempotency_key, outbox, feature flags, job_catalog, efs_ledger_outcome.
- T5.1 all inbound interfaces owned by ACE ingestion; T5.3 no P2 business event; T6.2 read-only service identity and SY-DATALOAD removed; T8 and T-A re-based; API-P2-013 and 014 retired; DL43 added.
- Member name kept as "P2 ... v2.md" so the pack member list is unchanged; the document is internally version 3.

### Member 3, P3 Case and workflow
- Document control, T1; T3.1 intro on business keys; 6 fields re-keyed: recovery_case.primary_person_key, case_account.account_key, case_party.person_key, interaction.person_key, interaction.contact_key (contact_type:key composite), case_entry_exclusion.account_key.
- Source column now ACE (ingested from ALS/EFS); T3.3 links re-pointed to v_ace_customer, v_ace_account, v_ace_contact; SY-DATALOAD removed; DL43 added.

### Member 4, P8 Payments and posting
- Document control, T1; proceeds.account_payment_id becomes payment_code (varchar 255, v_ace_payment); T3.3 link; T5.1 INT-02 and INT-16 into ACE, INT-03 confirmed on the ACE batch; SY-DATALOAD removed; DL43 added.

### Member 5, S1 Valuation and route
- Document control, T1; T3.1 replaced: v_ace_valuation (9 fields, DF-ACE-187..195), v_ace_score (10, DF-ACE-270..279), valuation_ext (7, DF-EXT-036..042); valuation and score tables and their field IDs retired.
- T3.3: 4 links (extension 1:1, appraisal to asset, score to account). T5.1 ACE read rows; T5.3 AceDataReady and ValuationAccepted; D6 corrected; DL43 added.

### Member 6, S5 Assets and auction
- Document control, T1; T3.1 replaced: v_ace_npa_asset (12, DF-ACE-208..219), v_ace_npa_sale (11, DF-ACE-220..230), listing and asset_sale re-keyed to asset_key; asset table and DF-COL-028..042 retired; DEF-05 note on the 7 carried AMIS columns.
- T3.3: 5 links; T5.1 INT-11/12/13 into ACE; API assetId paths become assetKey; SY-DATALOAD removed; DL43 added.

### Unchanged members (13, byte-for-byte)
P4, P5, P6, P7, P9, P10, S2, S3, S4, S6, S7, S8, S9.

## 2. 06 Data\Recovery Workbench Entity Relationship Diagram v4.html

- Rebuilt from Physical Schema v5 (92 tables), LDM v7 (122 entities, 1,366 fields), CDM v6 (14 data products and view metadata) and the 30-view SQL.
- Removed the 11 copy entities and 9 load entities. Added the 4 extension tables (orange left edge) and 30 ACE view boxes (dashed, pale, tagged "ACE view, read only - Tier 1/2"). 122 objects, 104 references, 18 business-key links, 86 foreign keys, 0 FKs into ACE.
- The 14 re-keyed links are drawn as business keys; the 4 extension tables are 1:1 by business key.
- Overview: new boundary figure (ACE Tier 1 and Tier 2, the 30 views, the recovery schema with Tier 3 and Tier 4), product summary and a product-to-product reference table. 17 tabs: 14 data products plus OPS, AGT and RPT, plus an ACE views catalogue, all relationships and notation.
- The 12 Section B columns are marked B on v_ace_account, v_ace_customer and v_ace_efs_action.
- Page style, nav, table style, colours and the IDEF1X legend are kept; the legend gains BK, dashed view box and extension-edge rows.
- Validated: HTML parses with no unbalanced tags, 172 tables all width-consistent, 122 object cards plus 30 catalogue cards, ASCII only, opens in Chrome.

## 3. 06 Data\Recovery Workbench Entity Relationship Diagram v4.pdf

- Generated from the v4 HTML with Chrome headless (`--headless --print-to-pdf --no-pdf-header-footer`). 96 pages, 2.38 MB, A4 portrait, light print stylesheet, all tabs printed, no URL header or footer. Opens in PyMuPDF.

## 4. Outstanding

1. DL43 is open. Section B (14 views and the 12 columns) and the S1/S5 features behind flags wait on the ACE team accepting RWB-ACE-001 by 21 November 2026.
2. LDM v7 draws listing.asset_key and asset_sale.asset_key to v_ace_asset. S5 reads the held asset from v_ace_npa_asset; the two views share asset_key. Recommended: LDM v7 names v_ace_npa_asset for the held asset in its next version.
3. DEF-05 remains on the 42 retained snapshot fields (including asset_sale DF-SAL-012..017/019 and dp_treatment DF-TRT-050/051); each owning story must drop the column or declare the snapshot.
4. The API Specification v3 must mirror the retirements made here: API-P1-003 to API-P1-008, API-P2-013 and API-P2-014.
5. The pre-existing folder 05 Technical architecture\Recovery Workbench Technical Specifications by Module v4\ (an earlier P2-only edit, P2 file named v3.md) was not used or modified; the v4 zip supersedes it and the stray folder should be retired at sign-off.
6. P2's member filename stays at v2 to preserve the pack member list while its internal version is 3. If versioned member names are preferred, rename and re-zip.
7. LDM v7 physical types for view fields are known to be wrong in places (register defect list); the ERD shows names and keys only, and S1/S5 take types from the view SQL, so the defect is not propagated.
8. P1 catalogues the 30 views but does not repeat all 304 view columns; the field list stays in LDM v7, as the Tier Map intends.
