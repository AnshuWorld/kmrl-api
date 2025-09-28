from transformers import pipeline
from langdetect import detect

# Load summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    if len(text.strip()) == 0:
        return "No text detected"
    return summarizer(text[:1000], max_length=120, min_length=30, do_sample=False)[0]["summary_text"]

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"
