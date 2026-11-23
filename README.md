# Outil terrain biodiversité

Questionnaire de pré-repérage biodiversité destiné à des non-spécialistes, pour une première lecture de la **sensibilité biodiversité d'un site** lors d'une visite unique (contexte de due diligence).

> **Statut : prototype de travail.** Les règles sont en cours de calibrage et l'outil ne remplace en aucun cas un diagnostic écologique.

## À quoi sert l'outil

- **Public** : un visiteur non écologue, venu sur site pour d'autres raisons (technique, foncier, environnement au sens large), sans connaissance de l'historique du site.
- **Ce qu'il produit** : un niveau de sensibilité par groupe (oiseaux, mammifères, chauves-souris, amphibiens, reptiles, libellules, criquets, papillons), des thèmes à part (zone humide, cours d'eau, flore et habitats), le type de contrainte attendue si l'enjeu est confirmé (C0 à C3) et la liste des éléments à préserver.
- **À quoi il sert** : orienter le choix des sites et éviter en amont les secteurs sensibles, puis cadrer le diagnostic écologique à commander.
- **Ce qu'il ne fait pas** : il n'évalue pas l'impact d'un projet (qui suppose un projet au moins esquissé), ne localise pas les enjeux et ne conclut jamais à l'absence d'espèces protégées. Un résultat « Faible » n'est délivré que sous conditions ; sinon le résultat est « Indéterminée ».

## Contenu du dépôt

| Dossier | Contenu |
| --- | --- |
| `app/` | Prototype de web app terrain (page HTML autonome : tuiles illustrées, appui long pour la fiche d'exemple, résultats, résumé à copier). S'ouvre directement dans un navigateur ; les réponses sont gardées dans le stockage local du navigateur. |
| `excel/` | Version Excel V2 (`Outil_terrain_biodiversite_V2.xlsx`) et le script Python qui la génère (`construire_excel.py`, openpyxl). |
| `moteur/` | Moteur V3 en Python (`engine_v3.py`) : table de décision, signal d'alerte du score et conditions du « Faible ». |
| `docs/` | Table de décision V3 (`table_de_decision.md`) : règles par groupe, conventions, décisions prises et points ouverts. |
| `validation/` | Test à l'aveugle sur 50 avis publics de MRAe : tableau de comparaison, données de codage et scripts d'analyse. |

## Versions

- **V2** (Excel et prototype actuels) : score additif pondéré par groupe, planchers sur les éléments déterminants, croisement avec la sensibilité réglementaire.
- **V3** (moteur et table de décision) : une **table de règles** fixe seule le niveau et le type de contrainte de chaque groupe ; le score additif ne sert plus que de **signal d'alerte** (seuil 30 %, vertébrés seulement). L'intégration de la V3 dans l'Excel et le prototype reste à faire.

Types de contrainte : **C0** aucune contrainte attendue · **C1** calendrier de travaux · **C2** expertise avant travaux · **C3** inventaires saisonniers, dérogation ou compensation possibles.

## Validation sur 50 avis de MRAe

Méthode en deux passes : la description physique du site, extraite de chaque avis, est d'abord codée en réponses au questionnaire et les sorties de l'outil sont figées ; les conclusions écologiques de l'avis sont ensuite extraites et comparées. Échantillon : 18 plateformes logistiques, 13 projets photovoltaïques ou agrivoltaïques, 8 ZAC ou lotissements, 7 data centers, 4 autres.

Taux de détection par groupe, sur les sites où l'avis relève un enjeu (règles actuelles, réponses non décrites traitées comme « Non ») :

| Groupe | Détectés |
| --- | --- |
| Oiseaux | 26/32 |
| Chauves-souris | 18/27 |
| Amphibiens | 11/16 |
| Reptiles | 6/17 |
| Insectes | 10/11 |
| Zones humides | 18/19 |
| Flore | 2/12 |
| Mammifères | 7/9 (9 sur-alertes sur 12 sites sans enjeu) |

Lecture : l'outil trie bien (un « Faible » est fiable : 1 à 4 faux « Faible » globaux sur 50 selon le traitement des réponses non décrites), mais discrimine peu, 43 sites sur 50 sortant en « Modérée » ou « Forte ». La flore et les reptiles sont les principaux angles morts. Des règles candidates (RE8, OI11, OI12, CS7) améliorent la détection sans sur-alerte supplémentaire, avec un risque de sur-ajustement à l'échantillon ; elles ne sont pas intégrées.

Pour relancer l'analyse :

```bash
cd validation
python3 analyse.py non   # réponses non décrites traitées comme « Non »
python3 analyse.py nsp   # réponses non décrites conservées en « pas sûr »
```

Limites du test : les avis de MRAe décrivent les sites de façon inégale, le codage a été fait à partir du texte et non d'une visite, et l'échantillon est biaisé vers des projets soumis à évaluation environnementale.

## Pistes de travail

- Intégrer la V3 dans l'Excel et le prototype.
- Ajouter une tuile « grandes cultures, plaine ouverte » (Œdicnème criard, busards).
- Rendre la vérification des zones humides au bureau systématique (cartes de prélocalisation).
- Distinguer, dans les résultats « Modérée », les cas relevant du seul calendrier de ceux qui demandent une expertise.
- Trancher l'usage de l'ancienneté du site (H1).
- Tableau de bord et gestion de portefeuilles de sites, dans un second temps.

## Licence

Aucune licence n'est définie pour l'instant : tous droits réservés par défaut.
