"""Apply story-header dependency deltas to the catalog graph (dry run unless imported by apply)."""
import collections
from delta import changes, stories, cat

svc = lambda k: k.split('-')[1]
legacy = lambda k: k.split('-')[2]
suffix = lambda k: k.rsplit('-', 1)[1]
is_con = lambda k: stories[k]['Work type'] == 'Contract'

adds, rems, skipped = {}, [], []
for src in sorted(changes):
    c = changes[src]
    for tgt in c['rem']:
        if (src, tgt) in cat:
            rems.append((src, tgt, cat[(src, tgt)]))
    for tgt, field in c['add'].items():
        if (src, tgt) in cat:
            continue
        if tgt not in stories:
            skipped.append((src, tgt, 'target not in the catalog'))
            continue
        if is_con(src):
            skipped.append((src, tgt, 'CON story holds no row (R5.7 rule 1)'))
            continue
        if svc(src) == 'ITG':
            if suffix(tgt) == 'APP':
                adds[(src, tgt)] = 'I'
            else:
                skipped.append((src, tgt, 'ITG rows carry only I edges to APP stories'))
            continue
        same = svc(src) == svc(tgt)
        if svc(tgt) == 'PLT':
            cls = 'H' if is_con(tgt) else ('H' if same else 'X')
        elif same:
            team = suffix(tgt) in ('DB', 'INF', 'OPS') and legacy(src) == legacy(tgt)
            cls = 'X' if team else 'H'
        elif is_con(tgt):
            cls = 'C'
        else:
            skipped.append((src, tgt, 'another service, not a CON story: no class allows it on this story'))
            continue
        adds[(src, tgt)] = cls

new = {k: v for k, v in cat.items() if (k[0], k[1], v) not in rems}
new.update(adds)


def cycles(graph):
    out = collections.defaultdict(list)
    for (a, b), c in graph.items():
        if c == 'H' and not is_con(b):
            out[a].append(b)
    state, found = {}, []

    def visit(n, path):
        state[n] = 1
        for m in out.get(n, []):
            if state.get(m) == 1:
                found.append(path[path.index(m):] + [m] if m in path else [n, m])
            elif not state.get(m):
                visit(m, path + [m])
        state[n] = 2

    for n in list(out):
        if not state.get(n):
            visit(n, [n])
    return found, out


if __name__ == '__main__':
    print('add', len(adds), collections.Counter(adds.values()), 'remove', len(rems), collections.Counter(r[2] for r in rems))
    for r, n in collections.Counter(s[2] for s in skipped).items():
        print('skipped', n, r)
    for s in skipped:
        if 'CON story holds' not in s[2] and 'ITG rows' not in s[2]:
            print('  ', s)
    print('cycles old', cycles(cat)[0][:5])
    print('cycles new', cycles(new)[0])
