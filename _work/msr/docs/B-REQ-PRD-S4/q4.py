import json
q = json.load(open('_work/msr/wp/queue-B.json', encoding='utf-8'))
for item in q:
    if item['wp'] == 'B-REQ-PRD-S4':
        print(json.dumps(item, indent=1, ensure_ascii=False))
print('---- count', len(q))
