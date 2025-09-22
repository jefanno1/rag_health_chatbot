# app.py
import streamlit as st
from rag_api import answer_question  # pakai langsung dari rag_api.py

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG Chatbot for Diabetes Articles")
st.write("Ask anything related to diabetes research")

# Simpan riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat lama
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input user
if prompt := st.chat_input("Write Your Question..."):
    # Tambahkan pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Panggil pipeline RAG
    with st.chat_message("assistant"):
        with st.spinner("Generating Answer"):
            answer = answer_question(prompt, top_k=5, max_context_tokens=8000)
            st.markdown(answer)

    # Simpan jawaban ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": answer})
