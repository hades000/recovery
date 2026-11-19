import json, io, re, collections

d = json.load(io.open(r'_work\data\hub_payload.json', encoding='utf-8'))
patterns = ['load_run', 'dq_exception', 'JOB-01', 'JOB-09', 'tracker_inventory', 'loan_account',
            'account_payment', 'contact_point', 'collections_history', 'party_product',
            'SY-DATALOAD', 'inbound load', 'file load']
for p in patterns:
    hits = []
    for doc in d['docs']:
        text = '\n'.join(s['t'] for s in doc['secs'])
        n = len(re.findall(re.escape(p), text, re.I))
        if n:
            hits.append((n, doc['file']))
    hits.sort(reverse=True)
    print(p, sum(x[0] for x in hits), hits[:6])
