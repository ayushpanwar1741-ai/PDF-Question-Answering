import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace
from pypdf import PdfReader

load_dotenv()

PDF_DIR = "data"
PERSIST_DIR = "chroma_db"

def load_pdf(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder,file))
            for i,page in enumerate(reader.pages,start = 1):
                text = page.extract_text() or ""
                docs.append({"source":file, "page": i, "text":text})
    return docs

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for d in docs:
        for c in splitter.split_text(d["text"]):
            chunks.append({**d,"chunk":c})
    return chunks

def build_db(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    texts = [c["chunk"] for c in chunks]
    metadatas = [{"source": c["source"], "page":c["page"]} for c in chunks]
    Chroma.form_texts(texts,embedding = embeddings, metadats=metadatas, persist_directory=PERSIST_DIR)
    
if __name__ == "__main__":
    docs = load_pdf(PDF_DIR)
    chunks = chunk_docs(docs)
    build_db(chunks)
    print(f"Done. {len(chunks)} chunks stored.")
    
    
                
