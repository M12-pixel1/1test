"""
Rūpestėlio Ekosistemos Dashboard v1.5 – Pilnai veikiantis su multimodal ir garso analize
Claude kodas + mano pataisymai ir integracijos
"""
import streamlit as st
import numpy as np
from PIL import Image
import io
from datetime import datetime
import time
import json
import requests
import base64

# Librosa su fallback (jei nepavyksta įsidiegti)
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    st.caption("ℹ️ Librosa neįdiegta – garso analizė simuliuojama")

st.set_page_config(
    page_title="Rūpestėlio Ekosistema",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gražus CSS (Claude originalas)
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
    .tool-badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 1rem; background: #e3f2fd; color: #1976d2; font-size: 0.85rem; margin: 0.2rem; font-weight: 600; }
    .success-banner { background: linear-gradient(90deg, #28a745 0%, #20c997 100%); color: white; padding: 1rem; border-radius: 0.5rem; font-weight: 600; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ==================== TOOLS (su multimodal ir garso) ====================
class ToolsManager:
    @staticmethod
    def view_image(image_bytes: bytes, prompt: str = "Aprašyk gyvūno simptomus lietuviškai") -> str:
        try:
            api_key = st.secrets.get("grok_api_key")
            if api_key:
                url = "https://api.x.ai/v1/chat/completions"
                img_base64 = base64.b64encode(image_bytes).decode()
                payload = {
                    "model": "grok-beta",
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                        ]
                    }]
                }
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
            # Fallback
            return """
**Multimodalinė analizė (simuliacija):**
- Aptiktas gyvūnas
- Matomas paraudimas arba patinimas
- Rekomendacija: konsultacija su veterinaru
            """
        except Exception as e:
            return f"Vaizdų analizės klaida: {str(e)}"

    @staticmethod
    def audio_analysis(audio_bytes: bytes) -> str:
        if not LIBROSA_AVAILABLE:
            return """
**Garso analizė (librosa neįdiegta):**
- Simuliacija: aptiktas kosulys
- Rekomendacija: konsultacija su veterinaru
            """
        try:
            y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
            zcr = np.mean(librosa.feature.zero_crossing_rate(y))
            energy = np.mean(librosa.feature.rms(y=y))
            spectral = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            
            diagnosis = "Normalus kvėpavimas"
            if zcr > 0.1 and energy > 0.05:
                diagnosis = "Galimas kosulys arba švokštimas"
            elif spectral > 2500:
                diagnosis = "Aukšti dažniai – galimas cypimas"
            
            return f"""
**Garso analizė:**
- Trukmė: {len(y)/sr:.1f}s
- Energija: {energy:.4f}
- ZCR: {zcr:.3f}
- Spektrinis centras: {spectral:.0f} Hz
**Diagnozė:** {diagnosis}
            """
        except Exception as e:
            return f"Garso analizės klaida: {str(e)}"

    @staticmethod
    def web_search(query: str) -> str:
        return f"Paieška '{query}' – rasta info apie simptomus (simuliacija)"

    @staticmethod
    def code_execution(code: str) -> str:
        return f"Kodas įvykdytas: {code[:50]}... (simuliacija)"

tools = ToolsManager()

# ==================== SESSION STATE ====================
def initialize_session_state():
    defaults = {
        'messages': [],
        'agent_outputs': {a: [] for a in ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]},
        'task_history': [],
        'tools_used': [],
        'total_tasks': 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

initialize_session_state()

# ==================== AGENTAI ====================
AGENTS = {
    "testuotojas": {"name": "🧪 Testuotojas", "description": "Tikrina kodą ir testus"},
    "vet_ekspertas": {"name": "🏥 Vet Ekspertas", "description": "Medicininis tikslumas"},
    "kodo_fixer": {"name": "🔧 Kodo Fixer'is", "description": "Taiso klaidas"},
    "image_analyzer": {"name": "📸 Image Analyzer", "description": "Multimodalinė vaizdų analizė"},
    "monetizacijos_strategas": {"name": "💰 Monetizacija", "description": "Pelno strategijos"}
}

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("🤖 Agentų Sistema")
    for agent_id, agent_data in AGENTS.items():
        with st.expander(agent_data["name"]):
            st.write(agent_data["description"])
            st.caption(f"Užduotys: {len(st.session_state.agent_outputs.get(agent_id, []))}")
    st.divider()
    st.markdown("### 🛠️ Tools")
    st.markdown("<span class='tool-badge'>view_image</span><span class='tool-badge'>audio_analysis</span><span class='tool-badge'>web_search</span>", unsafe_allow_html=True)
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

# ==================== MAIN ====================
st.title("🎯 Vadovo Komandų Centras")

# Failų įkėlimas
col1, col2 = st.columns(2)
with col1:
    uploaded_image = st.file_uploader("Foto (multimodalinei analizei)", type=["jpg","jpeg","png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Įkeltas foto", use_column_width=True)

with col2:
    uploaded_audio = st.file_uploader("Garso įrašas (kosuliui/kvėpavimui)", type=["wav","mp3"])
    if uploaded_audio:
        st.audio(uploaded_audio)

st.divider()

# Užduotis
with st.form("task_form"):
    task_input = st.text_area("Užduotis agentams", height=120)
    selected_agents = st.multiselect("Agentai", options=list(AGENTS.keys()), default=list(AGENTS.keys()))
    submitted = st.form_submit_button("Vykdyti užduotį")

if submitted and task_input:
    with st.spinner("Agentai dirba..."):
        time.sleep(1)  # simuliacija
        for agent in selected_agents:
            response = f"{AGENTS[agent]['name']} atsakymas į: {task_input[:50]}...\n\n"
            if agent == "image_analyzer" and uploaded_image:
                response += tools.view_image(uploaded_image.getvalue())
            elif agent == "vet_ekspertas" and uploaded_audio:
                response += tools.audio_analysis(uploaded_audio.getvalue())
            else:
                response += "Simuliuotas atsakymas – viskas veikia!"
            st.session_state.agent_outputs[agent].append(response)
        st.success("Užduotis įvykdyta!")
        st.rerun()

# Rezultatai
st.subheader("📊 Agentų Rezultatai")
tabs = st.tabs([AGENTS[a]["name"] for a in AGENTS])
for i, agent in enumerate(AGENTS):
    with tabs[i]:
        outputs = st.session_state.agent_outputs[agent]
        if outputs:
            for output in reversed(outputs[-5:]):
                st.markdown(f"<div class='agent-card'>{output}</div>", unsafe_allow_html=True)
                st.divider()
        else:
            st.info("Laukia užduoties...")

st.caption("Rūpestėlis Ekosistema v1.5 | Multimodal + Garso analizė | 2025")
