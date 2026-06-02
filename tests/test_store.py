from voiceops_rag.store import VectorStore

def test_add_and_query_returns_nearest(tmp_path):
    store = VectorStore(path=str(tmp_path / "db"), collection="test")
    store.reset()
    store.add(
        ids=["a", "b"],
        embeddings=[[1.0, 0.0], [0.0, 1.0]],
        documents=["alpha doc", "beta doc"],
        metadatas=[{"source_file": "a.md", "title": "Alpha"},
                   {"source_file": "b.md", "title": "Beta"}],
    )
    hits = store.query(embedding=[0.95, 0.05], k=1)
    assert len(hits) == 1
    assert hits[0]["id"] == "a"
    assert hits[0]["document"] == "alpha doc"
    assert hits[0]["metadata"]["title"] == "Alpha"
    assert hits[0]["score"] > 0.8
