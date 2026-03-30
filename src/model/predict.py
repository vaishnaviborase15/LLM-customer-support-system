from src.llm.llm_engine import get_llm_response

def predict_all(text: str):
    return get_llm_response(text)
