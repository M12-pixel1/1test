import streamlit as st
import asyncio
from datetime import datetime
from typing import Dict, List
import json
import sys
from pathlib import Path

# Importuojame LangGraph backend
try:
    from graph import create_agent_graph, AgentState
    from tools import get_available_tools
except ImportError as e:
    st.error(f"❌ Import klaida: {e}")
    st.info("Įsitikinkite, kad graph.py ir tools.py yra tame pačiame kataloge")
    st.stop()

# Konfigūracija
st.set_page_config(
    page_title="Rūpestėlio Ekosistemos Dashboard",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Patobūlintas CSS stilius
st.markdown("""
<style>
    .agent-card {
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 2px solid #e1e8ed;
        margin: 0.8rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .agent-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    .status-active { 
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-color: #28a745;
    }
    .status-idle { 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .status-working { 
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-color: #ffc107;
        animation: pulse 2s infinite;
    }
    .status-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-color: #dc3545;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    .task-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .tool-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        background: #e3f2fd;
        color: #1976d2;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 600;
    }
    .success-banner {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        text-align: center;
    }
    .error-banner {
        background: linear-gradient(90deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background: #f8f9fa;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializuojame session state su error handling
def init_session_state():
    """Inicializuoja session state su default reikšmėmis"""
    defaults = {
        'graph': None,
        'messages': [],
        'agent_outputs': {
            "testuotojas": [],
            "vet_ekspertas": [],
            "kodo_fixer": [],
            "image_analyzer": [],
            "monetizacijos_strategas": []
        },
        'current_task': None,
        'task_history': [],
        'execution_stats': {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'total_execution_time': 0
        },
        'available_tools': [],
        'tool_usage_count': {},
        'errors_log': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Inicializuojame graph tik jei dar neegzistuoja
    if st.session_state.graph is None:
        try:
            st.session_state.graph = create_agent_graph()
            st.session_state.available_tools = get_available_tools()
        except Exception as e:
            st.error(f"❌ Klaida inicializuojant sistemą: {e}")
            st.session_state.errors_log.append({
                'time': datetime.now().isoformat(),
                'error': str(e),
                'location': 'init_session_state'
            })

init_session_state()

# Agentų konfigūracija su išplėstais duomenimis
AGENTS = {
    "testuotojas": {
        "name": "🧪 Testuotojas",
        "role": "QA Inžinierius",
        "description": "Testuoja kodą, rašo unit testus, patikrina funkcionalumą",
        "color": "#3498db",
        "capabilities": ["Unit Testing", "Integration Testing", "Performance Testing", "Security Testing"],
        "tools": ["code_execution", "test_runner"]
    },
    "vet_ekspertas": {
        "name": "🏥 Veterinarijos Ekspertas",
        "role": "Gyvūnų Sveikatos Specialistas",
        "description": "Konsultuoja apie gyvūnų sveikatą, duoda rekomendacijas",
        "color": "#2ecc71",
        "capabilities": ["Health Assessment", "Nutrition Planning", "Disease Diagnosis", "Emergency Response"],
        "tools": ["web_search", "knowledge_base"]
    },
    "kodo_fixer": {
        "name": "🔧 Kodo Fixer'is",
        "role": "Bug Fixing Specialistas",
        "description": "Taiso klaidas, optimizuoja kodą, refactorinta",
        "color": "#e74c3c",
        "capabilities": ["Bug Detection", "Code Optimization", "Refactoring", "Security Patches"],
        "tools": ["code_execution", "static_analysis"]
    },
    "image_analyzer": {
        "name": "📸 Image Analyzer",
        "role": "Kompiuterinės Regos Ekspertas",
        "description": "Analizuoja nuotraukas, atpažįsta objektus, ekstraktuoja informaciją",
        "color": "#9b59b6",
        "capabilities": ["Object Detection", "Breed Classification", "Health Screening", "Emotion Recognition"],
        "tools": ["view_image", "ml_inference"]
    },
    "monetizacijos_strategas": {
        "name": "💰 Monetizacijos Strategas",
        "role": "Verslo Plėtros Vadovas",
        "description": "Planuoja monetizacijos strategijas, skaičiuoja ROI",
        "color": "#f39c12",
        "capabilities": ["Market Analysis", "Revenue Modeling", "Partnership Strategy", "Growth Hacking"],
        "tools": ["web_search", "analytics"]
    }
}

# =======================
# SIDEBAR
# =======================
with st.sidebar:
    st.title("🐾 Rūpestėlio Ekosistema")
    st.markdown("### Multi-Agent AI Sistema")
    
    # Sistema statistika
    st.divider()
    st.markdown("### 📊 Sistema Statistika")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Užduotys", st.session_state.execution_stats['total_tasks'])
        st.metric("Sėkmingos", st.session_state.execution_stats['successful_tasks'])
    with col2:
        if st.session_state.execution_stats['total_tasks'] > 0:
            success_rate = (st.session_state.execution_stats['successful_tasks'] / 
                          st.session_state.execution_stats['total_tasks'] * 100)
            st.metric("Sėkmė %", f"{success_rate:.1f}%")
        else:
            st.metric("Sėkmė %", "0%")
        st.metric("Nesėkmės", st.session_state.execution_stats['failed_tasks'])
    
    st.divider()
    
    # Agentų būsenos
    st.markdown("### 👥 Agentų Būsenos")
    for agent_id, agent_info in AGENTS.items():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{agent_info['name']}**")
                st.caption(agent_info['role'])
            with col2:
                if st.session_state.current_task:
                    if agent_id in st.session_state.current_task.get('agents', []):
                        if agent_id in st.session_state.current_task.get('results', {}):
                            st.markdown("✅")  # Completed
                        else:
                            st.markdown("🟡")  # Working
                    else:
                        st.markdown("⚪")  # Not assigned
                else:
                    st.markdown("🟢")  # Idle
    
    st.divider()
    
    # Available Tools
    st.markdown("### 🛠️ Priemonės")
    if st.session_state.available_tools:
        for tool in st.session_state.available_tools[:5]:
            st.markdown(f"<span class='tool-badge'>{tool}</span>", unsafe_allow_html=True)
    else:
        st.info("Kraunami tools...")
    
    st.divider()
    
    # Užduočių istorija
    st.markdown("### 📋 Paskutinės Užduotys")
    if st.session_state.task_history:
        for i, task in enumerate(reversed(st.session_state.task_history[-5:])):
            status_icon = "✅" if task.get('status') == 'success' else "❌"
            with st.expander(f"{status_icon} Užduotis #{len(st.session_state.task_history) - i}"):
                st.text(task['task'][:100] + "...")
                st.caption(f"⏱️ {task['timestamp']}")
                if task.get('execution_time'):
                    st.caption(f"⚡ {task['execution_time']:.2f}s")
    else:
        st.info("Dar nėra užduočių")
    
    st.divider()
    
    # System controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Log", use_container_width=True):
            st.session_state.task_history = []
            st.session_state.errors_log = []
            st.rerun()

# =======================
# MAIN CONTENT
# =======================
st.title("🎯 Vadovo Komandų Centras")
st.markdown("**Delegavimo sistema su pažangiomis priemonėmis**")

# Error display jei yra
if st.session_state.errors_log:
    with st.expander("⚠️ Sistemų Klaidos", expanded=False):
        for error in st.session_state.errors_log[-3:]:
            st.error(f"**{error['time']}** - {error['location']}: {error['error']}")

# Užduoties įvedimas
st.markdown("### 📝 Nauja Užduotis")

col1, col2 = st.columns([3, 1])

with col1:
    task_input = st.text_area(
        "Įveskite užduotį agentams:",
        placeholder="Pvz: Išanalizuok šunų mitybos rekomendacijas ir sukurk testą funkcionalumui...",
        height=120,
        help="Būkite konkretūs - geresnė užduotis = geresni rezultatai"
    )

with col2:
    st.markdown("**Prioritetas:**")
    priority = st.select_slider(
        "priority",
        options=["Žemas", "Vidutinis", "Aukštas", "Kritinis"],
        value="Vidutinis",
        label_visibility="collapsed"
    )
    
    delegate_all = st.checkbox("Visi agentai", value=True, help="Delegavimas visiems 5 agentams")
    
    use_tools = st.checkbox("Naudoti Tools", value=True, help="Įgalina web_search, code_execution ir kitus įrankius")

# Agentų pasirinkimas
if not delegate_all:
    st.markdown("**Pasirinkite agentus:**")
    selected_agents = []
    cols = st.columns(5)
    for i, (agent_id, agent_info) in enumerate(AGENTS.items()):
        with cols[i]:
            if st.checkbox(agent_info['name'].split()[1], key=f"select_{agent_id}", value=True):
                selected_agents.append(agent_id)
else:
    selected_agents = list(AGENTS.keys())

# Advanced options
with st.expander("🔧 Išplėstinės Nuostatos"):
    col1, col2, col3 = st.columns(3)
    with col1:
        max_iterations = st.slider("Max iteracijos", 1, 10, 5)
    with col2:
        timeout = st.slider("Timeout (s)", 10, 300, 60)
    with col3:
        parallel_exec = st.checkbox("Parallel vykdymas", value=False)

# Execute mygtukas
execute_col1, execute_col2, execute_col3 = st.columns([2, 1, 1])

with execute_col1:
    execute_button = st.button("🚀 Vykdyti Užduotį", type="primary", use_container_width=True)

with execute_col2:
    if st.button("💾 Išsaugoti Draft", use_container_width=True):
        st.info("Draft funkcionalumas - soon!")

with execute_col3:
    if st.button("📊 Analizė", use_container_width=True):
        st.info("Task analysis - soon!")

if execute_button:
    if task_input.strip():
        start_time = datetime.now()
        
        with st.spinner("🤖 Agentų sistema dirba..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Inicializuojame state
            initial_state = AgentState(
                task=task_input,
                messages=[],
                current_agent="supervisor",
                agent_outputs={},
                metadata={
                    "priority": priority,
                    "selected_agents": selected_agents,
                    "timestamp": datetime.now().isoformat(),
                    "use_tools": use_tools,
                    "max_iterations": max_iterations,
                    "timeout": timeout,
                    "parallel": parallel_exec
                }
            )
            
            try:
                # Vykdome graph su progress updates
                total_agents = len(selected_agents)
                completed_agents = 0
                
                status_text.text("Pradedama užduotis...")
                progress_bar.progress(10)
                
                final_state = st.session_state.graph.invoke(initial_state)
                
                progress_bar.progress(100)
                status_text.text("Užduotis įvykdyta!")
                
                # Apskaičiuojame execution time
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                # Išsaugome rezultatus
                st.session_state.current_task = {
                    "task": task_input,
                    "priority": priority,
                    "agents": selected_agents,
                    "results": final_state["agent_outputs"],
                    "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "execution_time": execution_time,
                    "status": "success",
                    "metadata": final_state.get("metadata", {})
                }
                
                st.session_state.task_history.append(st.session_state.current_task)
                
                # Atnaujiname statistiką
                st.session_state.execution_stats['total_tasks'] += 1
                st.session_state.execution_stats['successful_tasks'] += 1
                st.session_state.execution_stats['total_execution_time'] += execution_time
                
                # Atnaujiname agentų outputus
                for agent_id, output in final_state["agent_outputs"].items():
                    if agent_id in st.session_state.agent_outputs:
                        st.session_state.agent_outputs[agent_id].append({
                            "task": task_input,
                            "output": output,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "execution_time": execution_time
                        })
                
                # Success banner
                st.markdown(f"""
                <div class='success-banner'>
                    ✅ Užduotis įvykdyta sėkmingai! ⚡ {execution_time:.2f}s
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                st.rerun()
                
            except Exception as e:
                progress_bar.progress(0)
                status_text.text("")
                
                error_msg = str(e)
                st.markdown(f"""
                <div class='error-banner'>
                    ❌ Klaida vykdant užduotį: {error_msg}
                </div>
                """, unsafe_allow_html=True)
                
                # Log error
                st.session_state.errors_log.append({
                    'time': datetime.now().isoformat(),
                    'error': error_msg,
                    'location': 'task_execution',
                    'task': task_input[:100]
                })
                
                st.session_state.execution_stats['total_tasks'] += 1
                st.session_state.execution_stats['failed_tasks'] += 1
                
    else:
        st.warning("⚠️ Įveskite užduotį!")

st.divider()

# =======================
# AGENTŲ TABS
# =======================
st.markdown("### 🤖 Agentų Darbo Erdvės")

tabs = st.tabs([agent_info['name'] for agent_info in AGENTS.values()])

for tab_idx, (agent_id, agent_info) in enumerate(AGENTS.items()):
    with tabs[tab_idx]:
        # Agent header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"#### {agent_info['name']}")
            st.caption(f"**Rolė:** {agent_info['role']}")
            st.caption(f"**Aprašymas:** {agent_info['description']}")
        with col2:
            # Agent metrics
            total_tasks = len(st.session_state.agent_outputs[agent_id])
            st.metric("Užduočių", total_tasks)
        
        # Capabilities
        st.markdown("**💪 Gebėjimai:**")
        for capability in agent_info['capabilities']:
            st.markdown(f"- {capability}")
        
        # Tools
        st.markdown("**🛠️ Priemonės:**")
        for tool in agent_info['tools']:
            st.markdown(f"<span class='tool-badge'>{tool}</span>", unsafe_allow_html=True)
        
        st.divider()
        
        # Dabartinė užduotis
        if st.session_state.current_task and agent_id in st.session_state.current_task.get('agents', []):
            st.markdown("**🎯 Dabartinė Užduotis:**")
            st.info(st.session_state.current_task['task'])
            
            # Agento rezultatas
            if agent_id in st.session_state.current_task.get('results', {}):
                st.markdown("**📤 Agento Atsakymas:**")
                result = st.session_state.current_task['results'][agent_id]
                
                # Styled container
                st.markdown(f"""
                <div class="agent-card status-active">
                    {result.replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📋 Copy", key=f"copy_{agent_id}"):
                        st.info("Copy funkcionalumas - soon!")
                with col2:
                    if st.button("💾 Export", key=f"export_{agent_id}"):
                        st.download_button(
                            "Download",
                            result,
                            file_name=f"{agent_id}_output.txt",
                            key=f"dl_{agent_id}"
                        )
                with col3:
                    if st.button("🔄 Re-run", key=f"rerun_{agent_id}"):
                        st.info("Re-run funkcionalumas - soon!")
        
        # Istorija
        st.markdown("**📜 Užduočių Istorija:**")
        if st.session_state.agent_outputs[agent_id]:
            for i, item in enumerate(reversed(st.session_state.agent_outputs[agent_id][-5:])):
                with st.expander(f"Užduotis {len(st.session_state.agent_outputs[agent_id]) - i} - {item['timestamp']}"):
                    st.markdown("**Užduotis:**")
                    st.text(item['task'])
                    st.markdown("**Atsakymas:**")
                    st.write(item['output'])
                    if 'execution_time' in item:
                        st.caption(f"⚡ Vykdymo laikas: {item['execution_time']:.2f}s")
        else:
            st.info(f"{agent_info['name']} dar neturi atliktų užduočių")

# =======================
# FOOTER
# =======================
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🐾 <strong>Rūpestėlio Ekosistemos Agentūra</strong> | Production-Ready Multi-Agent Sistema</p>
    <p style='font-size: 0.9rem;'>Powered by LangGraph + Streamlit + Advanced Tools Integration</p>
    <p style='font-size: 0.8rem;'>v2.0.0 - Enhanced Edition with Error Handling & Real-time Stats</p>
</div>
""", unsafe_allow_html=True)
