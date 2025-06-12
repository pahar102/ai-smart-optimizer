import spacy
import nltk
from nltk.tokenize import sent_tokenize
import hashlib
from tinydb import TinyDB
import time

# Setup
nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")
db = TinyDB("log.json")  # saves usage data here

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

def adapt_for_model(prompt, model_name):
    if "claude" in model_name.lower():
        return f"Human: {prompt}\nAssistant:"
    elif "mistral" in model_name.lower():
        return f"<s>[INST] {prompt} [/INST]"
    else:  # default GPT style
        return f"{prompt}\n"

def generate_report(original, optimized):
    original_tokens = len(original.split())
    optimized_tokens = len(optimized.split())
    saved = original_tokens - optimized_tokens
    percent = (saved / original_tokens) * 100 if original_tokens > 0 else 0
    return {
        "original_tokens": original_tokens,
        "optimized_tokens": optimized_tokens,
        "tokens_saved": saved,
        "savings_percent": round(percent, 2)
    }

def log_usage(data):
    data["timestamp"] = time.time()
    db.insert(data)
    
