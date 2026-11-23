import sys
sys.path.insert(0, '22 Microservice Realignment/checks')
sys.path.insert(0, '22 Microservice Realignment/compat')
import run_all as R
res = R.c11()
mine = [x for x in res[1] if any(k in x for k in ('E1-030', 'E1-031', 'E1-032', 'E1-034', 'E1-037'))]
print('total', len(res[1]), 'mine', len(mine))
for x in mine:
    print(x)
