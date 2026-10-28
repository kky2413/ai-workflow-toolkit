# AI Workflow Toolkit (public, standard-library only)

A small **general-purpose** collection of scripts and prompts for AI-assisted task execution. Designed for local practice with VS Code / Codex; it does **not** contain actual test problems, private documents, API keys, or pre-completed assignments.

> This is an independent personal preparation resource, not an official SK hynix or examination tool. The current task instructions and the organizer's rules override everything in this repository.

## Contents

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Concise guidance for Codex when working inside this repository |
| `scripts/inventory.py` | Read-only inventory of provided files, types, and sizes |
| `scripts/data_profile.py` | CSV/JSON shape, missing values and numeric summaries |
| `scripts/verify_outputs.py` | Verify explicitly listed deliverables, without uploading |
| `templates/TASK_PLAN.md` | Scope and acceptance-criteria worksheet |
| `templates/DECISION_LOG.md` | Evidence / decision / result log |
| `templates/FINAL_CHECK.md` | Submission verification checklist |
| `PROMPTS.md` | Copyable task-analysis and review prompts |
| `examples/` | Synthetic demo dataset and manifest only |
| `tests/` | Unit tests for the three scripts |

All tools use **Python 3.9+ standard library only**. There is no `pip install` step.

## Quick start (PowerShell or Linux shell)

From the project root:

```bash
python scripts/inventory.py examples
python scripts/data_profile.py examples/sample_sales.csv
python scripts/data_profile.py examples/sample_cases.json
python scripts/verify_outputs.py --root . --manifest examples/manifest.sample.json
python -m unittest discover -s tests -v
```

On Ubuntu, `python3` may be required instead of `python`.

To save a report locally, redirect standard output to a file **outside the public toolkit directory**, e.g. PowerShell `python scripts/data_profile.py data.csv > report.json`, or Linux likewise. Do not commit assessment data or reports into a public repository.

## How to use when a task allows public GitHub downloads

1. Follow the assessment platform's instructions first. Only use the toolkit if publicly accessible GitHub code is explicitly permitted.
2. Within the permitted terminal, clone the public repository **into a separate helper folder**:

   ```bash
   git clone https://github.com/REPLACE_WITH_YOUR_USERNAME/ai-workflow-toolkit.git helpers/ai-workflow-toolkit
   ```

3. Work with the actual assignment materials only inside the permitted work environment. Review each script before running it. If necessary, run it against task files using explicit local paths; e.g. `python helpers/ai-workflow-toolkit/scripts/inventory.py .`.
4. Use only the relevant part of the toolkit. Implement and verify the actual assignment independently; do not substitute a previous complete solution for the assignment.
5. **Do not push/upload/send** assignment files, answers, logs, or generated outputs to GitHub or any external service.

`AGENTS.md` is repository-scoped guidance when Codex operates within this repository; cloning the toolkit as a subfolder does not automatically apply its instructions to unrelated task directories. Ask Codex to read the relevant guidance explicitly if permitted.

## Limits and privacy

- CSV and JSON are directly supported. PDF, DOCX, spreadsheets, and images need separate parsers/tools, which are **not** automatically installed or accessed here.
- A profile report is a heuristic preview, not a replacement for full data validation, semantic analysis, or manual review.
- Scripts operate on local paths only; there are no HTTP calls, shell hooks, remote loggers, telemetry, or API credentials.
- Never place private, restricted, or assignment-provided data into this public repository.
