import os
from dotenv import load_dotenv

# Load API keys from .env if present
load_dotenv() 

# Embedding Settings
# Explicitly use the physical local copy inside models folder
EMBEDDING_MODEL = "./models/all-MiniLM-L6-v2"

# Vector DB Settings
DB_DIR = "./chroma_db"
COLLECTIONS = ["Killing", "Theft", "Cybercrime", "Fraud", "Assault", "General"]

# LLM Selection (Easily modularized for swapping)
# Options: "ollama", "gemini", "groq", "openai"
LLM_PROVIDER = "ollama"  
OLLAMA_MODEL = "llama3.1"
