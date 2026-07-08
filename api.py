import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

from core.session_manager import session_manager
from core.document_loader import load_documents, split_documents

app = FastAPI(title="RAG PDF Chatbot API")

class QuestionRequest(BaseModel):
    question: str

class Source(BaseModel):
    filename: str
    page: int | str
    text_preview: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]

class FakeFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content
        
    def getvalue(self) -> bytes:
        return self.content

@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    session_id = session_manager.create_session()
    
    fake_files = []
    for f in files:
        if f.filename and not f.filename.lower().endswith(('.pdf', '.docx', '.txt', '.html', '.htm')):
            raise HTTPException(status_code=400, detail="Unsupported file format.")
        content = await f.read()
        fake_files.append(FakeFile(f.filename or "unknown.txt", content))
        
    try:
        raw_docs = load_documents(fake_files)
        split_docs = split_documents(raw_docs)
        
        if session_manager.add_documents(session_id, split_docs):
            return {
                "session_id": session_id,
                "message": f"Successfully processed {len(files)} files into {len(split_docs)} chunks."
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add documents")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDFs: {str(e)}")

@app.post("/ask/{session_id}", response_model=AnswerResponse)
def ask_question(session_id: str, request: QuestionRequest):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    result = session_manager.ask(session_id, request.question)
    return result

@app.get("/session/{session_id}")
def get_session_info(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    return {
        "session_id": session_id,
        "history_length": len(session["history"]),
        "documents_loaded": len(session["documents"])
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
