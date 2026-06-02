import os
from dataclasses import dataclass

@dataclass
class Config:
    llm_model: str
    embed_model: str
    chroma_path: str
    top_k: int
    chunk_size: int
    chunk_overlap: int
    min_score: float

def load_config() -> Config:
    return Config(
        llm_model=os.getenv("VOICEOPS_LLM_MODEL", "llama3"),
        embed_model=os.getenv("VOICEOPS_EMBED_MODEL", "nomic-embed-text"),
        chroma_path=os.getenv("VOICEOPS_CHROMA_PATH", "./chroma_db"),
        top_k=int(os.getenv("VOICEOPS_TOP_K", "4")),
        chunk_size=int(os.getenv("VOICEOPS_CHUNK_SIZE", "1200")),
        chunk_overlap=int(os.getenv("VOICEOPS_CHUNK_OVERLAP", "150")),
        min_score=float(os.getenv("VOICEOPS_MIN_SCORE", "0.30")),
    )
