"""Moteur V3 : table de décision (document « Table de décision de l'outil terrain biodiversité »)."""
GROUPS = ["Oiseaux", "Mammifères", "Chauves-souris", "Amphibiens", "Reptiles", "Libellules", "Criquets", "Papillons"]
VERTEBRES = GROUPS[:5]
LV = ["Faible", "Modérée", "Forte"]

# Poids V2 conservés pour le seul signal d'alerte
W = dict(A1=[3,3,3,2,2,1,2,2], A2=[1,1,2,3,1,3,0,0], V1=[2,2,1,1,2,1,2,2], V2=[1,1,1,1,0,0,0,0], V2b=[2,1,2,0,0,0,0,1],
         V3=[3,2,3,0,0,0,0,0], V4=[1,1,1,1,1,0,0,1], V4b=[2,2,1,0,2,0,1,1], V5=[1,1,1,1,1,1,1,1], V5b=[0,0,0,0,2,0,2,2],
         E1=[1,1,2,3,1,3,0,0], E2=[1,1,1,3,1,3,1,1], E3=[0,0,0,3,0,1,0,0], E4=[0,0,0,1,1,1,0,0], E4b=[1,0,0,1,0,1,0,0],
         B1=[0,1,0,1,2,0,1,0], B1b=[0,0,0,1,1,0,0,0], S1=[1,0,0,0,1,0,1,0], S1b=[1,0,0,0,1,0,1,1],
         B2=[1,1,1,0,1,0,0,0], B3=[2,1,3,0,1,0,0,0], B4=[3,1,3,0,2,0,0,0])
PARENT = dict(V2b="V2", V3="V2", V4b="V4", V5b="V5", E2="E1", E4b="E4", B1b="B1", B3="B2", B4="B2", S1b="S1")
DETERMINANTS = ["V3", "B3", "B4", "E1", "E3", "E4", "B1", "K1"]

# (id, groupe, condition, niveau 1|2, contrainte)
def R(*a): return a
RULES = [
    R("OI1", "Oiseaux", lambda y, a: y("V3"), 2, "C2"),
    R("OI2", "Oiseaux", lambda y, a: y("F1a") or y("I1"), 2, "C3"),
    R("OI3", "Oiseaux", lambda y, a: y("F1b"), 1, "C1"),
    R("OI13", "Oiseaux", lambda y, a: y("F9"), 2, "C2"),
    R("OI4", "Oiseaux", lambda y, a: y("B4"), 1, "C2"),
    R("OI5", "Oiseaux", lambda y, a: y("V4"), 1, "C1"),
    R("OI6", "Oiseaux", lambda y, a: y("V2b"), 1, "C1"),
    R("OI7", "Oiseaux", lambda y, a: y("S1b"), 1, "C3"),
    R("OI8", "Oiseaux", lambda y, a: y("S1") and (y("A2") or y("E1") or y("E3")), 1, "C3"),
    R("OI9", "Oiseaux", lambda y, a: y("E4b"), 1, "C3"),
    R("OI10", "Oiseaux", lambda y, a: y("S2"), 1, "C2"),
    R("MA1", "Mammifères", lambda y, a: y("K1"), 1, "C3"),
    R("MA2", "Mammifères", lambda y, a: y("V4") and y("A1"), 1, "C1"),
    R("MA3", "Mammifères", lambda y, a: y("V4b"), 1, "C1"),
    R("MA4", "Mammifères", lambda y, a: y("V2b"), 1, "C1"),
    R("MA5", "Mammifères", lambda y, a: y("F3") or y("I5"), 1, "C1"),
    R("CS1", "Chauves-souris", lambda y, a: y("F2") or y("I2"), 2, "C3"),
    R("CS2", "Chauves-souris", lambda y, a: y("V3"), 2, "C2"),
    R("CS3", "Chauves-souris", lambda y, a: y("B3") and y("B4"), 2, "C2"),
    R("CS4", "Chauves-souris", lambda y, a: y("B4"), 1, "C2"),
    R("CS5", "Chauves-souris", lambda y, a: y("B3"), 1, "C2"),
    R("CS6", "Chauves-souris", lambda y, a: y("V2b"), 1, "C1"),
    R("AM1", "Amphibiens", lambda y, a: y("F4") or y("I3"), 2, "C3"),
    R("AM2", "Amphibiens", lambda y, a: y("E1") and y("E2"), 2, "C3"),
    R("AM3", "Amphibiens", lambda y, a: y("E1") and a.get("E2") == "nsp", 1, "C3"),
    R("AM5", "Amphibiens", lambda y, a: y("E3"), 1, "C3"),
    R("AM6", "Amphibiens", lambda y, a: y("E4b"), 1, "C3"),
    R("AM7", "Amphibiens", lambda y, a: y("A2") and (y("V2b") or y("V4b")), 1, "C1"),
    R("RE1", "Reptiles", lambda y, a: y("F5") or y("I4"), 2, "C2"),
    R("RE2", "Reptiles", lambda y, a: y("B1") and y("V4"), 2, "C2"),
    R("RE3", "Reptiles", lambda y, a: y("B1") and y("V5"), 2, "C2"),
    R("RE4", "Reptiles", lambda y, a: y("B1"), 1, "C2"),
    R("RE5", "Reptiles", lambda y, a: y("V4b") and y("V5b"), 1, "C1"),
    R("RE6", "Reptiles", lambda y, a: y("S1b"), 1, "C1"),
    R("IN1", "Libellules", lambda y, a: y("K1"), 1, "C3"),
    R("IN2", "Papillons", lambda y, a: y("H1") and (y("V5") or y("S1")), 1, "C3"),
    R("IN3", "Libellules", lambda y, a: y("E1") and y("E2"), 1, "C0"),
    R("IN4a", "Criquets", lambda y, a: y("V5b"), 1, "C0"),
    R("IN4b", "Papillons", lambda y, a: y("V5b"), 1, "C0"),
]
THEMES = [
    ("ZH1", "Zone humide", lambda y, a: y("E3") or y("E4") or y("I6"), 2),
    ("ZH2", "Zone humide", lambda y, a: y("A2") or a.get("E3") == "nsp" or a.get("E4") == "nsp", 1),
    ("CE1", "Cours d'eau", lambda y, a: y("K1"), 2),
    ("FH2", "Flore", lambda y, a: y("H1") and y("V5b"), 2),
    ("FH1", "Flore", lambda y, a: y("H1") and (y("V5") or y("S1")), 1),
]


def evaluate(a, tour="oui", fh=True):
    """a : dict code -> 'oui' | 'non' | 'nsp'. Renvoie niveaux par groupe et thème, global, alertes."""
    def active(k):
        p = PARENT.get(k)
        return p is None or a.get(p) != "non"
    def yes(k):
        return a.get(k) == "oui" and active(k)
    def val(k):
        if not active(k):
            return 0
        v = a.get(k)
        if v == "oui": return 1
        if v == "nsp": return 0.5
        if v is None: return 0 if tour == "oui" else 0.5
        return 0
    groups = {g: (0, []) for g in GROUPS}
    for rid, g, cond, lv, c in RULES:
        if cond(yes, a):
            cur, why = groups[g]
            groups[g] = (max(cur, lv), why + [rid])
    themes = {}
    for rid, t, cond, lv in THEMES:
        if t == "Flore" and not fh:
            continue
        if cond(yes, a):
            cur = themes.get(t, (0, []))
            themes[t] = (max(cur[0], lv), cur[1] + [rid])
    score = {}
    for i, g in enumerate(GROUPS):
        den = sum(w[i] for w in W.values())
        score[g] = sum(W[k][i] * val(k) for k in W) / den
    alerts = [g for g in VERTEBRES if groups[g][0] == 0 and score[g] >= 0.30]
    glob = max([v[0] for v in groups.values()] + [v[0] for v in themes.values()] + [0])
    nsp_det = sum(1 for k in DETERMINANTS if a.get(k) == "nsp" and active(k))
    faible_ok = tour == "oui" and nsp_det <= 2 and not (yes("B2") and a.get("B3") == "nsp") and not alerts
    glob_lbl = LV[glob] if (glob > 0 or faible_ok) else "Indéterminée"
    return dict(groups={g: (LV[v[0]], v[1]) for g, v in groups.items()},
                themes={t: (LV[v[0]], v[1]) for t, v in themes.items()},
                score=score, alerts=alerts, glob=glob_lbl)


if __name__ == "__main__":
    ex = dict(A1="oui", V1="oui", V2="oui", V2b="non", V3="non", V4="oui", V4b="non", V5="oui", V5b="non", B2="oui", B3="non", B4="non")
    r = evaluate(ex)
    print(r["glob"], r["groups"], r["alerts"])
