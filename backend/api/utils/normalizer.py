import re

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\n", " ").strip()
    text = re.sub(r"\s+", " ", text)
    
    # Unicode normalize (ı, İ, etc.)
    text = text.replace("İ", "I").replace("ı", "i")

    return text
