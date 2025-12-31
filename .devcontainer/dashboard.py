"""
Rūpestėlio Ekosistemos Dashboard v1.0 – Startas su hibridu
CrewAI roles + LangGraph state (simuliacija pradžiai)
"""
import streamlit as st
from datetime import datetime

# Session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent_outputs' not in st.session_state:
    st.session_state.agent_outputs = {
        "testuotojas": [],
        "vet_ekspertas": [],
        "kodo_fixer": [],
        "image_analyzer": [],
        "monetizacijos_strategas": []
    }

# Gražus UI
st.set_page_config(page_title="Rūpestėlio Ekosistema", page_icon="🐾", layout="wide")
st.title("🐾 Rūpestėlio Ekosistemos Vadovo Centras")
st.markdown("**Multi-Agent AI Sistema – hibridas CrewAI + LangGraph**")

# Agentai
AGENTS = {
    "testuotojas": "🧪 Testuotojas – tikrina kodą ir testus",
    "vet_ekspertas": "🏥 Vet Ekspertas – medicininis tikslumas",
    "kodo_fixer": "🔧 Kodo Fixer'is – taiso klaidas",
    "image_analyzer": "📸 Image Analyzer – vaizdų analizė",
    "monetizacijos_strategas": "💰 Monetizacija – pelno planai"
}

# Sidebar
with st.sidebar:
    st.header("Agentai")
    for desc in AGENTS.values():
        st.write(desc)
    st.divider()
    st.caption("v1.0 | CrewAI + LangGraph hibridas")

# Užduotis
with st.form("task_form"):
    task = st.text_area("Užduotis agentams", height=120, placeholder="Pvz.: Išanalizuok šunų niežulį ir pataisyk kodą")
    selected = st.multiselect("Agentai", options=list(AGENTS.keys()), default=list(AGENTS.keys()))
    go = st.form_submit_button("Vykdyti užduotį")

if go and task:
    with st.spinner("Agentai dirba..."):
        # Simuliacija (realiam LangGraph invoke)
        for agent in selected:
            response = f"{AGENTS[agent]} gavo užduotį:\n{task}\n\n**Atsakymas:** Simuliuotas – viskas veikia! (Realus graph'as kitame žingsnyje)"
            st.session_state.agent_outputs[agent].append({"time": datetime.now().strftime("%H:%M"), "response": response})
        st.success("Užduotis įvykdyta!")
        st.rerun()

# Tabs su agentais
tabs = st.tabs(list(AGENTS.values()))
for i, agent in enumerate(AGENTS.keys()):
    with tabs[i]:
        outputs = st.session_state.agent_outputs[agent]
        if outputs:
            for out in reversed(outputs):
                st.markdown(f"**{out['time']}**")
                st.write(out["response"])
                st.divider()
        else:
            st.info("Dar nėra atsakymų – įvesk užduotį!")

st.caption("Rūpestėlis Ekosistema | Startas sėkmingas – einam toliau!")
