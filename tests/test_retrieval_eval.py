# tests/test_retrieval_eval.py
from voiceops_rag.store import VectorStore

# Deterministic 3-dim "embeddings": each doc owns one axis; queries lean toward one.
DOCS = {
    "one-way-audio.md": ([1.0, 0.0, 0.0], "RTP one-way audio NAT codec"),
    "sip-503.md":       ([0.0, 1.0, 0.0], "SIP 503 overload trunk channels"),
    "registration.md":  ([0.0, 0.0, 1.0], "REGISTER 401 403 credentials realm"),
}
EVAL = [
    ([0.9, 0.1, 0.0], "one-way-audio.md"),
    ([0.1, 0.9, 0.0], "sip-503.md"),
    ([0.0, 0.1, 0.9], "registration.md"),
]

def test_expected_source_in_top_k(tmp_path):
    store = VectorStore(path=str(tmp_path / "db"), collection="eval")
    store.reset()
    store.add(
        ids=list(DOCS.keys()),
        embeddings=[v for v, _ in DOCS.values()],
        documents=[d for _, d in DOCS.values()],
        metadatas=[{"source_file": k, "title": k} for k in DOCS],
    )
    for query_vec, expected in EVAL:
        hits = store.query(embedding=query_vec, k=2)
        assert expected in [h["id"] for h in hits], f"{expected} not retrieved"
