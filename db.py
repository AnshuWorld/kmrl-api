from fastapi import FastAPI, UploadFile, HTTPException, Query
from typing import List
import uvicorn
from datetime import datetime

from services.ocr import extract_text
from services.nlp import summarize_text, detect_language, categorize_text
from services.utils import clean_text, truncate_text
from db import save_document, get_documents, search_documents

app = FastAPI(title="KMRL Document Processing API",
              description="OCR + NLP summarization + MongoDB storage + search",
              version="1.2.0")

@app.post("/process-doc/")
async def process_doc(files: List[UploadFile]):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    results = []

    for file in files:
        try:
            content = await file.read()

            # OCR or text decode
            text = extract_text(file, content)
            text = clean_text(text)

            if not text.strip():
                raise ValueError("No readable text found")

            # Language detection
            try:
                lang = detect_language(text)
            except Exception:
                lang = "unknown"

            # Summarization
            try:
                summary = summarize_text(text)
            except Exception:
                summary = "Summarization failed"

            # Category
            category = categorize_text(text)

            doc_data = {
                "filename": file.filename,
                "language": lang,
                "category": category,
                "summary": summary,
                "excerpt": truncate_text(text, 200),
                "full_text": text,
                "timestamp": datetime.utcnow()
            }

            doc_id = save_document(doc_data)
            doc_data["_id"] = doc_id

            results.append(doc_data)

        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})

    return {"processed_docs": results}


@app.get("/documents/")
async def list_documents(limit: int = 10):
    docs = get_documents(limit=limit)
    for d in docs:
        d["_id"] = str(d["_id"])
    return {"documents": docs}


@app.get("/search/")
async def search_docs(q: str = Query(..., min_length=2),
                      category: str = Query(None),
                      limit: int = 10):
    docs = search_documents(q, category, limit)
    for d in docs:
        d["_id"] = str(d["_id"])
    return {"query": q, "category": category, "results": docs}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
