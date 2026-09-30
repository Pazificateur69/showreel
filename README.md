# Showreel · Alessandro Gagliardi

Mon CV en version showreel de motion design :

- Français : **https://pazificateur69.github.io/showreel/**
- English: **https://pazificateur69.github.io/showreel/en/**

Ingénieur cybersécurité et DevSecOps à Lyon. Le site se regarde comme une bande démo : amorce 3-2-1, timecode et barre de lecture, chiffres clés en compteurs, parcours sur une timeline de montage, scène red team / blue team, projets avec aperçus animés, générique de fin. Le CV est aussi téléchargeable en PDF (FR et EN).

- **Lecture** : faire défiler, ou appuyer sur « Lancer le showreel » (ou Espace) pour une lecture automatique.
- **Accessibilité** : avec « réduire les animations » activé dans le système, la page s'affiche en version statique complète.
- **Version rapide** : `?rapide` (ou `?quick` en anglais) affiche le CV en défilement simple, sans animation.
- **Machines modestes** : si l'ordinateur n'arrive pas à suivre, le site passe tout seul en mode allégé (défilement natif, titres fixes). On peut le forcer avec `?lite`.

## Technique

Pages statiques, sans build côté site.

- [GSAP](https://gsap.com) 3.13 + ScrollTrigger (séquences pilotées par le défilement), [Lenis](https://lenis.darkroom.engineering) (défilement fluide), chargés depuis cdnjs et jsDelivr avec contrôle d'intégrité (SRI).
- Polices Google Fonts : Anybody (axe de largeur animé), Instrument Sans, Martian Mono.
- Aperçus de projets dessinés en Canvas 2D, plus les vrais écrans (démos SVG des dépôts ExploitSpec et NightOwl, capture de curs3d.fr dans `img/`). Icônes Phosphor.
- Calque 3D en WebGL pur (sans bibliothèque) : 15 000 points qui prennent une forme par scène (anneau en orbite derrière le nom, flux sous le manifeste, océan de points sous les chiffres, hélice, sphère, champ profond, anneau autour de « FIN »). Ils s'écartent autour de la souris et s'agitent quand on défile vite. Moitié des points sur petit écran ; le calque s'éteint tout seul si la machine peine.
- Chiffres illustrés dessinés en Canvas 2D à leur échelle réelle (15 000 points, jauge CVSS, 901 cases sur 1 000…), redessinés seulement quand le défilement change l'image.
- Son coupé par défaut, synthétisé en direct avec la Web Audio API (aucun fichier audio) ; le choix est mémorisé dans le navigateur.
- `index.html` (FR) est la seule source. Après chaque modification, lancer `python3 build.py` : il recalcule les empreintes de la politique de sécurité (CSP) et régénère la version anglaise `en/index.html`, en s'arrêtant si un texte français n'a plus sa traduction.
- Sécurité : CSP stricte en balise meta (scripts en ligne autorisés par empreinte SHA-256), scripts tiers vérifiés par SRI, aucun cookie ni outil de mesure d'audience. Un petit défi attend dans la console du navigateur.

En local :

```bash
python3 -m http.server 8000
```
