"""Construit l'Outil terrain biodiversité V2."""
import math
import warnings
warnings.filterwarnings('ignore')
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, DataBarRule
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

OUT = sys.argv[1] if len(sys.argv) > 1 else "Outil_terrain_biodiversite_V2.xlsx"

# ---------------------------------------------------------------- styles
F = "Arial"
f_norm = Font(name=F, size=10)
f_bold = Font(name=F, size=10, bold=True)
f_title = Font(name=F, size=15, bold=True, color="1F4E3D")
f_sub = Font(name=F, size=10, italic=True, color="555555")
f_head = Font(name=F, size=10, bold=True, color="FFFFFF")
f_sect = Font(name=F, size=10, bold=True, color="1F4E3D")
f_small = Font(name=F, size=9, color="555555")
f_small_i = Font(name=F, size=9, italic=True, color="555555")
f_blue = Font(name=F, size=10, color="0000FF")
f_big = Font(name=F, size=13, bold=True)
fill_head = PatternFill("solid", fgColor="1F4E3D")
fill_sect = PatternFill("solid", fgColor="DDEBE3")
fill_input = PatternFill("solid", fgColor="FFF2CC")
fill_param = PatternFill("solid", fgColor="EAF1FB")
fill_grey = PatternFill("solid", fgColor="F2F2F2")
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
wrap_c = Alignment(wrap_text=True, vertical="center", horizontal="center")
wrap_l = Alignment(wrap_text=True, vertical="center")

FAIBLE, MODEREE, FORTE = "Faible", "Modérée", "Forte"
REPONSES = '"Oui,Non,Ne sait pas"'


def est_height(texts_widths, base=13.0, pad=4):
    lines = 1
    for txt, width in texts_widths:
        if not txt:
            continue
        n = 0
        for part in str(txt).split("\n"):
            n += max(1, math.ceil(len(part) / max(1, width * 1.15)))
        lines = max(lines, n)
    return lines * base + pad


def style_range(ws, rng, font=None, fill=None, align=None, brd=None):
    for row in ws[rng]:
        for c in row:
            if font: c.font = font
            if fill: c.fill = fill
            if align: c.alignment = align
            if brd: c.border = brd


# ---------------------------------------------------------------- groupes
GROUPES = [
    ("Oiseaux", FORTE,
     "La plupart des espèces sont protégées, y compris leurs sites de reproduction et de repos (arrêté du 29 octobre 2009).",
     "Mars à juillet."),
    ("Mammifères terrestres", MODEREE,
     "Plusieurs espèces communes sont protégées (Hérisson d'Europe, Écureuil roux…), d'autres non (arrêté du 23 avril 2007).",
     "Mars à octobre."),
    ("Chauves-souris", FORTE,
     "Toutes les espèces sont protégées, ainsi que leurs gîtes (arrêté du 23 avril 2007).",
     "Avril à septembre ; décembre à février pour les gîtes d'hiver."),
    ("Amphibiens", FORTE,
     "Toutes les espèces sont protégées, totalement ou partiellement (arrêté du 8 janvier 2021).",
     "Février à juin."),
    ("Reptiles", FORTE,
     "Toutes les espèces sont protégées, totalement ou partiellement (arrêté du 8 janvier 2021).",
     "Avril à juin, et septembre."),
    ("Libellules", FAIBLE,
     "Quelques espèces protégées, généralement localisées (arrêté du 23 avril 2007).",
     "Mai à août."),
    ("Criquets et sauterelles", FAIBLE,
     "Très peu d'espèces protégées au niveau national (arrêté du 23 avril 2007).",
     "Juillet à septembre."),
    ("Papillons", FAIBLE,
     "Quelques espèces protégées, dont certaines assez répandues (arrêté du 23 avril 2007).",
     "Avril à août."),
]
GN = [g[0] for g in GROUPES]
NG = len(GN)

# (code, parent, type, question, aide, poids[8], groupe observé)
# ordre : Oiseaux, Mammifères, Chauves-souris, Amphibiens, Reptiles, Libellules, Criquets, Papillons
Z = [0] * 8
SECTIONS = [
    ("1. Autour du site", [
        ("A1", None, "Habitat",
         "Y a-t-il des bois, des champs, des prairies ou des terrains en friche en bordure du site ?",
         "Ce qui est visible depuis le site, ou sur une vue aérienne (Google Maps, Géoportail).", [3, 3, 3, 2, 2, 1, 2, 2], None),
        ("A2", None, "Habitat",
         "Y a-t-il une rivière, un ruisseau, un étang ou une mare à proximité du site (quelques centaines de mètres) ?",
         "Vérifiable sur une vue aérienne.", [1, 1, 2, 3, 1, 3, 0, 0], None),
    ]),
    ("2. Végétation", [
        ("V1", None, "Habitat",
         "Une bonne partie du site est-elle couverte d'herbe, d'arbres ou de buissons (plutôt que de bâtiments, de bitume ou de gravier) ?",
         "Repère : au moins un tiers du site.", [2, 2, 1, 1, 2, 1, 2, 2], None),
        ("V2", None, "Habitat",
         "Y a-t-il de grands arbres, plus hauts qu'une maison ?",
         "", [1, 1, 1, 1, 0, 0, 0, 0], None),
        ("V2b", "V2", "Habitat",
         "Ces grands arbres sont-ils nombreux : un bois, un alignement ou plus d'une dizaine d'arbres ?",
         "Répondre Non pour quelques arbres isolés, même sur un grand site.", [2, 1, 2, 0, 0, 0, 0, 1], None),
        ("V3", "V2", "Habitat",
         "Ces arbres ont-ils des trous, des fentes, de l'écorce qui se décolle, des branches mortes ou beaucoup de lierre ?",
         "Regarder le tronc et les grosses branches ; plus facile en hiver, sans les feuilles.", [3, 2, 3, 0, 0, 0, 0, 0], None),
        ("V4", None, "Habitat",
         "Y a-t-il des haies, des buissons ou des ronces ?",
         "", [1, 1, 1, 1, 1, 0, 0, 1], None),
        ("V4b", "V4", "Habitat",
         "Ces haies ou fourrés occupent-ils une part importante du site ou de son pourtour ?",
         "Répondre Non pour quelques buissons isolés.", [2, 2, 1, 0, 2, 0, 1, 1], None),
        ("V5", None, "Habitat",
         "Y a-t-il des espaces en herbe sans entretien apparent (friche, prairie, herbe haute ou sèche, végétation qui pousse librement) ?",
         "Répondre Non pour une pelouse tondue régulièrement.", [1, 1, 1, 1, 1, 1, 1, 1], None),
        ("V5b", "V5", "Habitat",
         "Ces espaces en herbe couvrent-ils une grande partie du site (plus d'un quart) ?",
         "Répondre Non pour quelques bandes ou recoins.", [0, 0, 0, 0, 2, 0, 2, 2], None),
    ]),
    ("3. Eau", [
        ("E1", None, "Habitat",
         "Y a-t-il de l'eau sur le site : mare, étang, bassin, fossé ou ruisseau ?",
         "", [1, 1, 2, 3, 1, 3, 0, 0], None),
        ("E2", "E1", "Habitat",
         "Les bords sont-ils en pente douce, avec des herbes ou des roseaux ?",
         "Répondre Non pour des bords en béton ou à pic.", [1, 1, 1, 3, 1, 3, 1, 1], None),
        ("E3", None, "Habitat",
         "Y a-t-il des creux, des ornières ou des zones basses où l'eau semble stagner (eau, boue, dépôts de boue séchée) ?",
         "", [0, 0, 0, 3, 0, 1, 0, 0], None),
        ("E4", None, "Habitat",
         "Y a-t-il des roseaux, des joncs ou d'autres plantes de bord d'eau ?",
         "Reconnaissables toute l'année (tiges sèches en hiver).", [0, 0, 0, 1, 1, 1, 0, 0], None),
        ("E4b", "E4", "Habitat",
         "Ces roseaux ou joncs forment-ils une zone dense (une roselière), plutôt que quelques touffes ?",
         "", [1, 0, 0, 1, 0, 1, 0, 0], None),
    ]),
    ("4. Abris, sols nus et bâtiments", [
        ("B1", None, "Habitat",
         "Y a-t-il des tas de pierres, de gravats ou de bois, ou de vieux murets en pierre ?",
         "", [0, 1, 0, 1, 2, 0, 1, 0], None),
        ("B1b", "B1", "Habitat",
         "Y en a-t-il plusieurs, ou des murets en pierre sur une longueur importante ?",
         "Répondre Non pour un tas isolé.", [0, 0, 0, 1, 1, 0, 0, 0], None),
        ("S1", None, "Habitat",
         "Y a-t-il des zones de sol nu, de sable ou de cailloux, peu ou pas circulées (friche minérale, ancienne plateforme, carrière) ?",
         "Ne pas compter les parkings et voiries en service.", [1, 0, 0, 0, 1, 0, 1, 0], None),
        ("S1b", "S1", "Habitat",
         "Ces zones représentent-elles au total la surface d'un terrain de football ou plus ?",
         "Repère : un terrain de football fait environ 0,7 ha. Répondre Non pour quelques zones éparses.", [1, 0, 0, 0, 1, 0, 1, 1], None),
        ("B2", None, "Habitat",
         "Y a-t-il des bâtiments sur le site (maison, hangar, grange, ruine…) ?",
         "", [1, 1, 1, 0, 1, 0, 0, 0], None),
        ("B3", "B2", "Habitat",
         "Certains bâtiments ou parties de bâtiments sont-ils vides, abandonnés ou peu utilisés (greniers, combles, caves, granges) ?",
         "Si ces locaux n'ont pas pu être visités, répondre « Ne sait pas ».", [2, 1, 3, 0, 1, 0, 0, 0], None),
        ("B4", "B2", "Habitat",
         "Voyez-vous des fissures, des trous, des tuiles cassées ou des ouvertures dans les murs ou les toits ?",
         "", [3, 1, 3, 0, 2, 0, 0, 0], None),
    ]),
    ("5. Animaux vus ou entendus pendant la visite — ne rien voir ne veut pas dire qu'il n'y a rien", [
        ("F1", None, "Observation",
         "Voyez-vous des nids (dans les arbres, les haies, sous les toits), ou des oiseaux qui entrent et sortent d'un trou ou d'une toiture ?",
         "Les nids d'hirondelles en boue sous les avancées de toit restent visibles toute l'année.", Z, "Oiseaux"),
        ("F2", None, "Observation",
         "Voyez-vous des chauves-souris (par exemple suspendues dans un grenier, une cave ou sous un pont) ?",
         "", Z, "Chauves-souris"),
        ("F3", None, "Observation",
         "Voyez-vous un hérisson ou un écureuil ?",
         "", Z, "Mammifères terrestres"),
        ("F4", None, "Observation",
         "Voyez-vous des grenouilles, des crapauds ou des têtards ?",
         "", Z, "Amphibiens"),
        ("F5", None, "Observation",
         "Voyez-vous des lézards ou des serpents ?",
         "Par temps ensoleillé, au pied des murs et des tas de pierres.", Z, "Reptiles"),
        ("F6", None, "Observation",
         "Voyez-vous des libellules ?", "", Z, "Libellules"),
        ("F7", None, "Observation",
         "Entendez-vous des criquets, des sauterelles ou des grillons ?",
         "Surtout de juillet à septembre.", Z, "Criquets et sauterelles"),
        ("F8", None, "Observation",
         "Voyez-vous des papillons ?", "", Z, "Papillons"),
    ]),
    ("6. Projet envisagé (facultatif, si une intention est connue)", [
        ("P1", None, "Projet",
         "Une démolition, une rénovation lourde ou une extension des bâtiments est-elle envisagée ?", "", Z, None),
        ("P2", None, "Projet",
         "Des constructions ou aménagements sont-ils envisagés sur des espaces aujourd'hui non bâtis (herbe, arbres, friche) ?",
         "Y compris l'abattage d'arbres ou l'arrachage de haies.", Z, None),
    ]),
    ("7. Bonus — questions à un occupant ou au gestionnaire du site (facultatif ; seul un « Oui » est pris en compte)", [
        ("I1", None, "Bonus",
         "Des hirondelles ou des martinets font-ils leur nid chaque année sur les bâtiments ?",
         "Ne retenir que ce que l'interlocuteur a constaté lui-même ; noter sa fonction en commentaire.", Z, "Oiseaux"),
        ("I2", None, "Bonus",
         "Des chauves-souris ont-elles déjà été trouvées dans les bâtiments (combles, caves, locaux techniques) ?",
         "", Z, "Chauves-souris"),
        ("I3", None, "Bonus",
         "Des grenouilles ou des crapauds sont-ils vus sur le site, ou entendus chanter les soirs de printemps ?",
         "", Z, "Amphibiens"),
        ("I4", None, "Bonus",
         "Des lézards ou des serpents sont-ils vus sur le site aux beaux jours ?",
         "", Z, "Reptiles"),
        ("I5", None, "Bonus",
         "Des hérissons ou des écureuils sont-ils vus sur le site ?",
         "", Z, "Mammifères terrestres"),
        ("I6", None, "Bonus",
         "Une partie du site est-elle inondée ou détrempée chaque hiver, ou plusieurs semaines par an ?",
         "Ne pas compter les flaques passagères après un orage.", Z, None),
        ("I7", None, "Bonus",
         "Une étude faune-flore, zones humides ou une étude d'impact a-t-elle déjà été réalisée sur le site ?",
         "Si oui, demander le document.", Z, None),
    ]),
]

REGLES = [
    ("Oiseaux", "V3", None, FORTE, "Arbres à trous : nidification d'espèces protégées."),
    ("Oiseaux", "V4", None, MODEREE, "Haies et buissons : nidification de passereaux protégés."),
    ("Oiseaux", "B4", None, MODEREE, "Bâti avec ouvertures : martinets, hirondelles, moineaux."),
    ("Mammifères terrestres", "V4", "A1", MODEREE, "Haies reliées aux milieux voisins : Hérisson."),
    ("Chauves-souris", "V3", None, FORTE, "Arbres à trous et fentes : gîtes potentiels."),
    ("Chauves-souris", "B3", "B4", FORTE, "Bâtiment peu utilisé et ouvert : gîte potentiel."),
    ("Chauves-souris", "B4", None, MODEREE, "Fissures et ouvertures : gîtes potentiels."),
    ("Amphibiens", "E1", "E2", FORTE, "Point d'eau à bords favorables : site de reproduction."),
    ("Amphibiens", "E1", None, MODEREE, "Point d'eau : reproduction possible."),
    ("Amphibiens", "E3", None, MODEREE, "Eaux temporaires : reproduction possible."),
    ("Reptiles", "B1", "V4", FORTE, "Abris et lisières de buissons : habitat complet."),
    ("Reptiles", "B1", "V5", FORTE, "Abris et herbe haute : habitat complet."),
    ("Reptiles", "B1", None, MODEREE, "Abris : Lézard des murailles notamment."),
    ("Libellules", "E1", "E2", FORTE, "Point d'eau à bords végétalisés : reproduction."),
    ("Libellules", "E1", None, MODEREE, "Point d'eau."),
    ("Criquets et sauterelles", "V5", None, MODEREE, "Herbe haute peu entretenue."),
    ("Papillons", "V5", None, MODEREE, "Herbe haute peu entretenue."),
    ("Oiseaux", "V2b", None, MODEREE, "Bois ou nombreux grands arbres : nidification."),
    ("Chauves-souris", "V2b", None, MODEREE, "Bois ou nombreux grands arbres : gîtes et chasse."),
    ("Mammifères terrestres", "V2b", None, MODEREE, "Bois ou nombreux grands arbres : Écureuil roux."),
    ("Oiseaux", "S1b", None, MODEREE, "Grandes surfaces de sol nu caillouteux : Petit Gravelot, Œdicnème criard."),
]

QUESTIONS = [q for _, qs in SECTIONS for q in qs]
CODES = [q[0] for q in QUESTIONS]
assert len(set(CODES)) == len(CODES)
for g, a, b, *_ in REGLES:
    assert g in GN and a in CODES and (b is None or b in CODES)
for q in QUESTIONS:
    assert len(q[5]) == NG
    assert q[6] is None or q[6] in GN

wb = Workbook()
ws_n = wb.active
ws_n.title = "Notice"
ws_s = wb.create_sheet("Saisie")
ws_r = wb.create_sheet("Résultats")
ws_w = wb.create_sheet("Pondérations")
ws_p = wb.create_sheet("Paramètres")
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False

S = "Saisie!"
R = "'Résultats'!"
W = "'Pondérations'!"
P = "'Paramètres'!"

# ================================================================ SAISIE
ws = ws_s
widths = {"A": 6, "B": 66, "C": 38, "D": 14, "E": 24, "F": 32}
for k, v in widths.items():
    ws.column_dimensions[k].width = v
ws["A1"] = "Outil terrain biodiversité — Fiche de saisie"
ws["A1"].font = f_title
ws["A2"] = ("Faire le tour du site et répondre dans les cellules jaunes. En cas de doute, répondre « Ne sait pas » plutôt que « Non ». "
            "Les questions grisées « Sans objet » n'ont pas à être renseignées. Résultats dans l'onglet « Résultats ».")
ws["A2"].font = f_sub
ws.merge_cells("A2:F2")
ws["A2"].alignment = wrap
ws.row_dimensions[2].height = 28

META = [
    ("Nom du site / projet", "site"),
    ("Commune (département)", "commune"),
    ("Date de la visite (jj/mm/aaaa)", "date"),
    ("Observateur", "obs"),
    ("Partie du site visitée", "part"),
    ("Interlocuteur sur site (fonction), le cas échéant", "interl"),
]
META_CELL = {}
r = 4
for lab, key in META:
    ws.cell(r, 2, lab).font = f_bold
    c = ws.cell(r, 3)
    c.fill = fill_input
    c.border = border
    c.font = f_norm
    META_CELL[key] = f"C{r}"
    r += 1
ws[META_CELL["date"]].number_format = "DD/MM/YYYY"
dv_date = DataValidation(type="date", operator="greaterThan", formula1="36526", allow_blank=True,
                         error="Saisir une date au format jj/mm/aaaa.", errorTitle="Date")
dv_date.add(META_CELL["date"])
dv_part = DataValidation(type="list", formula1='"Totalité,Majeure partie,Partie seulement"', allow_blank=True)
dv_part.add(META_CELL["part"])
ws.add_data_validation(dv_part)
ws.add_data_validation(dv_date)

HEAD_ROW = r + 1
for j, h in enumerate(["N°", "Question", "Aide / repères", "Réponse", "Statut", "Commentaire (facultatif)"], 1):
    c = ws.cell(HEAD_ROW, j, h)
    c.font = f_head
    c.fill = fill_head
    c.alignment = wrap_c
    c.border = border
ws.row_dimensions[HEAD_ROW].height = 20

dv_rep = DataValidation(type="list", formula1=REPONSES, allow_blank=True,
                        error="Choisir Oui, Non ou Ne sait pas.", errorTitle="Réponse")
ws.add_data_validation(dv_rep)

SROW = {}   # code -> ligne Saisie
NUM = {}    # code -> numéro affiché
r = HEAD_ROW + 1
n = 0
for title, qs in SECTIONS:
    ws.cell(r, 1, title)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    style_range(ws, f"A{r}:F{r}", font=f_sect, fill=fill_sect, align=wrap_l)
    ws.row_dimensions[r].height = 18
    r += 1
    for code, parent, typ, q, aide, w, gobs in qs:
        n += 1
        SROW[code] = r
        NUM[code] = n
        ws.cell(r, 1, n).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(r, 2, q).alignment = wrap
        ws.cell(r, 3, aide).alignment = wrap
        ws.cell(r, 3).font = f_small_i
        d = ws.cell(r, 4)
        d.fill = fill_input
        d.alignment = Alignment(horizontal="center", vertical="top")
        dv_rep.add(f"D{r}")
        if typ in ("Bonus", "Projet"):
            ws.cell(r, 5, f'=IF(D{r}="","Facultatif","OK")')
        elif parent:
            pr = SROW[parent]
            ws.cell(r, 5, f'=IF($D${pr}="Non","Sans objet (Non en n° {NUM[parent]})",IF(D{r}="","À renseigner","OK"))')
        else:
            ws.cell(r, 5, f'=IF(D{r}="","À renseigner","OK")')
        ws.cell(r, 5).alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
        ws.cell(r, 6).fill = fill_input
        ws.cell(r, 6).alignment = wrap
        for j in range(1, 7):
            ws.cell(r, j).border = border
            if j not in (3,):
                ws.cell(r, j).font = f_norm
        ws.row_dimensions[r].height = est_height([(q, widths["B"]), (aide, widths["C"] * 1.1)])
        r += 1
LAST_S = r - 1
ws.conditional_formatting.add(f"A{HEAD_ROW+1}:F{LAST_S}",
                              FormulaRule(formula=[f'LEFT($E{HEAD_ROW+1},10)="Sans objet"'],
                                          fill=PatternFill("solid", fgColor="E7E6E6"),
                                          font=Font(name=F, color="808080")))
ws.conditional_formatting.add(f"E{HEAD_ROW+1}:E{LAST_S}",
                              FormulaRule(formula=[f'$E{HEAD_ROW+1}="À renseigner"'],
                                          font=Font(name=F, color="C65911", bold=True)))
ws.conditional_formatting.add(f"E{HEAD_ROW+1}:E{LAST_S}",
                              FormulaRule(formula=[f'$E{HEAD_ROW+1}="OK"'],
                                          font=Font(name=F, color="548235")))
ws.freeze_panes = f"A{HEAD_ROW+1}"
ws.print_title_rows = f"{HEAD_ROW}:{HEAD_ROW}"
ws.page_setup.orientation = "landscape"
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_area = f"A1:F{LAST_S}"

# ================================================================ PARAMÈTRES
ws = ws_p
for k, v in {"A": 30, "B": 16, "C": 16, "D": 16, "E": 58, "F": 13, "G": 13, "H": 12, "I": 10}.items():
    ws.column_dimensions[k].width = v
ws["A1"] = "Paramètres — réservé à l'écologue référent"
ws["A1"].font = f_title
ws["A2"] = "Valeurs modifiables en bleu (onglet protégé sans mot de passe : Révision > Ôter la protection de la feuille)."
ws["A2"].font = f_sub

REG = [
    ("Coefficient appliqué à « Ne sait pas »", 0.5, "0.00",
     "Part du poids retenue pour une réponse « Ne sait pas » (principe de précaution : 0 = comme Non, 1 = comme Oui)."),
    ("Seuil potentialité modérée", 0.30, "0%", "Score d'accueil à partir duquel la potentialité est modérée. À calibrer sur des sites déjà diagnostiqués."),
    ("Seuil potentialité forte", 0.55, "0%", "Score d'accueil à partir duquel la potentialité est forte. À calibrer sur des sites déjà diagnostiqués."),
    ("Premier mois favorable aux observations", 3, "0", "Mars."),
    ("Dernier mois favorable aux observations", 9, "0", "Septembre."),
    ("Taux de « Ne sait pas » : fiabilité bonne jusqu'à", 0.15, "0%", ""),
    ("Taux de « Ne sait pas » : fiabilité moyenne jusqu'à", 0.35, "0%", "Au-delà : fiabilité faible."),
]
ws["A3"], ws["B3"], ws["E3"] = "Réglage", "Valeur", "Commentaire"
for c in ("A3", "B3", "E3"):
    ws[c].font = f_head; ws[c].fill = fill_head; ws[c].border = border
PREF = {}
for i, (lab, val, fmt, com) in enumerate(REG):
    rr = 4 + i
    ws.cell(rr, 1, lab).font = f_norm
    c = ws.cell(rr, 2, val)
    c.font = f_blue; c.fill = fill_param; c.number_format = fmt; c.border = border
    c.alignment = Alignment(horizontal="center")
    ws.cell(rr, 5, com).font = f_small
    ws.cell(rr, 1).border = border
PREF = {"nsp": "$B$4", "sm": "$B$5", "sf": "$B$6", "m1": "$B$7", "m2": "$B$8", "fb": "$B$9", "fm": "$B$10"}

# Groupes
G0 = 13
for j, h in enumerate(["Groupe", "Sensibilité réglementaire", "", "", "Base réglementaire (résumé)", "Période d'inventaire favorable"], 1):
    pass
heads = {1: "Groupe", 2: "Sensibilité réglementaire", 5: "Base réglementaire (résumé)"}
ws.cell(G0 - 1, 1, "Groupes faunistiques").font = f_sect
for col, h in heads.items():
    c = ws.cell(G0, col, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
ws.merge_cells(start_row=G0, start_column=2, end_row=G0, end_column=4)
ws.cell(G0, 6, "Période d'inventaire favorable").font = f_head
ws.cell(G0, 6).fill = fill_head
ws.merge_cells(start_row=G0, start_column=6, end_row=G0, end_column=9)
ws.cell(G0, 6).alignment = wrap_c
dv_sens = DataValidation(type="list", formula1=f'"{FORTE},{MODEREE},{FAIBLE}"', allow_blank=False)
ws.add_data_validation(dv_sens)
GROW = {}
for i, (g, sens, base, per) in enumerate(GROUPES):
    rr = G0 + 1 + i
    GROW[g] = rr
    ws.cell(rr, 1, g).font = f_bold
    c = ws.cell(rr, 2, sens); c.font = f_blue; c.fill = fill_param; c.alignment = Alignment(horizontal="center", vertical="top")
    ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=4)
    dv_sens.add(f"B{rr}")
    ws.cell(rr, 5, base).font = f_small; ws.cell(rr, 5).alignment = wrap
    c = ws.cell(rr, 6, per); c.font = f_small; c.alignment = wrap
    ws.merge_cells(start_row=rr, start_column=6, end_row=rr, end_column=9)
    ws.cell(rr, 1).alignment = wrap
    ws.row_dimensions[rr].height = est_height([(base, 58), (per, 46)], base=12)
    for col in range(1, 10):
        ws.cell(rr, col).border = border
G_LAST = G0 + NG

# Matrice de vigilance
M0 = G_LAST + 3
ws.cell(M0 - 1, 1, "Matrice de vigilance (niveau retenu × sensibilité réglementaire)").font = f_sect
for j, h in enumerate(["Niveau retenu", FORTE, MODEREE, FAIBLE], 1):
    c = ws.cell(M0, j, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
MAT = [
    ("Faible", [FAIBLE, FAIBLE, FAIBLE]),
    ("Modérée", [MODEREE, MODEREE, FAIBLE]),
    ("Forte", [FORTE, MODEREE, MODEREE]),
    ("Présence avérée", [FORTE, FORTE, MODEREE]),
]
dv_niv = DataValidation(type="list", formula1=f'"{FORTE},{MODEREE},{FAIBLE}"', allow_blank=False)
ws.add_data_validation(dv_niv)
for i, (lab, vals) in enumerate(MAT):
    rr = M0 + 1 + i
    ws.cell(rr, 1, lab).font = f_bold
    ws.cell(rr, 1).border = border
    for j, v in enumerate(vals):
        c = ws.cell(rr, 2 + j, v)
        c.font = f_blue; c.fill = fill_param; c.border = border; c.alignment = Alignment(horizontal="center")
        dv_niv.add(c.coordinate)
MAT_RNG = f"$B${M0+1}:$D${M0+4}"
MAT_HEAD = f"$B${M0}:$D${M0}"

# Textes
T0 = M0 + 7
ws.cell(T0 - 1, 1, "Textes de restitution").font = f_sect
for j, h in enumerate(["Niveau", "Recommandation par groupe faunistique", "", "", "Zones humides", "Conclusion générale"], 1):
    if h:
        c = ws.cell(T0, j, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
ws.merge_cells(start_row=T0, start_column=2, end_row=T0, end_column=4)
ws.merge_cells(start_row=T0, start_column=6, end_row=T0, end_column=9)
TXT = [
    (FAIBLE,
     "Pas d'élément sensible relevé à ce stade.",
     "Aucun indice de zone humide relevé.",
     "Sensibilité faible : aucun élément sensible marqué n'a été relevé. Ce repérage ne remplace pas un diagnostic écologique, qui peut être exigé si le projet est soumis à évaluation environnementale."),
    (MODEREE,
     "Éléments favorables à préserver dans la conception ; avis d'un écologue conseillé.",
     "Contexte pouvant être favorable à une zone humide : vérification par un écologue conseillée.",
     "Sensibilité modérée : des éléments favorables à la faune sont présents. Les préserver dans la conception du projet limite les contraintes ; une visite de pré-diagnostic par un écologue est conseillée pour confirmer."),
    (FORTE,
     "Éléments à éviter dès la conception du projet ; à défaut, diagnostic écologique nécessaire (espèces protégées probables).",
     "Indices de zone humide : secteur à éviter dans la conception du projet ; à défaut, diagnostic zones humides. Au-delà de 0,1 ha de zone humide touchée, un dossier loi sur l'eau est requis (rubrique 3.3.1.0).",
     "Sensibilité forte : des éléments susceptibles d'abriter des espèces protégées ou des zones humides ont été relevés. Les éviter dès la conception du projet est le moyen le plus efficace de limiter les contraintes réglementaires ; à défaut, un diagnostic écologique sera nécessaire, avec des inventaires répartis sur un cycle annuel."),
]
for i, (niv, tg, tz, tc) in enumerate(TXT):
    rr = T0 + 1 + i
    ws.cell(rr, 1, niv).font = f_bold
    c = ws.cell(rr, 2, tg); c.font = f_blue; c.alignment = wrap; c.fill = fill_param
    ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=4)
    c = ws.cell(rr, 5, tz); c.font = f_blue; c.alignment = wrap; c.fill = fill_param
    c = ws.cell(rr, 6, tc); c.font = f_blue; c.alignment = wrap; c.fill = fill_param
    ws.merge_cells(start_row=rr, start_column=6, end_row=rr, end_column=9)
    ws.row_dimensions[rr].height = est_height([(tg, 46), (tz, 58), (tc, 46)], base=12.5)
    for col in range(1, 10):
        ws.cell(rr, col).border = border
TXT_NIV = f"$A${T0+1}:$A${T0+3}"
TXT_G = f"$B${T0+1}:$B${T0+3}"
TXT_Z = f"$E${T0+1}:$E${T0+3}"
TXT_C = f"$F${T0+1}:$F${T0+3}"

# Règles
RG0 = T0 + 7
ws.cell(RG0 - 1, 1, "Éléments clés : règles de niveau plancher (une réponse Oui à A, et à B si renseigné, impose au moins le niveau indiqué)").font = f_sect
for j, h in enumerate(["Groupe", "Question A (code)", "Question B (code)", "Niveau plancher", "Justification", "A remplie", "B remplie", "Déclenchée", "Valeur"], 1):
    c = ws.cell(RG0, j, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
ws.row_dimensions[RG0].height = 26
N_RULES_MAX = 40
dv_grp = DataValidation(type="list", formula1=f"=$A${G0+1}:$A${G_LAST}", allow_blank=True)
dv_pl = DataValidation(type="list", formula1=f'"{MODEREE},{FORTE}"', allow_blank=True)
ws.add_data_validation(dv_grp); ws.add_data_validation(dv_pl)
RG_FIRST, RG_LAST = RG0 + 1, RG0 + N_RULES_MAX
# PLAGES pondérations (définies plus bas, mais connues)
W_FIRST = 4
W_LAST = W_FIRST + len(QUESTIONS) - 1
W_CODE = f"{W}$A${W_FIRST}:$A${W_LAST}"
W_OUIACT = f"{W}$I${W_FIRST}:$I${W_LAST}"
for i in range(N_RULES_MAX):
    rr = RG_FIRST + i
    if i < len(REGLES):
        g, a, b, niv, just = REGLES[i]
        ws.cell(rr, 1, g); ws.cell(rr, 2, a); ws.cell(rr, 3, b); ws.cell(rr, 4, niv); ws.cell(rr, 5, just)
    for col in range(1, 6):
        c = ws.cell(rr, col); c.font = f_blue if col < 5 else f_small; c.fill = fill_param; c.border = border
        c.alignment = wrap if col == 5 else Alignment(horizontal="center", vertical="top")
    ws.cell(rr, 1).alignment = Alignment(vertical="top")
    dv_grp.add(f"A{rr}"); dv_pl.add(f"D{rr}")
    ws.cell(rr, 6, f'=IF($B{rr}="","",IFERROR(INDEX({W_OUIACT},MATCH($B{rr},{W_CODE},0)),"code ?"))')
    ws.cell(rr, 7, f'=IF($B{rr}="","",IF($C{rr}="",1,IFERROR(INDEX({W_OUIACT},MATCH($C{rr},{W_CODE},0)),"code ?")))')
    ws.cell(rr, 8, f'=IF($B{rr}="",0,IF(AND(F{rr}=1,G{rr}=1),1,0))')
    ws.cell(rr, 9, f'=IF(H{rr}=1,IF(D{rr}="{FORTE}",2,IF(D{rr}="{MODEREE}",1,0)),0)')
    for col in range(6, 10):
        c = ws.cell(rr, col); c.font = f_norm; c.border = border; c.alignment = Alignment(horizontal="center", vertical="top")
        c.fill = fill_grey
RG_GRP = f"{P}$A${RG_FIRST}:$A${RG_LAST}"
RG_VAL = f"{P}$I${RG_FIRST}:$I${RG_LAST}"

# ================================================================ PONDÉRATIONS
ws = ws_w
ws["A1"] = "Pondérations et calcul — réservé à l'écologue référent"
ws["A1"].font = f_title
ws["A2"] = ("Poids de 0 (sans effet) à 3 (élément déterminant) pour la potentialité d'accueil de chaque groupe. "
            "Les poids sont modifiables en bleu ; les colonnes grises sont calculées.")
ws["A2"].font = f_sub
hdr = ["Code", "N°", "Question", "Type", "Question mère", "Réponse", "Active", "Valeur", "Oui retenu", "Groupe observé"] + GN
for j, h in enumerate(hdr, 1):
    c = ws.cell(3, j, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
ws.row_dimensions[3].height = 40
for k, v in {"A": 7, "B": 5, "C": 60, "D": 12, "E": 9, "F": 11, "G": 8, "H": 8, "I": 8, "J": 18}.items():
    ws.column_dimensions[k].width = v
for j in range(NG):
    ws.column_dimensions[L(11 + j)].width = 11
WROW = {}
for i, (code, parent, typ, q, aide, w, gobs) in enumerate(QUESTIONS):
    rr = W_FIRST + i
    WROW[code] = rr
    sr = SROW[code]
    ws.cell(rr, 1, code).font = f_bold
    ws.cell(rr, 2, NUM[code])
    ws.cell(rr, 3, f"={S}$B${sr}")
    ws.cell(rr, 4, typ)
    ws.cell(rr, 5, parent)
    ws.cell(rr, 6, f'=IF({S}$D${sr}="","",{S}$D${sr})')
    if typ in ("Bonus", "Projet"):
        ws.cell(rr, 7, 0)
    elif parent:
        ws.cell(rr, 7, f'=IF(INDEX($F${W_FIRST}:$F${W_LAST},MATCH($E{rr},$A${W_FIRST}:$A${W_LAST},0))="Non",0,1)')
    else:
        ws.cell(rr, 7, 1)
    ws.cell(rr, 8, f'=G{rr}*IF(F{rr}="Oui",1,IF(F{rr}="Ne sait pas",{P}{PREF["nsp"]},0))')
    ws.cell(rr, 9, f'=IF(F{rr}="Oui",1,0)' if typ == "Bonus" else f'=IF(AND(G{rr}=1,F{rr}="Oui"),1,0)')
    ws.cell(rr, 10, gobs)
    for j in range(NG):
        c = ws.cell(rr, 11 + j, w[j] if typ in ("Habitat", "Contexte") else None)
        c.font = f_blue; c.fill = fill_param; c.alignment = Alignment(horizontal="center")
    for col in range(1, 11):
        c = ws.cell(rr, col)
        if col != 1:
            c.font = f_norm
        c.border = border
        c.alignment = Alignment(vertical="top", wrap_text=(col == 3), horizontal=None if col == 3 else "center")
        if col >= 6:
            c.fill = fill_grey
    for j in range(NG):
        ws.cell(rr, 11 + j).border = border
    ws.cell(rr, 8).number_format = "0.00"
    ws.row_dimensions[rr].height = est_height([(q, 60)], base=12.5)
TOT = W_LAST + 1
ws.cell(TOT, 3, "Score maximal (somme des poids)").font = f_bold
for j in range(NG):
    cl = L(11 + j)
    c = ws.cell(TOT, 11 + j, f"=SUM({cl}{W_FIRST}:{cl}{W_LAST})")
    c.font = f_bold; c.alignment = Alignment(horizontal="center"); c.border = border
ws.freeze_panes = "D4"
dv_w = DataValidation(type="whole", operator="between", formula1="0", formula2="3", allow_blank=True,
                      error="Poids entier de 0 à 3.", errorTitle="Poids")
ws.add_data_validation(dv_w)
dv_w.add(f"K{W_FIRST}:{L(10+NG)}{W_LAST}")

# ================================================================ RÉSULTATS
ws = ws_r
for k, v in {"A": 26, "B": 15, "C": 13, "D": 15, "E": 62, "F": 34}.items():
    ws.column_dimensions[k].width = v
ws["A1"] = "Outil terrain biodiversité — Résultats"
ws["A1"].font = f_title
ws["A2"] = ("Évaluation très préliminaire, établie lors d'une visite unique par un non-spécialiste (contexte de due diligence) : "
            "elle signale la sensibilité biodiversité du site pour orienter l'évitement en amont, sans remplacer un diagnostic écologique.")
ws["A2"].font = f_sub
ws.merge_cells("A2:F2"); ws["A2"].alignment = wrap; ws.row_dimensions[2].height = 26

info = [("Site", "site"), ("Commune", "commune"), ("Date de visite", "date"), ("Observateur", "obs"), ("Partie visitée", "part")]
for i, (lab, key) in enumerate(info):
    rr = 4 + i
    ws.cell(rr, 1, lab).font = f_bold
    c = ws.cell(rr, 2, f'=IF({S}{META_CELL[key]}="","—",{S}{META_CELL[key]})')
    c.font = f_norm
    c.alignment = Alignment(horizontal="left")
    ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=3)
ws["B6"].number_format = "DD/MM/YYYY"

WA = f"{W}$G${W_FIRST}:$G${W_LAST}"
WF = f"{W}$F${W_FIRST}:$F${W_LAST}"
ws["H4"] = f"=SUM({WA})"
ws["H5"] = f'=SUMPRODUCT(({WA}=1)*({WF}<>""))'
ws["H6"] = f'=SUMPRODUCT(({WA}=1)*({WF}="Ne sait pas"))'
ws["D4"] = '="Questions renseignées : "&H5&" sur "&H4'
ws["D5"] = '="Réponses « Ne sait pas » : "&H6'
ws["D6"] = (f'="Fiabilité : "&IF(H5=0,"—",IF(H6/H5<={P}{PREF["fb"]},"bonne",IF(H6/H5<={P}{PREF["fm"]},"moyenne","faible")))')
for rr in range(4, 7):
    ws.merge_cells(start_row=rr, start_column=4, end_row=rr, end_column=6)
    ws.cell(rr, 4).font = f_norm
    ws.cell(rr, 4).alignment = Alignment(horizontal="left")
EMPTY = "$H$5=0"

# Tableau par groupe : colonnes visibles A-F, colonnes techniques H-L (masquées)
H0 = 13
cols = ["Groupe", "Accueil potentiel du site", "Animaux observés ou signalés", "Sensibilité", "Recommandation", "Période favorable pour un inventaire"]
ws.cell(H0 - 1, 1, "Résultats par groupe d'animaux").font = f_sect
for j, h in enumerate(cols, 1):
    c = ws.cell(H0, j, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
ws.row_dimensions[H0].height = 30
for j, h in enumerate(["classe num", "élément clé num", "niveau num", "sensibilité", "vigilance num"], 8):
    ws.cell(H0, j, h).font = f_small
GR_FIRST = H0 + 1
for i, g in enumerate(GN):
    rr = GR_FIRST + i
    wc = L(11 + i)
    gr = GROW[g]
    ws.cell(rr, 1, f"={P}$A${gr}").font = f_bold
    ws.cell(rr, 2, f"=IF({W}{wc}${TOT}=0,0,SUMPRODUCT({W}$H${W_FIRST}:$H${W_LAST},{W}{wc}${W_FIRST}:{wc}${W_LAST})/{W}{wc}${TOT})")
    ws.cell(rr, 2).number_format = "0%"
    ws.cell(rr, 3, f'=IF({EMPTY},"—",IF(COUNTIFS({W}$J${W_FIRST}:$J${W_LAST},$A{rr},{W_OUIACT},1)>0,"Oui","Non"))')
    ws.cell(rr, 8, f'=IF(B{rr}>={P}{PREF["sf"]},2,IF(B{rr}>={P}{PREF["sm"]},1,0))')
    ws.cell(rr, 9, f"=SUMPRODUCT(MAX(({RG_GRP}=$A{rr})*{RG_VAL}))")
    ws.cell(rr, 10, f'=IF(C{rr}="Oui",3,MAX(H{rr},I{rr}))')
    ws.cell(rr, 11, f"={P}$B${gr}")
    ws.cell(rr, 4, f'=IF({EMPTY},"—",INDEX({P}{MAT_RNG},J{rr}+1,MATCH(K{rr},{P}{MAT_HEAD},0)))')
    ws.cell(rr, 12, f"=IFERROR(MATCH(D{rr},{P}{TXT_NIV},0)-1,0)")
    ws.cell(rr, 5, f'=IF({EMPTY},"",INDEX({P}{TXT_G},L{rr}+1))')
    ws.cell(rr, 6, f"={P}$F${gr}")
    for col in range(1, 7):
        c = ws.cell(rr, col)
        c.border = border
        if col != 1:
            c.font = f_norm
        c.alignment = wrap_l if col in (5, 6) else Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.cell(rr, 1).alignment = wrap_l
    ws.row_dimensions[rr].height = 34
GR_LAST = GR_FIRST + NG - 1

# Zones humides
ZR = GR_LAST + 3
ws.cell(ZR - 1, 1, "Zones humides").font = f_sect
for j, h in [(1, "Indices relevés"), (4, "Sensibilité"), (5, "Recommandation")]:
    c = ws.cell(ZR, j, h); c.font = f_head; c.fill = fill_head; c.border = border; c.alignment = wrap_c
ws.merge_cells(start_row=ZR, start_column=1, end_row=ZR, end_column=3)
ws.merge_cells(start_row=ZR, start_column=5, end_row=ZR, end_column=6)
zf = {c: f"{W}$F${WROW[c]}" for c in ("A2", "E3", "E4", "I6")}
lab = {"A2": "eau à proximité", "E3": "eau stagnante ou sol boueux", "E4": "plantes de bord d'eau", "I6": "inondation ou sol détrempé signalé"}
parts = "&".join([f'IF({zf[c]}="Oui","{lab[c]} ; ","")' for c in ("E3", "E4", "I6", "A2")])
zr = ZR + 1
ws.cell(zr, 1, f'=IF({EMPTY},"—",IF(({parts})="","Aucun",LEFT(({parts}),LEN(({parts}))-3)))')
ws.cell(zr, 8, f'=IF(OR({zf["E3"]}="Oui",{zf["E4"]}="Oui",{zf["I6"]}="Oui"),2,IF(OR({zf["A2"]}="Oui",{zf["E3"]}="Ne sait pas",{zf["E4"]}="Ne sait pas"),1,0))')
ws.cell(zr, 4, f'=IF({EMPTY},"—",INDEX({P}{TXT_NIV},H{zr}+1))')
ws.cell(zr, 5, f'=IF({EMPTY},"",INDEX({P}{TXT_Z},H{zr}+1))')
ws.merge_cells(start_row=zr, start_column=1, end_row=zr, end_column=3)
ws.merge_cells(start_row=zr, start_column=5, end_row=zr, end_column=6)
for col in range(1, 7):
    c = ws.cell(zr, col); c.border = border; c.font = f_norm
ws.cell(zr, 1).alignment = wrap_l
ws.cell(zr, 4).alignment = wrap_c
ws.cell(zr, 5).alignment = wrap_l
ws.row_dimensions[zr].height = 34

# Synthèse globale
ws["A9"] = "Sensibilité biodiversité du site"
ws["A9"].font = f_bold
ws["A9"].alignment = wrap_l
ws["H9"] = f"=MAX(L{GR_FIRST}:L{GR_LAST},H{zr})"
ws["B9"] = f'=IF({EMPTY},"Questionnaire non renseigné",INDEX({P}{TXT_NIV},H9+1))'
ws["B9"].font = f_big
ws["B9"].alignment = wrap_c
ws.merge_cells("B9:C10")
ws["D9"] = f'=IF({EMPTY},"",INDEX({P}{TXT_C},H9+1))'
ws["D9"].alignment = wrap_l
ws["D9"].font = f_norm
ws.merge_cells("D9:F10")
ws.merge_cells("A9:A10")
ws.row_dimensions[9].height = 28
ws.row_dimensions[10].height = 28
style_range(ws, "A9:F10", brd=border)

# Éléments sensibles à préserver (liste compactée ; colonnes P-Q masquées)
def ouiact(code): return f"{W}$I${WROW[code]}"
def rep(code): return f"{W}$F${WROW[code]}"
def act(code): return f"{W}$G${WROW[code]}"
ER0 = zr + 3
ws.cell(ER0 - 1, 1, "Éléments sensibles relevés, à préserver dans la conception du projet").font = f_sect
ELEMS = [
    ("V3", "Arbres à cavités, fentes ou lierre (chauves-souris, oiseaux)"),
    ("V2b", "Bois, alignement ou nombreux grands arbres (oiseaux, chauves-souris, mammifères)"),
    ("V2", "Grands arbres isolés (oiseaux, chauves-souris)"),
    ("V4", "Haies, buissons ou fourrés (oiseaux, reptiles, hérisson)"),
    ("V5", "Espaces en herbe sans entretien (reptiles, insectes)"),
    ("E1", "Mare, bassin ou fossé (amphibiens, libellules)"),
    ("E3", "Zones d'eau stagnante (zone humide possible, amphibiens)"),
    ("E4", "Roseaux ou joncs (zone humide possible)"),
    ("I6", "Partie du site inondée chaque hiver (zone humide possible)"),
    ("S1b", "Grandes surfaces de sol nu, sableux ou caillouteux (oiseaux nicheurs au sol, reptiles)"),
    ("S1", "Petites zones de sol nu ou caillouteux (reptiles, insectes)"),
    ("B1", "Tas de pierres, de bois ou murets (reptiles)"),
    ("B3", "Locaux vides ou peu utilisés (chauves-souris, oiseaux)"),
    ("B4", "Fissures et ouvertures du bâti (chauves-souris, oiseaux)"),
]
def elem_formula(code, label):
    if code == "I6":
        return f'=IF({rep("I6")}="Oui","{label}","")'
    nsp = f'IF(AND({act(code)}=1,{rep(code)}="Ne sait pas"),"{label} : à vérifier","")'
    if code in ("V2", "S1"):
        return f'=IF(AND({ouiact(code)}=1,{rep(code + "b")}<>"Oui"),"{label}",{nsp})'
    return f'=IF({ouiact(code)}=1,"{label}",{nsp})'
EL_ = f"$P${ER0}:$P${ER0+len(ELEMS)-1}"
EM_ = f"$Q${ER0}:$Q${ER0+len(ELEMS)-1}"
for i, (code, label) in enumerate(ELEMS):
    rr = ER0 + i
    ws.cell(rr, 16, elem_formula(code, label))
    ws.cell(rr, 17, f'=IF(P{rr}="","",COUNTIF($P${ER0}:P{rr},"?*"))')
    disp = f'IFERROR("• "&INDEX({EL_},MATCH({i+1},{EM_},0)),"")'
    if i == 0:
        disp = f'IF({EMPTY},"",IF(COUNTIF({EL_},"?*")=0,"Aucun élément sensible relevé.",{disp}))'
    c = ws.cell(rr, 1, "=" + disp)
    c.font = Font(name=F, size=10, color="1F4E3D")
    c.alignment = wrap_l
    ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=6)
    ws.row_dimensions[rr].height = 16
ER_LAST = ER0 + len(ELEMS) - 1

# Points d'attention (liste compactée ; colonnes N-O masquées)
AR = ER_LAST + 3
ws.cell(AR - 1, 1, "Points d'attention").font = f_sect
dcell = f"{S}{META_CELL['date']}"
ALERTES = [
    f'=IF($H$4-$H$5>0,"Questionnaire incomplet : "&($H$4-$H$5)&" question(s) sans réponse ; résultat provisoire.","")',
    f'=IF({dcell}="","Date de visite non renseignée.",IF(OR(MONTH({dcell})<{P}{PREF["m1"]},MONTH({dcell})>{P}{PREF["m2"]}),"Visite entre octobre et février : peu d\'animaux sont visibles à cette période ; le résultat repose sur les milieux décrits.",""))',
    f'=IF({S}{META_CELL["part"]}="Partie seulement","Visite partielle du site : le résultat ne vaut que pour la partie vue ; les zones non visitées peuvent présenter des enjeux.","")',
    f'=IF(AND({EMPTY}=FALSE,IF($H$5=0,0,$H$6/$H$5)>{P}{PREF["fm"]}),"Nombreuses réponses « Ne sait pas » : résultat à confirmer par un écologue.","")',
    f'=IF(AND({rep("P1")}="Oui",OR({ouiact("B3")}=1,{ouiact("B4")}=1,{ouiact("F1")}=1,{ouiact("F2")}=1)),"Travaux envisagés sur des bâtiments pouvant abriter des chauves-souris ou des oiseaux protégés : expertise des bâtiments par un écologue à prévoir avant travaux, avec un calendrier adapté.","")',
    f'=IF(AND({rep("P2")}="Oui",OR({ouiact("V2")}=1,{ouiact("V3")}=1,{ouiact("V4")}=1,{ouiact("V5")}=1,{ouiact("S1")}=1,{ouiact("E1")}=1,{ouiact("E3")}=1,{ouiact("E4")}=1)),"Aménagement envisagé sur des espaces favorables à la faune ou potentiellement humides : les éléments listés ci-dessus sont à éviter en priorité. Les abattages et défrichements sont à programmer hors période de nidification (mi-mars à fin août).","")',
]
ALERTES.append(f'=IF({rep("I7")}="Oui","Une étude environnementale existe sur le site : la récupérer, elle peut confirmer ou lever les enjeux pressentis.","")')
AL = f"$N${AR}:$N${AR+len(ALERTES)-1}"
AM = f"$O${AR}:$O${AR+len(ALERTES)-1}"
for i, fml in enumerate(ALERTES):
    rr = AR + i
    ws.cell(rr, 14, fml)
    ws.cell(rr, 15, f'=IF(N{rr}="","",COUNTIF($N${AR}:N{rr},"?*"))')
    disp = f'IFERROR("• "&INDEX({AL},MATCH({i+1},{AM},0)),"")'
    if i == 0:
        disp = f'IF(COUNTIF({AL},"?*")=0,"Aucun point d\'attention particulier.",{disp})'
    c = ws.cell(rr, 1, "=" + disp)
    c.font = Font(name=F, size=10, color="9C3D00")
    c.alignment = wrap_l
    ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=6)
    ws.row_dimensions[rr].height = 28
AR_LAST = AR + len(ALERTES) - 1

MR = AR_LAST + 2
ws.cell(MR, 1, "Comment lire ces résultats").font = f_sect
lect = [
    "Accueil potentiel : capacité des milieux décrits à accueillir le groupe (100 % = tous les milieux favorables sont présents).",
    "Sensibilité : tient compte des milieux présents et de leur étendue, de certains éléments déterminants (arbre à trous, bâtiment ouvert, mare…), des animaux observés et de la part d'espèces protégées dans le groupe.",
]
for i, t in enumerate(lect):
    rr = MR + 1 + i
    c = ws.cell(rr, 1, "• " + t); c.font = f_small; c.alignment = wrap_l
    ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=6)
    ws.row_dimensions[rr].height = 16

def cf_levels(rng, first):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{first}="Forte"'],
                                                   fill=PatternFill("solid", fgColor="F4B6B6"), font=Font(name=F, bold=True, color="7F0000")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{first}="Modérée"'],
                                                   fill=PatternFill("solid", fgColor="FCE4D6"), font=Font(name=F, bold=True, color="833C0B")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{first}="Faible"'],
                                                   fill=PatternFill("solid", fgColor="E2EFDA"), font=Font(name=F, color="375623")))
cf_levels(f"D{GR_FIRST}:D{GR_LAST}", f"D{GR_FIRST}")
cf_levels(f"D{zr}", f"D{zr}")
cf_levels("B9", "B9")
ws.conditional_formatting.add(f"C{GR_FIRST}:C{GR_LAST}", FormulaRule(formula=[f'C{GR_FIRST}="Oui"'],
                              font=Font(name=F, bold=True, color="7F0000")))
ws.conditional_formatting.add(f"B{GR_FIRST}:B{GR_LAST}",
                              DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="8FB9A8"))
for cl in ("G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"):
    ws.column_dimensions[cl].hidden = True
ws.page_setup.orientation = "landscape"
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_area = f"A1:F{MR+len(lect)}"

# ================================================================ NOTICE
ws = ws_n
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 26
ws.column_dimensions["C"].width = 95
ws["B1"] = "Outil terrain biodiversité — Version 2.0"
ws["B1"].font = f_title
ws["B2"] = "Repérage très préliminaire de la sensibilité biodiversité d'un site, en une visite, sans connaissance naturaliste."
ws["B2"].font = f_sub
NOTICE = [
    ("À quoi sert l'outil", "À repérer, lors d'une visite unique (due diligence, acquisition, audit), les éléments sensibles d'un site pour la biodiversité, afin de les éviter dès la conception d'un projet, et s'il faut prévoir une expertise écologique."),
    ("Ce qu'il ne fait pas", "Il ne remplace pas un diagnostic écologique et ne permet pas de conclure à l'absence d'enjeu auprès de l'administration."),
    ("Qui peut le remplir", "Toute personne visitant le site, sans connaissance naturaliste ni connaissance de son historique. Les questions portent sur ce qui est visible le jour de la visite."),
    ("Quand", "En toute saison : l'évaluation repose d'abord sur les milieux, visibles toute l'année. Les animaux observés ne font qu'affiner le résultat. Prévoir 20 à 30 minutes."),
    ("Sur place", "Faire le tour du site, regarder ses abords, et s'aider si besoin d'une vue aérienne sur téléphone (Google Maps, Géoportail). Répondre dans les cellules jaunes de l'onglet « Saisie »."),
    ("En cas de doute", "Répondre « Ne sait pas » plutôt que « Non » (zone non accessible, élément difficile à juger, projet non défini) : l'outil en tient compte par précaution. Les questions grisées « Sans objet » n'ont pas à être renseignées."),
    ("Exemple de réponse", ""),
    ("Résultats", "L'onglet « Résultats » donne la sensibilité biodiversité du site, le détail par groupe d'animaux, un repérage des zones humides, la liste des éléments sensibles à préserver et les points d'attention."),
    ("Questions bonus", "Si un occupant ou le gestionnaire est présent, lui poser les questions de la partie 7. Elles portent sur des faits précis et répétés (nids chaque année, inondation chaque hiver…). Seul un « Oui » est pris en compte : un « Non » ou une absence de réponse ne diminue pas le résultat."),
    ("Paramétrage", "Les onglets « Pondérations » et « Paramètres » sont réservés à l'écologue référent (protégés sans mot de passe : Révision > Ôter la protection de la feuille). Les pondérations et seuils sont à calibrer sur des sites déjà diagnostiqués."),
]
r = 4
for k, t in NOTICE:
    ws.cell(r, 2, k).font = f_bold
    ws.cell(r, 2).alignment = wrap
    c = ws.cell(r, 3, t); c.font = f_norm; c.alignment = wrap
    ws.row_dimensions[r].height = est_height([(t, 95)], base=13.5, pad=6)
    for col in (2, 3):
        ws.cell(r, col).border = border
    r += 1
ws.cell(r + 1, 2, "Légende").font = f_sect
ws.cell(r + 2, 2).fill = fill_input; ws.cell(r + 2, 2).border = border
ws.cell(r + 2, 3, "Cellule à renseigner (onglet Saisie)").font = f_norm
ws.cell(r + 3, 2).fill = fill_param; ws.cell(r + 3, 2).border = border
ws.cell(r + 3, 2, "1").font = f_blue
ws.cell(r + 3, 3, "Paramètre modifiable par l'écologue référent").font = f_norm
ws.cell(r + 4, 2).fill = fill_grey; ws.cell(r + 4, 2).border = border
ws.cell(r + 4, 3, "Valeur calculée (ne pas modifier)").font = f_norm
ws.cell(10, 3).value = (f"Question n° {NUM['V2']} (grands arbres) : Réponse « Oui » ; "
                       "Commentaire « deux platanes au nord du site, photos 12 à 14 ».")

# ================================================================ protection
for c in META_CELL.values():
    ws_s[c].protection = ws_s[c].protection.copy(locked=False)
for code, rr in SROW.items():
    for col in ("D", "F"):
        ws_s[f"{col}{rr}"].protection = ws_s[f"{col}{rr}"].protection.copy(locked=False)
for rr in range(W_FIRST, W_LAST + 1):
    for j in range(NG):
        c = ws_w.cell(rr, 11 + j)
        c.protection = c.protection.copy(locked=False)
for row in ws_p.iter_rows():
    for c in row:
        if c.fill is not None and c.fill.fgColor is not None and c.fill.fgColor.rgb in ("00EAF1FB", "FFEAF1FB"):
            c.protection = c.protection.copy(locked=False)
for ws in (ws_s, ws_r, ws_w, ws_p):
    ws.protection.sheet = True
    ws.protection.formatColumns = False
    ws.protection.formatRows = False
    ws.protection.autoFilter = False
ws_n.protection.sheet = False

for wsx, orient in ((ws_n, "portrait"), (ws_w, "landscape"), (ws_p, "landscape")):
    wsx.page_setup.orientation = orient
    wsx.page_setup.paperSize = wsx.PAPERSIZE_A4
    wsx.page_setup.fitToWidth = 1
    wsx.page_setup.fitToHeight = 0
    wsx.sheet_properties.pageSetUpPr.fitToPage = True
ws_s.sheet_properties.tabColor = "FFC000"
ws_r.sheet_properties.tabColor = "1F4E3D"
ws_w.sheet_properties.tabColor = "8EA9DB"
ws_p.sheet_properties.tabColor = "8EA9DB"
wb.active = 1

# exports pour tests
import json
json.dump({"SROW": SROW, "META": META_CELL, "GR_FIRST": GR_FIRST, "ZR": zr, "AR": AR, "NA": len(ALERTES)},
          open(OUT + ".map.json", "w"))
wb.save(OUT)
print("ok", OUT, "questions:", len(QUESTIONS))
