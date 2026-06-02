from voiceops_rag.rag import answer_question, RagResult

class FakeEmbedder:
    def embed_one(self, text): return [1.0, 0.0]

class FakeStore:
    def __init__(self, hits): self._hits = hits
    def query(self, embedding, k): return self._hits[:k]

class FakeLLM:
    def __init__(self): self.called = False
    def chat(self, system, prompt):
        self.called = True
        self.last_prompt = prompt
        return "Check the SDP for codec mismatch."

GOOD_HITS = [{
    "id": "audio-1", "document": "One-way audio is usually NAT or codec.",
    "metadata": {"source_file": "one-way-audio.md", "title": "One-Way Audio"},
    "score": 0.82,
}]

def test_grounded_answer_calls_llm_and_returns_sources():
    llm = FakeLLM()
    result = answer_question(
        "why is audio one-way?", FakeEmbedder(), FakeStore(GOOD_HITS), llm,
        top_k=4, min_score=0.3,
    )
    assert isinstance(result, RagResult)
    assert result.grounded is True
    assert llm.called is True
    assert result.answer == "Check the SDP for codec mismatch."
    assert result.sources[0]["title"] == "One-Way Audio"
    # retrieved context must be in the prompt
    assert "One-way audio is usually NAT or codec." in llm.last_prompt

def test_low_score_refuses_without_calling_llm():
    llm = FakeLLM()
    weak = [dict(GOOD_HITS[0], score=0.10)]
    result = answer_question(
        "what is the capital of France?", FakeEmbedder(), FakeStore(weak), llm,
        top_k=4, min_score=0.3,
    )
    assert result.grounded is False
    assert llm.called is False
    assert "don't have a source" in result.answer.lower()
    assert result.sources == []

def test_no_hits_refuses():
    llm = FakeLLM()
    result = answer_question(
        "anything", FakeEmbedder(), FakeStore([]), llm, top_k=4, min_score=0.3,
    )
    assert result.grounded is False
    assert llm.called is False
