import csv, collections

rows = list(csv.DictReader(open(r'_work/data/v5_fields.csv', encoding='utf-16')))
by = collections.OrderedDict()
for r in rows:
    by.setdefault(r['object_name'], []).append((r['field_id'], r['field_name']))

want = ['recovery_case', 'case_account', 'case_party', 'assignment', 'treatment', 'interaction',
        'contact_point_ext', 'listing', 'asset_sale', 'valuation_ext', 'legal_action',
        'partner_instruction', 'partner', 'partner_user', 'debt_sale_lot', 'debt_sale_account',
        'document', 'document_field', 'decision_log_entry', 'proceeds', 'write_off', 'lov_value',
        'reference_row', 'reference_version', 'case_list_row', 'measure_snapshot',
        'reconciliation_result', 'masking_rule', 'role', 'permission', 'job_catalog',
        'data_product_load', 'case_document_check', 'document_type', 'notice', 'task']
for o in want:
    if o in by:
        fs = by[o]
        print(o, len(fs), fs[0][0], fs[-1][0])
        print('   ' + ', '.join('%s=%s' % (n, i) for i, n in fs))
    else:
        print(o, 'MISSING')
