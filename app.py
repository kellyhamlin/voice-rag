# app.py
import streamlit as st
from voiceops_rag.config import load_config
from voiceops_rag.embeddings import OllamaEmbedder
from voiceops_rag.store import VectorStore
from voiceops_rag.llm import OllamaLLM
from voiceops_rag.rag import answer_question

st.set_page_config(page_title="VoiceOps RAG", page_icon="📞")
st.title("📞 VoiceOps Troubleshooting Assistant")
st.caption("Answers are grounded in indexed docs. If no source matches, it says so.")

@st.cache_resource
def _clients():
    cfg = load_config()
    return cfg, OllamaEmbedder(cfg.embed_model), VectorStore(cfg.chroma_path), OllamaLLM(cfg.llm_model)

cfg, embedder, store, llm = _clients()
question = st.text_input("Ask a voice/network troubleshooting question:")

if question:
    with st.spinner("Retrieving and answering..."):
        result = answer_question(question, embedder, store, llm,
                                 top_k=cfg.top_k, min_score=cfg.min_score)
    if result.grounded:
        st.success(result.answer)
        with st.expander(f"Sources ({len(result.sources)})"):
            for s in result.sources:
                st.markdown(f"**{s['title']}** — `{s['source_file']}` · score {s['score']}")
    else:
        st.warning(result.answer)
