import re, sys
sys.argv = ['x']
src = open(r'04 User stories/Recovery Workbench Build Notes Epic 2 v3.md', encoding='utf-8').read()
# replicate the first three edits only
e = [('Quartz starts this job; no person starts it. The trigger is daily and chained on an event: '
      'JOB-01 publishes LoadCompleted, event EV-26, when the ALS load for a business date has passed its checks, '
      'and JOB-08 runs after that.', 'XX', 1)]
for old, new, n in e:
    print('count', src.count(old))
t = src
for old, new, n in e:
    t = t.replace(old, new)
print([l for l in t.splitlines() if 'Quartz' in l])
