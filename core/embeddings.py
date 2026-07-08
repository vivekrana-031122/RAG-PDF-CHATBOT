from langchain_openai import OpenAIEmbeddings
from utils.config import EMBEDDING_MODEL, OPENAI_API_KEY

def get_embeddings():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
