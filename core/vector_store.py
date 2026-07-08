import os
import uuid
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from utils.config import DATA_DIR, VECTOR_DB_TYPE, PINECONE_API_KEY

def validate_session_id(session_id: str):
    try:
        uuid.UUID(session_id)
    except ValueError:
        raise ValueError("Security Alert: Invalid session ID format. Action blocked.")

def create_vectorstore(documents: List[Document], embeddings, session_id: str):
    validate_session_id(session_id)
    if VECTOR_DB_TYPE == "pinecone":
        index_name = "rag-chatbot-index"
        return PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name, namespace=session_id)
    else:
        return FAISS.from_documents(documents, embeddings)

def save_vectorstore(vectorstore, session_id: str):
    validate_session_id(session_id)
    if VECTOR_DB_TYPE == "faiss":
        path = os.path.join(DATA_DIR, session_id)
        vectorstore.save_local(path)
        return path
    return None

def load_vectorstore(session_id: str, embeddings):
    validate_session_id(session_id)
    if VECTOR_DB_TYPE == "pinecone":
        index_name = "rag-chatbot-index"
        return PineconeVectorStore.from_existing_index(index_name, embeddings, namespace=session_id)
    else:
        path = os.path.join(DATA_DIR, session_id)
        # Note: allow_dangerous_deserialization is required for loading pickled FAISS databases from LangChain.
        # We mitigate the security risk by strictly validating the session_id format to prevent path traversal.
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

