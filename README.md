# VELOciraptors HD website

A small static site generator: Markdown content in `content/` is built into
plain HTML pages in `public/`. There is no framework, no JavaScript build
step, and no database — just Python turning text files into a website.

If you just want to **edit text, add a blog post, change a color, or swap
an image**, you don't need anything on this page — see
[CONTENT-GUIDE.md](CONTENT-GUIDE.md) instead. This file is for whoever
maintains the build script itself.

## How it fits together

```
content/{de,en}/home.md         → /de/  and /en/            (home page)
content/{de,en}/blog/*.md       → /de/blog/ and /en/blog/    (one post per file)
content/{de,en}/imprint.md      → /de/imprint/ and /en/imprint/
data/site.yml                   → social links, sponsors, contact, site name
css/style.css, js/main.js, images/  → copied into public/ as-is
scripts/build.py                → reads all of the above, writes public/
```

Every `##` heading in a page's Markdown automatically becomes an entry in
that page's right-hand chapter navigation (and its mobile "Contents"
dropdown) — there's no separate table of contents to maintain. Blog posts
are the one exception: don't put a heading in the post body itself, its
`##` is generated automatically from the post's frontmatter `title`.

Image captions use the Markdown "title" slot: `` ![alt text](path "caption shown under the image") ``.

## Building locally

Requires Python 3. First time only:

```
pip install -r requirements.txt
```

Then, any time you want to preview changes:

```
python3 scripts/build.py
```

This regenerates the entire `public/` folder from scratch. The pages use
root-relative paths (e.g. `/css/style.css`) for clean URLs, so opening a
file directly (`file://...`) will *not* load the CSS/JS/images correctly —
serve it over a tiny local server instead:

```
python3 -m http.server 8000 --directory public
```

Then open <http://localhost:8000/de/> (or `/en/`) in a browser. Stop the
server with Ctrl+C when you're done. `public/` is gitignored; it's
rebuilt on every push by GitHub Actions, never committed.

## Deploying (GitHub Pages)

`.github/workflows/deploy.yml` has two jobs:

- **build** runs on every push to `main` — it just checks the site still
  builds correctly. It does *not* publish anything.
- **deploy** only runs when someone manually clicks **"Run workflow"** on
  the `deploy.yml` workflow in the repo's **Actions** tab (or
  `gh workflow run deploy.yml`). This is the step that actually goes
  live/updates the live site.

So pushing commits is always safe to do at any point — the site only ever
goes (or stays) live when someone deliberately triggers a deploy run. Once
you *do* want every push to auto-publish, delete the
`if: github.event_name == 'workflow_dispatch'` line from the `deploy` job.

One-time setup after the repo exists on GitHub: **Settings → Pages →
Source → "GitHub Actions"**. This alone doesn't publish anything — nothing
is actually live until the first manual "Run workflow" deploy.

**If the site ends up at `https://<user>.github.io/<repo-name>/`** (a
GitHub Pages *project* page, as opposed to a custom domain or a
`<user>.github.io` user/org page), set `baseUrl: "/<repo-name>"` in
`data/site.yml` — otherwise the site's internal links will point at the
domain root and 404. Leave it as `""` for a custom domain or a user/org
page.

## Build script internals

- `scripts/build.py` — the whole pipeline: frontmatter parsing, Markdown
  rendering, chapter/TOC extraction, blog post assembly, static asset
  copying.
- `templates/layout.py` — page/header/footer/chapter-nav HTML, built with
  plain Python f-strings (no templating engine — there are only six pages
  total: 3 kinds × 2 languages).
- `templates/icons.py` — the platform-name → inline SVG icon lookup used
  for header social links.

Frontmatter is a hand-rolled parser (flat `key: value` pairs only — no YAML
dependency needed for that). Markdown → HTML uses the `Markdown` package
with its `toc` extension, which is also what assigns heading `id`s and
supplies the chapter list; a custom slugify function spells out German
umlauts (`ü` → `ue`) instead of dropping them. `data/site.yml` uses
`PyYAML`.

Root-relative paths written in Markdown content (`/images/...`) are
rewritten with `baseUrl` at build time if it's set, so editors never need
to think about it.
