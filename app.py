# app.py
import streamlit as st
import requests
import extra_streamlit_components as stx
import uuid
import os

# Uses ENV variable if available, otherwise defaults to local FastAPI
API_URL = os.getenv("API_URL", "http://localhost:8000/chat")

st.set_page_config(page_title="SoleAgent Shoe Store", page_icon="👟")

# Initialize Cookie Manager

cookie_manager = stx.CookieManager()

st.title("👟 SoleAgent Store")

# Try to get the customer name from cookies
customer_name = cookie_manager.get(cookie="customer_name")

# ----------------------------------------
# NEW USER FLOW (No Cookie Found)
# ----------------------------------------
if not customer_name:
    st.write("Welcome to SoleAgent! To get started, please tell us your name:")
    
    with st.form("name_form"):
        name_input = st.text_input("Your Name:")
        submitted = st.form_submit_button("Save & Enter Store")
        
        if submitted and name_input:
            # Save name to cookie (lasts for 30 days)
            cookie_manager.set("customer_name", name_input, max_age=2592000)
            # Create a unique session ID for LangGraph memory and save to cookie
            cookie_manager.set("session_id", str(uuid.uuid4()), max_age=2592000)
            st.rerun()

# ----------------------------------------
# RETURNING USER FLOW (Cookie Found)
# ----------------------------------------
else:
    st.write(f"Welcome back, **{customer_name}**! 👋")
    session_id = cookie_manager.get(cookie="session_id")
    
    # NEW: Fallback if session_id is missing but name exists
    if not session_id:
        session_id = str(uuid.uuid4())
        cookie_manager.set("session_id", session_id, max_age=2592000)
            
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about stock or place an order..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Agent is checking..."):
            try:
                # We now pass the name and session ID to the API
                payload = {
                    "message": prompt,
                    "session_id": session_id,
                    "customer_name": customer_name
                }
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                ai_reply = response.json()["response"]
            except Exception as e:
                ai_reply = f"Error connecting to backend: {e}"

        with st.chat_message("assistant"):
            st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    if st.button("Sign Out (Clear Data)"):
        cookie_manager.delete("customer_name")
        cookie_manager.delete("session_id")
        st.session_state.messages = []
        st.rerun()

