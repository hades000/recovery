import re
t = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read()
blocks = re.split(r'(?m)^## (RWB-E2-\d+) ', t)
print('parts', len(blocks))
keys = blocks[1::2]
print(len(keys), keys)
no_module = []
for i in range(1, len(blocks), 2):
    body = blocks[i + 1]
    m = re.search(r'(?m)^Module: .*$', body)
    if not m:
        no_module.append(blocks[i])
    else:
        print(blocks[i], '|', m.group(0))
print('no module:', no_module)
