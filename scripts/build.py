#!/usr/bin/env python3
"""
Builds the static site: reads Markdown content from content/<lang>/ and
data/site.yml, and writes finished HTML pages into public/.

Run with:  python3 scripts/build.py
(GitHub Actions runs this same command automatically on every push.)
"""

import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import markdown  # noqa: E402
import yaml  # noqa: E402

from templates.layout import (  # noqa: E402
    UI_STRINGS,
    render_lang_redirect,
    render_page,
)

CONTENT_DIR = ROOT / "content"
DATA_FILE = ROOT / "data" / "site.yml"
PUBLIC_DIR = ROOT / "public"
LANGUAGES = ("de", "en")

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", re.DOTALL)
IMG_WITH_TITLE_RE = re.compile(r'<p>\s*(<img[^>]*\btitle="([^"]*)"[^>]*/?>)\s*</p>', re.IGNORECASE)

MONTHS = {
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
           "August", "September", "Oktober", "November", "Dezember"],
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
}


# ---------------------------------------------------------------------------
# Content parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(raw_text):
    """Splits '---\\nkey: value\\n---\\nbody' into (dict, body)."""
    match = FRONTMATTER_RE.match(raw_text)
    if not match:
        return {}, raw_text
    fm_text, body = match.groups()
    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        data[key] = value
    return data, body


def read_md_file(path):
    raw = path.read_text(encoding="utf-8")
    return parse_frontmatter(raw)


def parse_date(value):
    try:
        return datetime.strptime(str(value), "%Y-%m-%d")
    except (ValueError, TypeError):
        return datetime.min


def format_date(date_str, lang):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return date_str
    months = MONTHS[lang]
    if lang == "de":
        return f"{d.day}. {months[d.month - 1]} {d.year}"
    return f"{months[d.month - 1]} {d.day}, {d.year}"


# ---------------------------------------------------------------------------
# Markdown -> HTML, with captioned images and auto chapter/TOC extraction
# ---------------------------------------------------------------------------

def convert_captioned_images(html_body):
    """`![alt](src "caption")` renders as <img title="caption"> inside a <p>;
    turn that into a proper <figure><img><figcaption> and drop the now
    redundant title attribute (the caption is shown, not just on hover)."""

    def replace(match):
        img_tag, caption = match.groups()
        img_tag = re.sub(r'\s+title="[^"]*"', "", img_tag)
        return f'<figure class="content-figure">{img_tag}<figcaption>{caption}</figcaption></figure>'

    return IMG_WITH_TITLE_RE.sub(replace, html_body)


UMLAUT_MAP = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})


def slugify_de(value, separator):
    """Like the default TOC slugify, but spells out German umlauts (ü -> ue)
    instead of silently dropping them, so anchors stay readable."""
    value = value.lower().translate(UMLAUT_MAP)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip()
    return re.sub(r"[\s" + re.escape(separator) + "]+", separator, value)


def render_markdown(text):
    """Converts Markdown to HTML and returns (html, chapters) where chapters
    is the list of level-2 headings as [{"id": ..., "title": ...}, ...],
    auto-derived from the same heading ids used in the rendered HTML."""
    md = markdown.Markdown(
        extensions=["toc"],
        extension_configs={"toc": {"slugify": slugify_de}},
        output_format="html5",
    )
    html_body = md.convert(text)
    html_body = convert_captioned_images(html_body)
    html_body = re.sub(r"<img(?![^>]*\bloading=)", '<img loading="lazy"', html_body)
    chapters = [
        {"id": tok["id"], "title": tok["name"]}
        for tok in getattr(md, "toc_tokens", [])
        if tok["level"] == 2
    ]
    return html_body, chapters


def apply_base_url(html_body, site):
    """Editors write image/link paths in Markdown as root-relative
    ("/images/..."). If the site is deployed under a sub-path (baseUrl is
    non-empty), prefix those so they still resolve correctly."""
    base = site.get("baseUrl", "")
    if not base:
        return html_body
    return re.sub(r'(src|href)="/', f'\\1="{base}/', html_body)


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_home_page(lang, site):
    data, body = read_md_file(CONTENT_DIR / lang / "home.md")
    body_html, chapters = render_markdown(body)
    body_html = apply_base_url(body_html, site)
    title = data.get("title") or UI_STRINGS[lang]["home"]
    return render_page(lang, "home", title, data.get("description", ""), body_html, chapters, site)


def build_imprint_page(lang, site):
    data, body = read_md_file(CONTENT_DIR / lang / "imprint.md")
    body_html, chapters = render_markdown(body)
    body_html = apply_base_url(body_html, site)
    title = data.get("title") or UI_STRINGS[lang]["imprint"]
    return render_page(lang, "imprint", title, data.get("description", ""), body_html, chapters, site)


def build_blog_page(lang, site):
    posts_dir = CONTENT_DIR / lang / "blog"
    entries = []
    for path in sorted(posts_dir.glob("*.md")):
        data, body = read_md_file(path)
        if data.get("draft") is True:
            continue
        entries.append((data, body))
    entries.sort(key=lambda entry: parse_date(entry[0].get("date")), reverse=True)

    # Each post becomes its own "## Title" section in one combined Markdown
    # document — the exact same document shape as home.md — so the same
    # heading-harvest step drives the blog's chapter nav with no special
    # casing. The post body itself should NOT start with its own heading;
    # the chapter title always comes from the frontmatter "title" field.
    sections = []
    for data, body in entries:
        title = data.get("title", "Untitled")
        date_str = str(data.get("date", ""))
        meta_html = (
            f'<p class="post-meta"><time datetime="{date_str}">'
            f"{format_date(date_str, lang)}</time></p>"
        )
        sections.append(f"## {title}\n\n{meta_html}\n\n{body.strip()}\n")
    combined_markdown = "\n".join(sections)

    body_html, chapters = render_markdown(combined_markdown)
    body_html = apply_base_url(body_html, site)
    return render_page(lang, "blog", UI_STRINGS[lang]["blog"], "", body_html, chapters, site)


# ---------------------------------------------------------------------------
# Build orchestration
# ---------------------------------------------------------------------------

def load_site():
    with open(DATA_FILE, encoding="utf-8") as f:
        site = yaml.safe_load(f)
    # Lets `scripts/preview.py` build for local viewing (served at the
    # domain root) without having to edit data/site.yml's real baseUrl,
    # which is set for wherever the site is actually deployed.
    if "SITE_BASE_URL" in os.environ:
        site["baseUrl"] = os.environ["SITE_BASE_URL"]
    return site


def copy_static_assets():
    for name in ("css", "js", "images"):
        src = ROOT / name
        if src.exists():
            shutil.copytree(src, PUBLIC_DIR / name)


def write_page(path, html_content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_content, encoding="utf-8")


def main():
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True)

    site = load_site()

    copy_static_assets()
    (PUBLIC_DIR / ".nojekyll").write_text("", encoding="utf-8")
    write_page(PUBLIC_DIR / "index.html", render_lang_redirect(site))

    for lang in LANGUAGES:
        write_page(PUBLIC_DIR / lang / "index.html", build_home_page(lang, site))
        write_page(PUBLIC_DIR / lang / "blog" / "index.html", build_blog_page(lang, site))
        write_page(PUBLIC_DIR / lang / "imprint" / "index.html", build_imprint_page(lang, site))

    print(f"Built site into {PUBLIC_DIR}")


if __name__ == "__main__":
    main()
