# LUDIFU Website — Handover Document

**Version:** 2.22.0
**Last updated:** 12 September 2026
**Owner:** Puneet Rawat, Founder — LUDIFU, Mumbai
**Contact:** +91 98678 00451 (WhatsApp)

> **New chat? Start here.** This document contains everything needed to continue working on the LUDIFU website without re-explaining context. Read it fully before making changes.

---

## 1. What LUDIFU Is

LUDIFU ("Let Us Do It For U") is a Mumbai-based group of ventures founded by Puneet Rawat. It is **not** a single product company — it is a parent brand with five distinct ventures.

| Venture | What it is | Website | Status |
|---|---|---|---|
| **Clicarity** | Light manufacturing execution system (MES) — real-time work tracking that sits under an ERP/CRM/Sheets | clicarity.com | Live, actively sold, own site |
| **WA.Expert** | WhatsApp Business API platform — chatbots, bulk messaging, team inbox, mini CRM | wa.expert | Live, actively sold, own site |
| **LUCADEMY** (LUDIFU Academy) | EdTech — ran live cohorts May 2020–Dec 2023 | ludifu.com/academy.html | **Closed to open batches.** Enquiry-only |
| **LUDIFU PhotoBooks** | Bespoke custom coffee table books | ludifu.com/photobooks.html | Live, enquiry-only via WhatsApp |
| **ClickToWish** | Automated WhatsApp occasion wishes | clicktowish.com | Live, own site |

**Legal entity note:** WA.Expert's footer trades as "Paper Print Services".
**Office:** 209/A2, Shah & Nahar Industrial Estate, Lower Parel West, Mumbai 400013.

---

## 2. Tech Stack & Deployment

- **Pure static HTML/CSS/JS.** No framework, no build step, no bundler, no npm.
- **Hosted on Cloudflare Pages.** Push files to the connected repo → auto-deploys.
- **All CSS is inline** in each file's `<style>` block. There is no shared stylesheet. This is deliberate — it keeps each page self-contained and avoids a render-blocking external CSS request.
- **All JS is inline** and vanilla. No jQuery, no React.
- **No backend.** Forms build `wa.me` deep links client-side. Nothing is stored server-side.

### Cloudflare-specific files
| File | Purpose |
|---|---|
| `_headers` | Security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy) + cache rules |
| `_redirects` | 301s: `/case-study.html` → `/academy.html`, `/career` → `/careers.html`, `/jobs` → `/careers.html` |

### Deploy checklist
1. Push all files in this folder to repo root (not in a subfolder).
2. Verify `robots.txt` and `sitemap.xml` resolve at domain root.
3. Submit sitemap in Google Search Console.
4. **`og-image.jpg` does not exist yet** — must be created at 1200×630px and placed in root, or all social shares render blank.

---

## 3. File Structure

```
/
├── index.html              Parent homepage — all 5 ventures
├── academy.html            LUCADEMY — merged case study + training + recordings
├── careers.html            Careers — 5 roles, application form
├── founder.html            Founder profile — venture history, investor-facing
├── photobooks.html         PhotoBooks — full product page
├── terms.html              Terms & Conditions
├── privacy.html            Privacy Policy
├── refund-policy.html      Refund & Cancellation Policy
├── shipping-policy.html    Shipping Policy
├── 404.html                Not found page
├── favicon.svg             Green square, gold "L"
├── robots.txt
├── sitemap.xml
├── _headers                Cloudflare security headers
├── _redirects              Cloudflare 301 redirects
├── VERSION                 Current version number
└── HANDOVER.md             This file
```

---

## 4. Design System

**Do not deviate from these tokens.** Every page uses the same CSS variables.

### Typography
```css
/* Display — headings, numbers, quotes */
font-family: 'Cormorant Garamond', serif;

/* Body — everything else */
font-family: 'Outfit', sans-serif;
```
Loaded async from Google Fonts with `media="print" onload="this.media='all'"` + `<noscript>` fallback. `preconnect` to both `fonts.googleapis.com` and `fonts.gstatic.com` is required for LCP.

### Colour tokens
```css
:root {
  --cream:    #faf8f4;   /* page background */
  --white:    #ffffff;   /* cards */
  --ink:      #1e1e1e;   /* headings, dark sections */
  --ink2:     #3a3a3a;   /* body text */
  --forest:   #2c5f3f;   /* PRIMARY accent — buttons, links */
  --forest2:  #3d7a53;   /* hover state */
  --forest-lt:#e8f2eb;   /* tinted backgrounds */
  --gold:     #c19a3a;   /* eyebrows, numerals */
  --gold-lt:  #f5e9c8;   /* tinted */
  --warm:     #f2ece0;   /* alternate section bg */
  --muted:    #7a7464;   /* secondary text */
  --border:   #e2ddd4;
  --shadow:   rgba(28,28,28,0.07);
}
```

**PhotoBooks page uses a warmer variant** (parchment/umber/terracotta) — see that file's `:root`. It is intentionally distinct because it sells a premium physical product.

**academy.html uses a darker variant** (`--deep: #241c12`) for the case-study sections.

### Component conventions
- **Eyebrow**: `.eyebrow` — small caps, 2px letter-spacing, gold, with a `::before` rule line
- **Section heading**: `h2.section-h` with `<em>` for the italic forest-green accent word
- **Buttons**: `.btn-primary` (forest fill), `.btn-outline` (bordered), `.btn-apply` (WhatsApp green `#25D366`)
- **Cards**: white bg, `1px solid var(--border)`, `border-radius: 12–16px`, lift on hover

### Nav structure (important)
The nav logo must stay in **normal flex flow**, wrapped in `.nav-left` alongside the back-link. It must **never** use `position:absolute; left:50%` — that caused a visual collision in v2.5.0 when nav links grew past ~6 items and ran underneath the centred logo.

Keep desktop nav to a **maximum of 5 links**. Everything else belongs in the mobile menu and footer. Desktop breakpoint is `1100px` on academy.html.

### Hard rules
- ❌ **No emoji as UI icons on careers.html** — removed deliberately; reads as unserious to placement cells and academic audiences. Emoji are acceptable on index.html venture cards and photobooks.
- ✅ Every page has: skip-link, `#main-content`, hamburger mobile nav, floating WhatsApp button, cookie banner, `:focus-visible` styles
- ✅ Every external link needs `target="_blank" rel="noopener noreferrer"`
- ✅ Mobile breakpoint is `960px` (some files use `980px` — both acceptable)

---

## 5. Page-by-Page Notes

### index.html — Parent homepage
Positions LUDIFU as a family of five ventures. Tone is **"Warm & Human (startup story)"** — this was an explicit client choice.

- Hero: "We Build Things That Actually Help People."
- "A Startup That Kept Showing Up" story section
- Five venture cards → each links to its destination
- Dedicated sections for Clicarity, WA.Expert, ClickToWish (added because linking straight out gave them no room to sell)
- PhotoBooks section links through to `photobooks.html`
- **No CTA button in nav** — deliberate, so no venture is favoured

### academy.html — LUCADEMY
**This is the most important page.** It merges what were originally two pages (case study + academy).

Structure, in order:
1. Green banner for returning students → Thinkific recordings
2. Times of India press bar
3. Hero: "Three Lakh Leads. Six People. One System."
4. Stats: 3,00,000+ leads / 6,000+ students / 10 subjects / 6 people
5. **The Scale** — ~235 leads/day for 1,300 days
6. **The Team** — 1 founder, 1 designer, 10 professors, 3 rotating interns
7. **The Multiplier** — 4,500+ remote intern network
8. **The Founder** — "One Person Was the Entire Middle"
9. Story / Timeline / 6-vs-30
10. **Automation deep-dive** — 8 numbered blocks (this is the section academic audiences care about)
11. **The Funnel** — 3,00,000 → 6,000 with absolute numbers
12. Learnings / Press (newsprint feature)
13. Subjects / Recordings / Training on Request / Student voices

**Critical positioning:** LUCADEMY is **not selling courses**. Open batches closed Dec 2023. All copy is past tense. CTAs say "Enquire", never "Enrol" or "Book". Corporate/group training is still offered on request.

### careers.html — Careers
Five roles, each open as **internship OR full-time**.

- Roles: Automation Specialist, Web Development, Founder's Office Associate, Operations Associate, Product Manager
- **No stipend mentioned anywhere** — removed at client request (also removed from JobPosting schema)
- Application form at `#apply` builds a numbered WhatsApp message client-side
- Form adapts: Internship shows college/year/academics; Full-Time shows company/experience/notice period
- Travel-time field has a prominent callout — it's the #1 predictor of early dropout
- `JobPosting` JSON-LD for all 5 roles with `employmentType: ["INTERN","FULL_TIME"]` → enables Google for Jobs

### photobooks.html — PhotoBooks
Premium product page. Warm parchment palette, alternating light/dark sections.

- Pricing: **₹8,000 base (10 pages) + ₹800 per additional side** — confirmed by client
- Sizes: 10×10" and 12×12" closed; 20×10" and 24×12" open
- 7-step process, 3 binding types (lay-flat recommended), 2 YouTube testimonial videos
- Testimonials are **Indian mothers** — deliberate choice for relatability (kids, holidays, milestone birthdays/anniversaries)

### founder.html — The Founder
Investor-facing. Built from two client documents (`Puneet_Profile.docx`, `Family_BackGround.docx`) plus web verification.

Narrative spine: **the failures were not random.** 17 ventures, mostly closed, each taught something specific that shows up in Clicarity / WA.Expert / LUCADEMY. The honest 2018 quote ("not being successful at any so far") is included deliberately — it is the page's credibility anchor.

**⚠ PRIVACY — do not add:** `Puneet_Profile.docx` is a *matrimonial biodata*. It contains home address (Ansal Heights, Worli Naka), father's personal mobile and email, date **and time** of birth, physical description, and full family tree. None of it is on the page and none of it should be. The lineage section refers to grandfather/father without names or contact details.

### Policy pages
Terms, Privacy, Refund, Shipping. Refund policy is aligned per-product:
- Academy: full refund within 48hrs, **5–7 working days** processing
- PhotoBooks: refund only pre-design-approval, **7–10 working days**

---

## 6. Key Facts & Numbers (verified)

From the Times of India article (25 Aug 2020, by Sharmila Ganesan, Mumbai edition Page 2):
- LUDIFU Academy launched **15 May 2020**, mid-lockdown
- Started with **Excel and PowerPoint** workshops
- Origin: the family coffee table book printing firm was stalled by the pandemic — this is also the origin of LUDIFU PhotoBooks
- Early workshops priced **₹200–₹1,799**
- **400+ students** within three months, most under 23
- Founder quote used on site: *"Innovation is the answer to every difficult situation."*

Client-supplied operating figures:
- **3,00,000+** leads processed (2020–2023)
- **6,000+** paid students
- **10** subjects
- Course fees **₹1,000–₹15,000**
- Funnel: leads → ~60% registered → ~36% attended demo → ~29% stayed → **~2% paid**
- Team: 1 founder, 1 freelance designer, 10 professors, 3 rotating interns (post-late-2020)
- **4,500+** remote interns over 3 years

**Confirmed:** WhatsApp number **+91 98678 00451** — verified against wa.expert's own site footer.

---

## 6b. Venture Date Conflicts — NEEDS CLIENT CONFIRMATION

The two source documents disagree. `founder.html` currently uses the **Family_BackGround.docx** dates (the later, more specific document). Confirm before any investor sees this.

| Venture | Puneet_Profile.docx | Family_BackGround.docx | Used on site |
|---|---|---|---|
| Unified Florists | 2008–2010 | Jun 2009–Jun 2010 | 2009–2010 |
| CondomPoint | 2008–Present | Jun 2011–Jun 2016 | 2011–2016 |
| 22SEO | 2008–2014 | Dec 2011–Jun 2015 | 2011–2015 |
| CouponZatak | 2009–2010 | May 2012–Dec 2014 | 2012–2014 |
| Unified Stores | 2009–2014 | Sep 2011–Dec 2014 | 2011–2014 |
| My Pet Centre | 2010–2014 | Dec 2011–Dec 2014 | 2011–2014 |

Also unresolved: TOI (2020) says the flower site was "back in 2010"; Penn State dates are 2001–2004 in the profile doc but RocketReach lists 2001–2005. The Leaf end-date (2019) is **assumed** — client has not confirmed.

## 7. ⚠️ Open Items / Unverified

These must be resolved before or shortly after launch.

| Item | Issue | Action needed |
|---|---|---|
| **`og-image.jpg`** | Referenced by every page's OG tags but **does not exist** | Create 1200×630px branded image, place in root |
| **Thinkific URL** | Site uses `ludifurecordings.thinkific.com/collections` (10 places). LUDIFU's own terms page references `ludifu.thinkific.com` | **Confirm which is live.** If wrong, every past student hits a dead page |
| **4,500 intern figure** | Client offered "4,500 odd" after originally saying 8,000; LinkedIn shows 800+ self-listed | Verify against actual records. This page targets IIM/IIT/Ivy audiences who fact-check |
| **Intern value exchange** | Section says what interns *did*, not what they *received* | If interns got certificates / LOR / mentorship / course access, add it. Strengthens the section and removes any "unpaid labour" reading |
| **Intern count** | `founder.html` avoids a number; `academy.html` says 4,500+. Family doc (c.2018) says "more than 700". | Reconcile — 700 in 2018 growing to 4,500 by 2023 is plausible but needs confirming |
| **Second WhatsApp number** | Google Play listing for the LUDIFU app shows `919920510234`, site uses `919867800451` | Confirm which is current; update or remove the Play listing |
| **The Leaf end date** | Listed as 2017–2019, but client only said "Nov 2017 till date" in a c.2018 document | Confirm actual closure date |
| **Live site is behind** | As of 12 Sep 2026, live `academy.html` is an old build still selling "Book Free Workshop" for batches that aren't running | **Push urgently** |
| **photobooks.html never uploaded** | Only exists as `#photobooks` anchor on live homepage | Push |
| **careers.html never uploaded** | Not live | Push |

---

## 8. Version History

| Version | Date | Changes |
|---|---|---|
| **2.22.0** | 14 Sep 2026 | **Anchor offset bug fixed site-wide** — no page had `scroll-margin-top`, so every in-page link landed with its heading hidden under the 68px sticky nav. Now 88px on all 11 pages. New **section rail** on founder.html: fixed left-side dot navigation, 15 sections, labels expand on hover, active section tracked by IntersectionObserver, hidden below 1180px. Homepage gains a **full-record strip** linking to timeline and founder — deliberately not 15 venture cards, which would bury the five operating products. |
| 2.21.1 | 14 Sep 2026 | **Homepage consistency fix.** Two v2.8.0 replacements had silently failed (string used `&amp;` where file had `&`) — Clicarity card tagline and section heading still read "Solve JSR & TAT". More seriously, the homepage was still **selling closed LUCADEMY batches**: "12+ Courses · Live · Certified", "Explore Courses →", "free 1-hour workshops anyone can join today", and calling it "our most active venture". All repositioned to past tense with the case-study framing, matching academy.html. Footer links updated. **Lesson: verify string replacements actually fired — check counts after, not just exit code.** |
| 2.21.0 | 14 Sep 2026 | **New page: `timeline.html`** — scroll-driven vertical timeline, 1987→2026. Alternating cards on desktop, single column on mobile, colour-coded by type (venture / closure / press / milestone). Filter chips, reading-progress bar, gradient rail that fills on scroll, IntersectionObserver reveal with `prefers-reduced-motion` respected. No JS libraries. Wired into all nav/footers, sitemap, and `/journey` redirect. |
| 2.20.0 | 14 Sep 2026 | New **#the-question** section — the Harsh Mariwala lunch (won via ASCENT referral campaign, ~75 referrals) and the advice that turned The Leaf around: one-on-one, visibly, *"what would you do if you were in my shoes?"* Team 65→25, operation improved. ASCENT membership since 2016 and Trust Group facilitator 6 of 10 years added as credentials. The Leaf card expanded with real scale: 150 seats, 450-item menu, 250+ inventory lines, 45 of 65 staff being the franchiser's rotating training pool. **⚠ Trust Group member names deliberately NOT published — ASCENT Trust Groups are confidential by design. Do not add without written consent from each member.** |
| 2.19.0 | 14 Sep 2026 | Added two **WhatsApp community-group** bios to #press-kit — written conversationally, leading with the venture list and the closure reasons rather than credentials, closing on "not selling anything". Uses WhatsApp single-asterisk bold. Eight copy blocks total on the page. |
| 2.18.0 | 14 Sep 2026 | New **#investor-brief** section. Two copy-ready blocks: a ~230-word forwardable investor brief written in neutral third person for pasting into an IC note, and a **verification index** listing every claim on the page with where to check it independently. Includes an explicit statement that Clicarity financials are withheld from the site by design and shared under NDA. `/investors` redirects here. |
| 2.17.0 | 14 Sep 2026 | **Full audit vs Checklist v2.0 — 47% → 91% on testable items.** Fixed: titles trimmed under 60ch (3 pages), meta descriptions to 50–160ch (5 pages), 404 given canonical/OG/Twitter, LCP font preload on all pages, **CSP + HSTS headers added**, WebP generated for all images with `<picture>` fallback (~45% smaller), GA4 block added commented-out awaiting real Measurement ID. Added `audit.py` — re-runnable checklist audit. Remaining fails are deployment-dependent (GA4 ID, Search Console). |
| 2.16.0 | 14 Sep 2026 | **Content loss found and restored.** The Team / Multiplier / Founder-role sections were silently destroyed by the v2.7.0 thesis rebuild (section replace between two markers). Restored consolidated as **#operation** — 6-person team breakdown, 4,500 intern network, and the no-management-layer argument. **Added `CONTENT-MANIFEST.txt` + `check-content.sh`** — run after every edit; verifies every section ID and a content marker still exist. Div-balance checks do not catch cleanly-removed sections. Mobile fixes: 404.html had zero media queries; .poster and .bio-wrap had no mobile rules. |
| 2.15.0 | 14 Sep 2026 | New **press kit / bio** section on founder.html (`#press-kit`). Six copy-ready blocks with one-click clipboard: one-liner, short (~55w), medium (~130w), full (~270w), spoken stage introduction, and a structured key-facts block. Vanilla JS with execCommand fallback for non-HTTPS. `/bio` and `/press-kit` redirect here. **Maintenance note: these bios are the canonical source — update them here when any fact changes.** Decided against a downloadable founder deck: bios get pasted, decks go stale. |
| 2.14.0 | 14 Sep 2026 | **Documentary proof added to The Play.** Original 2013 poster (`cock-poster.jpg`) now displayed, carrying the sponsorship credit **"Protected by CondomPoint.com"**. Exact dates added (30–31 Jul, 1 Aug 2013, 7pm & 9:30pm), production company AllMyTea-Clustalz credited. Third-party verification via Nakuul Mehta's official site (nakuulmehta.com/#ttd), which records critical acclaim and sold-out houses at Prithvi and Jagriti. |
| 2.13.1 | 14 Sep 2026 | **Tone fix on The Play.** Heading "He Backed the Cast Before Anyone Knew Them" implied credit for other people's careers — replaced with **"We Sponsored the Play. They Made It Matter."** Removed the then/now framing on cast cards (read as condescending); each now simply lists their work. Added explicit line: *everything that made the production good was done by other people.* **Principle: when naming people more accomplished than the subject, credit flows to them, never borrowed.** |
| 2.13.0 | 14 Sep 2026 | New **The Play** section — the 2013 COCK sponsorship at Prithvi given full weight. All four cast members listed with verified Wikipedia links: Jim Sarbh, Sayani Gupta, Nakuul Mehta, Manish Gandhi, plus Mike Bartlett and the play itself. Framed as then-vs-now: none were household names in 2013, all four are now. Shruti Tejwani linked to her Facebook page with KidsStopPress attribution. |
| 2.12.0 | 14 Sep 2026 | **Positive reframe.** Hero changed from "Most of Them Did Not Work" to **"Fifteen Ventures. Seventeen Years. Never Raised a Rupee."** — leads with the self-funding achievement and sets up Clicarity as the first raise. Stats now lead with ₹0 raised. All section headings reframed strength-first: "Every Venture, Every Outcome", "Every Closure Was a Decision", "Fifteen Ventures, Zero Outside Capital", "He Was Offered 2% of What Became VistaPrint". **Principle: positive in headlines, honest in body — candour reads as confidence, not apology.** Body substance unchanged. |
| 2.11.0 | 14 Sep 2026 | **Count 14 → 15 (confirmed by client, final).** Print World reclassified from family business to venture — client confirms he built it from scratch within PPS and separated it out for individual accountability. Paper Print Services credited as the origin. Added Etam (sole VM print vendor from 2008, JV with Future Group), HUL Dove first Mumbai campaign incl. Orchid City Centre mall branding, Staples and Lee Cooper POS. **Multi-city work deliberately framed as coordination from Mumbai with local vendors invoicing independently** — accurate and avoids implying operational presence outside Mumbai. New "the thing he missed" callout: the successful venture was the one funding the experiments. Clicarity thesis retightened around Print World as proven competence. |
| 2.10.0 | 14 Sep 2026 | New **The Funding** section — answers how 14 ventures ran on ₹0 raised. Print World as the cash engine: Zodiac (one of only two approved vendors, ~8 years), Raymond, Oxemberg, NM Medical. Explains why ventures **overlap rather than queue** — self-funded operators need parallel income, not sequential. Visual funding-flow diagram. Print World venture card updated with the real client list. |
| 2.9.2 | 14 Sep 2026 | **Accuracy fix — venture count.** Page claimed 17 (earlier 16) ventures "started" by Puneet. Three of the 17 cards are not his foundings: Paper Print Services (father, 1987; joined 2005), Print World (family sister concern), Unified Prints (holding entity). Corrected to **14 ventures started**, with an explicit disclosure note in the ventures section explaining why the other three are listed. Title, meta, OG, stats and all body copy updated. **Rule: never state a count without listing what it contains.** |
| 2.9.1 | 14 Sep 2026 | **Bugfix:** `founder-photo.jpg` was referenced in v2.9.0 but never created — broken image on founder page. Now generated (640×640, centre-cropped, 66KB). Also generated the long-outstanding **`og-image.jpg`** (1200×630) from the same portrait — every page has referenced it since v2.1.0 with no file present, so all social shares were rendering blank. |
| 2.9.0 | 14 Sep 2026 | Founder photo added to hero (**requires `founder-photo.jpg` in repo root**). New **The Stack** section: ~1,000 live demos personally run Oct 2020–Jul 2021, then replaced by EverWebinar / Vimeo / Razorpay / ConvertKit / WhatsApp API — with WhatsApp piece becoming WA.Expert. **Prithvi Haldea** (Founder-Chairman, PRIME Database; SEBI committees) added as PhotoBooks first customer. **CondomPoint origin story**: newspaper ad, father's permission, Amit Jain the distributor, direct-to-CNF-agent margin insight. 3,00,000 figure now explained as free 30-min Excel workshop attendees. |
| 2.8.0 | 14 Sep 2026 | **Audience locked: investors only.** Dates corrected from LinkedIn (WA.Expert Jun 2021 not 2023; Clicarity Jan 2025; Paper Print Services director role 2005–2025; The Leaf Sep 2018–Nov 2019). Added **LUDIFU Coffee Table Books (2018)** with the Anmol Babani → Shruti Tejwani referral story. New **Where It Goes** section: the 3-year discipline as deliberate market testing, and Clicarity as the fundable venture with the intuitive-execution-system ambition. Investor enquiry CTA. No deck/financials on site by design. LinkedIn followers 24,800+. |
| 2.7.0 | 12 Sep 2026 | **Canonical dates locked** from client. **Bid2Splash removed entirely** at client request (legal caution) — 17 ventures becomes 16. Every closure reason replaced with the client's own stated reason. PhotoBooks split into app phase (2016–2020) and Coffee Table Books (current). ClickToWish pricing lesson added. Thesis section rebuilt around the client's line: *none of them closed because of money.* Penn State corrected to 2001–2005. |
| 2.6.1 | 12 Sep 2026 | Mined the client's original "Successful Failures" deck (Mar 2017). Added the **PrintBell/VistaPrint 2% refusal** as its own section — the origin of the entire e-commerce arc. Added a contemporaneous marketing-lessons section quoted from the deck. Corrected **Bid2Splash to "never launched."** Added real PhotoBooks numbers (23 Dec 2016 launch, ₹199, 1,750 downloads, angel funded). Intern growth curve now evidenced: 196→700→thousands. |
| 2.6.0 | 12 Sep 2026 | **New page: `founder.html`** — investor-facing founder profile. Three-generation lineage, education, all 17 ventures with dates/outcomes/learnings, "the failures were not random" thesis section, 6-publication press wall. Person JSON-LD. Wired into nav/footers/sitemap; `/about` and `/puneet` redirect to it. |
| 2.5.2 | 12 Sep 2026 | **Structural fixes found by full-site audit:** orphaned `</div>` in photobooks.html nav (introduced by 2.5.1 patch); `<div id="main-content">` left unclosed on 6 pages since the v2.1.0 accessibility pass — now closed before `<footer>` on all. Academy nav breakpoint moved to its own `@media(max-width:1100px)` block (the 2.5.1 edit had landed on a content block). Photobooks nav rebuilt with 4 section links. All 9 pages now validate with balanced div tags. |
| 2.5.1 | 12 Sep 2026 | **Bugfix:** nav logo collided with nav links on academy.html (logo was `position:absolute; left:50%` while nav had grown to 9 links). Logo moved into normal flex flow inside a `.nav-left` group; academy nav trimmed 9 → 5 links; same absolute-positioning removed from photobooks.html; desktop breakpoint raised 980px → 1100px. |
| 2.5.0 | 12 Sep 2026 | Careers: internship + full-time, client-side application form → WhatsApp, stipend removed, emoji removed, press strip added. Homepage: Clicarity repositioned as MES, WA.Expert updated to 7-module platform, PhotoBooks linked as page. Version stamping introduced. |
| 2.4.0 | 12 Sep 2026 | Careers page created — 5 roles, JobPosting schema, WhatsApp apply buttons |
| 2.3.0 | 27 Aug 2026 | Academy + case study merged into one page. Team / Network / Founder sections. Automation deep-dive (8 blocks). Reframed around 3 lakh leads. TOI press feature |
| 2.2.0 | 27 Aug 2026 | Case study page built. LUCADEMY rename. Academy repositioned from selling → enquiry-only |
| 2.1.0 | 22 Mar 2026 | SEO/perf/a11y pass: OG tags, JSON-LD, favicon, async fonts, lazy iframes, skip links, hamburger nav, cookie banner, WCAG contrast fix, 404 page |
| 2.0.0 | 22 Mar 2026 | Parent/child structure. 4 policy pages. robots.txt + sitemap.xml |
| 1.2.0 | 21 Mar 2026 | PhotoBooks page — 3 design directions explored, mid-tone version chosen |
| 1.1.0 | 6 Mar 2026 | Light "classy" direction adopted (dark tech direction rejected) |
| 1.0.0 | 6 Mar 2026 | Initial redesign |

**Versioning rule going forward:**
- **Patch** (x.x.1) — copy edits, link fixes, small tweaks
- **Minor** (x.1.0) — new sections, new features on existing pages
- **Major** (3.0.0) — new pages, structural changes, design system changes

When bumping: update `VERSION` file, the banner comment in every HTML file, `<meta name="version">`, and this table.

---

## 9. Working Conventions

**Writing style for this site:**
- Plain, direct sentences. No marketing fluff.
- Honest numbers beat inflated ones — the funnel section works *because* it admits 98% didn't convert
- Indian number formatting where natural (3,00,000 / ₹8,000 / lakh)
- British-Indian spelling: "organised", "personalised", "recognised"

**Things the client has explicitly rejected:**
- Dark "tech startup" aesthetic (v1.0) — "not some fancy tech company"
- Gaudy / busy layouts — "premium websites are always less gaudy"
- Emoji on careers page
- Pill-button styling for the Recordings nav link (reverted to plain text link)
- CTA button in homepage nav

**Things the client values:**
- Multi-venture exposure being visible
- The founder story landing as genuinely impressive without reading as self-congratulation
- Direct WhatsApp contact over forms/portals wherever possible
- SEO that an IIM-A / IIT / Ivy League audience would respect

---

## 10. Quick Commands

```bash
# Validate all JSON-LD on a page
python3 -c "
import re,json
h=open('careers.html').read()
for m in re.finditer(r'<script type=\"application/ld\+json\">(.*?)</script>', h, re.DOTALL):
    json.loads(m.group(1)); print('valid')
"

# Find broken placeholder links
grep -o 'href=\"#\"' *.html | sort | uniq -c

# Check version consistency
grep -h 'name=\"version\"' *.html | sort | uniq -c

# Package for deploy
cd .. && zip -r ludifu-site-v2.5.0.zip ludifu-site -x "*.DS_Store"
```

---

*End of handover — LUDIFU Website v2.22.0*
