# Showreel · Alessandro Gagliardi

Mon CV en version showreel de motion design : **https://pazificateur69.github.io/showreel/**

Ingénieur cybersécurité et DevSecOps à Lyon. Le site se regarde comme une bande démo : amorce 3-2-1, timecode et barre de lecture, chiffres clés en compteurs, parcours sur une timeline de montage, scène red team / blue team, projets avec aperçus animés, générique de fin.

- **Lecture** : faire défiler, ou appuyer sur « Lancer le showreel » (ou Espace) pour une lecture automatique.
- **Accessibilité** : avec « réduire les animations » activé dans le système, la page s'affiche en version statique complète.

## Technique

Un seul fichier `index.html`, sans build.

- [GSAP](https://gsap.com) 3.13 + ScrollTrigger (séquences pilotées par le défilement), [Lenis](https://lenis.darkroom.engineering) (défilement fluide), chargés depuis cdnjs et jsDelivr avec contrôle d'intégrité (SRI).
- Polices Google Fonts : Anybody (axe de largeur animé), Instrument Sans, Martian Mono.
- Aperçus de projets dessinés en Canvas 2D, icônes Phosphor.

En local :

```bash
python3 -m http.server 8000
```
