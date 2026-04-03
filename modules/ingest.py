import os
# Force entirely offline mode
os.environ["HF_HUB_OFFLINE"] = "1"

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from modules.config import EMBEDDING_MODEL, DB_DIR, COLLECTIONS
from modules.router import classify_domain

# Define paths
PDF_1 = "data/Cyber Crimes Offenses & Penalties In India[1].pdf"
PDF_2 = "data/ipc_sections_formatted.pdf"

def ingest():
    print("Loading documents...")
    docs = []
    
    if os.path.exists(PDF_1):
        docs.extend(PyPDFLoader(PDF_1).load())
    if os.path.exists(PDF_2):
        docs.extend(PyPDFLoader(PDF_2).load())

    print(f"Loaded {len(docs)} pages/documents.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    print(f"Split into {len(chunks)} chunks. Categorizing...")

    categorized_chunks = {k: [] for k in COLLECTIONS}

    for chunk in chunks:
        cat = classify_domain(chunk.page_content)
        categorized_chunks[cat].append(chunk)

    print(f"Initializing embeddings safely from completely local directory {EMBEDDING_MODEL}...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    except Exception as e:
        print(f"Error loading local model (Run setup_models.py first!). Details: {e}")
        return

    for cat, cat_chunks in categorized_chunks.items():
        if cat_chunks:
            print(f"Ingesting {len(cat_chunks)} chunks into collection '{cat}'...")
            Chroma.from_documents(
                documents=cat_chunks,
                embedding=embeddings,
                collection_name=cat,
                persist_directory=DB_DIR
            )
            print(f"Saved {cat} to {DB_DIR}")

    print("Ingestion complete. Vector DB relies only on the local ./models pipeline.")

if __name__ == "__main__":
    ingest()
