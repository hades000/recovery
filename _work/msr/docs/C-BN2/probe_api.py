import re, collections
t = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read()
occ = re.findall(r'/api/recovery/v1[^\s,)\]\`"\']*', t)
c = collections.Counter(occ)
for k, v in sorted(c.items()):
    print(v, k)
print('total', len(occ))
