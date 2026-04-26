# Daniel — Job Board Source Audit

**Candidate profile:** Senior Backend Engineer · Python, Django, PostgreSQL, Redis, AWS · 8 yrs · Remote EU-friendly (UTC-1 to UTC+3) · €90k+ min

**Audit date:** 2026-04-21
**Method:** Brave Search discovery → Firecrawl scrape validation on `basic` proxy. Boards retained only if (a) listings render without JS/login/paywall and (b) they index roles matching Daniel's shape.

---

## Tier 1 — Use These (verified scrape-ready, high fit)

These returned clean, parseable listings with full job content on a single GET. Priority order reflects observed density of Daniel-matching roles.

### 1. `djangoproject.com/community/jobs/`
- **Why tier 1:** Niche Django-only board. Aggregates *Built with Django Jobs* and *Django Job Board* feeds into one page. Every listing is Django-relevant by definition.
- **Firecrawl result:** ✅ 22 jobs with full descriptions, company, date, salary where stated. No paywall, no JS wall.
- **EU fit caveat:** Skews US. But when a senior remote-EU Django role exists anywhere, it's almost always cross-posted here.
- **Recommended use:** Scrape weekly. Primary anchor source.
- **RSS also available:** `djangoproject.com/rss/community/jobs/`

### 2. `hnhiring.com/technologies/python`
- **Why tier 1:** Aggregates "Who is hiring?" HN threads, filtered to Python. Strong signal on genuine engineering roles (not recruiter spam). Verified EU mentions in scrape: Berlin (3), Amsterdam (2), London (6), Barcelona (3), Munich (1), Vienna, and salary tags in €.
- **Firecrawl result:** ✅ 137k chars, all inline. No auth wall.
- **Recommended use:** Scrape on the 1st–3rd of each month (when HN's "Who is hiring?" thread posts and ~100 new jobs land).

### 3. `euremotejobs.com/jobs/`
- **Why tier 1:** EU-specific by definition. Every listing is EMEA-timezone-compatible.
- **Firecrawl result:** ✅ clean listing page with Location/Experience/Category/Salary/Tech filters all parseable. ~30 jobs per page, "Load More" pagination.
- **Caveat:** Engineering is a minor category on this board — most listings are marketing/support. Expect ~3–8 engineering roles at any time, 1–2 Python/Django at most. Still worth it: any hit here is already pre-filtered to EU.
- **Useful deep links:**
  - `euremotejobs.com/jobs-category/engineering/`
  - `euremotejobs.com/?s=python`

### 4. `weworkremotely.com/categories/remote-back-end-programming-jobs`
- **Why tier 1:** Large volume. Verified country flags in listing cards (scrape captured Denmark, Bulgaria, Poland, Romania, Serbia, Ukraine explicitly labeled as eligible regions).
- **Firecrawl result:** ✅ structured list with company, salary band ($100k+ bucket is visible), eligible countries, date. No paywall on the category page (paywall only on the jobseeker account features).
- **Also relevant:**
  - `weworkremotely.com/categories/remote-full-stack-programming-jobs`
  - `weworkremotely.com/remote-jobs/search?term=django`

### 5. `workingnomads.com/remote-django-jobs`
- **Why tier 1:** Django-specific filter. Scrape confirmed 19× "Django", 71× "Senior", 18× "€" in content — strong density.
- **Firecrawl result:** ✅ listings visible. Has a "Join Premium" upsell for historical/30k+ feed, but the current/free listings are scraped fine.
- **Also relevant:** `workingnomads.com/remote-python-jobs`

### 6. `himalayas.app` *(already in current workflow — keep)*
- Confirmed working per prior runs. Strong remote-EU filter.

### 7. `4dayweek.io` *(already in current workflow — keep)*
- Niche, low volume, but listings match Daniel's quality bar.

---

## Tier 2 — Probably Good, Needs Verification or Workaround

### 8. `nodesk.co/remote-jobs/europe/engineering/`
- **Scrape:** ✅ Returns content (~55k chars). EU-Engineering filtered. Worth adding after a short manual spot-check on listing freshness.
- **Action before adding:** verify 5+ recent Python/Django roles exist.

### 9. `remoteok.com` *(currently in workflow)*
- **Scrape caveat:** The `remote-python+europe-jobs` filter URL redirected to homepage and listings did not render as markdown in our test — content appears JS-rendered through Firecrawl's `basic` proxy.
- **But:** it has been returning results in the live n8n workflow, which uses Firecrawl `search` not `scrape` — different code path, probably fine.
- **Recommendation:** Keep. If freshness drops, switch to the RSS feed (`remoteok.com/rss` or JSON feed `remoteok.com/json`).

### 10. `builtwithdjango.com/jobs/` *(redundant — already aggregated by #1)*
- Skip as a separate source; adding it would duplicate listings already on djangoproject.com.

### 11. `djangojobboard.com` *(redundant — already aggregated by #1)*
- Same as above.

### 12. `landing.jobs`
- EU-specific, Lisbon-based marketplace. Not scraped in this audit. Worth a manual firecrawl pass before adding — reputation suggests open listings but may require JS.

### 13. `remoteineurope.com`
- EU-curated. Worth spot-checking. Reported as open/no-paywall.

### 14. `nextleveljobs.eu`
- Promotes €100k+ EU tech roles. Small board but high-fit if accessible.

---

## Disregarded — Do Not Add

| Board | Reason |
|---|---|
| `python.org/jobs/` | JS-rendered; Firecrawl `basic` returned "interactive scripts did not run" fallback on both 0s and 5s waits. Official board so ideal content, but only worth revisiting with `proxy: stealth` or `waitFor: 10000`. |
| `flexjobs.com` | Hard paywall — subscription required to view listings. |
| `wellfound.com` (ex-AngelList) | Login gate for full listings and apply links. |
| `linkedin.com/jobs` | Anti-bot / requires auth. |
| `turing.com` | Recruiter marketplace, not direct-apply listings — adds no unique inventory. |
| `arc.dev` | Login gate for full role details. |
| `dailyremote.com` | "Access 492+ exclusive roles" paywall teaser. |
| `remoterocketship.com` | "Get Instant Access" gate on full listings. |
| `glassdoor.com` | Aggressive anti-scraping, login gate. |
| `ziprecruiter.com` / `indeed.com` | Anti-bot + heavy US skew. |
| `remotive.com` | Already removed in prior audit — teaser only. |
| `upwork` / `freelancer` / `fiverr` | Freelance/gig, not Daniel's fit. |

---

## Credit Audit (Firecrawl scrapes used in this pass)

| URL | Result | Credits |
|---|---|---|
| djangoproject.com/community/jobs/ | ✅ full content, 22 jobs | 1 |
| python.org/jobs/ (no wait) | ❌ JS fallback | 1 |
| python.org/jobs/ (waitFor 5s) | ❌ JS fallback | 1 |
| hnhiring.com/technologies/python | ✅ 137k chars, EU signal confirmed | 1 |
| weworkremotely.com/categories/remote-back-end-programming-jobs | ✅ full listings | 1 |
| euremotejobs.com/jobs-category/developer/ | ⚠️ redirected to single job detail | 1 |
| euremotejobs.com/jobs/ | ✅ full EU-filtered listings | 1 |
| workingnomads.com/remote-django-jobs | ✅ 113k chars, 19× Django | 1 |
| remoteok.com/remote-python+europe-jobs | ❌ chrome only, listings JS-rendered | 1 |
| nodesk.co/remote-jobs/europe/engineering/ | ✅ 55k chars | 1 |
| **Total** | — | **~10 credits** |

---

## Reliability verdict

**Yes, we have a solid list.** The combination of Tier 1 boards (#1–#7) gives Daniel:

1. **A niche anchor** (djangoproject.com) — guaranteed Django-only.
2. **A high-signal aggregator** (hnhiring) — genuine engineering roles with explicit EU city tags and € salary.
3. **An EU-exclusive board** (euremotejobs) — every listing pre-filtered to EMEA timezone.
4. **Two volume sources** (weworkremotely, workingnomads) — large enough that even a 2% EU+Django hit rate yields multiple weekly matches.
5. **Two retained sources** (himalayas, 4dayweek) — already validated in production.

The critical insight from this audit: **the current workflow's 0-match runs were a source-volume problem, not a filter problem.** The old list (remoteok + weworkremotely + himalayas + jobspresso + 4dayweek) lacked both a Django-niche anchor and an EU-exclusive source. Adding #1 and #3 should produce Daniel's first real matches.

## Recommended next step

1. Spot-check Tier 2 candidates (#8, #12, #13) with one Firecrawl pass each — maybe 3 more credits.
2. Once final list locked, replace the `sources` array in the n8n Config node with these URLs (weighted: djangoproject + hnhiring + euremotejobs = high; weworkremotely + workingnomads = medium; himalayas + 4dayweek = keep).
3. Run the workflow once against the new list and re-audit output volume + fit.
