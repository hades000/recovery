"""Build Recovery Workbench API Specification v3.yaml from v2.yaml (D-RCV-35, ACE DB alignment).

usage: python api_build_v3.py V2.yaml V3.yaml
v2 is a yaml.safe_dump(sort_keys=False, allow_unicode=True, width=140) with a one-line comment
header, so v3 is written the same way.
"""
import re
import sys

import yaml

SRC, DST = sys.argv[1:3]
d = yaml.safe_load(open(SRC, encoding='utf-8'))
P = d['paths']
S = d['components']['schemas']
log = []

KEY = {'type': 'string', 'maxLength': 255}


def key(desc):
    return dict(KEY, description=desc)


def rename(schema, old, new, value=None):
    """Rename a property in place, keeping its position; update required."""
    s = S[schema]
    props = s['properties']
    out = {}
    for k, v in props.items():
        if k == old:
            out[new] = value if value is not None else v
        else:
            out[k] = v
    assert old in props, (schema, old)
    s['properties'] = out
    if 'required' in s:
        s['required'] = [new if r == old else r for r in s['required']]
    log.append('%s.%s -> %s' % (schema, old, new))


def drop_prop(schema, name):
    s = S[schema]
    del s['properties'][name]
    if 'required' in s:
        s['required'] = [r for r in s['required'] if r != name]
    log.append('%s.%s removed' % (schema, name))


def set_desc(op, text):
    """Set an operation description, placed before responses as in v2."""
    if 'description' in op:
        op['description'] = text
        return
    items = list(op.items())
    op.clear()
    for k, v in items:
        if k == 'responses':
            op['description'] = text
        op[k] = v


def rename_path(old, new, pmap):
    global P
    out = {}
    for k, v in P.items():
        if k == old:
            for m, op in v.items():
                for prm in op.get('parameters', []):
                    if prm['name'] in pmap:
                        prm['name'], prm['schema'], desc = pmap[prm['name']]
                        prm['description'] = desc
            for op in v.values():
                op['operationId'] = op['operationId'].replace('Assetid', 'Assetkey')
            out[new] = v
        else:
            out[k] = v
    d['paths'] = P = out
    log.append('path %s -> %s' % (old, new))


# ---------------------------------------------------------------- info
d['info']['version'] = '3.0.0'
d['info']['description'] = (
    'Endpoints of the recovery module in the ACE service. Every endpoint checks the role, the capability area, the right and the scope. '
    'Version 3.0.0, 15 November 2026: re-based on the ACE database under D-RCV-35 (U1 to U5). The Workbench takes no inbound source data; '
    'source records are read only through the SELECT-only recovery.v_ace_* views and linked by ACE business keys (account_key, person_key, '
    'payment_code, contact_key, asset_key, valuation_key) with no foreign key into ACE. Removed: the tracker endpoints (/admin/trackers and '
    'its sub-paths, RWB-E1-005, E1-010, E1-012; trackers are retired through the Cutover plan), source load reruns, the data quality '
    'exception list (RWB-E1-006; ACE ingestion checks) and the manual interface retirement sign-off. Re-keyed: CaseAccount.accountKey, '
    'CaseParty.personKey, Proceeds.paymentCode and the other links in Change Register v1 Appendix B. '
    '(C) Siam Commercial Bank and Henka Pte Ltd')
log.append('info.version 1.0.0 -> 3.0.0; description D-RCV-35 note')

# ---------------------------------------------------------------- removed paths
REMOVE_PATHS = ['/admin/trackers', '/admin/trackers/{trackerId}/loads', '/admin/trackers/{trackerId}/sign-off',
                '/admin/trackers/{trackerId}/retire', '/admin/trackers/retirement-report',
                '/admin/data-quality/exceptions', '/admin/interfaces/{interfaceCode}/manual-retirement']
for p in REMOVE_PATHS:
    del P[p]
    log.append('path %s removed' % p)

# ---------------------------------------------------------------- jobs: Workbench jobs only
op = P['/admin/jobs']['get']
op['summary'] = 'List Workbench jobs and outbound files with status'
set_desc(op, 'D-RCV-35: lists Workbench-owned jobs only (case intake from the ACE batch, outbound files, timers, measures, '
             'reconciliation, retention). Source loads are not Workbench jobs: ACE ingestion runs them and their completion is read '
             'from recovery.v_ace_batch_status (ace_batch_run). The type filter takes a job_catalog job ID.')
op = P['/admin/jobs/{jobId}/rerun']['post']
op['summary'] = 'Rerun a failed Workbench job'
set_desc(op, 'D-RCV-35: reruns a failed Workbench job from the job catalog, for example case intake for a business date or an '
             'outbound file. There is no source load rerun: a late or failed source batch is rerun by ACE ingestion, and the Workbench '
             'picks it up from ace_batch_run. A job that is not in the Workbench job catalog returns 404.')
S['Job']['description'] = 'A run of a Workbench job from the job catalog. Source loads are ACE ingestion runs and are not listed.'
S['Job']['properties']['type']['description'] = 'Job catalog job ID of the Workbench job'
S['Job']['properties']['businessDate']['description'] = 'ACE business date the run worked on'
S['Job']['properties']['checks']['description'] = 'Control totals of the run, for example cases created against v_ace_account rows'
log.append('/admin/jobs and /admin/jobs/{jobId}/rerun re-worded to Workbench jobs; Job described')

# ---------------------------------------------------------------- data products: view-based design
op = P['/data-products/freshness']['get']
op['summary'] = 'Read the freshness stamp of each data product from the ACE batch business date'
set_desc(op, 'D-RCV-35: the stamp is data_product_load, written from recovery.v_ace_batch_status over ACE ace_batch_run '
             '(RWB-ACE-001). The Workbench loads nothing: businessDate is the ACE business date of the last completed source '
             'batch, sourceExtractedAt its completion time, loadedAt when the Workbench recorded the stamp. A product is stale when '
             'no completed batch exists for the expected business date (RWB-E1-015).')
fp = S['DataProductFreshness']['properties']
S['DataProductFreshness']['description'] = 'Freshness of a data product, from data_product_load sourced from ace_batch_run.'
fp['productCode']['description'] = 'Data product code'
fp['productName']['description'] = 'Data product name'
new_fp = {}
for k, v in fp.items():
    new_fp[k] = v
    if k == 'productName':
        new_fp['sourceSystem'] = {'type': 'string', 'description': 'System ACE ingested the data from, as in ace_batch_run.source_system'}
fp = S['DataProductFreshness']['properties'] = new_fp
fp['businessDate']['description'] = 'ACE business date of the last completed batch (ace_batch_run.business_date)'
fp['sourceExtractedAt']['description'] = 'When ACE completed the source batch (ace_batch_run.completed_at)'
fp['loadedAt']['description'] = 'When the Workbench recorded the freshness stamp from the ACE batch record'
fp['status']['description'] = 'Current or stale'
fp['staleSince']['description'] = 'First business date with no completed ACE batch'
log.append('DataProductFreshness: sourceSystem added; fields described from ace_batch_run')

op = P['/data-products/{productCode}/records']['get']
op['summary'] = 'Read the rows of one data product for a case through the ACE views, masked by role, with its freshness stamp'
set_desc(op, 'D-RCV-35: source rows are read live through the recovery.v_ace_* views (for example v_ace_account, v_ace_payment, '
             'v_ace_customer, v_ace_contact, v_ace_collateral), filtered by the case\'s account_key and person_key values; Workbench '
             'rows come from the recovery tables and the extension tables. Nothing is copied. Masking is applied by role (RWB-E1-037) '
             'and every read is written to the access log.')
S['DataProductRecord']['description'] = 'One row of a data product, from a v_ace_* view or a Workbench table.'
S['DataProductRecord']['properties']['recordId']['description'] = (
    'Business key of the row: an ACE key such as account_key, person_key, payment_code, contact_key or asset_key, or the Workbench id')
S['DataProductRecord']['properties']['entity']['description'] = 'The v_ace_* view or the Workbench table the row is read from'

op = P['/admin/data-products']['get']
set_desc(op, 'D-RCV-35: the catalog lists each data product with its read path. Source products name ACE as the system of record '
             '("ACE (ingested from X)") and the v_ace_* views they read; Workbench products name the recovery tables.')
cp = S['DataProductCatalogEntry']['properties']
cp['systemOfRecord']['description'] = 'ACE (ingested from the source system) for source data, or the Workbench'
cp['refreshCycle']['description'] = 'Refresh cycle, as ACE ingests the source, or On change for Workbench data'
new_cp = {}
for k, v in cp.items():
    new_cp[k] = v
    if k == 'systemOfRecord':
        new_cp['sourceViews'] = {'type': 'array', 'items': {'type': 'string'},
                                 'description': 'The recovery.v_ace_* views the product is read through; empty for Workbench data'}
S['DataProductCatalogEntry']['properties'] = new_cp
log.append('DataProductCatalogEntry: sourceViews added; DataProductRecord described')

op = P['/admin/data-dictionary/fields']['get']
set_desc(op, 'D-RCV-35: reads v_data_dictionary over sys_objects and sys_fields: 122 objects (92 tables and 30 v_ace_* views) and '
             '1,366 fields. A view field carries sourceSystem ACE and sourceField the ACE column it maps (for example '
             'public.account.delay_days for days_past_due). The sourceSystem filter takes ACE or WORKBENCH.')
dp = S['DataDictionaryField']['properties']
dp['entity']['description'] = 'Workbench table or v_ace_* view'
dp['sourceSystem']['description'] = 'ACE for a field read through a v_ace_* view; WORKBENCH for a Workbench field'
dp['sourceField']['description'] = 'The ACE table and column the view field maps, for example public.account.delay_days'
dp['interfaceId']['description'] = 'Outbound interface that publishes the field, if any; no inbound interface remains'
log.append('DataDictionaryField descriptions re-worded to views')

op = P['/admin/data-contracts']['get']
op['summary'] = 'List data contracts: the ACE view contract and the outbound interfaces'
set_desc(op, 'D-RCV-35: there is no inbound load contract. The ACE contract is the v_ace_* view list and the RWB-ACE-001 field '
             'appendix, confirmed by the ACE team lead (DL43); the other contracts cover outbound interfaces only.')
S['DataContract']['properties']['sourceSystem']['description'] = 'ACE for the view contract, or the receiving system of an outbound interface'
S['DataContract']['properties']['interfaceIds']['description'] = 'Outbound interfaces the contract covers; empty for the ACE view contract'
P['/admin/data-contracts/{contractId}']['patch']['summary'] = "Record the system owner's confirmation of a data contract (the ACE team lead for the view contract)"
log.append('/admin/data-contracts re-worded to the ACE view contract and outbound interfaces')

# ---------------------------------------------------------------- re-keys (Change Register Appendix B)
rename('Case', 'primaryCustomerId', 'primaryPersonKey',
       key('ACE person_key of the borrower the case is opened for (v_ace_customer); business key, no foreign key'))
S['CaseAccount']['description'] = 'Links each ACE account to the case it is recovered under.'
rename('CaseAccount', 'accountId', 'accountKey',
       key('ACE account_key of the account (v_ace_account); business key, no foreign key'))
rename('CaseParty', 'partyId', 'personKey',
       key('ACE person_key of the customer (v_ace_customer); business key, no foreign key'))
rename('Notice', 'partyId', 'personKey', key('ACE person_key of the customer the notice is addressed to'))
rename('NoticeRequest', 'partyId', 'personKey', dict(KEY))
rename('Listing', 'assetId', 'assetKey', key('ACE asset_key of the asset offered (v_ace_npa_asset)'))
rename('AssetSale', 'assetId', 'assetKey', key('ACE asset_key of the asset sold (v_ace_npa_asset)'))
rename('Interaction', 'partyId', 'personKey', key('ACE person_key of the customer (v_ace_customer)'))
rename('Interaction', 'contactPointId', 'contactKey',
       key('The contact point reached, as the v_ace_contact composite key contact_type:key (PHONE, EMAIL or ADDRESS); '
           'the number or address is masked by role'))
S['Interaction']['properties']['sourceSystem']['description'] = 'EFS for collections history read from ACE (v_ace_efs_action), or the Workbench'
rename('Document', 'partyId', 'personKey', key('ACE person_key of the customer the document belongs to'))
rename('Proceeds', 'accountPaymentId', 'paymentCode',
       key('ACE payment_code of the payment matched (v_ace_payment); business key, no foreign key'))
rename('SignatureRequestCreate', 'partyId', 'personKey', dict(KEY))
rename('SignatureRequest', 'partyId', 'personKey', dict(KEY))
rename('MessageRequest', 'partyId', 'personKey', dict(KEY))
rename('CustomerProduct', 'partyId', 'personKey', dict(KEY))
S['CustomerProducts']['description'] = 'Other products of the case borrowers, read through v_ace_party_product.'
rename('MatchRequest', 'accountId', 'accountKey', dict(KEY))
arr = {'type': 'array', 'items': dict(KEY), 'description': 'ACE account_key values (v_ace_account)'}
for n in ('TreatmentRequest', 'LegalActionRequest', 'LotRequest'):
    rename(n, 'accountIds', 'accountKeys', dict(arr))

# Asset and valuation: the copy tables leave; read through v_ace_npa_asset, v_ace_valuation and valuation_ext
S['Asset']['description'] = ('An asset the bank holds after repossession, deed in lieu or auction purchase, read from ACE through '
                             'v_ace_npa_asset (AMIS, RPS).')
rename('Asset', 'id', 'assetKey', key('ACE asset_key of the held asset; business key'))
drop_prop('Asset', 'collateralId')
S['Asset']['properties']['caseId']['description'] = 'The recovery_case the asset is recovered under'
S['Valuation']['description'] = ('An appraisal of an asset, read from ACE through v_ace_valuation (SVAF), with the Workbench decision '
                                 'from valuation_ext.')
rename('Valuation', 'id', 'valuationKey', key('ACE valuation_key of the appraisal; business key'))
drop_prop('Valuation', 'collateralId')
rename('Valuation', 'assetId', 'assetKey', key('ACE asset_key of the asset appraised'))
vp = S['Valuation']['properties']
vp['valuerPartnerId']['description'] = 'The valuer, from valuation_ext'
vp['accepted']['description'] = 'True once accepted for the route decision, from valuation_ext'
vp['staleFlag']['description'] = 'True when the appraisal is older than appraisal.max.age at the ACE business date, from valuation_ext'
vp['ageDays']['description'] = 'Age of the appraisal in days at the ACE business date, from valuation_ext'
vr = S['ValuationRequest']
vr['description'] = 'Order a valuation, or accept an ACE appraisal. The appraised value arrives through ACE ingestion, not through this request.'
vr['properties'] = {
    'appraisalType': vr['properties']['appraisalType'],
    'valuerId': vr['properties']['valuerId'],
    'valuationKey': key('ACE valuation_key of the appraisal to accept; empty when ordering'),
    'accepted': {'type': 'boolean', 'description': 'True to accept the appraisal for the route decision'},
}
log.append('ValuationRequest: value and valuedOn removed; valuationKey and accepted added')

ak = ('assetKey', {'type': 'string', 'maxLength': 255}, 'ACE asset_key of the held asset (v_ace_npa_asset)')
for old in ('/assets/{assetId}', '/assets/{assetId}/valuations', '/assets/{assetId}/listings'):
    rename_path(old, old.replace('{assetId}', '{assetKey}'), {'assetId': ak})
op = P['/assets/{assetKey}/valuations']['post']
op['summary'] = 'Order a valuation, or accept an ACE appraisal for the route decision'
set_desc(op, 'D-RCV-35: SVAF appraisals arrive through ACE ingestion and are read through v_ace_valuation. This request orders a '
             'valuation from a valuer or records the Workbench acceptance in valuation_ext; it never writes an appraised value.')

op = P['/cases/{caseId}/interactions']['get']
op['description'] = op['description'].replace('contactPointId (uuid)', 'contactKey (string, composite contact_type:key from v_ace_contact)')
op = P['/proceeds/{proceedsId}/match']['post']
op['summary'] = 'Match a receipt to a case and an ACE account'

# ---------------------------------------------------------------- inbound NLEADS / EasyApp results now arrive through ACE
# TSD P2 v3 retires API-P2-013 (inbound credit result) and API-P2-014 (manual retirement sign-off).
item = P['/treatments/{treatmentId}/credit-result']
old = item.pop('post')
item['get'] = {
    'tags': old['tags'],
    'summary': 'Read the NLEADS credit decision for the treatment from ACE',
    'operationId': 'getTreatmentsTreatmentidCreditResult',
    'x-module': old['x-module'],
    'x-capability': {'area': 'Treatment and offer', 'right': 'R'},
    'x-first-release': old['x-first-release'],
    'parameters': old['parameters'],
    'description': ('D-RCV-35 and TSD P2 v3 (API-P2-013 retired): the Workbench no longer receives or records the NLEADS result. '
                    'NLEADS lands in ACE credit_decision (RWB-ACE-001) and this endpoint reads it through v_ace_credit_decision for '
                    "the treatment's account_key and nleadsRef. No decision returns 404 MSG-P3-024 until ACE holds it."),
    'responses': {
        '200': {'description': 'Success', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/CreditResult'}}}},
        '401': {'$ref': '#/components/responses/E401'},
        '403': {'$ref': '#/components/responses/E403'},
        '404': {'$ref': '#/components/responses/E404'},
        '503': {'$ref': '#/components/responses/E503'},
    },
}
S['CreditResult'] = {
    'type': 'object',
    'description': 'NLEADS credit decision as ingested into ACE, read through v_ace_credit_decision. Read only.',
    'properties': {
        'creditDecisionKey': key('ACE credit_decision_key; business key'),
        'accountKey': key('ACE account_key the decision is for'),
        'nleadsRef': {'type': 'string', 'maxLength': 30, 'description': 'NLEADS reference of the credit approval'},
        'result': {'type': 'string', 'maxLength': 10, 'description': 'Approved or refused, from NLEADS'},
        'reason': {'type': 'string', 'maxLength': 1000, 'description': 'Reason given by NLEADS; present when refused'},
        'decidedAt': {'type': 'string', 'format': 'date-time', 'description': 'When NLEADS gave the decision'},
        'sourceSystem': {'type': 'string', 'description': 'NLEADS'},
        'dataAsOf': {'type': 'string', 'format': 'date', 'description': 'ACE business date of the row'},
    },
}
tp = S['Treatment']['properties']
tp['nleadsRef']['description'] = 'NLEADS reference of the credit approval, read from v_ace_credit_decision; read only'
tp['creditResult']['description'] = 'Approved or refused, read from v_ace_credit_decision; read only'
tp['creditResultReason']['description'] = 'Reason given by NLEADS, read from v_ace_credit_decision; read only'
tp['creditResultAt']['description'] = 'When NLEADS gave the decision, read from v_ace_credit_decision; read only'
for f in ('nleadsRef', 'creditResult', 'creditResultReason', 'creditResultAt'):
    tp[f]['readOnly'] = True
log.append('POST /treatments/{treatmentId}/credit-result -> GET (read of v_ace_credit_decision); CreditResult reshaped '
           '(approvalLevel, resultDate removed; creditDecisionKey, accountKey, decidedAt, sourceSystem, dataAsOf added); '
           'Treatment credit fields read only')

sp = S['SignatureRequest']['properties']
sp['externalRef'].update({'description': 'EasyApp reference, read from v_ace_esign (EasyApp lands in ACE esign_request); read only',
                          'readOnly': True})
sp['status']['description'] = ('Signature status; for e-signature it follows v_ace_esign.status, for branch or paper it is recorded '
                               'through POST /signature-requests/{requestId}/result')
op = P['/signature-requests/{requestId}/result']['post']
set_desc(op, 'Branch and paper signatures only. EasyApp e-signature results are not received by the Workbench: they land in ACE '
             'esign_request and are read through v_ace_esign (D-RCV-35). An e-signature request returns 409.')
S['Role']['properties']['entraGroup'].update({'description': 'Entra ID group mapped to the role, read from v_ace_iam_group; read only',
                                              'readOnly': True})
log.append('SignatureRequest.externalRef and Role.entraGroup read only from v_ace_esign / v_ace_iam_group; '
           'signature result endpoint limited to branch and paper')

# ---------------------------------------------------------------- removed schemas
REMOVE_SCHEMAS = ['Tracker', 'TrackerField', 'TrackerSignOff', 'TrackerRetirement', 'TrackerRetirementReport',
                  'TrackerStatusItem', 'TrackerConfirmation', 'DataQualityException', 'InterfaceSignoff',
                  'ManualRetirementRequest']
for n in REMOVE_SCHEMAS:
    del S[n]
    log.append('schema %s removed' % n)

# ---------------------------------------------------------------- validate refs
text = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=140)
refs = set(re.findall(r"\$ref: '?#/components/(\w+)/(\w+)'?", text))
dangling = sorted('%s/%s' % r for r in refs if r[1] not in d['components'].get(r[0], {}))
used = {r[1] for r in refs if r[0] == 'schemas'}
orphans = sorted(n for n in S if n not in used)
stale = re.findall(r'loan_account|account_payment|contact_point(?!_ext)|tracker|DataQualityException|InterfaceSignoff', text, re.I)
assert not dangling, dangling

header = '# Recovery Workbench API specification v3. Henka Group, 15 November 2026.\n'
with open(DST, 'w', encoding='utf-8', newline='') as f:
    f.write(header + text)

ops = sum(1 for v in d['paths'].values() for m in v if m in ('get', 'post', 'put', 'patch', 'delete'))
print('\n'.join(log))
print('paths', len(d['paths']), 'operations', ops, 'schemas', len(S))
print('refs', len(refs), 'dangling', dangling)
print('unreferenced schemas', orphans)
print('stale terms', stale)
