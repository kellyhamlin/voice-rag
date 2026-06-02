markdown
# VoiceOps RAG

A local, citation-grounded RAG assistant that answers voice/network
troubleshooting questions from a document corpus — and **refuses to answer when
no source supports it**. Built with Ollama + ChromaDB. No cloud, no API keys.

> Clean-room project: the corpus is synthetic/public only. No proprietary data.

## How it works
Docs are chunked, embedded (`nomic-embed-text`), and stored in Chroma. A
question is embedded and matched to the nearest chunks; if the best match is
too weak, the assistant declines instead of guessing. Otherwise a local LLM
answers using only the retrieved context and cites its sources.

## Setup
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3 && ollama pull nomic-embed-text
python ingest.py
python query.py "why would a call have one-way audio?"   # CLI
streamlit run app.py                                      # web UI
```

## Tests
```bash
pytest -v
```

(screenshot/GIF here)
```
