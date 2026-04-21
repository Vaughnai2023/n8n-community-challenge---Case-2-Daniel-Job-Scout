# Case 2: Daniel — Job Scout Resource Pack

## Before You Start

This pack is designed to guide the build, not to force one exact output format.

- Treat the schema as a target structure, not a promise that every source can fill every field
- Different source selections are acceptable if the workflow explains its choices and produces defensible results
- If a field is unavailable, mark it as `unknown`, `unavailable`, or `not listed`
- Firecrawl tools available for this challenge include `Search`, `Scrape`, `Crawl`, `Map`, `Extract`, `Agent`, and `Browser`
- For most workflows in this case, the core tools are `Search`, `Scrape`, and sometimes `Extract`; `Agent` and `Browser` are advanced options
- Global challenge rules still apply: include Firecrawl in the workflow and use the n8n AI Agent node as the orchestrator

---

## Sample Input

Daniel's job criteria. Your workflow should use these parameters to search and filter roles.

```json
{
  "role": "Senior Backend Engineer",
  "stack": ["Python", "Django", "PostgreSQL", "Redis", "AWS"],
  "experience_years": 8,
  "location": "Remote (EU-friendly timezones)",
  "salary_minimum_eur": 90000,
  "deal_breakers": ["on-site only", "requires US citizenship", "crypto/web3"],
  "nice_to_have": ["4-day week", "open source culture", "Series A-C"],
  "max_listing_age_days": 7
}
```

For this challenge, interpret `EU-friendly timezones` as roles that either explicitly mention Europe or support working-hour overlap roughly within UTC-1 to UTC+3.

---

## Source Guidance

Part of this challenge is choosing which job sources and enrichment sources your workflow uses.

Prioritize sources that:

- Firecrawl can access reliably
- expose clear listing content
- provide public company information without requiring fragile workarounds

Good source categories:

- public job boards
- company career pages
- public company profile pages
- public funding or company-overview sources

Be careful with sources that are login-gated, rate-limited, or terms-sensitive. If a source is unreliable, choose another one instead of forcing it.

---

## Expected Output Structure

Your briefing format can differ, but each role should clearly separate source-backed facts from your fit analysis.

### Must-have fields

Each role in the output should include these at minimum:

| Field | Description |
|---|---|
| **Company** | Company name |
| **Role** | Job title |
| **Location** | Remote/hybrid/on-site plus region if stated |
| **Posted** | Posted date or best available recency signal |
| **Stack** | Technologies clearly mentioned in the listing |
| **Why it fits** | Short explanation of how it matches the criteria |
| **Link** | Direct link to the listing |
| **Source links** | Links to the listing and any enrichment sources used |

### Nice-to-have fields

These are useful enrichments, but should be included only if publicly available from reliable sources:

- Source notes when important data is missing or inferred
- Salary range
- Company size
- Funding stage or amount
- Public employer-review signal
- Fit score or ranking
- Filtered-out count with reasons
- Summary header for the whole briefing

### Salary guidance

Use this order of preference:

1. Salary explicitly stated in the listing
2. Salary stated on the company career page
3. `unavailable`

Only use an estimate if you can clearly justify it from a reputable public source. If not, mark it unavailable.

If salary is missing, either:

- exclude the role because it cannot be verified against Daniel's threshold, or
- include it clearly marked as salary unknown so Daniel can decide whether it is still worth reviewing

### Freshness guidance

"Posted in the last 7 days" can be interpreted using:

- an explicit posting date
- a visible recency label such as `3 days ago`
- a documented first-seen timestamp in your own workflow

If age cannot be determined, either exclude the role or label it clearly as age unknown.

---

## Expected Output Example

### Role Briefing Entry

| Field | Value |
|---|---|
| **Company** | ExampleCo |
| **Role** | Senior Backend Engineer |
| **Location** | Remote, Europe |
| **Salary range** | EUR 90k-110k if stated, otherwise unavailable |
| **Posted** | 3 days ago |
| **Stack** | Python, Django, PostgreSQL, AWS |
| **Company size** | 50-200 employees, if available |
| **Funding** | Series B, if available |
| **Public review signal** | Optional public review source if available |
| **Why it fits** | Strong stack overlap, remote in Europe, salary clears threshold |
| **Link** | Direct job URL |
| **Source links** | Job listing URL plus any public company-context sources used |

**Observed facts**
- Listing mentions Python, Django, PostgreSQL, and AWS
- Remote eligibility includes European time zones
- No obvious deal-breakers found

**Fit analysis**
- Strong match on core stack
- Meets remote requirement
- Salary acceptable if stated
- Nice-to-have criteria partially met

---

## What "done" looks like for this case

### Minimum viable

- [ ] Workflow runs on a weekly schedule
- [ ] Searches public job sources for matching roles
- [ ] Filters by Daniel's criteria such as stack, remote fit, deal-breakers, and listing age
- [ ] Produces a formatted briefing with links and concise reasoning
- [ ] Returns the best defensible matches found in the time window; returning zero is acceptable if no valid matches are found
- [ ] Handles missing salary or company data explicitly
- [ ] Workflow includes Firecrawl as part of the solution
- [ ] Uses the n8n AI Agent node as orchestrator

### Strong submission

- [ ] Enriches roles with company context from reliable public sources
- [ ] Explains why roles were filtered out
- [ ] Ranks or scores results in a defensible way
- [ ] Documents how freshness is determined
- [ ] Adds a creative improvement we did not explicitly ask for, as long as it helps Daniel find better roles faster or judge them more confidently
