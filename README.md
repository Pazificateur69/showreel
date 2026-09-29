# Showreel · Alessandro Gagliardi

Mon CV en version showreel de motion design :

- Français : **https://pazificateur69.github.io/showreel/**
- English: **https://pazificateur69.github.io/showreel/en/**

Ingénieur cybersécurité et DevSecOps à Lyon. Le site se regarde comme une bande démo : amorce 3-2-1, timecode et barre de lecture, chiffres clés en compteurs, parcours sur une timeline de montage, scène red team / blue team, projets avec aperçus animés, générique de fin. Le CV est aussi téléchargeable en PDF (FR et EN).

- **Lecture** : faire défiler, ou appuyer sur « Lancer le showreel » (ou Espace) pour une lecture automatique.
- **Accessibilité** : avec « réduire les animations » activé dans le système, la page s'affiche en version statique complète.
- **Machines modestes** : si l'ordinateur n'arrive pas à suivre, le site passe tout seul en mode allégé (défilement natif, titres fixes). On peut le forcer avec `?lite`.

## Technique

Pages statiques, sans build côté site.

- [GSAP](https://gsap.com) 3.13 + ScrollTrigger (séquences pilotées par le défilement), [Lenis](https://lenis.darkroom.engineering) (défilement fluide), chargés depuis cdnjs et jsDelivr avec contrôle d'intégrité (SRI).
- Polices Google Fonts : Anybody (axe de largeur animé), Instrument Sans, Martian Mono.
- Aperçus de projets dessinés en Canvas 2D, icônes Phosphor.
- `index.html` (FR) est la seule source. La version anglaise `en/index.html` se régénère avec `python3 build_en.py` : le script s'arrête si un texte français n'a plus sa traduction.

En local :

```bash
python3 -m http.server 8000
```
