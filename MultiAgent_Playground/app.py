import streamlit as st
from agents import MasterAgent

# ✅ Your Tomorrow.io API key
API_KEY = "2slvmbzX3bokTimnOQmJlwncqLbZjWPm"
master = MasterAgent(API_KEY)

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Options")

# Clear chat button
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat cleared! 👋"}
    ]

# Download chat button
if "messages" in st.session_state and len(st.session_state.messages) > 0:
    chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
    st.sidebar.download_button(
        label="⬇️ Download Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# ---------------- Main UI ----------------
st.title("🤖 Multi-Agent Chatbot")
st.caption("Ask me to calculate, check weather, manipulate text, or even general knowledge (LLM fallback).")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me something 👇"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your query..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response from MasterAgent
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = master.perform_task(prompt)
        st.markdown(response)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
