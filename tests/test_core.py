import os
from unittest.mock import patch, MagicMock
from core.session_manager import session_manager
from core.document_loader import load_documents

class FakeFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content
    def getvalue(self):
        return self.content

def test_pdf_loading():
    sample_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(sample_path, "rb") as f:
        content = f.read()
    
    fake_file = FakeFile("sample.pdf", content)
    docs = load_documents([fake_file])
    
    assert len(docs) > 0
    assert "page" in docs[0].metadata
    assert "source" in docs[0].metadata
    assert docs[0].metadata["source"] == "sample.pdf"

@patch("core.session_manager.get_embeddings")
@patch("core.session_manager.create_vectorstore")
@patch("core.session_manager.build_qa_chain")
def test_session_manager_flow(mock_build, mock_create_vs, mock_get_emb):
    mock_qa_chain = MagicMock()
    mock_qa_chain.invoke.return_value = {
        "result": "This is a mock answer.",
        "source_documents": []
    }
    mock_build.return_value = mock_qa_chain
    
    session_id = session_manager.create_session()
    assert session_id in session_manager.sessions
    
    session = session_manager.get_session(session_id)
    assert session is not None
    assert session["history"] == []
    
    success = session_manager.add_documents(session_id, [{"page_content": "dummy", "metadata": {}}])
    assert success is True
    assert len(session["documents"]) == 1
    
    res = session_manager.ask(session_id, "Hello?")
    assert res["answer"] == "This is a mock answer."
    assert len(res["sources"]) == 0
    assert len(session["history"]) == 1
