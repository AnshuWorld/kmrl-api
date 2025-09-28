from transformers import pipeline
from langdetect import detect

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Simple category classification based on keywords
CATEGORY_KEYWORDS = {
    "HR": ["training", "employee", "payroll", "leave", "HR", "staff"],
    "Finance": ["invoice", "payment", "budget", "finance", "contract"],
    "Safety": ["safety", "accident", "incident", "hazard", "bulletin"],
    "Engineering": ["design", "maintenance", "engineering", "drawing", "specs"]
}

def summarize_text(text: str) -> str:
    if len(text.strip()) == 0:
        return "No text detected"
    return summarizer(text[:1000], max_length=120, min_length=30, do_sample=False)[0]["summary_text"]

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"

def categorize_text(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in text_lower for word in keywords):
            return category
    return "General"
