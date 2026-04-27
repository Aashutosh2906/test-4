import json
import math
import random
import gradio as gr

MODELS = [
    {"name": "DVNC Sovereign", "tag": "flagship", "desc": "Maximum depth orchestration for frontier discovery"},
    {"name": "DVNC Atlas", "tag": "research", "desc": "Balanced reasoning, graph traversal, and synthesis"},
    {"name": "DVNC Curie", "tag": "lab", "desc": "Experimental hypothesis generation for anomalous signals"},
]

AGENTS = [
    "Query Interpreter",
    "Graph Divergence Mapper",
    "Evidence Harvester",
    "Analogy Engine",
    "Hypothesis Composer",
    "Adversarial Critic",
    "Experimental Program Designer",
]

NODES = [
    {"id": "seed", "label": "Seed Query", "group": "core", "x": 0, "y": 0, "z": 0},
    {"id": "bio", "label": "Biomaterials", "group": "domain", "x": 18, "y": 12, "z": -8},
    {"id": "card", "label": "Cardiac Repair", "group": "domain", "x": 34, "y": 2, "z": 14},
    {"id": "nano", "label": "Nanostructure", "group": "bridge", "x": 14, "y": -18, "z": 16},
    {"id": "selfasm", "label": "Self-Assembly", "group": "bridge", "x": 30, "y": -16, "z": -16},
    {"id": "electro", "label": "Electro-signalling", "group": "mechanism", "x": 48, "y": 12, "z": -10},
    {"id": "immune", "label": "Immune Modulation", "group": "mechanism", "x": 54, "y": -8, "z": 10},
    {"id": "trial", "label": "Validation Path", "group": "outcome", "x": 70, "y": 0, "z": 0},
    {"id": "alt1", "label": "Piezoelectric Scaffold", "group": "candidate", "x": 44, "y": 28, "z": 14},
    {"id": "alt2", "label": "Peptide Mesh", "group": "candidate", "x": 42, "y": -28, "z": -14},
]

EDGES = [
    ("seed", "bio"), ("seed", "nano"), ("bio", "card"), ("nano", "selfasm"),
    ("selfasm", "electro"), ("card", "immune"), ("electro", "trial"), ("immune", "trial"),
    ("card", "alt1"), ("selfasm", "alt2"), ("alt1", "trial"), ("alt2", "trial")
]

DEFAULT_PATH = ["seed", "nano", "selfasm", "electro", "trial"]

CANDIDATES = [
    {
        "title": "Piezoelectric Scaffold Cascade",
        "front": "Use mechano-electric scaffolds to convert cardiac strain into micro-current signalling.",
        "back": "Discovery path: anomalous healing signal -> piezoelectric analog -> ion-channel entrainment -> tissue regeneration. Risk: power density and fibrosis coupling.",
        "score": 92,
        "novelty": "High",
        "agent": "Hypothesis Composer"
    },
    {
        "title": "Peptide Self-Assembly Mesh",
        "front": "Deploy dynamic peptide meshes that self-assemble around damaged myocardium and guide repair.",
        "back": "Discovery path: self-assembly -> local immune choreography -> regenerative substrate formation. Risk: degradation timing and targeting specificity.",
        "score": 88,
        "novelty": "High",
        "agent": "Analogy Engine"
    },
    {
        "title": "Immune-Tuned Conductive Hydrogel",
        "front": "Blend conductivity with macrophage-state modulation to reduce scarring and restore conduction.",
        "back": "Discovery path: inflammation mismatch -> conductive medium -> macrophage polarization -> synchronized healing. Risk: persistence and biocompatibility.",
        "score": 85,
        "novelty": "Medium-High",
        "agent": "Adversarial Critic"
    }
]


def build_connectome_html(path_ids):
    active = set(path_ids)
    node_map = {n['id']: n for n in NODES}
    lines = []
    for a, b in EDGES:
        na, nb = node_map[a], node_map[b]
        active_edge = a in active and b in active and abs(path_ids.index(a) - path_ids.index(b)) == 1 if a in path_ids and b in path_ids else False
        cls = "edge active" if active_edge else "edge"
        lines.append(f'<line class="{cls}" x1="{na["x"]*6+420:.1f}" y1="{na["y"]*6+280:.1f}" x2="{nb["x"]*6+420:.1f}" y2="{nb["y"]*6+280:.1f}" />')
    circles = []
    labels = []
    for n in NODES:
        cx = n['x']*6 + 420
        cy = n['y']*6 + 280
        cls = f"node {n['group']} {'active' if n['id'] in active else ''}"
        circles.append(f'<g class="node-wrap"><circle class="{cls}" cx="{cx:.1f}" cy="{cy:.1f}" r="{17 if n["id"] in active else 12}" /><circle class="halo {'active' if n['id'] in active else ''}" cx="{cx:.1f}" cy="{cy:.1f}" r="{28 if n["id"] in active else 0}" /></g>')
        labels.append(f'<text class="label {'active' if n["id"] in active else ''}" x="{cx+16:.1f}" y="{cy-16:.1f}">{n["label"]}</text>')
    return f'''
    <div class="brain-shell">
      <div class="brain-header">
        <div>
          <p class="eyebrow">Connectome</p>
          <h3>Concept Brain</h3>
        </div>
        <div class="brain-legend">
          <span><i class="dot dot-live"></i> active route</span>
          <span><i class="dot dot-node"></i> concept nodes</span>
        </div>
      </div>
      <div class="brain-stage">
        <div class="orb orb-a"></div><div class="orb orb-b"></div>
      <svg viewBox="0 0 840 560" class="brain-svg" role="img" aria-label="DVNC connectome visualisation">                   <defs>          </defs>
          {''.join(lines)}
          {''.join(circles)}
          {''.join(labels)}
        </svg>
      </div>
    </div>
    '''


def build_cards_html(cards):
    items = []
    for i, c in enumerate(cards):
        items.append(f'''
        <article class="candidate-card" tabindex="0">
          <div class="candidate-card-inner">
            <div class="candidate-face candidate-front">
              <div class="candidate-top"><span class="chip">{c['agent']}</span><span class="score">{c['score']}</span></div>
              <h4>{c['title']}</h4>
              <p>{c['front']}</p>
              <div class="meta-row"><span>Novelty</span><strong>{c['novelty']}</strong></div>
              <button class="mini">Flip insight</button>
            </div>
            <div class="candidate-face candidate-back">
              <div class="candidate-top"><span class="chip alt">Alternative path</span><span class="score">{c['score']}</span></div>
              <h4>{c['title']}</h4>
              <p>{c['back']}</p>
              <div class="meta-row"><span>Swap into route</span><strong>Enabled</strong></div>
              <button class="mini">Return</button>
            </div>
          </div>
        </article>
        ''')
    return '<div class="candidate-grid">' + ''.join(items) + '</div>'


def build_agent_timeline(reasoning):
    rows = []
    for r in reasoning:
        rows.append(f'''
        <div class="agent-step">
          <div class="agent-index">{r['step']}</div>
          <div class="agent-copy">
            <div class="agent-head"><h4>{r['agent']}</h4><span>{r['tag']}</span></div>
            <p>{r['summary']}</p>
          </div>
        </div>
        ''')
    return '<div class="timeline">' + ''.join(rows) + '</div>'


def build_chat_html(query, result):
    bubbles = f'''
    <div class="chat-thread">
      <div class="bubble bubble-user">
        <span class="role">You</span>
        <p>{query}</p>
      </div>
      <div class="bubble bubble-ai">
        <span class="role">DVNC Sovereign</span>
        <p>{result['summary']}</p>
      </div>
      <div class="bubble bubble-system">
        <span class="role">Discovery Signal</span>
        <p><strong>Primary hypothesis:</strong> {result['primary_hypothesis']}</p>
      </div>
    </div>
    '''
    return bubbles


def build_models_html(selected):
    items = []
    for m in MODELS:
        active = 'active' if m['name'] == selected else ''
        items.append(f'''<div class="model-pill {active}"><span class="model-name">{m['name']}</span><span class="model-tag">{m['tag']}</span><small>{m['desc']}</small></div>''')
    return '<div class="model-switcher">' + ''.join(items) + '</div>'


def run_discovery(query, model_name):
    random.seed(len(query) + len(model_name))
    if "curie" in query.lower() or "einstein" in query.lower():
        primary = "Map the anomaly first, then force a distant analogy before composing the experimental programme."
        path = ["seed", "bio", "card", "immune", "trial"]
    else:
        primary = "Use a self-assembling conductive scaffold that transforms mechanical strain into local regenerative signalling."
        path = DEFAULT_PATH
    summaries = [
        "Normalises the user prompt into a graph-searchable seed and isolates the tension inside the question.",
        "Finds remote conceptual bridges instead of staying near the starting domain cluster.",
        "Pulls evidence packets and conflict signals required for grounded hypothesis formation.",
        "Generates cross-domain analogies with a bias toward mechanism transfer rather than keyword similarity.",
        "Composes the lead hypothesis and two structurally different variants.",
        "Attacks weak assumptions, hidden confounders, and feasibility gaps.",
        "Produces a staged validation plan with measurable falsification criteria."
    ]
    reasoning = [{"step": i+1, "agent": AGENTS[i], "tag": ["input","graph","evidence","analogy","compose","critique","experiment"][i], "summary": summaries[i]} for i in range(7)]
    result = {
        "summary": "A deeper route was chosen through the concept graph, with live alternatives preserved as candidate cards so the reasoning path can be swapped rather than hidden.",
        "primary_hypothesis": primary,
        "reasoning": reasoning,
        "cards": CANDIDATES,
        "path": path,
        "metrics": {
            "Novelty": 93,
            "Mechanistic clarity": 89,
            "Experimental tractability": 82,
            "Cross-domain distance": 91
        }
    }
    chat_html = build_chat_html(query, result)
    connectome_html = build_connectome_html(path)
    cards_html = build_cards_html(CANDIDATES)
    timeline_html = build_agent_timeline(reasoning)
    metrics = "\n".join([f"- {k}: {v}/100" for k, v in result["metrics"].items()])
    hypothesis = f"""# Discovery Output\n\n**Model:** {model_name}\n\n**Primary hypothesis:** {result['primary_hypothesis']}\n\n## Scoring\n{metrics}\n\n## Experimental outline\n1. Construct the candidate material or protocol.\n2. Test mechanistic signal expression under controlled conditions.\n3. Compare against baseline and nearest-neighbour alternatives.\n4. Falsify using the adversarial risk criteria surfaced in the reasoning path.\n"""
    return chat_html, connectome_html, timeline_html, cards_html, hypothesis, build_models_html(model_name)

CSS = r'''
:root {
    --bg: #ffffff; --bg2: #f8f8f8;
    --panel: rgba(248,248,248,.95);  --panel-solid: #fafafa;
    --panel-2: rgba(245,245,245,.95);   --line: rgba(0,0,0,.15);
    --soft: rgba(0,0,0,.60);  --text: #000000;
    --muted: #555555;   --gold: #ff6600;
  --teal: #7be7dd;
  --blue: #7ea9ff;
  --shadow: 0 20px 60px rgba(0,0,0,.38);
  --radius: 22px;
}
html, body, .gradio-container {
  background: #ffffff !important;  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
}
.gradio-container {max-width: 1550px !important; padding: 22px !important;}
#dvnc-shell {border: 1px solid var(--line); border-radius: 28px; overflow: hidden; background: #ffffff; box-shadow: var(--shadow); backdrop-filter: blur(18px);}#dvnc-shell .wrap {display:grid; grid-template-columns: 1.12fr .88fr; min-height: 84vh;}
#dvnc-shell .left, #dvnc-shell .right {padding: 24px;}
#dvnc-shell .left {border-right: 1px solid var(--line); display:flex; flex-direction:column; gap:18px;}
#dvnc-shell .right {display:grid; grid-template-rows:auto auto 1fr auto; gap:18px;}
.hero-bar {display:flex; justify-content:space-between; align-items:center; gap:16px; padding-bottom:8px;}
.brand {display:flex; align-items:center; gap:14px;}
.logo {width:42px; height:42px; border-radius:14px; background: linear-gradient(135deg, rgba(242,210,147,.28), rgba(123,231,221,.16)); border:1px solid rgba(255,255,255,.1); display:grid; place-items:center; box-shadow: inset 0 1px 0 rgba(255,255,255,.08);}
.logo svg {width:24px; height:24px; color: var(--gold);}
.brand h1 {font-size: 1.05rem; margin:0; font-weight: 650; letter-spacing:.02em;}
.brand p {margin:3px 0 0; color:var(--muted); font-size:.84rem;}
.status {display:flex; gap:10px; align-items:center; color:var(--soft); font-size:.85rem;}
.status-dot {width:10px; height:10px; border-radius:50%; background:var(--teal); box-shadow:0 0 0 6px rgba(123,231,221,.08), 0 0 18px rgba(123,231,221,.4);}
.panel {background: #ffffff; border:1px solid var(--line); border-radius: 22px; box-shadow: inset 0 1px 0 rgba(0,0,0,.04);}.chat-panel {padding:18px; display:flex; flex-direction:column; gap:14px; min-height: 340px;}
.querybox textarea, .querybox input {background: transparent !important; color: var(--text) !important;}
.querybox, .querybox > div {background: rgba(255,255,255,.02) !important; border-radius: 18px !important; border-color: var(--line) !important;}
.chat-thread {display:flex; flex-direction:column; gap:14px;}
.bubble {max-width: 86%; padding:16px 18px; border-radius: 22px; position:relative; border:1px solid var(--line);}
.bubble p {margin:8px 0 0; line-height:1.6; font-size:.96rem;}
.bubble .role {font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted);}
.bubble-user {align-self:flex-end; background: linear-gradient(135deg, rgba(126,169,255,.18), rgba(126,169,255,.08));}
.bubble-ai {align-self:flex-start; background: linear-gradient(135deg, rgba(255,255,255,.06), rgba(255,255,255,.03));}
.bubble-system {align-self:flex-start; background: linear-gradient(135deg, rgba(242,210,147,.12), rgba(242,210,147,.04));}
.model-switcher {display:grid; grid-template-columns:repeat(3,1fr); gap:12px;}
.model-pill {padding:14px; border:1px solid var(--line); border-radius:18px; background:rgba(255,255,255,.02); display:flex; flex-direction:column; gap:4px; min-height: 96px;}
.model-pill.active {border-color: rgba(242,210,147,.45); background: linear-gradient(135deg, rgba(242,210,147,.14), rgba(255,255,255,.03)); box-shadow: inset 0 0 0 1px rgba(242,210,147,.08);}
.model-name {font-weight:650;}
.model-tag {font-size:.76rem; text-transform:uppercase; letter-spacing:.12em; color:var(--gold);}
.model-pill small {color:var(--muted); line-height:1.45;}
.brain-shell {padding:18px; height:100%;}
.brain-header {display:flex; justify-content:space-between; align-items:flex-end; gap:16px; margin-bottom:10px;}
.eyebrow {font-size:.72rem; letter-spacing:.16em; text-transform:uppercase; color:var(--gold); margin:0 0 4px;}
.brain-header h3 {margin:0; font-size:1.12rem;}
.brain-legend {display:flex; gap:14px; color:var(--muted); font-size:.8rem; flex-wrap:wrap;}
.dot {width:10px; height:10px; display:inline-block; border-radius:50%; margin-right:6px;}
.dot-live {background:var(--gold); box-shadow:0 0 12px rgba(242,210,147,.65);} .dot-node {background:var(--teal);}
.brain-stage {position:relative; min-height:360px; overflow:auto; background: #ffffff; border:1px solid rgba(0,0,0,.05);.orb-a {width:180px; height:180px; background:rgba(123,231,221,.16); left:10%; top:18%;}
.brain-svg {width:1200px; height:auto; display:block; margin:0 0 0 -180px; min-height:500px;}.edge {stroke: rgba(132,153,153,.18); stroke-width:2;}.node.core {fill:#f5f7fb;} .node.domain {fill:#7be7dd;} .node.bridge {fill:#8ea4ff;} .node.mechanism {fill:#f2d293;} .node.outcome {fill:#ffd9a6;} .node.candidate {fill:#ddadff;}
.node.active {stroke:#fff7df; stroke-width:2.4; filter:url(#glow);}
.halo {fill:none;} .halo.active {stroke: rgba(242,210,147,.22); stroke-width:10;}
.label {fill: #000000; font-size: 12px; letter-spacing: .02em;} .label.active {fill: #000000;}.timeline {display:flex; flex-direction:column; gap:10px;}
.agent-step {display:grid; grid-template-columns:42px 1fr; gap:12px; padding:12px; border:1px solid var(--line); border-radius:18px; background:rgba(255,255,255,.02);}
.agent-index {width:42px; height:42px; border-radius:14px; display:grid; place-items:center; font-weight:700; color:var(--gold); background:rgba(242,210,147,.08); border:1px solid rgba(242,210,147,.16);}
.agent-head {display:flex; justify-content:space-between; gap:12px; align-items:center; margin-bottom:4px;}
.agent-head h4 {margin:0; font-size:.98rem;} .agent-head span {font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted);} .agent-copy p {margin:0; color:#cbd3e2; font-size:.9rem; line-height:1.55;}
.candidate-grid {display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:14px;}
.candidate-card {background:none; perspective:1200px; min-height: 250px;}
.candidate-card-inner {position:relative; width:100%; height:100%; min-height:250px; transition: transform .8s cubic-bezier(.2,.7,.1,1); transform-style:preserve-3d;}
.candidate-card:hover .candidate-card-inner, .candidate-card:focus .candidate-card-inner, .candidate-card:focus-within .candidate-card-inner {transform: rotateY(180deg) translateY(-4px);}
.candidate-face {position:absolute; inset:0; padding:18px; border-radius:22px; border:1px solid var(--line); background: linear-gradient(180deg, rgba(19,22,29,.96), rgba(11,13,18,.96)); backface-visibility:hidden; box-shadow: inset 0 1px 0 rgba(255,255,255,.04), var(--shadow); display:flex; flex-direction:column; gap:12px;}
.candidate-back {transform: rotateY(180deg); background: linear-gradient(180deg, rgba(29,23,16,.96), rgba(12,11,10,.96));}
.candidate-top {display:flex; justify-content:space-between; align-items:center; gap:8px;}
.chip {font-size:.72rem; text-transform:uppercase; letter-spacing:.12em; color:var(--teal); padding:7px 10px; border-radius:999px; background:rgba(123,231,221,.08); border:1px solid rgba(123,231,221,.18);} .chip.alt {color:var(--gold); background:rgba(242,210,147,.08); border-color: rgba(242,210,147,.18);}
.score {font-weight:700; color:var(--gold);}
.candidate-face h4 {margin:0; font-size:1rem; line-height:1.3;}
.candidate-face p {margin:0; color:#cbd3e2; line-height:1.6; font-size:.92rem;}
.meta-row {margin-top:auto; display:flex; justify-content:space-between; color:var(--muted); font-size:.84rem;}
.mini {margin-top:8px; align-self:flex-start; color:var(--text); padding:10px 12px; border-radius:14px; border:1px solid var(--line); background:rgba(255,255,255,.03);}
.prosebox {padding:18px; white-space:pre-wrap; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; line-height:1.55; color:#dfe6f3;}
.gr-button-primary {background: linear-gradient(135deg, rgba(242,210,147,.92), rgba(224,178,92,.92)) !important; color:#1b1408 !important; border: none !important;}
.gr-button-secondary {background: rgba(255,255,255,.05) !important; color: var(--text) !important; border: 1px solid var(--line) !important;}
footer {display:none !important;}
@keyframes pulseEdge {to {stroke-dashoffset: -32;}}
@media (max-width: 1180px){#dvnc-shell .wrap{grid-template-columns:1fr;}#dvnc-shell .left{border-right:0;border-bottom:1px solid var(--line)}.candidate-grid,.model-switcher{grid-template-columns:1fr;} }
'''

HEAD = '''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
'''

with gr.Blocks(css=CSS, head=HEAD, theme=gr.themes.Base(), fill_height=True) as demo:
    gr.HTML('''
    <div id="dvnc-shell">
          <div class="hero-bar">
            <div class="brand">
              <div class="logo" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 17L12 4l7 13"/><path d="M8.5 12.5h7"/><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/></svg>
              </div>
              <div>
                <h1>DVNC.AI</h1>
                <p>Sovereign discovery interface · connectome-native reasoning</p>
              </div>
            </div>
            <div class="status"><span class="status-dot"></span><span>Live orchestration</span></div>
          </div>
                      </div>
    ''')
    model_html = gr.HTML(build_models_html("DVNC Sovereign"))
    with gr.Row():
        model = gr.Dropdown(choices=[m["name"] for m in MODELS], value="DVNC Sovereign", label="Model tier")
    query = gr.Textbox(label="Discovery query", elem_classes=["querybox"], placeholder="Enter a scientific question, anomaly, or breakthrough direction…", lines=4)
    with gr.Row():
        run_btn = gr.Button("Run discovery", variant="primary")
        example_btn = gr.Button("Load example", variant="secondary")
    chat = gr.HTML('<div class="panel chat-panel"><div class="chat-thread"><div class="bubble bubble-ai"><span class="role">DVNC</span><p>Enter a query to activate the 7-agent discovery stack and illuminate the chosen path through the concept brain.</p></div></div></div>')
    connectome = gr.HTML(build_connectome_html(DEFAULT_PATH))
    timeline = gr.HTML('<div class="panel" style="padding:18px"><div class="timeline"></div></div>')
    cards = gr.HTML('<div class="panel" style="padding:18px"><div class="candidate-grid"></div></div>')
    output = gr.Markdown("# Discovery Output\n\nAwaiting query.")

    def load_example():
        return "How could a self-assembling conductive biomaterial improve cardiac tissue regeneration by converting mechanical strain into repair signalling?"

    example_btn.click(fn=load_example, outputs=query)
    run_btn.click(fn=run_discovery, inputs=[query, model], outputs=[chat, connectome, timeline, cards, output, model_html])

if __name__ == "__main__":
    demo.launch()
