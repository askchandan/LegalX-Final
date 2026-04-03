<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&pause=1000&color=F72585&center=true&vCenter=true&width=600&lines=Domain-Adaptive+Legal+AI;Enterprise+LLM+Assistant;100%25+Offline+%26+Secure" alt="Animated Typing SVG" />
</p>

# ⚖️ Domain-Adaptive Legal AI

An enterprise-grade, offline-first conversational AI built to provide highly accurate Legal Information Retrieval using Retrieval-Augmented Generation (RAG). 

## 📸 Interface Preview


![Project Preview 1](./assets/image.png)

![Project Preview 2](./assets/image1.png)

## 🌟 Key Features

* **Strict Legal Grounding:** Custom prompt-engineered LLM specifically instructed to reject non-legal queries and focus solely on the provided legal context.
* **100% Offline Processing:** Designed to run entirely on your local machine using **Ollama (Llama 3.1)** and locally cached HuggingFace sentence-transformers. Zero API costs, zero data leakages.
* **Domain-Adaptive Routing:** Dynamically parses user queries through a zero-shot intent router to target the most highly relevant semantic `ChromaDB` indices (Cybercrime, Theft, Assault, etc.).
* **Presidio Secure Memory:** Automatically detects and scrubs PII (Phones, Emails, Names) from all user inputs prior to vector analysis to protect confidential client data.
* **Session Export:** Users can instantly download secure raw text transcripts of their session, or trigger the AI to synthesize an *Executive Legal Summary*.
* **Speed Optimized Instance:** The architecture is configured with aggressively constrained token generation predictions and dynamic connection caching for maximum response throughput.

## 🛠️ Architecture & Tech Stack

* **Backend Server:** Flask
* **Orchestration:** LangChain Ecosystem
* **Core LLM Inference:** Ollama
* **Vector Database:** ChromaDB
* **Front-end Concept:** Vanilla HTML/JS with Glassmorphism CSS Themes
* **Embeddings Engine:** `all-MiniLM-L6-v2` Local Offline Cache

## 📦 Dependencies

The project relies heavily on several key Python frameworks. Ensure these are installed via the `requirements.txt`:
* **`langchain` & `langchain-community`** (Orchestration & Tools)
* **`langchain-huggingface`** (Local Embedding Wrappers)
* **`chromadb`** (Vector Store for Legal RAG)
* **`presidio-analyzer` & `presidio-anonymizer`** (PII Scrubbing and Safety)
* **`sentence-transformers`** (Generating Vector Embeddings)
* **`Flask`** (Web Environment)
* **`spacy`** (English core language processing)

## 🚧 Limitations

1. **Local Resource Heavy:** Running LLMs locally requires a machine with significant RAM and a capable GPU for fast inference times. Slower machines will experience heavy latency.
2. **Context Scope:** The LLM's primary accuracy is limited entirely to the PDFs provided to the ChromaDB (IPC sections, specific crime documents). It cannot formulate exact legal strategies for crimes outside its ingested documentation.
3. **Web Search Deprecation:** The DuckDuckGo fallback agent may experience initialization limitations depending on rapid ping frequency and library updates.
4. **Not Legal Binding:** The AI provides legal *information*, not legal *counsel*. Output should be verified by a registered legal professional before real-world enforcement.

## 🚀 Execution Procedure

### 1. Prerequisites
- Python 3.9+ 
- [Ollama](https://ollama.com/) loaded with Llama 3.1 (`ollama run llama3.1`)

### 2. Environment Setup
```powershell
# Ensure your virtual environment is active, then install dependencies:
pip install -r requirements.txt

# Load spaCy's English core for the Presidio Anonymizer
python -m spacy download en_core_web_sm
```

### 3. Model Bootstrapping
You must download and securely cache the HuggingFace sentence-transformers exactly once so the system doesn't ping external networks.
```powershell
python setup_models.py
```

**(Optional) Initialize the Vector Database:**
If you have brand new PDF data to process into the vector chunks:
```powershell
python modules/ingest.py
```

### 4. Launch Enterprise Server
```powershell
python app.py
```
*Navigate to **`http://localhost:8000`** in a modern browser to interact with the Legal Assistant!*

## 🎯 Conclusion

The **Domain-Adaptive Legal AI** demonstrates that advanced, highly secure legal assistance can successfully run entirely air-gapped on local hardware. By combining powerful RAG techniques, rigorous zero-shot routing, and active memory scrubbing, it achieves high-fidelity context awareness while strictly maintaining user privacy, speed, and domain boundaries.
