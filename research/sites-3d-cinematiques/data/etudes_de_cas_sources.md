# Sites 3D "cinématiques" pilotés par le scroll : études de cas (reverse-engineering du "wow")

> Méthode : recherche faite le 2026-10-11, uniquement avec WebSearch. WebFetch a échoué (`getaddrinfo ENOTFOUND www.awwwards.com`) : je n'ai donc pas pu lire les pages en entier, seulement les extraits renvoyés par la recherche.
> Chaque fait renvoie à une URL. Mention **[tiers]** = source secondaire (agrégateur, roundup, clone GitHub, réseau social), moins fiable que l'étude de cas du studio. **non documenté** = aucune source trouvée.
> Ce qui est très rarement publié, pour tous les sites : FOV/focale, longueur de scroll exacte en vh, présence de bloom. J'ai mis "non documenté" partout où c'est le cas, sans extrapoler.

---

## 1. Igloo Inc (igloo.inc), par Abeto x Bureaux

**Prix et contexte**
- Landing page d'Igloo Inc., maison mère de Pudgy Penguins. Bureaux a proposé la collaboration à Abeto [1].
- Awwwards SOTD en juillet 2024 (7,92/10), plus Honors Business & Services [2][4].
- Abeto annonce avoir gagné Site of the Year et Developer Site of the Year sur Awwwards [3].

**Technique et stack**
- WebGL temps réel, rendu entièrement en WebGL [5].
- Stack : Three.js, Svelte, GSAP, Houdini, Blender, avec beaucoup d'outils propriétaires par-dessus [5].
- Colorlib indique plutôt "Custom (Vite), three.js, GSAP" [6][tiers].
- Méthode de travail : le code et l'art 3D avancent en même temps, directement dans le navigateur [1].
- Les blocs de glace sont **procéduraux**. Un algorithme maison imite la croissance de cristaux de glace à l'intérieur d'un contenant (cube, cylindre…). Les raisons : contraintes de temps, et un pipeline capable de s'étendre si d'autres projets s'ajoutent [1][5].
- Au départ il y avait un seul bloc pour tous les projets. Ils ont été différenciés parce que les projets "se ressemblaient trop au scroll" [1].
- **Toute l'UI est rendue en WebGL** :
  - les glitchs de texte sont faits en shader ;
  - le "scramble" des lettres échange des offsets de texture SDF au lieu de relayouter le DOM à chaque frame [5].
  - Revers : tout le texte est dans le canvas, donc aucun texte HTML pour le SEO ni les lecteurs d'écran [6][tiers].

**Caméra**
- Au scroll, la caméra "vole" vers des cubes de glace flottants. Chaque cube contient une société du portefeuille, en commençant par Pudgy Penguins [6][tiers].
- La caméra "dérive" entre les scènes [5].
- L'étude de cas montre une prévisualisation (previs) du trajet caméra jusqu'aux particules du footer [7].
- Selon une page TikTok, la position du scroll pilote directement la caméra et l'état des objets, au lieu de déclencher des animations DOM séparées [8][tiers, faible fiabilité].
- FOV, lissage et longueur de scroll : non documentés.

**Découpage**
- Page en **trois sections**. Comme cela rendait l'engagement difficile, l'équipe a ajouté beaucoup d'éléments interactifs [7].
- Awwwards classe le site sous les tags "Infinite Scroll", "Transitions", "3D" [2].
- **Transitions** : mélange d'aberration chromatique, de "tech displacement" et d'effet de givre (frost) [5].

**Palette et lumière**
- Une source peu fiable parle de "palettes en niveaux de gris élégantes" [7][tiers, faible fiabilité].
- Les particules changent de couleur selon leur vitesse et "brillent" quand elles prennent une nouvelle forme [9].
- Bloom, grain, tone mapping : non documentés.

**Composition**
- Un sujet par plan : un bloc de glace unique par projet [1][5].

**Interaction et surprise**
- Footer : simulation de particules interactive. Les points s'agrègent en différentes formes 3D selon le lien survolé [7].
- Ces particules sont pilotées par des données volumétriques (VDB), via un exporteur VDB vers navigateur écrit sur mesure [5].
- **Son** : musique et effets sonores de Bureaux, synchronisés avec le mouvement des particules (outil : DaVinci Resolve) [9].

**Performances**
- Les données volumétriques sont compressées "plus petites qu'une image de site classique" [5].
- La performance a été mesurée pendant tout le développement, pour garder une navigation fluide sur les appareils bas de gamme [1].
- refs.gallery évoque des textures KTX2, des "request-idle observers" et un fallback `prefers-reduced-motion` [10][tiers, non vérifié].

Sources :
[1] https://www.awwwards.com/igloo-inc-case-study.html
[2] https://www.awwwards.com/sites/igloo-inc
[3] https://x.com/abeto_co/status/1900152588768579701?lang=en
[4] https://www.awwwards.com/sites/igloo-inc (mention Honors Business & Services, juillet 2024)
[5] https://www.webgpu.com/showcase/igloo-inc-procedural-crystals/
[6] https://colorlib.com/wp/animation-websites/
[7] https://www.awwwards.com/igloo-inc-case-study.html et https://www.webgpu.com/showcase/igloo-inc-procedural-crystals/ (extraits combinés)
[8] https://www.tiktok.com/discover/igloo-website
[9] https://www.awwwards.com/igloo-inc-case-study.html (sections son et particules)
[10] https://refs.gallery/projects/igloo-inc
Autres : https://discourse.threejs.org/t/landing-site-igloo-inc/67249, https://loadmo.re/posts/igloo-inc

---

## 2. Lusion (lusion.co) : Oryzo AI, My Little Storybook, sites du studio

### Oryzo AI (oryzo.ai, 2026)

**Concept et prix**
- Campagne satirique auto-initiée : un dessous de verre en liège lancé avec tout le sérieux d'un produit premium de l'ère IA [1][2].
- Awwwards SOTD, tags #storytelling #transitions #GSAP. Décrit comme "a cinematic product story that turns an ordinary cork coaster into an immersive digital experience" [3].
- Site of the Month avril 2026 et Developer Award selon Utsubo [4][tiers].

**Technique**
- Le produit est rendu en temps réel dans Three.js/WebGL, avec "inertie et poids" [5][tiers].
- Un miroir GitHub non officiel du front liste : objets de bureau en WebGL, physique qui réagit au pointeur, et animations pilotées par le scroll de la main, du coaster, de la table et de la caméra [6][tiers].
- Autre gag : le "modèle" ORYZO-1 est publié en open weight… au format OBJ [7].

**Caméra**
- Le scroll déplace la caméra en profondeur (axe Z) au lieu de faire glisser des calques 2D, avec une inertie qui imite la physique [4][tiers].
- FOV et longueur : non documentés.

**Composition**
- Un **objet unique central** (le coaster).
- Une analyse tierce note que le modèle 3D se redimensionne et se repositionne pour devenir un élément fonctionnel d'une mise en page UI plate [5][8][tiers ; attribution exacte entre ces deux pages non vérifiée].

**Non documentés** : palette, post-process, son.

### My Little Storybook (2021-2022)
- Histoire interactive en Three.js : une famille d'oiseaux traverse une rivière. C'est une "Lusion Monthly Experiment" (défi interne mensuel) [9][10].
- Équipe de 3 personnes. Webby Award 2022 "Best Visual Design – Aesthetic" [10][11].
- Mélange de WebGL, d'environnements 3D faits main et d'animation illustrée [12] :
  - modèles 3D : oiseaux, rivière, terrain, plantes, rochers, poissons ;
  - animation 2D sous Procreate ;
  - UI sous Figma [10].
- Inspiration : l'anime japonais [10].
- Caméra, transitions, son : non documentés (étude de cas Medium tronquée).

### Sites du studio
- **Site 2019** (SOTM mai 2019) :
  - environ un an de travail ; pipeline Houdini [13] ;
  - effet de distorsion temps réel pour environ 220 KB gzippés de données ArrayBuffer [13] ;
  - simulation de tissu précalculée pour 3 directions de course et stockée dans **2 PNG** (positions et normales). C'est de la vertex animation texture (VAT), lue frame par frame au runtime [13] ;
  - "WebGL scroll navigation" citée parmi les éléments marquants [13].
- **Lusion v3** (2023) :
  - Site of the Year 2023 et Developer Award selon le profil Awwwards [14] ;
  - éléments relevés : scroll animation et curseur réactif [15].
- Le studio prototype sous Houdini FX et Cinema 4D avant la production temps réel [16].

Sources :
[1] https://lusion.co/projects/oryzo_ai/
[2] https://oryzo.ai/
[3] https://x.com/awwwards/status/2043600792184099160
[4] https://www.utsubo.com/blog/best-threejs-websites-2026
[5] https://www.designrush.com/best-designs/websites/oryzo-website-design
[6] https://github.com/TommyConcept/orzo
[7] https://github.com/lusionltd/ORYZO-1
[8] https://mesh3d.gallery/website/oryzo-ai
[9] https://lusion.co/projects/my_little_story_book/
[10] https://medium.com/@PaulineStich/case-study-my-little-storybook-6f4293db9aba
[11] https://lusion.co/projects/my_little_story_book/ (Webby)
[12] https://tympanus.net/codrops/2026/04/13/lusion-where-digital-craft-meets-ambitious-experimentation/
[13] https://www.awwwards.com/case-study-for-lusion-by-lusion-winner-of-site-of-the-month-may.html
[14] https://www.awwwards.com/lusion/
[15] https://www.awwwards.com/inspiration/home-page-lusion-v3
[16] https://medium.com/lusion-ltd/from-concept-prototyping-to-production-in-a-creative-studio-f2083e96c4b9

---

## 3. Apple : pages produit (AirPods Pro, iPhone, Vision Pro)

### AirPods Pro (hero "lightpass", 2019)

**Technique**
- **Séquence d'images dessinée dans un `<canvas>`**, synchronisée au scroll, sans WebGL [1].
- L'effet consiste en une lumière qui glisse sur le produit : "shifting light effect" [1].
- Les frames sont des JPG numérotés sur 4 chiffres (`0001.jpg`…) [1].

**Chiffres repris des démos**
- `frameCount = 148` (frames 1 à 147) dans le code de l'article ; 147 dans la variante GreenSock [2][3].
- Canvas de **1158 × 770 px** [4][tiers : démos CodePen qui pointent vers les assets d'apple.com].

**Mécanique**
- `body` très haut, canvas `position: fixed` centré [2].
- Index de frame = fraction de scroll × nombre de frames, redessin dans `requestAnimationFrame`, préchargement des images [1].
- Variante GSAP : tween d'un index de frame, avec `scrub: 0.5` pour lisser [3].
- Un commentaire de l'article note que la balise `<video>` ne peut pas profiter de `requestAnimationFrame` pour cet usage [1].

**Caméra et composition**
- Caméra fixe : le produit est seul au centre, et c'est la lumière ou la rotation qui "bouge" dans les frames précalculées [1].

**Poids**
- Une analyse tierce compte 65 PNG pour "l'animation AirPods" et estime environ 1,7 MB en WebP [5][tiers ; page exacte non précisée].

### "Flow" : le codec maison d'Apple (pages iPhone, Watch)
- D'après le reverse-engineering de Graydon Pleasants, les animations liées au scroll d'Apple passent par "Flow" [6] :
  - compression **sans perte, par différences intra-frame** ;
  - une keyframe, puis des frames de diff ;
  - reconstruction dans le navigateur au chargement ;
  - nouvelle approche "quelque part en 2018".
- Manifest `flow_manifest.json` (page watchOS 2, 2015) : `"version":3, "frameCount":179, "blockSize":8` [7].
- Page iPhone 13 [8] :
  - `frameCount` 149, `blockSize` 8 (blocs de 8×8 px comme en compression vidéo) ;
  - `superframeFrequency: 4`, `reversible: true` ;
  - décodage par une fonction JS `_parseFrame` ;
  - aucune balise `<video>` : les fichiers téléchargés sont des "fragments" de diff.

### Vision Pro
- Recréation CSS-Tricks de l'animation "explode" du casque [9] :
  - Apple superpose des **PNG transparents à différentes profondeurs** ;
  - la phase "flip" qui révèle les oculaires est une **vidéo** ;
  - sur petit écran, l'animation est remplacée par une image statique.

### Image-sequence ou vidéo aujourd'hui ?
- Un article affirme qu'Apple est passé au **scrub vidéo** (une seule vidéo compressée, scroll → temps de lecture) et sépare "content motion" et "graphical motion" [10][tiers, non vérifié].
- Aucune source primaire ne le confirme : non documenté officiellement.

**Résolutions**
- Les résolutions des pages iPhone et Vision Pro ne sont pas documentées.

**Encodage d'une vidéo scrubbée (contrainte technique générale)**
- Le navigateur "seek" vers la keyframe la plus proche puis décode en avant : l'espacement des keyframes compte plus que la résolution ou le bitrate [11].
- `-g 1` (chaque frame est une keyframe) donne le scrub le plus fluide, au prix d'un fichier bien plus gros [12][13]. Exemple : `-g 1 -crf 20 scale=960:-1` [13].
- Firefox aurait besoin d'une keyframe toutes les 2 frames, contre 5 pour Chrome, Edge et Safari [14][tiers, anecdotique].
- Le serveur doit gérer les requêtes HTTP Range [15].

Sources :
[1] https://css-tricks.com/lets-make-one-of-those-fancy-scrolling-animations-used-on-apple-product-pages/
[2] https://github.com/xiaotiandada/blog/issues/126
[3] https://codepen.io/GreenSock/pen/ZEqxKyb et https://gsap.com/community/forums/topic/25188-airpods-image-sequence-animation-using-scrolltrigger/
[4] https://codepen.io/j-v-w/pen/ZEbGzyv
[5] https://geyer.dev/blog/css-image-sequence-animations/
[6] https://graydonpleasants.com/posts/flow-apples-secret-weapon/
[7] https://github.com/joykuang/applechina/blob/master/media/us/watchos-2-preview/2015/c60ca33d_d6df_46df_86fd_0dee4b507f3b/watch-os-preview/timelapse-macklake/large/flow/flow_manifest.json
[8] https://dev.to/tetra2000/compression-algorithm-for-iphone-13s-product-page-3gde (miroir de https://medium.com/@TETRA2000/compression-algorithm-for-iphone-13s-product-page-6e2ba76e6957)
[9] https://css-tricks.com/recreating-apples-vision-pro-animation-in-css/
[10] https://www.brad-holmes.co.uk/web-performance-ux/why-most-scroll-animations-miss-what-apple-gets-right/
[11] https://dev.to/nikhilswain/scroll-scrubbed-video-that-stays-smooth-with-any-video-file-5d8k
[12] https://gist.github.com/jeffpamer/f3134c5145238d0fd4752221b2d75eb7
[13] https://gist.github.com/ksachikonye/8c01488f0841f440d809a14a7c59335f
[14] https://medium.com/@chrislhow/scroll-to-scrub-videos-4664c29b4404
[15] https://github.com/nicolaslekai/peak-media

---

## 4. Active Theory (activetheory.net)

**Moteur maison "Hydra"**
- Développé depuis 2012 pour produire des projets animés multi-plateformes [1][2].
- Le portfolio actuel tourne dessus : particules temps réel, navigation par chat IA, environnements 3D [3].
- LCP d'environ 1,3 s sur desktop, attribué aux meshes compressés en Draco et aux vidéos chargées à la demande [3][tiers, non vérifié].

**v4 (Site of the Year selon un hall of fame Awwwards 2020 [5][tiers, miroir])** [4][5]
- Astuces d'éclairage peu coûteuses en GPU : brouillard volumétrique, diffusion de lumière.
- Géométrie calculée dans des WebWorkers pour accélérer l'arrivée sur le site.

**v5 (2019)**
- 3 environnements prévus, **8 construits**. Le but : jouer sur les transitions entre scènes et éviter la répétition [6].
- Décors : Venice Beach, canaux d'Amsterdam, environnements de projets passés [6].
- La barre espace fait passer d'un environnement à l'autre. Un grand écran dans chaque environnement diffuse les vidéos du portfolio [7].
- Navigation : déplacement temps réel dans les environnements.

**Fiomet (étude de cas technique)** [8][9]
- Sections 3D plein écran, une par argument marketing.
- Entrées multiples : scroll, clavier, puces, scrollbar native, drag. Les transitions sont **interruptibles**.
- **Transitions** :
  - un "portail" depuis la landing, qui fait entrer dans l'univers de chaque produit ;
  - une transition **latérale** qui relie les sections sombres et claires sans coupe franche.
- Le cadre et la **caméra réagissent à la vitesse de scroll** et à la position, ce qui donne une sensation physique.
- Titres en WebGL, avec deux textures par police, dont une **MSDF** qui définit la forme des lettres.

**adidas CHILE20 (2020, SOTM)** [10][11][12]
- **3 mondes pilotés au scroll**, on peut sauter de l'un à l'autre :
  - noir et blanc granuleux, graffiti, **grain film** ;
  - rue de l'ère pandémie, skateboards ;
  - néon [10][tiers].
- Les vêtements tournent au centre de chaque scène (**objet central**) [10].
- Plusieurs scènes 3D sont rendues en même temps pendant le scroll, le drag ou les passages entre mondes, avec des passes de réflexion [11].
- Optimisation : modèle de plus de 500 000 polygones avec des piles de textures 4K, réduit à des meshes mobiles avec deux textures 2K et des normal maps bakées depuis le high-poly [10][11].
- Mouvements de caméra : non documentés.

**Neve**
- Un timer de rendu **désactive le post-processing** si le budget de frame est dépassé [13].

Voir aussi Prometheus Fuels en §7a (Active Theory).

Sources :
[1] https://medium.com/active-theory/the-story-of-technology-built-at-active-theory-5d17ae0e3fb4
[2] https://www.webbyawards.com/crafted-with-code/active-theory/
[3] https://www.webgpu.com/showcase/active-theory-portfolio/
[4] https://thefwa.com/article/insights-active-theory-v4
[5] https://awwwards-2020.tubikstudio.com/hall-of-fame
[6] https://www.webbyawards.com/crafted-with-code/active-theory/
[7] https://www.commarts.com/webpicks/active-theory-1
[8] https://medium.com/active-theory/fiomet-case-study-9a0180268423
[9] https://www.commarts.com/webpicks/fiomet
[10] https://www.webgpu.com/showcase/chile20-active-theory-webgl-adidas-originals/
[11] https://medium.com/active-theory/adidas-chile20-4744a75f5968
[12] https://www.webbyawards.com/crafted-with-code/adidas-chile20/
[13] https://medium.com/active-theory/neve-webgl-and-vr-d42a25856d67

---

## 5. Bruno Simon (bruno-simon.com) et Three.js Journey

> Le portfolio n'est pas piloté par le scroll : c'est un jeu à conduire. Il sert de contre-modèle, où l'interaction et la physique créent le "wow".

**Portfolio 2019 (Awwwards SOTM novembre)** [1][2][3]
- Three.js pour le rendu, Cannon.js pour la physique.
- Collisions simplifiées en primitives (cubes, sphères, cylindres).
- Une chute de framerate venait des objets qui ne s'"endormaient" pas par défaut.
- Mobile : flou supprimé, pixel ratio plafonné, `matrixAutoUpdate` désactivé.
- Ombres statiques bakées dans Blender en PNG-8, modèles en glTF + Draco [4].

**Folio 2025** [5][6][7][8]
- Three.js avec TSL : WebGPU si disponible, sinon WebGL.
- Physique **Rapier**, audio **Howler.js**.
- 4 schémas d'entrée (clavier, souris, tactile, manette).
- Monde entièrement construit dans Blender, piloté par des conventions de nommage : les noms d'objets deviennent des corps physiques, et des Empties servent de colliders, de points de respawn et de limites de zones.
- Environ 78 400 brins d'herbe, un triangle chacun.
- Feuillage : plans orientés vers la caméra, feuilles en texture SDF.
- Code MIT avec les fichiers Blender. 15 devlogs vidéo.

**Caméra**
- Vue "isométrique en surplomb" selon un commentateur HN [9][tiers].
- FOV : non documenté.

**Son** : oui, via Howler.js [5].

**Three.js Journey, leçon "Scroll based animation"** [10][11]
- Three.js sert de fond à une page HTML classique ; OrbitControls est retiré.
- `objectsDistance = 4`, objets espacés sur Y.
- Dans `tick()` : `camera.position.y = -scrollY / sizes.height * objectsDistance`. La caméra fait donc un **travelling vertical**, à raison d'une "section" par hauteur d'écran.
- Parallaxe au curseur appliquée à un groupe parent de la caméra.

Sources :
[1] https://medium.com/@bruno_simon/bruno-simon-portfolio-case-study-960402cc259b
[2] https://thefwa.com/cases/bruno-simon-portfolio
[3] https://www.awwwards.com/bruno-simon-portfolio-wins-site-of-the-month-november.html
[4] https://medium.com/@bruno_simon/bruno-simon-portfolio-case-study-960402cc259b (baking et Draco)
[5] https://www.webgamedev.com/newsletter/025
[6] https://x.com/bruno_simon/status/1851977267611644187
[7] https://www.awwwards.com/brunos-portfolio-case-study.html
[8] https://github.com/brunosimon
[9] https://news.ycombinator.com/item?id=46206531
[10] https://threejs-journey.com/lessons/scroll-based-animation
[11] https://tympanus.net/codrops/2022/01/05/crafting-scroll-based-animations-in-three-js/

---

## 6. Abeto : Messenger (messenger.abeto.co, 2025)

> Ce n'est pas un site piloté par le scroll, mais un jeu multijoueur sur une mini-planète. Même studio qu'Igloo.

**Prix et équipe**
- **Developer Site of the Year 2025** sur Awwwards (54 votes) [1].
- Développeurs : Vicente Lucendo et Michael Sungaila [2].
- 2 131 points et 338 commentaires sur Hacker News [3].

**Stack** (sources tierces)
- WebGL et Three.js, sans Unity ni Godot [4].
- three-mesh-bvh pour les collisions sur la planète courbe [4].
- Modèles faits sous Houdini et Blender, textures Substance [4].
- Multijoueur en WebSocket sur Node.js [4].

**Concept**
- Planète si petite qu'on en fait le tour en environ 30 s. On livre du courrier [5].
- On communique avec les autres joueurs par emojis [3].

**Performances**
- Environ **5,7 MB** au chargement initial, 17,5 MB au maximum [4].
- Bande-son streamée, non incluse dans le bundle [4].

**Non documentés officiellement** : caméra (un clone non officiel utilise une caméra alignée sur la normale de surface [6]), palette, post-process.

Sources :
[1] https://www.awwwards.com/annual-awards/winners
[2] https://en.wikipedia.org/wiki/Messenger_(video_game)
[3] https://fresh-hacker-news.deno.dev/item?id=45396441
[4] https://x.com/zeuuss_01/status/2066949488682639703 et https://medium.com/@sujaltalreja04/messenger-by-abeto-didnt-change-three-js-it-changed-how-we-think-about-building-for-the-web-3349d966748f
[5] https://gamingph.com/2025/09/messenger-a-free-short-game-where-a-kid-delivers-messages-in-a-small-round-world-playable-in-browser/
[6] https://github.com/Glowin/messager

---

## 7. Studios : études de cas techniques

### 7a. Prometheus Fuels, par Active Theory (2021)

**Prix**
- Awwwards SOTD le 4 mai 2021, puis SOTM mai 2021 [1].
- Collection Awwwards : tags "Site of the Year 2021" et Developer Award [2].
- Un miroir Wikipédia crédite "Resn / Bader Rutter" pour ce SOTY 2021 [3]. C'est en contradiction avec l'article Awwwards "Prometheus Fuels by Active Theory" [1] et la page de l'agence [4].

**Récit et direction artistique**
- Monde zéro carbone net, esthétique **rétro-futuriste** [1].
- 2 chapitres : "The Birth of a New Era" et "A World of Possibilities" [1].
- Récit **linéaire au scroll**, planifié sur une série de **storyboards illustrés** [5].
- Objectif : garder la sensation d'une page qui défile verticalement tout en exploitant le moteur 3D [5].

**Technique**
- Éléments illustrés et photographiques plaqués sur des meshes 3D (2,5D), pour permettre de vrais mouvements de caméra 3D [5].

**Caméra**
- Système dédié qui laisse aux artistes le contrôle total du "camera flow", sans réexporter une spline à chaque retouche [5].
- **Chaque scène a une caméra de début et une caméra de fin.** Les paramètres sont exposés et modifiables en temps réel [5].
- Le scroll interpole donc entre deux caméras clés par plan.

**Transitions**
- Une seule scène est rendue à la fois. Pendant une transition, le moteur fait du "ping-pong" entre les deux scènes [5].

**Performances**
- Les effets secondaires (texture de route qui défile) sont limités à **12 fps**, la caméra principale reste à 60 fps. Les auteurs précisent que ce choix doit rester discret [5].

Sources :
[1] https://www.awwwards.com/prometheus-by-active-theory-wins-site-of-the-month-may-2021.html
[2] https://www.awwwards.com/mireia_ortega/collections/interactive-experience/
[3] https://wiki.neonvagabond.xyz/content/wikipedia_en_all_maxi_2024-01/A/Awwwards
[4] https://activetheory.net/work/prometheus
[5] https://medium.com/active-theory/prometheus-2d3c05b88ec0

### 7b. Dogstudio (dogstudio.co)

**Home : le chien 3D**
- Modèle glTF compressé en Draco [1][tiers].
- La couleur et le décor du chien changent derrière chaque titre de projet [1][tiers].
- Stack : WordPress, three.js, GSAP, Highway.js [1][tiers].
- Selon un développeur du projet [2] :
  - la scène est partie d'une expérience de week-end basée sur les matcaps / litsphere ;
  - l'influence de la normal map diminue avec la distance (calcul par vertex dans le shader) pour réduire l'aliasing ;
  - la transition de matcap dépend de la distance du modèle à un point fixe.

**Panasonic** [3]
- Plus de 30 produits répartis dans **4 pièces 3D**.
- **Caméra sur un chemin dont l'orientation change en permanence**, pour toujours montrer les produits à venir. Navigation au scroll et au clic.
- Défi principal : des assets très détaillés avec un polycount assez bas pour garder un bon framerate.

**Adobe "Taking Shape"**
- Pièces construites de zéro ; une fonctionnalité bonus ajoutée tard, avec peu de tests mobiles [4].

Sources :
[1] https://colorlib.com/wp/animation-websites/
[2] https://threadreaderapp.com/thread/1113161040265666560.html
[3] https://dogstudio.co/cases/panasonic/
[4] https://dogstudio.co/cases/adobe-taking-shape/

### 7c. Immersive Garden (immersive-g.com), Agency of the Year Awwwards 2025 [1]

**Site du studio (étude de cas Awwwards, mars 2025)** [2][3]
- Défi : obtenir un réalisme élevé tout en limitant la charge GPU et la mémoire.
- Pipeline d'assets :
  - textures compressées côté serveur, avec channel packing ;
  - exports automatisés avec gltf-transform et des scripts JS et Blender maison.
- Stack : three.js, GSAP, **Lenis**, Vue/Nuxt, Strapi, Vercel. Assets faits sous Blender, Houdini, ZBrush.
- Bas-relief 3D, et chiffres romains en 3D associés à chaque section du menu.
- "Plus de temps passé à retirer qu'à ajouter" : le minimalisme est assumé.

**David Whyte Experience (SOTD décembre 2024)** [4][5]
- Aquarelles de Matthew Phinn.
- **Environnement 3D et mouvement de caméra réglés d'abord dans Blender**, puis recréés en Three.js, principalement avec des shaders custom.
- Les peintures sont révélées par une simulation générative de gouttes d'eau, couche par couche.
- Paysages sonores sur mesure.

**Hatom (SOTD novembre 2024 ; SOTM décembre 2024 selon une autre page Awwwards)** [6][7][8]
- **5 chapitres** : un griffon éclot, s'arme, puis s'étend sur des planètes.
- Ouverture : un **œuf lumineux flottant dans le vide**, qui se fissure au scroll avant l'apparition du griffon.
- Stack : Three.js, Vue/Nuxt, GSAP et Lenis.
- Preloader progressif, pendant lequel un **appui long** (réglé différemment sur mobile et desktop) occupe l'utilisateur.
- Sound design de Ben Lukas Boysen.

**Cartier Watches & Wonders 2025 (CSSDA WOTD, 16 juillet 2025)** [9][10]
- **6 alcôves 3D flottantes**, une montre par alcôve.
- Horizons qui dérivent, eau, surfaces miroirs.
- Stack : Three.js, Blender, GSAP et Lenis, avec une bande-son en Web Audio.

**Audemars Piguet RD**
- Visite scrollable de 5 prototypes de montres, avec une caméra qui sait "rester immobile" [11][tiers].

**Artisans d'Idées**
- Parcours Three.js **horizontal**, presque entièrement dans l'ombre.
- **Audio couplé à l'état de la caméra** plutôt qu'à une horloge [12][tiers].

Sources :
[1] https://www.awwwards.com/annual-awards/winners
[2] https://www.awwwards.com/case-study-immersive-gardens-new-website.html
[3] https://www.commarts.com/webpicks/immersive-garden
[4] https://www.awwwards.com/case-study-david-whyte-experience-by-immersive-garden.html
[5] https://immersive-g.com/projects/david-whyte-experience/
[6] https://www.webgpu.com/showcase/hatom-griffin-mythology-webgl/
[7] https://immersive-g.com/projects/hatom/
[8] https://www.awwwards.com/awwwards/collections/webgl/ ou https://www.awwwards.com/du-haihang/collections/webgl-animations/ (page exacte non vérifiée)
[9] https://www.webgpu.com/showcase/cartier-watches-and-wonders-immersive-garden/
[10] https://www.cssdesignawards.com/sites/cartier-watches-and-wonders-2025/47763/
[11] https://www.webgpu.com/showcase/extraordinary-lab-audemars-piguet-webgl/
[12] https://www.webgpu.com/tag/scroll-animation/

### 7d. Resn : KPR (Site of the Year Awwwards, SOTM décembre 2022)

**Prix**
- Premier projet Web3 à remporter le prix principal [1][2].

**Récit et composition**
- Personnages 3D combinés à du design 2D [3].
- Au scroll, on traverse des **"tableaux"** au style concept art : The Keep, The Factions, The World [3].

**Technique et transitions**
- **Stencil buffer** : une scène 3D en masque une autre, à la manière d'un portail [3].
- Des scènes 3D et des calques de texte qui bougent à des vitesses différentes créent une parallaxe [4][tiers].

**Interaction**
- Un **clic maintenu** révèle une seconde couche de contenu sur les habitants de New Eden [3].

**Non documentés** : son, post-process, caméra.

Sources :
[1] https://www.einpresswire.com/article/620020684/resn-s-kpr-named-awwwards-site-of-the-year?code=3qxrdtb_IPJjYgzo
[2] https://www.mad-daily.com/resn-wins-again-at-awwwards/
[3] https://www.awwwards.com/kpr-by-resn-wins-sotm.html
[4] https://www.scribd.com/document/939945000/KPRverse-Kprverse-com-Front-End-Analysis

### 7e. 14islands : r3f-scroll-rig [1][2]
- **Un seul canvas global**, persistant entre les pages. La raison : le nombre de contextes WebGL est limité et les ressources ne se partagent pas entre contextes.
- Des éléments DOM servent de **proxies** : `ScrollScene`, `ViewportScrollScene` et `useTracker()` recalent les meshes sur leur position au scroll.
- Lenis anime le scroll natif pour que DOM et WebGL restent alignés.
- Approche : **progressive enhancement**. HTML et CSS sémantiques d'abord, WebGL ajouté par-dessus.
- Tutoriel Codrops associé : réfraction de lentille [3].
- Clients cités : Cartier 365, Lynxeye, Axolot Games [1].

Sources :
[1] https://github.com/14islands/r3f-scroll-rig
[2] https://github.com/darkroomengineering/lenis/blob/main/README.md
[3] https://tympanus.net/codrops/2023/10/10/progressively-enhanced-webgl-lens-refraction/

### 7f. Unseen Studio : Crosswire [1][2]
- Paysage 3D qui représente l'environnement numérique du client, pour rendre un service complexe lisible.
- Grille 3D dérivée des formes du logo.
- Un add-on Blender maison exporte la scène en nuage de points ; chaque modèle est ensuite placé en **instanced mesh**.
- **Matériau métallique qui reflète l'environnement à mesure qu'on scrolle**, avec des contournements parce que les réflexions et ombres temps réel coûtent cher.
- Analyse tierce des sites Unseen : Lenis ou ASScroll synchronisent le scroll avec la scène, et les transitions passent par du post-processing [3][tiers].
- Caméra liée au scroll sur la page projets : question ouverte sur le forum Three.js, sans réponse confirmée [4].

Sources :
[1] https://tympanus.net/codrops/2023/04/04/case-study-crosswire/
[2] https://tympanus.net/codrops/2023/02/13/recreating-crosswires-reflective-grid-with-three-js/
[3] https://chipsa.design/publications/legendy-veb-dizaina-texniceskii-razbor-rabot-studii-unseen
[4] https://discourse.threejs.org/t/how-is-the-scrolling-animation-implemented-on-the-unseen-studio-website/87789

### 7g. Locomotive (Montréal)
- Auteurs de Locomotive Scroll. La **v5 est une surcouche fine de Lenis** [1][2].
- Le studio se présente comme 7 fois Agency of the Year Awwwards, de 2018 à 2024 [3].
- Étude de cas WebGL cinématique : non documentée.

Sources :
[1] https://scroll.locomotive.ca/
[2] https://cdn.jsdelivr.net/npm/locomotive-scroll@5.0.1/README.md
[3] https://locomotive.ca/llms.txt

---

## 8. Tutoriels Codrops et briques techniques du "cinematic scroll"

**Codrops 2022 : "Crafting Scroll Based Animations in Three.js"** [1]
- Version écrite de la leçon Three.js Journey.
- Caméra en travelling Y proportionnel à `scrollY`, parallaxe sur un groupe parent de la caméra (voir §5).

**Codrops 2023 : caméra en fly-through au scroll avec Theatre.js + R3F (Andrew Prifer)** [2][3]
- Environ 50 lignes ; stack Theatre.js, R3F, Drei, Vite.
- `ScrollControls` et `useScroll` de Drei positionnent la tête de lecture de la séquence Theatre.
- La caméra suit donc des **keyframes** placées dans un éditeur de timeline.

**Codrops nov. 2025 : "How to Build Cinematic 3D Scroll Experiences with GSAP" (Joseph Santamaria)** [4][5]
- 2 démos :
  - un cylindre en shader avec des particules réactives ;
  - une scène 3D avec **caméras en mouvement** et typographie animée.
- ScrollSmoother et ScrollTrigger, courbes d'easing custom.

**Codrops avril 2026 : "More Than a Portfolio: Building a Scroll-Driven 3D World…" (Santamaria)** [6]
- **Chaque section est sa propre scène.** La progression du scroll pilote la caméra, les objets et le timing des révélations.
- Entrées gérées par GSAP Observer en plus de ScrollTrigger, plutôt que par les événements scroll bruts.
- Optimisation : Draco et frustum culling dynamique, plutôt que plusieurs niveaux de LOD.
- 3 mois de travail.

**Codrops juillet 2026 : galerie pilotée au scroll sur un chemin caméra Blender (Gaspard Hedde)** [7][8]
- Courbe de Bézier dessinée dans Blender, exportée en JSON par un script Python.
- Remap des axes : X Blender reste X, Z Blender devient Y, Y Blender devient −Z.
- Reconstruction en `CatmullRomCurve3` ; 500 plans d'images répartis le long de la courbe avec des offsets aléatoires ; **fog** pour la profondeur.
- GSAP **Observer** (molette, tactile, pointeur) et `gsap.quickTo()` pour faire glisser la caméra sur la courbe.
- Les plans proches grossissent jusqu'à ×14 selon une fonction de proximité cubique.

**Codrops mars 2026 : galerie réactive à la vélocité**
- L'entrée de scroll est lissée par un **lerp** avant de piloter la profondeur caméra [9].

**Drei `ScrollControls`** [10][11]
- `pages` : 1 page = 1 hauteur d'écran.
- `damping` : facteur de lissage (exemple : `pages={3} damping={0.25}`).
- `useScroll().offset` va de 0 à 1 ; les helpers `range`, `curve` et `visible` découpent le scroll en plages.
- Pattern courant : seek d'une timeline GSAP à `offset × duration` dans `useFrame`.
- Piège : OrbitControls capture la molette.

**Lenis + ScrollTrigger (recette officielle)** [12]
- `lenis.on('scroll', ScrollTrigger.update)`
- `gsap.ticker.add(t => lenis.raf(t*1000))`
- `gsap.ticker.lagSmoothing(0)`

**Vidéo scrubbée** : encodage tout-keyframes, voir §3.

Sources :
[1] https://tympanus.net/codrops/2022/01/05/crafting-scroll-based-animations-in-three-js/
[2] https://tympanus.net/codrops/2023/02/14/animate-a-camera-fly-through-on-scroll-using-theatre-js-and-react-three-fiber/
[3] https://github.com/AndrewPrifer/CodropsCameraFlyThroughTutorial
[4] https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/
[5] https://github.com/JosephASG/codrops-cinematic-scroll-animations
[6] https://tympanus.net/codrops/2026/04/28/more-than-a-portfolio-building-a-scroll-driven-3d-world-with-something-to-say/
[7] https://tympanus.net/codrops/2026/07/07/building-a-scroll-driven-3d-gallery-using-a-blender-camera-path-with-three-js-and-gsap/
[8] https://github.com/gaspoorf/curve-gallery
[9] https://tympanus.net/codrops/2026/03/09/building-a-scroll-reactive-3d-gallery-with-three-js-velocity-and-mood-based-backgrounds/
[10] https://drei.docs.pmnd.rs/controls/scroll-controls
[11] https://dev.to/wawasensei/scroll-animations-with-react-three-fiber-and-gsap-273j
[12] https://docsearch.algolia.com/mcp/docs/repo/darkroomengineering/lenis

---

## 9. Autres sites primés du genre

### Lando Norris, par OFF+BRAND (Awwwards Site of the Year 2025)

**Prix**
- SOTY 2025 avec 43 votes, et Users' Choice avec 596 votes [1].

**Stack**
- Webflow, GSAP, ScrollTrigger, SplitText, three.js, Rive, Lenis, Taxi.js [2][tiers].

**Composition et palette**
- **Casque 3D qui tourne** (objet central), typographie lime en gras, "scroll-driven cinematics" [3].
- Côté OFF+BRAND : "cinematic scrolling", animations inspirées de la vitesse, lazy-loading [4].

**Performances**
- Les miroirs non officiels montrent du Draco, des transcodeurs Basis Universal et des GLB de casques [5][tiers].

**Non documentés** : caméra et FOV.

Sources :
[1] https://www.awwwards.com/annual-awards/winners
[2] https://colorlib.com/wp/animation-websites/
[3] https://www.webgpu.com/showcase/mclaren-f1-driver-lando-norris-official-website/
[4] https://www.itsoffbrand.com/our-work/lando-norris
[5] https://github.com/nachitzaid/lando-noris

### Récapitulatif des prix majeurs cités

| Site | Studio | Prix | Source |
|---|---|---|---|
| Prometheus Fuels | Active Theory | SOTY 2021 + Developer | §7a |
| KPR | Resn | SOTY (édition 2022) | §7d |
| Lusion v3 | Lusion | SOTY 2023 + Developer | §2 |
| Igloo Inc | Abeto | SOTY + Developer SOTY 2024 | §1 |
| Lando Norris | OFF+BRAND | SOTY 2025 | ci-dessus |
| Messenger | Abeto | Developer SOTY 2025 | §6 |
| Immersive Garden | — | Agency of the Year 2025 | §7c |

---

## 10. Patterns transverses

Les comptes portent uniquement sur les sites et projets ci-dessus pour lesquels une source le documente. Ce sont des minima.

1. **WebGL temps réel avec Three.js comme socle : environ 12 sites ou studios.**
   - Concernés : Igloo, Oryzo, My Little Storybook, Bruno Simon, Messenger, Immersive Garden (site, David Whyte, Hatom, Cartier), Dogstudio, Lando Norris, Unseen, tutoriels Codrops.
   - Exceptions : Active Theory (moteur maison Hydra) et Apple (pas de WebGL : séquence d'images sur canvas, codec "Flow", vidéo).

2. **Le scroll est une tête de lecture, pas un déclencheur : environ 10 cas.**
   - Une valeur normalisée de 0 à 1 seek une timeline, un chemin ou un index de frame :
     - Apple (index de frame) ;
     - Drei `useScroll().offset` ;
     - Theatre.js (`sequence position`) ;
     - Codrops (courbe Blender, `quickTo`) ;
     - Three.js Journey (`scrollY → camera.y`) ;
     - Igloo (scroll → caméra et état des objets) ;
     - Prometheus (interpolation entre caméras début et fin) ;
     - Santamaria (progression → caméra, objets, révélations).

3. **Caméra auteurisée hors ligne (chemin, spline ou keyframes), jamais libre : environ 8 cas.**
   - Concernés : Prometheus (caméra de début et de fin par scène), Dogstudio Panasonic (chemin à orientation changeante), David Whyte (caméra posée dans Blender), Codrops Blender path, Theatre.js, Igloo (previs du trajet), Oryzo (dolly en Z), Three.js Journey (travelling vertical).
   - Mouvements dominants : **dolly ou fly-through vers l'avant**, et travelling. L'orbite libre est exclue : OrbitControls est retiré explicitement dans Three.js Journey et Drei.

4. **Lissage et inertie entre le scroll et la caméra : au moins 9 cas.**
   - Lenis, chez au moins 5 studios et plusieurs projets : Immersive Garden ×3, Lando Norris, 14islands, Locomotive v5, Unseen.
   - Autres formes : Drei `damping`, GSAP `scrub: 0.5`, `quickTo`, lerp (Codrops 2026), "inertie et poids" d'Oryzo, caméra sensible à la vitesse de scroll (Fiomet).

5. **Peu de plans, nettement séparés : 2 à 8 chapitres, environ 9 cas.**
   - Igloo : 3 sections. Prometheus : 2 chapitres. KPR : 3 tableaux. CHILE20 : 3 mondes. Dogstudio Panasonic : 4 pièces. Hatom : 5 chapitres. Cartier : 6 alcôves. Active Theory v5 : 8 environnements. Fiomet : sections plein écran.
   - Un plan correspond souvent à un objet ou à un produit.

6. **Transitions qui sont elles-mêmes un effet : environ 7 cas.**
   - Igloo : aberration chromatique + displacement + givre.
   - Fiomet : portail + transition latérale sombre/clair.
   - KPR : masque au stencil buffer, façon portail.
   - Prometheus : ping-pong entre deux scènes.
   - CHILE20 : plusieurs scènes rendues en même temps.
   - Hatom : l'œuf qui se fissure.
   - Active Theory v5 : 8 scènes pour "jouer sur les transitions".

7. **Sujet central unique, beaucoup de vide autour : environ 9 cas.**
   - Concernés : Apple (produit), Oryzo (coaster), Lando (casque), Dogstudio (chien), Hatom (œuf ou griffon "dans le vide"), CHILE20 (vêtement qui tourne au centre), Igloo (un bloc de glace par projet), Cartier (une montre par alcôve), Immersive Garden ("retirer plutôt qu'ajouter").

8. **Son conçu sur mesure et synchronisé au mouvement : environ 7 cas.**
   - Igloo (calé sur les particules), Hatom (Ben Lukas Boysen), Cartier (Web Audio), David Whyte (soundscapes), Artisans d'Idées (audio lié à l'état de la caméra), Messenger (bande-son streamée), Bruno Simon (Howler.js).

9. **Pipeline DCC Blender et/ou Houdini, avec du procédural ou du précalcul : environ 9 cas.**
   - Igloo (Houdini + Blender, cristaux procéduraux, VDB), Lusion (Houdini, VAT dans des PNG), Messenger (Houdini + Blender), Bruno Simon (monde Blender piloté par des conventions de nommage), Immersive Garden (Blender, Houdini, ZBrush, scripts d'export), Unseen (add-on Blender vers nuage de points), Codrops (chemin caméra Blender), Dogstudio (matcaps), Prometheus (illustrations plaquées sur meshes).

10. **Obsession du poids et du framerate : environ 10 cas.**
    - Compression : Draco, KTX2/Basis, gltf-transform, compression serveur des textures.
    - Budgets : Messenger 5,7 MB ; données VDB d'Igloo "plus légères qu'une image" ; distorsion Lusion à 220 KB.
    - Effets secondaires à 12 fps (Prometheus) ; post-process coupé si le budget est dépassé (Neve).
    - Baking : normal maps (CHILE20), ombres (Bruno Simon).
    - Rendu d'une seule scène à la fois (Prometheus) ; instancing (Unseen) ; frustum culling (Santamaria).
    - Preloader progressif occupé par une interaction (Hatom).
    - Pour la vidéo, encodage tout-keyframes.

11. **UI et texte rendus dans le WebGL (SDF/MSDF) pour des glitchs et morphs sans coût DOM : 3 cas.**
    - Igloo (SDF), Fiomet (MSDF), Santamaria (typographie animée).
    - Revers documenté : accessibilité et SEO (Igloo).
    - Approche inverse : le DOM reste la source et le WebGL suit des proxies (14islands).

12. **Palette et post-process : peu documentés, mais une tendance.**
    - Fonds sombres ou "dans le vide" avec un seul accent : Hatom (œuf lumineux), Artisans d'Idées (ombre), CHILE20 (N&B + grain film puis néon), Lando (lime), Igloo (niveaux de gris, source faible), Fiomet (alternance sombre/clair).
    - Post-process cités : aberration chromatique (Igloo), grain film (CHILE20), fog (Codrops, Active Theory v4), flou (Bruno Simon 2019).
    - **Bloom, DOF, tone mapping : non documentés** dans les sources trouvées.
    - **FOV et longueur de scroll en vh : non documentés** pour tous les sites primés.
    - Seuls les tutoriels donnent des ordres de grandeur : 1 page = 1 viewport (Drei), `objectsDistance` 4 par section (Three.js Journey), 4110vh pour un clone Apple (https://codepen.io/flcwl/pen/LYYevVr).
