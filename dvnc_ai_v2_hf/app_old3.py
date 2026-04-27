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
        checked = "checked" if name == selected else ""
        safe_id = name.lower().replace(" ", "-")
        out.append(f'''
        <label class="model-pill {active}" for="{safe_id}">
          <input type="radio" name="dvnc-model-card" value="{name}" id="{safe_id}" {checked}>
          <span>{name}</span>
          <small>{desc}</small>
        </label>
        ''')
        script = '''<script>
    document.addEventListener('DOMContentLoaded', function() {
        const radios = document.querySelectorAll('input[name="dvnc-model-card"]');
        radios.forEach(radio => {
            radio.addEventListener('change', function() {
                const dropdown = document.querySelector('select[aria-label="Model"]');
                if (dropdown && this.checked) {
                    dropdown.value = this.value;
                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        });
    });
    </script>'''
    return '<div class="model-strip">' + ''.join(out) + '</div>' + script


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
:root{--bg:#fffaf7;--panel:#ffffff;--panel2:#fff6f1;--line:rgba(17,24,39,.08);--text:#000;--muted:#5f6675;--orange:#ff6b35;--orange-light:#ff955f;--orange-pale:#fff3ec;--teal:#b9efe8;--blue:#8fb2ff;--radius:24px;--shadow:0 16px 44px rgba(17,24,39,.06)}
html,body,.gradio-container{background:linear-gradient(180deg,#fffaf7 0%,#fff 100%)!important;color:var(--text)!important;font-family:Inter,system-ui,sans-serif}
.gradio-container{max-width:1480px!important;padding:18px!important} footer{display:none!important}
#app-shell{border:1px solid var(--line);background:rgba(255,255,255,.92);backdrop-filter:blur(14px);box-shadow:var(--shadow);border-radius:32px;overflow:hidden}
#app-shell .grid{display:grid;grid-template-columns:1.08fr .92fr;min-height:72vh}.left,.right{padding:20px}.left{border-right:1px solid var(--line);display:flex;flex-direction:column;gap:14px}.right{display:grid;grid-template-rows:auto auto auto 1fr;gap:14px}
.hero{display:flex;justify-content:space-between;align-items:center;gap:12px}
.hero-plate{padding:22px 24px 18px 24px;min-height:160px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,rgba(255,255,255,.92) 0%,rgba(255,247,243,.88) 100%)}
.hero-copy{display:flex;flex-direction:column;justify-content:space-between;gap:16px;min-height:118px}
.brand{display:flex;gap:14px;align-items:center}
.logo{width:50px;height:50px;border-radius:16px;display:grid;place-items:center;border:1px solid rgba(255,107,53,.2);background:linear-gradient(135deg,var(--orange-pale),rgba(255,107,53,.08))}
.logo svg{width:26px;height:26px;color:var(--orange)}
.brand h1{margin:0;font-size:1.18rem;color:var(--text)}
.brand p{margin:4px 0 0;color:var(--muted);font-size:.9rem}
.live{display:flex;gap:10px;align-items:center;color:var(--text)}
.live i{width:10px;height:10px;border-radius:50%;background:var(--orange);display:inline-block;box-shadow:0 0 18px rgba(255,107,53,.4);animation:pulse 2s ease-in-out infinite}
.hero-orb-wrap{margin-left:auto;display:flex;align-items:center;justify-content:center;min-width:180px}
.hero-orb{position:relative;width:110px;height:110px;display:grid;place-items:center}
.hero-orb-core{width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 30% 28%,#ffd2be 0%,#ff9a6f 30%,#ff6b35 68%,#d94d1c 100%);box-shadow:0 12px 34px rgba(255,107,53,.28), inset -8px -10px 18px rgba(100,35,10,.22), inset 8px 10px 16px rgba(255,255,255,.22);animation:heroOrbFloat 5s ease-in-out infinite}
.hero-orb-ring{position:absolute;border-radius:50%;border:1px solid rgba(255,107,53,.16)}
.hero-orb-ring.ring-a{width:86px;height:86px;animation:spinSlow 10s linear infinite}
.hero-orb-ring.ring-b{width:108px;height:108px;border-color:rgba(255,107,53,.10);animation:spinReverse 14s linear infinite}
.hero-orb-glow{position:absolute;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,rgba(255,107,53,.18) 0%,rgba(255,107,53,.08) 42%,rgba(255,107,53,0) 72%)}
@keyframes heroOrbFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-5px) scale(1.03)}}
@keyframes spinSlow{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes spinReverse{from{transform:rotate(360deg)}to{transform:rotate(0deg)}}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.6;transform:scale(.9)}}
.panel{border:1px solid var(--line);background:#ffffff;border-radius:22px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.model-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.model-pill{position:relative;padding:0;border:1px solid var(--line);border-radius:18px;background:#fafbfc;display:flex;flex-direction:column;cursor:pointer;transition:all .22s ease;overflow:hidden}
.model-pill input{position:absolute;opacity:0;pointer-events:none}
.model-pill span,.model-pill small{display:block;padding:0 14px}
.model-pill span{padding-top:14px;font-weight:650;color:var(--text)}
.model-pill small{padding-bottom:14px;color:var(--muted)}
.model-pill:hover{border-color:var(--orange);transform:translateY(-2px);box-shadow:0 12px 24px rgba(255,107,53,.08)}
.model-pill.active{border-color:var(--orange);background:linear-gradient(180deg,#fff 0%,var(--orange-pale) 100%);box-shadow:0 10px 26px rgba(255,107,53,.10)}
.model-pill.active span{color:#111}
.querybox,.querybox>div{background:#fff!important;border:1.5px solid rgba(255,107,53,.28)!important;border-radius:20px!important;box-shadow:0 6px 22px rgba(255,107,53,.08)!important}.querybox textarea{color:#000!important;background:#fff!important}.querybox:focus-within,.querybox>div:focus-within{border-color:#ff6b35!important;box-shadow:0 0 0 4px rgba(255,107,53,.10),0 8px 28px rgba(255,107,53,.10)!important}
.chat-panel{padding:14px;display:flex;flex-direction:column;gap:10px;min-height:240px;max-height:300px;overflow:auto}.bubble{max-width:86%;padding:14px 16px;border:1px solid var(--line);border-radius:20px}.bubble .role{font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:var(--muted)}.bubble p{margin:6px 0 0;line-height:1.55;color:var(--text)}.bubble.user{margin-left:auto;background:var(--orange-pale);border-color:rgba(255,107,53,.22)}.bubble.ai{background:#fff}.bubble.system{background:var(--orange-pale);border-color:rgba(255,107,53,.22)}
.brain-shell{padding:14px}.brain-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;margin-bottom:10px}.eyebrow{margin:0 0 4px;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange)}.brain-head h3{margin:0;font-size:1.02rem;color:var(--text)}.brain-help{color:var(--muted);font-size:.8rem}#dvnc-three-root{height:300px;border-radius:20px;border:1px solid var(--line);overflow:hidden;background:linear-gradient(180deg,#fff7f3 0%,#fff 100%);position:relative}
.working-orb{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;border-radius:50%;background:radial-gradient(circle at 30% 30%,rgba(255,143,102,.9),var(--orange));box-shadow:0 8px 32px rgba(255,107,53,.4),inset 0 -4px 12px rgba(0,0,0,.15);animation:orbPulse 2.5s ease-in-out infinite,orbFloat 4s ease-in-out infinite}
@keyframes orbPulse{0%,100%{box-shadow:0 8px 32px rgba(255,107,53,.4),inset 0 -4px 12px rgba(0,0,0,.15)}50%{box-shadow:0 12px 48px rgba(255,107,53,.7),inset 0 -4px 12px rgba(0,0,0,.2)}}
@keyframes orbFloat{0%,100%{transform:translate(-50%,-50%) translateY(0)}50%{transform:translate(-50%,-50%) translateY(-12px)}}
.tray-panel{padding:14px;display:flex;flex-direction:column;gap:10px}.tray{border:1px solid var(--line);border-radius:18px;background:#ffffff;overflow:hidden}.tray summary{list-style:none;display:grid;grid-template-columns:42px 1fr;gap:12px;align-items:center;padding:12px 14px;cursor:pointer}.tray summary::-webkit-details-marker{display:none}.tray .step{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;color:#ffffff;font-weight:700;background:var(--orange);border:1px solid var(--orange-light)}.tray summary strong{display:block;color:var(--text)}.tray summary small{color:var(--muted);text-transform:uppercase;letter-spacing:.12em}.tray-body{padding:0 14px 14px 68px;color:var(--text);line-height:1.6}
.cards-panel{padding:16px}.candidate-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.candidate-card{perspective:1200px;min-height:250px}.candidate-card-inner{position:relative;min-height:250px;height:100%;transform-style:preserve-3d;transition:transform .8s cubic-bezier(.2,.7,.1,1)}.candidate-card:hover .candidate-card-inner,.candidate-card:focus .candidate-card-inner{transform:rotateY(180deg)}.candidate-face{position:absolute;inset:0;padding:18px;border-radius:22px;border:1px solid var(--line);backface-visibility:hidden;display:flex;flex-direction:column;gap:12px;box-shadow:0 4px 16px rgba(0,0,0,.06);background:#ffffff}.candidate-face.back{transform:rotateY(180deg);background:var(--orange-pale)}.top,.meta{display:flex;justify-content:space-between;gap:12px}.chip{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);padding:7px 10px;border-radius:999px;border:1px solid rgba(255,107,53,.2);background:var(--orange-pale)}.chip.alt{color:var(--blue);border-color:rgba(37,99,235,.2);background:rgba(37,99,235,.08)}.score{font-weight:700;color:var(--orange)}.candidate-face h4{margin:0;color:var(--text)}.candidate-face p{margin:0;color:var(--text);line-height:1.6}.meta{margin-top:auto;color:var(--muted)}
.gr-button-primary{background:linear-gradient(135deg,var(--orange),var(--orange-light))!important;color:#fff!important;border:none!important;font-weight:700!important;box-shadow:0 10px 24px rgba(255,107,53,.22)!important}.gr-button-secondary{background:#fff!important;color:#000!important;border:1px solid rgba(255,107,53,.18)!important}
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

function syncModelCards(){
  const root = document;
  const dropdown = root.querySelector('#real-model-select select, #real-model-select input, #real-model-select textarea');
  const radios = root.querySelectorAll('input[name="dvnc-model-card"]');
  if(!dropdown || !radios.length) return;

  radios.forEach(radio => {
    if(radio.dataset.bound === '1') return;
    radio.dataset.bound = '1';
    radio.addEventListener('change', () => {
      const next = radio.value;

      const select = root.querySelector('#real-model-select select');
      if(select){
        select.value = next;
        select.dispatchEvent(new Event('input', { bubbles:true }));
        select.dispatchEvent(new Event('change', { bubbles:true }));
      }

      root.querySelectorAll('.model-pill').forEach(card => card.classList.remove('active'));
      radio.closest('.model-pill')?.classList.add('active');
    });
  });
}

new MutationObserver(()=>{initDVNC(); syncModelCards();}).observe(document.documentElement,{childList:true,subtree:true});
window.addEventListener('load', ()=>{initDVNC(); syncModelCards();});
setInterval(()=>{initDVNC(); syncModelCards();}, 1200);
</script>
'''

with gr.Blocks(css=CSS, head=HEAD, theme=gr.themes.Base(), fill_height=True) as demo:
    gr.HTML('''
    <div id="app-shell">
      <div class="hero hero-plate">
        <div class="hero-copy">
          <div class="brand">
            <div class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 17L12 4l7 13"/><path d="M8.5 12.5h7"/><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/></svg></div>
            <div>
              <h1>DVNC.AI</h1>
              <p>Connectome-native reasoning · premium scientific discovery interface</p>
            </div>
          </div>
          <div class="live"><i></i><span>Claude-linked runtime</span></div>
        </div>
        <div class="hero-orb-wrap">
          <div class="hero-orb">
            <div class="hero-orb-core"></div>
            <div class="hero-orb-ring ring-a"></div>
            <div class="hero-orb-ring ring-b"></div>
            <div class="hero-orb-glow"></div>
          </div>
        </div>
      </div>
    ''')
    model_view = gr.HTML(build_models_html("DVNC Sovereign"))
    model = gr.Dropdown(
        choices=MODELS,
        value="DVNC Sovereign",
        label="Model",
        elem_id="real-model-select",
        visible=False
    )
    query = gr.Textbox(label="Discovery query", lines=3, elem_classes=["querybox"], placeholder="Ask a scientific question, anomaly, mechanism, or hypothesis target…")
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