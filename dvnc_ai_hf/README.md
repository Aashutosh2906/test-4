# DVNC.AI Hugging Face Space

A premium Gradio app for scientific discovery workflows with:
- cinematic chat interface inspired by modern editorial AI products
- 3D-style connectome view with active path illumination
- 7-agent reasoning timeline
- flippable candidate cards for alternative discovery paths
- model switching UI for orchestration tiers

## Files
- `app.py` — entrypoint for Hugging Face Spaces
- `requirements.txt` — Python dependencies
- `assets/` — reserved for local assets if needed

## Deploy
1. Create a new **Gradio** Space on Hugging Face.
2. Upload the full folder contents.
3. Ensure the entry file is `app.py`.
4. Launch.

## Notes
This package includes a working front-end prototype and demo orchestration logic. Replace the mock `run_discovery()` function with your production Claude / routing / graph backend.
