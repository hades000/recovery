## Sheet: Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. |
|---|
| (C) Siam Commercial Bank and Henka Pte Ltd |
| Recovery Workbench Reference Data and Lists of Values v5 |
| Next version of Recovery Workbench Reference Data and Lists of Values v4.xlsx. Decision D-RCV-60 microservice realignment. |
| Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. |
| Change log |
| v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| What changed in v5 |
| 1. Lists sheet: four columns are added at the end. 'Owning service (D-RCV-60)' and 'Owning schema (D-RCV-60)' give the service code and name and the rwb_<name> schema that hold the list, 'Shared-list route (D-RCV-60)' gives the contract a consumer calls, and 'Basis (D-RCV-60)' names the Ownership Map row behind it. Columns A to F are unchanged, cell for cell. |
| 2. Lists sheet: the holding service follows the Ownership Map, not the old single schema. 126 lists are held by P3 rwb-case in rwb_case (lov_value), 7 are ACE data read through P1 rwb-source-data, 2 are held by P5 rwb-document, 2 are held by P7 rwb-decision and 1 by P4 rwb-access. The business owner in column D is copied unchanged and stays the stewardship role. |
| 3. Reference tables sheet: the same four columns are added at the end (F to I). delegation_limit, role, permission and masking_rule go to P4 rwb-access (ASM-0070; Ownership Map sheet Tables), rule_row to P7 rwb-decision (ASM-0069), document_type and retention_rule to P5 rwb-document (Ownership Map sheet Tables; ASM-0076), template to P6 rwb-comms, partner to S9 rwb-partner, queue, timer and reference_row to P3 rwb-case, and feature flags to the platform library (R-PREC default ruling). |
| 4. New sheet 'Reference data starter', after Reference tables: 179 rows, one per service and starter item, with the item, the mode (Load or Read), the route, the wave and the basis. It is the refdata starter of the D-RCV-60 change: what each service needs at its first deployment, and where it comes from. |
| 5. Change process sheet: one step is added (step 9, shared list). A list is held once, in its owning service, and every other service reads it through that owner's contract with the asOf business date; no service loads a second copy (DP-07). |
| 6. Key sheet: four rows are added, one for each new term ('Owning service', 'Shared-list route', 'Starter mode' and 'Reference data starter'). |
| 7. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the change-log row. |
| What did not change |
| All 138 lists, the 124 closed and 14 source split, every list code, kind, 'Values or source', 'Owner', 'Used by' and 'Source' cell, all 598 values with their Thai label, order and valid from date, the 14 reference table rows, the 8 change steps and the 12 key rows of v4, and every number and date of v4 are copied unchanged. |
| The only dates in the source are the 598 'Valid from' dates of 30 November 2026 in the Values sheet. They are copied unchanged because they are the in-force dates of the values; the programme release of 30 November 2026 is carried as tentative by the programme documents, and no date is changed here. |
| Where v4 says 'the Workbench' or names a stewardship role in column D, v5 still says so, and the service owner is read from the appended column (GAP-0223; ASM-0313). |
| Counts |
| Lists: 138 rows with 4 appended columns, 552 appended cells. Owning service: P3 126, P1 7, P5 2, P7 2, P4 1. Shared-list route: rwb-case list read 124, rwb-case parameters contract 1, rwb-case queue resource 1, ACE read through P1 7, rwb-decision rule packages 2, rwb-document contract 2, rwb-access contract 1. |
| Reference data starter: 179 rows over 18 service codes (17 of the 19 services plus the platform library), 171 Load and 8 Read. Wave 0: 3, wave 1: 147, wave 2: 13, wave 3: 10, wave 4: 6. |
| Reference tables: 14 rows with 4 appended columns, 56 appended cells. Change process: 8 rows plus 1. Key: 12 rows plus 4. Values: 598 rows, no cell changed. |
| Open points |
| GAP-0217 to GAP-0223 and ASM-0307 to ASM-0313 in the Gap and Assumption registers hold what this version leaves open: the 25 codes of LOV-REF-TABLE against the twelve of the contract, the dropped payment_match_rule, the two services with no derived starter row, the starter rule itself, the source lists held in another service's table, the meaning of the Owner column, and the reference rows that name no table. |

## Sheet: Lists

| Lists of values |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 138 lists: 124 closed and 14 source lists. 23 name the ACE view or the Workbench table their values come from; the rest are held and versioned in the Workbench. Each has one owner. |  |  |  |  |  |  |  |  |  |
| List | Kind | Values or source | Owner | Used by | Source | Owning service (D-RCV-60) | Owning schema (D-RCV-60) | Shared-list route (D-RCV-60) | Basis (D-RCV-60) |
| LOV-PRODUCT | Closed list | 4 | Product heads | recovery_case.product_group, delegation_limit.product_group, template.product_group, case_list_row.product_group, reconciliation_result.product_group, parameter_value.product_group, approval.product_group, measure_snapshot.product_group, agent_policy.segment_product_group, agent_run.segment_product_group | v_ace_product (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_product on each release |
| LOV-CASE-STATUS | Closed list | 8 | Center of excellence | recovery_case.status, recovery_case.status_before_hold, case_list_row.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-STAGE | Closed list | 9 | Center of excellence | recovery_case.stage_code, case_list_row.stage_code, document_checklist_item.stage_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ROUTE | Closed list | 8 | Center of excellence | recovery_case.route_code, v_ace_score.route_code, case_list_row.route_code, document_checklist_item.route_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CLOSURE | Closed list | 8 | Center of excellence | recovery_case.closure_reason |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PARTY-ROLE | Closed list | 5 | Center of excellence | case_party.party_role |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DEVIATION | Closed list | 7 | Center of excellence | deviation.deviation_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DEV-OUTCOME | Closed list | 3 | Center of excellence | deviation.outcome |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-RAISED-BY | Closed list | 4 | Center of excellence | deviation.raised_by |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ASSIGN | Closed list | 4 | Center of excellence | queue.assignment_method |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ASSIGN-REASON | Closed list | 5 | Center of excellence | assignment.reason |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ELEMENT | Closed list | 7 | Center of excellence | task.element_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DISCRETION | Closed list | 3 | Center of excellence | task.discretion |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TASK-STATUS | Closed list | 4 | Center of excellence | task.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TIMER | Closed list | 9 | Center of excellence | timer.timer_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TIMER-STATUS | Closed list | 4 | Center of excellence | timer.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PARTY-TYPE | Closed list | 2 | Data steward and data product owner | v_ace_customer.party_type (Section B, after RWB-ACE-001) |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ID-TYPE | Closed list | 3 | Compliance | v_ace_customer.id_type (Section B, after RWB-ACE-001) |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SEGMENT | Closed list | 3 | Data steward and data product owner | v_ace_customer.segment (Section B, after RWB-ACE-001), v_ace_npa_asset.from_segment, debt_sale_lot.segment | v_ace_customer (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_customer on each release |
| LOV-CHANNEL | Closed list | 12 | Conduct and QA officer | v_ace_contact.contact_type, interaction.channel, template.channel, efs_ledger_outcome.channel |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CONTACT-SRC | Closed list | 5 | Conduct and QA officer | contact_point_ext.source |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CONSENT | Closed list | 3 | Compliance | contact_point_ext.consent_given |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-COLL-TYPE | Closed list | 6 | Data steward and data product owner | v_ace_collateral.collateral_type | v_ace_collateral (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_collateral on each release |
| LOV-OCCUPANCY | Closed list | 4 | Head of NPA | No live field after D-RCV-35; the list is kept with its values | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-ENCUMBRANCE | Closed list | 4 | Legal counsel | No live field after D-RCV-35; the list is kept with its values | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-APPRAISAL | Closed list | 5 | Head of NPA | v_ace_valuation.appraisal_type | v_ace_valuation (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_valuation on each release |
| LOV-ASSET-TYPE | Closed list | 6 | Head of NPA | v_ace_asset.asset_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TRANSFER-IN | Closed list | 3 | Head of NPA | v_ace_npa_asset.transfer_in_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-HOLDING | Closed list | 6 | Head of NPA | No live field after D-RCV-35; the list is kept with its values | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-TREATMENT | Closed list | 11 | Center of excellence | treatment.treatment_type, dp_treatment.treatment_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PROPOSER | Closed list | 3 | Center of excellence | treatment.proposed_by, dp_treatment.proposed_by |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-APPROVAL-LEVEL | Closed list | 6 | Risk | treatment.approval_level, decision_log_entry.approval_level, delegation_limit.approval_level, dp_treatment.approval_level, approval.approval_level |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TRT-OUTCOME | Closed list | 5 | Center of excellence | treatment.outcome, dp_treatment.outcome |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CLAIM-TYPE | Closed list | 4 | Guarantee officer | guarantee_claim.claim_type, dp_guarantee_claim.claim_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CLAIM-STATUS | Closed list | 5 | Guarantee officer | guarantee_claim.status, dp_guarantee_claim.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LEGAL-TYPE | Closed list | 6 | Head of Litigation | legal_action.action_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LEGAL-STATUS | Closed list | 6 | Head of Litigation | legal_action.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-NOTICE | Closed list | 4 | Legal counsel | notice.notice_type, template.notice_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DELIVERY | Closed list | 4 | Head of Litigation | notice.delivery_status | v_ace_pod (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_pod on each release |
| LOV-SENT-TYPE | Closed list | 2 | Head of Litigation | notice.sent_type | v_ace_pod (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_pod on each release |
| LOV-HEARING | Closed list | 4 | Head of Litigation | hearing.hearing_type | v_ace_hearing (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_hearing on each release |
| LOV-HEARING-OUTCOME | Closed list | 4 | Head of Litigation | hearing.outcome |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PARTNER-TYPE | Closed list | 8 | Partner and agency manager | partner.partner_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PANEL | Closed list | 4 | Partner and agency manager | partner.panel_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-INSTRUCTION | Closed list | 7 | Partner and agency manager | partner_instruction.instruction_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-INSTR-STATUS | Closed list | 6 | Partner and agency manager | partner_instruction.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SALE-CHANNEL | Closed list | 5 | Head of NPA | listing.sale_channel |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LISTING | Closed list | 5 | Head of NPA | listing.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-BUYER-CLASS | Closed list | 2 | Head of Asset Liquidity | debt_sale_lot.buyer_class |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LOT-STATUS | Closed list | 5 | Head of Asset Liquidity | debt_sale_lot.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PUTBACK | Closed list | 4 | Head of Asset Liquidity | debt_sale_account.put_back_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DIRECTION | Closed list | 2 | Conduct and QA officer | interaction.direction, interface_config.direction |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CONTACT-RESULT | Closed list | 5 | Conduct and QA officer | interaction.contact_result, v_ace_efs_action.contact_result (Section B, after RWB-ACE-001) |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CONDUCT | Closed list | 3 | Conduct and QA officer | interaction.conduct_check |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SOURCE | Closed list | 2 | Data steward and data product owner | interaction.source_system |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DOC-SOURCE | Closed list | 5 | Business lead with Legal | document.source, document_intake.source |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-REVIEW | Closed list | 4 | Business lead with Legal | document.review_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CUSTODY | Closed list | 6 | Business lead with Legal | document_custody.from_location, document_custody.to_location |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PROCEEDS-SRC | Closed list | 7 | Credit Administration | proceeds.source |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-MATCH | Closed list | 5 | Credit Administration | proceeds.matched_to |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ROUTE-SET | Closed list | 10 | Center of excellence | rule_row.route_set, rule_test_case.route_set |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ROLE-CLASS | Closed list | 3 | Security administrator | role.role_class |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SCOPE | Closed list | 4 | Security administrator | role.default_scope |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CAPABILITY | Closed list | 14 | Security administrator | permission.capability_area, approval.capability_area |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LANG | Closed list | 2 | Business lead | template.language |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-DATA-PRODUCT | Closed list | 14 | Center of excellence | data_product.product_code, data_product_access.product_code, data_product_load.product_code, retention_rule.product_code, interface_config.data_product, measure_definition.data_product |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-REFRESH | Closed list | 4 | Center of excellence | data_product.refresh_cycle |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-FRESHNESS | Closed list | 2 | Center of excellence | data_product_load.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CONTRACT-STATUS | Closed list | 3 | Center of excellence | data_contract.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LOAD-STATUS | Closed list | 6 | Center of excellence | ACE batch (no live field after D-RCV-35; the load table left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-DQ-STATUS | Closed list | 2 | Center of excellence | ACE ingestion (no live field after D-RCV-35; the data quality tables left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-DQ-RULE-TYPE | Closed list | 7 | Center of excellence | ACE ingestion (no live field after D-RCV-35; the data quality tables left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-TRACKER-LOCATION | Closed list | 4 | Center of excellence | Cutover plan (no live field after D-RCV-35; the tracker tables left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-UPDATE-CYCLE | Closed list | 4 | Center of excellence | Cutover plan (no live field after D-RCV-35; the tracker tables left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-TRACKER-DECISION | Closed list | 3 | Center of excellence | Cutover plan (no live field after D-RCV-35; the tracker tables left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-TRACKER-STATUS | Closed list | 5 | Center of excellence | Cutover plan (no live field after D-RCV-35; the tracker tables left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-PUBLISH-STATUS | Closed list | 3 | Center of excellence | case_list_row.publish_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-REC-RESULT | Closed list | 2 | Center of excellence | reconciliation_result.result |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-RETENTION-END | Closed list | 2 | Center of excellence | retention_rule.end_action |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TRANSPORT | Closed list | 2 | Center of excellence | interface_config.transport |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-INTERFACE-RUN | Closed list | 6 | Center of excellence | Outbound interfaces (no live field after D-RCV-35; the inbound run table left the schema) | Workbench list | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); no live field after D-RCV-35, the list is kept with its values |
| LOV-OUTBOUND-STATUS | Closed list | 5 | Center of excellence | outbound_item.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-OUTBOX-DELIVERY | Closed list | 4 | Center of excellence | outbox_delivery.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ENVIRONMENT | Closed list | 4 | Center of excellence | feature_flag_change.environment, parameter_value.environment |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PRODUCT-STATUS | Closed list | 4 | Center of excellence | v_ace_party_product.product_status | v_ace_party_product (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_party_product on each release |
| LOV-EXCLUSION-REASON | Closed list | 5 | Center of excellence | case_entry_exclusion.reason_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SNAPSHOT-STATUS | Closed list | 3 | Center of excellence | queue_measure.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PARAM-SCOPE | Closed list | 2 | Center of excellence | parameter_catalog.scope |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-VERSION-STATUS | Closed list | 6 | Center of excellence | parameter_value.status, reference_version.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TEST-RESULT | Closed list | 2 | Center of excellence | reference_version.test_result, rule_test_case.result |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-REF-TABLE | Closed list | 25 | Center of excellence | reference_version.table_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-RULE-TABLE | Closed list | 5 | Center of excellence | rule_row.rule_table |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TRANSFER-REASON | Closed list | 6 | Center of excellence | assignment.transfer_reason_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-PLAN-STATUS | Closed list | 4 | Center of excellence | recovery_case.plan_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-LEDGER-EVENT | Closed list | 14 | Center of excellence | interaction.event_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ACTOR-TYPE | Closed list | 3 | Center of excellence | interaction.actor_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SEND-STATUS | Closed list | 4 | Center of excellence | interaction.delivery_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CAPTURE-KIND | Closed list | 3 | Center of excellence | document.capture_kind |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SCAN-RESULT | Closed list | 2 | Center of excellence | document_intake.scan_result |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-OCR-STATUS | Closed list | 4 | Center of excellence | document_intake.ocr_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-INTAKE-MATCH | Closed list | 7 | Center of excellence | document_intake.match_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-EXTRACT-STATUS | Closed list | 3 | Center of excellence | document_intake.extract_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-INTAKE-REVIEW | Closed list | 5 | Center of excellence | document_intake.review_reason |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-INTAKE-OUTCOME | Closed list | 2 | Center of excellence | document_intake.review_outcome |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-RETENTION-ACTION | Closed list | 4 | Center of excellence | retention_action.action |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SIGN-METHOD | Closed list | 3 | Center of excellence | signature_request.method |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SIGN-STATUS | Closed list | 5 | Center of excellence | signature_request.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SIGNATURE-BASIS | Closed list | 2 | Center of excellence | template.signature_basis |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-TRT-SIGNATURE | Closed list | 3 | Center of excellence | treatment.signature_status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CREDIT-RESULT | Closed list | 2 | Center of excellence | v_ace_credit_decision.credit_result | v_ace_credit_decision (confirms the codes) | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071); the codes are confirmed by v_ace_credit_decision on each release |
| LOV-APPROVAL-STATUS | Closed list | 5 | Center of excellence | approval.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-MATCH-TYPE | Closed list | 3 | Center of excellence | payment_match_rule.match_type |  | P7 rwb-decision | rwb_decision | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-MEASURE-UNIT | Closed list | 4 | Center of excellence | measure_definition.unit |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-MEASURE-DIM | Closed list | 5 | Center of excellence | measure_snapshot.dimension_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-MEASURE-PUBLISH | Closed list | 2 | Center of excellence | measure_publish.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-AGENT | Closed list | 5 | Center of excellence | agent_policy.agent_code, agent_prompt.agent_code, agent_run.agent_code, agent_sample.agent_code, agent_evaluation_run.agent_code, agent_alert.agent_code |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-AUTONOMY | Closed list | 3 | Center of excellence | agent_policy.autonomy_mode, agent_run.autonomy_mode |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-CONFIG-STATUS | Closed list | 3 | Center of excellence | agent_policy.status, agent_prompt.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-AGENT-RUN | Closed list | 7 | Center of excellence | agent_run.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-SUBJECT-TYPE | Closed list | 3 | Center of excellence | agent_sample.subject_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-EVAL-STATUS | Closed list | 3 | Center of excellence | agent_evaluation_run.status |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-EXTRACT-APPROACH | Closed list | 4 | Center of excellence | agent_evaluation.approach |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-FEEDBACK | Closed list | 3 | Center of excellence | agent_feedback.verdict |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-AGENT-ALERT | Closed list | 2 | Center of excellence | agent_alert.alert_type |  | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row; lov_value is a P3 table of rwb_case (Ownership Map sheet Tables; ASM-0071) |
| LOV-ACTION-CODE | Source list | EFS action codes, 1,106 values, read from ACE through v_ace_efs_action_code | Data steward and data product owner | interaction.action_code, case_list_row.last_action_code, v_ace_efs_action.action_code, efs_ledger_outcome.action_code | v_ace_efs_action_code | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-BU | Source list | Business units, read from ACE through v_ace_branch | Data steward and data product owner | v_ace_account.business_unit (Section B, after RWB-ACE-001) | v_ace_branch | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-BUCKET | Source list | Arrears buckets, read from ACE through v_ace_account and v_ace_bucket_log | Data steward and data product owner | v_ace_account.daily_bucket (Section B, after RWB-ACE-001), v_ace_bucket_log.bucket | v_ace_account, v_ace_bucket_log | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-CLASS | Source list | BOT loan classification and stages, read from ACE through v_ace_account | Data steward and data product owner | v_ace_account.classification | v_ace_account | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-DECISION | Source list | D1 to D9 with sub-decisions, X1 to X7, held as a versioned Workbench list | Data steward and data product owner | decision_log_entry.decision_code, delegation_limit.decision_code, approval.decision_code | Workbench table rule_row | P7 rwb-decision | rwb_decision | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Lists sheet Source column; rule_row is a P7 table (Ownership Map sheet Tables) |
| LOV-DOC-TYPE | Source list | Document types, held in document_type and versioned | Data steward and data product owner | document.document_type, document_checklist_item.document_type, document_intake.predicted_type | Workbench table document_type | P5 rwb-document | rwb_document | rwb-document contract (DP-07) | Lists sheet Source column; document_type is a P5 table (Ownership Map sheet Tables) |
| LOV-EXPOSURE | Source list | Exposure bands, set by the center of excellence and held as a parameter | Data steward and data product owner | recovery_case.exposure_band | Workbench table parameter_catalog | P3 rwb-case | rwb_case | rwb-case parameters contract RWB-P3-E1042-CON (DP-06) | Lists sheet Source column; parameter_catalog is a P3 table (Ownership Map sheet Tables) |
| LOV-PAY-CHANNEL | Source list | Payment channels, read from ACE through v_ace_payment | Data steward and data product owner | v_ace_payment.payment_channel | v_ace_payment | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-PRODUCT-CODE | Source list | Core bank product codes, read from ACE through v_ace_product | Data steward and data product owner | v_ace_account.product_key, v_ace_product.product_code | v_ace_product | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-PROVINCE | Source list | The 77 provinces of Thailand, held as a closed reference list | Data steward and data product owner | v_ace_collateral_detail.province | Workbench table lov_value | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet Source column; lov_value is a P3 table (Ownership Map sheet Tables) |
| LOV-REGION | Source list | Regions, read from ACE through v_ace_branch | Data steward and data product owner | recovery_case.region_code, agent_policy.segment_region_code, agent_run.segment_region_code | v_ace_branch | P1 rwb-source-data | rwb_source_data | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet Source column; the values are ACE data read through the recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05) |
| LOV-RETENTION | Source list | Retention classes from the bank retention schedule, held in retention_rule | Data steward and data product owner | interaction.retention_class, document.retention_class, document_type.retention_class | Workbench table retention_rule | P5 rwb-document | rwb_document | rwb-document contract (DP-07) | Lists sheet Source column; retention_rule is a P5 table (Ownership Map sheet Tables) |
| LOV-ROLE | Source list | The 54 roles in the role table, versioned | Data steward and data product owner | recovery_case.next_action_owner_role, queue.role_code, task.owner_role, timer.escalated_to_role, rule_row.owner_role, data_product.owner_role, data_product_access.role_code, sys_fields.owner_role, interface_config.owner_role, interface_config.alert_role, outbound_item.owner_role, job_catalog.owner_role, parameter_catalog.owner_role, rule_test_case.expected_owner_role, masking_rule.role_code, role_conflict.role_code, partner_user.role_code, approval.route_role_code, agent_policy.alert_role, agent_alert.sent_to_role | Workbench table role | P4 rwb-access | rwb_access | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet Source column; role is a P4 table (Ownership Map sheet Tables) |
| LOV-TEAM | Source list | Teams, from the organisation structure held in queue | Data steward and data product owner | recovery_case.team_code, queue.team_code, case_list_row.team_code | Workbench table queue | P3 rwb-case | rwb_case | rwb-case queue resource (DP-13); the queue rows are reference rows of rwb_case | Lists sheet Source column; queue is a P3 table (Ownership Map sheet Tables) |

## Sheet: Values

| Values in the closed lists |  |  |  |  |  |
|---|---|---|---|---|---|
| 598 values. Thai labels follow DL10. Every value carries a version and a valid from date. |  |  |  |  |  |
| List | Code | English label | Thai label | Order | Valid from |
| LOV-PRODUCT | MORTGAGE | Mortgage | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PRODUCT | HIRE_PURCHASE | Hire purchase | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PRODUCT | SSME | SSME | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PRODUCT | UNSECURED | Unsecured | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CASE-STATUS | NEW | New | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CASE-STATUS | ASSIGNED | Assigned | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CASE-STATUS | IN_PROGRESS | In progress | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CASE-STATUS | WAITING_CUSTOMER | Waiting customer | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CASE-STATUS | WAITING_PARTNER | Waiting partner | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CASE-STATUS | WAITING_APPROVAL | Waiting approval | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-CASE-STATUS | ON_HOLD | On hold | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-CASE-STATUS | CLOSED | Closed | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-STAGE | RESTRUCTURE | Restructure | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-STAGE | SETTLEMENT | Settlement | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-STAGE | DEED_IN_LIEU | Deed in lieu | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-STAGE | GUARANTEE_CLAIM | Guarantee claim | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-STAGE | LITIGATION | Litigation | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-STAGE | ASSET_DISPOSAL | Asset disposal | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-STAGE | DEBT_SALE | Debt sale | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-STAGE | WRITE_OFF | Write-off | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-STAGE | DEVIATIONS | Deviations | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-ROUTE | R1 | Restructure | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ROUTE | R2 | Settlement | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ROUTE | R3 | Deed in lieu | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ROUTE | R4 | Guarantee claim | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ROUTE | R5 | Litigation | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ROUTE | R6 | Asset disposal | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-ROUTE | R7 | Debt sale | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-ROUTE | R8 | Write-off | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-CLOSURE | CURED | Cured | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CLOSURE | SETTLED | Settled | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CLOSURE | REALIZED | Realized | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CLOSURE | SOLD | Sold | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CLOSURE | WRITTEN_OFF | Written off | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CLOSURE | INSURANCE_SETTLED | Insurance settled | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-CLOSURE | MERGED | Merged | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-CLOSURE | CANCELED | Canceled | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-PARTY-ROLE | BORROWER | Borrower | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PARTY-ROLE | CO_BORROWER | Co-borrower | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PARTY-ROLE | GUARANTOR | Guarantor | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PARTY-ROLE | AUTHORIZED_SIGNATORY | Authorized signatory | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-PARTY-ROLE | HEIR | Heir | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-DEVIATION | X1 | Dispute or complaint | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DEVIATION | X2 | Vulnerable customer or hardship | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DEVIATION | X3 | Deceased customer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-DEVIATION | X4 | Fraud | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-DEVIATION | X5 | Bankruptcy or external seizure | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-DEVIATION | X6 | Lost contact | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-DEVIATION | X7 | Collateral event | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-DEV-OUTCOME | RETURNED | Returned | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DEV-OUTCOME | RE_ROUTED | Re-routed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DEV-OUTCOME | CASE_ENDED | Case ended | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-RAISED-BY | SCREENING_AGENT | Screening agent | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-RAISED-BY | RULE | Rule | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-RAISED-BY | OFFICER | Officer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-RAISED-BY | CUSTOMER_CONTACT | Customer contact | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ASSIGN | ROUND_ROBIN | Round robin | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ASSIGN | LOWEST_LOAD | Lowest load | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ASSIGN | NAMED_OWNER | Named owner | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ASSIGN | SKILL | Skill | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ASSIGN-REASON | ALLOCATION | Allocation | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ASSIGN-REASON | TRANSFER | Transfer | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ASSIGN-REASON | REBALANCE | Rebalance | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ASSIGN-REASON | MANUAL | Manual | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ASSIGN-REASON | ESCALATION | Escalation | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ELEMENT | HUMAN_TASK | Human task | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ELEMENT | CUSTOMER_TASK | Customer task | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ELEMENT | PARTNER_TASK | Partner task | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ELEMENT | DECISION_TASK | Decision task | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ELEMENT | STAGE_ENTRY | Stage entry | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ELEMENT | MILESTONE | Milestone | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-ELEMENT | EVENT_LISTENER | Event listener | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-DISCRETION | AUTOMATIC | Automatic | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DISCRETION | DISCRETIONARY | Discretionary | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DISCRETION | REQUIRED | Required | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TASK-STATUS | OPEN | Open | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TASK-STATUS | IN_PROGRESS | In progress | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TASK-STATUS | DONE | Done | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TASK-STATUS | CANCELED | Canceled | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TIMER | SERVICE_LEVEL | Service level | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TIMER | NOTICE_PERIOD | Notice period | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TIMER | CURE_PERIOD | Cure period | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TIMER | PRESCRIPTION | Prescription | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TIMER | HEARING_DEADLINE | Hearing deadline | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-TIMER | OFFER_VALIDITY | Offer validity | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-TIMER | HOLDING_AGE | Holding age | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-TIMER | CLAIM_DEADLINE | Claim deadline | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-TIMER | INSTALLMENT_DUE | Installment due | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-TIMER-STATUS | RUNNING | Running | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TIMER-STATUS | PAUSED | Paused | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TIMER-STATUS | EXPIRED | Expired | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TIMER-STATUS | STOPPED | Stopped | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-PARTY-TYPE | INDIVIDUAL | Individual | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PARTY-TYPE | JURISTIC_PERSON | Juristic person | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ID-TYPE | THAI_NATIONAL_ID | Thai national ID | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ID-TYPE | PASSPORT | Passport | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ID-TYPE | COMPANY_REGISTRATION | Company registration | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SEGMENT | RETAIL | Retail | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SEGMENT | SSME | SSME | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SEGMENT | CORPORATE | Corporate | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CHANNEL | MOBILE | Mobile | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CHANNEL | HOME_PHONE | Home phone | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CHANNEL | WORK_PHONE | Work phone | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CHANNEL | LINE | LINE | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CHANNEL | EMAIL | Email | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CHANNEL | POSTAL_ADDRESS | Postal address | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-CHANNEL | CALL | Call | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-CHANNEL | VISIT | Visit | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-CHANNEL | SMS | SMS | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-CHANNEL | LETTER | Letter | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-CHANNEL | PORTAL | Portal | Pending (DL10) | 11 | 30 Nov 2026 |
| LOV-CHANNEL | BRANCH | Branch | Pending (DL10) | 12 | 30 Nov 2026 |
| LOV-CONTACT-SRC | BANK_RECORD | Bank record | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CONTACT-SRC | FIELD_VISIT | Field visit | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONTACT-SRC | AGENCY | Agency | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CONTACT-SRC | BUREAU_TRACE | Bureau trace | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CONTACT-SRC | CUSTOMER | Customer | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CONSENT | GIVEN | Given | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CONSENT | WITHDRAWN | Withdrawn | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONSENT | UNKNOWN | Unknown | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-COLL-TYPE | LAND | Land | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-COLL-TYPE | HOUSE | House | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-COLL-TYPE | CONDOMINIUM | Condominium | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-COLL-TYPE | VEHICLE | Vehicle | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-COLL-TYPE | DEPOSIT | Deposit | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-COLL-TYPE | OTHER | Other | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-OCCUPANCY | OWNER | Owner | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-OCCUPANCY | TENANT | Tenant | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-OCCUPANCY | VACANT | Vacant | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-OCCUPANCY | UNKNOWN | Unknown | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ENCUMBRANCE | CLEAR | Clear | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ENCUMBRANCE | OTHER_CREDITOR | Other creditor | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ENCUMBRANCE | SEIZED | Seized | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ENCUMBRANCE | UNDER_DISPUTE | Under dispute | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-APPRAISAL | MARKET | Market | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-APPRAISAL | OFFICIAL | Official | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-APPRAISAL | FORCED_SALE | Forced sale | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-APPRAISAL | DESKTOP | Desktop | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-APPRAISAL | AGENT_ESTIMATE | Agent estimate | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ASSET-TYPE | DETACHED_HOUSE | Detached house | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ASSET-TYPE | TOWNHOUSE | Townhouse | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ASSET-TYPE | CONDOMINIUM | Condominium | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ASSET-TYPE | LAND | Land | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ASSET-TYPE | COMMERCIAL_BUILDING | Commercial building | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ASSET-TYPE | VEHICLE | Vehicle | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-TRANSFER-IN | AUCTION_PURCHASE | Auction purchase | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRANSFER-IN | DEED_IN_LIEU | Deed in lieu | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRANSFER-IN | REPOSSESSION | Repossession | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-HOLDING | HELD | Held | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-HOLDING | LISTED | Listed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-HOLDING | UNDER_OFFER | Under offer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-HOLDING | SOLD | Sold | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-HOLDING | TRANSFERRED | Transferred | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-HOLDING | RENTED | Rented | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-TREATMENT | RESTRUCTURE | Restructure | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TREATMENT | SETTLEMENT | Settlement | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TREATMENT | DEED_IN_LIEU | Deed in lieu | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TREATMENT | BUY_BACK | Buy-back | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TREATMENT | GUARANTEE_CLAIM | Guarantee claim | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-TREATMENT | REPOSSESSION | Repossession | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-TREATMENT | AUCTION | Auction | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-TREATMENT | DEBT_SALE | Debt sale | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-TREATMENT | WRITE_OFF | Write-off | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-TREATMENT | RAMC_TRANSFER | RAMC transfer | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-TREATMENT | RENTAL | Rental | Pending (DL10) | 11 | 30 Nov 2026 |
| LOV-PROPOSER | AGENT | Agent | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PROPOSER | RULE | Rule | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PROPOSER | PERSON | Person | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-APPROVAL-LEVEL | L1 | Board of Directors | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-APPROVAL-LEVEL | L2 | Executive Committee | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-APPROVAL-LEVEL | L3 | Problem Asset Resolution Committee or Management Committee | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-APPROVAL-LEVEL | L4 | Head of Recovery, function level, or Problem Asset Resolution Committee | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-APPROVAL-LEVEL | L5 | Recovery executive, division level | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-APPROVAL-LEVEL | L6 | Recovery executive, department level | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-TRT-OUTCOME | KEPT | Kept | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRT-OUTCOME | BROKEN | Broken | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRT-OUTCOME | COMPLETED | Completed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TRT-OUTCOME | CANCELED | Canceled | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TRT-OUTCOME | DECLINED | Declined | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CLAIM-TYPE | TCG | TCG | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CLAIM-TYPE | CREDIT_LIFE_INSURANCE | Credit life insurance | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CLAIM-TYPE | MORTGAGE_INSURANCE | Mortgage insurance | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CLAIM-TYPE | COLLATERAL_INSURANCE | Collateral insurance | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CLAIM-STATUS | PREPARING | Preparing | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CLAIM-STATUS | FILED | Filed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CLAIM-STATUS | DEFECT | Defect | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CLAIM-STATUS | PAID | Paid | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CLAIM-STATUS | REJECTED | Rejected | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-LEGAL-TYPE | NOTICE | Notice | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LEGAL-TYPE | CIVIL_CASE | Civil case | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LEGAL-TYPE | APPEAL | Appeal | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LEGAL-TYPE | ENFORCEMENT | Enforcement | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LEGAL-TYPE | BANKRUPTCY_PETITION | Bankruptcy petition | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-LEGAL-TYPE | LED_AUCTION | LED auction | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-LEGAL-STATUS | OPEN | Open | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LEGAL-STATUS | FILED | Filed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LEGAL-STATUS | JUDGMENT | Judgment | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LEGAL-STATUS | ENFORCING | Enforcing | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LEGAL-STATUS | CLOSED | Closed | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-LEGAL-STATUS | WITHDRAWN | Withdrawn | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-NOTICE | DEMAND | Demand | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-NOTICE | RECALL | Recall | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-NOTICE | STATUTORY_SALE_NOTICE | Statutory sale notice | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-NOTICE | GUARANTOR_NOTICE | Guarantor notice | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-DELIVERY | DELIVERED | Delivered | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DELIVERY | REFUSED | Refused | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DELIVERY | UNDELIVERABLE | Undeliverable | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-DELIVERY | PENDING | Pending | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-SENT-TYPE | BEFORE_NPL | Before NPL | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SENT-TYPE | NPL | NPL | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-HEARING | FIRST_HEARING | First hearing | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-HEARING | WITNESS | Witness | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-HEARING | JUDGMENT_READING | Judgment reading | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-HEARING | MEDIATION | Mediation | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-HEARING-OUTCOME | HELD | Held | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-HEARING-OUTCOME | ADJOURNED | Adjourned | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-HEARING-OUTCOME | SETTLED | Settled | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-HEARING-OUTCOME | JUDGMENT | Judgment | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | AGENCY | Agency | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | LAW_FIRM | Law firm | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | VALUER | Valuer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | AUCTION_VENDOR | Auction vendor | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | BROKER | Broker | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | DEBT_BUYER | Debt buyer | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | AMC | AMC | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-PARTNER-TYPE | RAMC | RAMC | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-PANEL | ACTIVE | Active | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PANEL | ON_NOTICE | On notice | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PANEL | SUSPENDED | Suspended | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PANEL | EXITED | Exited | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INSTRUCTION | COLLECT | Collect | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-INSTRUCTION | FILE_SUIT | File suit | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-INSTRUCTION | ENFORCE | Enforce | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-INSTRUCTION | APPRAISE | Appraise | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INSTRUCTION | REPOSSESS | Repossess | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-INSTRUCTION | LIST | List | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-INSTRUCTION | SELL | Sell | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-INSTR-STATUS | SENT | Sent | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-INSTR-STATUS | ACCEPTED | Accepted | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-INSTR-STATUS | DECLINED | Declined | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-INSTR-STATUS | IN_PROGRESS | In progress | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INSTR-STATUS | DONE | Done | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-INSTR-STATUS | RECALLED | Recalled | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-SALE-CHANNEL | DUTCH_AUCTION | Dutch auction | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SALE-CHANNEL | BROKER | Broker | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SALE-CHANNEL | DIRECT | Direct | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SALE-CHANNEL | LED_AUCTION | LED auction | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-SALE-CHANNEL | RAMC | RAMC | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-LISTING | DRAFT | Draft | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LISTING | LIVE | Live | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LISTING | UNDER_OFFER | Under offer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LISTING | SOLD | Sold | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LISTING | WITHDRAWN | Withdrawn | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-BUYER-CLASS | AMC | AMC | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-BUYER-CLASS | NON_AMC | Non-AMC | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LOT-STATUS | BUILDING | Building | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LOT-STATUS | OFFERED | Offered | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LOT-STATUS | AWARDED | Awarded | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LOT-STATUS | TRANSFERRED | Transferred | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LOT-STATUS | CLOSED | Closed | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-PUTBACK | NONE | None | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PUTBACK | CLAIMED | Claimed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PUTBACK | ACCEPTED | Accepted | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PUTBACK | REJECTED | Rejected | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-DIRECTION | INBOUND | Inbound | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DIRECTION | OUTBOUND | Outbound | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONTACT-RESULT | RIGHT_PARTY | Right party | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CONTACT-RESULT | THIRD_PARTY | Third party | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONTACT-RESULT | NO_ANSWER | No answer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CONTACT-RESULT | WRONG_NUMBER | Wrong number | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CONTACT-RESULT | REFUSED | Refused | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CONDUCT | PASSED | Passed | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CONDUCT | BLOCKED | Blocked | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONDUCT | NOT_APPLICABLE | Not applicable | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SOURCE | EFS | EFS | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SOURCE | WORKBENCH | Workbench | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DOC-SOURCE | SCAN | Scan | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DOC-SOURCE | UPLOAD | Upload | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DOC-SOURCE | GENERATED | Generated | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-DOC-SOURCE | PARTNER | Partner | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-DOC-SOURCE | EMAIL | Email | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-REVIEW | NOT_NEEDED | Not needed | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-REVIEW | PENDING | Pending | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-REVIEW | CONFIRMED | Confirmed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-REVIEW | CORRECTED | Corrected | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CUSTODY | VAULT | Vault | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CUSTODY | BRANCH | Branch | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CUSTODY | POST | Post | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CUSTODY | LAWYER | Lawyer | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CUSTODY | COURT | Court | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CUSTODY | LAND_OFFICE | Land office | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | CUSTOMER | Customer | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | LED | LED | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | AUCTION | Auction | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | BUYER | Buyer | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | AGENCY | Agency | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | INSURER | Insurer | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-PROCEEDS-SRC | GUARANTOR | Guarantor | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-MATCH | INSTALLMENT | Installment | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-MATCH | SETTLEMENT | Settlement | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-MATCH | FEE | Fee | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-MATCH | SALE_PROCEEDS | Sale proceeds | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-MATCH | UNMATCHED | Unmatched | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ROUTE-SET | RESTRUCTURE | Restructure | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ROUTE-SET | SETTLEMENT | Settlement | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ROUTE-SET | DEED_IN_LIEU | Deed in lieu | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ROUTE-SET | GUARANTEE_CLAIM | Guarantee claim | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ROUTE-SET | LITIGATION | Litigation | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-ROUTE-SET | ASSET_DISPOSAL | Asset disposal | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-ROUTE-SET | DEBT_SALE | Debt sale | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-ROUTE-SET | WRITE_OFF | Write-off | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-ROUTE-SET | DEVIATIONS | Deviations | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-ROUTE-SET | UNIVERSAL_RULES | Universal rules | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-ROLE-CLASS | BANK_USER | Bank user | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ROLE-CLASS | PARTNER_USER | Partner user | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ROLE-CLASS | NON_HUMAN_ACTOR | Non-human actor | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SCOPE | OWN | Own | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SCOPE | TEAM | Team | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SCOPE | REGION | Region | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SCOPE | ALL | All | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CAPABILITY | CASE_RECORD | Case record | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CAPABILITY | QUEUE_AND_ALLOCATION | Queue and allocation | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CAPABILITY | TREATMENT_AND_OFFER | Treatment and offer | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CAPABILITY | LITIGATION | Litigation | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CAPABILITY | ASSET_AND_DISPOSAL | Asset and disposal | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-CAPABILITY | DEBT_SALE | Debt sale | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-CAPABILITY | WRITE_OFF_AND_POSTING | Write-off and posting | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-CAPABILITY | DOCUMENTS | Documents | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-CAPABILITY | RULES_AND_PARAMETERS | Rules and parameters | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-CAPABILITY | REFERENCE_DATA | Reference data | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-CAPABILITY | DECISION_LOG | Decision log | Pending (DL10) | 11 | 30 Nov 2026 |
| LOV-CAPABILITY | PARTNER_PORTAL | Partner portal | Pending (DL10) | 12 | 30 Nov 2026 |
| LOV-CAPABILITY | REPORTING | Reporting | Pending (DL10) | 13 | 30 Nov 2026 |
| LOV-CAPABILITY | PLATFORM_ADMINISTRATION | Platform administration | Pending (DL10) | 14 | 30 Nov 2026 |
| LOV-LANG | TH | TH | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LANG | EN | EN | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP01 | Account and arrears | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP02 | Customer and party | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP03 | Case and ownership | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP04 | Treatment and offers | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP05 | Contact and promises | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP06 | Collateral and assets | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP07 | Legal events and cases | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP08 | Partner performance | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP09 | Debt sale | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP10 | Documents and extracted fields | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP11 | Scores and route economics | Pending (DL10) | 11 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP12 | Decision log | Pending (DL10) | 12 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP13 | Money and closure | Pending (DL10) | 13 | 30 Nov 2026 |
| LOV-DATA-PRODUCT | DP14 | Reference data | Pending (DL10) | 14 | 30 Nov 2026 |
| LOV-REFRESH | DAILY | Daily | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-REFRESH | WEEKLY | Weekly | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-REFRESH | MONTHLY | Monthly | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-REFRESH | ON_CHANGE | On change | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-FRESHNESS | LOADED | Loaded | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-FRESHNESS | STALE | Stale | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONTRACT-STATUS | DRAFT | Draft | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CONTRACT-STATUS | PUBLISHED | Published | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONTRACT-STATUS | SUPERSEDED | Superseded | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LOAD-STATUS | RUNNING | Running | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LOAD-STATUS | COMPLETED | Completed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LOAD-STATUS | REFUSED | Refused | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LOAD-STATUS | LATE | Late | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LOAD-STATUS | FAILED | Failed | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-LOAD-STATUS | SUPERSEDED | Superseded | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-DQ-STATUS | OPEN | Open | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DQ-STATUS | CLEARED | Cleared | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | NOT_NULL | Not null | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | UNIQUE_ACROSS | Unique across | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | RANGE | Range | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | SUM_EQUALS | Sum equals | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | EXISTS_LINK | Exists link | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | MAX_AGE_DAYS | Max age days | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-DQ-RULE-TYPE | FIELD_BEFORE | Field before | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-TRACKER-LOCATION | EXCEL | Excel | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRACKER-LOCATION | SHAREPOINT | SharePoint | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRACKER-LOCATION | LOCAL_FILE | Local file | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TRACKER-LOCATION | NONE | None | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-UPDATE-CYCLE | DAILY | Daily | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-UPDATE-CYCLE | WEEKLY | Weekly | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-UPDATE-CYCLE | MONTHLY | Monthly | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-UPDATE-CYCLE | AD_HOC | Ad hoc | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TRACKER-DECISION | LOAD | Load | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRACKER-DECISION | RETIRE | Retire | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRACKER-DECISION | KEEP | Keep | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TRACKER-STATUS | LISTED | Listed | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRACKER-STATUS | LOADED | Loaded | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRACKER-STATUS | SIGNED_OFF | Signed off | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TRACKER-STATUS | RETIRED | Retired | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TRACKER-STATUS | KEPT | Kept | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-PUBLISH-STATUS | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PUBLISH-STATUS | HELD | Held | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PUBLISH-STATUS | RELEASED | Released | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-REC-RESULT | PASS | Pass | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-REC-RESULT | BREAK | Break | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-RETENTION-END | ARCHIVE | Archive | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-RETENTION-END | REVIEW | Review | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRANSPORT | SFTP | SFTP | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRANSPORT | COLLINS | COLLINS | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-INTERFACE-RUN | RECEIVED | Received | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-INTERFACE-RUN | LOADED | Loaded | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-INTERFACE-RUN | REFUSED | Refused | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-INTERFACE-RUN | MISSING | Missing | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INTERFACE-RUN | DUPLICATE | Duplicate | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-INTERFACE-RUN | FAILED | Failed | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-OUTBOUND-STATUS | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-OUTBOUND-STATUS | SENT | Sent | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-OUTBOUND-STATUS | RETRY | Retry | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-OUTBOUND-STATUS | EXCEPTION | Exception | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-OUTBOUND-STATUS | ACKNOWLEDGED | Acknowledged | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-OUTBOX-DELIVERY | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-OUTBOX-DELIVERY | RETRYING | Retrying | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-OUTBOX-DELIVERY | DELIVERED | Delivered | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-OUTBOX-DELIVERY | EXCEPTION | Exception | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-ENVIRONMENT | DEV | DEV | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ENVIRONMENT | SIT | SIT | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ENVIRONMENT | UAT | UAT | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-ENVIRONMENT | PROD | PROD | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-PRODUCT-STATUS | ACTIVE | Active | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PRODUCT-STATUS | DELINQUENT | Delinquent | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PRODUCT-STATUS | CLOSED | Closed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PRODUCT-STATUS | WRITTEN_OFF | Written off | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-EXCLUSION-REASON | DECEASED | Deceased | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-EXCLUSION-REASON | FRAUD | Fraud | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-EXCLUSION-REASON | BANKRUPTCY | Bankruptcy | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-EXCLUSION-REASON | ACTIVE_PLAN | Active plan | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-EXCLUSION-REASON | OPEN_DISPUTE | Open dispute | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-SNAPSHOT-STATUS | TAKEN | Taken | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SNAPSHOT-STATUS | PUBLISHED | Published | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SNAPSHOT-STATUS | HELD | Held | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PARAM-SCOPE | PRODUCT | Product | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PARAM-SCOPE | GLOBAL | Global | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-VERSION-STATUS | VALIDATED | Validated | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-VERSION-STATUS | APPROVED | Approved | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-VERSION-STATUS | IN_FORCE | In force | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-VERSION-STATUS | SUPERSEDED | Superseded | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-VERSION-STATUS | ROLLED_BACK | Rolled back | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-VERSION-STATUS | REFUSED | Refused | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-TEST-RESULT | PASSED | Passed | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TEST-RESULT | FAILED | Failed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-REF-TABLE | PRODUCT | Product | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-REF-TABLE | REGION | Region | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-REF-TABLE | EXPOSURE_BAND | Exposure band | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-REF-TABLE | ROLE | Role | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-REF-TABLE | TEAM | Team | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-REF-TABLE | QUEUE | Queue | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-REF-TABLE | QUEUE_MEMBER | Queue member | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-REF-TABLE | SERVICE_LEVEL | Service level | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-REF-TABLE | DOCUMENT_TYPE | Document type | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-REF-TABLE | DOCUMENT_CHECKLIST | Document checklist | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-REF-TABLE | RETENTION_CLASS | Retention class | Pending (DL10) | 11 | 30 Nov 2026 |
| LOV-REF-TABLE | TEMPLATE | Template | Pending (DL10) | 12 | 30 Nov 2026 |
| LOV-REF-TABLE | DELEGATION_LIMIT | Delegation limit | Pending (DL10) | 13 | 30 Nov 2026 |
| LOV-REF-TABLE | PERMISSION | Permission | Pending (DL10) | 14 | 30 Nov 2026 |
| LOV-REF-TABLE | MASKING_RULE | Masking rule | Pending (DL10) | 15 | 30 Nov 2026 |
| LOV-REF-TABLE | PARTNER_USER | Partner user | Pending (DL10) | 16 | 30 Nov 2026 |
| LOV-REF-TABLE | LEGAL_PERIOD | Legal period | Pending (DL10) | 17 | 30 Nov 2026 |
| LOV-REF-TABLE | HOLIDAY | Holiday | Pending (DL10) | 18 | 30 Nov 2026 |
| LOV-REF-TABLE | PRODUCT_PARAMETER | Product parameter | Pending (DL10) | 19 | 30 Nov 2026 |
| LOV-REF-TABLE | PARAMETER | Parameter | Pending (DL10) | 20 | 30 Nov 2026 |
| LOV-REF-TABLE | ENTRY | Entry | Pending (DL10) | 21 | 30 Nov 2026 |
| LOV-REF-TABLE | EXCLUSION | Exclusion | Pending (DL10) | 22 | 30 Nov 2026 |
| LOV-REF-TABLE | ALLOCATION | Allocation | Pending (DL10) | 23 | 30 Nov 2026 |
| LOV-REF-TABLE | ASSIGNMENT | Assignment | Pending (DL10) | 24 | 30 Nov 2026 |
| LOV-REF-TABLE | TRANSFER | Transfer | Pending (DL10) | 25 | 30 Nov 2026 |
| LOV-RULE-TABLE | ENTRY | Entry | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-RULE-TABLE | EXCLUSION | Exclusion | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-RULE-TABLE | ALLOCATION | Allocation | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-RULE-TABLE | ASSIGNMENT | Assignment | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-RULE-TABLE | TRANSFER | Transfer | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-TRANSFER-REASON | R01 | Capacity | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRANSFER-REASON | R02 | Customer deceased | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRANSFER-REASON | R03 | Skill | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-TRANSFER-REASON | R04 | Owner absent | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-TRANSFER-REASON | R05 | Legal referral | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-TRANSFER-REASON | R06 | Wrong queue | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-PLAN-STATUS | CREATED | Created | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-PLAN-STATUS | APPROVED | Approved | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-PLAN-STATUS | BOOKED | Booked | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-PLAN-STATUS | BROKEN | Broken | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | CONTACT | Contact | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | LETTER | Letter | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | PROMISE | Promise | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | PAYMENT | Payment | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | HANDOVER | Handover | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | CASE_CREATED | Case created | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | CASE_ALLOCATED | Case allocated | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | CASE_TRANSFERRED | Case transferred | Pending (DL10) | 8 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | CASE_ESCALATED | Case escalated | Pending (DL10) | 9 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | DOCUMENT_ATTACHED | Document attached | Pending (DL10) | 10 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | DECISION_TAKEN | Decision taken | Pending (DL10) | 11 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | CORRECTION | Correction | Pending (DL10) | 12 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | PARTNER_RESULT | Partner result | Pending (DL10) | 13 | 30 Nov 2026 |
| LOV-LEDGER-EVENT | OFFER | Offer | Pending (DL10) | 14 | 30 Nov 2026 |
| LOV-ACTOR-TYPE | USER | User | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-ACTOR-TYPE | SERVICE | Service | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-ACTOR-TYPE | PARTNER | Partner | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SEND-STATUS | SENT | Sent | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SEND-STATUS | DELIVERED | Delivered | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SEND-STATUS | READ | Read | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SEND-STATUS | FAILED | Failed | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-CAPTURE-KIND | PHOTO | Photo | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CAPTURE-KIND | BILL | Bill | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CAPTURE-KIND | CHECKLIST | Checklist | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SCAN-RESULT | CLEAN | Clean | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SCAN-RESULT | INFECTED | Infected | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-OCR-STATUS | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-OCR-STATUS | DONE | Done | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-OCR-STATUS | RESCAN | Rescan | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-OCR-STATUS | FAILED | Failed | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | MATCHED | Matched | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | NO_MATCH | No match | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | MULTIPLE | Multiple | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | CONFLICT | Conflict | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | CASE_CLOSED | Case closed | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-INTAKE-MATCH | NO_TYPE | No type | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-EXTRACT-STATUS | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-EXTRACT-STATUS | DONE | Done | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-EXTRACT-STATUS | FAILED | Failed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-INTAKE-REVIEW | RESCAN | Rescan | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-INTAKE-REVIEW | UNREADABLE_FILE | Unreadable file | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-INTAKE-REVIEW | LOW_CONFIDENCE | Low confidence | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-INTAKE-REVIEW | MODEL_UNAVAILABLE | Model unavailable | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-INTAKE-REVIEW | UNKNOWN_TYPE | Unknown type | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-INTAKE-OUTCOME | ATTACHED | Attached | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-INTAKE-OUTCOME | DISCARDED | Discarded | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-RETENTION-ACTION | ARCHIVED | Archived | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-RETENTION-ACTION | LISTED | Listed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-RETENTION-ACTION | HELD | Held | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-RETENTION-ACTION | EXCEPTION | Exception | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-SIGN-METHOD | E_SIGNATURE | E-signature | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SIGN-METHOD | BRANCH | Branch | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SIGN-METHOD | PAPER | Paper | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SIGN-STATUS | QUEUED | Queued | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SIGN-STATUS | SENT | Sent | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SIGN-STATUS | SIGNED | Signed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-SIGN-STATUS | DECLINED | Declined | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-SIGN-STATUS | EXPIRED | Expired | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-SIGNATURE-BASIS | E_SIGNATURE_ALLOWED | E-signature allowed | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SIGNATURE-BASIS | WET_INK_REQUIRED | Wet ink required | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRT-SIGNATURE | PENDING | Pending | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-TRT-SIGNATURE | SIGNED | Signed | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-TRT-SIGNATURE | NOT_SIGNED | Not signed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CREDIT-RESULT | APPROVED | Approved | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CREDIT-RESULT | REFUSED | Refused | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-APPROVAL-STATUS | WAITING | Waiting | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-APPROVAL-STATUS | HELD_NO_LIMIT | Held, no limit | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-APPROVAL-STATUS | APPROVED | Approved | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-APPROVAL-STATUS | REFUSED | Refused | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-APPROVAL-STATUS | RETURNED | Returned | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-MATCH-TYPE | EXACT | Exact | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-MATCH-TYPE | WINDOW | Window | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-MATCH-TYPE | PARTIAL | Partial | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-MEASURE-UNIT | COUNT | Count | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-MEASURE-UNIT | THB | Baht | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-MEASURE-UNIT | DAYS | Days | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-MEASURE-UNIT | PERCENT | Percent | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-MEASURE-DIM | ROUTE | Route | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-MEASURE-DIM | AGE_BAND | Age band | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-MEASURE-DIM | QUEUE | Queue | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-MEASURE-DIM | STAGE | Stage | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-MEASURE-DIM | AGENT | Agent | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-MEASURE-PUBLISH | PUBLISHED | Published | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-MEASURE-PUBLISH | HELD | Held | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-AGENT | INTAKE | Intake | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-AGENT | SCREENING | Screening | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-AGENT | LEGAL_DOC | Legal doc | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-AGENT | EXTRACT | Extract | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-AGENT | TDR_OFFER | Tdr offer | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-AUTONOMY | OFF | Off | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-AUTONOMY | SHADOW | Shadow | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-AUTONOMY | L1 | L1 | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-CONFIG-STATUS | LOADED | Loaded | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-CONFIG-STATUS | APPROVED | Approved | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-CONFIG-STATUS | RETIRED | Retired | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-AGENT-RUN | ANSWERED | Answered | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-AGENT-RUN | TIMED_OUT | Timed out | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-AGENT-RUN | GUARDRAIL_FAILED | Guardrail failed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-AGENT-RUN | BELOW_FLOOR | Below floor | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-AGENT-RUN | TOOL_UNAVAILABLE | Tool unavailable | Pending (DL10) | 5 | 30 Nov 2026 |
| LOV-AGENT-RUN | MODEL_ERROR | Model error | Pending (DL10) | 6 | 30 Nov 2026 |
| LOV-AGENT-RUN | DISABLED | Disabled | Pending (DL10) | 7 | 30 Nov 2026 |
| LOV-SUBJECT-TYPE | CASE | Case | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-SUBJECT-TYPE | DOCUMENT | Document | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-SUBJECT-TYPE | LEGAL_ACTION | Legal action | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-EVAL-STATUS | RUNNING | Running | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-EVAL-STATUS | DONE | Done | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-EVAL-STATUS | FAILED | Failed | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-EXTRACT-APPROACH | AGENT | Agent | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-EXTRACT-APPROACH | OCR_TEMPLATE | OCR template | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-EXTRACT-APPROACH | MODEL | Model | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-EXTRACT-APPROACH | OCR_AND_MODEL | OCR and model | Pending (DL10) | 4 | 30 Nov 2026 |
| LOV-FEEDBACK | ACCEPTED | Accepted | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-FEEDBACK | CORRECTED | Corrected | Pending (DL10) | 2 | 30 Nov 2026 |
| LOV-FEEDBACK | REJECTED | Rejected | Pending (DL10) | 3 | 30 Nov 2026 |
| LOV-AGENT-ALERT | COST_CAP | Cost cap | Pending (DL10) | 1 | 30 Nov 2026 |
| LOV-AGENT-ALERT | DRIFT | Drift | Pending (DL10) | 2 | 30 Nov 2026 |

## Sheet: Reference tables

| Other reference data |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Reference data held as versioned rows, its owner and where it is specified. |  |  |  |  |  |  |  |  |
| Reference data | Table | What it holds | Owner | Specified in | Owning service (D-RCV-60) | Owning schema (D-RCV-60) | Shared route (D-RCV-60) | Basis (D-RCV-60) |
| Routing rules | rule_row | 448 rules in ten route sets | Center of excellence; Risk signs where a limit moves | Business Rules and Routing Logic | P7 rwb-decision | rwb_decision | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Reference tables sheet row; rule_row is a P7 table (Ownership Map sheet Tables) |
| Allocation table | rule_row | Product group, region and exposure band to queue | Shared operations | DL23 | P7 rwb-decision | rwb_decision | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Reference tables sheet row; rule_row is a P7 table (Ownership Map sheet Tables) |
| Delegation of authority | delegation_limit | Limits by decision, level, product and amount | Risk with the product heads | Delegation of Authority Matrix; DL18 | P4 rwb-access | rwb_access | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; delegation_limit is a P4 table (Ownership Map sheet Tables) |
| Roles | role | 54 roles | Application owner | Users, Roles and Permissions | P4 rwb-access | rwb_access | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; role is a P4 table (Ownership Map sheet Tables) |
| Permission matrix | permission | Roles against 14 capability areas | Application owner; security administrator loads | Users, Roles and Permissions | P4 rwb-access | rwb_access | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; permission is a P4 table (Ownership Map sheet Tables) |
| Queues | queue | Queues by team and role, with method, cap and overflow | Shared operations | DL23 | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Reference tables sheet row; queue is a P3 table (Ownership Map sheet Tables) |
| Service levels and timers | Reference table | Time allowed per state, warning and escalation | Business lead | DL22 | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Reference tables sheet row; timer is a P3 table (Ownership Map sheet Tables) |
| Letter and notice templates | template | Templates by type, product and language | Legal counsel | DL28 | P6 rwb-comms | rwb_comms | rwb-comms contract (DP-07) | Reference tables sheet row; template is a P6 table (Ownership Map sheet Tables) |
| Messages | Reference table | Screen and letter messages in English and Thai | Product owner; Legal and Compliance for customer wording | Error and Message Standard; DL10 | P3 rwb-case | rwb_case | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Reference tables sheet row; reference_row is a P3 table (Ownership Map sheet Tables) |
| Document types | Reference table | Types and the fields extracted from each | Business lead with Legal | DL19 | P5 rwb-document | rwb_document | rwb-document contract (DP-07) | Reference tables sheet row; document_type is a P5 table (Ownership Map sheet Tables) |
| Retention classes | Reference table | Retention period by data product and document type | Compliance | DL26 | P5 rwb-document | rwb_document | rwb-document contract (DP-07) | Reference tables sheet row; retention_rule is a P5 table (Ownership Map sheet Tables) |
| Masking rules | Reference table | Which role sees which personal field unmasked | Compliance | DL26 | P4 rwb-access | rwb_access | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; masking_rule is a P4 table (Ownership Map sheet Tables) |
| Partner panel | partner | Partners, contracts and panel status | Partner and agency manager | None | S9 rwb-partner | rwb_partner | rwb-partner contract (DP-07) | Reference tables sheet row; partner is an S9 table (Ownership Map sheet Tables) |
| Feature flags | Configuration | Flag values per environment | Tech leads | Engineering Practices | PLT platform library | platform library (a library object in each service schema) | platform library (R-PREC default ruling) | Reference tables sheet row; feature_flag is a PLT table (Ownership Map sheet Tables) |

## Sheet: Reference data starter

| Reference data starter |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 179 rows: one per service and starter item. The starter is the set of lists and reference tables a service reads or holds at its first deployment, in the wave of that service (Ownership Map sheet Services). |  |  |  |  |  |  |  |
| A row exists when the service owns a table whose column uses a list (Lists sheet 'Used by'; Ownership Map sheet Tables), owns the ACE view a list column is read from (P1 rwb-source-data, DP-05), or owns a reference table of the Reference tables sheet. A list is held once, in the service the Lists sheet names in 'Owning service (D-RCV-60)', and every other service reads it through that owner's contract (DP-07); an ACE-sourced list is read through the P1 contract and never loaded (DP-05). |  |  |  |  |  |  |  |
| Not in the starter: 11 closed lists that have no live field after D-RCV-35, and two services with no derived row, S1 rwb-valuation and S7 rwb-writeoff (GAP-0219; GAP-0220; ASM-0309; ASM-0310). |  |  |  |  |  |  |  |
| Service | Service name | Service wave | Starter item | Item kind | Starter mode | Route (D-RCV-60) | Basis (D-RCV-60) |
| P1 | rwb-source-data | 1 | LOV-ACTION-CODE | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-ACTION-CODE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-ACTOR-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ACTOR-TYPE, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-APPRAISAL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-APPRAISAL, 'Used by' v_ace_valuation; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-APPROVAL-LEVEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-APPROVAL-LEVEL, 'Used by' approval; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-ASSET-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ASSET-TYPE, 'Used by' v_ace_asset; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-BU | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-BU, 'Used by' v_ace_account; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-BUCKET | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-BUCKET, 'Used by' v_ace_account; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CASE-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CASE-STATUS, 'Used by' case_list_row; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CHANNEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CHANNEL, 'Used by' efs_ledger_outcome; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CLAIM-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CLAIM-STATUS, 'Used by' dp_guarantee_claim; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CLAIM-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CLAIM-TYPE, 'Used by' dp_guarantee_claim; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CLASS | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-CLASS, 'Used by' v_ace_account; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-COLL-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-COLL-TYPE, 'Used by' v_ace_collateral; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CONDUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CONDUCT, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CONSENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CONSENT, 'Used by' contact_point_ext; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CONTACT-RESULT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CONTACT-RESULT, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CONTACT-SRC | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CONTACT-SRC, 'Used by' contact_point_ext; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CONTRACT-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CONTRACT-STATUS, 'Used by' data_contract; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-CREDIT-RESULT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CREDIT-RESULT, 'Used by' v_ace_credit_decision; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-DATA-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DATA-PRODUCT, 'Used by' data_product; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-DIRECTION | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DIRECTION, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-FRESHNESS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-FRESHNESS, 'Used by' data_product_load; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-ID-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ID-TYPE, 'Used by' v_ace_customer; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-LEDGER-EVENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-LEDGER-EVENT, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PARTY-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PARTY-TYPE, 'Used by' v_ace_customer; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PAY-CHANNEL | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-PAY-CHANNEL, 'Used by' v_ace_payment; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PRODUCT-CODE | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-PRODUCT-CODE, 'Used by' v_ace_account; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PRODUCT-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT-STATUS, 'Used by' v_ace_party_product; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PROPOSER | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PROPOSER, 'Used by' dp_treatment; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PROVINCE | Source list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PROVINCE, 'Used by' v_ace_collateral_detail; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-PUBLISH-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PUBLISH-STATUS, 'Used by' case_list_row; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-REC-RESULT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-REC-RESULT, 'Used by' reconciliation_result; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-REFRESH | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-REFRESH, 'Used by' data_product; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-RETENTION | Source list | Load | rwb-document contract (DP-07) | Lists sheet row LOV-RETENTION, 'Used by' document; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-ROUTE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ROUTE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-SEGMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SEGMENT, 'Used by' debt_sale_lot; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-SEND-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SEND-STATUS, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-SOURCE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SOURCE, 'Used by' interaction; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-STAGE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-STAGE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-TEAM | Source list | Load | rwb-case queue resource (DP-13); the queue rows are reference rows of rwb_case | Lists sheet row LOV-TEAM, 'Used by' case_list_row; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-TRANSFER-IN | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TRANSFER-IN, 'Used by' v_ace_npa_asset; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-TREATMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TREATMENT, 'Used by' dp_treatment; Ownership Map sheet Tables |
| P1 | rwb-source-data | 1 | LOV-TRT-OUTCOME | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TRT-OUTCOME, 'Used by' dp_treatment; Ownership Map sheet Tables |
| P2 | rwb-integration | 1 | LOV-DATA-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DATA-PRODUCT, 'Used by' data_product; Ownership Map sheet Tables |
| P2 | rwb-integration | 1 | LOV-DIRECTION | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DIRECTION, 'Used by' interaction; Ownership Map sheet Tables |
| P2 | rwb-integration | 1 | LOV-OUTBOUND-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-OUTBOUND-STATUS, 'Used by' outbound_item; Ownership Map sheet Tables |
| P2 | rwb-integration | 1 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| P2 | rwb-integration | 1 | LOV-TRANSPORT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TRANSPORT, 'Used by' interface_config; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | Messages | Reference table | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | Queues | Reference table | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | Service levels and timers | Reference table | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-ASSIGN | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ASSIGN, 'Used by' queue; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-ASSIGN-REASON | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ASSIGN-REASON, 'Used by' assignment; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-CASE-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CASE-STATUS, 'Used by' case_list_row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-CLOSURE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CLOSURE, 'Used by' recovery_case; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-DISCRETION | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DISCRETION, 'Used by' task; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-ELEMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ELEMENT, 'Used by' task; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-ENVIRONMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ENVIRONMENT, 'Used by' feature_flag_change; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-EXCLUSION-REASON | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-EXCLUSION-REASON, 'Used by' case_entry_exclusion; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-EXPOSURE | Source list | Load | rwb-case parameters contract RWB-P3-E1042-CON (DP-06) | Lists sheet row LOV-EXPOSURE, 'Used by' recovery_case; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-PARAM-SCOPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PARAM-SCOPE, 'Used by' parameter_catalog; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-PARTY-ROLE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PARTY-ROLE, 'Used by' case_party; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-PLAN-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PLAN-STATUS, 'Used by' recovery_case; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-REF-TABLE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-REF-TABLE, 'Used by' reference_version; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-REGION | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-REGION, 'Used by' agent_policy; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-ROUTE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ROUTE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-SNAPSHOT-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SNAPSHOT-STATUS, 'Used by' queue_measure; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-STAGE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-STAGE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-TASK-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TASK-STATUS, 'Used by' task; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-TEAM | Source list | Load | rwb-case queue resource (DP-13); the queue rows are reference rows of rwb_case | Lists sheet row LOV-TEAM, 'Used by' case_list_row; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-TEST-RESULT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TEST-RESULT, 'Used by' reference_version; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-TIMER | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TIMER, 'Used by' timer; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-TIMER-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TIMER-STATUS, 'Used by' timer; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-TRANSFER-REASON | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TRANSFER-REASON, 'Used by' assignment; Ownership Map sheet Tables |
| P3 | rwb-case | 1 | LOV-VERSION-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-VERSION-STATUS, 'Used by' parameter_value; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | Delegation of authority | Reference table | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | Masking rules | Reference table | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | Permission matrix | Reference table | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | Roles | Reference table | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Reference tables sheet row; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-APPROVAL-LEVEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-APPROVAL-LEVEL, 'Used by' approval; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-CAPABILITY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CAPABILITY, 'Used by' approval; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-DECISION | Source list | Load | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Lists sheet row LOV-DECISION, 'Used by' approval; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-ROLE-CLASS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ROLE-CLASS, 'Used by' role; Ownership Map sheet Tables |
| P4 | rwb-access | 1 | LOV-SCOPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SCOPE, 'Used by' role; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | Document types | Reference table | Load | rwb-document contract (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | Retention classes | Reference table | Load | rwb-document contract (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-CAPTURE-KIND | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CAPTURE-KIND, 'Used by' document; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-CUSTODY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CUSTODY, 'Used by' document_custody; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-DATA-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DATA-PRODUCT, 'Used by' data_product; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-DOC-SOURCE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DOC-SOURCE, 'Used by' document; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-DOC-TYPE | Source list | Load | rwb-document contract (DP-07) | Lists sheet row LOV-DOC-TYPE, 'Used by' document; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-EXTRACT-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-EXTRACT-STATUS, 'Used by' document_intake; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-INTAKE-MATCH | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-INTAKE-MATCH, 'Used by' document_intake; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-INTAKE-OUTCOME | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-INTAKE-OUTCOME, 'Used by' document_intake; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-INTAKE-REVIEW | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-INTAKE-REVIEW, 'Used by' document_intake; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-OCR-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-OCR-STATUS, 'Used by' document_intake; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-RETENTION | Source list | Load | rwb-document contract (DP-07) | Lists sheet row LOV-RETENTION, 'Used by' document; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-RETENTION-ACTION | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-RETENTION-ACTION, 'Used by' retention_action; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-RETENTION-END | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-RETENTION-END, 'Used by' retention_rule; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-REVIEW | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-REVIEW, 'Used by' document; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-ROUTE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ROUTE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-SCAN-RESULT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SCAN-RESULT, 'Used by' document_intake; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-SIGN-METHOD | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SIGN-METHOD, 'Used by' signature_request; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-SIGN-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SIGN-STATUS, 'Used by' signature_request; Ownership Map sheet Tables |
| P5 | rwb-document | 1 | LOV-STAGE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-STAGE, 'Used by' case_list_row; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | Letter and notice templates | Reference table | Load | rwb-comms contract (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-CHANNEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CHANNEL, 'Used by' efs_ledger_outcome; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-DELIVERY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DELIVERY, 'Used by' notice; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-LANG | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-LANG, 'Used by' template; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-NOTICE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-NOTICE, 'Used by' notice; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-SENT-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SENT-TYPE, 'Used by' notice; Ownership Map sheet Tables |
| P6 | rwb-comms | 1 | LOV-SIGNATURE-BASIS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SIGNATURE-BASIS, 'Used by' template; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | Allocation table | Reference table | Load | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Reference tables sheet row; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | Routing rules | Reference table | Load | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Reference tables sheet row; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-APPROVAL-LEVEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-APPROVAL-LEVEL, 'Used by' approval; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-APPROVAL-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-APPROVAL-STATUS, 'Used by' approval; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-CAPABILITY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CAPABILITY, 'Used by' approval; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-DECISION | Source list | Load | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Lists sheet row LOV-DECISION, 'Used by' approval; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-ROUTE-SET | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ROUTE-SET, 'Used by' rule_row; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-RULE-TABLE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-RULE-TABLE, 'Used by' rule_row; Ownership Map sheet Tables |
| P7 | rwb-decision | 1 | LOV-TEST-RESULT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TEST-RESULT, 'Used by' reference_version; Ownership Map sheet Tables |
| P8 | rwb-payment | 2 | LOV-MATCH | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-MATCH, 'Used by' proceeds; Ownership Map sheet Tables |
| P8 | rwb-payment | 2 | LOV-MATCH-TYPE | Closed list | Load | rwb-decision rule packages RWB-P7-E1073-CON (DP-04) | Lists sheet row LOV-MATCH-TYPE, 'Used by' payment_match_rule.match_type; Ownership Map sheet Tables |
| P8 | rwb-payment | 2 | LOV-PROCEEDS-SRC | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PROCEEDS-SRC, 'Used by' proceeds; Ownership Map sheet Tables |
| P9 | rwb-reporting | 1 | LOV-DATA-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DATA-PRODUCT, 'Used by' data_product; Ownership Map sheet Tables |
| P9 | rwb-reporting | 1 | LOV-MEASURE-DIM | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-MEASURE-DIM, 'Used by' measure_snapshot; Ownership Map sheet Tables |
| P9 | rwb-reporting | 1 | LOV-MEASURE-PUBLISH | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-MEASURE-PUBLISH, 'Used by' measure_publish; Ownership Map sheet Tables |
| P9 | rwb-reporting | 1 | LOV-MEASURE-UNIT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-MEASURE-UNIT, 'Used by' measure_definition; Ownership Map sheet Tables |
| P9 | rwb-reporting | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-AGENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-AGENT, 'Used by' agent_alert; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-AGENT-ALERT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-AGENT-ALERT, 'Used by' agent_alert; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-AGENT-RUN | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-AGENT-RUN, 'Used by' agent_run; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-AUTONOMY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-AUTONOMY, 'Used by' agent_policy; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-CONFIG-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CONFIG-STATUS, 'Used by' agent_policy; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-EVAL-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-EVAL-STATUS, 'Used by' agent_evaluation_run; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-EXTRACT-APPROACH | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-EXTRACT-APPROACH, 'Used by' agent_evaluation; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-FEEDBACK | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-FEEDBACK, 'Used by' agent_feedback; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-PRODUCT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PRODUCT, 'Used by' agent_policy; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-REGION | Source list | Read | ACE read through the P1 contract, not loaded (DP-05) | Lists sheet row LOV-REGION, 'Used by' agent_policy; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| P10 | rwb-agent | 1 | LOV-SUBJECT-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SUBJECT-TYPE, 'Used by' agent_sample; Ownership Map sheet Tables |
| S2 | rwb-treatment | 2 | LOV-APPROVAL-LEVEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-APPROVAL-LEVEL, 'Used by' approval; Ownership Map sheet Tables |
| S2 | rwb-treatment | 2 | LOV-PROPOSER | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PROPOSER, 'Used by' dp_treatment; Ownership Map sheet Tables |
| S2 | rwb-treatment | 2 | LOV-TREATMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TREATMENT, 'Used by' dp_treatment; Ownership Map sheet Tables |
| S2 | rwb-treatment | 2 | LOV-TRT-OUTCOME | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TRT-OUTCOME, 'Used by' dp_treatment; Ownership Map sheet Tables |
| S2 | rwb-treatment | 2 | LOV-TRT-SIGNATURE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-TRT-SIGNATURE, 'Used by' treatment; Ownership Map sheet Tables |
| S3 | rwb-guarantee | 3 | LOV-CLAIM-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CLAIM-STATUS, 'Used by' dp_guarantee_claim; Ownership Map sheet Tables |
| S3 | rwb-guarantee | 3 | LOV-CLAIM-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-CLAIM-TYPE, 'Used by' dp_guarantee_claim; Ownership Map sheet Tables |
| S4 | rwb-litigation | 3 | LOV-HEARING | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-HEARING, 'Used by' hearing; Ownership Map sheet Tables |
| S4 | rwb-litigation | 3 | LOV-HEARING-OUTCOME | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-HEARING-OUTCOME, 'Used by' hearing; Ownership Map sheet Tables |
| S4 | rwb-litigation | 3 | LOV-LEGAL-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-LEGAL-STATUS, 'Used by' legal_action; Ownership Map sheet Tables |
| S4 | rwb-litigation | 3 | LOV-LEGAL-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-LEGAL-TYPE, 'Used by' legal_action; Ownership Map sheet Tables |
| S5 | rwb-asset | 2 | LOV-LISTING | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-LISTING, 'Used by' listing; Ownership Map sheet Tables |
| S5 | rwb-asset | 2 | LOV-SALE-CHANNEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SALE-CHANNEL, 'Used by' listing; Ownership Map sheet Tables |
| S6 | rwb-debtsale | 3 | LOV-BUYER-CLASS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-BUYER-CLASS, 'Used by' debt_sale_lot; Ownership Map sheet Tables |
| S6 | rwb-debtsale | 3 | LOV-LOT-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-LOT-STATUS, 'Used by' debt_sale_lot; Ownership Map sheet Tables |
| S6 | rwb-debtsale | 3 | LOV-PUTBACK | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PUTBACK, 'Used by' debt_sale_account; Ownership Map sheet Tables |
| S6 | rwb-debtsale | 3 | LOV-SEGMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-SEGMENT, 'Used by' debt_sale_lot; Ownership Map sheet Tables |
| S8 | rwb-deviation | 2 | LOV-DEV-OUTCOME | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DEV-OUTCOME, 'Used by' deviation; Ownership Map sheet Tables |
| S8 | rwb-deviation | 2 | LOV-DEVIATION | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-DEVIATION, 'Used by' deviation; Ownership Map sheet Tables |
| S8 | rwb-deviation | 2 | LOV-RAISED-BY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-RAISED-BY, 'Used by' deviation; Ownership Map sheet Tables |
| S9 | rwb-partner | 4 | Partner panel | Reference table | Load | rwb-partner contract (DP-07) | Reference tables sheet row; Ownership Map sheet Tables |
| S9 | rwb-partner | 4 | LOV-INSTR-STATUS | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-INSTR-STATUS, 'Used by' partner_instruction; Ownership Map sheet Tables |
| S9 | rwb-partner | 4 | LOV-INSTRUCTION | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-INSTRUCTION, 'Used by' partner_instruction; Ownership Map sheet Tables |
| S9 | rwb-partner | 4 | LOV-PANEL | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PANEL, 'Used by' partner; Ownership Map sheet Tables |
| S9 | rwb-partner | 4 | LOV-PARTNER-TYPE | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-PARTNER-TYPE, 'Used by' partner; Ownership Map sheet Tables |
| S9 | rwb-partner | 4 | LOV-ROLE | Source list | Load | rwb-access contract RWB-P4-E1037-CON (DP-08) | Lists sheet row LOV-ROLE, 'Used by' agent_alert; Ownership Map sheet Tables |
| PLT | platform library | 0 | Feature flags | Reference table | Load | platform library (R-PREC default ruling) | Reference tables sheet row; Ownership Map sheet Tables |
| PLT | platform library | 0 | LOV-ENVIRONMENT | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-ENVIRONMENT, 'Used by' feature_flag_change; Ownership Map sheet Tables |
| PLT | platform library | 0 | LOV-OUTBOX-DELIVERY | Closed list | Load | rwb-case list read, RWB-P3-E1043-CON (DP-07) | Lists sheet row LOV-OUTBOX-DELIVERY, 'Used by' outbox_delivery; Ownership Map sheet Tables |
| Counts: Load 171 and Read 8; wave 0 3, wave 1 147, wave 2 13, wave 3 10, wave 4 6. |  |  |  |  |  |  |  |

## Sheet: Change process

| How reference data changes |  |  |
|---|---|---|
| Every change to a Workbench reference list or table is a validated load with a version. None needs a code release. Lists read from ACE are not loaded. |  |  |
| Step | Stage | What happens |
| 1 | Request | The owner of the list or table raises the change with the reason and the date it should take effect |
| 2 | Prepare | The reference data administrator prepares the new version as a load file, with a test case for each changed row |
| 3 | Validate | The load runs against the schema and the completeness checks in SIT. A load with an exception is refused whole |
| 4 | Approve | The owner approves. Risk also approves where a limit or a threshold moves |
| 5 | Load | The new version loads into production with its valid from date. No code release |
| 6 | In force | New decisions use the new version from its date. Open cases keep the version they were decided under |
| 7 | Roll back | A breach returns the previous version through the same load |
| 8 | ACE-sourced lists | A list read from ACE through a v_ace_* view is not loaded and not versioned in the Workbench. A change to its values comes from the ACE batch; the Workbench reads the new values on the next request. |
| 9 | Shared list | A list is held once, in the service of its 'Owning service (D-RCV-60)' column, and loaded there through steps 1 to 7. No other service loads a copy: it reads the list through that owner's contract, with the asOf business date, and the read records the version it used (DP-07; RWB-P3-E1043-CON). A service that needs a code the owner does not hold raises the change with the owner, not in its own schema. |

## Sheet: Key

| Key |  |  |
|---|---|---|
| What each term means. |  |  |
| Item | Term | Meaning |
| Kind | Closed list | A fixed set of codes held in the Workbench |
| Kind | Source list | Values that come from ACE through a view or from a versioned Workbench table, not a fixed list held in this workbook |
| Column | Code | The value stored in the field |
| Column | Valid from | The date the value comes into force |
| Standard | Bank TSD section T3.2 | Closed lists of values |
| Value | Read from ACE | Values come from a recovery.v_ace_* view on every request. The Workbench does not load or store them |
| Term | Source view | The recovery.v_ace_* view that supplies or confirms a list of values |
| Value | Closed list with a source view | A closed list held in the Workbench whose codes mirror an ACE list. The view confirms the codes on each release; the values do not change on the read |
| Column | Owning service (D-RCV-60) | The service, from the Ownership Map, that holds the list or the reference table in its own rwb_<name> schema |
| Column | Shared-list route (D-RCV-60) | The contract a consumer calls to read the list, with the business date; the list is never copied into the consumer's schema |
| Column | Starter mode | Load: the values are held and versioned by the owning service. Read: the values are ACE data, read through the P1 contract and never loaded |
| Term | Reference data starter | The set of lists and reference tables a service reads or holds at its first deployment, in its wave, on the Reference data starter sheet |
