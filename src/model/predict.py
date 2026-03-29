"""
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sentiment_path = os.path.join(BASE_DIR, "models", "sentiment_model.pkl")
response_path = os.path.join(BASE_DIR, "models", "response_model.pkl")

with open(sentiment_path, "rb") as f:
    sentiment_model = pickle.load(f)

with open(response_path, "rb") as f:
    response_model = pickle.load(f)


def predict_all(text):
    sentiment = sentiment_model.predict([text])[0]
    response = response_model.predict([text])[0]

    # Priority logic
    if sentiment == "Negative":
        priority = "High"
    elif sentiment == "Neutral":
        priority = "Medium"
    else:
        priority = "Low"

    return sentiment, priority, response   """


from src.llm.llm_engine import get_llm_response

def parse_llm_output(result):
    sentiment = "Neutral"
    priority = "Medium"
    response = result

    try:
        lines = result.split("\n")

        for line in lines:
            if "sentiment" in line.lower():
                sentiment = line.split(":")[-1].strip()
            elif "priority" in line.lower():
                priority = line.split(":")[-1].strip()
            elif "response" in line.lower():
                response = line.split(":", 1)[-1].strip()

    except:
        pass

    return sentiment, priority, response


def predict_all(text):
    sentiment, priority, response = get_llm_response(text)
    return sentiment, priority, response