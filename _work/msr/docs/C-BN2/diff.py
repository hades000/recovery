import difflib, re
a = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read().splitlines()
b = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v4.md', encoding='utf-8').read().splitlines()
d = list(difflib.unified_diff(a, b, lineterm='', n=0))
removed = [l for l in d if l.startswith('-') and not l.startswith('---')]
added = [l for l in d if l.startswith('+') and not l.startswith('+++')]
print('removed lines', len(removed), 'added lines', len(added))
for l in removed:
    print('R|', l[:190])
