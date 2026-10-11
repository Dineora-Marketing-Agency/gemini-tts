# Outils de mesure

Scripts utilisés pour le rapport (`../RAPPORT.md`). Dépendances : `ffmpeg`/`ffprobe`, Python 3 + `numpy` + `Pillow`, Node + Playwright (Chromium).

| Script | Rôle |
| --- | --- |
| `probe.py <dossier_videos> <sortie.csv>` | Résolution, fps, durée, codec, débit, audio de chaque vidéo. |
| `analyze.py <video>...` | Une ligne JSON par vidéo : coupes, mouvement caméra, activité, palette (k-means), luminance, remplissage du cadre (grille 3×3), centre visuel, symétrie, couture de boucle. |
| `sheets.py <sortie> <video>...` | Planche contact de 8 images horodatées par vidéo. |
| `prompts_stats.py <dossier_prompts>` | Fréquence des motifs design/motion dans des prompts (polices, glass, blur-in, durées d'animation…). |
| `capture.cjs <url> <sortie> <nom> [s] [settle] [W] [H] [every]` | Enregistre une vidéo d'un scroll molette à vitesse constante. |
| `stepcap.cjs <url> <sortie> <nom> [N] [wait] [W] [H] [selecteur]` | Capture déterministe : N positions de scroll régulières, attente de stabilisation, capture d'écran. |
| `steps_analyze.py <nom>` | Analyse une capture `stepcap` : changements de plan par écran de scroll, caméra par écran, palette, remplissage, planche contact. |
| `scrollsheet.py` | Découpe et planche d'une capture `capture.cjs`. |
| `fps.cjs <url> <W> <H>` | Cadence de rendu, hauteur de scroll, capture de contrôle. |

## Comment lire `analyze.py`

- **Caméra** : flux optique par corrélation de phase sur une grille de patchs (48 px sur une image ramenée à 256 px de large), entre deux images espacées de 8 trames (1/3 s à 24 fps). On ajuste ensuite un modèle de similarité : translation, zoom, rotation.
  - `pan_x` / `tilt_y` en % de largeur par seconde. Négatif = le contenu glisse vers la gauche ou vers le haut.
  - `zoom` en % d'échelle par seconde. Positif = push-in, ou sujet qui grossit.
  - `roll` en °/s.
- **Validation** sur des vidéos synthétiques à mouvement connu, erreur ±5 % :
  - pan −3,13 %/s → −3,18 mesuré ;
  - tilt −2,34 %/s → −2,34 mesuré ;
  - zoom ≈ +2,25 %/s → +2,22 mesuré.
- **Limite** : l'outil mesure le mouvement de l'image. Un sujet qui tourne ou qui grossit ressemble à un mouvement de caméra. Dans le rapport, le type de mouvement caméra a donc été tranché par lecture visuelle des planches.
- **Coupes** : saut d'histogramme couleur + saut de luminance, recoupés avec le filtre `scdet` de ffmpeg. Calibration : une coupe franche donne un score `scdet` d'environ 16, un fondu enchaîné environ 1,3, donc il n'est pas détecté.
- **`loop_seam_ratio`** : écart entre la première et la dernière image, divisé par l'écart médian entre deux images consécutives. ≤ 3 ≈ boucle sans couture.

Rendu WebGL en headless : `--use-angle=swiftshader`. Le rendu logiciel tourne à 11–24 fps. Le Chromium de Playwright ne décode pas le H.264.
