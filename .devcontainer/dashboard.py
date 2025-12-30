"""
Rūpestėlio Ekosistemos Dashboard v1.1 – pataisyta, nebetuščias ekranas
"""
import streamlit as st
from datetime import datetime

try:
    from graph import create_agent_graph, AgentState
    from tools import get_available_tools
except ImportError as e:
    st.error(f"Import klaida: {e}")
    st.stop()

# CSS (tas pats)
st.markdown("""
<style>
/* ... visas Claude CSS ... */
</style>
""", unsafe_allow_html=True)

def init_session_state():
    defaults = {
        'graph': create_agent_graph(),
        'messages': [],
        'agent_outputs': {a: [] for a in ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]},
        'current_task': None,
        'task_history': [],
        'execution_stats': {'total_tasks': 0, 'successful_tasks': 0, 'failed_tasks': 0},
        'available_tools': get_available_tools(),
        'errors_log': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

AGENTS = { ... }  # tas pats

# Sidebar (tas pats)

# MAIN CONTENT – pridėtas default welcome, kad nebebūtų tuščias!
st.title("🎯 Rūpestėlio Ekosistemos Vadovo Centras")

if not st.session_state.current_task:
    st.markdown("""
    ### Sveiki atvykę į Rūpestėlio Ekosistemą! 🐾
    
    Tai multi-agent AI sistema, kuri padeda kurti ir tobulinti Rūpestėlis Vet AI.
    
    **Kaip naudotis:**
    1. Įveskite užduotį apačioje
    2. Pasirinkite agentus
    3. Spauskite "Vykdyti Užduotį"
    4. Stebėkite rezultatus tabs'ose
    
    **Pavyzdinė užduotis:** "Išanalizuok šunų niežulio simptomus ir pasiūlyk rekomendacijas"
    """)
    st.info("Sistema paruošta – įveskite pirmą užduotį!")

# Užduotis (tas pats kaip Claude)
with st.form("task_form"):
    # ... tas pats ...

if submitted and task_input:
    # ... tas pats execute blokas ...

# Tabs (tas pats)

st.caption("Rūpestėlis Ekosistema v1.1 | 2025 – pataisyta, visada rodo content'ą")
