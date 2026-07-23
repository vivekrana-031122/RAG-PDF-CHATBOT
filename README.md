# RAG PDF Chatbot

A production-ready Retrieval-Augmented Generation (RAG) system running a Streamlit UI frontend and a FastAPI REST API backend. 

## Features
- **Dual Interface:** Chat through the beautiful Streamlit wrapper, or interact programmatically via REST `/ask`.
- **Source Tracking:** The bot returns the exact filename and page number it used to synthesize the answer.
- **Persistent Vectors:** Embeddings are cached to FAISS locally.

## Local Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Add OpenAI Key:**
   Rename `.env.example` to `.env` and paste your `OPENAI_API_KEY`.

3. **Run the API Backend:**
   ```bash
   uvicorn api:app --reload
   ```
   *Available at `http://localhost:8000/docs`*

4. **Run the Streamlit UI:**
   ```bash
   streamlit run app.py
   ```
   *Available at `http://localhost:8501`*

## 🧪 Testing

We use `pytest` for automated testing. To run the integration and unit tests:
```bash
pytest tests/
```

## 🐳 Docker Deployment

The application is fully containerized using a dual-container `docker-compose.yml` orchestrating both the FastAPI and Streamlit services. 

1. Ensure your `.env` contains your `OPENAI_API_KEY`.
2. Run Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
3. **Streamlit UI** will be available at port `8501`.
4. **FastAPI Docs** will be available at port `8000`.

### Deploying to Render / Railway
Both platforms support deploying straight from the GitHub repo using `docker-compose`. Simply connect your repository, configure the deployment to use `docker-compose.yml`, and inject `OPENAI_API_KEY` into your environment secrets.

### Deploying to Hugging Face Spaces
If you only want to showcase the UI, you can deploy the Streamlit app to Hugging Face Spaces using the `Dockerfile.ui` or native Streamlit app settings.

## Folder Structure
- `app.py`: Streamlit frontend application.
- `api.py`: FastAPI REST endpoint application.
- `core/`: RAG pipelines, session memory, and LLM chains.
- `tests/`: Automated unit and integration testing suite.
