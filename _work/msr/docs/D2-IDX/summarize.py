import json, collections, re

rows = json.load(open('_work/msr/docs/D2-IDX/editlog_files.json', encoding='utf-8'))
story_prefix = '04 User stories/Recovery Workbench Service Story Files v1/'
docs = collections.Counter()
storyfiles = collections.Counter()
for wp, paths in rows.items():
    for p in paths:
        if p.startswith(story_prefix):
            top = p.split('/')[1]
            storyfiles[top] += 1
        else:
            docs[p] += 1
print('=== story folder families ===')
for k, v in storyfiles.items():
    print(v, k)
print()
print('=== other written files (path, times named) ===')
for k, v in sorted(docs.items()):
    print(v, '|', k)
