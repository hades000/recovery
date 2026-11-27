import os

from ed import STAGE

MD = os.path.join(STAGE, '05 Technical architecture/Recovery Workbench Service Contract Catalog v3.md')
raw = open(MD, 'rb').read()
EOL = '\r\n' if b'\r\n' in raw else '\n'
lines = raw.decode('utf-8').split(EOL)
i = next(n for n, l in enumerate(lines) if l.startswith('| GET /cases/retention-exclusions | /api'))
assert lines[i + 1].startswith('| GET /cases/closure-dates | /api')
lines[i], lines[i + 1] = lines[i + 1], lines[i]
# restore the order the previous version had (compare with the backup)
old = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Recovery Workbench Service Contract Catalog v3.md'), encoding='utf-8').read().split('\n')
o = [l.split('|')[1].strip() for l in old if l.startswith(('| GET /cases/closure-dates | /api', '| GET /cases/retention-exclusions | /api'))]
if lines[i].split('|')[1].strip() != o[0]:
    lines[i], lines[i + 1] = lines[i + 1], lines[i]
open(MD, 'wb').write(EOL.join(lines).encode('utf-8'))
print(o)
