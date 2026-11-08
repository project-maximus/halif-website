# Halif Auto Repair and Collision — website

A static site for Halif Auto Repair and Collision, 105 Ash St, Whitby, ON L1N 4B1.
Built on the MechanicHub HTML template, rebranded and rewritten end to end.

**Read [`CLIENT-TODO.md`](CLIENT-TODO.md) before launch** — it lists the domain setting and the
open questions for the client.

---

## Running it

It is plain HTML. Open `index.html`, or serve the folder:

```bash
cd Html-File
python3 -m http.server 8000
# http://localhost:8000
```

Upload the contents of `Html-File/` to the web root. The `_build/` folder is the source for the
pages and does not need to be uploaded (it is harmless if it is).

---

## Pages

| File | Page | Main search term |
|---|---|---|
| `index.html` | Home | auto body shop Whitby |
| `services.html` | All services | auto body services Whitby |
| `collision-repair.html` | Collision repair | collision repair Whitby |
| `auto-body-repair.html` | Auto body & bumper repair | auto body repair Whitby |
| `auto-paint-colour-matching.html` | Paint & colour matching | car paint shop Whitby |
| `dent-scratch-repair.html` | Dents & scratches | dent repair Whitby |
| `rust-repair.html` | Rust repair | rust repair Whitby |
| `insurance-claims.html` | Insurance claims | insurance claim body shop Whitby |
| `about.html` | About | Halif Auto Repair and Collision |
| `reviews.html` | Reviews | — |
| `contact.html` | Contact & directions | 105 Ash St Whitby body shop |
| `faq.html` | FAQ (25 questions, 5 categories) | — |
| `privacy.html` | Privacy policy | — |
| `404.html` | Not found | not indexed |

Plus `sitemap.xml`, `robots.txt` and `llms.txt`.

---

## Editing content

Pages are **generated**. Do not edit the `.html` files in the root — they are overwritten.

```
_build/
  build.py          shared shell: head, header, footer, schema, site constants
  pages/*.html      one file per page: front matter + body
```

Each page file starts with a `<!--META {...}-->` JSON block:

```json
{
  "slug":  "rust-repair.html",
  "title": "Rust Repair in Whitby & Durham | Halif Auto",
  "desc":  "…150–160 characters, ends with an action…",
  "h1":    "Rust repair in Whitby",
  "band":  "band-rust",              // breadcrumb banner image in images/halif/
  "band_sub": "one supporting line",
  "trail": [["Home","index.html"], ["Services","services.html"], ["Rust repair","rust-repair.html"]],
  "rating": false,                    // true only on pages that display the reviews
  "service": { "name": "…", "type": "…", "desc": "…" },   // emits Service schema
  "faq": [ ["Question?", "Answer."] ]                      // emits FAQPage schema
}
```

Tokens expanded in the body:

- `<!--SIDEBAR-->` — the service nav + contact CTA, with the current page marked active
- `<!--CTA-->` — the closing red call-to-action band
- `{{SMS}}` `{{WA}}` `{{TEL}}` — the pre-filled text, WhatsApp and call links

Then rebuild:

```bash
cd Html-File
python3 _build/build.py
```

Business facts (name, address, phone, hours, links, rating) live as constants at the top of
`build.py`. Change them in one place and every page, the footer, the schema, `llms.txt` and
`robots.txt` follow.

---

## Brand

Taken from the badge logo: black badge, vivid red car, chrome lettering, graphite gear.

| Token | Value | Used for |
|---|---|---|
| `--h-red` | `#D81F26` | Buttons, links, accents, active nav, section rules |
| `--h-red-dark` | `#AF171D` | Button hover |
| `--h-ink` | `#0B0B0D` | Top bar, footer, dark sections, hero overlay |
| `--h-charcoal` | `#16181C` | Main nav bar |
| `--h-graphite` | `#2A2E35` | Lead paragraphs, outline buttons |
| `--h-chrome` | `#C9CDD2` | Secondary accent on dark, logo subtitle |
| `--h-steel` | `#5B616A` | Body copy |
| `--h-paper` | `#F5F6F7` | Alternating section backgrounds |

White on `#D81F26` is 5.07:1 — above the WCAG AA 4.5:1 threshold for normal text.

Type: **Barlow Condensed** for headings and buttons, **Barlow** for body (Google Fonts).

### Stylesheets

| File | Role |
|---|---|
| `css/halif.css` | The brand layer — palette, typography, header, hero, all new components, responsive rules. **Edit this one.** |
| `css/style.css` | The template's stylesheet, recoloured to the Halif palette (navy `#233588` → red, yellow `#f8ec30` → chrome, dark navy → charcoal). |
| `css/responsive.css` | The template's responsive rules, recoloured the same way. |
| `css/_original/` | Untouched copies of the three template stylesheets, for reference. |

`css/halif.css` loads last and wins.

### JavaScript

`js/halif.js` (needs jQuery, loaded before it) handles: sticky header, mobile menu, accordions,
FAQ category filter, today's-hours highlight, scroll-to-top and smooth anchors. The template's `custom.js` and its plugin scripts were removed — the site
loads jQuery, Bootstrap, WOW, appear and easing only.

---

## How the site takes enquiries

There is **no backend and no contact form**. Every call to action opens the visitor's own phone
app directly:

| Action | Link |
|---|---|
| Text photos | `sms:+19057306089?&body=…` (pre-filled message; works on iOS and Android) |
| WhatsApp photos | `https://wa.me/19057306089?text=…` |
| Call | `tel:+19057306089` |
| Directions | Google Maps directions URL |

Nothing is transmitted until the visitor presses send in their own app, and nothing is stored.
That needs no server, no mail configuration and no data handling — and it matches how Halif
already takes estimates.

The "which photos to take" guidance lives in the **Send photos, get a price** section on the
home page and in the FAQ, rather than on a separate page.

---

## Search, AI answers and local SEO

- `AutoBodyShop` structured data on every page (NAP, geo, opening hours, `areaServed`, `sameAs`,
  `makesOffer`). `aggregateRating` only on the three pages that actually display the reviews.
- `Service` schema on each service page, `FAQPage` on all nine pages with FAQ blocks,
  `BreadcrumbList` on every inner page, `WebSite` on the home page.
- Every page opens with a highlighted answer block: the first two sentences state the plain
  definition plus the business name, town and phone — the shape AI assistants quote.
- Questions are H2/H3 headings with 40–60 word answers. Steps are numbered lists.
- Ontario rules are cited with outbound links to ontario.ca, FSRA and DRPS.
- `llms.txt` at the root gives assistants the facts in plain text.
- One main keyword per page, no two pages targeting the same term.
- Canonicals, Open Graph and Twitter cards on every page; `geo.*` meta for local search.

---

## Accessibility

Skip link, one H1 per page, alt text on every image, labelled form fields, keyboard-operable
accordions and tabs with `aria-expanded` / `aria-pressed`, visible focus rings, 4.5:1+ contrast
on text, and a `prefers-reduced-motion` block.

---

## Checked

- 14 pages at 1440 / 1280 / 1200 / 1024 / 768 / 500 px: no horizontal overflow, no broken images,
  no missing alt attributes, exactly one H1 each.
- Real mobile widths (430 / 390 / 360 px) verified in iframes.
- All internal links and asset references resolve.
- All JSON-LD parses; titles 40–65 chars, meta descriptions 110–165 chars.
- Accordions, FAQ filter, sticky bar, dropdowns and mobile menu all exercised in-browser.
- Nav item spacing measured as even (6px flex gap, zero phantom margins) at 1200–1440px.
- Copy checked against the brief's banned-word list, conditional-claims list and Canadian
  spelling. The only exclamation marks on the site are inside verbatim customer reviews.
