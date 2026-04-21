# Judges' Feedback — Workflow Changes Queued for Approval

Three judges reviewed the initial commit. Doc/README fixes have been applied. Workflow-JSON changes are listed below for your decision before I touch the n8n flow.

| Judge | Score | Headline |
|---|---|---|
| Storytelling | **8.5/10** | Strong narrative, clean wow moment — sources/screenshots gaps |
| Technical | **7.5/10** | Real engineering, but workflow self-contradicts the docs in places |
| n8n best-practices | **6.5/10** | "Zero-touch import" claim was materially false; hardcoded IDs |

---

## 🔴 Critical (would block community-template feature)

### 1. Add idempotent Data Table setup nodes
- **Issue:** README + submission claimed "tables auto-create on first run via `createIfNotExists: true`." No such nodes exist in the JSON. Data Table nodes reference hardcoded IDs (`hYVM1BcLgvLXRRZH`, `STCIGAGYetQlDOiC`, `Xvfz1mJVl4egDPK4`). On import to any other instance: every Data Table node fails.
- **Fix:** Add 3 × `dataTable` nodes in `create` mode with `createIfNotExists: true` between `Config + Run Context` and `Firecrawl Search`. Switch the four downstream Data Table nodes from `mode: "id"` to `mode: "name"` resourceLocators.
- **Docs already updated** to call this a v1 limitation, but workflow fix is the better outcome.

### 2. Move hardcoded values into Config
- **`Send Weekly Digest.sendTo`** = `"vaughnai2023@gmail.com"` — every importer's first run emails you.
- **`Upload CV to Drive.folderId`** = `"10E8bhtgDR8xJwoycQwSqop1Gi0itxaOV"` — Drive 404 on import.
- **Fix:** Add `recipient_email` and `drive_folder_id` to `Config + Run Context`, reference both via `{{ $('Config + Run Context').first().json.* }}`.

### 3. Resolve the source-list contradiction
Three docs disagreed (Config node vs `source-audit.md` vs memory). You're handling the source story separately — but right now the Config node ships `remoteok / weworkremotely / himalayas / jobspresso / 4dayweek`, while `Parse Candidates` only normalizes `remoteok / weworkremotely / remotive / 4dayweek`. **Himalayas + jobspresso URLs will currently bucket as `source: 'unknown'` and sort to the bottom.** Either remove them from Config, or add normalizers in `Parse Candidates`.

---

## 🟡 Important (judges will ding for this)

### 4. `Get Seen Roles` swallows errors silently
`onError: continueRegularOutput` + try/catch returning `[]` means a Data Table read failure → dedup becomes a no-op → Daniel gets the same role re-delivered weekly with new tailored CVs burning OpenAI credits. **Recommend:** keep `continueOnFail` for writes; fail loudly on the seen-roles read.

### 5. `Loop Over Candidates` has empty `options: {}`
Submission says "batch=1 + 90s timeout." Workflow has neither set explicitly. Set `batchSize: 1` and a real timeout so the docs match the code.

### 6. No `retryOnFail` on Firecrawl + OpenAI nodes
Add `retryOnFail: true, maxTries: 2, waitBetweenTries: 3000` to both Firecrawl nodes and both LLM nodes (Agent + CV Tailor).

### 7. Test webhook trigger left wired in production export
`Test Webhook Trigger` (path: `daniel-test`) coexists with the Schedule trigger. Either disable it for the public export, or add a sticky note explaining the dual-trigger pattern.

---

## 🟢 Optional polish

### 8. Score + Decide — actually be 40/20/20/20, or stop saying it
Current code is a stacked-bonus model where stack can swing 60 points and remote caps at 5. Docs have been softened to "weighted on stack · remote · salary · perks" — workflow is fine as-is unless you want to re-derive weights to match the original Job Finder ratios.

### 9. `Format Email Body` is a 100+ line inline HTML-in-JS Code node
Hard to maintain. Could be split into a template + variable substitution. Not blocking.

### 10. Sticky note on Role Qualifier Agent
Add a sticky explaining honestly that the Firecrawl Scrape is a deterministic pre-fetch (not an agent tool) because the community node doesn't implement `supplyData`. This honesty is in `submission.md §7b` but not on the canvas.

---

## 🚀 Bold creative suggestions (from judges)

### A. Sub-workflow per role *(n8n best-practices judge)*
Replace the global `$getWorkflowStaticData('global')` accumulator with a sub-workflow per role invoked via `Execute Workflow`. The parent then gets a clean `items` array natively from `$('Execute Sub-workflow').all()` — no static-data hack needed, per-role failures are isolated, and you unlock parallelism via `batchSize > 1`. Bonus: the sub-workflow becomes a reusable "score this URL" webhook. **This would showcase a less-known n8n capability and likely move the score up materially.**

### B. "Verify any claim in 60 seconds" panel *(technical judge)*
Add a top-of-README panel with three rows:
- "Evidence quote is verbatim" → screenshot of live JD + stored quote side-by-side
- "Tailored CV uses no fabricated content" → diff view of master vs. delivered CV bullets
- "Freshness ledger is authoritative" → screenshot of `daniel_seen_roles` with timestamps

Flips the four pillars from *asserted* to *auditable*. Mostly a docs/screenshot effort once a real run exists.

### C. Before/after CV diptych above the fold *(storytelling judge)*
Side-by-side image: master CV vs. tailored CV with green highlights on what changed. **"This becomes the screenshot every other reviewer shares."** Requires capturing a real before/after image once you have one.

---

## What I've already changed in docs

- `README.md` — simplified hero Mermaid (collapsed full version into `<details>`), removed broken screenshot placeholder, moved sources section below setup, fixed broken author link, softened "verbatim" claims, fixed node-count drift, rewrote setup steps to call out the manual table creation + hardcoded values
- `build/submission.md` — removed false "Setup: Ensure" claim from architecture, removed false agent-tool claim from Smart Orchestration row, softened 40/20/20/20 verbatim claim, rewrote setup §6, added idempotent setup + hardcoded values + retryOnFail to roadmap §8

Nothing in the workflow JSON has been touched.
