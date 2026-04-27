---
title: DVNC.AI
emoji: 🧠
colorFrom: gray
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
short_description: Connectome-native scientific discovery workspace
---

# DVNC.AI

This root patch lets the existing nested `dvnc_ai_v2_hf/` folder run on Hugging Face Spaces by providing a root-level `app.py` entrypoint, which Hugging Face requires for Gradio Spaces.[cite:166][cite:163]

## Required existing folder
This patch assumes the repository already contains the uploaded folder:
- `dvnc_ai_v2_hf/`

The bridge file imports the `demo` object from `dvnc_ai_v2_hf.app` so the existing implementation can remain in place while the Space launches from the repository root.[cite:166][cite:323]

## Required secret
Set `ANTHROPIC_API_KEY` in the Space secrets for live Claude calls.[cite:294][cite:300]
