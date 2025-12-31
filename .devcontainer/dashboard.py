"""
Rūpestėlio Ekosistemos Dashboard v1.1 - Pataisytas ir Optimizuotas
Kodo Inžinieriaus pataisymai: sintaksė, tools integracija, optimizacija, UI
"""
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Any
import time
import json

# ==================== KONFIGŪRACIJA ====================
st.set_page_config(
    page_title="Rūpestėlio Ekosistema",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== TOOLS INTEGRACIJA (su fallback) ====================
class ToolsManager:
    """Valdytojas AI įrankiams su fallback mechanizmu"""
    
    @staticmethod
    def view_image(image_path: str) -> Dict[str, Any]:
        """Vaizdų analizės įrankis"""
        try:
            # TODO: Integruoti realią Claude vision API
            return {
                "success": True,
                "analysis": f"Vaizdas '{image_path}' išanalizuotas (simuliacija)",
                "detected": ["šuo", "simptomas: paraudimas"],
                "confidence": 0.92
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def web_search(query: str) -> Dict[str, Any]:
        """Web paieškos įrankis"""
        try:
            # TODO: Integruoti Anthropic web_search tool
            return {
                "success": True,
                "results": [
                    {"title": "Šunų niežulys: priežastys", "url": "https://example.com/1"},
                    {"title": "Veterinarinė pagalba", "url": "https://example.com/2"}
                ],
                "query": query
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def code_execution(code: str) -> Dict[str, Any]:
        """Kodo vykdymo įrankis (saugus sandbox)"""
        try:
            # TODO: Integruoti saugų Python sandbox
            return {
                "success": True,
                "output": f"Kodas įvykdytas (simuliacija):\n{code[:100]}...",
                "execution_time": 0.05
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

# ==================== SESSION STATE VALDYMAS ====================
def initialize_session_state() -> None:
    """Inicializuoja session state su default reikšmėmis"""
    defaults = {
        'messages': [],
        'agent_outputs': {
            "testuotojas": [],
            "vet_ekspertas": [],
            "kodo_fixer": [],
            "image_analyzer": [],
            "monetizacijos_strategas": []
        },
        'task_history': [],
        'tools_used': [],
        'total_tasks': 0,
        'initialized': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ==================== AGENTŲ SISTEMA ====================
AGENTS = {
    "testuotojas": {
        "name": "🧪 Testuotojas",
        "description": "Tikrina kodą, atlieka testus, randa klaidas",
        "color": "#FF6B6B"
    },
    "vet_ekspertas": {
        "name": "🏥 Vet Ekspertas",
        "description": "Medicininis tikslumas, diagnozės",
        "color": "#4ECDC4"
    },
    "kodo_fixer": {
        "name": "🔧 Kodo Fixer'is",
        "description": "Taiso klaidas, optimizuoja kodą",
        "color": "#95E1D3"
    },
    "image_analyzer": {
        "name": "📸 Image Analyzer",
        "description": "Vaizdų analizė su AI",
        "color": "#F38181"
    },
    "monetizacijos_strategas": {
        "name": "💰 Monetizacija",
        "description": "Pelno strategijos, premium features",
        "color": "#FFD93D"
    }
}

def execute_agent_task(agent_id: str, task: str, tools: ToolsManager) -> Dict[str, Any]:
    """
    Vykdo agento užduotį su tools integracija
    
    Args:
        agent_id: Agento ID
        task: Užduotis tekstas
        tools: Tools manager instancija
    
    Returns:
        Dict su agento atsakymu
    """
    agent = AGENTS.get(agent_id, {})
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Simuliuojam agento darbą su tools
    response = {
        "agent": agent.get("name", agent_id),
        "timestamp": timestamp,
        "task": task,
        "response": "",
        "tools_used": [],
        "status": "success"
    }
    
    # Agento specifinis response
    if agent_id == "image_analyzer":
        tool_result = tools.view_image("user_upload.jpg")
        response["tools_used"].append("view_image")
        response["response"] = f"""
**Vaizdų Analizė:**
- Analizuotas vaizdas: user_upload.jpg
- Aptikta: {tool_result.get('detected', [])}
- Tikimybė: {tool_result.get('confidence', 0):.0%}

**Rekomendacijos:** Pastebėti simptomų požymiai, rekomenduoju konsultaciją su Vet Ekspertu.
        """
    
    elif agent_id == "vet_ekspertas":
        search_result = tools.web_search(f"veterinarija: {task}")
        response["tools_used"].append("web_search")
        response["response"] = f"""
**Veterinarinė Analizė:**
- Užklausa: {task}
- Rasti šaltiniai: {len(search_result.get('results', []))}

**Diagnozė (preliminari):** Pagal simptomus, galimas dermatitas. Reikalingas tikslesnis tyrimas.
**Rekomendacija:** Vizitas pas veterinarą per 24-48h.
        """
    
    elif agent_id == "kodo_fixer":
        response["response"] = f"""
**Kodo Analizė:**
- Patikrintas kodas: ✓
- Rastos klaidos: 0
- Optimizacijos galimybės: 2

**Atlikti pataisymai:**
1. Pridėtas error handling
2. Optimizuotas session state
3. Pridėti type hints

**Statusas:** Kodas stabilus ir paruoštas produkcijai.
        """
    
    elif agent_id == "testuotojas":
        response["response"] = f"""
**Testų Rezultatai:**
- Unit testai: ✓ 12/12 passed
- Integraciniai testai: ✓ 8/8 passed
- UI testai: ✓ 5/5 passed

**Aptikta problemų:** 0
**Padengimas:** 94%

**Rekomendacija:** Kodas paruoštas deployment'ui.
        """
    
    elif agent_id == "monetizacijos_strategas":
        response["response"] = f"""
**Monetizacijos Strategija:**

**Tier 1 (Free):**
- 5 užklausos/dieną
- Bazinė vaizdų analizė
- Riboti agentai

**Tier 2 (Premium - 9.99€/mėn):**
- Neriboti užklausos
- Visi agentai
- Prioritetinis palaikymas
- Export funkcijos

**Tier 3 (Professional - 29.99€/mėn):**
- API prieiga
- Custom agentai
- Analytics dashboard
- White-label opcija

**ROI prognozė:** 500+ vartotojų per 3 mėn = ~3000€/mėn
        """
    
    else:
        response["response"] = f"Gavo užduotį: {task}\n\nAtsakymas procesavimo stadijoje..."
    
    return response

# ==================== MAIN UI ====================
def main():
    """Pagrindinis dashboard'as"""
    
    # Inicializuojam state
    initialize_session_state()
    tools = ToolsManager()
    
    # Header su statistika
    st.title("🐾 Rūpestėlio Ekosistemos Vadovo Centras")
    st.markdown("**Multi-Agent AI Sistema** – CrewAI + LangGraph hibridas")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Viso Užduočių", st.session_state.total_tasks)
    with col2:
        st.metric("Aktyvūs Agentai", len(AGENTS))
    with col3:
        st.metric("Tools Panaudota", len(st.session_state.tools_used))
    with col4:
        st.metric("Statusas", "🟢 Online")
    
    st.divider()
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.header("🤖 Agentų Sistema")
        
        for agent_id, agent_data in AGENTS.items():
            with st.expander(agent_data["name"]):
                st.write(agent_data["description"])
                outputs_count = len(st.session_state.agent_outputs.get(agent_id, []))
                st.caption(f"Užduotys atliktos: {outputs_count}")
        
        st.divider()
        
        # Reset mygtukas
        if st.button("🔄 Reset Sistemą", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != 'initialized':
                    del st.session_state[key]
            st.rerun()
        
        st.divider()
        st.caption("v1.1 | Pataisyta ir Optimizuota")
        st.caption("Kodo Inžinierius © 2025")
    
    # ==================== UŽDUOTIS ====================
    st.subheader("📋 Nauja Užduotis")
    
    with st.form("task_form", clear_on_submit=True):
        task = st.text_area(
            "Aprašyk užduotį agentams",
            height=120,
            placeholder="Pvz.: Išanalizuok šunų niežulį, patikrink kodą ir pasiūlyk monetizacijos strategiją",
            help="Agentai dirbs bendrai, kad išspręstų užduotį"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected = st.multiselect(
                "Pasirink agentus",
                options=list(AGENTS.keys()),
                default=list(AGENTS.keys()),
                format_func=lambda x: AGENTS[x]["name"]
            )
        
        with col2:
            st.write("")
            st.write("")
            go = st.form_submit_button("▶ Vykdyti", type="primary", use_container_width=True)
    
    # ==================== UŽDUOTIES VYKDYMAS ====================
    if go and task and selected:
        st.session_state.total_tasks += 1
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, agent_id in enumerate(selected):
            progress = (idx + 1) / len(selected)
            progress_bar.progress(progress)
            status_text.text(f"🔄 {AGENTS[agent_id]['name']} dirba...")
            
            # Simuliuojam laiką
            time.sleep(0.5)
            
            # Vykdom užduotį
            result = execute_agent_task(agent_id, task, tools)
            st.session_state.agent_outputs[agent_id].append(result)
            st.session_state.tools_used.extend(result.get("tools_used", []))
        
        progress_bar.progress(1.0)
        status_text.empty()
        st.success(f"✅ Užduotis įvykdyta! {len(selected)} agentai baigė darbą.")
        
        # Įrašom istoriją
        st.session_state.task_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "agents": selected
        })
        
        time.sleep(1)
        st.rerun()
    
    # ==================== REZULTATŲ TABS ====================
    st.divider()
    st.subheader("📊 Agentų Rezultatai")
    
    tabs = st.tabs([AGENTS[aid]["name"] for aid in AGENTS.keys()])
    
    for idx, agent_id in enumerate(AGENTS.keys()):
        with tabs[idx]:
            outputs = st.session_state.agent_outputs.get(agent_id, [])
            
            if outputs:
                for output in reversed(outputs[-10:]):  # Paskutiniai 10
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**⏱ {output['timestamp']}**")
                        with col2:
                            st.markdown(f"*Tools: {', '.join(output.get('tools_used', []) or ['none'])}*")
                        
                        st.markdown(output["response"])
                        
                        with st.expander("📋 Užduotis"):
                            st.text(output["task"])
                        
                        st.divider()
            else:
                st.info(f"👋 {AGENTS[agent_id]['name']} laukia pirmosios užduoties!")
                st.markdown("""
                **Kaip naudoti:**
                1. Įvesk užduotį viršuje
                2. Pasirink šį agentą
                3. Spausk 'Vykdyti'
                """)
    
    # ==================== ISTORIJA ====================
    if st.session_state.task_history:
        st.divider()
        with st.expander("📜 Užduočių Istorija"):
            for entry in reversed(st.session_state.task_history[-20:]):
                st.markdown(f"**{entry['timestamp']}** - {entry['task'][:60]}...")
                st.caption(f"Agentai: {', '.join([AGENTS[a]['name'] for a in entry['agents']])}")
                st.divider()

# ==================== PALEIDIMAS ====================
if __name__ == "__main__":
    main()
