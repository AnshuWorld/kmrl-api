import pytesseract
from PIL import Image
import io

def extract_text(file, content):
    try:
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image, lang="eng+mal")
    except Exception:
        return content.decode("utf-8", errors="ignore")
