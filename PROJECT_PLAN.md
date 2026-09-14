# LUDIFU — Founder Story & Venture Pages
## Project Plan + Information Intake

**Prepared:** 12 September 2026
**Current site version:** v2.6.0
**Target version on completion:** v3.0.0 (major — new page architecture)

---

## 1. Honest Recommendation First

**Do not give all 17 ventures a full page.**

A page with three thin paragraphs actively damages credibility — an investor clicks it, finds nothing, and starts discounting everything else. Bid2Splash ran for one year as a penny auction. That deserves one honest line on a timeline, not a page with invented depth.

The material you have is uneven, and that is normal. So the architecture should be tiered:

| Tier | Treatment | Ventures |
|---|---|---|
| **Tier 1** | Full dedicated page | CondomPoint · 22SEO · LUDIFU PhotoBooks · LUCADEMY *(exists)* · Unified Stores · Unified Florists |
| **Tier 2** | Rich card on ventures index + timeline entry | CouponZatak · My Pet Centre · Unified Papers · The Leaf · Print World · Paper Print Services |
| **Tier 3** | Timeline entry only | Bid2Splash · Unified Prints |
| **External** | Link out to own site | Clicarity · WA.Expert · ClickToWish |

Tier can be promoted later as you find more material. Starting a venture in Tier 2 and moving it up is easy. Publishing a thin Tier 1 page and quietly deleting it is not.

---

## 2. Proposed Page Architecture

```
founder.html          The person — lineage, education, thesis  [EXISTS v2.6.0]
  │
timeline.html         ⭐ The centrepiece — interactive, scroll-driven
  │                      1987 → today, every venture, every publication
  │
ventures.html         Index of all 17 — filterable grid
  │                      (by decade · by outcome · by category)
  ├── ventures/condompoint.html
  ├── ventures/22seo.html
  ├── ventures/photobooks.html
  ├── ventures/unified-stores.html
  ├── ventures/unified-florists.html
  └── academy.html   (already live)
  │
press.html            Every publication, every venture, chronological
```

**Navigation change:** the top nav gains a **"The Journey"** item that opens to timeline / ventures / founder / press.

**Cross-linking rule:** every venture name mentioned anywhere on the site links to its page or its index card. Every publication mentioned links to press.html. No dead mentions.

---

## 3. The Timeline — Design Direction

You asked for something fancy and trendy for a young audience, that still reads seriously to an investor. Those pull in opposite directions, so here is how I would resolve it:

**Structure:** vertical scroll-driven timeline, 1987 → 2026. Entries alternate left/right on desktop, single column on mobile.

**What makes it feel modern without being juvenile:**
- Entries fade and rise into view as you scroll (CSS `@scroll-timeline` with IntersectionObserver fallback — no library)
- A thin progress rail down the centre that fills as you descend
- Year markers that pin briefly as you pass them
- Ventures render as cards; publications render as inline badges on the rail; personal milestones as small dots
- Colour-coded by outcome: operating (forest) · closed (stone) · family business (gold)
- A sticky filter at top: **All · Ventures · Press · Milestones**

**What keeps it investor-credible:**
- Every entry carries a real date
- Numbers appear inline, not as decoration
- Closed ventures are visually equal to operating ones — not hidden or greyed into shame
- One-line lesson on every closure

**Performance:** pure CSS + one small IntersectionObserver. No scroll library, no GSAP. Stays under the 2MB budget and keeps the PageSpeed score.

---

## 4. Session Plan

Realistic estimate: **4 to 6 working sessions**, depending entirely on how quickly Section 5 gets filled in.

| Session | Deliverable | Blocked by |
|---|---|---|
| **1** | `timeline.html` — full interactive timeline, all 17 ventures + 6 publications + personal milestones. Nav restructure. | Confirmed dates (Section 5A) |
| **2** | `ventures.html` index + filterable grid. Wayback snapshot recovery for old sites. | Nothing — can run on existing data |
| **3** | Tier 1 venture pages ×3 (CondomPoint, 22SEO, PhotoBooks) | Venture detail (Section 5B) |
| **4** | Tier 1 venture pages ×2–3 (Unified Stores, Unified Florists, + any promoted) | Venture detail (Section 5B) |
| **5** | `press.html` + full cross-linking pass + sitemap/schema | Publication scans (Section 5C) |
| **6** | *Buffer* — polish, mobile QA, PageSpeed pass, v3.0.0 release | — |

**Sessions 1 and 2 can start immediately** with what I already have. Sessions 3–5 need your input.

If you can only give me one thing to unblock the most work: **confirmed dates.** They affect the timeline, every venture page, and the founder page that is already live.

---

## 5. What I Need From You

### 5A — Dates (BLOCKING, highest priority)

Your two documents contradict each other on six ventures. Currently the site uses the Family_BackGround dates. Confirm or correct:

**There are now FOUR conflicting sources.** They cannot all be right.

| Venture | Profile doc | Family doc (~2018) | Pasted text (~2013) | 2017 Deck | Site uses |
|---|---|---|---|---|---|
| Unified Florists | 2008–2010 | Jun 2009–Jun 2010 | Jun 2010–Present | **2006–2007** | 2009–2010 |
| CondomPoint | 2008–Present | Jun 2011–Jun 2016 | Jun 2011–Present | Dormant | 2011–2016 |
| 22SEO | 2008–2014 | Dec 2011–Jun 2015 | — | **2009–2014** | 2011–2015 |
| CouponZatak | 2009–2010 | May 2012–Dec 2014 | May 2012–Present | **2009–2010** | 2012–2014 |
| Unified Stores | 2009–2014 | Sep 2011–Dec 2014 | Sep 2011–Present | **2008–2011** | 2011–2014 |
| My Pet Centre | 2010–2014 | Dec 2011–Dec 2014 | Dec 2011–Present | **2009–2010** | 2011–2014 |

**Analysis:** The Family doc and the ~2013 pasted text *corroborate each other* on start dates (CondomPoint Jun 2011, CouponZatak May 2012, Unified Stores Sep 2011, My Pet Centre Dec 2011). The 2017 deck disagrees with both, and the Profile doc disagrees with everything.

**Recommendation:** keep the current site dates (Family doc), since two independent documents agree on them. But this needs a single decision from you — **pick one canonical set and we use it everywhere.**

Also needed:
- **The Leaf** — actual end date? (currently assumed 2019)
- **Penn State** — 2001–2004 or 2001–2005?
- **Bid2Splash** — start and end months?
- **Unified Papers** — did it launch, or stop at concept?

---

### 5B — Per-Venture Detail

For each **Tier 1** venture, copy this block and fill what you can. Blank fields are fine — I would rather have five honest facts than fifteen guesses.

```
VENTURE: ________________

1. WHY IT STARTED
   What was the trigger? What did you see that made you think this was worth doing?

2. HOW IT ACTUALLY WORKED
   The mechanics. Who were the customers, how did they find you, what did they pay,
   how did the money move, who did the work?

3. NUMBERS (any you have — approximate is fine, say so)
   - Revenue / GMV at peak:
   - Customers or orders (total or monthly):
   - Traffic at peak:
   - Team size:
   - Total money spent building it:
   - Best month, and why:

4. THE HIGH POINT
   The moment it felt like it was working.

5. WHY IT ENDED
   The honest version. Market? Margin? Attention? Something broke?

6. WHAT IT TAUGHT
   One or two sentences. This is the most important field on the form.

7. WHERE IT SHOWS UP NOW
   Does a lesson from this venture live inside Clicarity, WA.Expert or how you operate?

8. ASSETS
   - Old logo / screenshots:
   - Press links:
   - Social pages still live:
   - Anything else (old decks, invoices, packaging, photos):
```

---

### 5C — Publications

For each of the six confirmed publications, I need whichever of these you have:

| Publication | Date | Need |
|---|---|---|
| Times of India | 25 Aug 2020 | ✅ Have PDF + photo |
| Hindustan Times | 25 Feb 2017, HT DO p11 | ☐ Scan or photo of the page |
| BW Disrupt | 15 Feb 2017 | ✅ Live URL confirmed |
| Mid-day | Holi weekend 2017 | ☐ Scan, date, headline |
| LBB | Feb 2017 | ☐ Link if still live |
| PrintWeek | Apr 2026 | ☐ Link or scan |
| Print Bulletin | May 2026 | ☐ Link or scan |

**Also worth asking:** were any of the *earlier* ventures covered anywhere? CondomPoint ran for five years with top-3 rankings and a Prithvi Theatre sponsorship — that often attracts coverage. Anything in trade press, blogs, or college publications counts.

---

### 5D — ✅ RECEIVED: The "Successful Failures" Deck

`LUDIFU_-_PUNEET_RAWAT.pptx` (March 2017, 21 slides) has been received and mined. It resolved several open questions and added major material:

**Resolved:**
- **Bid2Splash never launched.** Slide 1 lists it as "Did not Launch". Site corrected.
- **Intern growth curve established:** 196 (Mar 2017) → 700+ (2018) → thousands (2023). The 4,500 figure is now plausible rather than unverified.
- **LUDIFU launch date: 23 December 2016.** Seeded by GrooveBook on Shark Tank, March 2016.
- **LUDIFU was angel funded** — first round from a family member.
- **Original price ₹199** (not ₹399 as BW Disrupt reported, or ₹1,999 on the current Play listing — price evolved across three stages).
- **App downloads at Mar 2017:** Android 1,550 · iPhone 200.

**Major new material now on `founder.html`:**
- **The PrintBell / VistaPrint story** — offered 2% in 2007, refused it, PrintBell became VistaPrint India. This is now its own section and is arguably the strongest thing on the site.
- **Contemporaneous marketing lessons** — theatre ads, Fiverr, college sponsorship, honest product cons — quoted from the deck rather than reconstructed.

**Still worth having from the deck:** the two videos (Promo, and the unreleased DDLJ one), the publications screenshot on slide 18, the Yountre and downloads screenshots.

---

### 5E — Visual Assets

- A current professional photograph of you *(the founder page has no image — it needs one)*
- Any logos from the old ventures
- Photos of physical things: the printing press, the photobooks, the Prithvi play sponsorship, the Dog Fair stall, the restaurant
- **`og-image.jpg` at 1200×630** — still outstanding from v2.1.0 and blocking every social share on the site

---

## 6. What I Can Do Without You

Starting immediately, no input needed:

- Build the timeline structure using confirmed dates, leaving disputed ones flagged
- Recover archived snapshots of CondomPoint, CouponZatak, MyPetCentre, UnifiedStores, 22SEO and UnifiedFlorists from the Wayback Machine
- Pull the BW Disrupt article content properly
- Build `ventures.html` index from existing material
- Restructure navigation
- Write the Tier 2 and Tier 3 entries in full

That is genuinely Sessions 1 and 2 complete before you send me anything.

---

## 7. A Note on Investor Framing

You said the purpose is to show an investor neatly without losing them in data, while numbers still carry weight. The resolution is **layering**:

- **Timeline** = the shape of the story. Scannable in 90 seconds.
- **Ventures index** = the breadth. Scannable in 3 minutes.
- **Venture pages** = the depth. Only for those who want it.
- **Founder page** = the thesis. Why any of it matters.

An investor who spends 90 seconds should leave with: *third-generation operator, seventeen ventures, learned in public, current products built on specific earned lessons.*

An investor who spends 30 minutes should find that every claim in those 90 seconds holds up.

That is the design goal. Everything above serves it.

---

*LUDIFU — Project Plan v1.0 · prepared alongside site v2.6.0*
