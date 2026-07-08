import uuid
import os
import json
from typing import Dict, Optional
from langchain.schema import Document
from .vector_store import create_vectorstore, save_vectorstore, load_vectorstore
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
        try:
            uuid.UUID(session_id)
        except ValueError:
            return None

        # Check in memory
        session = self.sessions.get(session_id)
        if session:
            return session

        # Check if exists on disk
        from utils.config import DATA_DIR, VECTOR_DB_TYPE
        path_exists = False
        if VECTOR_DB_TYPE == "faiss":
            path = os.path.join(DATA_DIR, session_id)
            if os.path.exists(os.path.join(path, "index.faiss")):
                path_exists = True
        
        # Check metadata file
        metadata_path = os.path.join(DATA_DIR, f"{session_id}_metadata.json")
        if os.path.exists(metadata_path):
            path_exists = True

        if path_exists:
            self.sessions[session_id] = {
                "vectorstore": None,
                "qa_chain": None,
                "documents": [],
                "history": [],
            }
            session = self.sessions[session_id]

            # Load metadata
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        session["history"] = meta.get("history", [])
                        
                        reconstructed = []
                        for d in meta.get("documents", []):
                            if isinstance(d, dict) and "page_content" in d:
                                reconstructed.append(Document(page_content=d["page_content"], metadata=d.get("metadata", {})))
                            else:
                                reconstructed.append(d)
                        session["documents"] = reconstructed
                except Exception as e:
                    print(f"Error reading session metadata: {e}")

            # Reload vector store and build chain
            try:
                vectorstore = load_vectorstore(session_id, get_embeddings())
                session["vectorstore"] = vectorstore
                session["qa_chain"] = build_qa_chain(vectorstore)
            except Exception as e:
                print(f"Error rebuilding vector store session: {e}")
            
            return session

        return None

    def _save_metadata(self, session_id: str, session: dict):
        from utils.config import DATA_DIR
        metadata_path = os.path.join(DATA_DIR, f"{session_id}_metadata.json")
        serialized_docs = []
        for doc in session["documents"]:
            if hasattr(doc, "page_content"):
                serialized_docs.append({
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                })
            else:
                serialized_docs.append(doc)
        
        meta = {
            "history": session["history"],
            "documents": serialized_docs
        }
        try:
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error writing session metadata: {e}")

    def add_documents(self, session_id: str, documents):
        session = self.get_session(session_id)
        if not session:
            return False
        
        session["documents"].extend(documents)
        embeddings = get_embeddings()
        vectorstore = create_vectorstore(session["documents"], embeddings, session_id)
        session["vectorstore"] = vectorstore
        session["qa_chain"] = build_qa_chain(vectorstore)
        
        # Save vectorstore and metadata
        save_vectorstore(vectorstore, session_id)
        self._save_metadata(session_id, session)
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
        self._save_metadata(session_id, session)
        return {"answer": answer, "sources": sources}

session_manager = SessionManager()

