# Tailored CV Gallery — Vercel deployment

Static site. No build step at deploy time — `gallery/scripts/build.py` was already run locally and the resulting HTML is committed.

## What's here

```
gallery/
├── index.html              # Landing — 5 role cards
├── role/<slug>.html        # Per-role comparison page (master vs tailored)
├── tailored/<slug>.html    # Standalone tailored CV (used in iframe + direct link)
├── master-cv.html          # Daniel's master CV (the "before")
├── data/cvs.json           # Source of truth — pulled from n8n exec 114545
├── assets/styles.css       # Gallery shell styles
├── scripts/build.py        # Regenerator — only re-run if cvs.json changes
└── vercel.json             # Clean URLs + security headers
```

## Deploy on Vercel (manual)

**Option A — drag & drop (fastest, no GitHub needed):**
1. Open https://vercel.com/new
2. Drag the `gallery/` folder onto the dropzone.
3. Framework preset: **Other**. Root directory: leave empty. Build command: leave empty. Output directory: `.`
4. Hit Deploy. Done — you get a `*.vercel.app` URL.

**Option B — GitHub-connected:**
1. Push this repo to GitHub.
2. On Vercel, "Add New Project" → import the repo.
3. Set **Root Directory** to `gallery`. Build command: empty. Output directory: `.`
4. Deploy.

## Re-build after editing cvs.json

```
python3 gallery/scripts/build.py
```

Idempotent. Overwrites `index.html`, all `role/*.html`, all `tailored/*.html`, and `master-cv.html`.

## Data lineage

`data/cvs.json` was extracted from n8n execution `114545` (run timestamp `2026-04-26T04:55:05Z`). Every field on every CV in this gallery is verifiable in the workflow's `daniel_role_master` data table for that run. No fabrication.
