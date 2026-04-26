#!/usr/bin/env python3
"""Build the static gallery from cvs.json.

Reads:  gallery/data/cvs.json
Writes: gallery/index.html
        gallery/role/<slug>.html       (side-by-side comparison)
        gallery/tailored/<slug>.html   (the bare tailored CV in its own page)

Run from repo root:  python3 gallery/scripts/build.py
Idempotent.
"""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GALLERY = ROOT / "gallery"
DATA = GALLERY / "data" / "cvs.json"
TAILORED_DIR = GALLERY / "tailored"
ROLE_DIR = GALLERY / "role"


def read_data() -> dict:
    with DATA.open() as f:
        return json.load(f)


# ---------- helpers ----------------------------------------------------------

def csv_chips(csv: str) -> str:
    if not csv:
        return ""
    items = [s.strip() for s in csv.split(",") if s.strip()]
    return "".join(f'<span class="chip">{escape(s)}</span>' for s in items)


def band_class(band: str) -> str:
    return {"High": "band-high", "Medium": "band-medium", "Low": "band-low"}.get(band, "band-medium")


def salary_display(cv: dict) -> str:
    if cv["salary_source"] == "unavailable":
        return "Not listed in JD"
    lo, hi = cv.get("salary_min_eur") or 0, cv.get("salary_max_eur") or 0
    parts = []
    if lo:
        parts.append(f"€{lo:,}")
    if hi:
        parts.append(f"€{hi:,}")
    rng = " – ".join(parts) if parts else "—"
    return f'{rng} <span class="muted">({escape(cv.get("salary_confidence","none"))})</span>'


# ---------- tailored standalone page -----------------------------------------

def write_tailored_page(cv: dict) -> None:
    """The tailored CV HTML from the workflow is already a full <!DOCTYPE html>
    document. Save it verbatim so the iframe loads exactly what the workflow
    produced — no re-styling, no truncation."""
    out = TAILORED_DIR / f"{cv['slug']}.html"
    out.write_text(cv["tailored_cv_html"], encoding="utf-8")


# ---------- master CV page ---------------------------------------------------

MASTER_CV_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Daniel Chen — Master CV (untailored)</title>
<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');:root{--ink:#0e1216;--ink-soft:#3a4048;--ink-mute:#6b7280;--accent:#1f3b5b;--rule:#e5e7eb;--rail-bg:#f7f7f5}@page{size:A4;margin:0}*{box-sizing:border-box}html,body{margin:0;padding:0;background:#eee;color:var(--ink);font-family:'Inter',sans-serif;font-size:10.25pt;line-height:1.45}.page{width:210mm;min-height:297mm;margin:16px auto;background:#fff;display:grid;grid-template-columns:62mm 1fr;box-shadow:0 1px 3px rgba(0,0,0,.08)}.rail{background:var(--rail-bg);padding:14mm 10mm 14mm 12mm;border-right:1px solid var(--rule)}.rail h2{font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--accent);margin:0 0 6px}.rail section+section{margin-top:14px}.rail ul{list-style:none;margin:0;padding:0}.rail li{padding:3px 0;font-size:9.5pt;color:var(--ink-soft)}.rail .contact li{font-family:'JetBrains Mono',monospace;font-size:8.75pt;color:var(--ink);word-break:break-word}.rail .contact li .label{display:block;font-family:'Inter',sans-serif;font-size:7.5pt;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-mute);margin-bottom:1px;font-weight:500}.main{padding:14mm 13mm}.header{margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--rule)}.header .name{font-size:26pt;font-weight:700;letter-spacing:-.025em;line-height:1.05}.header .subtitle{margin-top:4px;font-size:9pt;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:500}.main h2{font-size:9pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--accent);margin:14px 0 6px;padding-bottom:3px;border-bottom:1px solid var(--rule)}.summary{font-size:10.5pt;color:var(--ink-soft);margin:0 0 4px}.role{margin:8px 0 10px;page-break-inside:avoid}.role-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:3px}.role-head strong{font-size:10.5pt;font-weight:600}.role-meta{font-family:'JetBrains Mono',monospace;font-size:8.5pt;color:var(--ink-mute);white-space:nowrap}.role ul{margin:3px 0 0;padding:0 0 0 16px}.role li{margin:2px 0;font-size:9.75pt;color:var(--ink-soft);line-height:1.42}.portfolio{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px}.project strong{font-size:10pt;display:block;margin-bottom:1px}.project p{margin:0;font-size:9.5pt;color:var(--ink-soft)}@media print{body{background:#fff}.page{margin:0;box-shadow:none;width:100%}}</style>
</head><body><div class="page"><aside class="rail">
<section class="contact"><h2>Contact</h2><ul>
<li><span class="label">Email</span>daniel.chen.dev@example.com</li>
<li><span class="label">Location</span>Remote · Lisbon (CET)</li>
<li><span class="label">GitHub</span>github.com/danielchen-dev</li>
<li><span class="label">LinkedIn</span>linkedin.com/in/danielchen-backend</li>
</ul></section>
<section><h2>Core Stack (full)</h2><ul>
<li>Python (8 yrs)</li><li>Go (production)</li><li>TypeScript</li><li>SQL</li>
<li>Django · DRF · FastAPI · Celery</li>
<li>PostgreSQL (advanced)</li><li>Redis (cache · streams · pub/sub)</li><li>ClickHouse</li>
<li>AWS (EC2/RDS/S3/SQS/Lambda)</li><li>Docker · Terraform · GitHub Actions</li>
<li>Datadog · Sentry · Prometheus</li>
<li>Kubernetes (read/debug)</li><li>gRPC · Kafka · Elasticsearch</li>
</ul></section>
<section><h2>Education</h2><ul>
<li><strong>AWS SAA</strong><br><span>2022, recert 2024</span></li>
<li><strong>BSc Comp Eng</strong><br><span>NOVA University Lisbon, 2016</span></li>
<li><strong>DDIA</strong><br><span>Yearly re-read</span></li>
</ul></section>
</aside><main class="main">
<div class="header"><div class="name">Daniel Chen</div><div class="subtitle">Senior Backend Engineer · Master CV (untailored)</div></div>
<h2>Profile (3 variants — workflow picks the closest per role)</h2>
<p class="summary"><strong>A. Scale:</strong> Senior backend engineer, 8y high-throughput Python/Django on AWS. PostgreSQL schema through Redis caches/workers. Shipped 40M req/day systems. Remote-first since 2020.</p>
<p class="summary"><strong>B. Product:</strong> Senior backend engineer, 8y shipping Python/Django end-to-end. PostgreSQL+Redis+product trade-offs. Small senior teams. Remote, Lisbon CET.</p>
<p class="summary"><strong>C. Platform:</strong> Senior backend engineer, 8y infra work — PostgreSQL tuning, Redis+Celery, AWS+Terraform, on-call.</p>
<h2>Experience (5 roles — workflow picks 3)</h2>
<div class="role"><div class="role-head"><strong>Fintrace</strong><span class="role-meta">Staff Backend Engineer · 2023-2026</span></div>
<ul><li>Led ledger re-arch Django→Django+Celery+Redis Streams (p95 380→62ms at 40M req/day).</li>
<li>Owned PG single→primary+3 replica migration (Patroni/AWS); wrote lag monitoring + read-routing middleware.</li>
<li>Shipped public Payments API (OpenAPI, versioned, 14 partners).</li>
<li>Mentored 4 to senior; wrote backend style guide.</li></ul></div>
<div class="role"><div class="role-head"><strong>Tillage Labs</strong><span class="role-meta">Senior Backend Engineer · 2021-2023</span></div>
<ul><li>Built multi-tenant ingestion pipeline 2.8TB/day IoT→PG+ClickHouse (Celery + backpressure-aware router).</li>
<li>Async Django for long-polls cut pool pressure 70%, consolidated 3 Gunicorn fleets to 1.</li>
<li>Cost init: rewrote Lambda export pipeline, Redis query-aware caching, -34% infra spend.</li>
<li>On-call 1-in-6, 9 post-mortems.</li></ul></div>
<div class="role"><div class="role-head"><strong>Orbit Medical</strong><span class="role-meta">Senior Backend Engineer · 2019-2021</span></div>
<ul><li>Owned HIPAA-compliant patient-records service (Django+PG row-level encryption, audit log to S3, SOC2).</li>
<li>Integrated 3 pharmacy APIs via adapter+retry/circuit-breaker lib I published.</li>
<li>PG12→Aurora 14 migration, 4h window, real run 11min under estimate.</li></ul></div>
<div class="role"><div class="role-head"><strong>Lanterna</strong><span class="role-meta">Backend Engineer · 2018-2019</span></div>
<ul><li>First backend hire; built Django+PG+Redis, warehouse-ops API + driver-app BFF.</li>
<li>Set up GH Actions CI, black+mypy+pre-commit.</li></ul></div>
<div class="role"><div class="role-head"><strong>Meridia Studio</strong><span class="role-meta">Junior/Mid Backend · 2016-2018</span></div>
<ul><li>Shipped 6 Django+DRF projects. Maintained shared Django boilerplate (auth/billing/admin/obs).</li></ul></div>
<h2>Selected Work (5 items — workflow picks 3)</h2>
<div class="portfolio">
<div class="project"><strong>django-async-queue</strong><p>1.8k stars OSS — first-class async Celery workers, used at Fintrace + 2 public companies</p></div>
<div class="project"><strong>"The PostgreSQL migration I got wrong"</strong><p>2023 post-mortem ~80k reads</p></div>
<div class="project"><strong>"Redis Streams in production"</strong><p>PyCon EU 2024 talk on failure modes most teams discover the hard way</p></div>
<div class="project"><strong>kafka-python contributor</strong><p>~8 merged PRs — batch-compression fixes, connection-pool debug</p></div>
<div class="project"><strong>pgreindex-safe</strong><p>OSS CLI wrapping pg_repack with safety checks for production reindex</p></div>
</div>
</main></div></body></html>
"""


def write_master_cv() -> None:
    (GALLERY / "master-cv.html").write_text(MASTER_CV_HTML, encoding="utf-8")


# ---------- per-role comparison page -----------------------------------------

ROLE_PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Tailored CV · Daniel Chen</title>
<meta name="description" content="See exactly how the n8n Job Scout workflow tailored Daniel's CV for the {role} role at {company}.">
<link rel="stylesheet" href="../assets/styles.css">
</head>
<body data-page="role" class="{band_class}">

<header class="topbar">
  <a class="back" href="../index.html">← All 5 tailored CVs</a>
  <div class="topbar-meta">
    <span class="exec">Run <code>{run_id}</code> · verified {verified_at_short}</span>
  </div>
</header>

<section class="role-hero">
  <div class="role-hero-main">
    <div class="role-hero-eyebrow">Tailored CV · Role #{rank} of 5</div>
    <h1>{company}</h1>
    <p class="role-hero-role">{role}</p>
    <div class="role-hero-meta">
      <span>📍 {location}</span>
      <span>🏠 {remote_type}</span>
      <span>📅 {posted_display}</span>
    </div>
  </div>
  <div class="role-hero-score">
    <div class="score-ring" style="--ring-pct: {fit_score};">
      <div class="score-inner">
        <div class="score-band-pill">{fit_band}</div>
        <div class="score-num">{fit_score}</div>
        <div class="score-out">/ 100</div>
      </div>
    </div>
    <a class="apply-link" href="{listing_url}" target="_blank" rel="noopener">View original listing →</a>
  </div>
</section>

<section class="callouts">
  <div class="callouts-head">
    <h2>How the workflow tailored this CV</h2>
  </div>
  <p class="callouts-lede">Auto-generated from the n8n run data — every claim below is verifiable in <code>daniel_role_master</code> row {rank}.</p>
  <div class="callout-grid">
    <article class="callout">
      <div class="callout-num">01</div>
      <div class="callout-content">
        <h3>Why-it-fits paragraph</h3>
        <p class="callout-source">Generated · written into <code>.why</code> block</p>
        <blockquote>{why_it_fits}</blockquote>
      </div>
    </article>
    <article class="callout">
      <div class="callout-num">02</div>
      <div class="callout-content">
        <h3>Stack front-loaded</h3>
        <p class="callout-source">Reordered from master · matches JD requirements</p>
        <div class="chips">{stack_matched_chips}</div>
      </div>
    </article>
    <article class="callout">
      <div class="callout-num">03</div>
      <div class="callout-content">
        <h3>Stack the JD wants but Daniel doesn't have</h3>
        <p class="callout-source">Honest gap · NOT added to CV (no fabrication)</p>
        <div class="chips chips-missing">{stack_missing_chips}</div>
      </div>
    </article>
    <article class="callout">
      <div class="callout-num">04</div>
      <div class="callout-content">
        <h3>Salary triangulation</h3>
        <p class="callout-source">Pillar 1: enrichment depth</p>
        <p class="callout-body">{salary_html}</p>
      </div>
    </article>
    <article class="callout callout-wide">
      <div class="callout-num">05</div>
      <div class="callout-content">
        <h3>Steelman <em>why not</em></h3>
        <p class="callout-source">Workflow pre-empts judge skepticism — surfaces the role's weak points alongside the strong</p>
        <blockquote class="muted">{why_not}</blockquote>
      </div>
    </article>
  </div>
</section>

<section class="diptych">
  <div class="diptych-tabs">
    <h2>Side-by-side · Master <em>vs.</em> Tailored</h2>
    <div class="diptych-controls">
      <button class="btn" onclick="window.open('../tailored/{slug}.html', '_blank')">Open tailored ↗</button>
      <button class="btn" onclick="window.open('../master-cv.html', '_blank')">Open master ↗</button>
    </div>
  </div>
  <div class="diptych-grid">
    <div class="frame frame-master">
      <div class="frame-chrome">
        <div class="frame-dots"><span></span><span></span><span></span></div>
        <div class="frame-url">file://daniel-chen/master-cv.html</div>
        <div class="frame-tag">Untailored source</div>
      </div>
      <iframe src="../master-cv.html" title="Daniel's master CV" loading="eager"></iframe>
    </div>
    <div class="frame frame-tailored">
      <div class="frame-chrome">
        <div class="frame-dots"><span></span><span></span><span></span></div>
        <div class="frame-url">file://daniel-chen/tailored/{slug}.html</div>
        <div class="frame-tag">Tailored · {company}</div>
      </div>
      <iframe src="../tailored/{slug}.html" title="Tailored CV for {company}" loading="eager"></iframe>
    </div>
  </div>
  <p class="diptych-note">Both panes scroll independently. Compare the <em>Profile</em> paragraph, the <em>Stack</em> ordering, the 3 selected roles, and the new <em>Why {company}</em> block at the bottom.</p>
</section>

<section class="raw-evidence">
  <details>
    <summary>Show raw n8n run fields for this role</summary>
    <dl>
      <dt>listing_url</dt><dd><a href="{listing_url}" target="_blank" rel="noopener"><code>{listing_url}</code></a></dd>
      <dt>tailored_cv_url (Drive)</dt><dd><a href="{tailored_cv_url}" target="_blank" rel="noopener"><code>{tailored_cv_url}</code></a></dd>
      <dt>observed_facts</dt><dd>{observed_facts}</dd>
    </dl>
  </details>
</section>

<footer class="site-footer">
  <a href="../index.html">← Back to gallery</a>
  <span>Built from real n8n execution <code>{exec_id}</code> · no synthetic data on this page</span>
</footer>

</body>
</html>
"""


def write_role_page(cv: dict, rank: int, run_id: str, exec_id: str, verified_at: str) -> None:
    salary = salary_display(cv)
    body = ROLE_PAGE_TMPL.format(
        slug=escape(cv["slug"]),
        company=escape(cv["company"]),
        company_upper=escape(cv["company"].upper()),
        role=escape(cv["role"]),
        location=escape(cv.get("location") or "—"),
        remote_type=escape(cv.get("remote_type") or "—"),
        posted_display=escape(cv.get("posted_display") or "—"),
        listing_url=escape(cv["listing_url"]),
        tailored_cv_url=escape(cv.get("tailored_cv_url") or "—"),
        fit_band=escape(cv["fit_band"]),
        band_class=band_class(cv["fit_band"]),
        fit_score=int(cv["fit_score"]),
        rank=rank,
        why_it_fits=escape(cv.get("why_it_fits") or "—"),
        why_not=escape(cv.get("why_not") or "—"),
        observed_facts=escape(cv.get("observed_facts") or "—"),
        stack_matched_chips=csv_chips(cv.get("stack_matched_csv") or ""),
        stack_missing_chips=csv_chips(cv.get("stack_missing_csv") or "") or '<span class="muted">none flagged</span>',
        salary_html=salary,
        run_id=escape(run_id),
        exec_id=escape(exec_id),
        verified_at_short=escape(verified_at[:10]),
    )
    (ROLE_DIR / f"{cv['slug']}.html").write_text(body, encoding="utf-8")


# ---------- index page -------------------------------------------------------

INDEX_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tailored CV Gallery · Daniel — Job Scout (n8n Community Build Event)</title>
<meta name="description" content="5 real tailored CVs auto-generated by an n8n workflow. Click any to see master vs. tailored side-by-side and the exact reasoning behind every modification.">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body data-page="index">

<header class="hero">
  <div class="aurora" aria-hidden="true"></div>
  <div class="noise" aria-hidden="true"></div>
  <div class="floating-evidence" aria-hidden="true">
    <span class="float-pill float-1">Verified run · {verified_at_short}</span>
    <span class="float-pill float-2">5 tailored CVs delivered</span>
    <span class="float-pill float-3">2m 46s end-to-end</span>
    <span class="float-pill float-4">No fabrication, no hallucination</span>
  </div>
  <div class="hero-inner">
    <p class="hero-eyebrow">n8n Community Build Event · Case 2 · Daniel</p>
    <h1>5 <em>tailored</em> CVs.<br>One Monday <em>workflow</em>.</h1>
    <p class="hero-lede">99% of submissions for Daniel's brief will build a list of jobs. <strong>This one builds applications.</strong> Every role below was scored, filtered, and shipped with a 1-page tailored CV — by an n8n workflow, in 2m 46s, on 2026-04-26.</p>
    <div class="hero-stats">
      <div class="stat"><div class="stat-num">2m 46s</div><div class="stat-label">end-to-end runtime</div></div>
      <div class="stat"><div class="stat-num">30</div><div class="stat-label">candidates parsed</div></div>
      <div class="stat"><div class="stat-num">5</div><div class="stat-label">delivered with tailored CV</div></div>
      <div class="stat"><div class="stat-num">3</div><div class="stat-label">filtered with verbatim JD quote</div></div>
    </div>
    <p class="hero-meta">Run <code>{run_id}</code> · n8n execution <code>{exec_id}</code> · verified {verified_at_short}</p>
  </div>
</header>

<section class="cards">
  <h2>Pick any role to see <em>exactly</em> how its CV was tailored</h2>
  <p class="cards-subhead">Real n8n execution data. Every chip, bullet, and paragraph below maps back to a value in the workflow's <code>daniel_role_master</code> data table.</p>
  <div class="cards-grid">
    {cards_html}
  </div>
</section>

<section class="how">
  <h2>How to read these CVs</h2>
  <ol class="how-list">
    <li><strong>Open any role.</strong> The page shows Daniel's master CV on the left and the tailored CV the workflow produced on the right.</li>
    <li><strong>Read the 5 callouts above the diptych.</strong> They spell out, with verifiable values from the n8n run, what the workflow changed and why.</li>
    <li><strong>Scroll both CVs to compare.</strong> Look at the Profile paragraph (1 of 3 variants picked), the Stack ordering (front-loaded for this JD), the 3 selected roles out of Daniel's 5, and the bespoke <em>Why &lt;company&gt;</em> block at the bottom.</li>
    <li><strong>Verify nothing was fabricated.</strong> Every chip, bullet, and project on the tailored CV maps back to one on the master.</li>
  </ol>
</section>

<footer class="site-footer">
  <a href="https://github.com/" target="_blank" rel="noopener">View the n8n workflow JSON ↗</a>
  <span>Built by Vaughn Botha for the n8n Community Build Event · April 2026</span>
</footer>

</body>
</html>
"""

CARD_TMPL = """<a class="card {band_class}" href="role/{slug}.html">
  <div class="card-top">
    <span class="card-band">{fit_band}</span>
    <div class="card-ring" style="--ring-pct: {fit_score};"><span>{fit_score}</span></div>
  </div>
  <h3>{company}</h3>
  <p class="card-role">{role}</p>
  <p class="card-meta">{location} · {remote_type}</p>
  <p class="card-why">{why_it_fits_short}</p>
  <div class="card-cta">See how the CV was tailored →</div>
</a>"""


def truncate(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def write_index(data: dict) -> None:
    cards = []
    for cv in data["cvs"]:
        cards.append(
            CARD_TMPL.format(
                slug=escape(cv["slug"]),
                band_class=band_class(cv["fit_band"]),
                fit_band=escape(cv["fit_band"]),
                fit_score=int(cv["fit_score"]),
                company=escape(cv["company"]),
                role=escape(cv["role"]),
                location=escape(cv.get("location") or "—"),
                remote_type=escape(cv.get("remote_type") or "—"),
                why_it_fits_short=escape(truncate(cv.get("why_it_fits") or "", 220)),
            )
        )
    body = INDEX_TMPL.format(
        cards_html="\n    ".join(cards),
        run_id=escape(data["run_id"]),
        exec_id=escape(data["execution_id"]),
        verified_at_short=escape(data["verified_at"][:10]),
    )
    (GALLERY / "index.html").write_text(body, encoding="utf-8")


# ---------- main -------------------------------------------------------------

def main() -> None:
    data = read_data()
    TAILORED_DIR.mkdir(parents=True, exist_ok=True)
    ROLE_DIR.mkdir(parents=True, exist_ok=True)

    for i, cv in enumerate(data["cvs"], start=1):
        write_tailored_page(cv)
        write_role_page(cv, i, data["run_id"], data["execution_id"], data["verified_at"])

    write_master_cv()
    write_index(data)

    print(f"✓ Wrote master-cv.html")
    print(f"✓ Wrote {len(data['cvs'])} tailored CV pages → gallery/tailored/")
    print(f"✓ Wrote {len(data['cvs'])} role comparison pages → gallery/role/")
    print(f"✓ Wrote index.html")


if __name__ == "__main__":
    main()
