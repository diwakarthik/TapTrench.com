# Tap Trench website

Static, SEO-ready website. No server needed: upload to GitHub Pages and it runs.

## Quick edits (no rebuild) — `assets/js/config.js`
- **Google Forms**: paste each form's embed URL into `contact`, `activate`, `reseller`, `waitlist`.
  Google Forms → **Send → `< >` tab → copy only the `src="…"` URL**.
- **Brand carousel**: add logo files to `assets/logos/` and list them under `brands`. Any number works (100+ is fine).

## Content edits — `_build/build.py`
Business details, products, prices, FAQ and page copy live at the top of `_build/build.py`.
After editing, run `python3 _build/build.py` and upload the changed files. It rewrites every page,
`sitemap.xml` and `robots.txt`.

Adding a product: add an entry to `PRODUCTS`, put four images in `assets/img/products/`
named `<img>-1.webp … <img>-4.webp` (plus `-sm` versions at half size), and rebuild.

## Publish on GitHub Pages
1. New repository → **Add file → Upload files** → drag in everything in this folder (including `.nojekyll`) → Commit.
2. **Settings → Pages** → Deploy from a branch → `main` / root → Save.
3. Live at `https://<username>.github.io/<repo>/` in a minute or two.

## Connect taptrench.com
1. **Settings → Pages → Custom domain** → `taptrench.com` → Save. Tick **Enforce HTTPS** once available.
2. DNS at your registrar: `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `CNAME` for `www` → `<username>.github.io`.

## After launch (SEO)
1. Add the site to **Google Search Console** and submit `https://taptrench.com/sitemap.xml`.
2. Link your **Google Business Profile** to taptrench.com.
3. Test product pages in Google's **Rich Results Test** (they include Product, FAQ and Breadcrumb data).
