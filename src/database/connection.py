import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 🔥 Paste your Render DB URL here for testing
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

print("🔥 DATABASE_URL:", DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found. Check your .env file!")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()