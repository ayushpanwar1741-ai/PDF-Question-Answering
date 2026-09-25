import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

load_dotenv()

PERSIST_DIR = "chroma_db"
PROMPT = """"Answer using ONLY the context. If not there, say you don't know. cite the page.

context:
{context}

Question: {question}

Answer:"""

def ask(question):
    db = Chroma(persist_directory = PERSIST_DIR,embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
    docs = db.similarity_search(question,k=4)
    context = "\n\n".join(
        f"[{d.metadata['source']} p.{d.metadata['page']}] {d.page_content}" for d in docs
    )
    
    prompt = PROMPT.format(context = context, question = question)
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        temperature=0,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"),
    )
    llm = ChatHuggingFace(llm=endpoint)
    return llm.invoke(prompt).content, docs


