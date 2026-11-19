# -*- coding: utf-8 -*-
"""Build the 133-row ACE field gap list from the LDM v6 external fields."""
import csv
import io
import openpyxl

# Field ID, Entity, Field, disposition, ace_target, read_path, note
MAP = {
    'DF-CAS-003': ('ACE reuse', 'product.product_category', 'v_ace_account.product_category', 'Via account.product_key.'),
    'DF-CAS-014': ('ACE reuse', 'account.delay_days', 'v_ace_account.days_past_due', 'Name mapped in the view.'),
    'DF-CAS-016': ('ACE reuse', 'account.total_balance', 'v_ace_account.total_balance', ''),
    'DF-CAS-046': ('ACE reuse', 'ace_case.case_business_id', 'v_ace_plan.plan_ref', 'ACE restructure case reference; confirm the identifier with the ACE team.'),
    'DF-CAS-047': ('ACE reuse', 'ace_case.current_station_name', 'v_ace_plan.plan_status', 'Derived from the ACE case station; confirm the status list.'),
    'DF-CAS-048': ('ACE reuse', 'cfsc_mg_ssme_tdr_case.approval_completed_timestamp', 'v_ace_plan.plan_status_as_of', ''),
    'DF-PTY-002': ('ACE reuse', 'customer.person_key', 'v_ace_customer.cif_no', 'ACE business key.'),
    'DF-PTY-003': ('ACE new', 'customer.party_type', 'v_ace_customer.party_type', 'Confirm whether customer.category already carries individual or juristic.'),
    'DF-PTY-004': ('ACE reuse', 'customer.first_name', 'v_ace_customer.first_name', ''),
    'DF-PTY-005': ('ACE reuse', 'customer.surname', 'v_ace_customer.last_name', ''),
    'DF-PTY-006': ('ACE new', 'customer.id_type', 'v_ace_customer.id_type', 'Not in ACE today.'),
    'DF-PTY-007': ('ACE reuse', 'customer.identification_number', 'v_ace_customer.id_no_masked', 'Held in clear in ACE. Masked in the view; role masking replaces tokenization (E1-037).'),
    'DF-PTY-008': ('ACE reuse', 'customer.birth_date', 'v_ace_customer.date_of_birth', ''),
    'DF-PTY-009': ('ACE new', 'customer.segment', 'v_ace_customer.segment', 'Not in ACE today.'),
    'DF-PTY-021': ('Recovery extension', 'recovery.party_ext.fraud_flag', 'recovery.party_ext', 'Workbench-owned flag keyed by person_key.'),
    'DF-PTY-016': ('ACE reuse', 'phone.phone_number / email.email / address.address', 'v_ace_contact.value', 'Union view with contact_type.'),
    'DF-ACC-002': ('ACE reuse', 'account.account_key', 'v_ace_account.account_no', 'ACE business key.'),
    'DF-ACC-003': ('ACE reuse', 'account.contract_number', 'v_ace_account.contract_no', ''),
    'DF-ACC-004': ('ACE reuse', 'product.product_key', 'v_ace_account.product_code', ''),
    'DF-ACC-005': ('ACE reuse', 'product.product_category_efs', 'v_ace_account.product_category_efs', ''),
    'DF-ACC-006': ('ACE new', 'account.business_unit', 'v_ace_account.business_unit', 'ALS gap.'),
    'DF-ACC-007': ('ACE reuse', 'account.contract_date', 'v_ace_account.contract_date', ''),
    'DF-ACC-008': ('ACE reuse', 'account.interest_rate', 'v_ace_account.interest_rate', 'ACE numeric(38,2); view casts to numeric(7,4).'),
    'DF-ACC-009': ('ACE new', 'account.principal_outstanding', 'v_ace_account.principal_outstanding', 'ALS gap. ACE holds total_balance only.'),
    'DF-ACC-010': ('ACE new', 'account.interest_outstanding', 'v_ace_account.interest_outstanding', 'ALS gap.'),
    'DF-ACC-011': ('ACE new', 'account.fees_outstanding', 'v_ace_account.fees_outstanding', 'ALS gap.'),
    'DF-ACC-012': ('ACE reuse', 'account.total_balance', 'v_ace_account.total_balance', ''),
    'DF-ACC-013': ('ACE reuse', 'account.accounting_balance', 'v_ace_account.accounting_balance', ''),
    'DF-ACC-014': ('ACE reuse', 'account.delay_days', 'v_ace_account.days_past_due', 'LDM and STTM worked example.'),
    'DF-ACC-015': ('ACE new', 'account.daily_bucket', 'v_ace_account.bucket', 'ALS gap. bucket_log_snapshot is monthly.'),
    'DF-ACC-016': ('ACE reuse', 'account.loan_classification', 'v_ace_account.classification', ''),
    'DF-ACC-017': ('ACE reuse', 'account.last_payment_date', 'v_ace_account.last_payment_date', ''),
    'DF-ACC-018': ('ACE reuse', 'account.next_installment_date', 'v_ace_account.next_installment_date', ''),
    'DF-ACC-019': ('ACE reuse', 'account.is_restructured', 'v_ace_account.tdr_flag', 'varchar Y/N cast to boolean in the view.'),
    'DF-ACC-020': ('ACE reuse', 'account.last_tdr_date', 'v_ace_account.last_tdr_date', ''),
    'DF-ACC-021': ('ACE reuse', 'account.core_banking_system_date', 'v_ace_account.data_as_of', 'The ACE batch date.'),
    'DF-ACC-030': ('ACE new', 'account.settlement_booked_date', 'v_ace_account.settlement_booked_date', 'ALS gap.'),
    'DF-ACC-031': ('ACE new', 'account.settlement_booked_amount', 'v_ace_account.settlement_booked_amount', 'ALS gap.'),
    'DF-ACC-024': ('ACE reuse', 'payment.pay_key', 'v_ace_payment.payment_code', 'ACE business key.'),
    'DF-ACC-025': ('ACE reuse', 'payment.pay_date', 'v_ace_payment.payment_date', 'pay_date is varchar; the view casts to date.'),
    'DF-ACC-026': ('ACE reuse', 'payment.total_amount', 'v_ace_payment.payment_amount', ''),
    'DF-ACC-027': ('ACE reuse', 'payment.pay_type', 'v_ace_payment.payment_channel', 'Confirm the code list with the ACE team.'),
    'DF-ACC-028': ('ACE reuse', 'account.core_banking_system_date', 'v_ace_payment.data_as_of', 'Read from the account snapshot; no new payment column.'),
    'DF-COL-002': ('ACE reuse', 'asset.asset_key', 'v_ace_collateral.collateral_no', 'ACE business key.'),
    'DF-COL-003': ('ACE reuse', 'asset.asset_type', 'v_ace_collateral.collateral_type', ''),
    'DF-COL-004': ('ACE new', 'collateral_detail.title_doc_no', 'v_ace_collateral_detail.title_doc_no', 'CCMS gap.'),
    'DF-COL-005': ('ACE new', 'collateral_detail.plot_no', 'v_ace_collateral_detail.plot_no', 'CCMS gap.'),
    'DF-COL-006': ('ACE new', 'collateral_detail.area_text', 'v_ace_collateral_detail.area_text', 'CCMS gap.'),
    'DF-COL-007': ('ACE new', 'collateral_detail.province', 'v_ace_collateral_detail.province', 'CCMS gap.'),
    'DF-COL-008': ('ACE new', 'collateral_detail.district', 'v_ace_collateral_detail.district', 'CCMS gap.'),
    'DF-COL-009': ('ACE new', 'collateral_detail.subdistrict', 'v_ace_collateral_detail.subdistrict', 'CCMS gap.'),
    'DF-COL-012': ('ACE new', 'collateral_detail.insured_value', 'v_ace_collateral_detail.insured_value', 'CCMS gap.'),
    'DF-COL-013': ('ACE new', 'collateral_detail.insurance_expiry', 'v_ace_collateral_detail.insurance_expiry', 'CCMS gap.'),
    'DF-COL-017': ('ACE new', 'collateral_detail.lien_rank', 'v_ace_collateral_detail.lien_rank', 'Moves from account_collateral to the collateral grain.'),
    'DF-COL-021': ('ACE new', 'valuation.appraisal_no', 'v_ace_valuation.appraisal_no', 'SVAF gap; new ACE table.'),
    'DF-COL-022': ('ACE new', 'valuation.appraisal_type', 'v_ace_valuation.appraisal_type', 'SVAF gap.'),
    'DF-COL-023': ('ACE new', 'valuation.appraised_value', 'v_ace_valuation.appraised_value', 'SVAF gap.'),
    'DF-COL-024': ('ACE new', 'valuation.forced_sale_value', 'v_ace_valuation.forced_sale_value', 'SVAF gap.'),
    'DF-COL-025': ('ACE new', 'valuation.appraisal_date', 'v_ace_valuation.appraisal_date', 'SVAF gap.'),
    'DF-COL-031': ('ACE reuse', 'asset.asset_key', 'v_ace_asset.asset_ref', 'ACE business key.'),
    'DF-COL-032': ('ACE new', 'npa_asset.asset_code', 'v_ace_npa_asset.asset_code', 'AMIS gap.'),
    'DF-COL-033': ('ACE reuse', 'asset.asset_type', 'v_ace_asset.asset_type', ''),
    'DF-COL-034': ('ACE new', 'npa_asset.transfer_in_type', 'v_ace_npa_asset.transfer_in_type', 'AMIS gap.'),
    'DF-COL-035': ('ACE new', 'npa_asset.from_segment', 'v_ace_npa_asset.from_segment', 'AMIS gap.'),
    'DF-COL-036': ('ACE new', 'npa_asset.transfer_in_date', 'v_ace_npa_asset.transfer_in_date', 'AMIS gap.'),
    'DF-COL-037': ('ACE new', 'npa_asset.book_value', 'v_ace_npa_asset.book_value', 'AMIS gap.'),
    'DF-COL-038': ('ACE new', 'npa_asset.auction_purchase_price', 'v_ace_npa_asset.auction_purchase_price', 'AMIS gap.'),
    'DF-COL-039': ('ACE new', 'npa_asset.repossessed_date', 'v_ace_npa_asset.repossessed_date', 'RPS gap.'),
    'DF-COL-040': ('ACE new', 'npa_asset.stock_date', 'v_ace_npa_asset.stock_date', 'RPS gap.'),
    'DF-TRT-009': ('ACE reuse', 'ai_recommended_plan.months', 'v_ace_plan.installments', ''),
    'DF-TRT-012': ('ACE reuse', 'cfsc_mg_ssme_tdr_case.plan_setup_completed_timestamp', 'v_ace_plan.booked_at', 'Booking date derived from the ACE plan; confirm.'),
    'DF-TRT-023': ('ACE new', 'credit_decision.nleads_ref', 'v_ace_credit_decision.nleads_ref', 'NLEADS gap; new ACE table.'),
    'DF-TRT-024': ('ACE new', 'credit_decision.credit_result', 'v_ace_credit_decision.credit_result', 'NLEADS gap.'),
    'DF-TRT-025': ('ACE new', 'credit_decision.credit_result_reason', 'v_ace_credit_decision.credit_result_reason', 'NLEADS gap.'),
    'DF-TRT-026': ('ACE new', 'credit_decision.decided_at', 'v_ace_credit_decision.decided_at', 'NLEADS gap.'),
    'DF-LEG-005': ('ACE new', 'lawsuit.lawsuit_no', 'v_ace_lawsuit.lawsuit_no', 'LIT gap.'),
    'DF-LEG-006': ('ACE new', 'lawsuit.black_case_no', 'v_ace_lawsuit.black_case_no', 'LIT gap.'),
    'DF-LEG-007': ('ACE new', 'lawsuit.red_case_no', 'v_ace_lawsuit.red_case_no', 'LIT gap.'),
    'DF-LEG-008': ('ACE new', 'lawsuit.court_name', 'v_ace_lawsuit.court_name', 'LIT gap.'),
    'DF-LEG-009': ('ACE new', 'lawsuit.claim_amount', 'v_ace_lawsuit.claim_amount', 'LIT gap.'),
    'DF-LEG-010': ('ACE new', 'lawsuit.filed_date', 'v_ace_lawsuit.filed_date', 'LIT gap.'),
    'DF-LEG-011': ('ACE new', 'lawsuit.judgment_date', 'v_ace_lawsuit.judgment_date', 'LIT gap.'),
    'DF-LEG-012': ('ACE new', 'lawsuit.judgment_amount', 'v_ace_lawsuit.judgment_amount', 'LIT gap.'),
    'DF-LEG-013': ('ACE new', 'lawsuit.lit_status', 'v_ace_lawsuit.lit_status', 'LIT gap.'),
    'DF-LEG-019': ('ACE new', 'pod_receipt.sent_date', 'v_ace_pod.sent_date', 'WIN gap.'),
    'DF-LEG-020': ('ACE new', 'pod_receipt.barcode', 'v_ace_pod.barcode', 'WIN gap.'),
    'DF-LEG-021': ('ACE new', 'pod_receipt.callback_date', 'v_ace_pod.callback_date', 'WIN gap.'),
    'DF-LEG-022': ('ACE new', 'pod_receipt.delivery_status', 'v_ace_pod.delivery_status', 'WIN gap.'),
    'DF-LEG-023': ('ACE new', 'pod_receipt.sent_type', 'v_ace_pod.sent_type', 'WIN gap.'),
    'DF-LEG-026': ('ACE new', 'hearing.hearing_date', 'v_ace_hearing.hearing_date', 'LIT gap.'),
    'DF-LEG-027': ('ACE new', 'hearing.hearing_type', 'v_ace_hearing.hearing_type', 'LIT gap.'),
    'DF-LEG-029': ('ACE new', 'hearing.next_date', 'v_ace_hearing.next_date', 'LIT gap.'),
    'DF-SAL-012': ('ACE new', 'npa_sale.contract_date', 'v_ace_npa_sale.contract_date', 'AMIS gap.'),
    'DF-SAL-013': ('ACE new', 'npa_sale.sale_date', 'v_ace_npa_sale.sale_date', 'AMIS gap.'),
    'DF-SAL-014': ('ACE new', 'npa_sale.sale_price', 'v_ace_npa_sale.sale_price', 'AMIS gap.'),
    'DF-SAL-015': ('ACE new', 'npa_sale.transfer_fee', 'v_ace_npa_sale.transfer_fee', 'AMIS gap.'),
    'DF-SAL-016': ('ACE new', 'npa_sale.specific_business_tax', 'v_ace_npa_sale.specific_business_tax', 'AMIS gap.'),
    'DF-SAL-017': ('ACE new', 'npa_sale.corporate_income_tax', 'v_ace_npa_sale.corporate_income_tax', 'AMIS gap.'),
    'DF-SAL-019': ('ACE new', 'npa_sale.incentive_amount', 'v_ace_npa_sale.incentive_amount', 'AMIS gap.'),
    'DF-SAL-035': ('ACE reuse', 'account.total_balance', 'v_ace_account.total_balance', 'Balance at the debt sale cut-off date; no new column.'),
    'DF-INT-007': ('ACE reuse', 'efs_action.action_code', 'v_ace_efs_action.action_code', ''),
    'DF-INT-008': ('ACE new', 'efs_action.contact_result', 'v_ace_efs_action.contact_result', 'Not in ACE today.'),
    'DF-DEC-006': ('ACE reuse', 'collins_score.model_version', 'v_ace_score.model_version', 'Read at decision time.'),
    'DF-DEC-022': ('ACE new', 'collins_score.model_code', 'v_ace_score.model_code', 'COLLINS score gap.'),
    'DF-DEC-023': ('ACE new', 'collins_score.model_version', 'v_ace_score.model_version', 'COLLINS score gap.'),
    'DF-DEC-024': ('ACE new', 'collins_score.score_value', 'v_ace_score.score_value', 'COLLINS score gap.'),
    'DF-DEC-025': ('ACE new', 'collins_score.estimate_value', 'v_ace_score.estimate_value', 'COLLINS score gap.'),
    'DF-DEC-026': ('ACE new', 'collins_score.route_code', 'v_ace_score.route_code', 'COLLINS score gap.'),
    'DF-DEC-027': ('ACE new', 'collins_score.scored_at', 'v_ace_score.scored_at', 'COLLINS score gap.'),
    'DF-FIN-006': ('ACE reuse', 'payment.total_amount', 'v_ace_payment.payment_amount', ''),
    'DF-FIN-007': ('ACE reuse', 'payment.pay_date', 'v_ace_payment.payment_date', 'varchar cast to date in the view.'),
    'DF-FIN-009': ('ACE reuse', 'payment.pay_key', 'v_ace_payment.payment_code', 'Confirm as the posting reference.'),
    'DF-FIN-013': ('ACE new', 'gl_write_off.amount', 'v_ace_write_off.amount', 'GL gap.'),
    'DF-FIN-016': ('ACE new', 'gl_write_off.posted_date', 'v_ace_write_off.posted_date', 'GL gap.'),
    'DF-FIN-017': ('ACE new', 'gl_write_off.responsibility_center', 'v_ace_write_off.responsibility_center', 'GL gap.'),
    'DF-FIN-018': ('ACE new', 'gl_write_off.cost_center', 'v_ace_write_off.cost_center', 'GL gap.'),
    'DF-FIN-019': ('ACE new', 'gl_write_off.gl_product', 'v_ace_write_off.gl_product', 'GL gap.'),
    'DF-REF-039': ('ACE new', 'iam_group.entra_group', 'v_ace_iam_group.entra_group', 'Entra ID gap; new ACE table. ACE owns the group-to-role mapping because ACE performs the sign-in.'),
    'DF-INT-031': ('ACE reuse', 'efs_action.account_key', 'v_ace_efs_action.account_no', ''),
    'DF-INT-032': ('ACE reuse', 'efs_action.action_id', 'v_ace_efs_action.efs_record_key', ''),
    'DF-INT-033': ('ACE reuse', 'efs_action.action_timestamp', 'v_ace_efs_action.contact_at', ''),
    'DF-INT-034': ('ACE reuse', 'efs_action.action_code', 'v_ace_efs_action.action_code', ''),
    'DF-INT-035': ('ACE new', 'efs_action.action_contact_status', 'v_ace_efs_action.action_contact_status', 'Not in ACE today.'),
    'DF-INT-036': ('ACE new', 'efs_action.contact_result', 'v_ace_efs_action.contact_result', 'Shared with DF-INT-008.'),
    'DF-INT-037': ('ACE reuse', 'efs_action.settle_total_amount', 'v_ace_efs_action.promise_amount', ''),
    'DF-INT-038': ('ACE reuse', 'efs_action.settlement_due_date', 'v_ace_efs_action.promise_date', ''),
    'DF-TRT-050': ('ACE reuse', 'account.contract_number', 'v_ace_account.contract_no', ''),
    'DF-TRT-051': ('ACE reuse', 'account.contract_date', 'v_ace_account.contract_date', ''),
    'DF-PTY-024': ('ACE new', 'party_product.product_type', 'v_ace_party_product.product_type', 'SCBPDM gap; new ACE table.'),
    'DF-PTY-025': ('ACE new', 'party_product.account_key', 'v_ace_party_product.account_no', 'SCBPDM gap.'),
    'DF-PTY-026': ('ACE new', 'party_product.product_status', 'v_ace_party_product.product_status', 'SCBPDM gap.'),
    'DF-PTY-027': ('ACE new', 'party_product.business_date', 'v_ace_party_product.data_as_of', 'SCBPDM gap.'),
    'DF-DOC-103': ('ACE new', 'esign_request.external_ref', 'v_ace_esign.external_ref', 'EasyApp gap; new ACE table. ACE receives the signature call-back, so the reference belongs with the ingestion, not on the Workbench document.'),
}

p = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb['Fields']
rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[0]]
ext = [r for r in rows if r[11] and str(r[11]).strip() not in ('Workbench', 'None', '')]

missing = [r[0] for r in ext if r[0] not in MAP]
extra = [k for k in MAP if k not in {r[0] for r in ext}]
print('ldm external', len(ext), 'mapped', len(MAP), 'missing', missing, 'extra', extra)

out = []
for r in ext:
    fid, ent, field = r[0], r[1], r[2]
    dispo, target, view, note = MAP[fid]
    out.append([fid, ent, field, r[3], r[11], r[12], dispo, target, view, note])

with io.open(r'_work\data\fields.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Field ID', 'Entity', 'Field', 'Data type', 'Source system', 'Source field',
                'Disposition', 'ACE object column', 'Read path', 'Note'])
    w.writerows(out)

from collections import Counter
c = Counter(x[6] for x in out)
print(c)
print('ACE new fields', c['ACE new'])
