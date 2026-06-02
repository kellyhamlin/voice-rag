import ollama

class OllamaEmbedder:
    def __init__(self, model: str):
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        out = []
        for t in texts:
            resp = ollama.embeddings(model=self.model, prompt=t)
            out.append(resp["embedding"])
        return out

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]
