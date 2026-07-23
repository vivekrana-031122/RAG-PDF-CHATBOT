import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from utils.config import LLM_MODEL, LLM_TEMPERATURE, TOP_K

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions based strictly on the provided context.
If the answer is not explicitly stated in the context, say "I don't know". Do not use external knowledge.

Context:
{context}

Question: {question}
Answer:"""

class LCELChainWrapper:
    def __init__(self, retriever, llm_chain):
        self.retriever = retriever
        self.llm_chain = llm_chain

    def invoke(self, inputs):
        question = inputs.get("query", "")
        docs = self.retriever.invoke(question)
        context_str = "\n\n".join(doc.page_content for doc in docs)
        
        answer = self.llm_chain.invoke({
            "context": context_str,
            "question": question
        })
        
        return {
            "result": answer,
            "source_documents": docs
        }

def build_qa_chain(vectorstore, llm_model=None, temperature=None, top_k=None):
    llm_model = llm_model or LLM_MODEL
    temperature = temperature if temperature is not None else LLM_TEMPERATURE
    top_k = top_k or TOP_K

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    load_dotenv(override=True)
    groq_key = os.getenv("GROQ_API_KEY")
    
    llm = ChatGroq(
        model=llm_model, 
        temperature=temperature, 
        api_key=groq_key
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    llm_chain = prompt | llm | StrOutputParser()
    
    return LCELChainWrapper(retriever, llm_chain)
