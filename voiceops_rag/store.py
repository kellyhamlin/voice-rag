import chromadb

class VectorStore:
    def __init__(self, path: str, collection: str = "voiceops"):
        self._client = chromadb.PersistentClient(path=path)
        self._name = collection

    def reset(self):
        try:
            self._client.delete_collection(self._name)
        except Exception:
            pass
        self._collection = self._client.get_or_create_collection(
            name=self._name, metadata={"hnsw:space": "cosine"}
        )

    def _coll(self):
        if not hasattr(self, "_collection"):
            self._collection = self._client.get_or_create_collection(
                name=self._name, metadata={"hnsw:space": "cosine"}
            )
        return self._collection

    def add(self, ids, embeddings, documents, metadatas):
        self._coll().add(ids=ids, embeddings=embeddings,
                         documents=documents, metadatas=metadatas)

    def query(self, embedding, k: int) -> list[dict]:
        res = self._coll().query(query_embeddings=[embedding], n_results=k)
        hits = []
        for i in range(len(res["ids"][0])):
            hits.append({
                "id": res["ids"][0][i],
                "document": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "score": 1.0 - res["distances"][0][i],
            })
        return hits
