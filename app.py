import streamlit as st
import os
import uuid
import logging
from dotenv import load_dotenv
from graph.workflow import workflow, AgentState
from agents.memory_writer import MemoryWriterAgent

# Load environment variables
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAS_Streamlit")

# Page Config
st.set_page_config(
    page_title="MAS Life Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .reasoning-step {
        font-size: 0.9em;
        color: #6c757d;
        font-style: italic;
        border-left: 3px solid #007bff;
        padding-left: 10px;
        margin: 5px 0;
    }
    .feedback-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = os.getenv("USER_ID", str(uuid.uuid4()))
if "current_steps" not in st.session_state:
    st.session_state.current_steps = []

# Sidebar
with st.sidebar:
    st.title("🤖 MAS Life Assistant")
    st.info("Your personal agentic decision engine powered by LangGraph.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write(f"User ID: `{st.session_state.user_id}`")

# Header
st.title("Personal Life Assistant")
st.write("Expert decisions tailored to your personal context.")

# Display Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display Reasoning Steps if they exist (only for assistant messages)
        if msg["role"] == "assistant" and "reasoning" in msg:
            with st.expander("Reasoning Steps"):
                for step in msg["reasoning"]:
                    st.markdown(f"*{step}*")
        
        # Feedback Section removed as requested

# Feedback Area removed as requested

# Node Name Mapping
NODE_MESSAGES = {
    "intent": "🧠 Identifying your intent...",
    "memory": "🗂️ Consulting your personal memories...",
    "search": "🔍 Searching the web for real-time info...",
    "decision": "💡 Crafting the best decision...",
    "critic": "🛡️ Quality-checking the response...",
    "writer": "📝 Recording new insights..."
}

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    # Clear previous reasoning steps
    st.session_state.current_steps = []
    
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        reasoning_container = st.empty()
        response_placeholder = st.empty()
        
        # Initial State
        state = {
            "query": prompt,
            "user_id": st.session_state.user_id,
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

        # Run Workflow Streaming
        steps_log = []
        try:
            for update in workflow.stream(state):
                # Update looks like: {'intent': {...}} or {'memory': {...}}
                for node_name, node_output in update.items():
                    msg = NODE_MESSAGES.get(node_name, f"Processing {node_name}...")
                    steps_log.append(msg)
                    
                    # Update status in UI
                    status_placeholder.info(msg)
                    
                    # Store data if relevant for reasoning display
                    # (In a more complex app, we'd capture more details from node_output here)
            
            # Final output is the last state
            final_state = workflow.invoke(state) # We run invoke to get the full final state easily
            # (Note: streaming captures updates, but invoke is easier for the final state object)
            
            decision = final_state.get("decision", "I couldn't reach a decision.")
            
            # Clear status and show final
            status_placeholder.empty()
            response_placeholder.markdown(decision)
            
            # Save to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": decision,
                "reasoning": steps_log
            })
            
            # Rerun to show buttons and stable layout from history loop
            st.rerun()
            
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            logger.exception("Workflow Error")

