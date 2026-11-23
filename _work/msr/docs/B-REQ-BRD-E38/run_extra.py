import importlib.util
from pathlib import Path

p = Path(r'22 Microservice Realignment/checks/run_all.py').resolve()
spec = importlib.util.spec_from_file_location('checks_rwb', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

wp = 'B-REQ-BRD-E38'
ROOT = m.ROOT
files = [ROOT / w for w in m._wp_writes(wp)]
files = [f for q in files for f in ([x for x in q.rglob('*') if x.is_file()] if q.is_dir() else [q]) if f.exists()]
print('files', len(files))
for name in ('C14', 'C15', 'C17', 'C19', 'C20', 'C16', 'C12', 'C13'):
    fn = m.ALL[name]
    res = fn(files)
    print(name, res[0], len(res[1]))
    for f in res[1][:6]:
        print('   ', f[:160])
