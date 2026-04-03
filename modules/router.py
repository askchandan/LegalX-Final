import re

def classify_domain(query: str) -> str:
    """Zero-shot/Heuristic intent router to classify the specific category of crime."""
    text_lower = query.lower()
    if re.search(r'\b(cyber|internet|hack|computer|electronic|phishing|online)\b', text_lower):
        return "Cybercrime"
    elif re.search(r'\b(murder|kill|homicide|death|culpable|manslaughter)\b', text_lower):
        return "Killing"
    elif re.search(r'\b(theft|steal|robbery|extortion|dacoity|burglary)\b', text_lower):
        return "Theft"
    elif re.search(r'\b(fraud|cheat|forgery|deceit|counterfeit)\b', text_lower):
        return "Fraud"
    elif re.search(r'\b(assault|hurt|criminal force|kidnap|rape|abduct|battery)\b', text_lower):
        return "Assault"
    else:
        return "General"
