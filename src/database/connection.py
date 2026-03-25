from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL connection (XAMPP)
DATABASE_URL = "mysql+pymysql://root:@localhost/support_system"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()