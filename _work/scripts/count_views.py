import io
import re

txt = io.open(r'15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql', encoding='utf-8').read()
parts = re.split(r'CREATE OR REPLACE VIEW ', txt)[1:]
total = 0
for v in parts:
    name = re.match(r'([a-z_.]+)', v).group(1)
    if ' AS\n' not in v:
        continue
    body = v.split(' AS\n', 1)[1]
    m = re.search(r'\nFROM ', body)
    select = body[:m.start()] if m else body
    aliases = re.findall(r'\bAS\s+([a-z_][a-z0-9_]*)', select)
    print('%-38s %d' % (name, len(aliases)))
    total += len(aliases)
print('views', len([v for v in parts if ' AS\n' in v]), 'fields', total)
