# Showreel · Alessandro Gagliardi

Mon CV en version showreel de motion design :

- Français : **https://pazificateur69.github.io/showreel/**
- English: **https://pazificateur69.github.io/showreel/en/**

Ingénieur cybersécurité et DevSecOps à Lyon. Le site se regarde comme une bande démo : amorce 3-2-1, timecode et barre de lecture, chiffres clés en compteurs, parcours sur une timeline de montage, scène red team / blue team, projets avec aperçus animés, générique de fin, clap de la prochaine scène et fin en éclipse. Le CV est aussi téléchargeable en PDF (FR et EN).

- **Lecture** : faire défiler, ou appuyer sur « Lancer le showreel » (ou Espace) pour une lecture automatique.
- **Table de montage** : la barre de lecture en bas se saisit à la souris ou au doigt pour parcourir le film. Au clavier, J / K / L comme dans un logiciel de montage (arrière, pause, avant ; un nouvel appui accélère jusqu'à ×4), ← → pour passer d'une scène à l'autre, M pour le son, ? pour l'aide.
- **Liens directs** : `#projets`, `#parcours`, `#contact`… ouvrent le showreel directement sur la scène, sans compte à rebours. Le compte à rebours ne se joue qu'une fois par session.
- **Page 404** : « Média hors ligne ». Le 404 est fait de points qui jaillissent de la tête de lecture, fuient la souris et se dérèglent par moments ; survoler une scène de la timeline la prévisualise, cliquer y emmène. Bilingue (FR sous `/showreel/`, EN sous `/showreel/en/` ou pour un navigateur non francophone).
- **Accessibilité** : avec « réduire les animations » activé dans le système, la page s'affiche en version statique complète.
- **Version rapide** : `?rapide` (ou `?quick` en anglais) affiche le CV en défilement simple, sans animation.
- **Machines modestes** : si l'ordinateur n'arrive pas à suivre, le site passe tout seul en mode allégé (défilement natif, titres fixes). On peut le forcer avec `?lite`.

## Technique

Pages statiques, sans build côté site.

- [GSAP](https://gsap.com) 3.13 + ScrollTrigger (séquences pilotées par le défilement), [Lenis](https://lenis.darkroom.engineering) (défilement fluide), chargés depuis cdnjs et jsDelivr avec contrôle d'intégrité (SRI).
- Polices Google Fonts : Anybody (axe de largeur animé), Instrument Sans, Martian Mono.
- Aperçus de projets dessinés en Canvas 2D, plus les vrais écrans (démos SVG des dépôts ExploitSpec et NightOwl, capture de curs3d.fr dans `img/`). Icônes Phosphor.
- Calque 3D en WebGL pur (sans bibliothèque) : 15 000 points qui prennent une forme par scène (anneau en orbite derrière le nom, flux sous le manifeste, océan de points sous les chiffres, hélice, sphère, champ profond, anneau autour de « FIN »). Ils s'écartent autour de la souris et s'agitent quand on défile vite. Moitié des points sur petit écran ; le calque s'éteint tout seul si la machine peine.
- Rendu pellicule : vignettage léger et grain argentique animé par-dessus l'image (un calque qui glisse, sans repeinture), perforations sur les bords du générique, moniteur de programme avec cadres de sécurité dans le Parcours. Désactivés en mode allégé et en animations réduites.
- Fin : le contact est un clap de tournage (timecode à l'heure de Lyon, il claque en entrant à l'écran), puis un fondu au noir qui se resserre en éclipse cerclée par l'anneau de points.
- Chiffres illustrés dessinés en Canvas 2D à leur échelle réelle (15 000 points, jauge CVSS, 901 cases sur 1 000…), redessinés seulement quand le défilement change l'image.
- Son coupé par défaut, synthétisé en direct avec la Web Audio API (aucun fichier audio) ; le choix est mémorisé dans le navigateur. Pendant la lecture automatique, un cliquetis de projecteur à 24 images par seconde ; un claquement quand le clap se ferme.
- Curseur viseur (souris uniquement) : quatre coins qui cadrent l'élément cliquable survolé, avec l'action en légende.
- `index.html` (FR) est la seule source. Après chaque modification, lancer `python3 build.py` : il recalcule les empreintes de la politique de sécurité (CSP) de `index.html` et de `404.html`, et régénère la version anglaise `en/index.html`, en s'arrêtant si un texte français n'a plus sa traduction. La 404 est bilingue dans un seul fichier, sans script tiers.
- Sécurité : CSP stricte en balise meta (scripts en ligne autorisés par empreinte SHA-256), scripts tiers vérifiés par SRI, aucun cookie ni outil de mesure d'audience. Un petit défi attend dans la console du navigateur.

En local :

```bash
python3 -m http.server 8000
```
