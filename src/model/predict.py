import pickle

# Load models once
with open("models/sentiment_model.pkl", "rb") as f:
    sentiment_model = pickle.load(f)

with open("models/response_model.pkl", "rb") as f:
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

    return sentiment, priority, response