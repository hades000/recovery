import sys
from pathlib import Path
sys.path.insert(0, '22 Microservice Realignment/checks')
sys.path.insert(0, '22 Microservice Realignment/compat')
import run_all as R
from common import ROOT

md = [str(p) for p in (ROOT / '04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration').glob('*E103[0-9]*.md')]
frag = [str(p) for p in (ROOT / '_work/msr/fragments').glob('RWB-ITG-E103*.json')]
reg = [str(ROOT / '_work/msr/gaps/B-ITG-W1-05.jsonl'), str(ROOT / '_work/msr/assumptions/B-ITG-W1-05.jsonl')]
log = [str(ROOT / '_work/msr/editlog/B-ITG-W1-05.md')]
files = md + frag + reg + log
for name, fn in [('C01', R.c01), ('C11', R.c11), ('C14', R.c14), ('C15', R.c15), ('C16', R.c16), ('C17', R.c17), ('C20', R.c20)]:
    res = fn(files)
    print(name, res[0], len(res[1]))
    for x in res[1][:20]:
        print('   ', x)
