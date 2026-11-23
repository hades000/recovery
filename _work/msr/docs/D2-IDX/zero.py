import json, glob, os

rows = json.load(open('_work/msr/docs/D2-IDX/editlog_files.json', encoding='utf-8'))
allw = [os.path.basename(p)[:-3] for p in glob.glob('_work/msr/editlog/*.md')]
zero = [w for w in allw if not rows.get(w)]
print('editlogs', len(allw), 'zero', len(zero))
print(zero[:60])
