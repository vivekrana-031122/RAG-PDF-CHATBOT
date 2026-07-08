import os
import tempfile
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredHTMLLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP

def load_document(uploaded_file) -> List[Document]:
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
        
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(tmp_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(tmp_path)
        elif ext == ".txt":
            loader = TextLoader(tmp_path, encoding='utf-8')
        elif ext in [".html", ".htm"]:
            loader = UnstructuredHTMLLoader(tmp_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
            
        documents = loader.load()
        for doc in documents:
            doc.metadata["source"] = filename
            if ext == ".pdf" and "page" in doc.metadata:
                doc.metadata["page"] += 1
            if "page" not in doc.metadata:
                doc.metadata["page"] = 1 # Fallback for formats without native paging
    finally:
        os.unlink(tmp_path)
        
    return documents

def load_documents(uploaded_files) -> List[Document]:
    all_docs = []
    for file in uploaded_files:
        all_docs.extend(load_document(file))
    return all_docs

def split_documents(documents: List[Document],
                    chunk_size: int = CHUNK_SIZE,
                    chunk_overlap: int = CHUNK_OVERLAP) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    return text_splitter.split_documents(documents)
