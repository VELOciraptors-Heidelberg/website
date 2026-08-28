"""
HTML page templates, built with plain Python functions and f-strings.
No templating engine is needed: there are only three page kinds (home,
blog, imprint) times two languages, six pages total.

Every string that comes from YAML data or Markdown frontmatter is passed
through escape_html() before being placed into HTML, since nothing else
protects against a stray "&", "<" or '"' breaking the markup.
"""

import html as _html

from templates.icons import get_icon

PAGE_PATHS = {"home": "", "blog": "blog/", "imprint": "imprint/"}

UI_STRINGS = {
    "de": {
        "skip_to_content": "Zum Inhalt springen",
        "contents": "Inhalt",
        "sponsors": "Unsere Sponsoren",
        "imprint": "Impressum",
        "language": "Sprache",
        "primary_navigation": "Hauptnavigation",
        "home": "Startseite",
        "blog": "Blog",
    },
    "en": {
        "skip_to_content": "Skip to content",
        "contents": "Contents",
        "sponsors": "Our Sponsors",
        "imprint": "Imprint",
        "language": "Language",
        "primary_navigation": "Main navigation",
        "home": "Home",
        "blog": "Blog",
    },
}


def escape_html(value):
    if value is None:
        return ""
    return _html.escape(str(value), quote=True)


def page_url(lang, page_kind, site):
    return f"{site.get('baseUrl', '')}/{lang}/{PAGE_PATHS[page_kind]}"


def asset_url(path, site):
    return f"{site.get('baseUrl', '')}{path}"


def render_header(lang, page_kind, site):
    t = UI_STRINGS[lang]
    home_href = page_url(lang, "home", site)
    site_name = escape_html(site["siteName"].get(lang, site["siteName"].get("en", "")))

    social_items = []
    for s in site.get("social", []):
        label = escape_html(s.get("label") or s.get("platform") or "")
        social_items.append(
            f'<li><a href="{escape_html(s.get("url", ""))}" aria-label="{label}" '
            f'target="_blank" rel="noopener noreferrer">{get_icon(s.get("platform"))}</a></li>'
        )
    social_html = "".join(social_items)

    lang_items = []
    for code, label in (("de", "DE"), ("en", "EN")):
        href = page_url(code, page_kind, site)
        current = ' aria-current="page"' if code == lang else ""
        lang_items.append(f'<a href="{href}"{current} hreflang="{code}">{label}</a>')
    lang_html = "".join(lang_items)

    nav_items = []
    for kind in ("home", "blog"):
        href = page_url(lang, kind, site)
        current = ' aria-current="page"' if kind == page_kind else ""
        nav_items.append(f'<a href="{href}"{current}>{t[kind]}</a>')
    nav_html = "".join(nav_items)

    logo_src = asset_url("/images/logo.svg", site)

    return f"""<header class="site-header">
  <div class="wrap">
    <a class="site-logo" href="{home_href}"><img src="{logo_src}" alt="{site_name}" width="44" height="44"></a>
    <p class="site-name"><a href="{home_href}">{site_name}</a></p>
    <div class="header-right">
      <ul class="social-links">{social_html}</ul>
      <nav class="lang-switch" aria-label="{t['language']}">{lang_html}</nav>
    </div>
  </div>
  <div class="wrap">
    <nav class="primary-nav" aria-label="{t['primary_navigation']}">{nav_html}</nav>
  </div>
</header>"""


def render_footer(lang, site):
    t = UI_STRINGS[lang]
    sponsors = site.get("sponsors", [])
    sponsors_block = ""
    if sponsors:
        items = []
        for sp in sponsors:
            name = escape_html(sp.get("name", ""))
            logo_src = asset_url(sp.get("logo", ""), site)
            items.append(
                f'<li><a href="{escape_html(sp.get("url", ""))}" target="_blank" rel="noopener noreferrer">'
                f'<img src="{logo_src}" alt="{name}" loading="lazy"></a></li>'
            )
        sponsors_block = (
            f'<h2 class="sponsors-heading">{t["sponsors"]}</h2>'
            f'<ul class="sponsors">{"".join(items)}</ul>'
        )

    contact = site.get("contact", {})
    contact_bits = []
    if contact.get("email"):
        email = escape_html(contact["email"])
        contact_bits.append(f'<a href="mailto:{email}">{email}</a>')
    if contact.get("phone"):
        contact_bits.append(f"<span>{escape_html(contact['phone'])}</span>")
    contact_html = " &middot; ".join(contact_bits)

    imprint_href = page_url(lang, "imprint", site)

    return f"""<footer class="site-footer">
  <div class="wrap">
    {sponsors_block}
    <div class="footer-bottom">
      <ul class="footer-links">
        <li><a href="{imprint_href}">{t['imprint']}</a></li>
      </ul>
      <p class="footer-contact">{contact_html}</p>
    </div>
  </div>
</footer>"""


def render_chapter_nav_desktop(chapters, lang):
    if len(chapters) < 2:
        return ""
    t = UI_STRINGS[lang]
    items = "".join(f'<li><a href="#{c["id"]}">{escape_html(c["title"])}</a></li>' for c in chapters)
    return f"""<aside class="chapter-nav-desktop" aria-label="{t['contents']}">
      <h2>{t['contents']}</h2>
      <nav><ol>{items}</ol></nav>
    </aside>"""


def render_chapter_nav_mobile(chapters, lang):
    if len(chapters) < 2:
        return ""
    t = UI_STRINGS[lang]
    items = "".join(f'<li><a href="#{c["id"]}">{escape_html(c["title"])}</a></li>' for c in chapters)
    return f"""<details class="chapter-nav-mobile">
      <summary>{t['contents']}</summary>
      <nav aria-label="{t['contents']}"><ol>{items}</ol></nav>
    </details>"""


def render_page(lang, page_kind, title, description, body_html, chapters, site):
    t = UI_STRINGS[lang]
    header = render_header(lang, page_kind, site)
    footer = render_footer(lang, site)
    nav_desktop = render_chapter_nav_desktop(chapters, lang)
    nav_mobile = render_chapter_nav_mobile(chapters, lang)
    site_name = site["siteName"].get(lang, "")
    page_title = escape_html(title) if title else ""
    full_title = f"{page_title} — {escape_html(site_name)}" if page_title else escape_html(site_name)

    alt_lang = "en" if lang == "de" else "de"
    this_href = page_url(lang, page_kind, site)
    alt_href = page_url(alt_lang, page_kind, site)
    css_href = asset_url("/css/style.css", site)
    js_src = asset_url("/js/main.js", site)
    icon_href = asset_url("/images/logo.svg", site)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{escape_html(description or '')}">
<link rel="alternate" hreflang="{lang}" href="{this_href}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">
<link rel="icon" href="{icon_href}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_href}">
</head>
<body>
<a class="skip-link" href="#main-content">{t['skip_to_content']}</a>
{header}
<div class="page-shell wrap">
{nav_mobile}
<div class="page-layout">
<main id="main-content" class="main-content">
{body_html}
</main>
{nav_desktop}
</div>
</div>
{footer}
<script src="{js_src}" defer></script>
</body>
</html>
"""


def render_lang_redirect(site):
    de_href = page_url("de", "home", site)
    en_href = page_url("en", "home", site)

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VELOciraptors HD</title>
<meta http-equiv="refresh" content="0;url={de_href}">
<script>
(function () {{
  var lang = (navigator.language || "de").toLowerCase();
  var target = lang.indexOf("en") === 0 ? "{en_href}" : "{de_href}";
  window.location.replace(target);
}})();
</script>
</head>
<body>
<p>Deutsch: <a href="{de_href}">weiter auf Deutsch</a></p>
<p>English: <a href="{en_href}">continue in English</a></p>
</body>
</html>
"""
