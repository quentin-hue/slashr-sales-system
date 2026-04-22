# Spec Crawl Screaming Frog — Reference

> Ce fichier definit la configuration standard pour les crawls Screaming Frog deposes dans le Drive avant /prepare.

## Quand fournir un crawl SF

Toujours si possible. Le crawl SF est la source de donnees la plus fiable pour l'analyse de contenu et technique. Le systeme fonctionne sans (fallback DataForSEO + garde-fous), mais la qualite du diagnostic est significativement meilleure avec.

## Configuration SF

- **Rendering :** JavaScript / Chromium
- **Respect robots.txt :** Oui
- **Vitesse :** 2 URLs/sec max (ne pas surcharger le site prospect)
- **Profondeur :** Illimitee (ou limiter a 5 niveaux si site > 10 000 pages)
- **Stockage :** Crawl complet, pas d'echantillonnage

## Colonnes d'export obligatoires

| Colonne SF | Usage systeme |
|-----------|--------------|
| Adresse (URL) | Identification + classification par archetype |
| Code HTTP | Pages cassees, redirections, soft 404 |
| Titre 1 | Optimisation on-page, detection duplicats |
| Meta Description 1 | Presence/absence, longueur |
| H1-1 | Coherence title/H1 |
| Nombre de mots | Mesure factuelle du contenu par page |
| Indexabilite | Noindex, canonical vers autre page, etc. |
| Statut d'indexabilite | Raison de non-indexabilite |
| Canonical Link Element 1 | Detection cannibalisation |
| Liens entrants internes | Maillage reel (nombre de pages qui linkent vers cette page) |
| Liens sortants internes | Maillage sortant |
| Type de contenu | HTML, JS, image, etc. |

## Extracteur custom (optionnel mais recommande)

Configurer 1 extracteur CSS ou XPath pour capturer le contenu editorial des pages categorie/listing. Le selecteur depend du CMS :

| CMS | Selecteur type |
|-----|---------------|
| OroCommerce | `.category-long-description`, `.cms-page__content` |
| Shopify | `.collection-description`, `.rte` |
| PrestaShop | `.category-description`, `#category-description` |
| Magento | `.category-description`, `.category-cms` |
| WooCommerce | `.term-description`, `.woocommerce-products-header` |
| Autre | Inspecter la page, identifier le bloc texte sous le H1 / au-dessus ou en-dessous des produits |

**Comment trouver le bon selecteur :** ouvrir une page categorie qui a du contenu visible, clic droit > Inspecter sur le texte editorial, noter la classe CSS du conteneur parent.

## Format d'export

- **Format :** CSV (separateur virgule ou point-virgule, UTF-8)
- **Nom de fichier :** libre, le systeme detecte automatiquement un CSV SF par ses colonnes
- **Ou le deposer :** dans le dossier Google Drive du deal (dossier_r1_link dans Pipedrive)

## Ce que le systeme fait avec le CSV

1. collector-drive le ramasse avec les autres fichiers
2. collector-website le detecte (colonnes "Adresse" + "Code HTTP") et le copie dans le cache
3. Les analystes (content, technical) l'utilisent en priorite sur le crawl automatique DataForSEO
4. Le resume est integre dans le SDB (nombre de pages, ratio contenu, word count moyen)

## Si pas de CSV SF

Le systeme continue avec DataForSEO. Si le site est protege par un WAF (Cloudflare, etc.), le systeme avertit le closer et applique les garde-fous (R22-R27). Le diagnostic est possible mais moins fiable sur les aspects contenu et technique page-level.
