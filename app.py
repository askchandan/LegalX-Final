import os
from flask import Flask, render_template, request, jsonify, send_file
from modules.agent import get_agent_response
from modules.llm_manager import get_llm
from modules.memory import generate_transcript_file, generate_summarized_transcript_file

app = Flask(__name__)

chat_histories = {} 
SESSION_KEY = "user_1" # Default simple session 

@app.route('/')
def home():
    if SESSION_KEY not in chat_histories:
        chat_histories[SESSION_KEY] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_route():
    data = request.json
    user_query = data.get("message", "")
    
    if user_query.strip().lower() == "clear":
        chat_histories[SESSION_KEY] = []
        return jsonify({
            "response": "Chat memory has been securely wiped. How can I assist you with your new session?",
            "scrubbed_query": "clear",
            "clear_action": True
        })
        
    history = chat_histories.get(SESSION_KEY, [])
    
    # Process message through agent
    response, scrubbed_query = get_agent_response(user_query, history)
    
    # Update history
    history.append((user_query, response))
    chat_histories[SESSION_KEY] = history
    
    return jsonify({
        "response": response,
        "scrubbed_query": scrubbed_query
    })

@app.route('/download', methods=['GET'])
def download():
    history = chat_histories.get(SESSION_KEY, [])
    filepath = generate_transcript_file(history)
    return send_file(filepath, as_attachment=True, download_name="Secure_Transcript.txt")

@app.route('/summarize_download', methods=['POST'])
def summarize_download():
    """Generates an AI summary of the chat history using the llama3.1 LLM model and returns a txt file."""
    data = request.json
    history = chat_histories.get(SESSION_KEY, [])
    
    if not history:
        return jsonify({"error": "No chat history to summarize."}), 400
        
    # Build a plain text string to summarize
    chat_text = "\n".join([f"User: {u}\nAI: {a}" for u, a in history])
    prompt = f"Summarize the following legal consultation comprehensively in a few sentences:\n\n{chat_text}\n\nSummary:"
    
    llm = get_llm()
    if not llm:
        return jsonify({"error": "LLM unable to load for summarization."}), 500
        
    try:
        summary_text = llm.invoke(prompt)
    except Exception as e:
        return jsonify({"error": f"Summarization failed with model llama3.1. Please check Ollama."}), 500
        
    filepath = generate_summarized_transcript_file(history, summary_text)
    
    # Send simply a URL that they can ping via GET, or return path to be handled natively?
    # Better to return the payload and trigger download natively, or just serve it:
    return jsonify({"success": True})

@app.route('/get_summarized_file', methods=['GET'])
def get_summarized_file():
    # Helper to download the newly created file
    return send_file("summarized_transcript.txt", as_attachment=True, download_name="Summarized_Consultation.txt")


if __name__ == "__main__":
    # In order to allow dynamic modifications without restarting entirely, rely on the LLM Manager.
    app.run(debug=True, port=8000, host="0.0.0.0", use_reloader=False)
