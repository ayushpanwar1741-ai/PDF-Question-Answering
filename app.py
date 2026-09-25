import streamlit as st
from rag import ask

st.title("📄 PDF Question Answering (Hugging Face)")
question = st.text_input("Ask a question about you PDF")
if st.button("Ask") and question:
    answer,docs = ask(question)
    st.markdown("###💬 Answer")
    st.write(answer)
    st.markdown("###📚 Sources")
    for d in docs:
        st.write(f":- {d.metadata['source']} (page{d.metadata['page']})")