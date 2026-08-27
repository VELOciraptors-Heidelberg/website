# Editing this website — no coding required

You never need to install anything. Every change below can be made
directly on github.com: open the file, click the pencil (✎) "Edit" icon,
make your change, and click "Commit changes" at the bottom. About a
minute later, the live site updates itself automatically.

Each page is a plain text file written in **Markdown** — a simple way to
write "bold", *italic*, headings, links, and images without any HTML.

## Edit existing text (home page or imprint)

Open the file for the page and language you want to change:

- `content/de/home.md` / `content/en/home.md` — the home page
- `content/de/imprint.md` / `content/en/imprint.md` — the imprint page

Lines starting with `##` are section headings — they automatically show up
in the "Contents" list on the right of the page, so you never need to
update that list by hand. Just edit the text underneath.

## Add a blog post

1. Go to `content/de/blog/` (or `content/en/blog/`).
2. Copy an existing post file — e.g. duplicate `2025-03-11-cycling-camp.md`
   by opening it, copying its contents, then creating a new file.
3. Name the new file `YYYY-MM-DD-a-short-title.md` (the date in the
   filename is just for humans browsing the folder — it doesn't control
   ordering).
4. At the top, edit the three lines between `---`:
   ```
   ---
   title: "Your Post Title"
   date: 2025-06-01
   draft: false
   ---
   ```
   The `date` field is what actually controls ordering — newest first.
   **Don't add a heading (`#` or `##`) in the text below** — the post's
   title on the page comes from `title:` above automatically.
5. Write the post underneath, in plain text / Markdown.
6. To hide a post without deleting it (e.g. a draft), set `draft: true`.

Add the exact same post (translated) to the other language's `blog/`
folder with the same filename, or skip it if a post only applies to one
language.

## Add an image with a caption

```
![Short description for accessibility](/images/blog/2025-06-01-example/photo.jpg "Caption text shown under the image")
```

- The part in `[...]` is read aloud by screen readers — always fill it in.
- The part in `"..."` after the image path is the visible caption.
- Upload the image file itself into the matching folder under `images/`
  (drag-and-drop works directly on github.com) — `.jpg`, `.png`, or `.svg`
  all work.
- On wide screens the image floats to the right with text wrapping beside
  it; on phones it automatically becomes a centered, full-width block —
  you don't need to do anything differently for that.

To swap an existing photo, upload a new file with the **same name** as the
one you're replacing.

## Add a bullet list of links

Any line starting with `- ` becomes a bullet point; wrap link text in
`[...]( )`:

```
- [Join our WhatsApp group](https://chat.whatsapp.com/example)
- [Follow us on Instagram](https://instagram.com/veloraptors_hd)
```

## Add a social media icon to the header

Open `data/site.yml`, find the `social:` list, and copy one block:

```yaml
  - platform: instagram
    url: "https://instagram.com/veloraptors_hd"
    label: "Instagram"
```

`platform` picks the icon automatically. Supported values: `instagram`,
`facebook`, `whatsapp`, `strava`, `komoot`, `youtube`, `tiktok`. Anything
else falls back to a generic link icon — the site won't break if you type
a platform that isn't in that list yet.

## Add a sponsor logo

1. Upload the logo file into `images/sponsors/`.
2. In `data/site.yml`, copy one block under `sponsors:`:
   ```yaml
     - name: "Sponsor Name"
       logo: "/images/sponsors/their-logo.png"
       url: "https://example.com"
   ```

## Change the site's colors

Open `css/style.css` — the very first section (clearly marked
`1. THEME — EDIT COLORS / FONTS HERE`) lists every color as a single line
like:

```
--color-primary: #3a6b35;     /* links, headings, buttons */
```

Change the `#` value (any hex color code) and save — that's the only part
of this file you should need to touch.

## Things to avoid

- Don't remove the `---` lines at the top of a content file, or the fields
  between them — the site won't know the page's title/date without them.
- Keep `##` for section headings (not `#`, which is reserved for the page
  title, or `###`, which won't show up in the Contents list).
- If a change doesn't seem to appear on the live site after a minute or
  two, check the "Actions" tab on GitHub for a red ✗ — it usually means a
  YAML file (`site.yml`) has a typo like a missing colon or quote.
