# Core Web Vitals — Seuils de reference

> Reference on-demand. Chargee par les subagents /audit et collector-website quand une analyse CWV est necessaire.

## Seuils (Juin 2025)

| Metrique | Bon | A ameliorer | Mauvais |
|----------|-----|-------------|---------|
| **LCP** (Largest Contentful Paint) | <= 2.5s | 2.5-4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | <= 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | <= 0.1 | 0.1-0.25 | > 0.25 |

## Notes
- **INP remplace FID** depuis mars 2024. Ne jamais utiliser FID.
- LCP est le plus impactant pour le SEO (correle avec le ranking).
- Mesurer avec PageSpeed Insights API ou Chrome UX Report (CrUX).
- Les donnees CrUX (field data) priment sur les donnees Lighthouse (lab data).

## Interpretation business
- LCP > 4s : "Votre site met plus de 4 secondes a afficher le contenu principal. Google penalise ce type de lenteur dans les classements."
- INP > 500ms : "Les interactions sur votre site sont lentes. Les visiteurs peuvent abandonner avant de convertir."
- CLS > 0.25 : "Votre page bouge pendant le chargement. C'est destabilisant pour les visiteurs et penalise par Google."
