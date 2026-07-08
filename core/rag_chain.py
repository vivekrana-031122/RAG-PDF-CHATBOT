from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from utils.config import LLM_MODEL, LLM_TEMPERATURE, TOP_K, OPENAI_API_KEY

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions based strictly on the provided context.
If the answer is not explicitly stated in the context, say "I don't know". Do not use external knowledge.

Context:
{context}

Question: {question}
Answer:"""

def build_qa_chain(vectorstore, llm_model=None, temperature=None, top_k=None):
    llm_model = llm_model or LLM_MODEL
    temperature = temperature if temperature is not None else LLM_TEMPERATURE
    top_k = top_k or TOP_K

    prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    llm = ChatOpenAI(model=llm_model, temperature=temperature, openai_api_key=OPENAI_API_KEY)

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
