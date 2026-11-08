#!/usr/bin/env python3
"""
Halif Auto Repair and Collision — static site builder.

Assembles the final .html files in Html-File/ from:
  _build/pages/*.html   page bodies + front matter
  _build/build.py       shared shell: head, header, footer, schema

Run:  python3 _build/build.py          (from the Html-File directory)

-----------------------------------------------------------------------------
 BEFORE LAUNCH: set SITE_URL below to the real domain.
 It is the only place the domain is written. Everything else (canonical tags,
 Open Graph URLs, sitemap.xml, robots.txt, llms.txt, JSON-LD) is derived
 from it.
-----------------------------------------------------------------------------
"""

import os
import re
import json
import datetime

# ---------------------------------------------------------------- site config

SITE_URL = "https://www.halifautorepair.ca"      # <-- PLACEHOLDER: set real domain
BUSINESS  = "Halif Auto Repair and Collision"
SHORT     = "Halif"
STREET    = "105 Ash St"
CITY      = "Whitby"
REGION    = "ON"
POSTAL    = "L1N 4B1"
COUNTRY   = "CA"
PHONE_TXT = "905-730-6089"
PHONE_TEL = "+19057306089"
LAT, LNG  = 43.8809397, -78.9390969
INSTAGRAM = "https://www.instagram.com/halifauto.repair/"
GOOGLE    = "https://share.google/MVxRX56wkRWIUuZFp"
GMAPS     = ("https://www.google.com/maps/place/Halif+Auto+Repair+and+Collision/"
             "@43.8809397,-78.9390969,17z")
DIRECTIONS = "https://www.google.com/maps/dir/?api=1&destination=105+Ash+St,+Whitby,+ON+L1N+4B1"
RATING, REVIEW_COUNT = "5.0", "10"
UPDATED   = "November 2026"
YEAR      = "2026"

SMS_BODY = ("Hi%20Halif%2C%20I%27d%20like%20a%20photo%20estimate.%20"
            "Here%20are%20photos%20of%20the%20damage.%20My%20vehicle%20is%3A%20")
SMS  = f"sms:{PHONE_TEL}?&body={SMS_BODY}"
WA   = f"https://wa.me/19057306089?text={SMS_BODY}"
TEL  = f"tel:{PHONE_TEL}"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(ROOT, "_build", "pages")

# ---------------------------------------------------------------- navigation

SERVICES = [
    ("collision-repair.html",           "Collision repair"),
    ("auto-body-repair.html",           "Auto body &amp; bumper repair"),
    ("auto-paint-colour-matching.html", "Paint &amp; colour matching"),
    ("dent-scratch-repair.html",        "Dents &amp; scratches"),
    ("rust-repair.html",                "Rust repair"),
    ("insurance-claims.html",           "Insurance claims"),
]

NAV = [
    ("index.html",        "Home",            []),
    ("services.html",     "Services",        [("services.html", "All services")] + SERVICES),
    ("insurance-claims.html", "Insurance claims", []),
    ("about.html",        "About",           [("about.html", "About Halif"),
                                              ("reviews.html", "Reviews"),
                                              ("faq.html", "FAQ")]),
    ("contact.html",      "Contact",         []),
]

HOURS_ROWS = [
    ("Monday",    "9:00 am – 5:30 pm", False),
    ("Tuesday",   "9:00 am – 5:30 pm", False),
    ("Wednesday", "9:00 am – 5:30 pm", False),
    ("Thursday",  "9:00 am – 5:30 pm", False),
    ("Friday",    "9:00 am – 5:30 pm", False),
    ("Saturday",  "9:00 am – 2:30 pm", False),
    ("Sunday",    "Closed",            True),
]

# ---------------------------------------------------------------- JSON-LD

def business_schema(page_url, with_rating=False):
    data = {
        "@context": "https://schema.org",
        "@type": "AutoBodyShop",
        "@id": f"{SITE_URL}/#business",
        "name": BUSINESS,
        "url": SITE_URL + "/",
        "image": f"{SITE_URL}/images/halif/logo-badge.png",
        "logo": f"{SITE_URL}/images/halif/logo-badge.png",
        "telephone": "+1 905-730-6089",
        "description": (
            "Halif Auto Repair and Collision is an auto body and collision repair shop "
            "at 105 Ash St in downtown Whitby, Ontario. The shop repairs collision damage, "
            "bodywork, paint and colour matching, dents, scratches and rust on cars, trucks "
            "and SUVs, and helps with insurance claims. Text or WhatsApp photos of the damage "
            "to 905-730-6089 for an estimate."),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": CITY,
            "addressRegion": REGION,
            "postalCode": POSTAL,
            "addressCountry": COUNTRY,
        },
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": GMAPS,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "09:00", "closes": "17:30"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:30"},
        ],
        "sameAs": [INSTAGRAM, GOOGLE],
        "areaServed": [
            {"@type": "City", "name": "Whitby"},
            {"@type": "City", "name": "Brooklin"},
            {"@type": "City", "name": "Oshawa"},
            {"@type": "City", "name": "Ajax"},
            {"@type": "City", "name": "Pickering"},
            {"@type": "City", "name": "Courtice"},
            {"@type": "City", "name": "Bowmanville"},
            {"@type": "AdministrativeArea", "name": "Durham Region, Ontario"},
        ],
        "currenciesAccepted": "CAD",
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
            for n in ["Collision repair", "Auto body repair", "Bumper repair",
                      "Car paint and colour matching", "Dent and scratch repair",
                      "Rust repair", "Insurance claim help"]
        ],
    }
    if with_rating:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": RATING,
            "reviewCount": REVIEW_COUNT,
            "bestRating": "5",
        }
    return data


def breadcrumb_schema(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             "item": f"{SITE_URL}/{slug}" if slug else None}
            for i, (name, slug) in enumerate(trail)
        ],
    }


def service_schema(name, description, url, service_type):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": service_type,
        "description": description,
        "url": url,
        "provider": {"@id": f"{SITE_URL}/#business"},
        "areaServed": [{"@type": "City", "name": c} for c in
                       ["Whitby", "Brooklin", "Oshawa", "Ajax", "Pickering", "Courtice", "Bowmanville"]],
        "availableChannel": {
            "@type": "ServiceChannel",
            "servicePhone": {"@type": "ContactPoint", "telephone": "+1 905-730-6089"},
            "serviceLocation": {"@id": f"{SITE_URL}/#business"},
        },
    }


def faq_schema(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "url": SITE_URL + "/",
        "name": BUSINESS,
        "inLanguage": "en-CA",
        "publisher": {"@id": f"{SITE_URL}/#business"},
    }


def jsonld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, indent=2, ensure_ascii=False)
            + '\n</script>')

# ---------------------------------------------------------------- partials

def head(page):
    url = f"{SITE_URL}/{page['slug']}" if page["slug"] != "index.html" else SITE_URL + "/"
    og_img = f"{SITE_URL}/images/halif/{page.get('og', 'og-halif')}.jpg"
    blocks = [jsonld(business_schema(url, page.get("rating", False)))]
    if page["slug"] == "index.html":
        blocks.append(jsonld(website_schema()))
    if page.get("trail"):
        blocks.append(jsonld(breadcrumb_schema(page["trail"])))
    for extra in page.get("schema", []):
        blocks.append(jsonld(extra))
    schema_html = "\n".join(blocks)

    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">

<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Whitby, Ontario">
<meta name="geo.position" content="{LAT};{LNG}">
<meta name="ICBM" content="{LAT}, {LNG}">

<meta property="og:type" content="website">
<meta property="og:locale" content="en_CA">
<meta property="og:site_name" content="{BUSINESS}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page['title']}">
<meta name="twitter:description" content="{page['desc']}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#0B0B0D">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/responsive.css">
<link rel="stylesheet" href="css/halif.css">

<link rel="apple-touch-icon" sizes="180x180" href="images/favicon/apple-touch-icon.png">
<link rel="icon" type="image/png" href="images/favicon/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="images/favicon/favicon-16x16.png" sizes="16x16">
<link rel="shortcut icon" href="images/favicon/favicon.ico">
<link rel="manifest" href="images/favicon/manifest.json">

{schema_html}
</head>
<body>
<a class="h-skip" href="#main">Skip to main content</a>
<div class="boxed_wrapper">
"""


def header(active):
    items = []
    for slug, label, children in NAV:
        cls = []
        if children:
            cls.append("dropdown")
        if active == slug or active in [c[0] for c in children]:
            cls.append("current")
        cls_attr = f' class="{" ".join(cls)}"' if cls else ""
        sub = ""
        if children:
            lis = "\n".join(
                f'                                    <li><a href="{s}">{t}</a></li>'
                for s, t in children)
            sub = f"\n                                <ul>\n{lis}\n                                </ul>\n                            "
        items.append(
            f'                            <li{cls_attr}><a href="{slug}">{label}</a>{sub}</li>')
    nav_html = "\n".join(items)

    return f"""
<!-- Top bar -->
<section class="top-bar-area">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 col-md-7 col-sm-12 col-xs-12">
                <div class="top-left">
                    <ul class="top-contact-info">
                        <li><i class="fa fa-map-marker" aria-hidden="true"></i> <a href="{DIRECTIONS}" target="_blank" rel="noopener">{STREET}, {CITY}, {REGION} {POSTAL}</a></li>
                        <li class="h-topbar-hours"><i class="fa fa-clock-o" aria-hidden="true"></i> Mon&ndash;Fri 9&nbsp;am&ndash;5:30&nbsp;pm &middot; Sat 9&nbsp;am&ndash;2:30&nbsp;pm</li>
                        <li class="h-topbar-rating"><i class="fa fa-star" aria-hidden="true"></i> {RATING} on Google</li>
                    </ul>
                </div>
            </div>
            <div class="col-lg-4 col-md-5 col-sm-12 col-xs-12">
                <div class="top-right">
                    <a class="h-topbar-phone" href="{TEL}"><i class="fa fa-phone" aria-hidden="true"></i> {PHONE_TXT}</a>
                    <ul class="social-links">
                        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Halif on Instagram"><i class="fa fa-instagram" aria-hidden="true"></i></a></li>
                        <li><a href="{GOOGLE}" target="_blank" rel="noopener" aria-label="Halif on Google"><i class="fa fa-google" aria-hidden="true"></i></a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Main menu -->
<section class="mainmenu-area stricky">
    <div class="container">
        <div class="row">
            <div class="col-lg-12 clearfix">
                <div class="logo">
                    <a href="index.html" aria-label="{BUSINESS} &mdash; home">
                        <img src="images/halif/logo-badge-160.png" width="160" height="160" alt="{BUSINESS} logo">
                        <span class="h-logo-text">
                            <b>Halif</b>
                            <span>Auto Repair and Collision</span>
                        </span>
                    </a>
                </div>
                <nav class="main-menu" aria-label="Main">
                    <div class="navbar-collapse collapse clearfix" id="halif-nav">
                        <ul class="navigation clearfix">
{nav_html}
                        </ul>
                    </div>
                </nav>
                <div class="h-header-cta">
                    <button type="button" class="navbar-toggle h-nav-toggle" data-toggle="collapse" data-target="#halif-nav" aria-controls="halif-nav" aria-expanded="false" aria-label="Open menu">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>
"""


def breadcrumb(page):
    trail = page.get("trail") or []
    crumbs = []
    for i, (name, slug) in enumerate(trail):
        last = i == len(trail) - 1
        if last:
            crumbs.append(f'<li class="active">{name}</li>')
        else:
            crumbs.append(f'<li><a href="{slug}">{name}</a></li>'
                          f'<li><i class="fa fa-angle-right" aria-hidden="true"></i></li>')
    intro = f'<p>{page["band_sub"]}</p>' if page.get("band_sub") else ""
    return f"""
<section class="breadcrumb-area" style="background-image: url(images/halif/{page.get('band', 'band-general')}.jpg);">
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="breadcrumbs">
                    <h1>{page['h1']}</h1>
                    {intro}
                </div>
            </div>
        </div>
    </div>
    <div class="breadcrumb-botton">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <ul class="left">
                        {''.join(crumbs)}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
"""


def footer():
    hours = "\n".join(
        '                            <tr><th>%s</th><td%s>%s</td></tr>'
        % (d, ' class="closed"' if closed else '', h)
        for d, h, closed in HOURS_ROWS)
    svc = "\n".join(
        f'                        <li><a href="{s}">{t}</a></li>' for s, t in SERVICES)

    return f"""
<!-- Mobile sticky action bar -->
<div class="h-sticky-bar" role="navigation" aria-label="Quick actions">
    <ul>
        <li><a class="primary" href="{SMS}"><i class="fa fa-camera" aria-hidden="true"></i> <span>Text photos</span></a></li>
        <li><a href="{WA}" target="_blank" rel="noopener"><i class="fa fa-whatsapp" aria-hidden="true"></i> WhatsApp</a></li>
        <li><a href="{TEL}"><i class="fa fa-phone" aria-hidden="true"></i> Call</a></li>
    </ul>
</div>

<footer class="footer-area">
    <div class="container">
        <div class="row">
            <div class="col-lg-4 col-md-6 col-sm-6 col-xs-12">
                <div class="single-footer-widget">
                    <div class="h-foot-logo">
                        <img src="images/halif/logo-badge-160.png" width="160" height="160" alt="{BUSINESS} logo">
                        <span>
                            <b>Halif</b>
                            <span>Auto Repair and Collision</span>
                        </span>
                    </div>
                    <p>An auto body and collision shop in downtown Whitby. Bodywork, paint and colour matching, dents, scratches, rust and insurance claims for cars, trucks and SUVs.</p>
                    <ul class="h-foot-nap">
                        <li><i class="fa fa-map-marker" aria-hidden="true"></i>
                            <span><a href="{DIRECTIONS}" target="_blank" rel="noopener">{STREET}<br>{CITY}, {REGION} {POSTAL}</a></span></li>
                        <li><i class="fa fa-phone" aria-hidden="true"></i>
                            <span><a href="{TEL}">{PHONE_TXT}</a></span></li>
                        <li><i class="fa fa-camera" aria-hidden="true"></i>
                            <span><a href="{SMS}">Text photos for an estimate</a></span></li>
                    </ul>
                    <ul class="h-foot-social">
                        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram"><i class="fa fa-instagram" aria-hidden="true"></i></a></li>
                        <li><a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa fa-whatsapp" aria-hidden="true"></i></a></li>
                        <li><a href="{GOOGLE}" target="_blank" rel="noopener" aria-label="Google listing"><i class="fa fa-google" aria-hidden="true"></i></a></li>
                    </ul>
                </div>
            </div>

            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">
                <div class="single-footer-widget">
                    <div class="title"><h3>What we fix</h3></div>
                    <ul class="h-foot-links">
{svc}
                    </ul>
                </div>
            </div>

            <div class="col-lg-2 col-md-6 col-sm-6 col-xs-12">
                <div class="single-footer-widget">
                    <div class="title"><h3>Company</h3></div>
                    <ul class="h-foot-links">
                        <li><a href="about.html">About Halif</a></li>
                        <li><a href="reviews.html">Reviews</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                        <li><a href="contact.html">Contact &amp; directions</a></li>
                        <li><a href="privacy.html">Privacy</a></li>
                    </ul>
                </div>
            </div>

            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">
                <div class="single-footer-widget">
                    <div class="title"><h3>Opening hours</h3></div>
                    <table class="h-foot-hours">
                        <tbody>
{hours}
                        </tbody>
                    </table>
                    <p class="h-service-area-line">Serving Whitby, Brooklin, Port Whitby, Oshawa, Ajax, Pickering, Courtice, Bowmanville and the rest of Durham Region.</p>
                </div>
            </div>
        </div>
    </div>
</footer>

<section class="footer-bottom-area">
    <div class="container">
        <div class="row">
            <div class="col-md-7 col-sm-12">
                <div class="copyright-text">
                    <p>&copy; {YEAR} {BUSINESS}. {STREET}, {CITY}, {REGION} {POSTAL}. All rights reserved.</p>
                </div>
            </div>
            <div class="col-md-5 col-sm-12">
                <ul class="h-legal">
                    <li><a href="privacy.html">Privacy policy</a></li>
                    <li><a href="contact.html">Contact</a></li>
                    <li><a href="{GOOGLE}" target="_blank" rel="noopener">Google listing</a></li>
                </ul>
            </div>
        </div>
    </div>
</section>

</div>

<div class="scroll-to-top scroll-to-target" data-target="html" role="button" tabindex="0" aria-label="Back to top"><span class="fa fa-chevron-circle-up" aria-hidden="true"></span></div>

<script src="js/jquery-1.11.1.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/wow.js"></script>
<script src="js/jquery.appear.js"></script>
<script src="js/jquery.easing.min.js"></script>
<script src="js/halif.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- components

def service_sidebar(active):
    items = []
    for slug, label in SERVICES:
        cls = ' class="active"' if slug == active else ""
        items.append(f'                <li{cls}><a href="{slug}">{label}</a></li>')
    links = "\n".join(items)
    return f"""<aside class="h-side">
            <nav aria-label="Services">
                <ul class="h-side-nav">
{links}
                </ul>
            </nav>
            <div class="h-side-cta">
                <h3>Not sure what it needs?</h3>
                <p>Send three photos of the damage and we will tell you what the repair involves and what it costs.</p>
                <a class="h-btn h-btn-block" href="{SMS}"><i class="fa fa-camera" aria-hidden="true"></i> <span>Text photos</span></a>
                <a class="h-btn h-btn-block h-btn-light" href="{WA}" target="_blank" rel="noopener"><i class="fa fa-whatsapp" aria-hidden="true"></i> WhatsApp photos</a>
                <a class="h-side-phone" href="{TEL}">{PHONE_TXT}</a>
                <p style="margin-top:10px;font-size:14px;">Mon&ndash;Fri 9&nbsp;am&ndash;5:30&nbsp;pm &middot; Sat 9&nbsp;am&ndash;2:30&nbsp;pm</p>
            </div>
        </aside>"""


CTA_BAND = f"""<section class="h-cta">
    <div class="container">
        <div class="h-cta-inner">
            <div>
                <h2>Text us a photo. Get a straight answer.</h2>
                <p>Send three photos of the damage to {PHONE_TXT} and we will tell you what the repair involves and what it costs.</p>
            </div>
            <div class="h-btn-row">
                <a class="h-btn" href="{SMS}"><i class="fa fa-camera" aria-hidden="true"></i> Text photos</a>
                <a class="h-btn h-btn-light" href="{TEL}"><i class="fa fa-phone" aria-hidden="true"></i> Call {PHONE_TXT}</a>
            </div>
        </div>
    </div>
</section>"""


def expand_tokens(body, slug):
    body = body.replace("<!--SIDEBAR-->", service_sidebar(slug))
    body = body.replace("<!--CTA-->", CTA_BAND)
    body = body.replace("{{SMS}}", SMS).replace("{{WA}}", WA).replace("{{TEL}}", TEL)
    return body


# ---------------------------------------------------------------- page loader

FM = re.compile(r"^<!--META\s*(\{.*?\})\s*-->\s*", re.S)


def load_pages():
    pages = []
    for fn in sorted(os.listdir(PAGES_DIR)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(PAGES_DIR, fn), encoding="utf-8").read()
        m = FM.match(raw)
        if not m:
            raise SystemExit(f"{fn}: missing <!--META {{...}}--> front matter")
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        meta.setdefault("slug", fn)
        pages.append(meta)
    return pages


def resolve_schema(meta):
    """Turn declarative schema hints in front matter into JSON-LD objects."""
    out = []
    url = f"{SITE_URL}/{meta['slug']}"
    if "service" in meta:
        s = meta["service"]
        out.append(service_schema(s["name"], s["desc"], url, s["type"]))
    if "faq" in meta:
        out.append(faq_schema([(q, a) for q, a in meta["faq"]]))
    return out


def build():
    pages = load_pages()
    written = []
    for p in pages:
        p["schema"] = resolve_schema(p)
        html = head(p)
        html += header(p["slug"])
        if p["slug"] != "index.html":
            html += breadcrumb(p)
        html += '\n<main id="main">\n' + expand_tokens(p["body"], p["slug"]).rstrip() + "\n</main>\n"
        html += footer()
        out = os.path.join(ROOT, p["slug"])
        open(out, "w", encoding="utf-8").write(html)
        written.append(p)
        print(f"  wrote {p['slug']:<34} {len(html)//1024} KB")

    write_sitemap(written)
    write_robots()
    write_llms(written)
    print(f"\n{len(written)} pages + sitemap.xml + robots.txt + llms.txt")


PRIORITY = {"index.html": "1.0", "contact.html": "0.8", "insurance-claims.html": "0.8"}


def write_sitemap(pages):
    today = datetime.date(2026, 11, 9).isoformat()
    urls = []
    for p in pages:
        if p.get("noindex"):
            continue
        loc = SITE_URL + "/" + ("" if p["slug"] == "index.html" else p["slug"])
        pr = PRIORITY.get(p["slug"], "0.7")
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
                    f"    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)


def write_robots():
    txt = f"""# {BUSINESS} — {STREET}, {CITY}, {REGION} {POSTAL} — {PHONE_TXT}
User-agent: *
Allow: /

# AI assistants: plain-text facts about this business
# {SITE_URL}/llms.txt

Sitemap: {SITE_URL}/sitemap.xml
"""
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(txt)


def write_llms(pages):
    svc_lines = "\n".join(f"- [{t.replace('&amp;', '&')}]({SITE_URL}/{s})" for s, t in SERVICES)
    txt = f"""# {BUSINESS}

> An auto body and collision repair shop in downtown Whitby, Ontario. Halif repairs
> collision damage, bodywork and bumpers, paint and colour matching, dents, scratches
> and rust on cars, trucks and SUVs, and helps customers with insurance claims.
> The easiest way to start is to text or WhatsApp photos of the damage to {PHONE_TXT}.

## Business facts

- Name: {BUSINESS}
- Address: {STREET}, {CITY}, {REGION} {POSTAL}, Canada
- Phone, text and WhatsApp: {PHONE_TXT} (+1 905-730-6089)
- Coordinates: {LAT}, {LNG} (Plus code V3J6+99 Whitby)
- Location: downtown Whitby, just off Dundas Street East (Highway 2), Durham Region, Ontario
- Hours: Monday to Friday 9:00 am – 5:30 pm; Saturday 9:00 am – 2:30 pm; Sunday closed
- Google rating: {RATING} from {REVIEW_COUNT} reviews
- Experience: the team brings over 30 years of experience
- Instagram: {INSTAGRAM}
- Google listing: {GOOGLE}
- Last updated: {UPDATED}

## Services

{svc_lines}

Vehicles: cars, trucks and SUVs.

## Service area

Whitby (including Downtown Whitby, Brooklin and Port Whitby), Oshawa, Ajax, Pickering,
Courtice, Bowmanville and the rest of Durham Region, Ontario.

## How to get an estimate

1. Take three photos: a wide shot of the whole vehicle, a close-up of the damage, and one from an angle.
2. Text or WhatsApp them to {PHONE_TXT} with your name and the vehicle's make, model and year.
3. Halif replies with an estimate. You can also visit 105 Ash St during opening hours.

## Ontario facts Halif publishes

- In Ontario, drivers have the right to choose their own repair shop, tow operator and rental company (source: FSRA).
- A repair shop must give a written estimate before charging, and the final bill cannot exceed the estimate by more than 10% (source: Government of Ontario).
- A collision with combined damage over $5,000 must be reported to a Collision Reporting Centre within 48 hours. The Durham Collision Reporting Centre is at 650 Rossland Road East, Whitby, open daily 10 am to 6 pm (source: Durham Regional Police Service).

## Key pages

- [Home]({SITE_URL}/)
- [All services]({SITE_URL}/services.html)
- [Insurance claims]({SITE_URL}/insurance-claims.html)
- [Frequently asked questions]({SITE_URL}/faq.html)
- [Reviews]({SITE_URL}/reviews.html)
- [Contact and directions]({SITE_URL}/contact.html)
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    build()
