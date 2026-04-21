# Daniel Chen — Senior Backend Engineer

> Master CV (markdown). The n8n workflow reads this file, then the CV Tailor LLM Chain selects & reorders content per role to produce a tailored 1-page A4 HTML CV.

## Contact
- **Email:** daniel.chen.dev@example.com
- **Location:** Remote · Lisbon, Portugal (CET / UTC+1)
- **GitHub:** github.com/danielchen-dev
- **LinkedIn:** linkedin.com/in/danielchen-backend
- **Phone:** available on request

## Summary (3 variants — pick closest to role)

**A. Distributed systems / scale-oriented roles**
Senior backend engineer with 8 years building high-throughput Python/Django services on AWS. Comfortable owning systems from PostgreSQL schema design through Redis-backed caches and async workers. Have shipped production systems handling 40M+ requests/day. Remote-first since 2020, strong async-written-communication habit.

**B. Product-focused / smaller company roles**
Senior backend engineer, 8 years shipping Python/Django products end-to-end. Equally at home designing the PostgreSQL schema, wiring the Redis queue, and pairing with product on the right trade-off. Prefer small, senior teams that ship weekly. Remote-first since 2020, based in Lisbon (CET).

**C. Platform / infrastructure roles**
Senior backend engineer with 8 years of hands-on infrastructure work behind Python/Django services — PostgreSQL performance tuning, Redis + Celery pipelines, AWS provisioning with Terraform, incident-response rotations. Left "everything-by-hand" companies to find teams that invest in their platform. Remote, CET.

## Core Stack
- **Languages:** Python (primary, 8 yrs), Go (conversational, production-shipped), TypeScript (backend + scripting), SQL
- **Frameworks:** Django (8 yrs), FastAPI, Django REST Framework, Celery
- **Data:** PostgreSQL (advanced — query tuning, partitioning, replication), Redis (cache + streams + pub/sub), ClickHouse (analytics workloads)
- **Cloud & infra:** AWS (EC2, RDS, S3, SQS, Lambda, CloudFront), Docker, Terraform, GitHub Actions
- **Observability:** Datadog, Sentry, structured logging, Prometheus/Grafana
- **Nice-to-have:** Kubernetes (read/debug level), gRPC, Kafka (contributor), Elasticsearch

## Experience

### Staff Backend Engineer — Fintrace (fintech, Series B) · 2023-2026 (remote)
- Led re-architecture of the transaction-ledger service from a Django monolith to a Django + Celery + Redis Streams hybrid — cut p95 latency from 380ms to 62ms at 40M requests/day.
- Owned the PostgreSQL migration from a single primary to a primary + 3 read-replicas topology (via Patroni on AWS); wrote the replica-lag monitoring + read-routing Django middleware.
- Designed and shipped the public Payments API (OpenAPI spec, versioned, rate-limited) — currently integrated by 14 partner platforms.
- Mentored 4 mid-level engineers through the senior-engineer progression; wrote the company's internal "Backend style guide" now referenced in interviews.

### Senior Backend Engineer — Tillage Labs (agtech SaaS) · 2021-2023 (remote)
- Built the multi-tenant data-ingestion pipeline processing 2.8 TB/day of IoT sensor data into PostgreSQL + ClickHouse, using Celery workers and a custom backpressure-aware router.
- Introduced async Django views for long-polling endpoints — reduced connection-pool pressure by 70%, let us consolidate from 3 Gunicorn fleets to 1.
- Led an AWS-cost-reduction initiative — rewrote the batch-export Lambda pipeline, shipped query-aware caching in Redis, cut monthly infra spend by 34%.
- On-call rotation (1-in-6), wrote 9 post-mortem documents, ran 3 of them as scribe.

### Senior Backend Engineer — Orbit Medical (health-tech, Series A) · 2019-2021 (remote + Lisbon)
- Owned the HIPAA-compliant patient-records service — Django + PostgreSQL with row-level encryption, audit-log stream to S3, SOC2-ready access controls.
- Integrated 3 third-party pharmacy APIs (Surescripts, RxNT, Change Healthcare) using an adapter pattern + retry/circuit-breaker library I published internally.
- Migrated on-premise PostgreSQL (12) to AWS RDS Aurora (14) during a scheduled 4-hour window — wrote and tested a full dry-run playbook; real migration ran 11 minutes under estimate.

### Backend Engineer — Lanterna (logistics, Series A) · 2018-2019 (Lisbon, hybrid)
- First backend hire. Built the initial Django + PostgreSQL + Redis stack, shipped the warehouse-operations API and the driver-mobile-app BFF.
- Set up GitHub Actions CI, introduced pre-commit hooks + black + mypy to a previously untyped codebase.

### Junior / Mid Backend Engineer — Meridia Studio (consultancy) · 2016-2018 (Lisbon)
- Shipped Django + DRF backends for 6 different client projects across e-commerce, travel, and logistics. Small team; wore many hats.
- Maintained a shared internal "Django boilerplate" — auth, billing, admin, observability — used as the starting point for every new client engagement.

## Selected Work / Portfolio

### 1. Open-source: `django-async-queue` (2024, 1.8k GitHub stars)
A small library for first-class async Celery-style workers in Django. Designed after repeated pain shipping long-running jobs in async views. Used in production at Fintrace and 2 public companies.

### 2. Technical writing: "The PostgreSQL migration I got wrong" (2023, ~80k reads)
Widely-shared post-mortem of a 2022 production incident where a botched ALTER TABLE during peak traffic caused a 23-minute outage. Includes the exact SQL, the monitoring that would have caught it, and the runbook that resulted.

### 3. Talk: "Redis Streams in production: the failure modes we didn't expect" (PyCon EU 2024)
30-minute talk on moving from Celery+RabbitMQ to Redis Streams — the edge cases the docs don't cover (consumer-group rebalances, tombstone compaction, slow-consumer poison).

### 4. Contribution: Kafka-Python (ongoing, ~8 merged PRs)
Small but sustained contributions to the Python Kafka client — batch-compression fixes, connection-pool debugging tooling.

### 5. Internal tool: `pgreindex-safe` (2022, open-sourced)
A small Python CLI wrapping `pg_repack` with safety checks (replica lag gate, vacuum-state check, partition-aware ordering). Written after rebuilding an index during peak traffic and learning what happens when you forget the lag check.

## Certifications & Education
- **AWS Solutions Architect — Associate** (2022, re-certified 2024)
- **BSc Computer Engineering** — NOVA University Lisbon (2016)
- **Crafting Interpreters** (2021, completed), **Designing Data-Intensive Applications** (read cover-to-cover, re-read yearly)

## Remote work / working preferences
- Working hours: flexible within CET (typically 09:30-18:00 Lisbon)
- Strong async-written-communication habit — weekly written updates, decisions in docs not chat
- Prefer small senior teams (10-40 engineers) over very early stage or very large
- Not interested in: crypto/web3, US-only companies (visa/timezone friction), roles requiring on-site presence, pure management tracks

## What I'm looking for (role filter — used by the workflow)
- Senior or Staff Backend Engineer
- Python/Django primary, PostgreSQL + Redis + AWS stack
- Remote, European-friendly hours (UTC-1 to UTC+3 overlap)
- EUR 90k+ base
- Series A to C preferred; open-source culture a big plus; 4-day week a big plus
