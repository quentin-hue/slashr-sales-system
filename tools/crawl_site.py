#!/usr/bin/env python3
"""
SLASHR Website Crawl — Module 11

Crawle le site prospect (homepage + sitemap + pages cles) et produit
4 fichiers JSON dans .cache/deals/{deal_id}/website/ :
  - homepage.json      : analyse detaillee page d'accueil
  - sitemap.json       : structure sitemap et distribution URLs
  - sampled_pages.json : analyse 3-5 pages echantillonnees
  - crawl_summary.json : synthese + scoring_hints (consomme par l'agent)

Contraintes :
  - Max 10 requetes HTTP, timeout 60s global, 20s/requete
  - Respecte robots.txt
  - stdlib uniquement (Python 3.9+)

Usage:
    python3 tools/crawl_site.py <domain> <deal_id>

Exit codes:
    0 = OK
    1 = erreur d'usage
    2 = domaine injoignable (homepage KO)
    3 = erreur inattendue
"""

import json
import os
import re
import ssl
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = "SLASHR-Bot/1.0 (+https://slashr.fr/bot)"
TIMEOUT_PER_REQUEST = 20  # seconds
TIMEOUT_GLOBAL = 60  # seconds
MAX_REQUESTS = 10
MAX_REDIRECTS = 3
MAX_BODY_BYTES = 500_000  # 500 KB
SITEMAP_URL_CAP = 5000
MAX_SAMPLE_PAGES = 5
CACHE_FRESHNESS_HOURS = 24

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"

# ---------------------------------------------------------------------------
# Logging helpers (match preflight_check.py style)
# ---------------------------------------------------------------------------

logs = []


def log(level, msg):
    line = "[{}] {}".format(level, msg)
    logs.append(line)
    print(line)


def log_info(msg):
    log("INFO", msg)


def log_warn(msg):
    log("WARN", msg)


def log_error(msg):
    log("ERROR", msg)


def log_skip(msg):
    log("SKIP", msg)


# ---------------------------------------------------------------------------
# RequestBudget — global counters
# ---------------------------------------------------------------------------

class RequestBudget:
    def __init__(self):
        self.count = 0
        self.start_time = time.time()

    def can_request(self):
        if self.count >= MAX_REQUESTS:
            return False
        if time.time() - self.start_time >= TIMEOUT_GLOBAL:
            return False
        return True

    def record(self):
        self.count += 1

    def elapsed(self):
        return time.time() - self.start_time

    def remaining_time(self):
        return max(0, TIMEOUT_GLOBAL - self.elapsed())


budget = RequestBudget()

# ---------------------------------------------------------------------------
# SSL context (accept certificates — some sites have bad chains)
# ---------------------------------------------------------------------------

_ssl_ctx = ssl.create_default_context()


# ---------------------------------------------------------------------------
# PageFetcher — HTTP GET with redirects, body cap, encoding
# ---------------------------------------------------------------------------

class PageFetcher:

    @staticmethod
    def fetch(url, max_bytes=MAX_BODY_BYTES, retries=1):
        """Fetch a URL. Returns (body_str, final_url, status) or raises."""
        if not budget.can_request():
            raise BudgetExhausted("Budget HTTP epuise ({} requetes, {:.0f}s)".format(
                budget.count, budget.elapsed()))

        last_err = None
        for attempt in range(retries + 1):
            try:
                timeout = min(TIMEOUT_PER_REQUEST, budget.remaining_time())
                if timeout <= 0:
                    raise BudgetExhausted("Timeout global atteint")

                req = urllib_request.Request(url, headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
                    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.5",
                })

                resp = urllib_request.urlopen(req, timeout=timeout, context=_ssl_ctx)
                budget.record()

                final_url = resp.url
                raw = resp.read(max_bytes)

                # Detect encoding
                charset = "utf-8"
                ct = resp.headers.get("Content-Type", "")
                m = re.search(r"charset=([\w-]+)", ct, re.I)
                if m:
                    charset = m.group(1)

                try:
                    body = raw.decode(charset, errors="replace")
                except (LookupError, UnicodeDecodeError):
                    body = raw.decode("utf-8", errors="replace")

                return body, final_url, resp.status

            except (HTTPError, URLError, OSError, BudgetExhausted) as e:
                last_err = e
                if attempt < retries and not isinstance(e, BudgetExhausted):
                    time.sleep(1)
                    continue
                raise

        raise last_err  # unreachable but satisfies linter


class BudgetExhausted(Exception):
    pass


# ---------------------------------------------------------------------------
# RobotsTxtChecker
# ---------------------------------------------------------------------------

class RobotsTxtChecker:
    def __init__(self):
        self.disallowed = []
        self.sitemaps = []
        self.fetched = False

    def fetch(self, domain):
        url = "https://{}/robots.txt".format(domain)
        try:
            body, _, status = PageFetcher.fetch(url, max_bytes=100_000, retries=0)
            self.fetched = True
            self._parse(body)
            log_info("robots.txt: {} regles Disallow, {} sitemaps declares".format(
                len(self.disallowed), len(self.sitemaps)))
        except Exception:
            log_warn("robots.txt: inaccessible, on continue sans restrictions")
            self.fetched = True

    def _parse(self, body):
        applies = False
        for line in body.splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            if line.lower().startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip().lower()
                applies = agent in ("*", "slashr-bot")
            elif applies and line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    self.disallowed.append(path)
            elif line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                # Re-join because ":" was split
                if not sitemap_url.startswith("http"):
                    sitemap_url = "Sitemap:" + sitemap_url
                    sitemap_url = sitemap_url.split(":", 1)[1].strip()
                # Handle case where URL was split on ":" in protocol
                if sitemap_url and not sitemap_url.startswith("http"):
                    pass  # ignore malformed
                else:
                    self.sitemaps.append(sitemap_url)

    def is_allowed(self, path):
        for rule in self.disallowed:
            if rule.endswith("*"):
                if path.startswith(rule[:-1]):
                    return False
            elif path.startswith(rule):
                return False
        return True


# ---------------------------------------------------------------------------
# LightweightPageAnalyzer — HTMLParser subclass
# ---------------------------------------------------------------------------

class LightweightPageAnalyzer(HTMLParser):
    """Analyse legere d'une page HTML : headings, meta, schema, links, images, forms."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_desc = ""
        self.og_tags = {}
        self.headings = []  # [(level, text)]
        self.schema_types = []
        self.internal_links = []
        self.external_links = []
        self.images_total = 0
        self.images_no_alt = 0
        self.has_form = False
        self.cta_count = 0
        self.nav_items = 0
        self.word_count = 0
        self.content_word_count = 0  # excluding nav/header/footer boilerplate
        self.has_meta_desc = False

        # Parser state
        self._in_title = False
        self._in_nav = False
        self._in_header = False
        self._in_footer = False
        self._in_heading = False
        self._current_heading_level = 0
        self._current_heading_text = ""
        self._current_text = []
        self._boilerplate_text = []  # text inside nav/header/footer
        self._in_script = False
        self._in_style = False
        self._scripts_text = []
        self._base_url = ""

    def set_base_url(self, url):
        self._base_url = url

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower == "title":
            self._in_title = True
        elif tag_lower == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_desc = content
                self.has_meta_desc = True
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._in_heading = True
            self._current_heading_level = int(tag_lower[1])
            self._current_heading_text = ""
        elif tag_lower == "a":
            href = attrs_dict.get("href", "")
            if href and not href.startswith(("#", "javascript:", "mailto:", "tel:")):
                full = urljoin(self._base_url, href)
                parsed = urlparse(full)
                base_parsed = urlparse(self._base_url)
                if parsed.netloc == base_parsed.netloc:
                    self.internal_links.append(full)
                else:
                    self.external_links.append(full)
            # Detect CTA patterns
            classes = attrs_dict.get("class", "").lower()
            text_hint = attrs_dict.get("title", "").lower()
            cta_keywords = ("cta", "btn", "button", "acheter", "commander",
                            "devis", "contact", "panier", "cart", "buy",
                            "order", "shop", "ajouter")
            if any(kw in classes or kw in text_hint or kw in href.lower()
                   for kw in cta_keywords if href):
                self.cta_count += 1
        elif tag_lower == "img":
            self.images_total += 1
            alt = attrs_dict.get("alt", "")
            if not alt or not alt.strip():
                self.images_no_alt += 1
        elif tag_lower == "form":
            self.has_form = True
        elif tag_lower == "nav":
            self._in_nav = True
        elif tag_lower == "header":
            self._in_header = True
        elif tag_lower == "footer":
            self._in_footer = True
        elif tag_lower == "li" and self._in_nav:
            self.nav_items += 1
        elif tag_lower == "script":
            self._in_script = True
            # Check for JSON-LD schema
            stype = attrs_dict.get("type", "").lower()
            if stype == "application/ld+json":
                pass  # will capture in handle_data
        elif tag_lower == "style":
            self._in_style = True

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = False
        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self._in_heading:
                self.headings.append((self._current_heading_level,
                                      self._current_heading_text.strip()))
                self._in_heading = False
        elif tag_lower == "nav":
            self._in_nav = False
        elif tag_lower == "header":
            self._in_header = False
        elif tag_lower == "footer":
            self._in_footer = False
        elif tag_lower == "script":
            self._in_script = False
        elif tag_lower == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_heading:
            self._current_heading_text += data
        if self._in_script:
            self._scripts_text.append(data)
        if not self._in_script and not self._in_style:
            self._current_text.append(data)
            if self._in_nav or self._in_header or self._in_footer:
                self._boilerplate_text.append(data)

    def finalize(self):
        """Call after feeding all data."""
        text = " ".join(self._current_text)
        self.word_count = len(text.split())

        boilerplate = " ".join(self._boilerplate_text)
        boilerplate_wc = len(boilerplate.split())
        self.content_word_count = max(0, self.word_count - boilerplate_wc)

        # Extract Schema.org from JSON-LD
        for script_text in self._scripts_text:
            try:
                obj = json.loads(script_text)
                self._extract_schema_types(obj)
            except (json.JSONDecodeError, ValueError):
                continue

    def _extract_schema_types(self, obj):
        if isinstance(obj, dict):
            t = obj.get("@type")
            if t:
                if isinstance(t, list):
                    self.schema_types.extend(t)
                else:
                    self.schema_types.append(t)
            # Recurse into @graph
            graph = obj.get("@graph", [])
            if isinstance(graph, list):
                for item in graph:
                    self._extract_schema_types(item)
        elif isinstance(obj, list):
            for item in obj:
                self._extract_schema_types(item)

    def to_dict(self):
        return {
            "title": self.title.strip(),
            "meta_description": self.meta_desc,
            "has_meta_description": self.has_meta_desc,
            "og_tags": self.og_tags,
            "headings": [{"level": h[0], "text": h[1]} for h in self.headings],
            "heading_depth": max((h[0] for h in self.headings), default=0),
            "h1_count": sum(1 for h in self.headings if h[0] == 1),
            "schema_types": sorted(set(self.schema_types)),
            "internal_links_count": len(self.internal_links),
            "external_links_count": len(self.external_links),
            "images_total": self.images_total,
            "images_no_alt": self.images_no_alt,
            "has_form": self.has_form,
            "cta_count": self.cta_count,
            "nav_items": self.nav_items,
            "word_count": self.word_count,
            "content_word_count": self.content_word_count,
            "is_spa_suspect": self.content_word_count < 50,
        }


def analyze_page(body, url):
    """Parse a page and return analysis dict."""
    parser = LightweightPageAnalyzer()
    parser.set_base_url(url)
    try:
        parser.feed(body)
    except Exception:
        pass  # HTMLParser can be lenient
    parser.finalize()
    result = parser.to_dict()
    result["url"] = url
    return result, parser


# ---------------------------------------------------------------------------
# SitemapParser
# ---------------------------------------------------------------------------

class SitemapParser:
    def __init__(self, domain, robots):
        self.domain = domain
        self.robots = robots
        self.urls = []
        self.url_sources = {}  # url -> sub-sitemap filename that contained it
        self.is_index = False
        self.sub_sitemaps = []

    def parse(self):
        """Try to fetch and parse sitemap. Returns url list."""
        # Try sitemaps declared in robots.txt first
        sitemap_urls = list(self.robots.sitemaps) if self.robots.sitemaps else []
        if not sitemap_urls:
            sitemap_urls = [
                "https://{}/sitemap.xml".format(self.domain),
                "https://{}/sitemap_index.xml".format(self.domain),
            ]

        for sm_url in sitemap_urls:
            if not budget.can_request():
                break
            try:
                body, _, status = PageFetcher.fetch(sm_url, max_bytes=MAX_BODY_BYTES, retries=0)
                self._parse_xml(body, sm_url)
                if self.urls:
                    log_info("Sitemap: {} URLs trouvees depuis {}".format(
                        len(self.urls), sm_url))
                    break
                elif self.sub_sitemaps:
                    log_info("Sitemap index: {} sub-sitemaps depuis {}".format(
                        len(self.sub_sitemaps), sm_url))
                    break
            except Exception:
                continue

        # If we found a sitemap index, fetch sub-sitemaps (budget permitting)
        if self.sub_sitemaps and not self.urls:
            for sub_url in self.sub_sitemaps[:3]:  # max 3 sub-sitemaps
                if not budget.can_request():
                    break
                try:
                    body, _, _ = PageFetcher.fetch(sub_url, max_bytes=MAX_BODY_BYTES, retries=0)
                    self._parse_xml(body, sub_url)
                except Exception:
                    continue
            if self.urls:
                log_info("Sitemap: {} URLs trouvees (via {} sub-sitemaps)".format(
                    len(self.urls), len(self.sub_sitemaps)))

        if not self.urls:
            log_warn("Sitemap: aucune URL trouvee")

        return self.urls[:SITEMAP_URL_CAP]

    def _parse_xml(self, body, source_url):
        try:
            root = ElementTree.fromstring(body)
        except ElementTree.ParseError:
            return

        # Strip namespace
        ns = ""
        m = re.match(r"\{(.+?)\}", root.tag)
        if m:
            ns = "{" + m.group(1) + "}"

        # Sitemap index?
        for sitemap in root.findall("{}sitemap".format(ns)):
            loc = sitemap.find("{}loc".format(ns))
            if loc is not None and loc.text:
                self.sub_sitemaps.append(loc.text.strip())
                self.is_index = True

        # URL set — track source sub-sitemap for classification
        source_filename = urlparse(source_url).path.split("/")[-1].lower()
        for url_elem in root.findall("{}url".format(ns)):
            loc = url_elem.find("{}loc".format(ns))
            if loc is not None and loc.text:
                url = loc.text.strip()
                self.urls.append(url)
                self.url_sources[url] = source_filename
                if len(self.urls) >= SITEMAP_URL_CAP:
                    break

    # Sub-sitemap filename → category mapping (WordPress, Shopify, PrestaShop, etc.)
    _SITEMAP_NAME_HINTS = {
        "product": ("product", "produit", "produkt", "productos"),
        "category": ("category", "categorie", "collection", "taxon"),
        "blog": ("post", "blog", "article", "actualite", "news", "recette"),
        "page": ("page",),
    }

    def _classify_by_sitemap_name(self, filename):
        """Classify a URL based on its source sub-sitemap filename."""
        for category, keywords in self._SITEMAP_NAME_HINTS.items():
            if any(kw in filename for kw in keywords):
                return category
        return None

    def classify_urls(self):
        """Classify URLs into categories.

        Priority:
          1. Sub-sitemap filename (most reliable — CMS-generated)
          2. URL path pattern (regex on known segments)
          3. Structural analysis (sibling count per parent path)
        """
        categories = {
            "product": 0,
            "category": 0,
            "blog": 0,
            "page": 0,
            "other": 0,
        }

        product_patterns = re.compile(
            r"/(produit|product|shop|boutique|p/|item|article-de-|sku)[/s]?", re.I)
        category_patterns = re.compile(
            r"/(categorie|category|collection|rayon|gamme|famille)[/s]?", re.I)
        blog_patterns = re.compile(
            r"/(blog|actualite|actus?|news|magazine|journal|recette|conseil)[/s]?", re.I)

        # Pass 1: classify by sub-sitemap name, then URL pattern
        unclassified = []
        for url in self.urls:
            source = self.url_sources.get(url, "")
            cat = self._classify_by_sitemap_name(source)
            if cat:
                categories[cat] += 1
                continue

            path = urlparse(url).path.lower()
            if product_patterns.search(path):
                categories["product"] += 1
            elif category_patterns.search(path):
                categories["category"] += 1
            elif blog_patterns.search(path):
                categories["blog"] += 1
            elif path in ("/", "") or path.count("/") <= 2:
                categories["page"] += 1
            else:
                unclassified.append(url)

        # Pass 2: structural analysis on remaining unclassified URLs.
        # If many URLs share the same parent path (>5 siblings), it's a catalog section.
        if unclassified:
            parent_counts = {}
            for url in unclassified:
                path = urlparse(url).path.rstrip("/")
                parent = path.rsplit("/", 1)[0] if "/" in path else ""
                parent_counts.setdefault(parent, []).append(url)

            for parent, urls in parent_counts.items():
                if len(urls) >= 5:
                    # Catalog section (many siblings = product listing)
                    categories["product"] += len(urls)
                else:
                    categories["page"] += len(urls)

        total = len(self.urls) or 1
        editorial = categories["blog"] + categories["page"]
        catalog = categories["product"] + categories["category"]

        return {
            "total_urls": len(self.urls),
            "distribution": categories,
            "editorial_count": editorial,
            "catalog_count": catalog,
            "editorial_ratio": round(editorial / total, 2),
            "catalog_ratio": round(catalog / total, 2),
            "is_sitemap_index": self.is_index,
            "sub_sitemaps_count": len(self.sub_sitemaps),
        }


# ---------------------------------------------------------------------------
# PageSampler — select diverse pages to sample
# ---------------------------------------------------------------------------

class PageSampler:
    # Language path prefixes to exclude (avoids sampling translated duplicates)
    _LANG_PREFIXES = re.compile(
        r"^/(en|de|es|it|pt|nl|ja|zh|ko|ru|ar|pl|sv|da|no|fi|cs|tr|ro|hu|el|he|th|vi|uk|id|ms)"
        r"(/|$)", re.I)

    @classmethod
    def _is_lang_variant(cls, url):
        path = urlparse(url).path
        return bool(cls._LANG_PREFIXES.match(path))

    @staticmethod
    def select(sitemap_urls, homepage_internal_links, domain, max_pages=MAX_SAMPLE_PAGES):
        """Select a diverse set of pages to sample."""
        candidates = set()

        # From sitemap: pick varied paths
        if sitemap_urls:
            # Group by first path segment, excluding language variants
            by_segment = {}
            for url in sitemap_urls:
                parsed = urlparse(url)
                if parsed.netloc and domain not in parsed.netloc:
                    continue
                if PageSampler._is_lang_variant(url):
                    continue
                parts = parsed.path.strip("/").split("/")
                segment = parts[0] if parts and parts[0] else "_root"
                by_segment.setdefault(segment, []).append(url)

            # Take one from each top segment
            segments_sorted = sorted(by_segment.keys(),
                                     key=lambda s: len(by_segment[s]), reverse=True)
            for seg in segments_sorted[:max_pages]:
                urls = by_segment[seg]
                # Pick one that's not too deep
                best = min(urls, key=lambda u: len(urlparse(u).path))
                candidates.add(best)

        # Fill from homepage internal links if needed (also excluding lang variants)
        if len(candidates) < max_pages and homepage_internal_links:
            for link in homepage_internal_links:
                if link not in candidates and not PageSampler._is_lang_variant(link):
                    candidates.add(link)
                if len(candidates) >= max_pages:
                    break

        # Remove homepage itself
        homepage_variants = {
            "https://{}/".format(domain),
            "https://{}".format(domain),
            "https://www.{}/".format(domain),
            "https://www.{}".format(domain),
        }
        candidates -= homepage_variants

        return list(candidates)[:max_pages]


# ---------------------------------------------------------------------------
# CacheManager
# ---------------------------------------------------------------------------

class CacheManager:
    def __init__(self, deal_id):
        self.cache_dir = CACHE_DIR / "deals" / str(deal_id) / "website"

    def is_fresh(self):
        """Check if cache exists and is <24h old."""
        summary = self.cache_dir / "crawl_summary.json"
        if not summary.exists():
            return False
        age_hours = (time.time() - summary.stat().st_mtime) / 3600
        return age_hours < CACHE_FRESHNESS_HOURS

    def cache_age_hours(self):
        summary = self.cache_dir / "crawl_summary.json"
        if not summary.exists():
            return None
        return (time.time() - summary.stat().st_mtime) / 3600

    def ensure_dir(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def write(self, filename, data):
        self.ensure_dir()
        path = self.cache_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path


# ---------------------------------------------------------------------------
# Scoring hints generator
# ---------------------------------------------------------------------------

def compute_scoring_hints(homepage_data, sitemap_data, sampled_data):
    """Generate scoring hints for S2, S3, S4 from crawl data."""
    hints = {"s2": [], "s3": [], "s4": []}

    # --- S2: Architecture & technique ---
    if homepage_data:
        schema_types = homepage_data.get("schema_types", [])
        expected_schema = {"Organization", "WebSite", "LocalBusiness",
                           "Product", "BreadcrumbList"}
        found = set(schema_types)
        missing_schema = expected_schema - found
        if schema_types:
            hints["s2"].append("Schema.org: {} type(s) trouve(s) ({})".format(
                len(schema_types), ", ".join(sorted(found))))
        else:
            hints["s2"].append("Schema.org: AUCUN type trouve (manque donnees structurees)")

        if missing_schema:
            hints["s2"].append("Schema.org manquants recommandes: {}".format(
                ", ".join(sorted(missing_schema))))

        h1 = homepage_data.get("h1_count", 0)
        if h1 == 0:
            hints["s2"].append("Homepage: pas de H1")
        elif h1 > 1:
            hints["s2"].append("Homepage: {} H1 (devrait etre unique)".format(h1))

        depth = homepage_data.get("heading_depth", 0)
        if depth < 2:
            hints["s2"].append("Hierarchie headings faible (profondeur max: H{})".format(depth))

        if homepage_data.get("is_spa_suspect"):
            hints["s2"].append("SPA suspect: word_count={} (<50 mots sur homepage)".format(
                homepage_data.get("word_count", 0)))

    if sitemap_data:
        total = sitemap_data.get("total_urls", 0)
        if total == 0:
            hints["s2"].append("Pas de sitemap XML detecte")
        else:
            hints["s2"].append("Sitemap: {} URLs indexables".format(total))

    # Sampled pages: schema coverage
    if sampled_data:
        pages_with_schema = sum(
            1 for p in sampled_data if p.get("schema_types"))
        total_sampled = len(sampled_data)
        if total_sampled > 0:
            pct = round(100 * pages_with_schema / total_sampled)
            hints["s2"].append("Schema.org coverage pages echantillonnees: {}% ({}/{})".format(
                pct, pages_with_schema, total_sampled))

    # --- S3: Contenu ---
    if sitemap_data:
        total = sitemap_data.get("total_urls", 0)
        editorial = sitemap_data.get("editorial_count", 0)
        catalog = sitemap_data.get("catalog_count", 0)
        ratio = sitemap_data.get("editorial_ratio", 0)

        if total > 0:
            hints["s3"].append("Pages sitemap: {} total ({} editoriales, {} catalogue)".format(
                total, editorial, catalog))
            hints["s3"].append("Ratio editorial: {:.0%}".format(ratio))
        if total < 20:
            hints["s3"].append("Moins de 20 pages — site tres leger")

    if sampled_data:
        word_counts = [p.get("content_word_count", p.get("word_count", 0))
                       for p in sampled_data]
        if word_counts:
            avg_wc = sum(word_counts) // len(word_counts)
            hints["s3"].append("Word count moyen contenu (hors nav/header/footer): {} mots".format(avg_wc))
            thin = sum(1 for wc in word_counts if wc < 300)
            if thin > 0:
                hints["s3"].append("Thin content: {}/{} pages < 300 mots (contenu seul)".format(
                    thin, len(word_counts)))

        no_meta = sum(1 for p in sampled_data if not p.get("has_meta_description"))
        if no_meta > 0:
            hints["s3"].append("Meta descriptions manquantes: {}/{} pages".format(
                no_meta, len(sampled_data)))

    # --- S4: UX / Conversion ---
    if homepage_data:
        cta = homepage_data.get("cta_count", 0)
        hints["s4"].append("CTAs homepage: {}".format(cta))
        if cta == 0:
            hints["s4"].append("Aucun CTA detecte sur la homepage")

        nav = homepage_data.get("nav_items", 0)
        hints["s4"].append("Navigation: {} items".format(nav))

        if homepage_data.get("has_form"):
            hints["s4"].append("Formulaire detecte sur homepage")
        else:
            hints["s4"].append("Pas de formulaire sur homepage")

        imgs_no_alt = homepage_data.get("images_no_alt", 0)
        imgs_total = homepage_data.get("images_total", 0)
        if imgs_no_alt > 0:
            hints["s4"].append("Images sans alt: {}/{} sur homepage".format(
                imgs_no_alt, imgs_total))

    return hints


# ---------------------------------------------------------------------------
# CrawlOrchestrator — main pipeline
# ---------------------------------------------------------------------------

class CrawlOrchestrator:
    def __init__(self, domain, deal_id):
        self.domain = domain.lower().strip().rstrip("/")
        # Strip protocol if provided
        if self.domain.startswith("http://"):
            self.domain = self.domain[7:]
        if self.domain.startswith("https://"):
            self.domain = self.domain[8:]
        if self.domain.startswith("www."):
            self.domain = self.domain[4:]

        self.deal_id = deal_id
        self.cache = CacheManager(deal_id)
        self.robots = RobotsTxtChecker()
        self.homepage_url = "https://{}".format(self.domain)

        self.homepage_data = None
        self.sitemap_data = None
        self.sampled_pages_data = []
        self.errors = []

    def run(self):
        """Main crawl pipeline."""
        print("\n=== SLASHR Website Crawl — Module 11 ===")
        print("Domaine: {}".format(self.domain))
        print("Deal ID: {}\n".format(self.deal_id))

        # 1. Cache check
        if self.cache.is_fresh():
            age = self.cache.cache_age_hours()
            log_info("Cache fresh ({:.1f}h), skipping crawl".format(age))
            print("\nResult: CACHE_HIT (reuse)")
            return 0

        # 2. robots.txt
        self.robots.fetch(self.domain)

        # 3. Homepage
        try:
            homepage_body, final_url, status = PageFetcher.fetch(
                self.homepage_url, retries=1)
            log_info("Homepage: {} ({} chars)".format(final_url, len(homepage_body)))

            analysis, parser = analyze_page(homepage_body, final_url)
            self.homepage_data = analysis
            homepage_links = parser.internal_links

        except BudgetExhausted as e:
            log_error("Homepage: budget epuise — {}".format(e))
            self.errors.append("Homepage inaccessible (budget)")
            return self._write_and_exit(2)
        except Exception as e:
            log_error("Homepage KO: {}".format(e))
            self.errors.append("Homepage inaccessible: {}".format(e))
            return self._write_and_exit(2)

        # 4. Sitemap
        sitemap_parser = SitemapParser(self.domain, self.robots)
        sitemap_urls = []
        try:
            sitemap_urls = sitemap_parser.parse()
            self.sitemap_data = sitemap_parser.classify_urls()
        except BudgetExhausted:
            log_warn("Sitemap: budget epuise, skip")
            self.sitemap_data = {"total_urls": 0, "distribution": {},
                                 "editorial_count": 0, "catalog_count": 0,
                                 "editorial_ratio": 0, "catalog_ratio": 0,
                                 "is_sitemap_index": False, "sub_sitemaps_count": 0}
        except Exception as e:
            log_warn("Sitemap: erreur ({})".format(e))
            self.sitemap_data = {"total_urls": 0, "distribution": {},
                                 "editorial_count": 0, "catalog_count": 0,
                                 "editorial_ratio": 0, "catalog_ratio": 0,
                                 "is_sitemap_index": False, "sub_sitemaps_count": 0}

        # 5. Sample pages
        if budget.can_request():
            sample_urls = PageSampler.select(
                sitemap_urls, homepage_links, self.domain)
            log_info("Pages a echantillonner: {}".format(len(sample_urls)))

            for url in sample_urls:
                if not budget.can_request():
                    log_warn("Budget epuise, arret echantillonnage")
                    break

                path = urlparse(url).path
                if not self.robots.is_allowed(path):
                    log_skip("Page bloquee par robots.txt: {}".format(path))
                    continue

                try:
                    body, final_url, _ = PageFetcher.fetch(url, retries=0)
                    page_data, _ = analyze_page(body, final_url)
                    self.sampled_pages_data.append(page_data)
                    log_info("  Echantillon: {} ({} mots contenu)".format(
                        final_url, page_data.get("content_word_count", 0)))
                except Exception as e:
                    log_warn("  Echantillon KO {}: {}".format(url, e))
                    self.errors.append("Page {} inaccessible: {}".format(url, e))

        # 6. Write output
        return self._write_and_exit(0)

    def _write_and_exit(self, exit_code):
        """Write 4 JSON files and display summary."""

        # homepage.json
        hp_output = self.homepage_data or {}
        self.cache.write("homepage.json", hp_output)

        # sitemap.json
        sm_output = self.sitemap_data or {}
        self.cache.write("sitemap.json", sm_output)

        # sampled_pages.json
        self.cache.write("sampled_pages.json", self.sampled_pages_data)

        # scoring hints
        scoring_hints = compute_scoring_hints(
            self.homepage_data, self.sitemap_data, self.sampled_pages_data)

        # crawl_summary.json
        summary = {
            "domain": self.domain,
            "deal_id": self.deal_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "http_requests": budget.count,
            "elapsed_seconds": round(budget.elapsed(), 1),
            "exit_code": exit_code,
            "homepage_ok": self.homepage_data is not None,
            "sitemap_urls_found": (self.sitemap_data or {}).get("total_urls", 0),
            "pages_sampled": len(self.sampled_pages_data),
            "errors": self.errors,
            "scoring_hints": scoring_hints,
        }
        self.cache.write("crawl_summary.json", summary)

        # Summary display
        print("\n--- Synthese ---")
        print("Requetes HTTP: {}/{}".format(budget.count, MAX_REQUESTS))
        print("Temps: {:.1f}s / {}s".format(budget.elapsed(), TIMEOUT_GLOBAL))
        print("Homepage: {}".format("OK" if self.homepage_data else "KO"))
        print("Sitemap URLs: {}".format(
            (self.sitemap_data or {}).get("total_urls", 0)))
        print("Pages echantillonnees: {}".format(len(self.sampled_pages_data)))

        if scoring_hints:
            print("\n--- Scoring Hints ---")
            for force, hints in scoring_hints.items():
                if hints:
                    print("{}:".format(force.upper()))
                    for h in hints:
                        print("  - {}".format(h))

        if self.errors:
            print("\n--- Erreurs ---")
            for e in self.errors:
                print("  - {}".format(e))

        output_dir = self.cache.cache_dir
        print("\nFichiers: {}".format(output_dir))
        print("Result: {}".format(
            "OK" if exit_code == 0 else "DEGRADED" if exit_code == 2 else "ERROR"))

        return exit_code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tools/crawl_site.py <domain> <deal_id>")
        print("Exemple: python3 tools/crawl_site.py biscuiterie-mere-poulard.com 560")
        sys.exit(1)

    domain = sys.argv[1]
    deal_id = sys.argv[2]

    try:
        orchestrator = CrawlOrchestrator(domain, deal_id)
        code = orchestrator.run()
        sys.exit(code)
    except KeyboardInterrupt:
        print("\nInterrompu.")
        sys.exit(3)
    except Exception as e:
        print("\n[FATAL] Erreur inattendue: {}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()
