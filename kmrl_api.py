from fastapi import FastAPI, UploadFile
from typing import List
import uvicorn
from services.ocr import extract_text
from services.nlp import summarize_text, detect_language

app = FastAPI()

@app.post("/process-doc/")
async def process_doc(files: List[UploadFile]):
    results = []

    for file in files:
        content = await file.read()

        # OCR or text decode
        text = extract_text(file, content)

        # Language detect
        lang = detect_language(text)

        # Summarization
        summary = summarize_text(text)

        results.append({
            "filename": file.filename,
            "language": lang,
            "summary": summary,
            "excerpt": text[:200]
        })

    return {"processed_docs": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
