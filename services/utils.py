import chardet

def safe_decode(content: bytes) -> str:
    try:
        detected = chardet.detect(content)
        encoding = detected.get("encoding", "utf-8")
        return content.decode(encoding, errors="ignore")
    except Exception:
        return content.decode("utf-8", errors="ignore")


def clean_text(text: str) -> str:
    return " ".join(text.split())


def truncate_text(text: str, limit: int = 200) -> str:
    return text[:limit] + ("..." if len(text) > limit else "")
