# Halif Auto Repair and Collision — open items before launch

Everything on the site today traces back to a verified fact in `halif-content-brief/01-client-facts.md`
or to an official Ontario source. **Nothing has been invented.** Where a fact was missing, the
claim was left off the site rather than guessed or marked `[TBC]` in public copy.

This is the list of what is still open, in the order it blocks launch.

---

## 1. Blocking — must be done before the site goes live

| # | Item | Where it lives | What to do |
|---|---|---|---|
| 1 | **Domain name** | `_build/build.py` → `SITE_URL` (line ~28) | Currently the placeholder `https://www.halifautorepair.ca`. Set the real domain and re-run `python3 _build/build.py`. It feeds every canonical tag, Open Graph URL, `sitemap.xml`, `robots.txt`, `llms.txt` and the JSON-LD. |
| 2 | **Approve the five review quotes** | `reviews.html`, `index.html`, `about.html`, `auto-paint-colour-matching.html` | Pierre K. (×2), Lousian K., MotorLux, Christine G. — all quoted word for word from the public Google listing with first name + last initial, as the brief requires. Confirm the client is happy to display them. |
| 3 | **Confirm the paint booth is in-house** | `auto-paint-colour-matching.html`, `about.html`, `index.html` | The booth is referenced because a customer review mentions it. If it is not Halif's own booth, those three sections need rewording. |
| 4 | **Point the Google "Website" button at the new site** | Google Business Profile | It currently points at Instagram. |
| 5 | **Replace the stock photography** | `images/halif/` | See section 3 below. The current images are licensed stock, chosen to match each section, but real shop photos will outperform them. |

---

## 2. Questions for the client (answers unlock copy that is currently missing)

Each answer below lets us add a section that competitors in Durham do not have.

| Question | What it unlocks |
|---|---|
| **Does Halif do mechanical repair** (brakes, engine, maintenance) or body/collision only? | The business name says "Auto Repair". Right now the site says body and collision only. If mechanical work is offered, it needs its own page. |
| **How fast do you reply to a photo estimate?** | "We reply within X hours" on the hero and in the FAQ. This is the single strongest conversion line we are missing. |
| **Is the estimate free?** | Currently phrased neutrally ("if a shop charges, Ontario law says it must tell you in advance"). "Free estimates" cannot be published until confirmed. |
| **What is your warranty?** (cover and duration) | The site currently states only the Ontario legal minimum (90 days / 5,000 km). Chains advertise lifetime warranties — stating Halif's real terms plainly is better than staying silent. |
| **Which insurers do you work with directly?** Any preferred-shop programmes? | Named insurers on the insurance page. Currently we only say "we help with claims", which is all the logo supports. |
| **Do you accept tow-ins? Do you arrange towing?** | The FAQ currently tells drivers to call first. If tow-ins are welcome, we can say so outright — a high-intent moment. |
| **Courtesy car or help booking a rental?** | A section on the insurance page. |
| **Who is George?** Role, surname, happy to be named and photographed? | A real named person on the About page. Chains cannot do this. |
| **Any training or certifications** (I-CAR, paint brand, OEM)? | A credentials block. Nothing can be claimed without proof. |
| **Which paint system do you use?** | Strengthens the colour-matching page. |
| **Can we publish any prices or "from $" ranges?** | A price indication on dents/scratches and bumper repair. Competitors do not publish any. |
| **Languages spoken at the shop?** | A line in the trust strip and footer. |
| **TikTok and Facebook page URLs** | Footer and top-bar social links, plus `sameAs` in the structured data. Only Instagram and Google are linked today. |
| **Do you do frame/structural work, glass, ADAS sensor calibration, paintless dent repair?** | Each would add a section to the relevant service page. |
| **Do you want dealer/trade work?** | The MotorLux review shows a trade customer already uses Halif. A trade section could be added. |
| **Business email address** | There is deliberately no email anywhere on the site, because none was verified. Phone, text and WhatsApp carry everything today. |

---

## 3. Photography

The site currently uses **licensed stock photography** from Pexels (free for commercial use,
no attribution required). Every image was chosen to match its section — spray booth, panel
work, rust on a sill, a salted winter road, a clean waiting area, and so on.

**Nothing is presented as Halif's own work.** The homepage gallery is captioned by process
("Prep, paint, panel and finish") and links out to Instagram for real jobs, so the site stays
honest.

Swapping in real photos is the single biggest visual upgrade available. Ask the client for:

| Priority | Shot needed | File to replace |
|---|---|---|
| 1 | The paint booth with a car in it | `images/halif/paint-booth.jpg` (1000×640) |
| 1 | The shop floor, wide | `images/halif/shop-busy.jpg`, `shop-floor.jpg` (1000×640) |
| 1 | The waiting area | `images/halif/waiting-area.jpg` (1000×640) |
| 1 | A hero shot — a car mid-repair in the booth | `images/halif/hero-home.jpg` (1920×820) |
| 2 | Before/after pairs per service | `card-*.jpg` (640×450), `band-*.jpg` (1920×420) |
| 2 | George and the team | New section on `about.html` |
| 3 | The shop exterior / sign on Ash St | Would go on `contact.html` |

The client already has 11 photos on the Google profile and 14 Instagram posts — ask for the
original files rather than re-downloading the compressed versions.

Keep the same filenames and dimensions and nothing else needs changing. Originals of the
current stock images are kept outside the web root in `../_image-sources/` if you need to
re-crop.

---

## 4. Name consistency (local SEO)

- Instagram says "Halif Auto Repair & Collision**s**". Google and the logo say
  "Halif Auto Repair **and Collision**". The site uses the Google/logo version everywhere.
  **Fix the Instagram bio to match** — search engines and AI assistants match on exact spelling.
- Use the identical name, address and phone on every directory: Yelp.ca, YellowPages.ca, BBB,
  Apple Maps, Bing Places.

---

## 5. To wire up at launch

- Google Analytics 4, Google Search Console, Bing Webmaster Tools, Microsoft Clarity.
- Track as conversions: tap-to-call, tap-to-text, WhatsApp tap, "Get a photo estimate" clicks,
  directions clicks.
- Submit `sitemap.xml` to Search Console.
- Set up a 404 handler so unknown URLs serve `404.html`.
- Serve over HTTPS and enable gzip/brotli.

---

## 6. Review the dated content

Two pages carry an "Updated November 2026" line because they quote Ontario rules that change:

- `insurance-claims.html`
- `faq.html`

Re-check these sources before launch and once a year after:

- [Government of Ontario — car repair shops: your rights](https://www.ontario.ca/page/car-repair-shops-your-rights)
- [FSRA — your rights and responsibilities](https://www.fsrao.ca/consumers/auto-insurance/purchasing-your-policy/your-rights-and-responsibilities-consumer)
- [FSRA — claims process after an accident](https://fsrao.ca/consumers/auto-insurance/protect-yourself/claims-process-after-accident)
- [Durham Regional Police — Collision Reporting Centre](https://www.drps.ca/community-safety-and-support/collision-reporting-center-crc/)

Also keep the **5.0 / 10 reviews** figure current. It appears on `index.html`, `about.html`,
`reviews.html` and in the structured data on those three pages. Update all four together, or
the rich result will not match the page.
