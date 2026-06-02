# query.py
import sys
from voiceops_rag.config import load_config
from voiceops_rag.embeddings import OllamaEmbedder
from voiceops_rag.store import VectorStore
from voiceops_rag.llm import OllamaLLM
from voiceops_rag.rag import answer_question

def main():
    if len(sys.argv) < 2:
        print('Usage: python query.py "your question"')
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    cfg = load_config()
    result = answer_question(
        question,
        OllamaEmbedder(cfg.embed_model),
        VectorStore(cfg.chroma_path),
        OllamaLLM(cfg.llm_model),
        top_k=cfg.top_k, min_score=cfg.min_score,
    )
    print("\n" + result.answer + "\n")
    if result.sources:
        print("Sources:")
        for s in result.sources:
            print(f"  - {s['title']} ({s['source_file']}, score {s['score']})")

if __name__ == "__main__":
    main()
