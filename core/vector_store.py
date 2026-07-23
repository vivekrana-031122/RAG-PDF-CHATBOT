import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from utils.config import DATA_DIR, VECTOR_DB_TYPE, PINECONE_API_KEY

def create_vectorstore(documents: List[Document], embeddings, session_id: str):
    if VECTOR_DB_TYPE == "pinecone":
        from pinecone import Pinecone
        from langchain_community.vectorstores import Pinecone as PineconeVectorStore
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index_name = "rag-chatbot-index"
        return PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name, namespace=session_id)
    else:
        return FAISS.from_documents(documents, embeddings)

def save_vectorstore(vectorstore, session_id: str):
    if VECTOR_DB_TYPE == "faiss":
        path = os.path.join(DATA_DIR, session_id)
        vectorstore.save_local(path)
        return path
    return None

def load_vectorstore(session_id: str, embeddings):
    if VECTOR_DB_TYPE == "pinecone":
        from langchain_community.vectorstores import Pinecone as PineconeVectorStore
        index_name = "rag-chatbot-index"
        return PineconeVectorStore.from_existing_index(index_name, embeddings, namespace=session_id)
    else:
        path = os.path.join(DATA_DIR, session_id)
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
