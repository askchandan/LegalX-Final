import os
# Force huggingface library into entirely offline mode so it stops forcing HEAD checks that terminate the client
os.environ["HF_HUB_OFFLINE"] = "1"

from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
from modules.config import EMBEDDING_MODEL, DB_DIR
from modules.router import classify_domain

# Initialize purely from local physical folder
try:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
except Exception as e:
    print(f"Failed to load local embeddings. Please run `python setup_models.py` first. Error: {e}")
    embeddings = None

def get_chroma_collection(collection_name):
    """Loads a specific Vector Database collection dynamically."""
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )

@tool
def rag_search_tool(query: str) -> str:
    """Searches the appropriate Legal Vector Database for relevant sections based on classified domain."""
    domain = classify_domain(query)
    print(f"[Agent] Router classified domain as: {domain}")
    try:
        db = get_chroma_collection(domain)
        docs = db.similarity_search(query, k=3)
        if docs:
            return "\n".join([f"Source: {domain} DB\n" + d.page_content for d in docs])
        return "No strictly relevant legal context found in the database for this domain."
    except Exception as e:
        return f"Database error for domain {domain}: {str(e)}"

# Setup external search tool safely mapped
try:
    web_search = DuckDuckGoSearchRun()
except Exception as e:
    web_search = None
    print(f"Warning: DuckDuckGo initialization failed ({e}). Proceeding without web search.")

@tool
def legal_web_search(query: str) -> str:
    """Fallback search tool to look up general legal information on the web."""
    if web_search:
        try:
            return web_search.run(query)
        except Exception as e:
            return f"Web search failed: {str(e)}"
    return "Web search is currently unavailable."
