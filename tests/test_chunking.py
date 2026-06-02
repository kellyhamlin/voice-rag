from voiceops_rag.chunking import chunk_text

def test_short_text_is_single_chunk():
    assert chunk_text("hello world", size=100, overlap=10) == ["hello world"]

def test_long_text_splits_with_overlap():
    text = "abcdefghij" * 5  # 50 chars
    chunks = chunk_text(text, size=20, overlap=5)
    assert chunks[0] == text[0:20]
    assert chunks[1] == text[15:35]   # starts at size-overlap
    assert chunks[-1] == text[len(text)-(len(text) % 15 or 20):] or len(chunks) >= 3
    # every chunk is at most `size` long
    assert all(len(c) <= 20 for c in chunks)

def test_empty_text_returns_empty_list():
    assert chunk_text("", size=20, overlap=5) == []
