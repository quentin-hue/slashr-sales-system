# Audit technique SEO — Reference

> Reference on-demand. Chargee par le subagent collector-website et /audit.

## 9 categories d'audit technique

### 1. Crawlability
- robots.txt : Disallow critiques, User-agent specifiques
- Sitemap XML : present, valide, a jour (< 48h pour les sites dynamiques)
- Nombre de pages dans le sitemap vs pages indexees (ratio)
- Profondeur de crawl (pages a > 3 clics de la homepage)

### 2. Indexability
- Meta robots : noindex sur des pages importantes ?
- Canonical : coherents, pas de boucles
- Pages orphelines (dans le sitemap mais pas linkees)

### 3. Securite
- HTTPS : certificat valide, pas de mixed content
- HSTS headers

### 4. URLs
- Structure propre (pas de parametres excessifs)
- Redirections : pas de chaines (301 → 301 → 301)
- 404 sur des pages importantes

### 5. Mobile
- Viewport meta tag
- Responsive design
- Tap targets suffisamment espaces

### 6. Performance (CWV)
- Voir `context/references/cwv-thresholds.md`

### 7. Structured Data
- Types de schema presents
- Validation (pas d'erreurs dans le Rich Results Test)
- Couverture (% de pages avec schema)

### 8. Rendu JavaScript
- Le contenu principal est-il dans le HTML initial ou genere par JS ?
- SSR/SSG vs CSR (impact sur le crawl)

### 9. Internationalisation
- hreflang (si multilingue)
- Coherence langue/region
