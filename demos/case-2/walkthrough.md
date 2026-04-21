# Walkthrough Script — Case 2: Daniel, Job Scout Hunter

**Target length:** 3-5 minutes
**Audience:** n8n Community Build Event judges
**Goal:** by minute 1 they understand the thesis; by minute 3 they want to import the workflow.

---

## Beat 1 — Hook (0:00–0:20)

> "99% of submissions for this case will build the same thing: Firecrawl search, LLM filter, Google Sheet. A list.
>
> I built something different. By the time Daniel opens his Monday email, every matched role already has a tailored CV waiting. He picks two or three, hits apply. The workflow doesn't produce a list — it produces applications."

---

## Beat 2 — The brief (0:20–0:40)

Show Daniel's input JSON on screen:
- Senior Backend Engineer, Python/Django/PostgreSQL/Redis/AWS
- 8 years experience, EU-friendly remote, €90k+, no crypto, no on-site

> "This is what we're solving for. Now let me show you how."

---

## Beat 3 — Architecture (0:40–1:10)

Zoom out on the n8n canvas. Trace the flow with the cursor:

> "Schedule fires Monday 8am → Config holds the criteria → idempotent table setup → Firecrawl Search hits multiple boards in one call → parse, dedup, cap → loop one role at a time through an AI Agent that does the qualification → score it → if it's a keeper, the CV Tailor builds a 1-page A4 HTML → save, register, repeat → aggregate the week → email digest with every CV attached."

---

## Beat 4 — Trigger + Config (1:10–1:30)

Open the Config node. Highlight:
- The criteria block (mirrors Daniel's brief)
- Source list with weights
- `dry_run` toggle (budget guardrail from the Job Finder system)

> "One node, all the levers. No hunting through 30 nodes to change a parameter."

---

## Beat 5 — Firecrawl Search (1:30–2:00)

Run a single iteration. Show:
- The multi-site search call (one Firecrawl request, multiple boards)
- Parsed candidates in the output
- Dedup pulling against `daniel_seen_roles`

> "One Firecrawl call, multiple sources. The Freshness Ledger here is the second pillar — if a board doesn't expose a posting date, our `first_seen_utc` becomes the authoritative recency signal."

---

## Beat 6 — The Agent loop (2:00–2:40)

Pick one candidate. Show the Agent:
- Pre-fetched JD markdown (Firecrawl Scrape inline, not as agent tool — explain why in 5 seconds)
- Structured Output Parser pulling 16 flat fields
- Score + Decide running the 40/20/20/20 rubric

When it filters one out, **open the Filtered-Out table** and point at `reason_quote`:

> "That's the verbatim JD substring that triggered the rejection. Pillar three: deal-breaker evidence quotes. The agent is instructed this MUST be a substring — never invented. Any judge can verify any rejection against the live JD."

---

## Beat 7 — The CV Tailor *(the showstopper, 2:40–3:40)*

Open `daniel_sample_cv.html` in the browser. Then back to n8n:
- Show the LLM Chain prompt
- Highlight: targeted modifications, no fabrication, content selected by JD overlap

> "Pillar one. Every role on the ranked list arrives with this. A 1-page A4 HTML CV, print-safe, designed for senior-engineer aesthetics. Daniel double-clicks the attachment, Cmd-P, PDF, apply.
>
> The tailoring rules are ported verbatim from the production Job Finder system that's been running for months — they're not speculative."

---

## Beat 8 — Email digest + close (3:40–4:30)

Show the Monday email mockup:
- Warm header ("Morning Daniel, 3 strong matches this week")
- Per-band cards, ranked
- Honest "why not" alongside "why it fits"
- Filter-outs collapsed by default
- Tailored CVs as `.html` attachments

> "Pillar four — every role tagged with its source. We can see week over week which boards produce High-band matches and rotate weak ones out without touching any other logic. The workflow doesn't just execute. It improves.
>
> Four creative pillars, all genuinely unexpected in the job-scout space. One workflow that ships applications instead of lists. Import, attach credentials, run."

---

## Recording tips

- Record in 1080p minimum. Workflow canvas needs to be readable.
- Use the n8n editor in light mode (better contrast on screen recordings).
- Have `daniel_sample_cv.html` open in a separate tab — switching to it is the visual punch.
- Don't apologize for the source-list section being TBD on camera — just say "source curation is the v2 conversation."
