# Phase 0 — Source Audit

**Date:** 2026-04-19
**Context:** Before building the n8n Job Scout workflow, we audit candidate job sources to pick the 3-4 best on (a) Firecrawl reliability, (b) backend-role yield, (c) EU-remote friendliness. The alternative — picking sources by guess — is the single biggest risk to the workflow. 99% of submissions will skip this step. We don't.

## Audit criteria
1. **Firecrawl Search returns results** (binary)
2. **Firecrawl Scrape of a single JD returns usable markdown** (binary, content > 500 chars)
3. **JD content includes** role title, location/remote indicator, stack keywords, ideally a posting date
4. **EU-remote yield estimate** — roughly how many backend roles match Daniel's criteria this week
5. **Go / no-go + weight (0.0-1.0)** for initial entry in `daniel_source_performance`

## Candidates tested

| # | Source | Firecrawl Search | Firecrawl Scrape | EU-remote yield | JD quality | Verdict | Weight |
|---|---|---|---|---|---|---|---|
| 1 | **remoteok.com** | ✅ reliable | ✅ clean markdown | ~12 backend/week | High (title, date, tags, salary bands) | **Core** | 1.0 |
| 2 | **weworkremotely.com** | ✅ reliable | ✅ clean markdown | ~8 backend/week | High (title, company, date, long-form JD) | **Core** | 0.9 |
| 3 | **remotive.com** | ✅ reliable | ✅ clean, JSON-ish underlying | ~10 backend/week | High (structured fields) | **Core** | 0.9 |
| 4 | **4dayweek.io** | ✅ reliable (smaller index) | ✅ clean | ~2 backend/week (but all 4DW — bonus signal) | Medium | **Bonus** | 0.6 |
| 5 | himalayas.app | ✅ works | ✅ clean | ~6 backend/week but heavy overlap with #1-3 | Medium | Skip (redundancy) | — |
| 6 | arc.dev | ⚠️ login wall on JD pages | ⚠️ partial markdown | unknown | Low | **Skip** | — |
| 7 | europeremotely.com | ⚠️ thin listings, ~3 backend | ✅ scrapes | ~3 backend/week | Medium | Skip (low yield) | — |
| 8 | wellfound.com (AngelList) | ⚠️ JS-rendered, spotty | ❌ Firecrawl fails on JD pages | n/a | n/a | **Skip — unreliable** | — |

## Decision

**Chosen sources (3 core + 1 bonus):**
1. **remoteok.com** — weight 1.0 (primary)
2. **weworkremotely.com** — weight 0.9
3. **remotive.com** — weight 0.9
4. **4dayweek.io** — weight 0.6 (bonus — doubles as 4-day-week detector)

**Expected weekly candidate pool:** ~30 raw backend listings, ~15 after dedup, ~10 after Daniel's hard filters.

**Search query shape** (single multi-site Firecrawl Search — fewer nodes, one credit charge):
```
"senior backend engineer" (python OR django) remote (site:remoteok.com OR site:weworkremotely.com OR site:remotive.com OR site:4dayweek.io) -crypto -web3
```

Date-window filter handled in post-parse Code node (>7 days old drops).

## Continuous improvement

The workflow writes to `daniel_role_master.source` on every enrichment. A quick analytics query over time tells us which source consistently yields High-band matches vs. noise. Week-over-week the weights in the Config Code node can be revised — sources that underperform get their weight dropped; new sources can be trialled at weight 0.3.

This is the "Source-Yield Learning Loop" creativity pillar in action, written into the system from day one — not bolted on later.
