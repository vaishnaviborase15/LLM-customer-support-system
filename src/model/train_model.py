import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier

# LOAD DATA
df = pd.read_csv("data/processed/final_ai_dataset.csv")

# Use cleaned text
X = df["clean_text"]

# Targets
y_sentiment = df["sentiment"]
y_response = df["suggested_response"]

df = df.dropna(subset=["clean_text", "sentiment", "suggested_response"])

# TRAIN SENTIMENT MODEL
sentiment_model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression())
])

sentiment_model.fit(X, y_sentiment)


# TRAIN RESPONSE MODEL
response_model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression())
])

response_model.fit(X, y_response)


# SAVE MODELS
os.makedirs("models", exist_ok=True)

with open("models/sentiment_model.pkl", "wb") as f:
    pickle.dump(sentiment_model, f)

with open("models/response_model.pkl", "wb") as f:
    pickle.dump(response_model, f)

print("Models trained and saved!")