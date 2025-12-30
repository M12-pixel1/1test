"""
Rūpestėlio Ekosistemos Dashboard v1.0
Streamlit + LangGraph multi-agent sistema
"""
import streamlit as st
import numpy as np
from PIL import Image
import io
from datetime import datetime

# Lazy tools import
def load_tools():
    try:
        from tools import get_available_tools
        return get_available_tools()
    except:
        return ["view_image", "web_search", "code_execution"]  # fallback

# Graph import
try:
    from graph import create_agent_graph, AgentState
except ImportError as e:
    st.error(f"Import klaida: {e}. Įsitikinkite, kad graph.py ir tools.py yra kataloge.")
    st.stop()

# CSS stilius (Claude originalas + pataisytas)
st.markdown("""
<style>
    .agent-card { padding: 1.5rem; border-radius: 0.8rem; border: 2px solid #e1e8ed; margin: 0.8rem 0; background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; }
    .agent-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); transform: translateY(-2px); }
    .status-active { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-color: #28a745; }
    .status-idle { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    .status-working { background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-color: #ffc107; animation: pulse 2s infinite; }
    .status-error { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-color: #dc3545; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
    .task-header { font-size: 1.3rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem; }
    .metric-card { background: white; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #3498db; margin: 0.5rem 0; }
    .tool-badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 1rem; background: #e3f2fd; color: #1976d2; font-size: 0.85rem; margin: 0.2rem; font-weight: 600; }
    .success-banner { background: linear-gradient(90deg, #28a745 0%, #20c997 100%); color: white; padding: 1rem; border-radius: 0.5rem; font-weight: 600; text-align: center; }
    .error-banner { background: linear-gradient(90deg, #dc3545 0%, #c82333 100%); color: white; padding: 1rem; border-radius: 0.5rem; font-weight: 600; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 12px 24px; background: #f8f9fa; border-radius: 8px 8px 0 0; font-weight: 600; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white !important; }
</style>
""", unsafe_allow_html=True)

# Session state
def init_session_state():
    defaults = {
        'graph': create_agent_graph(),
        'messages': [],
        'agent_outputs': {agent: [] for agent in ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]},
        'current_task': None,
        'task_history': [],
        'execution_stats': {'total_tasks': 0, 'successful_tasks': 0, 'failed_tasks': 0, 'total_execution_time': 0},
        'available_tools': load_tools(),
        'tool_usage_count': {},
        'errors_log': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Agentai
AGENTS = {
    "testuotojas": {"name": "🧪 Testuotojas", "role": "QA Inžinierius", "description": "Testuoja kodą ir funkcionalumą", "color": "#3498db", "tools": ["code_execution"]},
    "vet_ekspertas": {"name": "🏥 Vet Ekspertas", "role": "Veterinarijos Specialistas", "description": "Konsultuoja sveikatą", "color": "#2ecc71", "tools": ["web_search"]},
    "kodo_fixer": {"name": "🔧 Kodo Fixer'is", "role": "Bug Taisymas", "description": "Taiso klaidas", "color": "#e74c3c", "tools": ["code_execution"]},
    "image_analyzer": {"name": "📸 Image Analyzer", "role": "Vaizdų Analizė", "description": "Atpažįsta simptomus vaizduose", "color": "#9b59b6", "tools": ["view_image"]},
    "monetizacijos_strategas": {"name": "💰 Monetizacija", "role": "Verslo Strategas", "description": "Planuoja pelną", "color": "#f39c12", "tools": ["web_search"]}
}

# Sidebar
with st.sidebar:
    st.title("🐾 Rūpestėlio Ekosistema")
    st.markdown("### Multi-Agent Sistema")
    
    # Statistika
    st.metric("Užduotys", st.session_state.execution_stats['total_tasks'])
    st.metric("Sėkmingos", st.session_state.execution_stats['successful_tasks'])
    
    # Tools
    st.markdown("### 🛠️ Tools")
    for tool in st.session_state.available_tools:
        st.markdown(f"<span class='tool-badge'>{tool}</span>", unsafe_allow_html=True)
    
    # Reset
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

# Main
st.title("🎯 Vadovo Komandų Centras")

# Užduotis
with st.form("task_form"):
    task_input = st.text_area("Užduotis agentams", height=120)
    selected_agents = st.multiselect("Agentai", options=list(AGENTS.keys()), default=list(AGENTS.keys()))
    use_tools = st.checkbox("Naudoti tools", value=True)
    submitted = st.form_submit_button("Vykdyti")

if submitted and task_input:
    with st.spinner("Agentai dirba..."):
        initial_state = AgentState(
            task=task_input,
            messages=[],
            selected_agents=selected_agents,
            use_tools=use_tools
        )
        try:
            final_state = st.session_state.graph.invoke(initial_state)
            st.success("Užduotis įvykdyta!")
            st.rerun()
        except Exception as e:
            st.error(f"Klaida: {e}")

# Tabs
tabs = st.tabs([info['name'] for info in AGENTS.values()])
for i, (agent_id, info) in enumerate(AGENTS.items()):
    with tabs[i]:
        st.markdown(f"#### {info['name']}")
        st.caption(info['description'])
        if st.session_state.agent_outputs[agent_id]:
            for item in reversed(st.session_state.agent_outputs[agent_id][-5:]):
                st.write(item['output'])
        else:
            st.info("Dar nėra atsakymų")

st.caption("Rūpestėlis Ekosistema v1.0 | LangGraph + Streamlit")
