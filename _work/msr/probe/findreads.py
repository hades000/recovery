import re
from pathlib import Path
t = Path(r'_work/msr/directive/mp/out/RWB-ITG-E4045-ITG.md').read_text(encoding='utf-8')
print(re.findall(r"LOV-[A-Z0-9-]+|`[a-z]+(?:\.[a-z_]+){1,}`", t))
for s in ('E1042', 'E1043', 'parameters contract', 'reference-data contract'):
    print(s, s in t)
