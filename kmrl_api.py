from fastapi import FastAPI, UploadFile, HTTPException
from typing import List
import uvicorn

from services.ocr import extract_text
from services.nlp import summarize_text, detect_language
from services.utils import clean_text, truncate_text

app = FastAPI(title="KMRL Document Processing API",
              description="OCR + NLP summarization + multilingual support",
              version="1.0.0")

@app.post("/process-doc/")
async def process_doc(files: List[UploadFile]):
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files uploaded")

    results = []

    for file in files:
        try:
            content = await file.read()

            # OCR or text decode
            text = extract_text(file, content)
            text = clean_text(text)

            if not text.strip():
                raise ValueError("No readable text found in document")

            # Language detection (safe fallback)
            try:
                lang = detect_language(text)
            except Exception:
                lang = "unknown"

            # Summarization (safe fallback)
            try:
                summary = summarize_text(text)
            except Exception:
                summary = "Summarization failed"

            results.append({
                "filename": file.filename,
                "language": lang,
                "summary": summary,
                "excerpt": truncate_text(text, 200)
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })

    return {"processed_docs": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
