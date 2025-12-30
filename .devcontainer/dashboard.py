"""
Rūpestėlio Ekosistemos Dashboard v1.2 – Indentation pataisyta + stabilus
"""
import streamlit as st
from datetime import datetime

# Importai
try:
    from graph import create_agent_graph, AgentState
    from tools import get_available_tools
except ImportError as e:
    st.error(f"Import klaida: {e}. Patikrink, ar graph.py ir tools.py yra kataloge.")
    st.stop()

# CSS (tas pats gražus)
st.markdown("""
<style>
    /* ... visas Claude CSS kodas ... */
</style>
""", unsafe_allow_html=True)

# Session state
def init_session_state():
    defaults = {
        'graph': create_agent_graph(),
        'messages': [],
        'agent_outputs': {a: [] for a in ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]},
        'current_task': None,
        'task_history': [],
        'execution_stats': {'total_tasks': 0, 'successful_tasks': 0, 'failed_tasks': 0, 'total_execution_time': 0},
        'available_tools': get_available_tools(),
        'errors_log': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# Agentai (tas pats)
AGENTS = { ... }  # kopijuok iš Claude

# Sidebar (tas pats)
with st.sidebar:
    st.title("🐾 Rūpestėlio Ekosistema")
    # ... statistika, tools, reset ...

# Main
st.title("🎯 Vadovo Komandų Centras")

# Užduotis – teisinga indentacija!
with st.form("task_form"):
    task_input = st.text_area("Užduotis agentams", height=120)
    selected_agents = st.multiselect("Agentai", options=list(AGENTS.keys()), default=list(AGENTS.keys()))
    use_tools = st.checkbox("Naudoti tools", value=True)
    submitted = st.form_submit_button("Vykdyti")

# Teisinga indentacija – visas if blokas po with!
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

# Tabs (tas pats)
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

st.caption("Rūpestėlis Ekosistema v1.2 | LangGraph + Streamlit – klaidos pataisytos")
