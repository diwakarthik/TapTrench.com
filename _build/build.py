#!/usr/bin/env python3
"""
Tap Trench static site builder.

Edit the SITE / PRODUCTS data below, then run:   python3 _build/build.py
It rewrites every .html page, sitemap.xml and robots.txt in the site root.
(Forms and the brand carousel live in assets/js/config.js — edit those directly.)
"""
import json, os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _asset_version():
    """Short hash of CSS/JS/logo files, appended as ?v= so browsers fetch fresh files after every push."""
    import hashlib
    h = hashlib.sha1()
    for sub in ("assets/css", "assets/js", "assets/logos"):
        d = os.path.join(ROOT, sub)
        for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            with open(os.path.join(d, name), "rb") as fh:
                h.update(name.encode()); h.update(fh.read())
    return h.hexdigest()[:8]

ASSET_V = _asset_version()

SITE = {
    "name": "Tap Trench",
    "url": "https://taptrench.com",          # canonical domain (used for SEO tags + sitemap)
    "tagline": "In the trenches with you.",
    "email": "hello@taptrench.com",
    "phone": "",                              # e.g. "02 0000 0000" — "" hides it
    "address": "Sydney, NSW, Australia",
    "hours": "Monday – Friday, 9am – 5pm AEST",
    "abn": "",                                # e.g. "12 345 678 901" — "" hides it
    "socials": {"instagram": "", "facebook": "", "linkedin": "", "tiktok": ""},
    "trademark": "All trademarks, logos and brand names shown are the property of their respective owners and are used for identification purposes only.",
}

PRODUCTS = [
    {
        "slug": "google-review-tap-plate",
        "cat": "review",
        "name": "Star Tile",
        "kind": "Google Review Tap Plate",
        "variant": "Square",
        "price": 90, "compare": 150, "sold": "40,000+",
        "img": "review-square",
        "short": "One tap opens your Google review page. No app, no searching.",
        "description": "The fastest way to collect genuine Google reviews at the counter. Customers tap the plate with their iPhone or Android phone and your Google review page opens instantly, ready for their stars and words. We program your own review link into the secure chip before it ships, so it works from day one, every time.",
        "features": [
            "Opens your Google review page with a single tap",
            "Works with iPhone and Android phones, no app needed",
            "Your review link is programmed and locked by us before dispatch",
            "Glossy domed finish that wipes clean on busy counters",
            "Built for life: no battery, no charging, no monthly subscription",
        ],
        "alts": ["Google Review Tap Plate on a studio background",
                 "Phone tapping the Google Review Tap Plate to open a review page",
                 "Google Review Tap Plate on a shop counter",
                 "Google Review Tap Plate close-up on a dark background"],
        "keywords": "NFC Google review plate, tap to review Google, Google review stand, get more Google reviews",
    },
    {
        "slug": "menu-tap-plate-square",
        "cat": "menu",
        "name": "Menu Tile",
        "kind": "Tap-to-Order Menu Plate",
        "variant": "Square",
        "price": 90, "compare": 150, "sold": "40,000+",
        "img": "menu-square",
        "short": "Customers tap to open your menu or ordering page instantly.",
        "description": "Put your menu in every customer's hand without printing a single page. A tap of any iPhone or Android phone opens your online menu or ordering page straight away. Ideal for tables, counters and takeaway windows in cafés, restaurants and bars.",
        "features": [
            "Opens your online menu or ordering page in one tap",
            "Works with iPhone and Android phones, no app needed",
            "Your menu link is programmed and locked by us before dispatch",
            "Sleek matte-black look with a glossy domed finish",
            "Built for life: no battery, no charging, no monthly subscription",
        ],
        "alts": ["Square Tap-to-Order Menu Plate on a studio background",
                 "Phone tapping the square menu plate to open a menu",
                 "Square menu tap plate on a restaurant counter",
                 "Square menu tap plate close-up on a dark background"],
        "keywords": "NFC menu plate, tap to order menu, contactless menu, digital menu stand",
    },
    {
        "slug": "menu-tap-plate-round",
        "cat": "menu",
        "name": "Menu Disc",
        "kind": "Tap-to-Order Menu Plate",
        "variant": "Round",
        "price": 70, "compare": 130, "sold": "40,000+",
        "img": "menu-circle",
        "short": "A compact round plate that fits any table. Tap to see the menu.",
        "description": "A neat round tap plate that sits perfectly on café tables, bar tops and menu holders. One tap from any iPhone or Android phone opens your menu or ordering page, so guests can browse and order without waiting.",
        "features": [
            "Opens your online menu or ordering page in one tap",
            "Works with iPhone and Android phones, no app needed",
            "Your menu link is programmed and locked by us before dispatch",
            "Compact round shape made for tables and bar tops",
            "Built for life: no battery, no charging, no monthly subscription",
        ],
        "alts": ["Round Tap-to-Order Menu Plate on a studio background",
                 "Phone tapping the round menu plate to open a menu",
                 "Round menu tap plate on a café counter",
                 "Round menu tap plate close-up on a dark background"],
        "keywords": "round NFC menu tag, tap to order, contactless table menu",
    },
]

INDUSTRIES = ["Cafés", "Restaurants", "Salons", "Barbers", "Gyms", "Dentists", "Clinics", "Tradies", "Retail stores",
              "Bars", "Bakeries", "Hotels", "Mechanics", "Real estate", "Day spas", "Florists", "Pet groomers", "Physios"]

FAQ = [
    ("How it works", [
        ("What is a Tap Trench plate?", "A glossy plate with a secure NFC chip inside. When a customer taps it with their phone, it instantly opens the page we've programmed into it, such as your Google review page or your online menu."),
        ("Which phones does it work with?", "Both iPhone and Android. Modern iPhones read NFC automatically, and most Android phones do too. Customers simply hold the top of their phone near the plate."),
        ("Do my customers need an app?", "No. Tapping opens a normal web page in their phone's browser, so there's nothing to download."),
        ("What happens when a customer taps the review plate?", "It opens your Google review page directly, so the customer can choose their stars and write their review in their own words."),
        ("Does it need batteries or charging?", "No. The chip is powered by the customer's phone during the tap, so there's nothing to charge or replace."),
    ]),
    ("Setup & activation", [
        ("How do I get my review link?", "Open your Google Business Profile, tap 'Get more reviews' (sometimes called 'Ask for reviews'), and copy the link it shows you. Send that link to us when you activate your product."),
        ("Who sets the plate up?", "We do. An authorised Tap Trench technician programs your link into the secure chip and locks it, so the plate is ready to use the moment it arrives."),
        ("Can the link be changed later?", "No. For security, the link is locked into the chip once it has been set, which stops anyone from tampering with it. Need a plate for a different link? Simply order another one."),
        ("How many times can it be tapped?", "As many times as you like. There's no tap limit and no expiry."),
        ("Is there a monthly fee?", "No. You pay once for the plate. Unlike many review products, there's no subscription, ever."),
    ]),
    ("Orders, durability & returns", [
        ("Why is everything sold out?", "Demand has outpaced our production runs. Join the waitlist on any product page and we'll reserve yours from the next batch."),
        ("How long does a plate last?", "Tap Trench plates are built for life. There's no battery to run flat, nothing to charge, and the chip is sealed under a tough epoxy dome, so it keeps working tap after tap."),
        ("Can I return a plate I haven't used?", "No. Each plate's secure chip is programmed and locked to your business, so it can't be reused for anyone else. If your plate arrives damaged or doesn't work on arrival, email us and we'll make it right."),
        ("Do you offer bulk or multi-venue orders?", "Yes. Contact us with the number of venues and plates you need, including if you'd like to resell Tap Trench plates."),
    ]),
]

# ---------------------------------------------------------------- helpers
E = html.escape
TODAY = datetime.date.today().isoformat()

ICONS = {
    "check": '<path d="M5 12l5 5L20 7"/>',
    "truck": '<path d="M3 6h11v10H3z"/><path d="M14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    "star": '<path d="M12 3l2.6 5.6 6.1.6-4.6 4.1 1.4 6L12 16.2 6.5 19.3l1.4-6L3.3 9.2l6.1-.6z"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "bag": '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "nfc": '<path d="M8 8a6 6 0 0 1 0 8"/><path d="M12 5a10 10 0 0 1 0 14"/><path d="M16 2a14 14 0 0 1 0 20"/>',
    "phoneTap": '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M11 18.5h2"/><path d="M2.5 9.5a4 4 0 0 1 0 5"/><path d="M21.5 9.5a4 4 0 0 0 0 5"/>',
    "counter": '<path d="M7 3h10l2 18H5z"/><path d="M3 21h18"/><path d="M10 9a3 3 0 0 1 4 0"/><path d="M8.5 7a5.5 5.5 0 0 1 7 0"/>',
    "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "infinity": '<path d="M7.5 15.5C5 15.5 3 13.9 3 12s2-3.5 4.5-3.5C11 8.5 13 15.5 16.5 15.5 19 15.5 21 13.9 21 12s-2-3.5-4.5-3.5C13 8.5 11 15.5 7.5 15.5z"/>',
    "smile": '<circle cx="12" cy="12" r="9"/><path d="M8.5 14.5a4.5 4.5 0 0 0 7 0"/><path d="M9 9.5h.01M15 9.5h.01"/>',
    "zap": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7"/><path d="M18 14a6.5 6.5 0 0 1 3.5 6"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "dollar": '<path d="M12 2v20"/><path d="M17 6.5c-1-1.3-2.8-2-5-2-3 0-4.5 1.5-4.5 3.5 0 5 10 2.5 10 8 0 2-1.8 3.5-5 3.5-2.4 0-4.4-.8-5.5-2.2"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
    "megaphone": '<path d="M3 10v4h4l7 5V5L7 10z"/><path d="M18 8a5 5 0 0 1 0 8"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "fb": '<path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V10H6v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h2z"/>',
    "li": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>',
    "tt": '<path d="M14 3v11a4 4 0 1 1-4-4"/><path d="M14 3a5 5 0 0 0 5 5"/>',
    "android": '<rect x="5" y="9" width="14" height="10" rx="2"/><path d="M8 9a4 4 0 0 1 8 0"/><path d="M7 5l1.5 2M17 5l-1.5 2"/><path d="M9.5 12.5h.01M14.5 12.5h.01"/>',
}

def icon(name, size=20, sw=2, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def stars(n=5, size=18):
    return '<span class="stars" aria-hidden="true">' + "".join(icon("star", size) for _ in range(n)) + "</span>"

LOGO = '<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#1D1C1A"/><path d="M12 25v4h16v-4" fill="none" stroke="#CE8558" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="20" cy="21" r="2.4" fill="#CE8558"/><path d="M15 16a7 7 0 0 1 10 0" fill="none" stroke="#CE8558" stroke-width="2.6" stroke-linecap="round"/><path d="M11.5 12.5a12 12 0 0 1 17 0" fill="none" stroke="#CE8558" stroke-width="2.6" stroke-linecap="round"/></svg>'

# Payment marks (simplified, for "accepted payments" display)
def _pm(inner, bg="#fff", stroke="#D9D2CA", label=""):
    return f'<svg viewBox="0 0 50 32" role="img" aria-label="{label}"><rect x=".5" y=".5" width="49" height="31" rx="5" fill="{bg}" stroke="{stroke}"/>{inner}</svg>'
PAY = [
    _pm('<text x="25" y="21" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="900" font-style="italic" font-size="13" fill="#1A1F71" letter-spacing=".5">VISA</text>', label="Visa"),
    _pm('<circle cx="20" cy="16" r="8" fill="#EB001B"/><circle cx="30" cy="16" r="8" fill="#F79E1B"/><path d="M25 9.8a8 8 0 0 1 0 12.4 8 8 0 0 1 0-12.4z" fill="#FF5F00"/>', label="Mastercard"),
    _pm('<text x="25" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="900" font-size="10.5" fill="#fff" letter-spacing=".3">AMEX</text>', bg="#2E77BC", stroke="#2E77BC", label="American Express"),
    _pm('<path d="M14.6 11.2c.5-.6.8-1.4.7-2.2-.7 0-1.6.5-2.1 1.1-.5.5-.9 1.3-.8 2.1.8.1 1.6-.4 2.2-1z M15.3 12.4c-1.2-.1-2.2.7-2.8.7-.6 0-1.4-.6-2.4-.6-1.2 0-2.4.7-3 1.8-1.3 2.2-.3 5.5.9 7.3.6.9 1.3 1.8 2.3 1.8.9 0 1.2-.6 2.3-.6s1.4.6 2.4.6 1.6-.9 2.2-1.8c.7-1 1-2 1-2.1 0 0-1.9-.7-1.9-2.9 0-1.8 1.5-2.7 1.6-2.8-.9-1.3-2.2-1.4-2.6-1.4z" fill="#fff"/><text x="21" y="20.5" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="10" fill="#fff">Pay</text>', bg="#000", stroke="#000", label="Apple Pay"),
    _pm('<text x="8" y="20.5" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="11"><tspan fill="#4285F4">G</tspan><tspan fill="#3C4043"> Pay</tspan></text>', label="Google Pay"),
    _pm('<text x="25" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="900" font-style="italic" font-size="10.5"><tspan fill="#003087">Pay</tspan><tspan fill="#009CDE">Pal</tspan></text>', label="PayPal"),
    _pm('<text x="25" y="19.5" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="8.6" fill="#000">afterpay</text>', bg="#B2FCE4", stroke="#B2FCE4", label="Afterpay"),
    _pm('<text x="25" y="20.5" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="900" font-size="12" fill="#1A0826">zip</text>', bg="#AA8FFF", stroke="#AA8FFF", label="Zip"),
]
PAY_ROW = "".join(PAY)

NAV = [("shop.html", "Shop", "shop"), ("how-it-works.html", "How it works", "how"), ("about.html", "About", "about"), ("faq.html", "FAQs", "faq"), ("contact.html", "Contact", "contact")]

def product_url(p): return f"{p['slug']}.html"
def full_name(p): return f"{p['name']} · {p['kind']}"
def save(p): return round(100 - p["price"] / p["compare"] * 100)
def img(p, n, sm=False): return f"assets/img/products/{p['img']}-{n}{'-sm' if sm else ''}.webp"
def abs_url(path): return SITE["url"].rstrip("/") + "/" + ("" if path == "index.html" else path)

# ---------------------------------------------------------------- shell
def head(page):
    t, d, path = page["title"], page["desc"], page["path"]
    og_img = page.get("og", "assets/img/og-image.png")
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in page.get("ld", []))
    robots = '<meta name="robots" content="noindex">' if page.get("noindex") else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(t)}</title>
<meta name="description" content="{E(d)}">
{robots}
<link rel="canonical" href="{abs_url(path)}">
<meta property="og:site_name" content="Tap Trench">
<meta property="og:type" content="{page.get('ogtype','website')}">
<meta property="og:title" content="{E(t)}">
<meta property="og:description" content="{E(d)}">
<meta property="og:url" content="{abs_url(path)}">
<meta property="og:image" content="{abs_url(og_img)}">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(t)}">
<meta name="twitter:description" content="{E(d)}">
<meta name="twitter:image" content="{abs_url(og_img)}">
<meta name="theme-color" content="#1A1817">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v={ASSET_V}">
<script>document.documentElement.classList.add("js");try{{var t=localStorage.getItem("tt-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
{ld}
</head>"""

def header(active):
    CUR = ' aria-current="page"'
    links = "".join(f'<li><a href="{h}"{CUR if k == active else ""}>{n}</a></li>' for h, n, k in NAV)
    ann_items = [("truck", "Free shipping Australia-wide · Shipping worldwide"), ("star", "100,000+ businesses trust Tap Trench"),
                 ("shield", "Built for life: no battery, no charging"), ("dollar", "No monthly subscription, ever"),
                 ("phoneTap", "Works with iPhone and Android")]
    ann = "".join(f"<span>{icon(i,16)}{t}</span>" for i, t in ann_items)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="announce" aria-label="Highlights"><div class="announce-track">{ann}<span aria-hidden="true"></span>{ann}</div></div>
<header class="site-header"><div class="wrap nav">
<a class="logo" href="index.html" aria-label="Tap Trench home">{LOGO}<span>Tap Trench</span></a>
<nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
<div class="nav-actions">
<button class="icon-btn" type="button" data-theme-toggle aria-label="Switch colour theme">{icon("moon",20,2,"i-moon")}{icon("sun",20,2,"i-sun")}</button>
<button class="icon-btn" type="button" data-cart-open aria-label="Open cart">{icon("bag")}</button>
<a class="btn btn-primary nav-cta" href="activate.html">Activate your product</a>
<button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu" data-menu>{icon("menu",20,2,"i-menu")}{icon("close",20,2,"i-close").replace("<svg", "<svg hidden",1)}</button>
</div></div>
</header>
<nav class="mobile-menu" id="mobile-menu" aria-label="Mobile"><ul>{links}</ul><a class="btn btn-copper" href="activate.html">Activate your product</a></nav>"""

def footer():
    s = SITE["socials"]
    soc = "".join(f'<a href="{E(s[k])}" target="_blank" rel="noopener" aria-label="{lab}">{icon(ic,18)}</a>'
                  for k, ic, lab in [("instagram", "ig", "Instagram"), ("facebook", "fb", "Facebook"), ("linkedin", "li", "LinkedIn"), ("tiktok", "tt", "TikTok")] if s.get(k))
    shop = "".join(f'<li><a href="{product_url(p)}">{E(p["name"])}</a></li>' for p in PRODUCTS)
    contact = f'<li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>' + (f'<li><a href="tel:{SITE["phone"].replace(" ","")}">{SITE["phone"]}</a></li>' if SITE["phone"] else "") + f'<li>{E(SITE["address"])}</li><li>{E(SITE["hours"])}</li>'
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="index.html">{LOGO}<span>Tap Trench</span></a>
<p class="foot-blurb">Tap-to-review and tap-to-order NFC plates for businesses everywhere. One payment, built for life, no subscription.</p>{f'<div class="socials">{soc}</div>' if soc else ''}</div>
<div><h3>Shop</h3><ul>{shop}<li><a href="shop.html">All products</a></li></ul></div>
<div><h3>Help</h3><ul><li><a href="how-it-works.html">How it works</a></li><li><a href="activate.html">Activate your product</a></li><li><a href="faq.html">FAQs</a></li><li><a href="shipping.html">Shipping</a></li><li><a href="returns.html">Returns &amp; product care</a></li></ul></div>
<div><h3>Company</h3><ul><li><a href="about.html">About us</a></li><li><a href="reseller.html">Become a Reseller</a></li><li><a href="contact.html">Contact us</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li></ul></div>
<div><h3>Contact</h3><ul class="foot-contact">{contact}</ul></div>
</div>
<p class="foot-tag" aria-hidden="true">In the trenches <span>with you.</span></p>
<div class="foot-pay" aria-label="Payment methods we accept">{PAY_ROW}</div>
<div class="foot-bottom"><p>© {datetime.date.today().year} Tap Trench{(' · ABN ' + SITE['abn']) if SITE['abn'] else ''}. {E(SITE['trademark'])}</p><p>Proudly Australian. Serving businesses worldwide.</p></div>
</div></footer>"""

def overlays():
    return f"""<div class="modal-back" data-drawer-back></div>
<aside class="drawer" aria-label="Cart" data-drawer><div class="drawer-head"><h2>Your cart</h2><button class="icon-btn" type="button" data-drawer-close aria-label="Close cart">{icon("close")}</button></div>
<div class="drawer-body">{icon("bag",48,1.5)}<p><b style="color:var(--tt-ink)">Your cart is empty.</b></p><p style="font-size:15px">Our plates are selling faster than we can make them. Join the waitlist and we'll reserve yours from the next batch.</p><button class="btn btn-copper btn-shine" type="button" data-waitlist="checkout">{icon("bell",18)} Join the waitlist</button><a class="btn btn-ghost" href="shop.html">Browse the shop</a><div class="pay-row" style="justify-content:center;margin-top:10px">{PAY_ROW}</div></div></aside>
<div class="modal-back" data-modal role="dialog" aria-modal="true" aria-labelledby="wl-title"><div class="modal"><button class="icon-btn modal-close" type="button" data-modal-close aria-label="Close">{icon("close")}</button><div class="modal-head"><span class="eyebrow">Next batch</span><h2 id="wl-title">Be first in line.</h2><p class="muted" data-modal-sub></p></div><div class="modal-body" data-modal-body></div></div></div>
<script src="assets/js/config.js?v={ASSET_V}" defer></script>
<script src="assets/js/forms.js?v={ASSET_V}" defer></script>
<script src="assets/js/main.js?v={ASSET_V}" defer></script>"""

def page(p, body):
    return head(p) + f'\n<body data-email="{SITE["email"]}">\n' + header(p.get("active", "")) + '\n<main id="main">\n' + body + "\n</main>\n" + footer() + "\n" + overlays() + "\n</body>\n</html>\n"

def crumbs(items):
    li = "".join((f'<li><a href="{h}">{E(n)}</a></li>' if h else f'<li aria-current="page">{E(n)}</li>') for n, h in items)
    return f'<nav aria-label="Breadcrumb"><ol class="breadcrumb">{li}</ol></nav>'

def bc(items, path):
    """items: [(name, href or None)] ; returns (html, ld)"""
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(h if h else path)} for i, (n, h) in enumerate(items)]}
    return crumbs(items), ld

def cta(title, text, primary=("activate.html", "Activate your product"), secondary=("shop.html", "Shop the range")):
    return f"""<section class="section flush-top"><div class="wrap"><div class="cta-band reveal"><span class="cta-rings" aria-hidden="true"></span>
<div><h2>{title}</h2><p>{text}</p></div>
<div class="btns"><a class="btn btn-primary btn-shine" href="{primary[0]}">{primary[1]}</a><a class="btn btn-ghost" href="{secondary[0]}">{secondary[1]}</a></div></div></div></section>"""

def pcard(p, i=0):
    d = f" d{i % 3}" if i else ""
    return f"""<a class="pcard reveal{d}" href="{product_url(p)}" data-cat="{p['cat']}">
<div class="pcard-media"><img src="{img(p,1,True)}" alt="{E(p['alts'][0])}" width="700" height="700" loading="lazy"><img class="alt" src="{img(p,2,True)}" alt="" width="700" height="700" loading="lazy" aria-hidden="true">
<div class="badges"><span class="badge sold">Sold out</span><span class="badge sale">Save {save(p)}%</span></div></div>
<div class="pcard-body"><span class="kind">{E(p['kind'])} · {p['variant']}</span><h3>{E(p['name'])}</h3>
<div class="rating">{stars(5,15)}<span>{p['sold']} sold</span></div><p>{E(p['short'])}</p>
<div class="price"><b>${p['price']}</b><s>${p['compare']}</s><span>AUD</span></div>
<span class="soldline"><i class="dot"></i>Sold out, join the waitlist</span></div></a>"""

def stage():
    s5 = "".join(f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS["star"][9:-3]}"/></svg>' for _ in range(5))
    return f"""<div class="stage" aria-hidden="true" data-parallax=".04">
<div class="stage-arch"></div><div class="stage-glow"></div>
<div class="ripple"></div><div class="ripple r2"></div><div class="ripple r3"></div>
<div class="stage-plate"><img src="assets/img/products/review-plate-cutout.webp" alt="" width="800" height="800"></div>
<div class="stage-phone"><div class="screen">
<div class="screen-idle">{icon("nfc",48,2.2)}<span>Tap the plate</span></div>
<div class="screen-live"><b>Your Business</b><small>Rate and review</small><div class="screen-stars">{s5}</div><div class="screen-box">Share details of your own experience…</div><div class="screen-btn">Post review</div></div>
</div></div>
<div class="stage-chip"><span class="chip-dot">{icon("check",16,3)}</span><span>Review page opened<small>1 tap · no app</small></span></div>
</div>"""

# ---------------------------------------------------------------- pages
PAGES = {}

def add(path, meta, body):
    meta = dict(meta, path=path)
    PAGES[path] = page(meta, body)

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Tap Trench", "url": SITE["url"],
       "logo": abs_url("assets/img/apple-touch-icon.png"), "slogan": SITE["tagline"], "email": SITE["email"],
       "areaServed": "AU", "description": "Tap Trench makes NFC tap plates that open a business's Google review page or online menu with one tap of an iPhone or Android phone."}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "name": "Tap Trench", "url": SITE["url"]}

# ---- Home
stats = f"""<div class="stats-grid" data-counters>
<div class="stat reveal"><div class="num" data-count="100000" data-suffix="+">100,000+</div><div class="lbl">Businesses trust Tap Trench</div></div>
<div class="stat reveal d1"><div class="num" data-count="0" data-prefix="$">$0</div><div class="lbl">Monthly subscription, ever</div></div>
<div class="stat reveal d2"><div class="num">For life</div><div class="lbl">No battery, no charging, sealed in epoxy</div></div>
<div class="stat reveal d3"><div class="num" data-count="1" data-suffix=" tap">1 tap</div><div class="lbl">From happy customer to your review page</div></div>
</div>"""
industries = "".join(f'<span class="industry">{x}</span>' for x in INDUSTRIES)
add("index.html", {"title": "Tap Trench | NFC Google Review Plates & Tap-to-Order Menus Australia",
                   "desc": "Get more Google reviews with one tap. Tap Trench NFC review plates and menu plates work with iPhone and Android, need no app and and no subscription. Built for life.",
                   "active": "home", "ld": [ORG, WEBSITE]}, f"""
<section class="hero"><div class="wrap hero-grid">
<div>
<span class="eyebrow">NFC tap plates for local business</span>
<h1>In the trenches <em>with you.</em></h1>
<p class="lead">Tap Trench plates turn happy customers into Google reviews. One tap of any iPhone or Android phone opens your review page instantly. No app, no searching, no subscription.</p>
<div class="hero-ctas"><a class="btn btn-primary btn-shine" href="shop.html">{icon("bag",18)} Shop tap plates</a><a class="btn btn-ghost" href="activate.html">Activate your product</a></div>
<div class="trust-line">{stars()}<span><b style="color:var(--tt-ink)">100,000+</b> businesses trust Tap Trench</span></div>
<div class="hero-ticks"><span>{icon("check",18)}iPhone &amp; Android</span><span>{icon("check",18)}Built for life</span><span>{icon("check",18)}No monthly fees</span></div>
</div>
{stage()}
</div></section>

<section class="brands" aria-labelledby="brands-h">
<h2 id="brands-h"><strong>100,000+</strong> businesses trust Tap Trench</h2>
<div class="brand-rows" data-brands></div>
<p class="tm-note">{E(SITE['trademark'])}</p>
</section>

<section class="section"><div class="wrap split">
<div class="reveal">
<span class="eyebrow">Why reviews matter</span>
<h2>Your next customer is reading reviews right now.</h2>
<p class="lead">Before anyone walks through your door, they check your stars. More recent Google reviews help you show up higher in local search and win the click over the shop down the road.</p>
<p class="lead" style="margin-top:14px">Most happy customers would leave a review. They just forget. A Tap Trench plate puts your review page in their hand while they're still smiling.</p>
<a class="btn btn-primary" style="margin-top:28px" href="how-it-works.html">See how it works {icon("arrow",18)}</a>
</div>
<div class="reveal d2"><div class="photo" data-tilt><img src="assets/img/products/review-square-2.webp" alt="A phone tapping a Tap Trench Google Review plate to open the review page" width="1400" height="1400" loading="lazy"></div></div>
</div></section>

<section class="section flush-top"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">The range</span><h2>Pick your tap plate.</h2></div>
<p class="lead">The Star Tile for reviews, the Menu Tile and Menu Disc for every table. Each is programmed with your link before it ships.</p></div>
<div class="products">{''.join(pcard(p, i) for i, p in enumerate(PRODUCTS))}</div>
<div style="text-align:center;margin-top:40px"><a class="btn btn-ghost" href="shop.html">View the shop {icon("arrow",18)}</a></div>
</div></section>

<section class="section dark"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Why Tap Trench</span><h2>Pay once. Tap forever.</h2></div>
<p class="lead">Many review products charge you every month. Ours don't. You buy the plate once and it just keeps working: no battery, no charging, no renewals.</p></div>
{stats}
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">How it works</span><h2>Three steps. Zero fuss.</h2></div>
<p class="lead">You send us your link. We program it into your plate. Your customers just tap.</p></div>
<div class="steps">
<article class="step reveal"><div class="step-top"><span class="step-icon">{icon("link",34,1.8)}</span><span class="step-num">01</span></div><h3>Copy your review link</h3><p>In your Google Business Profile, tap “Get more reviews” and copy the link it gives you.</p></article>
<article class="step reveal d1"><div class="step-top"><span class="step-icon">{icon("lock",34,1.8)}</span><span class="step-num">02</span></div><h3>We program and lock it</h3><p>Send it to us when you activate. We program it into your plate's secure chip and lock it in.</p></article>
<article class="step feature reveal d2"><div class="step-top"><span class="step-icon">{icon("phoneTap",34,1.8)}</span><span class="step-num">03</span></div><h3>Customers tap, you get reviews</h3><p>Any iPhone or Android phone opens your review page with one tap. Unlimited taps, forever.</p></article>
</div></div></section>

<section class="section flush-top"><div class="wrap"><div class="benefits">
<div class="benefit reveal"><span class="b-ico">{icon("smile",26)}</span><div><h3>No more awkward asking</h3><p>The plate does the asking. Your team just points to it with a smile.</p></div></div>
<div class="benefit reveal d1"><span class="b-ico">{icon("zap",26)}</span><div><h3>Catch them while they're happy</h3><p>Reviews happen at the counter, not “later”, which is when they get forgotten.</p></div></div>
<div class="benefit reveal d2"><span class="b-ico">{icon("phoneTap",26)}</span><div><h3>iPhone and Android</h3><p>Our advanced NFC chips work with both, so no customer gets left out.</p></div></div>
<div class="benefit reveal d3"><span class="b-ico">{icon("shield",26)}</span><div><h3>Secure and tamper-proof</h3><p>Your link is locked into a high-security chip, so nobody can redirect your customers.</p></div></div>
</div></div></section>

<section class="section-tight flush-top" aria-label="Industries we serve">
<div class="wrap" style="text-align:center"><span class="eyebrow">Made for every kind of local business</span></div>
<div class="marquee reverse" style="margin-top:26px"><div class="marquee-track" style="--dur:55s">{industries}{industries}</div></div>
</section>

<section class="section"><div class="wrap split">
<div class="reveal d1 order-first"><div class="photo gloss" data-tilt><img src="assets/img/family.webp" alt="Tap Trench Google review plate and menu tap plates" width="2000" height="1400" loading="lazy"></div></div>
<div class="reveal">
<span class="eyebrow">For cafés and restaurants</span>
<h2>Your menu, one tap away.</h2>
<p class="lead">Put a Menu Tile or Menu Disc on every table. Guests tap to open your menu or ordering page, and you never reprint a paper menu again.</p>
<ul class="checklist"><li>{icon("check",22)}<span>Square Menu Tile or round Menu Disc to suit any table</span></li><li>{icon("check",22)}<span>Works with any online menu or ordering system</span></li><li>{icon("check",22)}<span>Wipe-clean glossy finish built for hospitality</span></li></ul>
<a class="btn btn-primary" style="margin-top:28px" href="shop.html#menus">Shop menu plates {icon("arrow",18)}</a>
</div></div></section>

{cta("Ready to get in the trenches?", "Already ordered? Activate your product and we'll program your plates with your link.")}
""")

# ---- Shop
bch, bld = bc([("Home", "index.html"), ("Shop", None)], "shop.html")
itemlist = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "url": abs_url(product_url(p)), "name": full_name(p)} for i, p in enumerate(PRODUCTS)]}
add("shop.html", {"title": "Shop NFC Review & Menu Tap Plates | Tap Trench",
                  "desc": "Shop Tap Trench NFC tap plates: Star Tile Google review plate, Menu Tile and Menu Disc tap-to-order menu plates. iPhone and Android, built for life, no subscription.",
                  "active": "shop", "ld": [bld, itemlist]}, f"""
<section class="page-hero"><div class="wrap">{bch}
<h1>Shop tap plates.</h1>
<p class="lead" style="max-width:660px">Every plate is programmed with your link by our team before it ships. Demand is high: when a batch sells out, join the waitlist and we'll reserve yours from the next run.</p>
</div></section>
<section class="section flush-top" id="menus"><div class="wrap">
<div class="shop-bar"><div class="filters" role="group" aria-label="Filter products">
<button class="chip" type="button" data-filter="all" aria-pressed="true">All plates</button>
<button class="chip" type="button" data-filter="review" aria-pressed="false">Review plates</button>
<button class="chip" type="button" data-filter="menu" aria-pressed="false">Menu plates</button></div>
<span class="muted" style="font-size:15px">{len(PRODUCTS)} products · more coming soon</span></div>
<div class="products">{''.join(pcard(p, i) for i, p in enumerate(PRODUCTS))}</div>
</div></section>
<section class="section-tight flush-top"><div class="wrap"><div class="trust-row" style="max-width:900px;margin:0 auto">
<div>{icon("truck",24)}Free shipping in Australia, worldwide delivery</div><div>{icon("shield",24)}Built for life</div><div>{icon("dollar",24)}No monthly subscription</div></div></div></section>
{cta("Need plates for several venues?", "Talk to us about bulk orders, or about reselling Tap Trench.", ("contact.html", "Contact us"), ("reseller.html", "Become a Reseller"))}
""")

# ---- Product pages
for p in PRODUCTS:
    path = product_url(p)
    bch, bld = bc([("Home", "index.html"), ("Shop", "shop.html"), (full_name(p), None)], path)
    prod_ld = {"@context": "https://schema.org", "@type": "Product", "name": full_name(p), "sku": p["slug"],
               "image": [abs_url(img(p, n)) for n in range(1, 5)], "description": p["description"],
               "brand": {"@type": "Brand", "name": "Tap Trench"}, "category": "NFC tap plate",
               "offers": {"@type": "Offer", "url": abs_url(path), "priceCurrency": "AUD", "price": str(p["price"]),
                          "availability": "https://schema.org/OutOfStock", "itemCondition": "https://schema.org/NewCondition",
                          "seller": {"@type": "Organization", "name": "Tap Trench"},
                          "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "AUD"},
                                              "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "AU"}}}}
    ON, LAZY = ' class="on"', ' loading="lazy"'
    gallery = "".join(f'<img{ON if n == 1 else ""} src="{img(p,n)}" alt="{E(p["alts"][n-1])}" width="1400" height="1400"{"" if n == 1 else LAZY}>' for n in range(1, 5))
    thumbs = "".join(f'<button type="button" data-thumb aria-label="Show image {n}" aria-current="{"true" if n == 1 else "false"}"><img src="{img(p,n,True)}" alt="" width="700" height="700" loading="lazy"></button>' for n in range(1, 5))
    feats = "".join(f"<li>{E(f)}</li>" for f in p["features"])
    opens = "your Google review page" if p["cat"] == "review" else "your online menu or ordering page"
    others = [q for q in PRODUCTS if q is not p]
    add(path, {"title": f"{p['name']} | {p['kind']} ({p['variant']}) | Tap Trench",
               "desc": f"{p['name']}, the {p['kind'].lower()} ({p['variant'].lower()}) by Tap Trench. {p['short']} iPhone and Android, built for life, no subscription. {p['sold']} sold.",
               "active": "shop", "ld": [prod_ld, bld], "og": img(p, 1), "ogtype": "product"}, f"""
<section class="section" style="padding-top:36px"><div class="wrap pdp">
<div><div class="gallery-main gloss" data-gallery tabindex="0" aria-label="Product images, swipe or use arrow keys">{gallery}<div class="badges"><span class="badge sold">Sold out</span></div></div>
<div class="thumbs">{thumbs}</div></div>
<div class="pdp-info">
{bch}
<span class="kind">{E(p['kind'])} · {p['variant']}</span>
<h1>{E(p['name'])}</h1>
<div class="trust-line" style="margin:0">{stars()}<span><b style="color:var(--tt-ink)">5.0</b> · {p['sold']} sold</span></div>
<div class="pdp-price"><b>${p['price']} AUD</b><s>${p['compare']}</s><span class="pill">Save {save(p)}%</span></div>
<p class="muted" style="font-size:15px;margin-top:-8px">One-off payment · no subscription</p>
<p class="lead" style="font-size:18px">{E(p['description'])}</p>
<div class="soldout-box">{icon("bell",22)}<div><b>Sold out due to high demand</b><span class="muted" style="font-size:15px">Our last batch sold out. Join the waitlist to reserve yours from the next production run.</span></div></div>
<button class="btn btn-copper btn-block btn-shine" type="button" data-waitlist="{E(full_name(p))}">{icon("bell",18)} Notify me when it's back</button>
<div class="pay-label">{icon("lock",14)} Secure checkout with</div>
<div class="pay-row">{PAY_ROW}</div>
<div class="trust-row"><div>{icon("truck",22)}Ships worldwide</div><div>{icon("shield",22)}Built for life</div><div>{icon("phoneTap",22)}iPhone &amp; Android</div></div>
<div class="acc">
<details open><summary>What you get</summary><div class="acc-body"><ul>{feats}</ul></div></details>
<details><summary>Specifications</summary><div class="acc-body"><table class="spec"><tr><th scope="row">Shape</th><td>{p['variant']}</td></tr><tr><th scope="row">Opens</th><td>{opens[0].upper() + opens[1:]}</td></tr><tr><th scope="row">Technology</th><td>High-security NFC chip, programmed and locked by Tap Trench</td></tr><tr><th scope="row">Works with</th><td>iPhone and Android phones</td></tr><tr><th scope="row">Finish</th><td>Glossy domed, wipe-clean</td></tr><tr><th scope="row">Power</th><td>None needed, powered by the tap</td></tr><tr><th scope="row">Durability</th><td>Built for life, sealed under an epoxy dome</td></tr><tr><th scope="row">Subscription</th><td>None</td></tr></table></div></details>
<details><summary>How activation works</summary><div class="acc-body">After you order, send us your link through the <a href="activate.html">Activate your product</a> page. {"For reviews, open your Google Business Profile, tap “Get more reviews” and copy the link." if p["cat"] == "review" else "Use the link to your online menu or ordering page."} Our team programs it into your plate's secure chip and locks it, so it's ready to use the moment it arrives.</div></details>
<details><summary>Shipping &amp; returns</summary><div class="acc-body">Free shipping in Australia and delivery worldwide. Because each chip is locked to your business, unused plates can't be returned. <a href="shipping.html">Shipping</a> · <a href="returns.html">Returns &amp; product care</a></div></details>
</div>
</div></div></section>

<section class="section dark"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Why it works</span><h2>The plate does the asking.</h2></div><p class="lead">Your customer taps. {opens[0].upper() + opens[1:]} opens. That's it.</p></div>
<div class="steps">
<article class="step reveal"><div class="step-top"><span class="step-icon">{icon("counter",32,1.8)}</span></div><h3>Place it</h3><p>Counter, table, door or by the till.</p></article>
<article class="step reveal d1"><div class="step-top"><span class="step-icon">{icon("phoneTap",32,1.8)}</span></div><h3>They tap</h3><p>Any iPhone or Android phone, no app.</p></article>
<article class="step reveal d2"><div class="step-top"><span class="step-icon">{icon("infinity",32,1.8)}</span></div><h3>Forever</h3><p>Unlimited taps, no monthly fees.</p></article>
</div></div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Complete the setup</span><h2>You might also like</h2></div></div>
<div class="products">{''.join(pcard(q, i) for i, q in enumerate(others))}</div>
</div></section>
""")

# ---- How it works
bch, bld = bc([("Home", "index.html"), ("How it works", None)], "how-it-works.html")
howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "How to set up a Tap Trench Google Review plate",
         "step": [{"@type": "HowToStep", "name": n, "text": t} for n, t in [
             ("Order your plate", "Choose a Google Review Tap Plate or a Tap-to-Order Menu Plate from the Tap Trench shop."),
             ("Copy your Google review link", "Open your Google Business Profile, tap 'Get more reviews' and copy the link."),
             ("Send it to us", "Submit the link on the Activate your product page."),
             ("We program and lock your plate", "An authorised Tap Trench technician programs the link into the secure chip and locks it."),
             ("Customers tap", "Customers tap the plate with an iPhone or Android phone to open your review page.")]]}
add("how-it-works.html", {"title": "How Tap Trench NFC Review Plates Work | Tap Trench",
                          "desc": "How Tap Trench works: copy your Google review link, send it to us, and we program and lock it into your NFC plate. Customers tap with iPhone or Android to leave a review.",
                          "active": "how", "ld": [bld, howto]}, f"""
<section class="page-hero"><div class="wrap">{bch}
<h1>Simple for you. Simpler for your customers.</h1>
<p class="lead" style="max-width:680px">You don't program anything yourself. Send us your link, our team sets up your plate and locks it in, and from then on your customers just tap.</p>
</div></section>

<section class="section flush-top"><div class="wrap split">
<div class="reveal"><ol class="timeline">
<li><div><h3>Order your plate</h3><p>Pick a review plate, a menu plate or both from the <a href="shop.html">shop</a>.</p></div></li>
<li><div><h3>Copy your Google review link</h3><p>Open your Google Business Profile, tap “Get more reviews” and copy the link it gives you. For a menu plate, copy the link to your online menu or ordering page.</p>
<div class="path"><span>Google Business Profile</span>{icon("arrow",14)}<span>Get more reviews</span>{icon("arrow",14)}<span>Copy link</span></div></div></li>
<li><div><h3>Send it to us</h3><p>Share the link on our <a href="activate.html">Activate your product</a> page along with your order details.</p></div></li>
<li><div><h3>We program and lock it</h3><p>An authorised Tap Trench technician programs your link into the plate's high-security chip and locks it, so it can't be changed or tampered with.</p></div></li>
<li><div><h3>Customers tap. Forever.</h3><p>Place the plate on your counter or table. Every tap opens your page instantly, with no limit and no monthly fee.</p></div></li>
</ol></div>
<div class="reveal d2"><div class="photo" data-tilt><img src="assets/img/products/review-square-2.webp" alt="Customer tapping a Tap Trench plate with a phone" width="1400" height="1400" loading="lazy"></div></div>
</div></section>

<section class="section dark"><div class="wrap split">
<div class="reveal"><span class="eyebrow">For your customers</span>
<h2>One tap. Straight to your review page.</h2>
<p class="lead">When a customer taps your review plate, your Google review page opens immediately. They choose their stars, write their review in their own words and post it.</p>
<ul class="checklist"><li>{icon("check",22)}<span>No app to download</span></li><li>{icon("check",22)}<span>No searching for your business on Google</span></li><li>{icon("check",22)}<span>Works on iPhone and Android with our advanced NFC chips</span></li></ul></div>
<div class="reveal d2"><div class="photo"><img src="assets/img/products/menu-square-3.webp" alt="Tap Trench menu plate on a counter" width="1400" height="1400" loading="lazy"></div></div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Built to last</span><h2>Set once. Works forever.</h2></div></div>
<div class="benefits">
<div class="benefit reveal"><span class="b-ico">{icon("lock",26)}</span><div><h3>Locked for security</h3><p>Your link is locked into a high-security chip, so nobody can redirect your customers somewhere else.</p></div></div>
<div class="benefit reveal d1"><span class="b-ico">{icon("infinity",26)}</span><div><h3>Unlimited taps</h3><p>There's no tap limit and no expiry. Use it as many times as your customers like.</p></div></div>
<div class="benefit reveal d2"><span class="b-ico">{icon("dollar",26)}</span><div><h3>No subscription</h3><p>Many major players charge a monthly fee. You pay once for a Tap Trench plate.</p></div></div>
<div class="benefit reveal d3"><span class="b-ico">{icon("shield",26)}</span><div><h3>Built for life</h3><p>No battery to run flat and nothing to charge. The chip is sealed under a tough epoxy dome.</p></div></div>
</div></div></section>
{cta("Got your plates?", "Send us your link and we'll get them working.")}
""")

# ---- Activate
bch, bld = bc([("Home", "index.html"), ("Activate your product", None)], "activate.html")
add("activate.html", {"title": "Activate Your Tap Trench Product | Tap Trench",
                      "desc": "Activate your Tap Trench NFC plate. Send us your Google review link or menu link and our team will program and lock it into your plate.",
                      "active": "", "ld": [bld]}, f"""
<section class="page-hero" style="padding-bottom:16px"><div class="wrap">{bch}</div></section>
<section class="section flush-top"><div class="wrap form-layout">
<div>
<span class="eyebrow">Activate</span>
<h1 style="font-size:clamp(40px,5.4vw,70px);font-weight:800;letter-spacing:-.04em;margin:16px 0">Activate your product.</h1>
<p class="lead">Bought a Tap Trench plate? Fill in the form with your order details and your link. Our authorised team programs it into your plate's secure chip and locks it in.</p>
<ol class="timeline" style="margin-top:30px">
<li><div><h3>Copy your review link</h3><p>Google Business Profile → “Get more reviews” → copy the link. For menu plates, copy your online menu link.</p></div></li>
<li><div><h3>Submit the form</h3><p>Include your order number, business name and the link.</p></div></li>
<li><div><h3>We program and lock it</h3><p>Your plate is set up permanently, ready for unlimited taps.</p></div></li>
</ol>
<div class="notice"><b>Please double-check your link.</b> Once it's programmed, it's locked for security and can't be changed.</div>
</div>
<div class="form-frame" data-form="activate" data-form-title="Activate my Tap Trench product"></div>
</div></section>
""")

# ---- Reseller
bch, bld = bc([("Home", "index.html"), ("Become a Reseller", None)], "reseller.html")
add("reseller.html", {"title": "Become a Tap Trench Reseller | Sell NFC Review Plates",
                      "desc": "Become a Tap Trench reseller. Sell NFC review and menu tap plates to the businesses you work with. Get in touch to find out more.",
                      "active": "reseller", "ld": [bld]}, f"""
<section class="page-hero"><div class="wrap">{bch}
<span class="eyebrow" style="margin-top:20px">Reseller program</span>
<h1>Sell Tap Trench to the businesses you know.</h1>
<p class="lead" style="max-width:680px">Local businesses want more reviews and easier menus. You bring the customers, we handle production and programming. Get in touch and we'll talk you through how it works.</p>
<div class="hero-ctas"><a class="btn btn-primary btn-shine" href="#apply">Apply to become a reseller</a></div>
</div></section>

<section class="section flush-top"><div class="wrap"><div class="benefits">
<div class="benefit reveal"><span class="b-ico">{icon("tag",26)}</span><div><h3>Reseller pricing</h3><p>Contact us for reseller pricing.</p></div></div>
<div class="benefit reveal d1"><span class="b-ico">{icon("lock",26)}</span><div><h3>We do the programming</h3><p>Send us your customers' links and we program and lock every plate before it ships.</p></div></div>
<div class="benefit reveal d2"><span class="b-ico">{icon("megaphone",26)}</span><div><h3>Sales support</h3><p>Product photos and talking points to help you pitch to local businesses.</p></div></div>
<div class="benefit reveal d3"><span class="b-ico">{icon("dollar",26)}</span><div><h3>An easy sell</h3><p>No subscription and built for life, so it's a simple yes for business owners.</p></div></div>
</div></div></section>

<section class="section dark"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">How it works</span><h2>Three steps to your first sale.</h2></div></div>
<div class="steps">
<article class="step reveal"><div class="step-top"><span class="step-icon">{icon("users",32,1.8)}</span><span class="step-num">01</span></div><h3>Apply</h3><p>Tell us about you and the businesses you work with.</p></article>
<article class="step reveal d1"><div class="step-top"><span class="step-icon">{icon("box",32,1.8)}</span><span class="step-num">02</span></div><h3>Order at wholesale</h3><p>Order plates for your customers with their links.</p></article>
<article class="step reveal d2"><div class="step-top"><span class="step-icon">{icon("dollar",32,1.8)}</span><span class="step-num">03</span></div><h3>Sell and earn</h3><p>Deliver to your customers and keep the difference.</p></article>
</div></div></section>

<section class="section" id="apply"><div class="wrap form-layout">
<div><span class="eyebrow">Apply</span><h2 style="font-size:clamp(34px,4.4vw,54px);font-weight:800;margin:14px 0 16px">Apply to resell.</h2>
<p class="lead">Fill in the form, or email us at <a href="mailto:{SITE['email']}">{SITE['email']}</a>, and our team will be in touch.</p>
<div class="perks"><div><b>Who it's for</b><span class="muted">Marketing agencies, web designers, POS and signage suppliers, and local business consultants.</span></div><div><b>Where</b><span class="muted">Anywhere in the world.</span></div></div></div>
<div class="form-frame" data-form="reseller" data-form-title="Tap Trench reseller application"></div>
</div></section>
""")

# ---- About
bch, bld = bc([("Home", "index.html"), ("About", None)], "about.html")
add("about.html", {"title": "About Tap Trench | In the Trenches With You",
                   "desc": "Tap Trench makes NFC tap plates that help local businesses get more Google reviews and serve menus with one tap. No subscription, built for life.",
                   "active": "about", "ld": [bld, ORG]}, f"""
<section class="page-hero"><div class="wrap">{bch}
<span class="eyebrow" style="margin-top:20px">Our story</span>
<h1>We're in the trenches with you.</h1>
<p class="lead" style="max-width:700px">Running a local business means doing a hundred jobs at once. Chasing reviews shouldn't be one of them. We built Tap Trench so the people behind the counter can focus on their customers, and let a small plate quietly do the asking.</p>
</div></section>
<section class="section flush-top"><div class="wrap split">
<div class="reveal"><h2>Small plate. Big difference.</h2>
<p class="lead">Most happy customers are glad to leave a review. They just never get around to it. Tap Trench closes that gap with one tap, right there at the counter.</p>
<p class="lead" style="margin-top:14px">And we think you should own what you buy. That's why there's no subscription: you pay once, and your plate keeps working.</p></div>
<div class="reveal d2"><div class="photo gloss" data-tilt><img src="assets/img/family.webp" alt="Tap Trench review and menu plates" width="2000" height="1400" loading="lazy"></div></div>
</div></section>
<section class="section dark"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">What we stand for</span><h2>How we work.</h2></div></div>
{stats}
<div class="steps" style="margin-top:48px">
<article class="step reveal"><div class="step-top"><span class="step-icon">{icon("smile",32,1.8)}</span></div><h3>Plain and simple</h3><p>No apps, no dashboards, no jargon. Tap and done.</p></article>
<article class="step reveal d1"><div class="step-top"><span class="step-icon">{icon("lock",32,1.8)}</span></div><h3>Secure by design</h3><p>Links are programmed and locked by our team, so they can't be tampered with.</p></article>
<article class="step reveal d2"><div class="step-top"><span class="step-icon">{icon("shield",32,1.8)}</span></div><h3>Built to last</h3><p>Built for life, unlimited taps and no monthly fees.</p></article>
</div></div></section>
{cta("Let's get to work.", "Shop the range, or activate the plates you've already ordered.")}
""")

# ---- FAQ
bch, bld = bc([("Home", "index.html"), ("FAQs", None)], "faq.html")
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, qs in FAQ for q, a in qs]}
faq_html = ""
for i, (sec, qs) in enumerate(FAQ):
    sid = ["how", "setup", "orders"][i]
    faq_html += f'<div id="{sid}" class="reveal"><h2 style="font-size:32px;margin-bottom:10px">{sec}</h2><div class="acc">' + "".join(
        f"<details><summary>{E(q)}</summary><div class=\"acc-body\">{E(a)}</div></details>" for q, a in qs) + "</div></div>"
add("faq.html", {"title": "FAQs: NFC Google Review Plates | Tap Trench",
                 "desc": "Answers about Tap Trench NFC review and menu plates: iPhone and Android compatibility, getting your Google review link, activation, durability and no subscription.",
                 "active": "faq", "ld": [bld, faq_ld]}, f"""
<section class="page-hero"><div class="wrap">{bch}
<h1>Questions, answered.</h1>
<p class="lead" style="max-width:620px">Can't find what you're after? <a href="contact.html">Get in touch</a> and a real person will reply within one business day.</p>
</div></section>
<section class="section flush-top"><div class="wrap" style="max-width:900px;display:flex;flex-direction:column;gap:48px">{faq_html}</div></section>
{cta("Still have questions?", "Talk to our team. We're happy to help.", ("contact.html", "Contact us"), ("shop.html", "Shop the range"))}
""")

# ---- Contact
bch, bld = bc([("Home", "index.html"), ("Contact", None)], "contact.html")
phone_card = f'<a class="contact-card" href="tel:{SITE["phone"].replace(" ","")}"><span class="ci">{icon("phone")}</span><span><small>Phone</small><b>{E(SITE["phone"])}</b></span></a>' if SITE["phone"] else ""
add("contact.html", {"title": "Contact Tap Trench",
                     "desc": "Contact the Tap Trench team about NFC review plates, menu plates, bulk orders or reselling. We reply within one business day.",
                     "active": "contact", "ld": [bld]}, f"""
<section class="page-hero" style="padding-bottom:16px"><div class="wrap">{bch}</div></section>
<section class="section flush-top"><div class="wrap form-layout">
<div><span class="eyebrow">Contact us</span>
<h1 style="font-size:clamp(40px,5.4vw,70px);font-weight:800;letter-spacing:-.04em;margin:16px 0">Talk to a real person.</h1>
<p class="lead">Questions about our plates, bulk orders or activation? Send us a message and we'll get back to you within one business day.</p>
<div class="contact-cards">
<a class="contact-card" href="mailto:{SITE['email']}"><span class="ci">{icon("mail")}</span><span><small>Email</small><b>{SITE['email']}</b></span></a>
{phone_card}
<div class="contact-card"><span class="ci">{icon("clock")}</span><span><small>Hours</small><b>{E(SITE['hours'])}</b></span></div>
<div class="contact-card"><span class="ci">{icon("pin")}</span><span><small>Based in</small><b>{E(SITE['address'])}</b></span></div>
</div>
<p class="muted" style="margin-top:24px;font-size:15px">Already ordered? <a href="activate.html">Activate your product</a>. Interested in reselling? Just email us.</p></div>
<div class="form-frame" data-form="contact" data-form-title="Tap Trench contact enquiry"></div>
</div></section>
""")

# ---- Shipping
bch, bld = bc([("Home", "index.html"), ("Shipping", None)], "shipping.html")
add("shipping.html", {"title": "Shipping | Tap Trench", "desc": "Free shipping in Australia and delivery worldwide on Tap Trench NFC plates. Each plate is programmed with your link before dispatch.",
                      "active": "", "ld": [bld]}, f"""
<section class="page-hero"><div class="wrap">{bch}<h1>Shipping.</h1><p class="lead" style="max-width:620px">Free shipping across Australia, and we deliver worldwide.</p></div></section>
<section class="section flush-top"><div class="wrap">
<div class="benefits" style="margin-bottom:52px">
<div class="benefit"><span class="b-ico">{icon("truck",26)}</span><div><h3>Free shipping in Australia</h3><p>On every order, no minimum spend. We also ship worldwide.</p></div></div>
<div class="benefit"><span class="b-ico">{icon("lock",26)}</span><div><h3>Programmed before dispatch</h3><p>We program and lock your link into each plate before it ships.</p></div></div>
</div>
<div class="prose">
<h2>Processing times</h2><p>Once we have your link from the <a href="activate.html">Activate your product</a> form, we program your plates and dispatch them, usually within a few business days. Delivery within Australia then takes around 3–7 business days. International delivery times vary by country.</p>
<h2>Sold-out products and the waitlist</h2><p>When a product is sold out you can join the waitlist. We'll contact you before the next batch is ready to confirm your order. Joining the waitlist doesn't commit you to buy.</p>
<h2>Tracking</h2><p>You'll receive a tracking link by email as soon as your order ships.</p>
<h2>International orders</h2><p>We ship worldwide. International shipping costs and delivery times depend on your country and are confirmed before you pay. Any import duties or taxes are set by your country and payable on delivery.</p>
<h2>Lost or damaged parcels</h2><p>If your parcel arrives damaged or hasn't arrived within 10 business days of dispatch, <a href="contact.html">get in touch</a> and we'll sort it out.</p>
</div></div></section>
""")

# ---- Returns & product care
bch, bld = bc([("Home", "index.html"), ("Returns & product care", None)], "returns.html")
add("returns.html", {"title": "Returns & Product Care | Tap Trench",
                     "desc": "Tap Trench NFC plates are built for life, with no battery and no subscription. Plates are locked to your business, so unused plates can't be returned.",
                     "active": "", "ld": [bld]}, f"""
<section class="page-hero"><div class="wrap">{bch}<h1>Built for life.</h1><p class="lead" style="max-width:640px">Pay once and your plate just keeps working. No battery, no charging, no subscription.</p></div></section>
<section class="section flush-top"><div class="wrap">
<div class="benefits" style="margin-bottom:52px">
<div class="benefit"><span class="b-ico">{icon("shield",26)}</span><div><h3>Built for life</h3><p>The chip needs no battery and is sealed under a tough epoxy dome, so there's nothing to wear out.</p></div></div>
<div class="benefit"><span class="b-ico">{icon("dollar",26)}</span><div><h3>No subscription, ever</h3><p>Many major players charge every month to keep their products working. We don't.</p></div></div>
</div>
<div class="prose">
<h2>Caring for your plate</h2><p>Wipe it with a soft damp cloth. Avoid harsh solvents, scraping, heat and bending, and keep it away from metal surfaces, which can block the tap.</p>
<h2>Returns</h2><p>Each plate contains a high-security chip that is programmed and locked to your business. Because it can't be reprogrammed for anyone else, <strong>we can't accept returns of unused plates</strong> or change-of-mind returns.</p>
<p>Please check your link carefully before submitting it on the <a href="activate.html">Activate your product</a> page.</p>
<h2>Damaged on arrival</h2><p>If your plate arrives damaged or doesn't work when it arrives, email <a href="mailto:{SITE['email']}">{SITE['email']}</a> with your order number and a photo, and we'll make it right.</p>
<h2>Need another plate?</h2><p>Want a plate for a second location, another counter or a different link? Simply <a href="shop.html">order another one</a>.</p>
</div></div></section>
""")

# ---- Privacy
bch, bld = bc([("Home", "index.html"), ("Privacy", None)], "privacy.html")
add("privacy.html", {"title": "Privacy Policy | Tap Trench", "desc": "How Tap Trench collects, uses and protects your personal information.", "active": "", "ld": [bld]}, f"""
<section class="page-hero"><div class="wrap">{bch}<h1>Privacy policy.</h1><p class="muted">Last updated: {TODAY}</p></div></section>
<section class="section flush-top"><div class="wrap prose">
<p>Tap Trench (“we”, “us”) respects your privacy. This policy explains what personal information we collect, why, and how you can access or correct it.</p>
<h2>What we collect</h2><ul><li><strong>Information you give us</strong>: your name, business name, email, phone, address and the links you ask us to program, when you activate a product, join a waitlist, apply as a reseller, contact us or place an order.</li><li><strong>Website analytics</strong>: basic, aggregated information about how this website is used.</li></ul>
<h2>Forms</h2><p>Our contact, activation, reseller and waitlist forms are provided by Google Forms. Information you submit through them is processed by Google on our behalf and is subject to <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's Privacy Policy</a>.</p>
<h2>How we use it</h2><ul><li>To program and deliver your plates</li><li>To respond to enquiries and reseller applications</li><li>To let you know when waitlisted products are available</li><li>To send product updates and offers, if you've agreed (you can unsubscribe anytime)</li></ul>
<h2>Sharing</h2><p>We don't sell your personal information. We share it only with service providers who help us run our business (such as payment, shipping, email and form providers), or where required by law.</p>
<h2>Access and correction</h2><p>Ask to see or correct the personal information we hold about you by emailing <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
<h2>Complaints</h2><p>If you have a privacy concern, email us at <a href="mailto:{SITE['email']}">{SITE['email']}</a> and we'll respond within 30 days.</p>
</div></section>
""")

# ---- Terms
bch, bld = bc([("Home", "index.html"), ("Terms", None)], "terms.html")
add("terms.html", {"title": "Terms of Use | Tap Trench", "desc": "Terms of use for the Tap Trench website and NFC tap plates.", "active": "", "ld": [bld]}, f"""
<section class="page-hero"><div class="wrap">{bch}<h1>Terms of use.</h1><p class="muted">Last updated: {TODAY}</p></div></section>
<section class="section flush-top"><div class="wrap prose">
<h2>Products and orders</h2><p>Prices are in Australian dollars and include GST where applicable. Joining a waitlist does not create an order or any obligation to buy.</p>
<h2>Programming and locked links</h2><p>We program each plate with the link you provide and lock it for security. You're responsible for making sure the link is correct and points to lawful content. Once programmed, a plate's link can't be changed.</p>
<h2>Reviews</h2><p>Tap Trench review plates open your review page so customers can leave their own reviews. You must not offer incentives for reviews or use our products in a way that breaks the rules of the review platform you link to.</p>
<h2>Resellers</h2><p>Reseller pricing and terms are provided separately on approval of a reseller application.</p>
<h2>Customer showcase</h2><p>By activating a Tap Trench product, you allow Tap Trench to display your business name and logo on our website and marketing materials to show you as a customer. You can withdraw this permission at any time by emailing <a href="mailto:{SITE['email']}">{SITE['email']}</a>, and we'll remove it from our website within 14 days.</p>
<h2>Trademarks</h2><p>Tap Trench and its logo are our trademarks. {E(SITE['trademark'])}</p>
<h2>Your rights</h2><p>Nothing in these terms limits any rights you have under the consumer laws of your country.</p>
<h2>Governing law</h2><p>Tap Trench is based in Sydney, Australia, and these terms are governed by the laws of New South Wales. If something goes wrong, please email us first and we'll work with you to put it right.</p>
</div></section>
""")

# ---- 404
add("404.html", {"title": "Page not found | Tap Trench", "desc": "This page doesn't exist.", "active": "", "noindex": True}, f"""
<section class="section"><div class="wrap" style="text-align:center;display:flex;flex-direction:column;align-items:center;gap:20px">
<span class="eyebrow">Error 404</span><h1 style="font-size:clamp(52px,10vw,130px);font-weight:800;letter-spacing:-.05em">Lost in the trench.</h1>
<p class="lead" style="max-width:520px">That page doesn't exist, but we're still here with you.</p>
<div class="hero-ctas" style="justify-content:center"><a class="btn btn-primary" href="index.html">Back home</a><a class="btn btn-ghost" href="shop.html">Visit the shop</a></div>
</div></section>""")

# ---------------------------------------------------------------- write
for path, content in PAGES.items():
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(content)

prio = {"index.html": "1.0", "shop.html": "0.9"}
urls = "".join(f"<url><loc>{abs_url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(p, '0.8' if p.endswith('plate-square.html') or p.endswith('plate-round.html') or p.startswith('google') else '0.6')}</priority></url>\n"
               for p in PAGES if p != "404.html")
open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {abs_url('sitemap.xml')}\n")
print("built", len(PAGES), "pages")
