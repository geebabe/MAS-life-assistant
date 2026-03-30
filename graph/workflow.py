import logging
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

# Import Agents
from agents.intent import IntentAgent
from agents.memory_retrieval import MemoryRetrievalAgent
from agents.search import SearchAgent
from agents.decision import DecisionAgent
from agents.critic import CriticAgent
from agents.memory_writer import MemoryWriterAgent

logger = logging.getLogger(__name__)

# Define the state structure
class AgentState(TypedDict):
    # Input
    query: str
    user_id: str
    
    # Intent output
    intent_category: Optional[str]
    search_needed: bool
    search_query: Optional[str]
    
    # Retrieval output
    memories: List[str]
    external_context: Optional[str]
    
    # Decision output
    decision: Optional[str]
    
    # Critic output
    is_valid: bool
    critic_feedback: Optional[str]
    revision_count: int
    
    # Final output
    insights: List[str]

# Instantiate agents globally so they can hold config/clients efficiently
intent_agent = IntentAgent()
memory_agent = MemoryRetrievalAgent()
search_agent = SearchAgent()
decision_agent = DecisionAgent()
critic_agent = CriticAgent()
writer_agent = MemoryWriterAgent()

# --- Define Nodes ---
def intent_node(state: AgentState) -> Dict:
    result = intent_agent.classify(state["query"])
    return {
        "intent_category": result.get("category"),
        "search_needed": result.get("search_needed", False),
        "search_query": result.get("search_query", state["query"])
    }

def memory_node(state: AgentState) -> Dict:
    memories = memory_agent.retrieve(state["query"], user_id=state["user_id"])
    return {"memories": memories}

def search_node(state: AgentState) -> Dict:
    # Only called if search_needed is true
    if state.get("search_needed") and state.get("search_query"):
        context = search_agent.search(state["search_query"])
        return {"external_context": context}
    return {"external_context": None}

def decision_node(state: AgentState) -> Dict:
    decision = decision_agent.decide(
        query=state["query"],
        memories=state.get("memories", []),
        external_context=state.get("external_context"),
        critic_feedback=state.get("critic_feedback")
    )
    # Increment revision count when deciding
    new_count = state.get("revision_count", 0) + 1
    return {"decision": decision, "revision_count": new_count}

def critic_node(state: AgentState) -> Dict:
    evaluation = critic_agent.evaluate(
        query=state["query"],
        decision=state["decision"],
        memories=state.get("memories", [])
    )
    return {
        "is_valid": evaluation.get("is_valid", True),
        "critic_feedback": evaluation.get("feedback")
    }

def writer_node(state: AgentState) -> Dict:
    insights = writer_agent.write(
        query=state["query"],
        decision=state["decision"],
        user_feedback=None,  # Handled separately post-interaction
        user_id=state["user_id"]
    )
    return {"insights": insights}

# --- Define Routing Functions ---
def route_after_memory(state: AgentState) -> str:
    """Route to search if needed, else directly to decision."""
    if state.get("search_needed"):
        return "search"
    return "decision"

def route_after_critic(state: AgentState) -> str:
    """Route back to decision if invalid (up to a limit), else proceed to save memory."""
    if not state.get("is_valid") and state.get("revision_count", 0) < 2:
        logger.info(f"Critic rejected decision. Retrying. (Attempt {state.get('revision_count')})")
        return "decision"
    return "writer"

# --- Build LangGraph ---
builder = StateGraph(AgentState)

builder.add_node("intent", intent_node)
builder.add_node("memory", memory_node)
builder.add_node("search", search_node)
builder.add_node("decision", decision_node)
builder.add_node("critic", critic_node)
builder.add_node("writer", writer_node)

builder.set_entry_point("intent")

builder.add_edge("intent", "memory")
builder.add_conditional_edges("memory", route_after_memory, {"search": "search", "decision": "decision"})
builder.add_edge("search", "decision")
builder.add_edge("decision", "critic")
builder.add_conditional_edges("critic", route_after_critic, {"decision": "decision", "writer": "writer"})
builder.add_edge("writer", END)

workflow = builder.compile()

def run_workflow(query: str, user_id: str = "default_user") -> AgentState:
    """
    Executes the main decision engine workflow for a given query.
    """
    logger.info(f"Starting workflow for query: '{query}'")
    
    initial_state = {
        "query": query,
        "user_id": user_id,
        "intent_category": None,
        "search_needed": False,
        "search_query": None,
        "memories": [],
        "external_context": None,
        "decision": None,
        "is_valid": True,
        "critic_feedback": None,
        "revision_count": 0,
        "insights": []
    }
    
    # Run the graph
    final_state = workflow.invoke(initial_state)
    logger.info("Workflow execution completed.")
    
    return final_state

if __name__ == "__main__":
    # Internal module testing
    logging.basicConfig(level=logging.INFO)
    test_q = "Should I study at home or go to a cafe?"
    res = run_workflow(test_q)
    print("\n--- Final Decision ---")
    print(res.get("decision"))
    print("\n--- Extracted Insights ---")
    print(res.get("insights"))
