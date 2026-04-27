---
title: DVNC.AI
emoji: 🧠
colorFrom: gray
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
short_description: Connectome-native scientific discovery workspace for Hugging Face Spaces
---

# DVNC.AI — Hugging Face Space (Version 2)

This package is designed for direct upload to a **Gradio** Hugging Face Space.

## Root files to keep at the top level
- `app.py`
- `requirements.txt`
- `README.md`
- `core/`
- `ui/`
- `assets/`

## What this version adds
- Claude API wiring scaffold using the Anthropic Python SDK
- Three.js-based connectome canvas embedded inside the Gradio interface
- Agent-by-agent expandable trays
- Candidate cards that flip to show alternative discovery routes
- A clearer repository structure so you can replace mock orchestration with your production backend

## Hugging Face upload instructions
If you are uploading manually in the Hugging Face web UI, upload the **contents** of this folder directly into the **root of your Space repository**.

That means these paths should exist at the top level of the Space:
- `app.py`
- `requirements.txt`
- `README.md`
- `core/dvnc_engine.py`
- `ui/connectome.html`

Do **not** upload the zip itself into a nested folder inside the Space. Extract it locally first, then upload the extracted contents to the repository root.[cite:276][cite:292][cite:166]

## Required secret
In your Hugging Face Space, go to **Settings → Variables and secrets** and add:
- `ANTHROPIC_API_KEY` = your Claude API key

The Anthropic Python SDK reads `ANTHROPIC_API_KEY` from the environment.[cite:294][cite:300]

## How to swap in your real logic
- Replace `core/dvnc_engine.py` graph mocks with your real query router, KG lookup, and 7-agent orchestration.
- Keep `app.py` as the Gradio entrypoint expected by Hugging Face Spaces.[cite:276]

## Notes
This build uses a no-bundle Three.js import-map workflow suitable for a static embedded front-end panel.[cite:297][cite:299]
