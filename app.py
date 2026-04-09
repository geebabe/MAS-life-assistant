import streamlit as st
import os
import uuid
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MAS_Streamlit")

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")

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
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = os.getenv("USER_ID", str(uuid.uuid4()))

# Sidebar
with st.sidebar:
    st.title("🤖 MAS Life Assistant")
    st.info("Your personal agentic decision engine.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.write(f"User ID: `{st.session_state.user_id}`")
    st.write(f"API Target: `{API_URL}`")
    
    # Simple Health Check Button
    if st.button("Check API Connectivity"):
        try:
            res = requests.get(f"{API_URL}/")
            if res.status_code == 200:
                st.success("API is Online")
            else:
                st.error(f"API connection error: {res.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")

# Header
st.title("Personal Life Assistant")
st.write("Expert decisions tailored to your personal context via FastAPI.")

# Display Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display Details if they exist (only for assistant messages)
        if msg["role"] == "assistant" and "details" in msg:
            with st.expander("Agent Reasoning Details"):
                details = msg["details"]
                if details.get("intent_category"):
                    st.markdown(f"**Intent**: {details['intent_category']}")
                if details.get("memories"):
                    st.markdown("**Retrieved Memories**:")
                    for m in details["memories"]:
                        st.markdown(f"- {m}")
                if details.get("search_needed"):
                    st.markdown(f"**Search Query**: {details['search_query']}")
                if details.get("insights"):
                    st.markdown("**Insights Logged**:")
                    for insight in details["insights"]:
                        st.markdown(f"✓ {insight}")

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        response_placeholder = st.empty()
        
        status_placeholder.info("🤖 Agent is thinking and processing...")

        try:
            # Call the FastAPI backend
            payload = {
                "query": prompt,
                "user_id": st.session_state.user_id
            }
            
            response = requests.post(f"{API_URL}/api/chat/", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                decision = data.get("decision", "No decision made.")
                
                # Clear status and show final
                status_placeholder.empty()
                response_placeholder.markdown(decision)
                
                # Save to history with rich details from API
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": decision,
                    "details": data
                })
                st.rerun()
            else:
                status_placeholder.error(f"API Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            status_placeholder.error(f"Network error: {str(e)}")
            logger.exception("API Communication Failure")

