G = ["Oiseaux","Mammifères","Chauves-souris","Amphibiens","Reptiles","Libellules","Criquets","Papillons"]
SENS = [2,1,2,2,2,0,0,0]
MAT = {2:[0,1,2,2],1:[0,1,1,2],0:[0,0,1,1]}
LV = ["Faible","Modérée","Forte"]
W = dict(A1=[3,3,3,2,2,1,2,2],A2=[1,1,2,3,1,3,0,0],V1=[2,2,1,1,2,1,2,2],V2=[1,1,1,1,0,0,0,0],V2b=[2,1,2,0,0,0,0,1],V3=[3,2,3,0,0,0,0,0],
 V4=[1,1,1,1,1,0,0,1],V4b=[2,2,1,0,2,0,1,1],V5=[1,1,1,1,1,1,1,1],V5b=[0,0,0,0,2,0,2,2],E1=[1,1,2,3,1,3,0,0],E2=[1,1,1,3,1,3,1,1],
 E3=[0,0,0,3,0,1,0,0],E4=[0,0,0,1,1,1,0,0],E4b=[1,0,0,1,0,1,0,0],B1=[0,1,0,1,2,0,1,0],B1b=[0,0,0,1,1,0,0,0],S1=[1,0,0,0,1,0,1,0],S1b=[1,0,0,0,1,0,1,1],
 B2=[1,1,1,0,1,0,0,0],B3=[2,1,3,0,1,0,0,0],B4=[3,1,3,0,2,0,0,0])
# règles actuelles (planchers) : (groupe, A, B, niveau)
FLOORS = [(0,"V3",None,2),(0,"V4",None,1),(0,"B4",None,1),(1,"V4","A1",1),(2,"V3",None,2),(2,"B3","B4",2),(2,"B4",None,1),
 (3,"E1","E2",2),(3,"E1",None,1),(3,"E3",None,1),(4,"B1","V4",2),(4,"B1","V5",2),(4,"B1",None,1),(5,"E1","E2",2),(5,"E1",None,1),
 (6,"V5",None,1),(7,"V5",None,1),(0,"V2b",None,1),(2,"V2b",None,1),(1,"V2b",None,1),(0,"S1b",None,1)]
# table de décision proposée : planchers actuels + règles d'étendue/contexte, sans score
TABLE = FLOORS + [(0,"E4b",None,1),(1,"V4b",None,1),(3,"E4b",None,1),(3,"A2","V2b",1),(3,"A2","V4b",1),
 (4,"V4b","V5b",1),(4,"S1b",None,1),(5,"E4b",None,1),(6,"V5b",None,2),(6,"S1b",None,1),(7,"V5b",None,2)]
def additive(a):
    out=[]
    for i in range(8):
        den=sum(w[i] for w in W.values()); num=sum(W[k][i] for k in a if k in W)
        sc=num/den; cls=2 if sc>=.55 else 1 if sc>=.30 else 0
        fl=max([lv for g,x,y,lv in FLOORS if g==i and x in a and (y is None or y in a)]+[0])
        out.append((MAT[SENS[i]][max(cls,fl)], sc, cls, fl))
    return out
def table(a):
    out=[]
    for i in range(8):
        lv=max([lv for g,x,y,lv in TABLE if g==i and x in a and (y is None or y in a)]+[0])
        out.append(MAT[SENS[i]][lv])
    return out
CASES = {
 "Zone d'activités périurbaine": {"A1","A2","V1","V2","V4","V5","B2"},
 "Pavillon et jardin": {"V1","V2","V4","B2","B4"},
 "Grande friche herbacée": {"A1","V1","V5","V5b","V4","V4b"},
 "Parc boisé bordant une rivière": {"A1","A2","V1","V2","V2b","V4","V4b","V5"},
 "Plateforme minérale": {"S1","S1b","B2"},
 "Ancienne ferme": {"A1","V1","V2","V3","V4","B1","B2","B3","B4","V5"},
}
for name,a in CASES.items():
    ad=additive(a); tb=table(a)
    diff=[f"{G[i]}: additif {LV[ad[i][0]]} (score {ad[i][1]:.0%}) / table {LV[tb[i]]}" for i in range(8) if ad[i][0]!=tb[i]]
    print(f"\n{name} | global additif {LV[max(x[0] for x in ad)]} | global table {LV[max(tb)]}")
    for d in diff: print("   ", d)
