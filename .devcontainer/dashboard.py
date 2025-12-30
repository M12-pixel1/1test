"""
Rūpestėlio Ekosistemos Dashboard v1.0
"""
import streamlit as st
from datetime import datetime

# Importai iš vietinių failų
try:
    from graph import create_agent_graph, AgentState
    from tools import get_available_tools
except ImportError as e:
    st.error(f"❌ Klaida importuojant graph.py arba tools.py: {e}")
    st.info("Įsitikinkite, kad visi 3 failai yra tame pačiame kataloge")
    st.stop()

# CSS (tas pats gražus dizainas kaip Claude)
st.markdown("""
<style>
    /* ... visas Claude CSS kodas iš tavo žinutės ... */
</style>
""", unsafe_allow_html=True)

# Session state inicializacija
def init_session_state():
    defaults = {
        'graph': create_agent_graph(),
        'messages': [],
        'agent_outputs': {a: [] for a in ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]},
        'current_task': None,
        'task_history': [],
        'execution_stats': {'total_tasks': 0, 'successful_tasks': 0, 'failed_tasks': 0, 'total_execution_time': 0},
        'available_tools': get_available_tools(),
        'tool_usage_count': {},
        'errors_log': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# Agentų aprašymai (tas pats kaip Claude)
AGENTS = { ... }  # kopijuok iš Claude kodo

# Sidebar (tas pats kaip Claude)
with st.sidebar:
    st.title("🐾 Rūpestėlio Ekosistema")
    # ... statistika, tools, reset ...

# Pagrindinis turinys (tas pats kaip Claude – užduoties įvedimas, execute ir tabs)
# ... visas Claude kodas nuo st.title("🎯 Vadovo Komandų Centras") iki pabaigos ...

st.caption("Rūpestėlis Ekosistema v1.0 | LangGraph + Streamlit")
