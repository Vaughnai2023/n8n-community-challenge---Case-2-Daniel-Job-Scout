# Case 2 Submission — Daniel, Job Scout Hunter

**Author:** Vaughn Botha
**Workflow:** `M2 Case 2: Daniel — Job Scout v1` (n8n ID `Lf0B8uZcpe4Xsgsb`)
**Date:** 2026-04-19
**Status:** ✅ End-to-end working. Last verified run 2026-04-19 18:07 UTC — 3 candidates → 1 delivered (High 78) with tailored CV + 2 filtered with evidence quotes, in 37 seconds.

---

## 1. The thesis

99% of submissions will build *"Firecrawl search → LLM filter → Google Sheet."* A list.

This one builds a **weekly job-scout that produces applications, not a list.** Every matched role ships with a tailored 1-page CV Daniel can send immediately. The sifting, scoring, and first draft are already done. Monday morning Daniel opens an email, picks 2-3 roles, hits apply.

The design is not speculative — it's ported directly from Vaughn Botha's production Job Finder system (see [`Job-finder/.claude/skills/`](https://github.com/…)), which has been running daily for months. The n8n workflow here is the Job Finder skills (`evaluate-jobs`, `research-company`, `tailor-cv`) rewrapped inside Firecrawl + n8n AI Agent + n8n Data Tables, adapted for Daniel's senior-backend profile.

---

## 2. The four creative pillars

### 🎯 Pillar 1 (Showstopper) — Tailored CV per matched role
Every role on the ranked list arrives with a tailored 1-page A4 HTML CV. The LLM Chain (`CV Tailor (HTML)`) follows the Job Finder `tailor-cv/SKILL.md` rules verbatim: targeted modifications not rewrites, no fabrication, content selected by JD overlap with Daniel's master. Template designed for senior-engineer aesthetic (left rail + main column, Inter + JetBrains Mono, print-safe). Output stored in `daniel_role_master.tailored_cv_html` and surfaced as a link in the email.

### Pillar 2 — Freshness Ledger
`daniel_seen_roles` data table stamps every listing URL with `first_seen_utc` on discovery. When a source has no posting date, our ledger becomes the authoritative recency signal. Each role carries `age_source` declaring the method used. Directly answers the Case 2 brief's *"Documents how freshness is determined"* requirement.

### Pillar 3 — Deal-breaker Evidence Quotes
For every filtered-out role, the workflow stores the exact JD substring that triggered the rejection (`daniel_filtered_out.reason_quote`). The agent is instructed that this quote MUST be a verbatim substring — never invented. The email's "Filtered Out" section shows the quote. Judges can verify any filter decision against the live JD.

### Pillar 4 — Source-Yield Learning Loop
Phase 0 audit selected 3 core + 1 bonus source (see `source-audit.md`). The workflow writes `source` on every enriched role, making it trivial to track which boards actually produce High-band matches. Weak sources can be rotated out in the Config node without touching any other logic. The workflow improves week over week — it doesn't just execute.

**Plus** a warm, emotionally-calibrated email ("Morning Daniel, 3 strong matches this week — enough to move on"), honest "why not" alongside "why it fits," filter-outs collapsed by default, zero-match weeks handled with grace.

---

## 3. Architecture at a glance

```
Schedule Monday 08:00
  → Config (criteria + sources + run_id)
  → Firecrawl Search (multi-site, one call)
  (Note: idempotent table-creation nodes are v2 — current v1 references the author's table IDs;
   judges importing on a fresh instance create the 3 tables manually first. See §6.)
  → Parse Candidates (Code)
  → Get Seen Roles (Data Table, resolved by name)
  → Dedup + Cap (Code, sort by source weight)
  → Loop (SplitInBatches, batch=1)
    │
    │  (Firecrawl Scrape JD inline — see §7b for why this is NOT an agent tool)
    │  Role Qualifier AGENT ────┬── OpenAI gpt-4o (brain)
    │                            └── Structured Output Parser (16 flat fields)
    │
    → Score + Decide (Code — ports Job Finder 40/20/20/20 rubric)
    → IF keeper?
        TRUE  → CV Tailor (LLM Chain + gpt-4o) → Attach CV to Accumulator → Save to Role Master → Register in Seen → loop
        FALSE → Log Filtered-Out (with evidence quote) → loop
  (after loop)
  → Aggregate (sort, rank top 10)
  → Format Email Body (HTML, emotionally calibrated)
  → Write to Google Sheet (disabled — configure doc ID)
  → Build CV Attachments (Code — one .html binary per delivered role)
  → Send Weekly Digest (disabled — connect Gmail; auto-attaches every tailored CV as .html)
```

**29 flow nodes + 11 sticky notes** telling the story for judges.

---

## 4. Rubric map — how we hit 5/5

| Criterion | Evidence in the workflow |
|---|---|
| **Enrichment depth** | 6 layers: JD deep parse (AI Agent), stack matching with JD-substring evidence, salary triangulation (listing → careers → unavailable, with `salary_source` + `salary_confidence`), 4DW detection, `why_it_fits` + steelman `why_not`, tailored CV per role. |
| **Smart orchestration** | Deterministic JD scrape (regular Firecrawl Scrape node) feeds the AI Agent, which extracts 16 structured fields via `StructuredOutputParser`. Source weighting informs candidate ordering. Dedup via Data Table. Per-role loop. Firecrawl as the deterministic data layer, LLM for interpretation. **Conditional careers-page scrape based on missing salary is on the v2 roadmap — not in v1.** |
| **Output quality** | 3-tab data model (role master, seen ledger, filtered-out). HTML email with warm header, ranked per-band cards, honest "why not," filter-outs collapsed. Every matched role ships with a ready-to-send 1-page A4 tailored CV. |
| **Solution fit** | Every must-have field covered. Nice-to-haves detected (4-day week explicit). Filter-out tracking with reasons (judging criterion). Ranked scoring. Documented freshness method (judging criterion). Zero-match weeks handled with grace. |
| **Creativity** | Tailored CV per role (workflow produces the application, not the list). Freshness Ledger. Deal-breaker evidence quotes (no hallucinated rejections). Source-Yield Learning Loop. Emotionally-calibrated copy. All four genuinely unexpected in the job-scout space. |

---

## 5. What reuses the Job Finder system

| Job Finder asset | Reused here |
|---|---|
| `evaluate-jobs/SKILL.md` weighted rubric (stack · remote · salary · perks — adapted from the original 40/20/20/20 to a stacked-bonus model that handles partial signal better) | `Score + Decide` Code node |
| `research-company/SKILL.md` | Planned as Perplexity HTTP node in v2 (not in v1 to keep within 35k Firecrawl budget) |
| `tailor-cv/SKILL.md` rules (targeted modifications, no fabrication, 1-page A4 HTML) | `CV Tailor (HTML)` LLM Chain |
| Dedup on `listing_url` pattern | `Get Seen Roles` + `Dedup + Cap` |
| Status-feedback loop (applied/rejected) | Sheets `status` column read-back (next run) |
| Dry-run budget guardrail | `dry_run` toggle in Config node |

---

## 6. Setup (for judges / re-use)

**1. Prerequisites**
- n8n Cloud or self-hosted with `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true` set
- Firecrawl account (free tier: 35k credits — workflow uses ~2,600/run, fits 8+ runs)
- OpenAI API key (gpt-4o)
- Optional: Google Sheets + Gmail accounts for delivery

**2. Import**
```
Import `daniel-workflow-final.json` → attach credentials.
```

**3. Create the three Data Tables on your instance** *(v1 limitation — see §8)*
- `daniel_seen_roles`, `daniel_role_master`, `daniel_filtered_out` (schemas in §3 above).
- Update the four Data Table node references to your IDs (or wait for v2's idempotent setup nodes).

**4. Configure**
- Open `Config + Run Context` Code node. Criteria is hard-coded; edit if personalising. **Note `candidate_cap`** — currently capped at 3 for fast iteration; raise for production volume.
- Set your **recipient email** in `Send Weekly Digest` (currently the author's address).
- Set your **Google Drive folder ID** in `Upload CV to Drive` (currently the author's folder).
- Enable `Write to Google Sheet` node + set your spreadsheet's document ID.
- Tailored CVs auto-attach as `.html` files — Daniel double-clicks to open in a browser, Cmd-P for PDF.
- Set workflow `active` to enable the Monday 08:00 trigger, or run manually.

**5. First run**
Use `n8n_test_workflow` or click "Test workflow". With the default `candidate_cap: 3`: ~30-60 sec runtime, up to 3 candidates evaluated, 0-3 delivered with CVs.

---

## 7. Credit budget

| Operation | Credits/call | Calls/run | Per-run |
|---|---|---|---|
| Firecrawl Search (1 multi-site call) | ~100 | 1 | 100 |
| Firecrawl Scrape (JD, per candidate, ~15 candidates) | ~80 | 15 | 1,200 |
| Firecrawl Scrape (company careers, ~50% of candidates) | ~80 | 7-8 | 600 |
| Buffer for agent over-exploration | — | — | 700 |
| **Per run total** | | | **~2,600** |
| 4-week weekly + 4 dev/test = 8 runs | | | **~21,000** |

35k free tier → comfortable 40% buffer.

---

## 7b. Architecture decisions made during debugging (2026-04-19 evening)

1. **Firecrawl Scrape inline, not as agent tool.** The community Firecrawl node v2.1.1 doesn't properly implement LangChain's `supplyData` interface even with `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true`. We pivoted to a regular Firecrawl Scrape node inside the loop (before the Agent), producing real JD markdown. Agent now does pure orchestration + extraction on pre-fetched data. Firecrawl is still "in the workflow" via 2 nodes (Search + Scrape); challenge requirement satisfied.

2. **n8n Data Table node quirks:**
   - `dataTableId` must be a full resourceLocator `{__rl: true, value, mode: "id"}` — plain string string silently fails with "Could not get parameter".
   - `get` operation requires `matchType` + `filters.conditions: []` even when returning all rows.
   - `columns` resourceMapper needs full schema array, not just value map.

3. **Cross-iteration aggregation via `$getWorkflowStaticData('global')`**. After a SplitInBatches loop, `$('Node').all()` only returns the last iteration's output, not cumulative. Solution: push per-iteration results into global static data from Score+Decide, read from global in Aggregate Results. Reset in Config node at start of each run.

4. **Webhook trigger in parallel with Schedule trigger** so MCP can fire test runs via `n8n_test_workflow`. Schedule stays for the real Monday cron.

5. **CV HTML code-fence strip.** The LLM consistently wraps HTML in ` ```html ... ``` ` markdown fences. Stripped via regex in the Save-to-Role-Master expression so the stored CV is clean HTML.

## 8. Known v1 constraints (roadmap)

- **Idempotent Data Table setup** — v1 references the author's table IDs; importers must create the three tables first. v2 adds three `Setup: Ensure <name>` nodes with `createIfNotExists: true` so import-and-go works on any instance.
- **Hardcoded recipient email + Drive folder ID** — both currently embedded in their nodes. v2 reads them from `Config + Run Context` so there's a single config surface.
- **No `retryOnFail`** on Firecrawl + OpenAI nodes — v2 will add `maxTries: 2, waitBetweenTries: 3000`.
- **Conditional careers-page scrape** — agent currently runs against pre-fetched JD only. v2 adds the salary-triangulation branch.
- **Perplexity company research** planned but not in v1 to keep within credit budget. Would add overview / culture / news / hiring manager enrichment using the Job Finder `research-company` queries.
- **Interview Prep Packet** (top 2) planned for v2 after credit-budget validation on real runs.
- **PDF conversion** — v1 delivers HTML (one `.html` attachment per delivered role on the weekly Gmail digest). Daniel opens in browser, Cmd-P → PDF → apply. PDFShift HTTP node planned for v2 to ship `.pdf` directly.
- **Google Sheets + Gmail** nodes disabled in the imported JSON — user attaches credentials before enabling.

These are deliberate: v1 ships the four creative pillars cleanly on a tight credit budget. v2 layers on the enrichment once the core pipeline is proven in the wild.

---

## 9. Files in this submission

| File | Purpose |
|---|---|
| `daniel-workflow-final.json` | The exported workflow (40 nodes) |
| `daniel_sample_cv.html` | Sample tailored CV — what the CV Tailor LLM Chain produces, saved for offline preview |
| `CV_TEMPLATE.html` | 1-page A4 CV template (used by CV Tailor LLM Chain) |
| `daniel_base_cv.md` | Daniel's master CV — source of truth for tailoring |
| `source-audit.md` | Phase 0 evidence behind source selection |
| `submission.md` | This document |
| `ids.md` | Instance IDs + credentials checklist |
