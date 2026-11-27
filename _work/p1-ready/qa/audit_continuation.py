from pathlib import Path
from collections import Counter
import csv,re,zipfile
from openpyxl import load_workbook
from docx import Document
import yaml

set_dir=Path('../..').resolve()
reviews=set_dir.parent/'RWB Story Review P1'/'rereview'
stage=Path('stage')
p1,=stage.glob('04 User stories/* v3/RWB-SVC-P1 rwb-source-data*')
keys={re.search(r'^# (RWB-P1-[\w-]+) ',p.read_text(encoding='utf-8-sig'),re.M)[1] for p in p1.glob('*.md')}
verdicts={}
for d in reviews.iterdir():
    if d.is_dir():
        rd,=d.glob('*review.md')
        before, verdict, *_=re.split(r'^## [A-Z]\. ',rd.read_text(encoding='utf-8-sig'),flags=re.M)
        key = d.name if d.name in keys else d.name + "-APP"
        verdicts[key]=re.search(r'\b(NOT READY|READY WITH MINOR GAPS|READY)\b',verdict)[1]
assert set(verdicts)==keys,(len(verdicts),len(keys),sorted(set(verdicts)-keys),sorted(keys-set(verdicts)))
print('Recorded re-review:', dict(Counter(verdicts.values())),flush=True)
for p in sorted(Path('packets').glob('rereview * items.csv')):
    with p.open(encoding='utf-8-sig',newline='') as f:
        counts=Counter(r['severity'] for r in csv.DictReader(f))
    print(p.name,sum(counts.values()),dict(counts),flush=True)
validated=Counter()
for p in stage.rglob('*'):
    ext=p.suffix.lower()
    if ext in {'.xlsx','.docx'}:
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None,p
        if ext=='.xlsx':
            wb=load_workbook(p,read_only=True)
            assert wb.sheetnames,p
            wb.close()
        else:
            Document(p)
    elif ext in {'.yaml','.yml'}:
        with p.open(encoding='utf-8-sig') as f:
            list(yaml.safe_load_all(f))
    else:
        continue
    validated[ext]+=1
print('Structurally valid staged files:',dict(validated),flush=True)





