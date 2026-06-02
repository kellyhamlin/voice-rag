import ollama

class OllamaLLM:
    def __init__(self, model: str):
        self.model = model

    def chat(self, system: str, prompt: str) -> str:
        resp = ollama.chat(model=self.model, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ])
        return resp["message"]["content"]
