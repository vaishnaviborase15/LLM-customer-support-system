import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "final_ai_dataset.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data
df = pd.read_csv(DATA_PATH)

texts = df['Ticket_Description'].fillna("").tolist()
responses = df['suggested_response'].fillna("").tolist()

# Create embeddings
embeddings = model.encode(texts)

# FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def retrieve_similar(query):
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, k=1)

    idx = indices[0][0]

    return texts[idx], responses[idx]