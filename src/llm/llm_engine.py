import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# LOAD ONCE (GLOBAL)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db_path = os.path.join(BASE_DIR, "vector_db")

try:
    db = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("Vector DB loaded successfully")
except Exception as e:
    print("Error loading vector DB:", e)
    db = None


def get_llm_response(user_query):
    try:
        if db is None:
            return "Neutral", "Medium", "Support system initializing..."

        docs = db.similarity_search(user_query, k=1)

        if docs:
            response = docs[0].page_content
        else:
            response = "Our support team will assist you shortly."

        # FAST RULE-BASED (no extra delay)
        sentiment = "Neutral"
        priority = "Medium"

        if any(word in user_query.lower() for word in ["refund", "not working", "issue", "error", "failed"]):
            priority = "High"

        return sentiment, priority, response

    except Exception as e:
        return "Neutral", "Medium", "AI service temporarily unavailable"