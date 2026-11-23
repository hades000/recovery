import pathlib

src = pathlib.Path('04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md').read_text(encoding='utf-8').splitlines()
legacy = [l.strip() for l in src[2281:2303] if l.strip()]

p = pathlib.Path('04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3014 APP Unlock the asset as a non performing asset by rule v1.md')
f = p.read_text(encoding='utf-8').splitlines()
start = [i for i, l in enumerate(f) if l.startswith('  Scenario: AC1')][0]
fence = [i for i, l in enumerate(f) if l.strip().startswith('```') and i > start][0]
mine = [l.strip() for l in f[start:fence] if l.strip()]
print('legacy', len(legacy), 'mine', len(mine))
for l in legacy:
    print(('OK      ' if l in mine else 'MISSING '), l)
