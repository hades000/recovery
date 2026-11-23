import sys
from pathlib import Path

sys.path.insert(0, str(Path('22 Microservice Realignment/checks').resolve()))
sys.path.insert(0, str(Path('22 Microservice Realignment/compat').resolve()))
import run_all as R

wp = 'B-TESTDOC-39'
files = [R.ROOT / w for w in R._wp_writes(wp)]
files = [f for p in files for f in ([x for x in p.rglob('*') if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print('files:', len(files))
for n in ('C14', 'C17', 'C20'):
    res = R.ALL[n](files)
    print(n, res[0], len(res[1]))
    for x in res[1][:10]:
        print('   ', x)
