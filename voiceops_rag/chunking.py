def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if size <= overlap:
        raise ValueError("size must be greater than overlap")
    chunks = []
    start = 0
    step = size - overlap
    while start < len(text):
        chunks.append(text[start:start + size])
        start += step
    return chunks
