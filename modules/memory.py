import os
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Ensure PII protection globally
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def scrub_pii(text: str) -> str:
    """Detects and scrubs sensitive PII markers from the text to ensure secure memory usage."""
    results = analyzer.analyze(text=text, entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"], language='en')
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized_text.text

def generate_transcript_file(history: list, filename="chat_transcript.txt") -> str:
    """Generates a downloadable text transcript of the user's secure memory session without summary."""
    content = "--- Enterprise Legal Assistant Chat Transcript ---\n\n"
    if not history:
        content += "No messages yet.\n"
    else:
        for user_msg, bot_msg in history:
            content += f"User: {user_msg}\n"
            content += f"Assistant: {bot_msg}\n\n"
            
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def generate_summarized_transcript_file(history: list, summary: str, filename="summarized_transcript.txt") -> str:
    """Generates a downloadable text transcript alongside an AI-generated session summary."""
    content = "--- Enterprise Legal Consultation Summary ---\n\n"
    content += f"EXECUTIVE SUMMARY:\n{summary}\n\n"
    content += "=================================================\n\n"
    content += "--- Detailed Transcript ---\n\n"
    
    if not history:
        content += "No messages yet.\n"
    else:
        for user_msg, bot_msg in history:
            content += f"User: {user_msg}\n"
            content += f"Assistant: {bot_msg}\n\n"
            
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename
