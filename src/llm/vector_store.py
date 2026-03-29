import pandas as pd
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def create_vector_store():
    file_path = os.path.join(BASE_DIR, "data", "processed", "final_ai_dataset.csv")

    df = pd.read_csv(file_path)

    documents = []

    for _, row in df.iterrows():
        content = f"""
        Issue: {row.get('Ticket_Description', '')}
        Type: {row.get('Ticket_Type', '')}
        Response: {row.get('suggested_response', '')}
        """

        documents.append(Document(page_content=content))

    # FREE EMBEDDINGS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(documents, embeddings)

    db.save_local(os.path.join(BASE_DIR, "vector_db"))

    print("Vector DB Created Successfully")