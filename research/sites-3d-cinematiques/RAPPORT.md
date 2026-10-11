# Sites web 3D « cinématiques » pilotés par le scroll : reverse-engineering du « wow »

*Analyse du 11 octobre 2026. Mesures image par image, lecture du code source, études de cas publiées.*

---

## 0. L'essentiel en 12 points

1. **Le wow ne vient pas du montage.**
   - 75 vidéos hero analysées, **0 coupe franche**. Chaque vidéo est un plan-séquence unique d'environ 10 s.
   - Sur les sites 3D au scroll, un « plan » dure **≈ 0,8 à 1 écran de scroll**, pas un nombre de secondes.
2. **La caméra bouge peu, et toujours de façon écrite à l'avance.**
   - Dans les heroes vidéo, caméra **fixe dans 76 % des cas**. Le mouvement vient du sujet : rotation, matière vivante, lumière.
   - Quand elle bouge, c'est un push-in lent : médiane **0,86 % d'échelle par seconde**.
   - Sur les sites WebGL, la caméra suit des keyframes ou une spline, et **le scroll sert de tête de lecture**.
3. **Un seul sujet, centré, dans du vide.**
   - Centre visuel horizontal médian à **0,50**. 86 % des vidéos sont centrées à ±8 %.
   - Le **tiers haut est la zone la plus vide dans 62 % des cas** : c'est là que va le titre.
4. **Fond sombre et un seul accent lumineux.**
   - 56 % des heroes sont sombres (luminance moyenne < 0,25), et 35 % ont plus de la moitié des pixels quasi noirs.
   - **Le bleu domine** (54 %) ; les teintes froides l'emportent 46 contre 20.
   - Sur la démo Codrops : 97 % de pixels quasi noirs et 7 à 10 % du cadre occupé.
5. **La lumière fait le spectacle.**
   - Lueur émissive (40/72), contre-jour ou rim light (31/72).
   - Reflet qui glisse sur un objet, néon qui s'allume, flash.
6. **La surprise est un événement de lumière ou d'échelle, rarement de montage.**
   - Flash blanc : sur Chronos, la luminance moyenne monte de 0,11 à **0,93** en 0,6 écran, puis retombe à 0,11 en 0,2 écran.
   - Coup de FOV de +25°.
   - Plan muet en plongée zénithale à −65° à mi-parcours.
   - Recul révélateur, montée puis noir total.
7. **Les transitions sont des effets, pas des coupes.** Portail, flash, FOV, aberration chromatique, givre (Igloo), stencil (KPR), œuf qui se fissure (Hatom).
8. **Le lissage fait le « cinéma ».**
   - Valeurs relevées : Lenis `lerp 0.09` ou `duration 1.15`, ScrollSmoother `smooth 4`, GSAP `scrub 0.5–1`, NYT `damping 0.5`.
   - Damping caméra : `1 − 0.001^dt`.
9. **Le texte est découpé en beats.**
   - Un titre par plan, sa position change à chaque plan : centre → gauche → droite → haut-gauche…
   - Entrée lettre par lettre (stagger 0,02), ou blur-in plus fade-up.
   - Durées médianes de 0,6 s.
10. **Une seule couleur dominante par chapitre.** Chronos change l'étalonnage complet (brouillard, fond, accent) à chaque époque : vert → ambre → cuivre → bleu → violet.
11. **Côté MotionSites, la « 3D » est presque toujours de la vidéo IA précalculée, pas du WebGL.**
    - 1 prompt sur 65 mentionne Spline, aucun Three.js.
    - La vidéo est générée en 24 fps, 10 s, puis posée en `autoplay muted loop` (72 % des prompts).
    - La couture de boucle est masquée par un fondu JS de 500 ms (14 % des prompts le décrivent explicitement).
12. **La vidéo scrubbée exige un encodage all-intra.**
    - Une image clé à chaque image : 240/240 vérifiées sur Scroll-Cinema.
    - **≈ 30 images par écran de scroll**.

---

## 1. Corpus et méthode

| Corpus | Contenu | Ce qui a été mesuré |
| --- | --- | --- |
| **A. Heroes vidéo MotionSites** | 85 fichiers du miroir public [TheSatyam-Singh/motionsites.ai](https://github.com/TheSatyam-Singh/motionsites.ai), soit **75 vidéos uniques** (9 doublons, 1 playlist HLS vide). Parmi elles, 71 heroes et 4 fonds de deck. Plus 65 prompts gratuits et 67 prompts Pro. | `ffprobe`, coupes (histogramme + `scdet`), flux optique caméra, activité, palette k-means, remplissage 3×3, centre visuel, symétrie, couture de boucle. Lecture visuelle de 75 planches contact de 8 images. Statistiques des prompts. |
| **B. Sites 3D au scroll open source, lancés en local** | [Codrops « Cinematic 3D Scroll Experiences »](https://github.com/JosephASG/codrops-cinematic-scroll-animations) (R3F + GSAP), [Chronos](https://github.com/harivansh-b/Chronos) (Three.js + GSAP + Lenis), [Scroll-Cinema](https://github.com/indranilnnd-creator/amazing-3d-animated-website-creator) (vidéo scrubbée + objet 3D), [NYTimes three-story-controls](https://github.com/nytimes/three-story-controls) (caméra). | Paramètres exacts lus dans le code : caméras, FOV, lissage, longueur de scroll, lumières, palettes. Captures pas à pas dans Chromium headless (WebGL logiciel), puis les mêmes mesures **par écran de scroll**. |
| **C. Sites primés** | Igloo Inc, Lusion (Oryzo), Apple (AirPods / iPhone / Vision Pro), Active Theory (Prometheus, Fiomet, CHILE20), Immersive Garden (Hatom, Cartier, David Whyte), Resn KPR, Dogstudio, Lando Norris, Bruno Simon, tutoriels Codrops / Three.js Journey. | Études de cas publiées, recherche web. Détail sourcé dans [`data/etudes_de_cas_sources.md`](data/etudes_de_cas_sources.md). |

**Limites, à lire avant d'utiliser les chiffres :**

- **Sites live inaccessibles.** La politique réseau de cet environnement bloquait l'accès direct à motionsites.ai, Apple, Lusion, Awwwards et les autres. Le corpus C repose donc sur les études de cas publiées, pas sur une mesure directe de ces sites.
- **Mouvement de l'image ≠ mouvement de caméra.** Le flux optique mesure le mouvement de l'image : un objet qui tourne ou grossit ressemble à un mouvement de caméra. Le type de mouvement a été tranché visuellement ; les vitesses chiffrées ne sont données que pour les vrais mouvements caméra.
- **Rendu logiciel.** Les captures WebGL ont tourné à 11–24 fps. Les chiffres « par écran de scroll » sont fiables ; ceux « par seconde » ne s'appliquent pas aux sites au scroll.
- **Pas de H.264 dans le Chromium de Playwright.** Le film de Scroll-Cinema n'a pas été décodé pendant la capture. Ses chiffres viennent du fichier et du code.
- **Scène trop sombre pour le flux optique.** Le flux optique ne marche pas sur Codrops (97 % de noir). Sa caméra est décrite depuis les keyframes du code, qui sont exactes.
- **Outil validé.** Pan, tilt et zoom synthétiques sont mesurés à ±5 % (détail dans `tools/README.md`).

---

## 2. Trois familles techniques

| Famille | Comment ça marche | Exemples | Ce qu'on contrôle |
| --- | --- | --- | --- |
| **Hero vidéo en boucle** | Un clip de 5 à 16 s en `autoplay muted loop playsInline`, `object-cover`, avec l'UI (glass, titres) par-dessus. | MotionSites (tout le corpus A) | Composition, lumière et action du clip ; boucle ; animation d'entrée du texte. |
| **Vidéo ou séquence scrubbée au scroll** | `currentTime = progression × durée`, ou index d'image dessiné dans un `<canvas>`. | Apple AirPods Pro (148 images, canvas 1158×770, codec « Flow » sur les pages iPhone) ; Scroll-Cinema (240 images all-intra) | Le scroll **est** la timeline : le film avance et recule avec le doigt. |
| **WebGL temps réel, caméra pilotée par le scroll** | Scène Three.js / R3F. Le scroll (0→1) fait avancer une timeline de keyframes caméra ou une spline, avec lissage. | Codrops, Chronos, Igloo, Lusion, Immersive Garden, Prometheus | Tout : caméra, FOV, lumière, post-process, transitions, interaction. |

---

## 3. Caméras

### 3.1 Heroes vidéo : 75 vidéos classées visuellement

| Mouvement | Nombre | Vitesse mesurée | Exemples |
| --- | --- | --- | --- |
| **Fixe ou quasi fixe (trépied)** | **57 (76 %)** | < 0,2 %/s | Velorah, Space Voyage, NOVA, New Era Automotive, Viktor Portfolio |
| **Push-in lent / dolly avant** | 11 (15 %) | 0,12 à 3,55 %/s (médiane 0,86) ; cumul de +1,5 à +53 % | Aethera (+27 %, accélère au milieu), CodeNest (+21 %), Framelix (+53 %, accélère sur toute la durée), Logoisum (+5,5 %, ease-out jusqu'à l'arrêt) |
| **Fly-through avant** | 2 | jusqu'à 10,5 %/s (+80 % en 8 s) | Nexora (forêt illustrée, boucle sans couture) ; Dark Portfolio (dans la matière) |
| **Pull-out révélateur** | 2 | −3,0 à −3,4 %/s (−35 à −37 %) | SkyElite : du réacteur incandescent à l'avion entier, rapide puis freiné. Vitesse par tiers : 11,3 → 8,2 → 1,9. |
| **Orbite** | 2 | — | Framelix (insecte de verre), SkyElite (combinée au recul) |
| **Travelling d'accompagnement (camera car)** | 1 | — | Targo (voiture, néons, étincelles) |

Autres constats :

- **Angles.** Le frontal domine (38/72), puis la contre-plongée (18), le 3/4 (15) et la plongée (13).
- **Valeurs de plan, en deux familles :**
  - **packshot** en gros plan ou plan moyen, un objet seul : 22 gros plans, 18 plans moyens ;
  - **diorama ou monde miniature** en plan large ou d'ensemble : 34.
- **Optique.** Le sujet est plus net que les bords dans 42/71 vidéos : isolement ou faible profondeur de champ.

> À retenir : dans un hero vidéo, **la caméra pose le cadre et le sujet fait le spectacle**. Un push-in de 0,5 à 2 %/s suffit à donner de la vie. Au-delà de 3 %/s, on entre dans le fly-through.

### 3.2 Sites 3D au scroll : la caméra est écrite et le scroll sert de tête de lecture

Dans les études de cas, **aucun site primé ne laisse la caméra libre** : OrbitControls est retiré (8 cas documentés). Les dispositifs relevés :

- **Keyframes interpolées** :
  - Codrops : 10 positions et cibles, `ease: none` ;
  - Prometheus : « une caméra de début et une caméra de fin par scène » ([Active Theory](https://medium.com/active-theory/prometheus-2d3c05b88ec0)) ;
  - Theatre.js + Drei `ScrollControls`.
- **Spline**. Codrops 2026 : courbe de Bézier dessinée dans Blender, exportée en JSON puis rejouée en `CatmullRomCurve3` ([Codrops](https://tympanus.net/codrops/2026/07/07/building-a-scroll-driven-3d-gallery-using-a-blender-camera-path-with-three-js-and-gsap/)). Dogstudio Panasonic : chemin dont l'orientation change en permanence.
- **Formules** :
  - Three.js Journey : `camera.y = −scrollY / hauteur × 4`, un travelling vertical d'une section par écran ;
  - Chronos : orbite puis dolly avant par époque.

**Codrops « Cinematic 3D Scroll », démo 2 : parcours exact** (900svh de contenu, 8 écrans de scroll, FOV 45, `ScrollSmoother smooth: 4`, `scrub: true`) :

| Plan | Scroll | Écrans | Distance au sujet | Angle vertical | Rotation autour du sujet | Titre (position) |
| --- | --- | --- | --- | --- | --- | --- |
| départ | 0 % | — | 25 | +37° (contre-plongée) | — | — |
| 1 | 0 → 11,9 % | 0,95 | 10,4 | +17° | −90° | DISCOVER (centre) |
| 2 | → 23,7 % | 0,94 | 10,6 | +11° | −17° | CYBERPUNK (gauche) |
| 3 | → 35,6 % | 0,95 | 10,0 | 0° | +107° | INNOVATION (droite) |
| 4 | → 45,8 % | 0,82 | 10,4 | +17° | 0° | ELEVATION (haut-gauche) |
| **5** | → 52,5 % | 0,54 | 16,6 | **−65° (plongée zénithale)** | **−135°** | **aucun : plan muet** |
| 6 | → 62,7 % | 0,82 | 15,0 | −42° | +18° | VISION (centre) |
| 7 | → 69,5 % | 0,54 | 12,2 | −24° | 0° | ARCHITECTURE (bas-droite) |
| 8 | → 77,9 % | 0,67 | 16,3 | +14° | −45° | FUTURE (bas-gauche) |
| 9 | → 84,7 % | 0,54 | 25,5 | +11° | −18° | SUMMIT (haut) |
| 10 | → 100 % | 1,22 | 22,4 | 0° | −27° | WELCOME (centre) |

La grammaire est lisible :

1. Plan large d'ouverture.
2. Approche serrée en contre-plongée, qui donne la monumentalité.
3. Grue qui monte le long du sujet (y de 2 à 35).
4. **À mi-parcours, rupture d'angle de −65° sans texte** : c'est la respiration et la surprise.
5. Redescente.
6. **Recul final en plan large** : c'est la révélation.

Le dernier plan est le plus long (1,22 écran) : on laisse l'image finale respirer. Le plan muet est parmi les plus courts (0,54 écran) : la surprise est brève.

**Chronos : parcours exact** (séquence épinglée de 700vh, soit 6 écrans de scroll ; FOV 50, 62 en portrait) :

- **0 → 20 % (1,2 écran) : plongée dans le portail.**
  - La caméra orbite en se rapprochant : le rayon passe de 11 à 1,4, avec une courbe smoothstep.
  - Pendant ce temps, le portail grossit de ×1 à ×5 (`1 + a³·4`).
- **5 époques de 0,96 écran chacune.** Dans chaque époque :
  - **dolly avant** de 34 unités (z de 14 à −20) ;
  - légère arche latérale (±2,5) et verticale (de 1,2 à 2,7).
- **Jonctions entre époques** : coup de FOV de +25° (de 50 à 75°) sur ±0,18 écran, puis flash blanc qui passe de 85 % d'opacité à 0 en 1,1 s.
- **Lissage caméra** : `lerp(1 − 0.001^dt)`, soit 99,9 % de rattrapage en 1 s, indépendamment du framerate. Il est multiplié par 2,5 pendant le voyage.
- **Regard libre** : on peut faire glisser pour tourner la tête autour du chemin scripté. La caméra reste guidée.

### 3.3 Lissage et inertie : valeurs relevées

| Projet | Lissage du scroll | Lissage des animations ou de la caméra |
| --- | --- | --- |
| Codrops démo 1 / 2 | ScrollSmoother `smooth: 4` (4 s de rattrapage) | `scrub: true` (caméra), `scrub: 0.5` (texte) |
| Chronos | Lenis `duration: 1.15`, synchronisé au ticker GSAP | caméra `1 − 0.001^dt` |
| Scroll-Cinema | Lenis `lerp: 0.09` | `scrub: 1`, seek vidéo seulement si l'écart dépasse 1/30 s |
| NYTimes three-story-controls | — | `dampingFactor: 0.5`, marge de 10 % |
| Drei `ScrollControls` (doc) | `damping: 0.25` (exemple) | — |
| Apple AirPods (reconstitution GSAP) | — | `scrub: 0.5` |

---

## 4. Rythme : le « nombre de plans par seconde »

### 4.1 Heroes vidéo

- **0 coupe franche sur 75 vidéos.**
  - Score `scdet` maximal mesuré : 2,17. Une vraie coupe donne environ 16 en calibration.
  - **1 plan par vidéo**, soit 0,1 plan/s pour une boucle de 10 s.
- **Cadence** : 65/71 à **24 fps**, 4 à 30 fps, 1 à 60 fps (objet WebM avec alpha), 1 à 12 fps.
- **Durée** : médiane **10,04 s**, soit 241 images. Répartition :
  - 41/71 autour de 10 s ;
  - 18 entre 12 et 16 s ;
  - 9 à 8 s ;
  - 2 à 5 s.
  - Ces durées correspondent aux sorties standard des générateurs vidéo IA. Deux fichiers portent la balise d'encodeur `Google`, compatible avec Veo.
- **Morphs cachés** : 7 vidéos montrent des transformations brusques sans coupe. Exemples : l'avion de SkyElite change de modèle entre 0 et 2,9 s ; la texture du globe de Finlytic se dédouble. Ce sont des artefacts de génération IA, pas un choix de montage.
- **Énergie à l'écran** : variation de luminance médiane de 6,2 %/s, donc c'est calme. Profil dans le temps :
  - 22 crescendos (l'action monte vers la fin) ;
  - 15 decrescendos ;
  - 34 plats.
  - Le pic d'activité tombe n'importe où dans le clip : aucune règle universelle du « moment wow à 2/3 ».

### 4.2 Sites au scroll : on compte en plans par écran

| Site | Longueur de scroll | Plans ou chapitres | Écrans par plan |
| --- | --- | --- | --- |
| Codrops démo 2 | 8 écrans | 10 keyframes caméra | **0,54 à 1,22 (moyenne 0,8)** |
| Chronos (voyage) | 6 écrans épinglés | 1 plongée + 5 époques | **1,2 puis 0,96** |
| Chronos (page entière) | 19,1 écrans (à 960×540) | 7 ruptures visuelles mesurées, soit 8 segments | 2,4 en moyenne. Les chapitres 3D sont groupés, et des sections HTML classiques s'intercalent. |
| Scroll-Cinema | 8,1 écrans (à 1280×720) | 1 film de 240 images, 8 « actes » de chorégraphie | **≈ 30 images de film par écran** (1 image tous les 24 px) |
| Three.js Journey | n sections | 1 section par écran | 1 |
| Sites primés (études de cas) | non publiée | **2 à 8 chapitres** : Igloo 3, Prometheus 2, KPR 3 tableaux, CHILE20 3 mondes, Panasonic 4 pièces, Hatom 5, Cartier 6 alcôves, Active Theory v5 8 | — |

**Les beats de texte suivent les plans.** Sur Codrops, chaque titre a sa propre timeline :

| Phase | Part du plan | Animation | Easing |
| --- | --- | --- | --- |
| Entrée | 25 % | lettres de x −100 à 0, opacité de 0 à 1, stagger −0,02 (de droite à gauche) | `power2.out` |
| Tenue | 50 % | — | — |
| Sortie | 25 % | lettres vers x +100 | `power2.in` |

**Animations d'interface, d'après 65 prompts MotionSites** :

- **Durées** : médiane **0,6 s** (p25 0,6, p75 0,8).
- **Délais** : médiane **0,4 s**, par paliers de 0,1 à 0,8 s.
- **Easings** : courbes custom rares (11 %). On trouve surtout `[0.25,0.1,0.25,1]`, `[0.4,0,0.2,1]` et `power3.out`.
- **Chronos** :
  - titre hero : lignes qui montent de 110 % (`yPercent`) en 1,3 s, `expo.out`, stagger 0,12 ;
  - titre « anomalie » : espacement des lettres de 0,4 em à 0 et flou de 10 px à 0, stagger 0,15.

---

## 5. Couleur et lumière

### 5.1 Heroes vidéo (71 heroes, mesure k-means)

- **Luminance** : médiane de 0,22.
  - **40 sombres** (< 0,25), 18 intermédiaires, 13 claires (> 0,6, high-key « produit/SaaS »).
  - 25/71 ont plus de 50 % de pixels quasi noirs.
- **Teinte dominante** : **bleu 38/71**, rouge 7, vert 6, orange 6, cyan 5, violet 4, or 2, rose 1. Froid contre chaud : **46 contre 20**.
- **Monochromie** : 29/71 vidéos ont plus de 80 % de leurs pixels colorés dans une seule famille de teinte. Recette type : une teinte et des neutres, plus éventuellement un accent complémentaire (bleu nuit et or chez Velorah, bleu et orange).
- **Saturation** : médiane de 0,46. On est sur des couleurs franches mais pas fluo, sauf pour l'accent.
- **Lumière, d'après la lecture visuelle de 72 vidéos** :
  - lueur émissive : 40 ;
  - contre-jour ou rim light : 31 ;
  - studio ou softbox : 18 ;
  - low-key : 10 ; nuit : 10 ; néon : 9 ; high-key : 9 ; volumétrique : 8.
  - Le centre est plus lumineux que les bords (spot ou vignettage) dans 30/71 vidéos.

Palettes mesurées représentatives (hex k-means, part des pixels) :

| Vidéo | Palette |
| --- | --- |
| Framelix 3D (libellules de verre) | `#020205` 66 % · `#080a1b` 18 % · `#16183f` 7 % · `#252774` 5 % · `#4446a3` 3 % · `#8483cc` 1 % |
| Velorah (nuit étoilée, golden light) | `#0d3c53` 67 % · `#201f16` 16 % · `#4f482e` 8 % · `#886529` 5 % · `#ce972c` 3 % · `#f4ee7b` 2 % |
| New Era Automotive | `#020100` 47 % · `#ae370a` 32 % · `#681b06` 8 % · `#eba662` 3 % |
| Nexora (forêt illustrée, high-key) | `#fcfdfc` 48 % · `#132a2c` 23 % · `#38574a` 10 % · `#b2cfd9` 7 % |
| Apex SaaS (verre bleu) | `#01020c` 60 % · `#2c59c1` 10 % · `#192c85` 9 % · `#4595d6` 8 % · `#aedbef` 4 % |

### 5.2 Sites 3D au scroll

**Codrops :**

- fond `#0a0a0a` et brouillard de la **même couleur** entre 12 et 28 unités : le décor se dissout dans le noir ;
- lumières : ambiante 0,4, deux directionnelles (1,2 et 0,6), une **seule lumière d'accent cyan `#00ffff`** ;
- fenêtres rouge-orange (`#e8623e`) ;
- mesuré : **97 % de pixels quasi noirs**.

**Chronos :**

- tone mapping **ACES Filmic, exposition 1,1** ;
- éclairage en trois points : hémisphérique `#9fd8ff` à 0,6, key blanche à 1,6, **rim violette `#a77bff` à 2,2** ;
- grain film en overlay SVG `feTurbulence` ;
- **étalonnage complet par chapitre**, sur un fond de base `#02040a` et un brouillard `#040a18` :

| Époque | Brouillard | Fond | Accent | Accent 2 |
| --- | --- | --- | --- | --- |
| Préhistoire | `#06140e` | `#030a07` | `#2fd18a` | `#d4b45a` |
| Antiquité | `#2a1708` | `#140a03` | `#ffb347` | `#c7843f` |
| Ère industrielle | `#1c0f08` | `#0c0604` | `#e0753a` | `#b86b3c` |
| Présent | `#061226` | `#02060f` | `#7cc7ff` | `#ffffff` |
| Futur | `#0b0620` | `#04020c` | `#a77bff` | `#3ef2ff` |

**Scroll-Cinema** : étalonnage CSS par acte. Luminosité de 0,92 à 1,02, saturation de 1,00 à 1,05, `sine.inOut`.

**Sites primés :**

- fonds sombres ou « dans le vide » avec un accent : Hatom (œuf lumineux), Artisans d'Idées (presque tout dans l'ombre), Lando Norris (lime) ;
- CHILE20 : noir et blanc granuleux avec grain film, puis néon ;
- bloom, profondeur de champ et FOV ne sont presque jamais documentés.

---

## 6. Composition : à quel point le cadre est rempli

### 6.1 Heroes vidéo

- **Remplissage** (part du cadre avec du détail) : médiane de **53 %**.
  - 17 vides (< 35 %), 27 aérés, 27 denses (> 65 %).
  - Les vides sont les abstraits sombres : verre, néon, objet sur noir. Les denses sont les dioramas, paysages et scènes cartoon.
- **Centrage** : centre visuel horizontal médian à **0,50**, et 61/71 vidéos sont à ±8 % du centre. Vertical médian à 0,53 : le sujet est légèrement sous le centre.
- **Zone vide réservée au texte** : remplissage moyen par bande de 44 % en haut, 66 % au milieu, 60 % en bas.
  - **La bande haute est la plus vide dans 44/71 vidéos**, la basse dans 22.
  - Le titre va donc en haut et le CTA en bas, ou l'inverse quand le sujet est haut.
- **Symétrie gauche-droite** : corrélation médiane de 0,52. Les compositions frontales et symétriques dominent.
- **Recette type** : un sujet unique, centré, sous le centre, avec un ciel ou du noir au-dessus. Velorah en est l'exemple parfait :
  - 60 % supérieurs = ciel étoilé vide ;
  - personnages et livres en bas ;
  - caméra fixe.

### 6.2 Sites 3D au scroll

- **Codrops** : 7 à 10 % du cadre occupé.
  - Une silhouette sombre de gratte-ciel, avec quelques fenêtres rouges et le brouillard qui avale le reste.
  - **Le texte change de coin à chaque plan** (centre, gauche, droite, haut-gauche, bas-droite, bas-gauche, haut). Il équilibre la masse du sujet, qui se déplace avec la caméra.
- **Chronos** : 36 % de remplissage moyen, avec 69 % de pixels quasi noirs.
  - Hero : objet à droite, texte à gauche.
  - Époques : titre en bas à gauche, liste des époques à droite, scène au centre.
- **Scroll-Cinema** : l'objet 3D **change de côté à chaque acte** (x de −1,35 à +1,35), toujours à l'opposé du texte.
- **Sites primés** : « un sujet central unique, beaucoup de vide autour », documenté dans 9 cas (Apple, Oryzo, Lando, Dogstudio, Hatom, CHILE20, Igloo, Cartier, Immersive Garden). Immersive Garden résume : « plus de temps passé à retirer qu'à ajouter ».

---

## 7. Ce qui se passe à l'écran

Les types d'action relevés dans les 72 heroes, du plus fréquent au plus rare :

1. **Matière vivante** : gel qui respire, fourrure, verre qui coule, ruban de soie, liquide qui s'effondre puis rebondit. C'est le « satisfying ».
2. **Objet qui tourne** (packshot sur plateau) : globe, cube prismatique, casque.
3. **Balayage de lumière** : reflet qui glisse sur une carrosserie (New Era, 4,3–8,6 s), néon qui se rallume (AKOR), glint qui traverse un logo (Power AI à ≈ 10 s).
4. **Micro-animation de personnage** : clin d'œil, salut, petit saut (Orbis NFT, NeoVision qui tourne la tête à 4–5,7 s).
5. **Environnement qui vit** : timelapse de nuages, pétales qui tombent, paysage qui défile derrière une vitre (Railroad).
6. **Croissance ou transformation** : fleur qui éclot, fusée qui décolle (NOVA, allumage à 1,4 s), ruban qui devient un tube de lumière (Apex, 5,7–8,6 s).
7. **Particules** : essaim qui s'éveille (Stellar, 7–10 s), débris qui frôlent l'objectif (Weblex, 10,3 s).

Côté sites au scroll, l'action est **déclenchée et réversible par le scroll** :

- la caméra avance ;
- les époques défilent ;
- le film avance ou recule ;
- l'objet tourne (+2,2 rad par acte sur Scroll-Cinema).

L'interaction s'ajoute par-dessus : parallaxe au curseur, drag pour regarder autour (Chronos), clic maintenu pour révéler (KPR), particules qui prennent une forme au survol (footer d'Igloo), son synchronisé (7 cas documentés).

---

## 8. Catalogue des effets de surprise, avec mesures

| Effet | Mesure ou paramètre | Où |
| --- | --- | --- |
| **Flash / whiteout** | luminance moyenne 0,11 → 0,56 → **0,93** en 0,6 écran, puis 0,11 en 0,2 écran ; overlay de 85 % à 0 en 1,1 s `power2.out` | Chronos, entrée dans le portail |
| **Coup de FOV** (warp) | FOV de 50 à 75° sur ±0,18 écran autour de chaque jonction | Chronos, changements d'époque |
| **Plan muet à angle extrême** | plongée à −65° et rotation de −135°, sans texte, entre 45,8 et 52,5 % du scroll | Codrops, mi-parcours |
| **Révélation d'échelle par recul** | −37 % d'échelle en 10 s, vitesse par tiers 11,3 → 8,2 → 1,9 (ease-out) | SkyElite (réacteur → avion) ; Codrops, plan final à distance 22–25 |
| **Crescendo puis noir** | luminance 0,05 → 0,39 sur ≈ 1,6 écran, puis **0,04** en 0,4 écran | Chronos, « anomalie » |
| **Plongée dans un objet / portail** | orbite dont le rayon passe de 11 à 1,4, portail ×5 | Chronos ; Fiomet (portail) ; KPR (stencil) |
| **Transition-effet** | aberration chromatique + displacement + givre | Igloo |
| **Ouverture-mystère** | œuf lumineux dans le vide qui se fissure au scroll | Hatom |
| **Objet qui frôle l'objectif** | blocs rocheux au premier plan à 10,3–10,6 s | Weblex |
| **Transformation de matière** | ruban → tube de lumière ; forme qui s'effondre puis rebondit | Apex, DesignPro |
| **Lumière qui « allume » l'objet** | balayage de reflet, néon qui se rallume | New Era, AKOR, Digitwist |
| **Interaction cachée** | clic maintenu, particules qui forment une silhouette au survol | KPR, Igloo |

Le principe commun : **une rupture sur un seul axe à la fois**, pendant que le reste ne bouge pas.

- La lumière, quand la caméra reste fixe.
- L'angle, quand le texte disparaît.
- L'échelle, quand on recule.
- La couleur, quand on change de chapitre.

---

## 9. La couche interface (65 prompts MotionSites)

| Motif | Part des prompts |
| --- | --- |
| Titre géant (`clamp()`, > 64 px, text-7xl+) | 80 % |
| Boutons pilule (`rounded-full`) | 78 % |
| Vidéo `autoplay` + `loop` + `muted` | 72 % |
| `object-cover` | 68 % |
| Interlettrage négatif (`tracking-tight`) | 60 % |
| `backdrop-blur` (glass) | 54 % |
| Inter | 46 % |
| Fade + slide-up | 45 % |
| Italique (souvent un accent serif) | 42 % |
| Instrument Serif | 37 % |
| Dégradé par-dessus la vidéo | 37 % |
| Framer Motion | 35 % |
| Blur-in (`blur(Npx)` → 0) | 32 % |
| Fondu JS de boucle : 500 ms d'entrée et 500 ms de sortie déclenchée 0,55 s avant la fin, `requestAnimationFrame`, remise à zéro de `currentTime` après 100 ms | 14 % (décrit explicitement) |
| « Liquid glass » | 31 % |
| Stagger | 29 % |
| HLS.js (vidéo en streaming) | 22 % |
| Marquee infini | 17 % |
| Three.js / Spline (3D temps réel) | **≈ 2 %** |

Ce fondu de boucle compense un défaut réel : seules **27/71** vidéos bouclent sans couture (`loop_seam_ratio` ≤ 3) et **27** sautent visiblement. Les vidéos qui sautent sont surtout celles qui font monter un effet : fusée, crescendo de particules, néon qui s'allume.

---

## 10. Recettes pour reproduire

*Recommandations tirées des mesures ci-dessus. Les valeurs sont des points de départ.*

### 10.1 Hero vidéo cinématique (génération IA + overlay)

**Le clip :**

- **Un seul plan** de 8 à 10 s en 24 fps.
- **Caméra fixe, ou push-in de 0,5 à 2 %/s.**
- Sujet unique centré, légèrement sous le centre.
- **Tiers haut vide** (ciel, noir, brume).

**Lumière et couleur :**

- Fond sombre (luminance moyenne ≈ 0,1–0,2).
- **Une teinte dominante** avec ses neutres, et un accent émissif ou en contre-jour.
- Bleu, violet ou teal pour le « tech » ; or ou orange pour le « premium chaud ».

**Action et boucle :**

- Une seule action continue : matière, rotation ou balayage de lumière.
- Un événement-wow qui ne se répète pas.
- Pour une boucle propre, faire que l'état final soit égal à l'état initial (rotation complète, respiration). Sinon, prévoir le fondu JS de 500 ms.

**Squelette de prompt vidéo** (Veo, Kling…) :

> *Single continuous shot, no cuts, 24fps, 10 seconds. Locked-off camera* [ou : *very slow dolly-in*], *frontal / slight low angle, 50mm, shallow depth of field. Centered* [sujet] *in the lower half, upper third empty* [night sky / black void / soft fog]. *Dark background, monochrome* [deep blue] *palette with a single* [warm gold] *emissive accent, rim light from behind. The* [sujet] [action continue : slowly rotates / breathes / light sweeps across its surface]; *at mid-clip* [événement : a light pulse / petals start to fall]. *Ends in the same pose as it starts (seamless loop).*

**L'overlay :**

- Titre géant en tracking serré, avec un mot en italique serif.
- Entrée en blur-in ou fade-up : 0,6 s, délais de 0,1 à 0,4 s en cascade.
- Navbar en verre (`backdrop-blur`), boutons pilule.
- Dégradé vers la couleur de fond en bas de la vidéo.

### 10.2 Site 3D au scroll (WebGL)

**Structure :**

- **6 à 10 plans sur 8 à 10 écrans de scroll**, soit 0,8 à 1 écran par plan. Pour un récit plus ample, 2 à 8 chapitres.
- Chaque plan = une position et une cible caméra. Interpolation `ease: none` sur la timeline ; c'est le lissage qui donne l'inertie.

**Courbe de caméra** :

1. Large.
2. Serré en contre-plongée.
3. Grue qui monte.
4. **Plan muet à angle extrême** (plongée ou contre-plongée) à 45–55 %.
5. Redescente.
6. **Recul final**, sur le plan le plus long : ≈ 1,2 écran.

**Optique et lissage :**

- FOV de 45 à 50° (60–62 en portrait). Coup de FOV de +20 à 25° sur les jonctions.
- Lenis `lerp` 0,08–0,1 ou `duration` ≈ 1,1–1,2 s, ou ScrollSmoother 1–4.
- Caméra amortie par `1 − 0.001^dt`.

**Lumière et couleur :**

- Brouillard de la couleur du fond, pour dissoudre le décor.
- Une seule lumière d'accent ; tone mapping ACES, exposition ≈ 1,1 ; grain léger.
- Un étalonnage par chapitre : brouillard, fond et accent en hex.

**Transitions** : un effet par chapitre (flash de 85 % à 0 en 1,1 s, portail, aberration chromatique), jamais une coupe sèche.

**Texte :**

- Un titre par plan, position différente à chaque plan, toujours à l'opposé de la masse du sujet.
- Lettres en stagger 0,02 : 25 % d'entrée, 50 % de tenue, 25 % de sortie.

**Performances** (pratiques des studios primés) : Draco / KTX2, une scène rendue à la fois, preloader qui occupe l'utilisateur, effets secondaires à cadence réduite.

### 10.3 Film scrubbé (Apple-style)

- Encodage **all-intra** (`-g 1`, une image clé à chaque image) en 720p–1080p.
- **≈ 30 images par écran de scroll** : un film de 8 s à 30 fps couvre environ 8 écrans.
- `currentTime = progression × durée`, appliqué dans `requestAnimationFrame`, et seulement si `readyState ≥ 2` et que la vidéo n'est pas déjà en train de chercher une image.
- Dessiner chaque image dans un canvas en gardant la dernière image valide, pour éviter les flashs noirs.
- Serveur compatible HTTP Range.

---

## 11. Fichiers

**Données (`data/`) :**

- `hero_videos_metrics.jsonl` : mesures de chacune des 75 vidéos.
- `hero_videos_probe.csv` : fiche technique de chaque vidéo.
- `hero_videos_visual.jsonl` : 72 descriptions visuelles structurées (sujet, action, valeur de plan, angle, caméra, optique, lumière, rendu, composition, zone texte, palette, effet wow, transitions, boucle, score).
- `prompt_features.json` : motifs relevés dans chaque prompt.
- `scroll_captures/*.json` : mesures pas à pas des captures au scroll (Codrops, Chronos, Scroll-Cinema).
- `etudes_de_cas_sources.md` : les études de cas, avec une URL par fait.

**Outils (`tools/`)** : scripts de mesure, réutilisables sur n'importe quelle vidéo ou URL locale. Voir `tools/README.md`.
