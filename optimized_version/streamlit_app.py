import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Geography Agent", page_icon="🌍")
st.title("🌍 Geography Study Assistant (Optimized)")
st.caption("Ask about NCERT Geography — retrieval-only tool, agent synthesizes answer")

if "messages" not in st.session_state:
    st.session_state.messages = []
   
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])   


if user_input := st.chat_input("Ask about geography..."):
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = run_agent(user_input)
    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    
    st.rerun()
