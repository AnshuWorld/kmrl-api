# services/nlp.py
from transformers import pipeline

# Summarizer already exists
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Simple classifier placeholder (can be replaced with fine-tuned model later)
CATEGORY_KEYWORDS = {
    "HR": ["training", "employee", "payroll", "leave", "HR", "staff"],
    "Finance": ["invoice", "payment", "budget", "finance", "contract"],
    "Safety": ["safety", "accident", "incident", "hazard", "bulletin"],
    "Engineering": ["design", "maintenance", "engineering", "drawing", "specs"]
}

def categorize_text(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in text_lower for word in keywords):
            return category
    return "General"
