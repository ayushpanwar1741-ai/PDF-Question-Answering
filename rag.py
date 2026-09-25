from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

PERSIST_DIR = "chroma_db"
PROMPT = """"Answer using ONLY the context. If not there, say you don't know. cite the page.

context:
{context}

Question: {question}

Answer:"""

def ask(question):
    db = Chroma(persist_directory = PERSIST_DIR,embedding_function=HUggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
    docs = db.siilarity_search(question,k=4)
    context = "\n\n".join(
        f"[{d.metadata['source']} p.{d.metadata['page']}] {d.page_content}" for d in docs
    )
    
    prompt = PROMPT.format(context = context, question = question)
    llm = HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.2-1B-Instruct", temperature=0)
    return llm.invoke(prompt), docs
