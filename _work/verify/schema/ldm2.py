import openpyxl, sys
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ents = [r for r in wb['Entities'].iter_rows(min_row=5, values_only=True) if r[0]]
flds = [r for r in wb['Fields'].iter_rows(min_row=5, values_only=True) if r[0]]
d = sys.argv[2]
dbo = set(l.strip() for l in open(d+'/db_obj.txt', encoding='utf-8') if l.strip())
dbf = [l.rstrip('\n').split('|') for l in open(d+'/db_fld.txt', encoding='utf-8') if l.strip()]
lo = set(r[0] for r in ents)
print('LDM entities', len(ents), 'unique', len(lo), 'DB', len(dbo))
print('in LDM not DB', sorted(lo-dbo)[:10], 'in DB not LDM', sorted(dbo-lo)[:10])
lf = set((r[0], r[1], r[2]) for r in flds); df = set((a,b,c) for a,b,c,_ in dbf)
print('LDM fields', len(flds), 'unique', len(lf), 'DB', len(dbf))
print('in LDM not DB', sorted(lf-df)[:10]); print('in DB not LDM', sorted(df-lf)[:10])
lp = {(r[0]): r[4] for r in flds}; mism = [(a, lp.get(a), p) for a,b,c,p in dbf if lp.get(a) != p]
print('physical_type mismatch LDM vs DB', len(mism), mism[:5])
fsum = sum(int(r[7] or 0) for r in ents); print('sum Entities.Fields', fsum)
from collections import Counter
c = Counter(r[1] for r in flds); bad = [(r[0], r[7], c[r[0]]) for r in ents if int(r[7] or 0) != c[r[0]]]
print('entity field-count mismatches', bad[:10])
