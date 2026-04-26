# Screenshot capture guide — Case 2 README

Take 8 screenshots, save them in this folder with the exact filenames listed below. The main `README.md` already references these paths — once you drop the file in, the README renders the image. If a shot is hard to capture, skip it (the README degrades gracefully).

**General settings:** 1080p minimum (1440×900 ideal), n8n editor in **light mode** (better contrast for printed/PDF judges). Crop tightly. JPEG → PNG if the workflow re-converts.

---

| # | Filename | What to capture | Where on n8n |
|---|---|---|---|
| 1 | `01-canvas-overview.png` | Full n8n canvas zoomed so all 11 sticky notes are readable. Include the schedule trigger on the left and the Send Weekly Digest on the right. | Workflow editor → fit-to-screen |
| 2 | `02-config-node.png` | The `Config + Run Context` Code node opened. Show the `criteria`, `allSources`, and `delivery` blocks. | Click the Config node → "Code" tab |
| 3 | `03-credentials-attached.png` | The Credentials side panel showing the 4 credential types (Firecrawl / OpenAI / Drive / Gmail) attached. **Blur the actual credential names** if they contain personal info. | Settings → Credentials, OR open any node and screenshot its Credentials dropdown |
| 4 | `04-data-tables-after-run.png` | The n8n Data Tables UI showing the 3 auto-created tables populated: `daniel_seen_roles`, `daniel_role_master`, `daniel_filtered_out`. | Sidebar → Data Tables, click each table to show row counts |
| 5 | `05-execution-success.png` | Execution timeline of run `114545` (or any fresh successful run). Show the green nodes and total runtime. | Sidebar → Executions → click 114545 |
| 6 | `06-monday-email.png` | A rendered Monday digest email — the warm header, 1 High card, 4 Medium cards, filtered-out section collapsed. | Gmail inbox → open the digest email |
| 7 | `07-tailored-cv-preview.png` | One delivered tailored CV opened in browser at full A4 width. The DNA.inc one (highest fit score, 80) is the best showcase. | Open `gallery/tailored/dna-inc.html` in browser, hit fullscreen |
| 8 | `08-filtered-evidence-quote.png` | A row from `daniel_filtered_out` data table showing `reason_code` + `reason_quote` (verbatim JD substring). | Data Tables → daniel_filtered_out → expand any row |

---

After you drop the files in this folder, the main README at the repo root will display them automatically. No further edits needed.
