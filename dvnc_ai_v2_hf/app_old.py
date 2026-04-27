import json
import pathlib
import gradio as gr
from .core.dvnc_engine import run_discovery

MODELS = ["DVNC Sovereign", "DVNC Atlas", "DVNC Curie"]

BASE_DIR = pathlib.Path(__file__).resolve().parent

#CONNECTOME_SNIPPET = (BASE_DIR / "ui" / "connectome.html").read_text(encoding="utf-8")
# replaced base connectome with enhanced connectome.

CONNECTOME_SNIPPET = (BASE_DIR / "ui" / "enhanced_connectome.html").read_text(encoding="utf-8")



def build_models_html(selected):
    data = {
        "DVNC Sovereign": "Maximum depth orchestration",
        "DVNC Atlas": "Balanced research mode",
        "DVNC Curie": "Experimental anomaly mode",
    }
    out = []
    for name, desc in data.items():
        active = "active" if name == selected else ""
        out.append(f'<div class="model-pill {active}"><span>{name}</span><small>{desc}</small></div>')
    return '<div class="model-strip">' + ''.join(out) + '</div>'


def build_chat_html(query, data):
    return f'''
    <div class="chat-panel panel">
      <div class="bubble user"><span class="role">You</span><p>{query}</p></div>
      <div class="bubble ai"><span class="role">DVNC</span><p>{data.get("summary","")}</p></div>
      <div class="bubble system"><span class="role">Primary Hypothesis</span><p>{data.get("primary_hypothesis","")}</p></div>
    </div>
    '''


def build_reasoning_html(steps):
    chunks = []
    for s in steps:
        chunks.append(f'''
        <details class="tray" {'open' if s['step']==1 else ''}>
          <summary><span class="step">{s['step']}</span><div><strong>{s['agent']}</strong><small>{s['tag']}</small></div></summary>
          <div class="tray-body">{s['summary']}</div>
        </details>
        ''')
    return '<div class="panel tray-panel">' + ''.join(chunks) + '</div>'


def build_cards_html(cards):
    html = []
    for c in cards:
        html.append(f'''
        <article class="candidate-card" tabindex="0">
          <div class="candidate-card-inner">
            <div class="candidate-face front">
              <div class="top"><span class="chip">{c['agent']}</span><span class="score">{c['score']}</span></div>
              <h4>{c['title']}</h4>
              <p>{c['front']}</p>
              <div class="meta"><span>Novelty</span><strong>{c['novelty']}</strong></div>
            </div>
            <div class="candidate-face back">
              <div class="top"><span class="chip alt">Alt path</span><span class="score">{c['score']}</span></div>
              <h4>{c['title']}</h4>
              <p>{c['back']}</p>
              <div class="meta"><span>Swap state</span><strong>Ready</strong></div>
            </div>
          </div>
        </article>
        ''')
    return '<div class="panel cards-panel"><div class="candidate-grid">' + ''.join(html) + '</div></div>'


def build_metrics_md(metrics, model_used):
    lines = [f"# Discovery Output\n", f"**Claude model used:** {model_used}\n", "## Metrics"]
    for k, v in metrics.items():
        lines.append(f"- {k}: {v}/100")
    lines.append("\n## Next action\n- Replace `core/dvnc_engine.py` with your production graph and evidence stack.")
    return "\n".join(lines)


def build_frontend_payload(data):
    return f"""
    <script>
    window.__DVNC_GRAPH__ = {json.dumps(data.get('graph', {}))};
    </script>
    {CONNECTOME_SNIPPET}
    """


def run(query, model_name):
    data = run_discovery(query, model_name)
    return (
        build_models_html(model_name),
        build_chat_html(query, data),
        build_frontend_payload(data),
        build_reasoning_html(data.get("reasoning", [])),
        build_cards_html(data.get("cards", [])),
        build_metrics_md(data.get("metrics", {}), data.get("model_used", "unknown")),
    )

CSS = r'''
:root{--bg:#ffffff;--panel:#fafbfc;--panel2:#f5f6f8;--line:rgba(0,0,0,.08);--text:#0a0c12;--muted:#5a6372;--orange:#ff6b35;--orange-light:#ff8f66;--orange-pale:#fff4f0;--teal:#8ce7dc;--blue:#7ea6ff;--radius:24px;--shadow:0 8px 32px rgba(0,0,0,.06)}
html,body,.gradio-container{background:#ffffff!important;color:var(--text)!important;font-family:Inter,system-ui,sans-serif}
.gradio-container{max-width:1550px!important;padding:20px!important} footer{display:none!important}
#app-shell{border:1px solid var(--line);background:#fafbfc;box-shadow:var(--shadow);border-radius:30px;overflow:hidden}
#app-shell .grid{display:grid;grid-template-columns:1.04fr .96fr;min-height:88vh}.left,.right{padding:24px}.left{border-right:1px solid var(--line);display:flex;flex-direction:column;gap:18px}.right{display:grid;grid-template-rows:auto auto auto 1fr;gap:18px}
.hero{display:flex;justify-content:space-between;align-items:center;gap:12px}.brand{display:flex;gap:14px;align-items:center}.logo{width:46px;height:46px;border-radius:15px;display:grid;place-items:center;border:1px solid rgba(255,107,53,.2);background:linear-gradient(135deg,var(--orange-pale),rgba(255,107,53,.08))}.logo svg{width:25px;height:25px;color:var(--orange)}.brand h1{margin:0;font-size:1.08rem;color:var(--text)}.brand p{margin:3px 0 0;color:var(--muted);font-size:.86rem}.live{display:flex;gap:10px;align-items:center;color:var(--text)}.live i{width:10px;height:10px;border-radius:50%;background:var(--orange);display:inline-block;box-shadow:0 0 18px rgba(255,107,53,.4);animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.6;transform:scale(.9)}}
.panel{border:1px solid var(--line);background:#ffffff;border-radius:22px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.model-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.model-pill{padding:14px;border:1px solid var(--line);border-radius:18px;background:#fafbfc;display:flex;flex-direction:column;gap:4px;cursor:pointer;transition:all .2s}.model-pill:hover{border-color:var(--orange);transform:translateY(-1px)}.model-pill.active{border-color:var(--orange);background:var(--orange-pale)}.model-pill span{font-weight:650;color:var(--text)}.model-pill small{color:var(--muted)}
.querybox,.querybox>div{background:#ffffff!important;border:1px solid var(--line)!important;border-radius:18px!important}.querybox textarea{color:var(--text)!important}
.chat-panel{padding:18px;display:flex;flex-direction:column;gap:14px;min-height:360px}.bubble{max-width:86%;padding:16px 18px;border:1px solid var(--line);border-radius:22px}.bubble .role{font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:var(--muted)}.bubble p{margin:8px 0 0;line-height:1.6;color:var(--text)}.bubble.user{margin-left:auto;background:var(--orange-pale);border-color:rgba(255,107,53,.2)}.bubble.ai{background:#fafbfc}.bubble.system{background:var(--orange-pale);border-color:rgba(255,107,53,.2)}
.brain-shell{padding:18px}.brain-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;margin-bottom:12px}.eyebrow{margin:0 0 4px;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange)}.brain-head h3{margin:0;font-size:1.1rem;color:var(--text)}.brain-help{color:var(--muted);font-size:.8rem}#dvnc-three-root{height:400px;border-radius:20px;border:1px solid var(--line);overflow:hidden;background:#fafbfc;position:relative}
.working-orb{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;border-radius:50%;background:radial-gradient(circle at 30% 30%,rgba(255,143,102,.9),var(--orange));box-shadow:0 8px 32px rgba(255,107,53,.4),inset 0 -4px 12px rgba(0,0,0,.15);animation:orbPulse 2.5s ease-in-out infinite,orbFloat 4s ease-in-out infinite}
@keyframes orbPulse{0%,100%{box-shadow:0 8px 32px rgba(255,107,53,.4),inset 0 -4px 12px rgba(0,0,0,.15)}50%{box-shadow:0 12px 48px rgba(255,107,53,.7),inset 0 -4px 12px rgba(0,0,0,.2)}}
@keyframes orbFloat{0%,100%{transform:translate(-50%,-50%) translateY(0)}50%{transform:translate(-50%,-50%) translateY(-12px)}}
.tray-panel{padding:14px;display:flex;flex-direction:column;gap:10px}.tray{border:1px solid var(--line);border-radius:18px;background:#ffffff;overflow:hidden}.tray summary{list-style:none;display:grid;grid-template-columns:42px 1fr;gap:12px;align-items:center;padding:12px 14px;cursor:pointer}.tray summary::-webkit-details-marker{display:none}.tray .step{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;color:#ffffff;font-weight:700;background:var(--orange);border:1px solid var(--orange-light)}.tray summary strong{display:block;color:var(--text)}.tray summary small{color:var(--muted);text-transform:uppercase;letter-spacing:.12em}.tray-body{padding:0 14px 14px 68px;color:var(--text);line-height:1.6}
.cards-panel{padding:16px}.candidate-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.candidate-card{perspective:1200px;min-height:250px}.candidate-card-inner{position:relative;min-height:250px;height:100%;transform-style:preserve-3d;transition:transform .8s cubic-bezier(.2,.7,.1,1)}.candidate-card:hover .candidate-card-inner,.candidate-card:focus .candidate-card-inner{transform:rotateY(180deg)}.candidate-face{position:absolute;inset:0;padding:18px;border-radius:22px;border:1px solid var(--line);backface-visibility:hidden;display:flex;flex-direction:column;gap:12px;box-shadow:0 4px 16px rgba(0,0,0,.06);background:#ffffff}.candidate-face.back{transform:rotateY(180deg);background:var(--orange-pale)}.top,.meta{display:flex;justify-content:space-between;gap:12px}.chip{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);padding:7px 10px;border-radius:999px;border:1px solid rgba(255,107,53,.2);background:var(--orange-pale)}.chip.alt{color:var(--blue);border-color:rgba(37,99,235,.2);background:rgba(37,99,235,.08)}.score{font-weight:700;color:var(--orange)}.candidate-face h4{margin:0;color:var(--text)}.candidate-face p{margin:0;color:var(--text);line-height:1.6}.meta{margin-top:auto;color:var(--muted)}
.gr-button-primary{background:linear-gradient(135deg,var(--orange),var(--orange-light))!important;color:#ffffff!important;border:none!important;font-weight:600!important}.gr-button-secondary{background:#ffffff!important;color:var(--text)!important;border:1px solid var(--line)!important}
@media (max-width:1180px){#app-shell .grid{grid-template-columns:1fr}.left{border-right:0;border-bottom:1px solid var(--line)}.model-strip,.candidate-grid{grid-template-columns:1fr}}
'''

HEAD = '''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.156.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.156.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

function initDVNC(){
  const root = document.getElementById('dvnc-three-root');
  const graph = window.__DVNC_GRAPH__;
  if(!root || !graph || root.dataset.ready === '1') return;
  root.dataset.ready = '1';
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(52, root.clientWidth / root.clientHeight, 0.1, 1000);
  camera.position.set(0, 0, 120);
  const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
  renderer.setSize(root.clientWidth, root.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  root.innerHTML='';
  root.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.autoRotate = true;
  controls.autoRotateSpeed = .45;
  controls.enablePan = false;

  const ambient = new THREE.AmbientLight(0xffffff, .7); scene.add(ambient);
  const key = new THREE.PointLight(0xff6b35, 2.5, 260); key.position.set(30, 40, 50); scene.add(key);
  const fill = new THREE.PointLight(0xff8f66, 2.0, 240); fill.position.set(-40, -20, 40); scene.add(fill);
  
  const nodeMeshes = {};
  const active = new Set(graph.active_path || []);
  const palette = {core:0xff6b35, domain:0xff8f66, bridge:0xffa280, mechanism:0xffb399, outcome:0xffc2ad, candidate:0xff8f66};
  
  const nodeGeom = new THREE.SphereGeometry(1.8, 22, 22);
  const haloGeom = new THREE.SphereGeometry(3.4, 22, 22);

  for(const n of graph.nodes || []){
    const mat = new THREE.MeshStandardMaterial({ color: palette[n.group] || 0x9aa8c7, emissive: active.has(n.id) ? 0xff6b35 : 0x000000, emissiveIntensity: active.has(n.id) ? 1.2 : 0.15, roughness:.3, metalness:.15 });
    const mesh = new THREE.Mesh(nodeGeom, mat);
    mesh.position.set(n.x, n.y, n.z);
    scene.add(mesh);
    nodeMeshes[n.id] = mesh;
    if(active.has(n.id)){
      const halo = new THREE.Mesh(haloGeom, new THREE.MeshBasicMaterial({ color:0xff6b35, transparent:true, opacity:.08 }));      
      halo.position.copy(mesh.position);
      scene.add(halo);
      mesh.userData.halo = halo;
    }
  }

  function edgeActive(a,b){
    const path = graph.active_path || [];
    const ia = path.indexOf(a), ib = path.indexOf(b);
    return ia >= 0 && ib >= 0 && Math.abs(ia-ib) === 1;
  }

  for(const e of graph.edges || []){
    const [a,b] = e;
    if(!nodeMeshes[a] || !nodeMeshes[b]) continue;
    const pts = [nodeMeshes[a].position, nodeMeshes[b].position];
    const geo = new THREE.BufferGeometry().setFromPoints(pts);
    const mat = new THREE.LineBasicMaterial({ color: edgeActive(a,b) ? 0xff6b35 : 0xcccccc, transparent:true, opacity: edgeActive(a,b) ? 1 : .45 });    const line = new THREE.Line(geo, mat);
    line.userData.active = edgeActive(a,b);
    scene.add(line);
  }

  const stars = new THREE.Points(
    new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(Array.from({length:1200},()=> (Math.random()-.5)*220), 3)),
    new THREE.PointsMaterial({ color:0x8da6d8, size:.35, transparent:true, opacity:.6 })
  );
  scene.add(stars);

  const clock = new THREE.Clock();
  function animate(){
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    Object.values(nodeMeshes).forEach((m,i)=>{
      m.scale.setScalar(1 + Math.sin(t*1.6 + i)*0.03);
      if(m.userData.halo){
        const s = 1 + (Math.sin(t*2.2 + i)+1)*0.08;
        m.userData.halo.scale.setScalar(s);
      }
    });
    controls.update();
    renderer.render(scene,camera);
  }
  animate();

  const resize = ()=>{
    if(!root.clientWidth || !root.clientHeight) return;
    camera.aspect = root.clientWidth / root.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(root.clientWidth, root.clientHeight);
  };
  window.addEventListener('resize', resize, { passive:true });
}

new MutationObserver(()=>initDVNC()).observe(document.documentElement,{childList:true,subtree:true});
window.addEventListener('load', initDVNC);
setInterval(initDVNC, 1200);
</script>
'''

with gr.Blocks(css=CSS, head=HEAD, theme=gr.themes.Base(), fill_height=True) as demo:
    gr.HTML('''
    <div id="app-shell">
     <div class="hero">
      <div class="brand">
          <div class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 17L12 4l7 13"/><path d="M8.5 12.5h7"/><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/></svg></div>
          <div><h1>DVNC.AI</h1><p>Connectome-native reasoning · premium scientific discovery interface</p></div>
        </div>
        <div class="live"><i></i><span>Claude-linked runtime</span></div>
      </div>
    ''')
    model_view = gr.HTML(build_models_html("DVNC Sovereign"))
    model = gr.Dropdown(choices=MODELS, value="DVNC Sovereign", label="Model")
    query = gr.Textbox(label="Discovery query", lines=4, elem_classes=["querybox"], placeholder="Ask a scientific question, anomaly, mechanism, or hypothesis target…")
    with gr.Row():
        run_btn = gr.Button("Run discovery", variant="primary")
        example_btn = gr.Button("Load example", variant="secondary")
    chat = gr.HTML('<div class="chat-panel panel"><div class="bubble ai"><span class="role">DVNC</span><p>Enter a discovery prompt to trigger Claude-backed orchestration or demo mode if no API key is set.</p></div></div>')
    gr.HTML('</section><section class="right">')
    connectome = gr.HTML(CONNECTOME_SNIPPET)
    trays = gr.HTML('<div class="panel tray-panel"></div>')
    cards = gr.HTML('<div class="panel cards-panel"></div>')
    output = gr.Markdown('# Discovery Output\n\nAwaiting query.')
    gr.HTML('</section></div></div>')

    example_btn.click(lambda: "How could a self-assembling conductive biomaterial improve cardiac repair by converting mechanical strain into regenerative signalling?", outputs=query)
    run_btn.click(run, inputs=[query, model], outputs=[model_view, chat, connectome, trays, cards, output])

if __name__ == '__main__':
    demo.launch()
