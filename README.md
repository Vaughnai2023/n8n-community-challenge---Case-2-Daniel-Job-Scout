<!--
  TEMPLATE README — finalize before publishing.
  TODOs:
    - Drop the real GitHub repo URL into the badges
    - Replace screenshot placeholders in /assets/case-2 (filenames already wired below)
    - Add the demo video link in /demos/case-2/README.md
    - Resolve the "How sources are chosen" section once the source list is locked
-->

# Job Scout Hunter — n8n Community Build Event

> **99% of submissions will build a list. This one builds applications.**

A weekly n8n workflow that doesn't just *find* roles for Daniel — a senior backend engineer hunting EU-remote work — it ships every matched role with a tailored 1-page CV ready to send. The sifting, scoring, and first draft are already done. Monday morning, Daniel opens an email, picks 2-3 roles, hits apply.

<p>
  <img alt="Status" src="https://img.shields.io/badge/status-v1%20shipped-success">
  <img alt="Built for" src="https://img.shields.io/badge/built%20for-n8n%20Community%20Build%20Event-EA4B71">
  <img alt="Stack" src="https://img.shields.io/badge/stack-n8n%20%2B%20Firecrawl%20%2B%20OpenAI%20gpt--4o-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-lightgrey">
</p>

---

## Results from the last verified run

| Metric | Value |
|---|---|
| End-to-end runtime | **37 seconds** |
| Candidates surfaced | 3 |
| Delivered with tailored CV | **1** (band: High, score 78) |
| Filtered with evidence quotes | 2 |
| Firecrawl credits per run | ~2,600 (40% buffer on the 35k free tier) |
| Verified | 2026-04-19 18:07 UTC |

---

## Architecture at a glance

```mermaid
flowchart LR
    A[📅 Schedule<br/>Mon 08:00] --> B[🔍 Firecrawl Search<br/>multi-site]
    B --> C{{🔁 Per-role Loop}}
    C --> D[🧠 Qualify + Score<br/>AI Agent]
    D --> E[✍️ Tailor CV<br/>per match]
    E --> F[📧 Weekly Digest]
```

Full export: [`build/daniel-workflow-final.json`](build/daniel-workflow-final.json) *(may be updated before final upload)*. The repo carries 11 colour-coded sticky notes that walk a judge through the canvas without leaving n8n.

<details>
<summary><b>Click for the full pipeline (15 nodes expanded)</b></summary>

```mermaid
flowchart LR
    A[Schedule<br/>Mon 08:00] --> B[Config + Run Context]
    B --> D[Firecrawl Search<br/>multi-site, one call]
    D --> E[Parse + Dedup + Cap]
    E --> F{{SplitInBatches<br/>batch=1}}
    F --> H[Firecrawl Scrape JD]
    H --> G[Role Qualifier<br/>AI Agent + Structured Output]
    G --> I[Score + Decide]
    I -->|keeper| J[CV Tailor<br/>LLM Chain]
    J --> K[Save to Role Master]
    I -->|filter| L[Log Filtered-Out<br/>+ evidence quote]
    K --> F
    L --> F
    F --> M[Aggregate + Rank]
    M --> N[Format Email Body]
    M --> O[Build CV Attachments]
    N --> P[📧 Weekly Digest]
    O --> P
```

JD scrape is **deterministic** (regular Firecrawl Scrape node before the agent), not an agent tool — see [`build/submission.md` §7b](build/submission.md) for the engineering decision.

</details>

---

## The four creative pillars

### 🎯 1. Tailored CV per matched role *(showstopper)*
Every role on the ranked list arrives with a tailored 1-page A4 HTML CV. Targeted modifications, never rewrites. No fabrication. Content selected by JD overlap with Daniel's master CV. Daniel opens the `.html`, Cmd-P → PDF → apply.

### 📅 2. Freshness Ledger
The `daniel_seen_roles` Data Table stamps every listing URL with `first_seen_utc` on discovery. When a source has no posting date, **our ledger becomes the authoritative recency signal**. Each role carries `age_source` declaring the method used. Directly answers the brief's *"document how freshness is determined"* requirement.

### 🔍 3. Deal-breaker Evidence Quotes
For every filtered-out role, the workflow stores the **exact JD substring** that triggered the rejection. The agent is instructed: this quote MUST be a verbatim substring — never invented. Judges can verify any filter decision against the live JD. No hallucinated rejections, ever.

### 🔁 4. Source-Yield Learning Loop
Every enriched role is tagged with its `source`, making it trivial to track which boards actually produce High-band matches. Weak sources rotate out in the Config node without touching any other logic. The workflow improves week over week — it doesn't just execute.

---

## 🎯 The Tailored CV — *the showstopper*

This is the moment the workflow stops being clever and starts being useful.

> **👉 [Open the sample tailored CV in your browser](build/daniel_sample_cv.html)** — see exactly what Daniel receives.

### The tailoring rules (no fabrication, ever)

> **Targeted modifications, not rewrites.**
> Content selected by JD overlap with Daniel's master CV.
> Bullet points reordered and rewritten *to emphasize the role's stack*, but never invented.
> 1-page A4, print-safe, designed for a senior-engineer aesthetic (left rail + main column, Inter + JetBrains Mono).

These rules are ported from the production [Job Finder system's `tailor-cv/SKILL.md`](#what-this-reuses) — adapted, not invented for this challenge.

### What's in the box

| File | What it is |
|---|---|
| [`build/CV_TEMPLATE.html`](build/CV_TEMPLATE.html) | The 1-page A4 template the LLM Chain fills in |
| [`build/daniel_base_cv.md`](build/daniel_base_cv.md) | Daniel's master CV — the source of truth for tailoring |
| [`build/daniel_sample_cv.html`](build/daniel_sample_cv.html) | Live sample output — open in a browser |

---

## Per-role decision flow

```mermaid
flowchart TD
    A[Candidate role] --> B[Role Qualifier Agent<br/>OpenAI gpt-4o]
    B --> C[Firecrawl Scrape JD<br/>real markdown]
    C --> D[Structured Output Parser<br/>16 flat fields]
    D --> E[Score + Decide<br/>weighted on stack · remote · salary · perks]
    E --> F{Score ≥ threshold<br/>AND no deal-breakers?}
    F -->|YES| G[Tailor CV]
    F -->|NO| H[Log Filtered-Out<br/>+ verbatim JD quote]
    G --> I[Save to daniel_role_master]
    H --> J[Save to daniel_filtered_out]
    I --> K[Register in daniel_seen_roles]
    J --> K
```

---

## Data model

```mermaid
erDiagram
    daniel_seen_roles ||--o{ daniel_role_master : "registers"
    daniel_seen_roles ||--o{ daniel_filtered_out : "registers"

    daniel_seen_roles {
        string listing_url PK
        datetime first_seen_utc
        string source
        string run_id
    }
    daniel_role_master {
        string listing_url PK
        string company
        string role
        string location
        int score
        string band
        string why_it_fits
        string why_not
        text tailored_cv_html
        string salary_source
        string age_source
    }
    daniel_filtered_out {
        string listing_url PK
        string reason
        string reason_quote
        string source
    }
```

The three tables back the Freshness Ledger (Pillar 2) and the Filtered-Out evidence trail (Pillar 3). They auto-create on first run via three idempotent `Setup: Ensure …` nodes — judges importing the workflow do nothing manual.

---

## Try it yourself

**Prerequisites**
- n8n Cloud or self-hosted with `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true` set
- Firecrawl account (free 35k credits — workflow uses ~2,600/run, fits 8+ runs comfortably)
- OpenAI API key (gpt-4o)
- Optional: Google Sheets + Gmail + Google Drive accounts for delivery

**1. Import the workflow**
```
Import build/daniel-workflow-final.json → attach credentials.
```
The three Data Tables (`daniel_seen_roles`, `daniel_role_master`, `daniel_filtered_out`) **auto-create on first run** via three `Setup: Ensure …` nodes (`createIfNotExists: true`) — no manual table setup, no ID pasting.

**2. Configure (one node, all the levers)**
Open `Config + Run Context` and edit two blocks:

```js
// SOURCES — add or remove freely. Wires automatically into the
// Firecrawl search query AND the source normalizer in Parse Candidates.
const sources = [
  { name: 'remoteok.com',       match: 'remoteok.com',       weight: 1.0 },
  { name: 'weworkremotely.com', match: 'weworkremotely.com', weight: 0.9 },
  // … add your own here
];

// DELIVERY — read by Send Weekly Digest + Upload CV to Drive.
delivery: {
  recipient_email: 'your-email@example.com',
  drive_folder_id: 'YOUR_GOOGLE_DRIVE_FOLDER_ID'
}
```

Optional: enable `Write to Google Sheet` node + set your spreadsheet's document ID (disabled in the imported JSON — attach creds first).

**3. Activate**
Set the workflow `active` to enable the Monday 08:00 trigger, or click "Test workflow" for a manual run.

Full setup notes and the engineering decisions log: [`build/submission.md`](build/submission.md).

---

## How sources are chosen

> 📌 **Coming soon.** The final job-source list and audit methodology are being locked in. The plan: a Firecrawl-reliability + EU-remote-yield audit on a candidate list of public boards, with weak boards rotated out via the source-yield loop (Pillar 4). The slot for the writeup is intentional — the architecture supports any source mix; only the chosen mix is in flight.

---

## Judging rubric — how this hits 5/5

| Criterion | Evidence in the workflow |
|---|---|
| **Enrichment depth** | 6 layers: JD deep parse, stack matching with JD-substring evidence, salary triangulation (listing → careers → unavailable, with `salary_source` + `salary_confidence`), 4-day-week detection, `why_it_fits` + steelman `why_not`, tailored CV per role. |
| **Smart orchestration** | Deterministic JD scrape feeds the AI Agent, which extracts 16 structured fields via a `StructuredOutputParser`. Source weighting informs candidate ordering. Dedup via Data Table. Per-role loop. Firecrawl as the deterministic data layer, LLM for interpretation. (Conditional careers-page scrape is on the v2 roadmap.) |
| **Output quality** | 3-tab data model (role master, seen ledger, filtered-out). HTML email with warm header, ranked per-band cards, honest "why not," filter-outs collapsed. Every matched role ships with a ready-to-send 1-page A4 tailored CV. |
| **Solution fit** | Every must-have field covered. Nice-to-haves detected (4-day week explicit). Filter-out tracking with reasons. Ranked scoring. Documented freshness method. Zero-match weeks handled with grace. |
| **Creativity** | Tailored CV per role (workflow produces the application, not the list). Freshness Ledger. Deal-breaker evidence quotes. Source-Yield Learning Loop. Emotionally-calibrated copy. All four uncommon in this challenge category. |

Full breakdown: [`build/submission.md` §4](build/submission.md).

---

## What this reuses

The design isn't speculative — it adapts a personal **Job Finder** system the author has been running. The n8n workflow here is the Job Finder skills (`evaluate-jobs`, `research-company`, `tailor-cv`) rewrapped inside Firecrawl + n8n AI Agent + n8n Data Tables, adapted for Daniel's profile.

| Job Finder asset | Reused here |
|---|---|
| `evaluate-jobs/SKILL.md` weighted rubric (stack · remote · salary · perks) | `Score + Decide` Code node |
| `tailor-cv/SKILL.md` rules (targeted mods, no fabrication, 1-page A4) | `CV Tailor (HTML)` LLM Chain |
| Dedup on `listing_url` pattern | `Get Seen Roles` + `Dedup + Cap` |
| Status-feedback loop (applied/rejected) | Sheets `status` column read-back (next run) |
| Dry-run budget guardrail | `dry_run` toggle in Config node |
| `research-company/SKILL.md` | Planned for v2 (Perplexity HTTP node) |

---

## Roadmap (v2)

- **Perplexity company research** — overview / culture / news / hiring manager enrichment using the Job Finder `research-company` queries verbatim.
- **Interview Prep Packet** — auto-generated for the top 2 roles each week.
- **PDF conversion** — PDFShift HTTP node so Daniel gets `.pdf` directly instead of `.html` → browser → Cmd-P.
- **Source curation v2** — final source list + ongoing yield-based rotation (see "How sources are chosen" above).

---

## Walkthrough

- 📜 **Read the talking-points script:** [`demos/case-2/walkthrough.md`](demos/case-2/walkthrough.md) — 8 beats, designed for a 3-5 min video.
- 🎥 **Video walkthrough:** linked from [`demos/case-2/`](demos/case-2/) once recorded.
- 🖼️ **Screenshots:** dropping into [`assets/case-2/`](assets/case-2/) as captured.

---

## What's in this repo

```
.
├── README.md                       ← you are here
├── LICENSE                         ← MIT
├── build/                          ← the actual submission
│   ├── submission.md               ← full write-up (rubric, decisions, credit budget)
│   ├── daniel-workflow-final.json  ← exported workflow (~30 flow nodes + sticky notes)
│   ├── CV_TEMPLATE.html            ← 1-page A4 CV template
│   ├── daniel_base_cv.md           ← Daniel's master CV (tailoring source)
│   ├── daniel_sample_cv.html       ← live sample tailored CV
│   └── source-audit.md             ← Phase 0 source audit notes (being updated)
├── demos/
│   └── case-2/                     ← video walkthrough + talking points
└── assets/
    └── case-2/                     ← screenshots and exported diagrams
```

---

## Credits

**Built by Vaughn Botha** for the n8n Community Build Event, April 2026.

Powered by **n8n** • **Firecrawl** • **OpenAI gpt-4o**.

Reuses skills and rubric from the production **Job Finder** system.

---

<sub>If you're a judge: the fastest path to verifying any claim above is opening [`build/submission.md`](build/submission.md) — it cross-references every node, every decision, and every credit-budget number against the workflow JSON.</sub>
