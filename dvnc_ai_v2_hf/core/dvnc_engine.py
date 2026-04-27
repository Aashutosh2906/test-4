import os
import json
from anthropic import Anthropic

DEFAULT_MODEL = "claude-opus-4-7"
MODEL_MAP = {
    "DVNC Sovereign": "claude-opus-4-7",
    "DVNC Atlas": "claude-sonnet-4-5",
    "DVNC Curie": "claude-sonnet-4-5",
}

SYSTEM_PROMPT = """
You are DVNC.AI, a connectome-native scientific discovery engine.
Think in seven explicit phases:
1. interpret the question
2. locate anomalous tension
3. surface distant graph bridges
4. produce evidence-aware analogies
5. compose a primary hypothesis and alternatives
6. critique assumptions adversarially
7. output an experiment programme
Respond in strict JSON.
""".strip()

DEMO_GRAPH = {
    "nodes": [
        {"id": "seed", "label": "Seed Query", "group": "core", "x": 0, "y": 0, "z": 0},
        {"id": "bio", "label": "Biomaterials", "group": "domain", "x": 14, "y": 10, "z": -6},
        {"id": "nano", "label": "Nanostructure", "group": "bridge", "x": 14, "y": -14, "z": 11},
        {"id": "selfasm", "label": "Self-Assembly", "group": "bridge", "x": 30, "y": -8, "z": -10},
        {"id": "electro", "label": "Electro-signalling", "group": "mechanism", "x": 45, "y": 8, "z": -10},
        {"id": "immune", "label": "Immune Modulation", "group": "mechanism", "x": 46, "y": -9, "z": 8},
        {"id": "trial", "label": "Validation", "group": "outcome", "x": 62, "y": 0, "z": 0},
        {"id": "alt1", "label": "Piezoelectric Scaffold", "group": "candidate", "x": 38, "y": 24, "z": 10},
        {"id": "alt2", "label": "Peptide Mesh", "group": "candidate", "x": 35, "y": -24, "z": -10}
    ],
    "edges": [
        ["seed","bio"],["seed","nano"],["bio","immune"],["nano","selfasm"],["selfasm","electro"],["electro","trial"],["immune","trial"],["electro","alt1"],["selfasm","alt2"],["alt1","trial"],["alt2","trial"]
    ],
    "active_path": ["seed","nano","selfasm","electro","trial"]
}

DEMO_REASONING = [
    {"step":1,"agent":"Query Interpreter","tag":"input","summary":"Normalises the seed query and extracts the anomaly that makes discovery worthwhile."},
    {"step":2,"agent":"Graph Divergence Mapper","tag":"graph","summary":"Moves away from nearest-neighbour concepts and surfaces distant but mechanistically relevant bridges."},
    {"step":3,"agent":"Evidence Harvester","tag":"evidence","summary":"Collects evidence packets, counter-signals, and high-uncertainty zones."},
    {"step":4,"agent":"Analogy Engine","tag":"analogy","summary":"Builds mechanism-level analogies instead of stylistic or keyword analogies."},
    {"step":5,"agent":"Hypothesis Composer","tag":"compose","summary":"Creates a lead hypothesis plus alternative discovery cards that can be swapped into the route."},
    {"step":6,"agent":"Adversarial Critic","tag":"critique","summary":"Attacks assumptions, feasibility, safety, and hidden confounders."},
    {"step":7,"agent":"Experimental Program Designer","tag":"experiment","summary":"Produces a staged validation programme with falsification criteria."}
]

DEMO_CARDS = [
    {
        "title": "Piezoelectric Scaffold Cascade",
        "front": "Convert cardiac motion into local repair signalling through a piezoelectric scaffold.",
        "back": "Alternative route: anomaly -> mechanoelectric transfer -> ion-channel entrainment -> repair response.",
        "score": 92,
        "novelty": "High",
        "agent": "Hypothesis Composer"
    },
    {
        "title": "Peptide Self-Assembly Mesh",
        "front": "Create a peptide mesh that self-assembles at the injury interface and choreographs local repair.",
        "back": "Alternative route: self-assembly -> immune choreography -> regenerative substrate formation.",
        "score": 88,
        "novelty": "High",
        "agent": "Analogy Engine"
    },
    {
        "title": "Immune-Tuned Conductive Hydrogel",
        "front": "Balance conductivity and macrophage-state modulation to reduce scarring while restoring conduction.",
        "back": "Alternative route: inflammation mismatch -> conductive medium -> synchronized healing.",
        "score": 85,
        "novelty": "Medium-High",
        "agent": "Adversarial Critic"
    }
]


def _demo_response(query, model_name):
    return {
        "summary": "DVNC.AI selected a deeper discovery route through the graph and preserved alternative branches as swap-ready candidate cards.",
        "primary_hypothesis": "Use a self-assembling conductive scaffold that transforms mechanical strain into regenerative signalling.",
        "graph": DEMO_GRAPH,
        "reasoning": DEMO_REASONING,
        "cards": DEMO_CARDS,
        "metrics": {
            "Novelty": 93,
            "Mechanistic clarity": 89,
            "Experimental tractability": 82,
            "Cross-domain distance": 91
        },
        "model_used": MODEL_MAP.get(model_name, DEFAULT_MODEL),
        "query": query,
    }


def _extract_text(resp):
    parts = []
    for item in resp.content:
        if getattr(item, "type", None) == "text":
            parts.append(item.text)
    return "\n".join(parts).strip()


def _call_claude(query, model_name):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _demo_response(query, model_name)
    client = Anthropic(api_key=api_key)
    schema_hint = {
        "summary": "string",
        "primary_hypothesis": "string",
        "graph": {"nodes": [{"id":"string","label":"string","group":"string","x":0,"y":0,"z":0}], "edges": [["a","b"]], "active_path": ["id"]},
        "reasoning": [{"step":1,"agent":"string","tag":"string","summary":"string"}],
        "cards": [{"title":"string","front":"string","back":"string","score":0,"novelty":"string","agent":"string"}],
        "metrics": {"Novelty":0,"Mechanistic clarity":0,"Experimental tractability":0,"Cross-domain distance":0}
    }
    prompt = f"User query: {query}\n\nReturn valid JSON matching this schema exactly: {json.dumps(schema_hint)}"
    response = client.messages.create(
        model=MODEL_MAP.get(model_name, DEFAULT_MODEL),
        max_tokens=1800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    text = _extract_text(response)
    try:
        data = json.loads(text)
    except Exception:
        data = _demo_response(query, model_name)
        data["summary"] = text[:600] if text else data["summary"]
    data["model_used"] = MODEL_MAP.get(model_name, DEFAULT_MODEL)
    data["query"] = query
    return data


def run_discovery(query, model_name):
    return _call_claude(query, model_name)
