# Discovery Dashboard — Communications Services Zone

Tracks TDI discovery flow (`In Discovery` → `Ready to Plan`) for the
Communications Services zone in Jira, bucketed into the org's 3S (3-sprint,
42-day) cycles.

**Live dashboard:** see the repo's GitHub Pages URL (Settings → Pages).

## How it stays fresh

A scheduled GitHub Action (`.github/workflows/refresh.yml`) runs on weekday
mornings (and can be triggered manually from the Actions tab), re-pulls data
from Jira, and commits the refreshed `index.html` / `dashboard.html` /
`data.json` back to this repo. GitHub Pages serves `index.html` directly —
no server needed to view it.

The Jira credentials are stored as repo secrets (`JIRA_EMAIL`,
`JIRA_API_TOKEN`) and never appear in code or commit history.

## Local development

```bash
python3 pipeline.py   # pulls fresh data from Jira into data.json
python3 build.py       # renders template.html + data.json -> dashboard.html / index.html
python3 server.py      # optional: local server at http://localhost:8765, adds a live "Refresh from Jira" button
```

Edit `template.html` for layout/behavior changes, then re-run `build.py`.

## Data model

- **TDIs** = Jira project `TDI`, issue type `Feature`, Zone = Communications
  Services, with an assignee and a target quarter (Fix Version) both set —
  this matches the GitHub release dashboard's counts.
- **Discovery allocation** = sum of "Allocation in Days" on child Epics (any
  project) whose title contains "discovery" and whose parent is the TDI.
- **3S cycles** are fixed 42-day windows anchored to the org's official 3S
  calendar; a TDI's transition is assigned to the cycle containing its
  actual `In Discovery → Ready to Plan` changelog timestamp.
