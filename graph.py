# graph.py
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    task: str
    messages: List[str]
    current_agent: str
    agent_outputs: Dict[str, str]
    metadata: Dict[str, Any]
    tools_used: List[str]
    errors: List[Dict]

def create_agent_graph():
    # Paprastas graph – supervisor deleguoja agentams
    def supervisor(state: AgentState) -> AgentState:
        state["messages"].append("Vadovas: užduotis priimta")
        return state
    
    def dummy_agent(state: AgentState) -> AgentState:
        agent = state["current_agent"]
        state["agent_outputs"][agent] = f"{agent.capitalize()} atliko užduotį: {state['task'][:50]}..."
        return state
    
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor)
    
    agents = ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]
    for agent in agents:
        graph.add_node(agent, dummy_agent)
        graph.add_edge(agent, END)
    
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        lambda state: state["metadata"].get("selected_agents", agents),
        {agent: agent for agent in agents}
    )
    
    return graph.compile()
