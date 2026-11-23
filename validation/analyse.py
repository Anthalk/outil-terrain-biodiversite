import json, sys, os
from collections import Counter, defaultdict
T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'donnees','tool_out.json')))
G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'donnees','pass2.json')))
P1 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'donnees','pass1.json')))
variant = sys.argv[1] if len(sys.argv) > 1 else 'non'
MAP = {'OIS':'Oiseaux','MAM':'Mammifères','CHI':'Chauves-souris','AMP':'Amphibiens','REP':'Reptiles'}
rows = []
res = defaultdict(Counter)
details = defaultdict(list)
for k in T:
    t = T[k][variant]; g = G[k]
    for code, grp in MAP.items():
        truth = g.get(code, 'nd')
        if truth == 'nd': continue
        lvl = t['groups'][grp]
        res[grp][(truth, lvl)] += 1
        if truth == 'oui' and lvl == 'Faible': details[grp].append(k)
    # insectes
    if g.get('INS') in ('oui','non'):
        lvl = max((t['groups'][x] for x in ('Libellules','Criquets','Papillons')), key=['Faible','Modérée','Forte'].index)
        res['Insectes'][(g['INS'], lvl)] += 1
        if g['INS']=='oui' and lvl=='Faible': details['Insectes'].append(k)
    if g.get('ZH') in ('oui','non'):
        lvl = t['themes'].get('Zone humide', 'Faible')
        res['Zone humide'][(g['ZH'], lvl)] += 1
        if g['ZH']=='oui' and lvl=='Faible': details['Zone humide'].append(k)
    if g.get('FLO') in ('oui','non'):
        lvl = t['themes'].get('Flore', 'Faible')
        res['Flore'][(g['FLO'], lvl)] += 1
        if g['FLO']=='oui' and lvl=='Faible': details['Flore'].append(k)
print(f"=== Variante : non décrit -> {variant}")
print(f"{'Groupe':<15}{'n':>3} | présents: détectés / faux faibles | absents: faibles / sur-alertes")
for grp, c in res.items():
    pos = sum(v for (tr,l),v in c.items() if tr=='oui'); neg = sum(v for (tr,l),v in c.items() if tr=='non')
    fn = c[('oui','Faible')]; tp = pos-fn; tn = c[('non','Faible')]; fp = neg-tn
    print(f"{grp:<15}{pos+neg:>3} | {pos:>2}: {tp:>2} / {fn:>2}  ({(tp/pos*100 if pos else 0):.0f} %) | {neg:>2}: {tn:>2} / {fp:>2}")
print("faux faibles :", dict(details))
# global
print("\nGlobal outil vs global avis")
ct = Counter()
for k in T:
    ga = G[k].get('GLOBAL','nd'); gt = T[k][variant]['glob']
    sig = any(G[k].get(c)=='oui' for c in ('OIS','MAM','CHI','AMP','REP','ZH','DEROG','FLO','INS'))
    ct[(ga, gt)] += 1
    if gt in ('Faible',) and (sig or ga in ('modéré','fort')): print('  faux faible global :', k, ga, {c:G[k].get(c) for c in ('OIS','CHI','AMP','REP','ZH','DEROG')})
for kk in sorted(ct): print(' ', kk, ct[kk])
