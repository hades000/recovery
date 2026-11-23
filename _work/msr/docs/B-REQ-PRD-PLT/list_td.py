import glob, io

ps = sorted(glob.glob(r'_work/msr/docs/B-REQ-PRD-PLT/td-slide-*.md'), key=lambda x: int(x.split('-')[-1].split('.')[0]))
for p in ps:
    t = io.open(p, encoding='utf-8').read().strip().split('\n')
    print(p.split('\\')[-1], '|', (t[0][:100] if t else ''))
