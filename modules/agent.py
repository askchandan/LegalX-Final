import logging
from modules.prompts import SYSTEM_PROMPT
from modules.memory import scrub_pii
from modules.tools import rag_search_tool, legal_web_search
from modules.llm_manager import get_llm

logging.basicConfig(level=logging.INFO)

def get_agent_response(user_query: str, chat_history: list) -> tuple:
    """Main Orchestration flow hardcoded to llama3.1."""
    # 1. Scrub PII from secure memory perspective
    scrubbed_query = scrub_pii(user_query)
    if scrubbed_query != user_query:
        logging.info("[Agent] Notice: Sensitive Information (PII) detected and redacted.")
    
    # 2. Extract evidence using RAG and fallback
    rag_context = rag_search_tool.run(scrubbed_query)
    
    if "No strictly relevant" in rag_context:
        web_context = legal_web_search.run(scrubbed_query)
        context = f"[Live Web Search context fallback]\n{web_context}"
    else:
        context = f"[Internal Enterprise DB Results]\n{rag_context}"
    
    # 3. Format history for prompting
    history_str = ""
    for role, act in chat_history[-2:]:
        history_str += f"{role}: {act}\n"
        
    formatted_prompt = SYSTEM_PROMPT.format(
        context=context,
        history=history_str,
        user_query=scrubbed_query
    )
    
    # 4. Invoke LLM
    llm = get_llm()
    if llm:
        try:
            response = llm.invoke(formatted_prompt)
        except Exception as e:
            response = f"I encountered an error connecting to my core processing engine (llama3.1). Please ensure Ollama is running locally."
            logging.error(e)
    else:
         response = "System configuration error. Dynamic LLM Provider is unavailable."
         
    return response, scrubbed_query
