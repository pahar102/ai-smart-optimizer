import spacy
import nltk
from nltk.tokenize import sent_tokenize
import hashlib

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

def compress_prompt(prompt):
    doc = nlp(prompt)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(keywords[:30])

def detect_intent(prompt):
    sentences = sent_tokenize(prompt)
    if any("how" in s.lower() or "explain" in s.lower() for s in sentences):
        return "Explanation"
    elif any("write" in s.lower() or "generate" in s.lower() for s in sentences):
        return "Content Generation"
    return "General"

def fingerprint(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()
  
