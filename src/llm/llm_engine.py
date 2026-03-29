import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_llm_response(user_query):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db_path = os.path.join(BASE_DIR, "vector_db")
    db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)

    docs = db.similarity_search(user_query, k=1)

    if docs:
        response = docs[0].page_content
    else:
        response = "Our support team will assist you shortly."

    # Basic logic (same as your ML before)
    sentiment = "Neutral"
    priority = "Medium"

    return sentiment, priority, response