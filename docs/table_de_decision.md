# Table de décision de l'outil terrain biodiversité

Version du 21 novembre 2026.

## Objet et principes

La table fixe seule le niveau de sensibilité de chaque groupe ; le score pondéré ne sert plus qu'à signaler une fiche à relire. Le document est à valider règle par règle avant le passage en V3 de l'Excel et du prototype.

1. **Une règle relie un élément relevé, ou une combinaison d'éléments, à un groupe, un niveau et un type de contrainte.** L'étendue intervient comme un élément à part entière (par exemple « bois ou nombreux grands arbres »).
2. **Le niveau d'un groupe est le plus haut niveau parmi les règles déclenchées.** Aucune règle déclenchée donne « Faible », sous les conditions de la dernière partie.
3. **Une observation ou un signalement d'occupant est une règle comme une autre**, de niveau généralement fort.
4. **Le niveau intègre déjà le statut réglementaire du groupe.** La matrice de croisement avec la sensibilité réglementaire disparaît : chaque règle porte directement le niveau retenu.
5. **Le niveau et la contrainte sont deux informations distinctes.** Le niveau exprime la probabilité que l'enjeu soit réel ; la contrainte décrit ce qu'il impliquerait s'il est confirmé. Une règle peut être de niveau modéré et de contrainte lourde (Petit Gravelot sur une grande friche minérale).
6. **Le score pondéré de la V2 est conservé comme signal d'alerte** : un groupe classé « Faible » par la table mais avec un score élevé est signalé à l'écologue en relecture.

La distinction des contraintes s'appuie sur l'avis du Conseil d'État du 9 décembre 2022 (n° 463563) : une dérogation n'est requise que si le risque pour les espèces protégées reste suffisamment caractérisé après mesures d'évitement et de réduction ([analyse sur le site du Conseil d'État](https://www.conseil-etat.fr/fr/arianeweb/CE/analyse/2022-12-09/463563)).

## Conventions

Trois niveaux, quatre types de contrainte et une trentaine d'éléments codifiés, dont trois nouveaux, servent à écrire toutes les règles.

**Niveaux**

| Niveau | Signification |
| --- | --- |
| Forte | Présence d'espèces protégées ou d'une zone humide probable, ou avérée |
| Modérée | Présence possible ; à confirmer par un écologue |
| Faible | Aucun élément déterminant relevé |

**Types de contrainte, si l'enjeu est confirmé**

| Code | Contrainte | Conséquence typique pour le projet |
| --- | --- | --- |
| C0 | Aucune contrainte réglementaire attendue | Bonnes pratiques de chantier |
| C1 | Calendrier de travaux | Abattage, débroussaillage ou démolition hors période sensible ; pas de dérogation en général |
| C2 | Expertise avant travaux | Vérification ciblée (bâti, arbres, abris), mesures de réduction (exclusion, défavorabilisation, gîtes de substitution) |
| C3 | Inventaires saisonniers, dérogation ou compensation possibles | Inventaires sur un cycle annuel ; dossier espèces protégées ou loi sur l'eau si l'évitement est impossible |

**Éléments relevés**

| Code | Élément | Statut |
| --- | --- | --- |
| A1 | Bois, champs, prairies ou friches en bordure | V2 |
| A2 | Cours d'eau, étang ou mare à proximité | V2 |
| V1 | Site en bonne partie végétalisé | V2 |
| V2 / V2b | Grands arbres / bois, alignement ou plus de 10 | V2 |
| V3 | Arbres à cavités, fentes, écorce décollée ou lierre dense | V2 |
| V4 / V4b | Haies, buissons, ronces / haies ou fourrés importants | V2 |
| V5 / V5b | Herbe sans entretien / plus d'un quart du site | V2 |
| E1 / E2 | Mare, bassin ou fossé / berges en pente douce et végétalisées | V2 |
| E3 | Eau stagnante, boue | V2 |
| E4 / E4b | Roseaux, joncs / zone dense | V2 |
| B1 / B1b | Tas de pierres, de gravats ou de bois / plusieurs tas ou murets | V2 |
| B2 | Bâtiments | V2 |
| B3 | Locaux vides ou peu utilisés | V2 |
| B4 | Fissures, trous, tuiles cassées, ouvertures | V2 |
| S1 / S1b | Sol nu, sable ou cailloux / surface d'un terrain de football ou plus | V2 |
| K1 | Cours d'eau traversant ou longeant le site | Nouveau |
| H1 | Partie du site non construite et non terrassée depuis plus de 20 ans | Nouveau |
| S2 | Front vertical de sable ou de terre meuble (talus, stock, carrière) | Nouveau |
| F1 à F8 | Animaux observés pendant la visite (F1 scindé en F1a, nids en boue sous les toits, et F1b, nids dans la végétation) | V2 |
| I1 à I7 | Faits signalés par un occupant | V2 |

H1 se renseigne au bureau, à partir de l'étude historique de la due diligence ou des photographies aériennes anciennes.

## Oiseaux

Les oiseaux sortent rarement en dessous de « Modérée » dès qu'il y a de la végétation ou du bâti ouvert ; la contrainte, elle, va du simple calendrier à la dérogation selon l'espèce et le support du nid.

| Règle | Déclencheur | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- |
| OI1 | V3 | Forte | C2 | Arbres à cavités : nidification d'espèces cavicoles protégées (pics, mésanges, chouettes) |
| OI2 | F1a ou I1 | Forte | C3 | Nids d'hirondelles en boue, réutilisés chaque année ; leur destruction relève en pratique de la dérogation |
| OI3 | F1b | Modérée | C1 | Nid dans un arbre ou une haie : passereaux communs, gérés par le calendrier |
| OI4 | B4 | Modérée | C2 | Ouvertures et débords de toit : martinets (nids invisibles depuis le sol), moineaux, rougequeues |
| OI5 | V4 | Modérée | C1 | Haies et buissons : nidification de passereaux protégés communs |
| OI6 | V2b | Modérée | C1 | Bois ou nombreux grands arbres : nidification arboricole |
| OI7 | S1b | Modérée | C3 | Grandes surfaces minérales : Petit Gravelot ; Œdicnème criard si le contexte est ouvert (A1) |
| OI8 | S1 et (A2, E1 ou E3) | Modérée | C3 | Gravier ou sable nu près de l'eau, même sur petite surface : contexte typique de nidification du Petit Gravelot |
| OI9 | E4b | Modérée | C3 | Roselière : passereaux paludicoles (rousserolles, Bruant des roseaux) |
| OI10 | S2 | Modérée | C2 | Front de sable vertical : colonies possibles d'Hirondelle de rivage |

F1a est illustré par une photo de nid d'hirondelle en boue, reconnaissable toute l'année ; les nids de martinets, rarement visibles, sont couverts par B4. OI8 traite le Petit Gravelot par le contexte plutôt que par la surface : l'espèce s'installe volontiers sur de petites surfaces minérales proches de l'eau.

## Mammifères terrestres

L'enjeu porte surtout sur le Hérisson d'Europe et l'Écureuil roux, gérés par le calendrier, et sur les mammifères semi-aquatiques des cours d'eau, qui relèvent d'inventaires.

| Règle | Déclencheur | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- |
| MA1 | K1 | Modérée | C3 | Berges : Campagnol amphibie, Loutre, Castor, espèces protégées |
| MA2 | V4 et A1 | Modérée | C1 | Haies reliées aux milieux voisins : gîtes et déplacements du Hérisson |
| MA3 | V4b | Modérée | C1 | Haies ou fourrés importants : Hérisson |
| MA4 | V2b | Modérée | C1 | Bois ou nombreux grands arbres : nids d'Écureuil roux |
| MA5 | F3 ou I5 | Modérée | C1 | Présence avérée d'espèces protégées communes ; précautions de défrichement et de calendrier ; espèce citée nommément dans la restitution |

MA5 abaisse le niveau de la V2, qui donnait « Forte » pour un hérisson observé ; en contrepartie, l'espèce observée est citée nommément dans la restitution.

## Chauves-souris

Toutes les règles portent sur les gîtes, arboricoles ou dans le bâti ; les terrains de chasse seuls ne déclenchent rien et relèvent du signal d'alerte.

| Règle | Déclencheur | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- |
| CS1 | F2 ou I2 | Forte | C3 | Gîte avéré : dérogation probable en cas d'atteinte |
| CS2 | V3 | Forte | C2 | Gîtes arboricoles potentiels ; abattage après vérification, de préférence en septembre-octobre |
| CS3 | B3 et B4 | Forte | C2 | Local peu fréquenté et accessible : gîte potentiel d'été ou d'hiver |
| CS4 | B4 | Modérée | C2 | Fissures, disjointements, bardages : gîtes potentiels |
| CS5 | B3 | Modérée | C2 | Local vide sans ouverture visible : accès possible par de petites fentes |
| CS6 | V2b | Modérée | C1 | Bois ou nombreux grands arbres : gîtes et chasse |

CS5 est nouvelle : la V2 ne relevait un local vide qu'en présence d'ouvertures visibles, alors qu'une fente de 1,5 cm suffit à une pipistrelle.

## Amphibiens

Sans point d'eau sur le site ni milieu aquatique proche, les amphibiens restent « Faible » : c'est la principale correction par rapport au score additif de la V2.

| Règle | Déclencheur | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- |
| AM1 | F4 ou I3 | Forte | C3 | Présence avérée, reproduction probable sur le site |
| AM2 | E1 et E2 | Forte | C3 | Point d'eau à berges favorables : site de reproduction |
| AM3 | E1, berges en « pas sûr » | Modérée | C3 | Berges non vérifiées : reproduction possible |
| AM4 | E1, berges défavorables (E2 « Non ») | Faible | C0 | Bassin abrupt, sans végétation, bétonné ou bâché : très faible intérêt écologique |
| AM5 | E3 | Modérée | C3 | Eaux temporaires : espèces pionnières (Crapaud calamite, Sonneur à ventre jaune) |
| AM6 | E4b | Modérée | C3 | Roselière : milieu aquatique ou très humide |
| AM7 | A2 et (V2b ou V4b) | Modérée | C1 | Habitat terrestre d'hivernage proche d'un milieu aquatique |

E2 ne se répond « Non » que si les trois critères sont réunis : bords abrupts, absence de végétation, béton ou bâche ; la question sera reformulée en ce sens. Aucune règle ne relie le cours d'eau (K1) aux amphibiens : la plupart des espèces ne se reproduisent pas en eau courante, et les annexes ou bras morts sont captés par E1, E3 et E4. AM7 reprend la seule part légitime de l'ancien score : des boisements ou des haies importantes près d'un milieu aquatique peuvent abriter des amphibiens en phase terrestre.

## Reptiles

Le niveau fort exige des abris associés à une végétation de lisière ; les grandes friches, herbacées ou minérales, donnent un niveau modéré même sans abri visible.

| Règle | Déclencheur | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- |
| RE1 | F5 ou I4 | Forte | C2 | Présence avérée : défavorabilisation avant travaux, dérogation si des individus ne peuvent être évités |
| RE2 | B1 et V4 | Forte | C2 | Abris et lisières de buissons : habitat complet (Lézard des murailles, couleuvres, Orvet) |
| RE3 | B1 et V5 | Forte | C2 | Abris et herbe haute : habitat complet |
| RE4 | B1 | Modérée | C2 | Abris isolés : Lézard des murailles notamment |
| RE5 | V4b et V5b | Modérée | C1 | Lisières et friches étendues |
| RE6 | S1b | Modérée | C1 | Bordures et fissures des grandes friches minérales |

B1b (plusieurs tas ou murets) ne change pas le niveau, déjà fixé par la présence d'un abri ; il pourra préciser l'ampleur des mesures dans la restitution à l'écologue.

## Insectes

Les trois groupes d'insectes restent distincts dans la restitution, leurs enjeux et leurs habitats différant ; ils sont plafonnés à « Modérée », peu d'espèces étant protégées, mais deux contextes peuvent en abriter de localisées.

| Règle | Déclencheur | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- |
| IN1 | K1 | Modérée | C3 | Ruisseaux ensoleillés : libellules rhéophiles protégées (Agrion de Mercure, Cordulie à corps fin) |
| IN2 | H1 et (V5 ou S1) | Modérée | C3 | Pelouses ou friches anciennes : papillons protégés (Azurés, Damier de la Succise), à vérifier au printemps |
| IN3 | E1 et E2 | Modérée | C0 | Mare favorable : cortège de libellules, rarement protégé |
| IN4 | V5b | Modérée | C0 | Grande friche herbacée : criquets et papillons, rarement protégés |
| IN5 | F6, F7 ou F8 | Faible | C0 | Insectes communs observés : sans incidence réglementaire attendue |

IN5 retire l'effet actuel d'une observation de papillon ou de criquet, qui faisait monter le groupe sans justification réglementaire. Les insectes du bois mort (Grand Capricorne) restent hors du champ, faute de question accessible à un non-spécialiste ; V3 et V2b les couvrent indirectement.

## Zones humides et autres contraintes

Trois contraintes ne dépendent d'aucun groupe d'animaux : zone humide, cours d'eau, flore et habitats anciens. Elles figurent à part dans la restitution.

| Règle | Déclencheur | Thème | Niveau | Contrainte | Justification |
| --- | --- | --- | --- | --- | --- |
| ZH1 | E3, E4 ou I6 | Zone humide | Forte | C3 | Indices d'hydromorphie ou de végétation hygrophile ; au-delà de 0,1 ha touché, dossier loi sur l'eau (rubrique 3.3.1.0) |
| ZH2 | A2, ou E3 ou E4 en « pas sûr » | Zone humide | Modérée | C2 | Contexte favorable ; sondages pédologiques à prévoir |
| CE1 | K1 | Cours d'eau | Forte | C3 | Travaux en lit ou en berge soumis à la loi sur l'eau ; ripisylve et frayères à préserver |
| FH1 (provisoire) | H1 et (V5 ou S1) | Flore et habitats | Modérée | C3 | Milieux anciens non remaniés : flore protégée et habitats d'intérêt plausibles ; inventaire floristique printanier |
| FH2 (provisoire) | H1 et V5b | Flore et habitats | Forte | C3 | Grande surface de végétation ancienne non entretenue |

FH1 et FH2 restent provisoires : la traduction de l'ancienneté en niveau n'est pas tranchée. Alternative : H1 ne fixe aucun niveau et figure seulement dans la restitution destinée à l'écologue, comme incitation à vérifier la flore au printemps. La renouée asiatique est retirée de l'outil, un non-spécialiste l'identifiant mal.

## Signal d'alerte et conditions d'un « Faible »

Un groupe classé « Faible » avec un score de 30 % ou plus est signalé à l'écologue, et la sensibilité globale ne peut être « Faible » que si quatre conditions sont réunies.

**Signal d'alerte du score**

- Le score pondéré de la V2 reste calculé pour chaque groupe, sans effet sur le niveau.
- Seuil retenu : 30 %, par sécurité, appliqué aux seuls vertébrés (oiseaux, mammifères, chauves-souris, amphibiens, reptiles), les insectes produisant surtout des signaux sans portée réglementaire. Sur les six sites fictifs, il signale quatre fiches : zone d'activités (chauves-souris, amphibiens, reptiles), pavillon (mammifères), parc boisé (reptiles), ancienne ferme (amphibiens).
- Chaque fiche signalée puis jugée par l'écologue indique soit une règle manquante, soit un poids à corriger : c'est la source principale de calibrage.

**Conditions d'une sensibilité globale « Faible »**

1. Le tour complet des espaces extérieurs a été fait.
2. Les éléments déterminants (V3, B3, B4, E1, E3, E4, B1, K1) comptent au plus deux réponses « pas sûr ».
3. S'il y a des bâtiments, la question sur les locaux vides a reçu une réponse ferme : ils ont été visités ou leur absence est certaine.
4. Aucun groupe n'est signalé par le score.

Si une condition manque, le résultat affiché est « Indéterminée, à confirmer par un écologue », avec la condition en cause. Les niveaux « Modérée » et « Forte » restent délivrés sans condition : un manque d'information ne peut pas faire baisser une sensibilité déjà établie.

## Points à trancher

Sept points sur huit sont tranchés et intégrés à la table ; seul l'usage de l'ancienneté (H1) reste ouvert. Les réponses apportées en relecture figurent après chaque question.

- **Nids (OI2, OI3)** : séparer F1 en « nids sur les bâtiments » et « nids dans la végétation » ? — Oui, mais pas sûr qu'un non-expert sache identifier un nid d'hirondelle, et un nid de martinet est rarement visible. Ajouter dans l'outil une image de nid d'hirondelle peut-être ?
- **Hérisson ou écureuil observé (MA5)** : niveau modéré proposé, au lieu du niveau fort de la V2. — Oui, en les citant dans le compte rendu.
- **Point d'eau aux berges défavorables (AM3)** : bassin bâché ou bétonné en « Modérée », ou « Faible » ? — Il faut effectivement déterminer les cas où les points d'eau sont défavorables, parce qu'un bassin abrupt, sans végétation et bétonné n'a que très peu d'intérêt écologique.
- **Cours d'eau et amphibiens** : faut-il une règle K1 pour les annexes et bras morts, ou le signal d'alerte suffit-il ? — Pour les cours d'eau, il faut faire attention, car toutes les espèces ne sont pas rhéophiles.
- **Ancienneté (H1)** : seuil de 20 ans, et source privilégiée (étude historique de la due diligence, photographies aériennes anciennes de l'IGN). — Difficile à traduire vraiment en alerte.
- **Petit Gravelot sur petites surfaces de gravier** : ajouter une règle saisonnière (S1 seul, visite entre mars et juillet), ou accepter cet angle mort ? — Il faut peut-être regarder le contexte dans ce cas, par rapport à l'écologie de l'espèce.
- **Seuil du signal d'alerte** : 40 %, à ajuster après le calage sur des dossiers archivés. — Prendre une sécurité d'ordre scientifique.
- **Insectes côté client** : une seule ligne « Insectes », ou détail par groupe ? — Tous les groupes d'insectes ne portant pas les mêmes enjeux et les mêmes habitats, il faut différencier.

**Décisions intégrées**

| Point | Décision | Règles modifiées |
| --- | --- | --- |
| Nids | F1 scindé ; photo de nid d'hirondelle en boue ; martinets couverts par B4 | OI2, OI3, OI4 |
| Hérisson ou écureuil | Niveau modéré, espèce citée dans la restitution | MA5 |
| Point d'eau | « Faible » si bords abrupts, sans végétation, bétonnés ou bâchés ; « Modérée » si non vérifié | AM3, AM4 |
| Cours d'eau et amphibiens | Pas de règle : la plupart des espèces ne sont pas rhéophiles | aucune |
| Petit Gravelot | Règle de contexte : sol nu près de l'eau, quelle que soit la surface | OI7, OI8 |
| Signal d'alerte | 30 %, vertébrés seulement | Signal d'alerte |
| Insectes | Trois groupes distincts dans la restitution | IN1 à IN5 |
| Renouée | Retirée de l'outil | EE1 supprimée |
| Ancienneté | Ouvert : règle de niveau, ou simple information pour l'écologue | FH1, FH2 provisoires |
