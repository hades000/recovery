import json, collections, os

rows = json.load(open('_work/msr/docs/D2-IDX/editlog_files.json', encoding='utf-8'))
story_prefix = '04 User stories/Recovery Workbench Service Story Files v1/'
docs = collections.Counter()
for wp, paths in rows.items():
    for p in paths:
        if p.startswith(story_prefix):
            continue
        docs[p] += 1
print('missing:', [k for k in docs if not os.path.exists(k)])
print()
print('=== existing, grouped by folder ===')
by = collections.defaultdict(list)
for k in docs:
    if os.path.exists(k):
        by[os.path.dirname(k)].append(os.path.basename(k))
for d in sorted(by):
    print('FOLDER:', d)
    for n in sorted(by[d]):
        print('    ', n)
