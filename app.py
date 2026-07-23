import streamlit as st
from dotenv import load_dotenv
import os
import time

from core.document_loader import load_documents, split_documents
from core.embeddings import get_embeddings
from core.vector_store import create_vectorstore
from core.rag_chain import build_qa_chain
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, LLM_MODEL, LLM_TEMPERATURE

load_dotenv()

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="AI Doc Chat", page_icon="✨", layout="wide")

# ========== CUSTOM CSS – ANIMATED, GLASS, ELEGANT ==========
st.markdown("""
<style>
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Animated gradient background targeting the exact root Streamlit element */
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f172a) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* True Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.5) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Login Form & Other standard containers */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
        padding: 2.5rem !important;
        transition: all 0.3s ease !important;
    }

    /* Buttons */
    [data-testid="stFormSubmitButton"] button, [data-testid="stBaseButton-primary"] button, button[kind="primary"] {
        background: linear-gradient(135deg, #ff6ac4, #8a2387) !important;
        border: none !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="stFormSubmitButton"] button:hover, [data-testid="stBaseButton-primary"] button:hover, button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 106, 196, 0.5) !important;
    }
    
    /* Standard outline buttons (Logout/Clear) */
    [data-testid="stBaseButton-secondary"] button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stBaseButton-secondary"] button:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: #ff6ac4 !important;
        transform: translateY(-2px) !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: rgba(15, 12, 41, 0.8) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.4) !important;
        backdrop-filter: blur(15px) !important;
        padding: 0.5rem !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }

    /* Native Chat wrappers */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Custom inner message bubbles */
    .user-message, .assistant-message {
        padding: 1.2rem;
        border-radius: 20px;
        margin-bottom: 0.5rem;
        animation: fadeInUp 0.4s ease-out;
        color: white !important;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background: linear-gradient(135deg, rgba(0, 150, 255, 0.15), rgba(0, 255, 255, 0.15));
        border-left: 4px solid #00E5FF;
        border-top-right-radius: 5px;
    }
    .assistant-message {
        background: linear-gradient(135deg, rgba(138, 35, 135, 0.15), rgba(255, 106, 196, 0.15));
        border-left: 4px solid #ff6ac4;
        border-top-left-radius: 5px;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Title and text visibility */
    h1, h2, h3, p, label {
        color: #F8FAFC !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Text Inputs (Username/Password/Chunk overrides) */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #ff6ac4 !important;
        box-shadow: 0 0 10px rgba(255, 106, 196, 0.3) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 106, 196, 0.5);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #ff6ac4;
    }
</style>
""", unsafe_allow_html=True)

# ========== LOGIN SYSTEM (Simple Session State) ==========
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.markdown("<h1 style='text-align: center;'>✨ Welcome to AI Doc Chat ✨</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Login to chat with your documents</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="••••••")
                submit = st.form_submit_button("🔐 Login", use_container_width=True)
                if submit:
                    # Simple demo auth
                    if username and password:
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Please enter both username and password")
        st.stop()

check_login()

# ========== MAIN CHAT UI (After Login) ==========
st.title("🤖 AI Doc Chat")
st.markdown("<p style='margin-top:-20px;'>Upload documents & ask anything – answers with sources</p>", unsafe_allow_html=True)

# Sidebar – file upload and settings
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.markdown("## ⚙️ Settings")
    model = st.selectbox("LLM Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"], index=1)
    temperature = st.slider("Temperature", 0.0, 1.0, LLM_TEMPERATURE, 0.05)
    top_k = st.slider("Top K", 1, 10, TOP_K)
    chunk_size = st.number_input("Chunk Size", 500, 2000, CHUNK_SIZE)
    chunk_overlap = st.number_input("Chunk Overlap", 0, 500, CHUNK_OVERLAP)
    
    st.divider()
    st.markdown("## 📂 Upload Documents")
    uploaded_files = st.file_uploader(
        "PDF, DOCX, TXT, HTML", type=["pdf","docx","txt","html"], accept_multiple_files=True
    )
    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary", use_container_width=True):
            with st.spinner("Indexing..."):
                docs = load_documents(uploaded_files)
                chunks = split_documents(docs, chunk_size, chunk_overlap)
                embeddings = get_embeddings()
                
                # Our vector_store.create_vectorstore implementation expects 3 arguments: documents, embeddings, session_id
                # Providing a default generic session_id since we bypassed session_manager
                session_id = "default-ui-session" 
                vectorstore = create_vectorstore(chunks, embeddings, session_id)
                qa_chain = build_qa_chain(vectorstore, model, temperature, top_k)
                
                st.session_state.vectorstore = vectorstore
                st.session_state.qa_chain = qa_chain
                st.session_state.chunks = chunks
                st.success(f"✅ {len(uploaded_files)} file(s) → {len(chunks)} chunks")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# Display chat history with custom styling
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 Sources"):
                for src in msg["sources"]:
                    st.markdown(f"**{src['filename']}** (p.{src['page']}) – *{src['text_preview'][:100]}...*")

# Chat input
if prompt := st.chat_input("Ask anything..."):
    if st.session_state.qa_chain is None:
        st.error("Please upload and process documents first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.qa_chain.invoke({"query": prompt})
                    answer = result["result"]
                    sources = []
                    if "source_documents" in result:
                        for doc in result["source_documents"]:
                            sources.append({
                                "filename": doc.metadata.get("source", "unknown"),
                                "page": doc.metadata.get("page", "?"),
                                "text_preview": doc.page_content[:200]
                            })
                    st.markdown(f"<div class='assistant-message'>{answer}</div>", unsafe_allow_html=True)
                    if sources:
                        with st.expander("📚 Sources"):
                            for src in sources:
                                st.markdown(f"**{src['filename']}** (p.{src['page']}) – *{src['text_preview']}...*")
                except Exception as e:
                    st.error(f"Error: {e}")
                    answer = "Sorry, an error occurred."
        
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources if 'sources' in locals() else []})
