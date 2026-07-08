import streamlit as st
from dotenv import load_dotenv
from core.session_manager import session_manager
from core.document_loader import load_documents, split_documents
from core.embeddings import get_embeddings
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP

load_dotenv()

st.set_page_config(page_title="RAG PDF Chatbot", page_icon="📄", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = session_manager.create_session()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("📁 Document Upload")
    uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "docx", "txt", "html", "htm"], accept_multiple_files=True)
    
    if uploaded_files:
        with st.spinner("Processing Documents..."):
            raw_docs = load_documents(uploaded_files)
            split_docs = split_documents(raw_docs)
            embeddings = get_embeddings()
            
            if session_manager.add_documents(st.session_state.session_id, split_docs):
                st.success(f"✅ Added {len(split_docs)} chunks from {len(uploaded_files)} Documents")
            else:
                st.error("❌ Failed to add documents")
    
    st.subheader("⚙️ Settings")
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.number_input("Chunk Size", value=CHUNK_SIZE)
    with col2:
        chunk_overlap = st.number_input("Chunk Overlap", value=CHUNK_OVERLAP)

# Main chat
st.header("💬 RAG Chatbot")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("Sources"):
                for idx, source in enumerate(message["sources"], 1):
                    st.markdown(f"**{idx}. {source['filename']} (Page {source['page']})**")
                    st.markdown(f"> {source['text_preview']}")

if prompt := st.chat_input("Ask a question about your Documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = session_manager.ask(st.session_state.session_id, prompt)
            
        answer = response.get("answer", "Error getting response.")
        sources = response.get("sources", [])
        
        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for idx, source in enumerate(sources, 1):
                    st.markdown(f"**{idx}. {source['filename']} (Page {source['page']})**")
                    st.markdown(f"> {source['text_preview']}")
                    
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

