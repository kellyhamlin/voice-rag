# ingest.py
import glob, os
from voiceops_rag.config import load_config
from voiceops_rag.chunking import chunk_text
from voiceops_rag.embeddings import OllamaEmbedder
from voiceops_rag.store import VectorStore

def _title_for(path: str, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("title:"):
            return line.split("title:", 1)[1].strip()
    return os.path.basename(path)

def main():
    cfg = load_config()
    embedder = OllamaEmbedder(cfg.embed_model)
    store = VectorStore(cfg.chroma_path)
    store.reset()

    ids, embeddings, documents, metadatas = [], [], [], []
    for path in glob.glob("data/docs/*.md") + glob.glob("data/docs/*.txt"):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        title = _title_for(path, text)
        for i, chunk in enumerate(chunk_text(text, cfg.chunk_size, cfg.chunk_overlap)):
            ids.append(f"{os.path.basename(path)}::{i}")
            documents.append(chunk)
            metadatas.append({"source_file": os.path.basename(path), "title": title})

    print(f"Embedding {len(documents)} chunks...")
    embeddings = embedder.embed(documents)
    store.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print(f"Indexed {len(documents)} chunks from data/docs into {cfg.chroma_path}")

if __name__ == "__main__":
    main()
