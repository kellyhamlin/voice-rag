from dataclasses import dataclass, field

SYSTEM_PROMPT = (
    "You are a voice/network troubleshooting assistant. Answer ONLY using the "
    "provided context. If the context is insufficient, say you don't know. "
    "Cite the source titles you used."
)

REFUSAL = ("I don't have a source for that. Try rephrasing, or this topic may "
           "not be covered by the indexed documents.")

@dataclass
class RagResult:
    answer: str
    sources: list = field(default_factory=list)
    grounded: bool = False

def _build_prompt(question: str, hits: list[dict]) -> str:
    blocks = []
    for h in hits:
        title = h["metadata"].get("title", h["metadata"].get("source_file", "?"))
        blocks.append(f"[Source: {title}]\n{h['document']}")
    context = "\n\n".join(blocks)
    return f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

def answer_question(question, embedder, store, llm, top_k: int, min_score: float) -> RagResult:
    q_vec = embedder.embed_one(question)
    hits = store.query(embedding=q_vec, k=top_k)
    if not hits or hits[0]["score"] < min_score:
        return RagResult(answer=REFUSAL, sources=[], grounded=False)
    prompt = _build_prompt(question, hits)
    answer = llm.chat(SYSTEM_PROMPT, prompt)
    sources = [{
        "title": h["metadata"].get("title"),
        "source_file": h["metadata"].get("source_file"),
        "score": round(h["score"], 3),
    } for h in hits]
    return RagResult(answer=answer, sources=sources, grounded=True)
