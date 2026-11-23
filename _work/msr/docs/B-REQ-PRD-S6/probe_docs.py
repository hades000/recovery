import json

d = json.load(open('_work/msr/plan/docs.json', encoding='utf-8'))
for row in d:
    s = json.dumps(row, ensure_ascii=False)
    if 'PRD' in s:
        print(s[:800])
        print()
