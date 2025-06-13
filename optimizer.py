import spacy
import nltk
from nltk.tokenize import sent_tokenize
import hashlib

# ✅ Punkt downloader with safe check
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# ✅ Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ✅ Compress prompt: removes stop words and keeps important tokens
def compress_prompt(prompt):
    if not prompt:
        return ""
    doc = nlp(prompt)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(keywords[:30])

# ✅ Detect intent: simple heuristic-based classification
def detect_intent(prompt):
    if not prompt:
        return "Unknown"
    sentences = sent_tokenize(prompt)
    if any("how" in s.lower() or "explain" in s.lower() for s in sentences):
        return "Explanation"
    elif any("write" in s.lower() or "generate" in s.lower() for s in sentences):
        return "Content Generation"
    return "General"

# ✅ Generate unique fingerprint using SHA-256
def fingerprint(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest() if prompt else ""
    
