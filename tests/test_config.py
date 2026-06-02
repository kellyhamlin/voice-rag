import os
from voiceops_rag.config import load_config

def test_defaults_when_env_absent(monkeypatch):
    for k in list(os.environ):
        if k.startswith("VOICEOPS_"):
            monkeypatch.delenv(k, raising=False)
    cfg = load_config()
    assert cfg.llm_model == "llama3"
    assert cfg.embed_model == "nomic-embed-text"
    assert cfg.top_k == 4
    assert cfg.chunk_size == 1200
    assert cfg.chunk_overlap == 150
    assert cfg.min_score == 0.54

def test_env_overrides(monkeypatch):
    monkeypatch.setenv("VOICEOPS_TOP_K", "7")
    monkeypatch.setenv("VOICEOPS_LLM_MODEL", "gemma")
    cfg = load_config()
    assert cfg.top_k == 7
    assert cfg.llm_model == "gemma"
