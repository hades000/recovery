import os, re, collections

base = '04 User stories/Recovery Workbench Service Story Files v1'
counts = collections.Counter()
tot = 0
other = []
for d in sorted(os.listdir(base)):
    p = os.path.join(base, d)
    if not os.path.isdir(p):
        continue
    n = 0
    for f in os.listdir(p):
        if f.endswith('.md') and f.startswith('RWB '):
            n += 1
        else:
            other.append(os.path.join(p, f))
    counts[d] = n
    tot += n
print('story files', tot)
for d, n in counts.items():
    print(n, d)
print('other files', other)
