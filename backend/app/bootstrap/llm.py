from app.rag.llm.groq_llm import GroqLLM

_llm = None


def get_llm():

    global _llm

    if _llm is None:

        _llm = GroqLLM()

    return _llm