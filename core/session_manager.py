import uuid
from typing import Dict, Optional
from .vector_store import create_vectorstore
from .embeddings import get_embeddings
from .rag_chain import build_qa_chain

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "vectorstore": None,
            "qa_chain": None,
            "documents": [],
            "history": [],
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        return self.sessions.get(session_id)

    def add_documents(self, session_id: str, documents):
        session = self.get_session(session_id)
        if not session:
            return False
        session["documents"].extend(documents)
        embeddings = get_embeddings()
        vectorstore = create_vectorstore(session["documents"], embeddings, session_id)
        session["vectorstore"] = vectorstore
        session["qa_chain"] = build_qa_chain(vectorstore)
        return True

    def ask(self, session_id: str, question: str) -> dict:
        session = self.get_session(session_id)
        if not session or not session["qa_chain"]:
            return {"answer": "No documents uploaded yet. Please upload a document.", "sources": []}
            
        result = session["qa_chain"].invoke({"query": question})
        answer = result["result"]
        
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append({
                    "filename": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", "Unknown"),
                    "text_preview": doc.page_content[:200] + "..."
                })
                
        session["history"].append((question, answer))
        return {"answer": answer, "sources": sources}

session_manager = SessionManager()
