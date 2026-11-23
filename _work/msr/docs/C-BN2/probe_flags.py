import re, collections
t = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read()
c = collections.Counter(re.findall(r'\brwb\.[A-Za-z0-9_.-]+', t))
for k, v in sorted(c.items()):
    print(v, k)
