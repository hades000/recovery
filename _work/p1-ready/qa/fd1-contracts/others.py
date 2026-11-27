import csv, re
rows = list(csv.DictReader(open('packets/requests all agents.csv', encoding='utf-8-sig')))
inc = {l.split()[1] for l in open('qa/fd1-contracts/myrequests.txt', encoding='utf-8') if l.startswith('[')}
for r in rows:
    if r['edit_id'] in inc: continue
    k = (r['file'] or '') + ' ' + (r['target'] or '')
    if re.search(r'yaml|asyncapi|API Spec|Contract Catalog|gateway-bff\.yaml', k, re.I):
        print(r['edit_id'], '|', r['file'][:150], '|', r['after'][:300])
