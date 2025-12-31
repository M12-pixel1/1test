# graph.py
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from datetime import datetime

class AgentState(TypedDict):
    task: str
    messages: List[str]
    agent_outputs: Dict[str, str]
    metadata: Dict[str, any]
    tools_used: List[str]
    errors: List[dict]

def create_agent_graph():
    def supervisor(state: AgentState):
        state["messages"].append(f"Vadovas priėmė užduotį: {state['task']}")
        return state

    def dummy_agent(state: AgentState):
        agent = list(state["agent_outputs"].keys())[0]  # paprastas pavyzdys
        state["agent_outputs"][agent] = f"{agent.capitalize()} atliko: {state['task'][:100]}..."
        return state

    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor)
    
    agents = ["testuotojas", "vet_ekspertas", "kodo_fixer", "image_analyzer", "monetizacijos_strategas"]
    for agent in agents:
        graph.add_node(agent, dummy_agent)
        graph.add_edge(agent, END)
    
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges("supervisor", lambda s: agents[:1])  # paprastas testui
    
    return graph.compile()
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
# Grok jei turi SDK, arba per custom

llm_claude = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key="tavo_key")
llm_gpt = ChatOpenAI(model="gpt-4o", api_key="tavo_key")
llm_grok = ChatOpenAI(base_url="https://api.x.ai/v1", model="grok-beta", api_key="tavo_key")

# Agentams priskiri:
kodo_agent.llm = llm_claude
image_agent.llm = llm_gpt
vet_agent.llm = llm_grok
