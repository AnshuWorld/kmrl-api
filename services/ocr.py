import pytesseract
from PIL import Image
import io
from services.utils import safe_decode

def extract_text(file, content):
    try:
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image, lang="eng+mal")
    except Exception:
        return safe_decode(content)
