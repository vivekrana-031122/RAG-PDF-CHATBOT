import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from utils.config import EMBEDDING_MODEL

def get_embeddings():
    load_dotenv(override=True)
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
