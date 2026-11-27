import csv, glob, os, re, collections
BS = chr(92)
rows=[]; seen={}
mp = os.path.join('..','..','24 P1 Developer Readiness v1','Temp ID to register ID v1.csv')
mapped={r['temp_id'].strip():r['register_id'].strip() for r in csv.DictReader(open(mp,encoding='utf-8-sig'))}
for p in sorted(glob.glob('editlog/*.csv')):
  ag=os.path.basename(p)[:-4]
  for r in csv.DictReader(open(p,encoding='utf-8-sig')):
    a=(r.get('action') or '').upper()
    if a not in ('NEW-GAP','NEW-ASM'): continue
    txt=' '.join([r.get('after',''),r.get('section',''),r.get('gap_asm_refs','')])
    ids=re.findall(r'NEW-(?:GAP|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', txt) or ['(no temp id) '+ag+' '+r.get('edit_id','')]
    for t in ids:
      if t in seen: seen[t]['raised_by']+='; '+ag; continue
      d={'temp_id':t,'type':'ASM' if 'ASM' in t or a=='NEW-ASM' else 'GAP','already_mapped':mapped.get(t,''),'text':(r.get('after') or '')[:600],'file':r.get('file',''),'decision_refs':r.get('decision_refs',''),'raised_by':ag}
      seen[t]=d; rows.append(d)
with open('packets/new gaps all agents.csv','w',encoding='utf-8',newline='') as fh:
  w=csv.DictWriter(fh,fieldnames=list(rows[0].keys()),quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rows)
print(len(rows),'temp IDs; mapped:',sum(1 for r in rows if r['already_mapped']))
req=collections.Counter(); reqrows=[]
for p in glob.glob('editlog/*.csv'):
  ag=os.path.basename(p)[:-4]
  for r in csv.DictReader(open(p,encoding='utf-8-sig')):
    if (r.get('action') or '').upper()=='REQUEST':
      f=os.path.basename((r.get('file') or '').replace(BS,'/'))
      t=re.sub(r' v\d+.*$','',f)[:70]; req[t]+=1; r['agent_log']=ag; r['target']=t; reqrows.append(r)
keys=sorted({k for r in reqrows for k in r.keys()})
with open('packets/requests all agents.csv','w',encoding='utf-8',newline='') as fh:
  w=csv.DictWriter(fh,fieldnames=keys,quoting=csv.QUOTE_ALL,extrasaction='ignore'); w.writeheader(); w.writerows(reqrows)
print(sum(req.values()),'REQUEST rows')
for k,v in req.most_common(40): print(v,k)
