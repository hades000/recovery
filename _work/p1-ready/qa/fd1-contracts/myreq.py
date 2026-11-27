import csv, re

BS = chr(92)
rows = list(csv.DictReader(open('packets/requests all agents.csv', encoding='utf-8-sig')))
out = []
for r in rows:
    k = (r['file'] or '').replace(BS, '/')
    if re.search(r'^04 User stories|^C:.*04 User stories|^RWB[ -]P\d.*(CON|APP|OPS)', k):
        continue
    if re.search(r'\.yaml|asyncapi|API Spec|Contract Catalog|rwb-case contract|contract owner', k, re.I):
        out.append(r)
print(len(out))
with open('qa/fd1-contracts/myrequests.txt', 'w', encoding='utf-8') as o:
    for i, r in enumerate(out):
        o.write(f"[{i}] {r['edit_id']} {r['agent']} act={r['action']}\n  FILE: {r['file']}\n  SEC: {r['section']}\n  BEFORE: {r['before']}\n  AFTER: {r['after']}\n  F: {r['finding_refs']} | D: {r['decision_refs']} | G: {r['gap_asm_refs']}\n")
