import sys
t = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read().splitlines()
want = [17, 19, 227, 229, 247, 249, 367, 425, 499, 501, 507, 535, 751, 849, 1225, 1671, 1687, 1859, 1861, 1919, 1959, 139, 309, 1133, 1771]
for n in want:
    print('---', n)
    print(t[n - 1])
